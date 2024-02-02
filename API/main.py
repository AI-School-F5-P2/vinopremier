from flask import Flask, request, jsonify
# from flask_limit import Limiter
import logging
import pickle 
import pandas as pd 
from sklearn.preprocessing import StandardScaler

# INSTANCIAMOS FLASK 
app = Flask(__name__)
logging.basicConfig(filename="./Model/app.log", level=logging.INFO)

# CARGAMOS EL MODELO
with open('./Model/knn_model.pkl', 'rb') as file:
    knn_model = pickle.load(file)

# CARGAMOS EL DATASET
data = pd.read_csv('./Model/data.csv')
df_vinos = data

features = data[['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino']]
# Convertir variables categóricas a variables dummy
features = pd.get_dummies(features)
# Normalizar los datos (opcional pero recomendado para KNN)
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)



features_train = pd.get_dummies(data[['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino']])
features_train_scaled = scaler.transform(features_train)


# Función para encontrar los vinos más similares a uno dado
def encontrar_vinos_similares(vino_id, features_train, n_vecinos=5):
    # Obtener las características del vino de interés
    # vino_interes = data.loc[data['SKU'] == vino_id, features_train]
    vino_interes = df_vinos.loc[df_vinos['SKU'] == vino_id, ['uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino', 'bodega']]
    vino_interes = pd.get_dummies(vino_interes)
    # Asegurarnos de que las columnas dummy coincidan con las del conjunto de entrenamiento
    vino_interes = vino_interes.reindex(columns=features.columns, fill_value=0)
    vino_interes_scaled = scaler.transform(vino_interes)

    # Encontrar los vecinos más cercanos usando el conjunto de entrenamiento
    _, indices_vecinos = knn_model.kneighbors(vino_interes_scaled)

    # Mostrar los n_vecinos más cercanos (excluyendo el propio vino)
    vinos_similares = data.iloc[indices_vecinos[0][:n_vecinos + 1]]['SKU']
    return vinos_similares

# RUTA
@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/wineRecommendation', methods=['POST'])
def wineRecommendation():
    try:
        result = None
        input_wine = request.args.get('wine')
        if not input_wine or input_wine == "" or input_wine is None:
            return jsonify({"Error al consultar vinos"}), 400
        if input_wine:
            result = encontrar_vinos_similares(input_wine, features_train_scaled, 5)
            result_list = result.tolist() if isinstance(result, pd.Series) else result
            return jsonify({"result": result_list}), 200
    except Exception as e:
        logging.error(e)
        return jsonify({"algo paso"}), 400


if __name__ == '__main__':
    app.run(host="", port="", debug=True)
