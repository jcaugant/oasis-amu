import streamlit as st
import requests as rq
from datetime import datetime
import pandas as pd

def evolution_depot(col, annee_d, annee_f) :
    nb_code, date_hal = [], []
    annee_d, annee_f = int(annee_d), int(annee_f)
    for year in range(annee_d, annee_f+1) : 
        for month in range(1, 13) : 
            url_code = f"https://api.archives-ouvertes.fr/search/{col}/?rows=0&fq=submittedDateY_i:{year}&fq=submittedDateM_i:{month}&fq=docType_s:SOFTWARE"
            req_code= rq.get(url_code)
            req_code = req_code.json()
            code = req_code['response']['numFound']
            Hdate = f"{year}-{month}"
            date_format = "%Y-%m"
            date = datetime.strptime(Hdate, date_format)
            nb_code.append(code)
            date_hal.append(date)
    df = pd.DataFrame(
   {
       "Dates": date_hal,
       "Nombre de codes": nb_code,
   }
    )
    df=df.set_index("Dates")
    st.line_chart(df[['Nombre de codes']])
    st.dataframe(df, width = 500)

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser pour faire des tests", "")
year_s = st.selectbox(
'Sélectionnez une année de départ',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024))
year_e = st.selectbox(
'Sélectionnez une année de fin',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
if portail == "" :
    st.text("Le portail ou la collection n'ont pas été renseignés")
else :
    evolution_depot(portail,year_s,year_e)
    
