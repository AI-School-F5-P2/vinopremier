import numpy as np


class VinoAgotado:
    def __init__(self):

        pass

    def obtener_vino_agotado(self, sku, df_completo):
        vino_agotado = df_completo[df_completo['SKU'] == sku]
        vino_agotado = vino_agotado[['SKU','name','uvas', 'añada', 'D.O.', 'tipo_crianza', 'meses_barrica', 'tipo_vino','final_price', 'proveedor', 'image']]
        
        # VALIDACIONES
        if vino_agotado.empty:
            raise ValueError(f"El SKU {sku} no se encuentra en el DataFrame.")
        # Validar el tipo de vino
        if self.validar_tipo_vino_agotado(sku, df_completo):
            raise ValueError("El tipo de vino del vino seleccionado no es válido. Debe ser tinto, blanco o rosado.")
        if vino_agotado.isnull().any().any():
            raise ValueError("¡Hay valores NaN en las características del vino!")
        
        # vino_agotado.fillna(0, inplace=True)  # Reemplazar NaN con 0
        # vino_agotado = vino_agotado.replace([np.inf, -np.inf], np.nan).dropna()  # Eliminar filas con infinitos
        
        return vino_agotado.to_dict(orient='records')



    def validar_tipo_vino_agotado(self, sku_vino, df_completo):
        # Obtener el tipo de vino asociado al SKU
        tipo_vino_sku = df_completo.loc[df_completo['SKU'] == sku_vino, 'tipo_vino'].iloc[0]

        # Verificar si el tipo de vino es tinto, blanco o rosado
        tipos_validos = ['Vino Tinto', 'Vino Blanco', 'Vino Rosado']
        if tipo_vino_sku in tipos_validos:
            return False
        else:
            return True
       
        