import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

def licence(col,year) :
    licence, nb_licence = [],[]
    url = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&fq=publicationDateY_i:{year}&fq=structId_i:{col}&wt=json&fq=submitType_s:file&indent=true&facet=true&facet.field=fileLicenses_s"
    req = rq.get(url).json()
    limit = len(req['facet_counts']['facet_fields']['fileLicenses_s'])
    for i in range(0, limit) :
        if int(i) % 2 ==0 :
            licence.append(req['facet_counts']['facet_fields']['fileLicenses_s'][i])
        else :
            nb_licence.append(req['facet_counts']['facet_fields']['fileLicenses_s'][i])
    df = pd.DataFrame(
   {
       "Licence": licence,
       "Nombre de dépôts": nb_licence,
   }
    )
    df.drop(df.loc[df["Nombre de dépôts"] == 0].index, inplace=True)
    df=df.set_index("Licence")
    df = df.sort_values(by=['Nombre de dépôts'], ascending = False)
    st.bar_chart(df[['Nombre de dépôts']])
    
portail = st.text_input("Entrez le code de la structure à analyser", "")
year = st.selectbox(
'Sélectionnez une année',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
licence(portail,year)
