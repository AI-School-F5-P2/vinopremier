from fastapi import FastAPI
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from fastapi.responses import JSONResponse
from obtener_img import Vino
# INSTANCIA DE FASTAPI
app = FastAPI()

# CARGAMOS EL DATASET
df = pd.read_csv('./Model/dataset_vinos.csv')

class sku(BaseModel):
    SKU: str

# RUTA
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/wineRecommendation")
def encontrar_vinos_similares(sku:sku):
    # PASAR A UNA DICT
    try:
        vino = Vino()
        vino_agotado = df[df['SKU'] == sku.SKU]

        categoricas = ['uvas', 'añada', 'DO', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'bodega']
        numericas = ['final_price']
        
        # Cargar el modelo y objetos necesarios desde el archivo pickle
        with open('./Model/modelo.pickle', 'rb') as f:
            knn_loaded, label_encoders_loaded, scaler_loaded = pickle.load(f)

        def obtener_numero_codificado(columna, valor_original):
            # Aplicar la transformación para obtener el número codificado
            numero_codificado = label_encoders_loaded[columna].transform([valor_original])[0]
            return numero_codificado
        

        # Extraer solo las características categóricas
        vino_agotado_categoricas = vino_agotado[categoricas]

        # Aplicar la función obtener_numero_codificado a las características categóricas de data_vino
        # para recuperar los números con los que se codificó anteriormente al hacer el entrenamiento del modelo
        for columna in categoricas:
            vino_agotado_categoricas.loc[:, columna] = obtener_numero_codificado(columna, vino_agotado_categoricas[columna].iloc[0])

        # Agregar las variables numéricas
        vino_agotado_categoricas[numericas] = vino_agotado[numericas]

        # Escalar todos los atributos
        vino_agotado_scaled = scaler_loaded.transform(vino_agotado_categoricas)

        # Realizar predicciones
        vino_agotado_codificado = vino_agotado_scaled.reshape(1, -1) # Reshape para satisfacer las dimensiones esperadas
        distancias, indices = knn_loaded.kneighbors(vino_agotado_codificado)
        
        indices = indices.tolist()

        vino_similar_indices = indices[0][:15]
        vino_similar = df.iloc[vino_similar_indices]
        # filtro que no se muestre el mismo vino agotado
        vino_similar = vino_similar[vino_similar['SKU'] != sku.SKU]
        sku_vino_similar_dict = vino_similar['SKU']
        sku_ordenados_por_precios = filtrar_por_precio(sku.SKU, sku_vino_similar_dict)
        
        # obtengo las filas del DataFrame
        filas_seleccionadas_list = df.loc[df['SKU'].isin(sku_ordenados_por_precios)].to_dict('records')
        # le agrego la imagen a todas las filas seleccionadas
        filas_seleccionadas_list = vino.img(filas_seleccionadas_list)

        return filas_seleccionadas_list
        
        # return vino_agotado
    except Exception as e:
        # return con tipo de error 400 en mi return y un mensaje de error con la e
        return JSONResponse(content={"message": f"Hubo un problema al hacer la solicitud, Error: {e}"}, status_code=400)










# esta funcion ordena primero los vinos que si estan en el rango de precios
# y los que no los pone de ultimo
def filtrar_por_precio(vino_id, vinos_similares_id):
    matches = []
    no_matches = []
    # obtener el precio del vino
    precio_vino = df[df['SKU'] == vino_id]['final_price'].values[0]

    # calcular el mínimo y el máximo
    porcentaje_por_encima = 0.2
    porcentaje_por_debajo = 0.05
    precio_min = abs(precio_vino * porcentaje_por_debajo - precio_vino)
    precio_max = precio_vino * porcentaje_por_encima + precio_vino

    for id_vino in vinos_similares_id:
        # Verificar si el ID del vino está presente en el dataframe
        if id_vino in df['SKU'].values:
            vino = df[df['SKU'] == id_vino]
            precio_del_vino = vino['final_price'].values[0]
            if precio_min <= precio_del_vino <= precio_max:
                matches.append(vino['SKU'].values[0])
            else:
                no_matches.append(vino['SKU'].values[0])
        else:
            print(f"El vino con SKU {id_vino} no se encuentra en el dataframe.")

    
    results = matches

    return results

