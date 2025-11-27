import streamlit as st
import requests as rq
from datetime import datetime
import pandas as pd

def repartition_code(col) :
    language, nb_depot = [],[]
    url_code = f"https://api.archives-ouvertes.fr/search/{col}/?q=*:*&wt=json&rows=0&fq=docType_s:SOFTWARE&&indent=true&facet=true&facet.field=softProgrammingLanguage_s"
    req_code = rq.get(url_code)
    req_code = req_code.json()
    limit = len(req_code['facet_counts']['facet_fields']['softProgrammingLanguage_s'])
    for i in range(0, limit) :
        if int(i) % 2 ==0 :
            language.append(req_code['facet_counts']['facet_fields']['softProgrammingLanguage_s'][i])
        else :
            nb_depot.append(req_code['facet_counts']['facet_fields']['softProgrammingLanguage_s'][i])
    df = pd.DataFrame(
   {
       "Language": language,
       "Nombre": nb_depot,
   }
    )
    df.drop(df.loc[df["Nombre"] == 0].index, inplace=True)
    df=df.set_index("Language")
    df = df.sort_values(by=['Nombre'], ascending = False)
    graph = st.bar_chart(df[['Nombre']])
    st.dataframe(df, width = 500)

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
repartition_code(portail)
