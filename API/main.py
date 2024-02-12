from fastapi import FastAPI
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from fastapi.responses import JSONResponse
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

        vino_similar_indices = indices[0]
        vino_similar = df.iloc[vino_similar_indices]
        vino_similar = vino_similar[vino_similar['SKU'] != sku.SKU]

        return vino_similar.to_dict(orient='records')
        
        # return vino_agotado
    except Exception as e:
        # return con tipo de error 400 en mi return y un mensaje de error con la e
        return JSONResponse(content={"message": f"Hubo un problema al hacer la solicitud, Error: {e}"}, status_code=400)

