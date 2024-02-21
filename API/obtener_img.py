import pandas as pd

class Vino():
    def __init__(self) -> None:
        self.df_sku_image = pd.read_csv('dataset/dataset_sku_image.csv')
     
    def img(self, vinos_similares_list):

        vinos_con_img_list = []
        for vino_similar in vinos_similares_list:
            sku = vino_similar['SKU']
            img_url = self.df_sku_image[self.df_sku_image['SKU'] == sku]['image'].iloc[0]
            vino_similar['url_img'] = img_url
            vinos_con_img_list.append(vino_similar)

        return vinos_con_img_list
        




