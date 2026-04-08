import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

def repartition_projet(col) :
    type_projet_anr, type_projet_erc, nb_depot_anr, nb_depot_erc = [],[],[],[]
    url_depot_anr = f"https://api.archives-ouvertes.fr/search/{col}/?q=*%3A*&rows=0&wt=json&fq=submitType_s:file&indent=true&facet=true&facet.field=anrProjectCallTitle_s"
    url_depot_erc = f"https://api.archives-ouvertes.fr/search/{col}/?q=*%3A*&rows=0&wt=json&fq=submitType_s:file&indent=true&facet=true&facet.field=europeanProjectAcronym_s"
    req_depot_anr = rq.get(url_depot_anr)
    req_depot_erc = rq.get(url_depot_erc)
    req_depot_anr = req_depot_anr.json()
    req_depot_erc = req_depot_erc.json()
    limit_anr = len(req_depot_anr['facet_counts']['facet_fields']['anrProjectCallTitle_s'])
    limit_erc = len(req_depot_erc['facet_counts']['facet_fields']['europeanProjectAcronym_s'])
    for i in range(0, limit_anr) :
        if int(i) % 2 ==0 :
            type_projet_anr.append(req_depot_anr['facet_counts']['facet_fields']['anrProjectCallTitle_s'][i])
        else :
            nb_depot_anr.append(req_depot_anr['facet_counts']['facet_fields']['anrProjectCallTitle_s'][i])
    for i in range(0, limit_erc) :
        if int(i) % 2 ==0 :
            type_projet_erc.append(req_depot_erc['facet_counts']['facet_fields']['europeanProjectAcronym_s'][i])
        else :
            nb_depot_erc.append(req_depot_erc['facet_counts']['facet_fields']['europeanProjectAcronym_s'][i])
    df_anr = pd.DataFrame(
   {
       "Nom du projet ANR": type_projet_anr,
       "Nombre de dépôts": nb_depot_anr,
   }
    )

    df_erc = pd.DataFrame(
   {
       "Nom du projet ERC": type_projet_erc,
       "Nombre de dépôts": nb_depot_erc,
   }
    )

    graph_anr, tab_anr, graph_erc, tab_erc = st.tabs(["Répartition des projets ANR", "Tableau des projets ANR", "Répartition des projets ERC", "Tableau des projets ERC"])
    with graph_anr :
        df_anr.drop(df_anr.loc[df_anr["Nombre de dépôts"] == 0].index, inplace=True)
        df_anr=df_anr.set_index("Nom du projet ANR")
        df_anr = df_anr.sort_values(by=['Nombre de dépôts'], ascending = False)
        st.bar_chart(df_anr[['Nombre de dépôts']])
        st.dataframe(df_anr, width = 500)
    with tab_anr :
        st.dataframe(df_anr, width = 500)
    with graph_erc :
        df_erc.drop(df_erc.loc[df_erc["Nombre de dépôts"] == 0].index, inplace=True)
        df_erc=df_erc.set_index("Nom du projet ERC")
        df_erc = df_erc.sort_values(by=['Nombre de dépôts'], ascending = False)
        st.bar_chart(df_erc[['Nombre de dépôts']])
        st.dataframe(df_erc, width = 500)
    with tab_erc :
        st.dataframe(df_erc, width = 500)

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
repartition_projet(portail)
