from fastapi import FastAPI
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# INSTANCIA DE FASTAPI
app = FastAPI()

# CARGAMOS EL DATASET
df = pd.read_csv('./Model/dataset_vinos.csv')

class data_vino(BaseModel):
    SKU: List[str]
    name: List[str]
    uvas: List[str]
    añada: List[str]
    DO : List[str]
    tipo_crianza: List[str]
    meses_barrica: List[str]
    tipo_vino: List[str]
    bodega: List[str]
    final_price: List[float]

# RUTA
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/prueba")
def encontrar_vinos_similares(data_vino: data_vino):
    # PASAR A UNA DICT
    data_vino = data_vino.dict()
    categoricas = ['uvas', 'añada', 'DO', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'bodega']
    numericas = ['final_price']
    
    # Cargar el modelo y objetos necesarios desde el archivo pickle
    with open('./Model/modelo.pickle', 'rb') as f:
        knn_loaded, label_encoders_loaded, scaler_loaded = pickle.load(f)

    def obtener_numero_codificado(columna, valor_original):
        # Aplicar la transformación para obtener el número codificado
        numero_codificado = label_encoders_loaded[columna].transform([valor_original])[0]
        return numero_codificado
    
    # Generar un dataframe con todos los atributos
    vino_agotado = pd.DataFrame(data_vino)
    # Generar un dataframe con todos los atributos
    #vino_agotado = pd.DataFrame(data_vino)

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
   
    

    vino_similar_indices = indices[0]
    vino_similar = df.iloc[vino_similar_indices]

    # Descartar el mismo vino que se pasa a la función
    vino_similar = vino_similar[vino_similar['SKU'] != data_vino['SKU'][0]]
    
    return vino_similar.to_dict(orient='records')
 