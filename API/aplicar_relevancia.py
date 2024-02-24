class PuntuadorDeVinos:
    def __init__(self, puntos_por_precio=8, puntos_por_plan_de_marketing=1):
        self.puntos_por_precio = puntos_por_precio
        self.puntos_por_plan_de_marketing = puntos_por_plan_de_marketing


    def asignar_puntos_de_relevancia(self, vinos_precio_y_marketin, vinos_similares):

        sku_vinos_con_plan_marketin = []
        sku_vinos_con_precio_mas_similar = []

        for vino_precio_y_marketin_key, vino_precio_y_marketin_value in vinos_precio_y_marketin.items():
            if vino_precio_y_marketin_key == 'precio':
                # agrego solo los sku a la lista de sku de vinos con precio similar
                sku_vinos_con_precio_mas_similar.extend(v['SKU'] for v in vino_precio_y_marketin_value)
            if vino_precio_y_marketin_key == 'marketin':
                sku_vinos_con_plan_marketin.extend(m['SKU'] for m in vino_precio_y_marketin_value)

        data_con_relevancia = []

        if not vinos_precio_y_marketin['marketin'] and not vinos_precio_y_marketin['precio']:
            return data_con_relevancia


        for vino_similar in vinos_similares:
            sku_vino_similar = vino_similar['SKU']
            relevancia = 0
            if sku_vino_similar in sku_vinos_con_plan_marketin:
                relevancia += 1  # Si hay marketing, sumamos 2 puntos
            if sku_vino_similar in sku_vinos_con_precio_mas_similar:
                relevancia += 8  # Si hay precio similar, sumamos 1 punto

            vino_similar['nivel_relevancia'] = relevancia
            # Agregamos el SKU con su puntuación de relevancia
            data_con_relevancia.append(vino_similar)

        # Ordenamos la lista de mayor a menor puntuación de relevancia
        data_con_orden_de_relevancia = sorted(data_con_relevancia, key=lambda x: x['nivel_relevancia'], reverse=True)

        return data_con_orden_de_relevancia