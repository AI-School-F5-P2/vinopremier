import pandas as pd

class Plan_marketin:
    def __init__(self,):
        pass

    def filtrar_vinos_con_plan_marketing(self, vinos_con_precio_mas_similar, df_bodega, df_vinos):

        if vinos_con_precio_mas_similar == []:
            print('No hay vinos con precio similares, por lo tanto no se puede verificar si tienen plan de marketin')
            return []
        
        bodegas_con_plan = df_bodega[df_bodega['plan_marketing_enabled'] == 1]['name']

        vinos_con_pla_marketing = []

        for vino_similar in vinos_con_precio_mas_similar:
            sku_vino_similar = vino_similar['SKU']
            proveedor = df_vinos[df_vinos['SKU'] == sku_vino_similar]['proveedor'].values
            print
            if proveedor in bodegas_con_plan.values:
                vinos_con_pla_marketing.append(vino_similar)
            else:
                print('no se encontro vino con plan marketin')
                
        return vinos_con_pla_marketing