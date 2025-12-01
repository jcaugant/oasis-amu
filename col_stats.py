import streamlit as st
import requests as rq
import pandas as pd
from datetime import datetime

def evolution_depot(col, annee_d, annee_f) :
    nb_notice, nb_text, date_hal = [], [], []
    annee_d, annee_f = int(annee_d), int(annee_f)
    for year in range(annee_d, annee_f+1) :
        for month in range(1, 13) : 
            url_notice = f"https://api.archives-ouvertes.fr/search/{col}/?rows=0&fq=submittedDateY_i:{year}&fq=submittedDateM_i:{month}&fq=submitType_s:notice"
            url_text = f"https://api.archives-ouvertes.fr/search/{col}/?rows=0&fq=submittedDateY_i:{year}&fq=submittedDateM_i:{month}&fq=submitType_s:file"
            req_notice, req_text = rq.get(url_notice), rq.get(url_text)
            req_notice, req_text = req_notice.json(), req_text.json()                
            notice = req_notice['response']['numFound']
            text = req_text['response']['numFound']
            Hdate = f"{year}-{month}"
            date_format = "%Y-%m"
            date = datetime.strptime(Hdate, date_format)
            nb_notice.append(notice)
            nb_text.append(text)
            date_hal.append(date)  
    df = pd.DataFrame(
   {
       "Dates": date_hal,
       "Notices": nb_notice,
       "Avec texte intégral": nb_text,
   }
    )
    df=df.set_index("Dates")
    url_typo = f"https://api.archives-ouvertes.fr/search/{col}/?q=*%3A*&rows=0&wt=json&indent=true&facet=true&facet.field=docType_s"
    req_typo = rq.get(url_typo)
    req_typo = req_typo.json()
    annee_y, nb_typo, typo = [], [], []
    for i in range(0,11,2):
       typo.append(req_typo['facet_counts']['facet_fields']['docType_s'][i])    
    for year in range(annee_d, annee_f+1) :
        url_typo = f"https://api.archives-ouvertes.fr/search/{col}/?q=*%3A*&rows=0&wt=json&fq=submittedDateY_i:{year}&indent=true&facet=true&facet.field=docType_s"
        req_typo = rq.get(url_typo)
        req_typo = req_typo.json()
        annee_y.append(year)
        a = []
        for j in range(1,12,2):
            a.append(req_typo['facet_counts']['facet_fields']['docType_s'][j])
        nb_typo.append(a)
    df_typo = pd.DataFrame(nb_typo, index = annee_y, columns = typo)
    df_typo = df_typo.T
    graph_evo, tab_evo, graph_typo, tab_typo = st.tabs(["Courbe d'évolution", "Tableau d'évolution", "Diagramme d'évolution typologique", "Tableau d'évolution typologique"])
    with graph_evo :
        st.line_chart(df[['Notices','Avec texte intégral']])
    with tab_evo :
        st.dataframe(df, width = 500)
    with graph_typo :
        st.bar_chart(df_typo)
    with tab_typo :
        st.dataframe(df_typo, width = 500)

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
year_s = st.selectbox(
'Sélectionnez une année de départ',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
year_e = st.selectbox(
'Sélectionnez une année de fin',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026))
evolution_depot(portail,year_s,year_e)
