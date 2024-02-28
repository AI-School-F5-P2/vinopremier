from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from fastapi.responses import JSONResponse
from obtener_img import Vino
from filtrar_por_precio import FiltroPrecio
from buscar_vinos_similares_con_knn import Encontrar_vinos_similares
from buscar_vinos_similares_con_embeding import Predictor
from verificar_plan_marketin import Plan_marketin
from aplicar_relevancia import PuntuadorDeVinos
from fastapi.middleware.cors import CORSMiddleware
from obtener_solo_vino_agotado import VinoAgotado

# INSTANCIA DE FASTAPI
app = FastAPI()
encontrar_vino = Encontrar_vinos_similares()
encontrar_vino_similare_con_m_embeding = Predictor()
filtar = FiltroPrecio()
plan_marketin = Plan_marketin()
puntuadorDeVinos = PuntuadorDeVinos()
obtener_vino_agotado = VinoAgotado()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Encabezados permitidos
)

df = pd.read_csv('./model_training/knn/dataset_train/vinos_filtrados.csv')
df_bodega = pd.read_csv('dataset/suppliers.csv')
df_completo = pd.read_csv('dataset/dataset_de_productos_completo.csv')

class sku(BaseModel):
    SKU: str

# RUTA
@app.get("/")
def read_root():
    return {"Hello": "World"}

#MODELO KNN
@app.post("/wineRecommendation")
def encontrar_vinos_similares(sku: sku):
    try:  
        sku = sku.SKU
        vinos_similares_list = encontrar_vino.encontrar_vinos_similares(sku, df)
        vinos_con_precio_mas_similar =  filtar.filtrar_por_precio(sku, vinos_similares_list, df)
        vinos_con_plan_marketin = plan_marketin.filtrar_vinos_con_plan_marketing(vinos_con_precio_mas_similar, df_bodega, df)
        # unifico los vinos con plan de marketing y precio similares en un solo diccionario
        # para luego pasárselo a la función que va a puntuar con su nivel de relevancia
        vinos_precio_y_marketing = {'precio': vinos_con_precio_mas_similar, 'marketin': vinos_con_plan_marketin}
        # aplico el nivel de relevancia 
        vinos_con_relevancia = puntuadorDeVinos.asignar_puntos_de_relevancia(vinos_precio_y_marketing, vinos_similares_list)
        # elimino la descripción de los vinos
        for vino in vinos_con_relevancia:
            if 'description' in vino:
                del vino['description']
        return  vinos_similares_list
    
    except KeyError:
        raise HTTPException(status_code=404, detail="SKU no encontrado")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    



# # MODELO EMBEDING
@app.post("/obtener_vinos_similares_con_m_embeding/")
def obtener_vinos_similares_con_m_embeding(sku: sku):
    try:
        sku = sku.SKU
        vinos_similares_list = encontrar_vino_similare_con_m_embeding.predecir_vinos_similares_con_m_embeding(sku)
        vinos_con_precio_mas_similar =  filtar.filtrar_por_precio(sku, vinos_similares_list, df)
        vinos_con_plan_marketin = plan_marketin.filtrar_vinos_con_plan_marketing(vinos_similares_list, df_bodega, df)
        # unifico los vinos con plan de marketing y precio similares en un solo diccionario
        # para luego pasárselo a la función que va a puntuar con su nivel de relevancia
        vinos_precio_y_marketing = {'precio': vinos_con_precio_mas_similar, 'marketin': vinos_con_plan_marketin}
        # aplico el nivel de relevancia 
        vinos_con_relevancia = puntuadorDeVinos.asignar_puntos_de_relevancia(vinos_precio_y_marketing, vinos_similares_list)  
        # elimino la descripción de los vinos
        for vino in vinos_con_relevancia:
            if 'description' in vino:
                del vino['description']
        # return  vinos_con_precio_mas_similar 
        return vinos_con_relevancia
    except KeyError:
        raise HTTPException(status_code=404, detail="SKU no encontrado")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    


@app.get("/vino_agotado/{sku}")
def vino_agotado(sku: str):
    vino = obtener_vino_agotado.obtener_vino_agotado(sku, df_completo)
    return vino



