class FiltroPrecio:
    def __init__(self):
        pass

    def filtrar_por_precio(self, vino_id_agotado, vinos_similares_list, df):
        results = self.filtrar(vino_id_agotado, vinos_similares_list, df, 0.2, 0.05)

        if len(results) < 1:
            print('no se encontraron vinos con precios en el rango de 0.2 y 0.05')
            results = self.filtrar(vino_id_agotado, vinos_similares_list, df, 0.2, 0.3)  

        return results
        

    
    def filtrar(self, vino_id_agotado, vinos_similares_list, df, p_min, p_max):
        try:
            matches = []
            # obtener el precio del vino
            precio_vino = df[df['SKU'] == vino_id_agotado]['final_price'].values[0]
            # calcular el mínimo y el máximo
            porcentaje_por_encima = p_min #0.2
            porcentaje_por_debajo = p_max #0.05
            precio_min = abs(precio_vino * porcentaje_por_debajo - precio_vino)
            precio_max = precio_vino * porcentaje_por_encima + precio_vino
            
            for vino_similar in vinos_similares_list:
                sku_vino_similar = vino_similar['SKU']
                # Verificar si el ID del vino está presente en el dataframe
                if sku_vino_similar in df['SKU'].values:
                    vino = df[df['SKU'] == sku_vino_similar]
                    precio_del_vino = vino['final_price'].values[0]
                    
                    if precio_min <= precio_del_vino <= precio_max:
                        matches.append(vino_similar)
                        
                else:
                    print(f"El vino con SKU {sku_vino_similar} no se encuentra en el dataframe.")
            results = matches 
            return results
        except IndexError:
            raise ValueError("Índice fuera de rango al acceder al precio del vino en el DataFrame.")
        except KeyError:
            raise ValueError("La columna 'SKU' no existe en el DataFrame.")

    


