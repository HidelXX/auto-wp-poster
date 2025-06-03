import pandas as pd
import config

def carregar_dados(caminho):
    return pd.read_excel(caminho).head(config.LIMITE_PRODUTOS)