import os
import pandas as pd
import plotly as plt

def save_dataframe(dataframe: pd.DataFrame, nom_fichier: str, emplacement_relatif_fichier: str="./"):
    dataframe_path = os.path.realpath(f"{emplacement_relatif_fichier}{nom_fichier}")
    dataframe.to_pickle(dataframe_path)

def seuil_depasse(fenetre_valeurs: pd.Series, seuil: int) -> bool:
    return all(valeur > seuil for valeur in fenetre_valeurs)

"""
    @param {string} date_debut - date au format "yyyy/mm/dd"
    @param {string} date_fin - date au format "yyyy/mm/dd"
    @param {int} periode_information_recommendation - période exprimée en heure
    @param {int} periode_alerte - période exprimée en heure
"""
def time_series_concentration_polluant(
        df: pd.DataFrame,
        date_debut: str,
        date_fin: str,
        nom_station: str,
        nom_polluant: str,
        seuil_information_recommendation: int,
        periode_information_recommendation: int,
        seuil_alerte: int,
        periode_alerte: int
    ) -> plt.graph_objs.Figure:
    px = plt.express
    go = plt.graph_objs

    # filtrage
    filtered_df = df.loc[(df["date_debut"] >= date_debut) & (df["date_debut"] <= date_fin)]
    filtered_df = filtered_df.query(f"nom_station=='{nom_station}'")
    filtered_df = filtered_df.query(f"nom_poll=='{nom_polluant}'")

    # tri
    filtered_df = filtered_df.sort_values(by="date_debut")

    # ajout de colonnes
    filtered_df["seuil_information"] = filtered_df["valeur"].rolling(window=periode_information_recommendation).apply(
        lambda fenetre_valeurs: seuil_depasse(fenetre_valeurs, seuil_information_recommendation)
    ).fillna(0).astype(int)
    filtered_df["seuil_alerte"] = filtered_df["valeur"].rolling(window=periode_alerte).apply(
        lambda fenetre_valeurs: seuil_depasse(fenetre_valeurs, seuil_alerte)
    ).fillna(0).astype(int)

    fig = px.line(filtered_df, x="date_debut", y="valeur", title=f"Évolution de la concentration de {nom_polluant}")

    fig.update_layout(
        xaxis_title="Date et heure",
        yaxis_title="Concentration (µg.m-3)"
    )

    # seuil d'information et de recommendation (plotly version 5.14 or higher)
    fig.add_hline(
        y=seuil_information_recommendation,
        line_width=1,
        line_color="rgb(256, 126, 0)",
        annotation_text="seuil d'information et de recommendation", 
        annotation_position="bottom right",
        annotation_font_color="rgb(256, 126, 0)"
    )
    # seuil d'alerte (plotly version 5.14 or higher)
    fig.add_hline(
        y=seuil_alerte,
        line_width=1,
        line_color="rgb(204, 0, 0)",
        annotation_text="seuil d'alerte", 
        annotation_position="top right",
        annotation_font_color="rgb(204, 0, 0)"
    )

    information_highlighted = filtered_df[filtered_df["seuil_information"] == 1]
    alerte_highlighted = filtered_df[filtered_df["seuil_alerte"] == 1]

    fig.add_trace(
        go.Scatter(
            x=information_highlighted["date_debut"],
            y=information_highlighted["valeur"],
            mode="markers",
            name="Information et recommandation",
            fillcolor="rgb(255, 204, 0)",
            marker=dict(
                color="rgb(255, 204, 0)"
            )
        )
    )
    fig.add_trace(
        go.Scatter(
            x=alerte_highlighted["date_debut"],
            y=alerte_highlighted["valeur"],
            mode="markers",
            name="Alerte",
            fillcolor="rgb(255, 204, 0)",
            marker=dict(
                color="rgb(204, 0, 0)"
            )
        )
    )

    return fig
