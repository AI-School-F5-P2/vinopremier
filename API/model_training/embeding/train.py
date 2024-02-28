import os
import pandas as pd
import pickle
import re
import html
from gensim.models import Word2Vec

class EntrenadorModeloWord2Vec:
    def __init__(self, ruta_datos):
        self.df = pd.read_csv(ruta_datos)
        self.directorio_modelos = "models/"
        os.makedirs(self.directorio_modelos, exist_ok=True)

    def limpiar_html_en_lista(self, elemento):
        elemento_sin_html = html.unescape(elemento)
        elemento_sin_html = re.sub(r'<.*?>', '', elemento_sin_html)
        return elemento_sin_html

    def entrenar_modelos_word2vec(self):
        tipos_de_vino = self.df['tipo_vino'].unique()
        
        for tipo_de_vino in tipos_de_vino:
            name_tipo_vino = tipo_de_vino
            df_tipo_vino = self.df[self.df['tipo_vino'] == name_tipo_vino]

            descripcion_vino = df_tipo_vino[['description']]
            descripcion_vino.fillna('', inplace=True) 
            descripcion_vino = descripcion_vino['description'].str.lower()

            corpus = [[palabra.lower() for palabra in descripcion.split()] for descripcion in descripcion_vino]
            model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)
            model.save(os.path.join(self.directorio_modelos, f'modelo_word2vec_{name_tipo_vino}.pkl'))

            caracteristicas_del_vino = df_tipo_vino[['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'proveedor', 'final_price']]
            caracteristicas_del_vino.fillna('', inplace=True)

            df_tipo_vino['caracteristicas_combinada'] = caracteristicas_del_vino.apply(
                lambda row: ' '.join([str(row[col]) for col in caracteristicas_del_vino.columns]),
                axis=1
            )

            caracteristicas_combinada_dict = df_tipo_vino[['SKU', 'caracteristicas_combinada']].to_dict(orient='records')
            sku_y_descripcion_combinada_dict = [{"SKU": vino['SKU'], "descripcion": vino['caracteristicas_combinada'].lower()} for vino in caracteristicas_combinada_dict]

            ruta_archivo = os.path.join(self.directorio_modelos, f'modelo_word2vec_{name_tipo_vino}.pkl')

            with open(ruta_archivo, 'wb') as f:
                pickle.dump((model, sku_y_descripcion_combinada_dict), f)

if __name__ == "__main__":
    entrenador = EntrenadorModeloWord2Vec('dataset_train/vinos_filtrados.csv')
    entrenador.entrenar_modelos_word2vec()
