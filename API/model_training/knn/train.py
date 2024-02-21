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
from sklearn.model_selection import cross_val_score

df_sin_nulos = pd.read_csv('dataset_train/vinos_filtrados.csv')
# df_bodega = pd.read_csv('dataset/suppliers.csv')
# df_completo = pd.read_csv('dataset/dataset_de_productos_completo.csv')
# df_stock_limpio = pd.read_csv('dataset/df_stock_limpio.csv')

df_original = df_sin_nulos.copy()


df_original['nivel_de_relevancia'] = 0
df_original['porcentage_similitud'] = '0%'
df = df_sin_nulos
df_original

categoricas = ['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino']
numericas = ['final_price']

# ------------- LABEL ENCODE -------------
label_encoders = {}

# hago el label encode de cada columna por separado
for columna in categoricas:
    label_encoders[columna] = LabelEncoder()
    df[columna] = label_encoders[columna].fit_transform(df[columna])

# DataFrame con las características categóricas
df_cat = df[categoricas].copy()
# agrego las variables numericas
df_cat[numericas] = df[numericas]

# hago el escalado de todos los atributos
scaler = MinMaxScaler()
df_cat = scaler.fit_transform(df_cat)

# ----------- ENTRENAR MODELO ------------

X = df_cat
knn = NearestNeighbors(n_neighbors=10)
knn.fit(X)


# Guardar el modelo y los objetos LabelEncoder y MinMaxScaler en un archivo pickle
with open('models/modelo_knn_v1.pkl', 'wb') as f:
    pickle.dump((knn, label_encoders, scaler), f)