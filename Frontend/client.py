import streamlit as st
import requests
from PIL import Image
from io import BytesIO

class SKU:
    def __init__(self, SKU):
        self.SKU = SKU

def obtener_productos_similares(sku):
    url = "http://localhost:8000/wineRecommendation"
    response = requests.post(url, json=sku.__dict__)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(response.json())
        mensaje = response.json()
        mensaje = {'error':mensaje['detail']}
        return mensaje

def mostrar_descripcion_producto(producto):
    st.write(f"Nombre: {producto['name']}")
    st.write(f"Uvas: {producto['uvas']}")
    st.write(f"Añada: {producto['añada']}")
    st.write(f"DO: {producto['D.O.']}")
    st.write(f"Tipo de crianza: {producto['tipo_crianza']}")
    st.write(f"Meses de barrica: {producto['meses_barrica']}")
    st.write(f"Tipo de vino: {producto['tipo_vino']}")
    st.write(f"proveedor: {producto['proveedor']}")
    st.write(f"Precio: ${producto['final_price']}")
    # Agrega aquí cualquier otra información que se desee mostrar

def mostrar_descripcion_recomendacion(producto):
    # st.write(f"SKU: {producto['SKU']}")
    st.write(f"Nombre: {producto['name']}")
    st.write(f"Uvas: {producto['uvas']}")
    st.write(f"Añada: {producto['añada']}")
    st.write(f"DO: {producto['D.O.']}")
    st.write(f"Tipo de crianza: {producto['tipo_crianza']}")
    st.write(f"Meses de barrica: {producto['meses_barrica']}")
    st.write(f"Tipo de vino: {producto['tipo_vino']}")
    st.write(f"proveedor: {producto['proveedor']}")
    st.write(f"Precio: ${producto['final_price']}")
    # Agrega aquí cualquier otra información que se desee mostrar

def main():
    st.set_page_config(
        page_title="Vinopremier Recomendación de Vinos",
        page_icon="🍷",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Vinopremier Recomendación🍷")

    # Interfaz de Streamlit para ingresar el SKU del producto
    sku_input = st.text_input("Ingrese el SKU del producto:")

    if sku_input:
        # Instancia de la clase SKU con el SKU proporcionado
        sku_obj = SKU(SKU=sku_input)
        # Llamada a la función para obtener productos similares
        productos_similares = obtener_productos_similares(sku_obj)

        if 'error' in productos_similares:
            st.error(f"Error al obtener productos similares: {productos_similares['error']}")
            return
                

        if productos_similares:
            # Muestra la imagen y la descripción del producto original
            st.write("Producto Original:")

            imagen_url_original = productos_similares[0].get('url_img', '')
            if imagen_url_original:
                try:
                    response = requests.get(imagen_url_original)
                    response.raise_for_status()
                    imagen_original = Image.open(BytesIO(response.content))
                    # Muestra la imagen en un tamaño específico pudiendose ampliar o no
                    col1, col2 = st.columns([1, 2])
                    col1.image(imagen_original, caption=f"SKU: {sku_input}", width=200)
                except Exception as e:
                    st.write(f"Error al descargar la imagen para SKU: {sku_input}. Detalles: {str(e)}")
            else:
                st.write(f"URL de imagen no proporcionada para SKU: {sku_input}")

            # Muestra la descripción del producto original al lado de la imagen
            with col2:
                st.write("Descripción del Producto Original:")
                mostrar_descripcion_producto(productos_similares[0])

            # Muestra las imágenes y descripciones de las recomendaciones en filas
            st.write("\nRecomendaciones de Vinos:")

            # Utiliza una estructura de cuadrícula para mostrar las recomendaciones en columnas
            col_recomendaciones = st.columns(len(productos_similares))

            for i, producto in enumerate(productos_similares[1:], start=1):
                with col_recomendaciones[i-1]:
                    st.write(f"Recomendación {i}:")

                    # Muestra la imagen de la recomendación
                    imagen_url_recomendacion = producto.get('url_img', '')
                    if imagen_url_recomendacion:
                        try:
                            response = requests.get(imagen_url_recomendacion)
                            response.raise_for_status()
                            imagen_recomendacion = Image.open(BytesIO(response.content))
                            # Muestra la imagen en un tamaño específico
                            st.image(imagen_recomendacion, caption=f"SKU: {producto['SKU']}", width=150)
                        except Exception as e:
                            st.write(f"Error al descargar la imagen para SKU: {producto['SKU']}. Detalles: {str(e)}")
                    else:
                        st.write(f"URL de imagen no proporcionada para SKU: {producto['SKU']}")

                    # Muestra la descripción de la recomendación debajo de la imagen
                    # st.write("Descripción de la Recomendación:")
                    mostrar_descripcion_recomendacion(producto)
                    st.markdown("---")  # Agrega un separador entre las recomendaciones

if __name__ == "__main__":
    main()