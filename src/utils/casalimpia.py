
import glob
import os
import pandas as pd
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import re

def to_int(x):
    """
    Pasa los valores de precio "Gratis" a int 0
    """
    exp = re.findall(r'\d+|Gratis',x)[0]
    if exp == 'Gratis':
        return 0
    else: return int(exp)

def save_casa_limpia():
    """
    Limpia la tabla obtenida del scraping:
    - elimin duplicados
    - elimina las últimas filas por tener insuficientes datos
    - extrae los datos de los años y los precios
    """
    all_files = glob.glob(os.path.join('../data/parciales', "*.csv"))
    all_files.sort()
    casa_df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
    casa_df = casa_df.drop_duplicates('title').drop(['Unnamed: 0'],axis=1).reset_index(drop=True)
    clean_casa_df = casa_df.iloc[0:4275,:].copy()
    clean_casa_df.to_csv("../data/casa-encendida/casa_enc.csv")
    casa_df = pd.read_csv("../data/casa-encendida/casa_enc.csv",index_col=0)
    casa_df["year"] = casa_df["date"].str.extract(r'(\d\d\d\d$)')
    # Archivo final
    casa_df.to_csv("../data/casa-encendida/casa_enc_year.csv")

def get_casa_limpia():
    """
    Dataframe con los datos separados por años
    """
    return pd.read_csv("../data/casa-encendida/casa_enc_year.csv",index_col=0)

def get_precios():
    """
    Dataframe con precios, sus fechas y su categoría
    """
    casa_df = get_casa_limpia()
    precios = casa_df[["Precio","date","category"]].dropna()
    precios.loc[:,"Precio"] = precios["Precio"].apply(to_int)
    precios = precios.sort_index(ascending=False)
    return precios


