import pandas as pd

class Vino():
    def __init__(self) -> None:
        self.df_sku_image = pd.read_csv('./Model/dataset_sku_image.csv')
     
    def img(self, sku_list):
        vinos_con_img_list = []
        for vino in sku_list:
            sku = vino['SKU']
            img_url = self.df_sku_image[self.df_sku_image['SKU'] == sku]['image'].iloc[0]
            vino['url_img'] = img_url
            vinos_con_img_list.append(vino)

        return vinos_con_img_list
        




