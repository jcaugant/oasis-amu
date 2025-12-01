import requests as rq
import pandas as pd
import streamlit as st

def detect_doublon(col, annee_d, annee_f) :
    title, doi = [], []
    annee_d, annee_f = int(annee_d), int(annee_f)
    for y in range(annee_d,annee_f+1):
        url = f"https://api.archives-ouvertes.fr/search/{col}/?q=*:*&wt=json&fl=title_s,doiId_s&rows=5000&fq=submittedDateY_i:{y}"
    req = rq.get(url)
    req = req.json()
    for i in range(0, len(req['response']['docs'])):
        title.append(req['response']['docs'][i]['title_s'][0])
        try :
            doi.append(req['response']['docs'][i]['doiId_s'])
        except :
            doi.append("Pas de DOI")
    columns = ['Titre','DOI']
    df = pd.DataFrame(columns = columns)
    df['Titre'] = title
    df['DOI'] = doi
    db_title = df['Titre'].value_counts()
    db_doi = df['DOI'].value_counts()
    st.write("Doublons détectés sur les titres")
    st.write(db_title[db_title>1])
    st.write("Doublons détectés sur les DOI")
    st.write(db_doi[db_doi>1])
    st.write("Attention, les doublons récupérées se basent uniquement sur des titres et des doi exacts. Il ne s'agit en aucun cas de doublons certifiés, il convient d'opérer à un travail de vérification basé sur ces résultats")

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
year_s = st.selectbox(
'Sélectionnez l\'année de départ de votre sélection',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024))
year_e = st.sidebar.selectbox(
'Sélectionnez l\'année d\'arrivée de votre sélection',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
detect_doublon(portail,year_s,year_e)
