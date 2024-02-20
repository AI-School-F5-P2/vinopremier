from fastapi import FastAPI, HTTPException
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from fastapi.responses import JSONResponse
from obtener_img import Vino
from filtrar_por_precio import FiltroPrecio


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from heapq import nlargest

import re
from bs4 import BeautifulSoup
import html
from gensim.models import Word2Vec


class Predictor:
    def __init__(self):
        # Carga de datos y modelo al inicializar la clase
        self.df_con_descripcion_combinada = pd.read_csv('Modelo_con_embeding/dataset_vinos_para_modelo_embeding.csv')
        self.df_original_completo = pd.read_csv('Modelo_con_embeding/dataset_de_productos_completo.csv')
        with open('modelo_con_embeding/modelo_embeding_v1.pkl', 'rb') as f:
            self.model, self.sku_decripcion_combinada_list = pickle.load(f)
        
    def limpiar_html_en_lista(self, elemento):
        elemento_sin_html = html.unescape(elemento)
        elemento_sin_html = re.sub(r'<.*?>', '', elemento_sin_html)
        return elemento_sin_html
    
    def predecir_vinos_similares_con_m_embeding(self, sku):
        vino_img = Vino()
        descripcion_entrada = self.df_original_completo[self.df_original_completo['SKU'] == sku].copy()

        descripcion_entrada['description'] = descripcion_entrada['description'].apply(self.limpiar_html_en_lista)

        caracteristicas = descripcion_entrada[['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'proveedor', 'final_price']]
        descripcion_entrada.fillna('', inplace=True)


        descripcion_entrada['descripcion_combinada'] = caracteristicas.apply(
            lambda row: ' '.join([str(row[col]) for col in caracteristicas.columns]),
            axis=1

        )

        descripcion_entrada = descripcion_entrada['descripcion_combinada'].iloc[0]

        tokens_entrada = descripcion_entrada.lower().split()
        vector_entrada = np.mean([self.model.wv[token] for token in tokens_entrada if token in self.model.wv], axis=0)

        similitudes = []
        for vino in self.sku_decripcion_combinada_list:
            tokens_vino = vino["descripcion"].lower().split()
            vector_vino = np.mean([self.model.wv[token] for token in tokens_vino if token in self.model.wv], axis=0)
            # Normalizar vector de vino
            # vector_vino /= np.linalg.norm(vector_vino)
            similitud = cosine_similarity([vector_entrada], [vector_vino])[0][0]
            similitudes.append((vino["SKU"], similitud))

        vino_similar = max(similitudes, key=lambda x: x[1])
        top_10_vinos_similares = nlargest(10, similitudes, key=lambda x: x[1])

        vinos_predichos = []
        for vino in top_10_vinos_similares:
            vino_predicho = self.df_con_descripcion_combinada[self.df_con_descripcion_combinada['SKU'] == vino[0]].copy()
            vino_predicho['porcentage_similitud'] = vino[1]
            vinos_predichos.append(vino_predicho.to_dict(orient='records')[0])
        
        # Agrego la imagen a cada vino 
        vinos_predichos = vino_img.img(vinos_predichos)

        return vinos_predichos[1:]