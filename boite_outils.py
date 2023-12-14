import os
import pandas as pd

def save_dataframe(dataframe: pd.DataFrame, nom_fichier: str, emplacement_relatif_fichier: str="./"):
    dataframe_path = os.path.realpath(f"{emplacement_relatif_fichier}{nom_fichier}")
    dataframe.to_pickle(dataframe_path)
