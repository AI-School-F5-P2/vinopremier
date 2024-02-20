from fastapi import FastAPI, HTTPException
import pandas as pd 
import pickle 
from pydantic import BaseModel
from typing import List
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from fastapi.responses import JSONResponse
from obtener_img import Vino
from filtrar_por_precio import FiltroPrecio


class Encontrar_vinos_similares:
    def __init__(self):
        self.df_completo = pd.read_csv('./Model/dataset_de_productos_completo.csv')
        pass

    def validar_tipo_vino_agotado(self, sku_vino):
        # Obtener el tipo de vino asociado al SKU
        tipo_vino_sku = self.df_completo.loc[self.df_completo['SKU'] == sku_vino, 'tipo_vino'].iloc[0]

        # Verificar si el tipo de vino es tinto, blanco o rosado
        tipos_validos = ['Vino Tinto', 'Vino Blanco', 'Vino Rosado']
        if tipo_vino_sku in tipos_validos:
            return False
        else:
            return True
    
    def encontrar_vinos_similares(self, sku, df):
        # PASAR A UNA DICT
        try:
            vinos_similares_list = []
            vino = Vino()
            vino_agotado = self.df_completo[self.df_completo['SKU'] == sku]
            # valido que el sku exista en dataframe
            if vino_agotado.empty:
                raise ValueError(f"El SKU {sku} no se encuentra en el DataFrame.")

            # valido que el sku sea del tipo de vino valido
            if self.validar_tipo_vino_agotado(sku):
                raise ValueError("El tipo de vino del vino seleccionado no es válido. Debe ser tinto, blanco o rosado.")
                
            categoricas = ['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino']
            numericas = ['final_price']
            
            # Cargar el modelo y objetos necesarios desde el archivo pickle
            with open('./Model/modelo2.pkl', 'rb') as f:
                knn_loaded, label_encoders_loaded, scaler_loaded = pickle.load(f)

            def obtener_numero_codificado(columna, valor_original):
                # Aplicar la transformación para obtener el número codificado
                numero_codificado = label_encoders_loaded[columna].transform([valor_original])[0]
                return numero_codificado

            # Extraer solo las características categóricas
            vino_agotado_categoricas = vino_agotado[categoricas]

            # Verifico si hay valores NaN en las características categóricas
            if vino_agotado_categoricas.isnull().any().any():
                raise ValueError("¡Hay valores NaN en las características del vino.!")

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

            vino_similar_indices = indices[0][:10]
            vino_similar = df.iloc[vino_similar_indices]
            
            # obtengo el porcentage de similitud
            similitudes_porcentaje = 1 / (1 + distancias)
            
            # Imprimir los porcentajes de similitud de los vinos más similares
            for indice, porcentaje in zip(indices[0], similitudes_porcentaje[0]):
                vino_similar = df.iloc[indice]  # Obtener el vino similar
                vino_similar['porcentage_similitud'] = f"{porcentaje:.2%}"
                if vino_similar['SKU'] != sku:
                    vinos_similares_list.append(vino_similar)

            # agrego la imagen a cada vino 
            vinos_similares_list = vino.img(vinos_similares_list)
               
            return vinos_similares_list
        
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        
        except Exception as e:
            # return con tipo de error 400 en mi return y un mensaje de error con la e
            return JSONResponse(content={"message": f"Hubo un problema al hacer la solicitud, Error: {e}"}, status_code=400)







