from heapq import nlargest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import pandas as pd
import pickle
import re
from bs4 import BeautifulSoup
import html
from obtener_img import Vino


from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Predictor:
    def __init__(self):
        self.ruta_modelos = 'model_training/embeding/models'
        self.df_original_completo = pd.read_csv('dataset/dataset_de_productos_completo.csv')
        self.df = pd.read_csv('model_training/embeding/dataset_train/vinos_filtrados.csv')

    def validar_tipo_vino_agotado(self, sku_vino):
        # Obtener el tipo de vino asociado al SKU
        tipo_vino_sku = self.df_original_completo.loc[self.df_original_completo['SKU'] == sku_vino, 'tipo_vino'].iloc[0]

        # Verificar si el tipo de vino es tinto, blanco o rosado
        tipos_validos = ['Vino Tinto', 'Vino Blanco', 'Vino Rosado']
        if tipo_vino_sku in tipos_validos:
            return False
        else:
            return True

    def cargar_modelo_word2vec(self, sku):
        vino_agotado = self.df_original_completo[self.df_original_completo['SKU'] == sku]
        
        if vino_agotado.empty:
            raise ValueError(f"El SKU {sku} no se encuentra en el DataFrame.")

            # valido que el sku sea del tipo de vino valido
        if self.validar_tipo_vino_agotado(sku):
            raise ValueError("El tipo de vino del vino seleccionado no es válido. Debe ser tinto, blanco o rosado.")

        tipo_vino_agotado = vino_agotado['tipo_vino'].iloc[0]

        if tipo_vino_agotado == 'Vino Blanco':
            nombre_del_modelo = 'modelo_word2vec_Vino Blanco.pkl'
        elif tipo_vino_agotado == 'Vino Tinto':
            nombre_del_modelo = 'modelo_word2vec_Vino Tinto.pkl'
        elif tipo_vino_agotado == 'Vino Rosado':
            nombre_del_modelo = 'modelo_word2vec_Vino Rosado.pkl'

        modelo_a_usar = f'{self.ruta_modelos}/{nombre_del_modelo}'
        
        with open(modelo_a_usar, 'rb') as f:
            model, sku_decripcion_combinada_list = pickle.load(f)
        
        return model, sku_decripcion_combinada_list, vino_agotado

    def predecir_vinos_similares_con_m_embeding(self, sku):

        vino_img = Vino()
        model, sku_decripcion_combinada_list, vino_agotado = self.cargar_modelo_word2vec(sku)

        df_caracteristicas = vino_agotado[['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'final_price']]
        df_caracteristicas.fillna('', inplace=True)
        df_caracteristicas['caracteristicas_combinada'] = df_caracteristicas.apply(
            lambda row: ' '.join([str(row[col]) for col in df_caracteristicas.columns]),
            axis=1
        )
        caracteristicas_combinada = df_caracteristicas['caracteristicas_combinada'].iloc[0]

        tokens_entrada = caracteristicas_combinada.lower().split()
        vector_entrada = np.mean([model.wv[token] for token in tokens_entrada if token in model.wv], axis=0)

        similitudes = []
        for vino in sku_decripcion_combinada_list:
            tokens_vino = vino["descripcion"].lower().split()
            vector_vino = np.mean([model.wv[token] for token in tokens_vino if token in model.wv], axis=0)
            similitud = cosine_similarity([vector_entrada], [vector_vino])[0][0]
            similitudes.append((vino["SKU"], similitud))

        top_10_vinos_similares = nlargest(10, similitudes, key=lambda x: x[1])
        vinos_predichos = []
        for vino in top_10_vinos_similares:
            vino_predicho = self.df[self.df['SKU'] == vino[0]]
            vino_predicho['porcentage_similitud'] = vino[1]
            vinos_predichos.append(vino_predicho.to_dict(orient='records')[0])

        vinos_predichos = vinos_predichos[1:]
        vinos_predichos = vino_img.img(vinos_predichos)
        
        return  vinos_predichos # Excluir el primer vino que es el mismo agotado
    






# if __name__ == "__main__":
#     sistema_recomendacion = Predictor()
#     vinos_recomendados = sistema_recomendacion.predecir_vinos_similares_con_m_embeding('arzuagareserva')
#     print(vinos_recomendados)