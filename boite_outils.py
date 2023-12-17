import os
import pandas as pd
import plotly as plt

def save_dataframe(dataframe: pd.DataFrame, nom_fichier: str, emplacement_relatif_fichier: str="./"):
    dataframe_path = os.path.realpath(f"{emplacement_relatif_fichier}{nom_fichier}")
    dataframe.to_pickle(dataframe_path)

"""
    @param {string} date_debut - date au format "yyyy/mm/dd"
    @param {string} date_fin - date au format "yyyy/mm/dd"
"""
def time_series_concentration_polluant(
        df: pd.DataFrame,
        date_debut: str,
        date_fin: str
    ) -> plt.graph_objs.Figure:
    px = plt.express

    # dates au format "yyyy/mm/dd"
    # date_debut = "2023/07/01"
    # date_fin = "2023/07/31"
    nom_station = "Bourg Murat"
    nom_polluant = "Dioxyde de soufre"

    filtered_df = df.loc[(df["date_debut"] >= date_debut) & (df["date_debut"] <= date_fin)]
    filtered_df = filtered_df.query(f"nom_station=='{nom_station}'")
    filtered_df = filtered_df.query(f"nom_poll=='{nom_polluant}'")

    filtered_df = filtered_df.sort_values(by="date_debut")

    fig = px.line(filtered_df, x="date_debut", y="valeur", title="Évolution de la concentration de S02")

    fig.update_layout(
        xaxis_title="Date et heure",
        yaxis_title="Concentration (µg.m-3)"
    )

    # seuil d'information et de recommendation (plotly version 5.14 or higher)
    fig.add_hline(y=300, line_width=1, line_color="rgb(256, 126, 0)", label=dict(
        text="seuil d'information et de recommendation",
        textposition="bottom right",
        font=dict(color="rgb(256, 126, 0)")
    ))
    # seuil d'alerte (plotly version 5.14 or higher)
    fig.add_hline(y=500, line_width=1, line_color="rgb(204, 0, 0)", label=dict(
        text="seuil d'alerte",
        textposition="top right",
        font=dict(color="rgb(204, 0, 0)")
    ))

    return fig
