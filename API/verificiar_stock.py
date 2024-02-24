import pandas as pd

class Veririficar_stock():
    def __init__(self) -> None:
        self.df_stock_limpio = pd.read_csv('dataset/df_stock_limpio.csv')

    def verificar(self,vinos_similares):
        vinos_en_stock_array = []
        vino = vinos_similares[0]
        for vino_similar in vinos_similares:
            sku_vino_similar = vino_similar['SKU']
            if sku_vino_similar in self.df_stock_limpio['sku'].values:
                vinos_en_stock_array.append(vino_similar)
        return vinos_en_stock_array
    




# stock = Veririficar_stock()
# stock.verificar()
    
# vinos_en_stock_array = []

# for sku_vino_similar in vino_similar['SKU']:
#     if sku_vino_similar in df_stock_limpio['sku'].values:
#         vinos_en_stock_array.append(sku_vino_similar)