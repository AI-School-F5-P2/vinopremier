import pandas as pd

class Plan_marketin:
    def __init__(self,):
        pass

    def filtrar_vinos_con_plan_marketing(self, vinos_similares, df_bodega, df_vinos):
        bodegas_con_plan = df_bodega[df_bodega['plan_marketing_enabled'] == 1]['name']
        vinos_con_pla_marketing = []

        for vino_similar in vinos_similares:
            sku_vino_similar = vino_similar['SKU']
            proveedor = df_vinos[df_vinos['SKU'] == sku_vino_similar]['proveedor'].values
            if proveedor in bodegas_con_plan.values:
                vinos_con_pla_marketing.append(vino_similar)
                
        return vinos_con_pla_marketing