import streamlit as st
import requests as rq
import pandas as pd
from datetime import datetime

def repartition_depot(col) :
    type_doc, nb_depot = [],[]
    url_depot = f"https://api.archives-ouvertes.fr/search/{col}/?q=*%3A*&rows=0&wt=json&fq=submitType_s:file&indent=true&facet=true&facet.field=docType_s"
    req_depot = rq.get(url_depot)
    req_depot = req_depot.json()
    limit = len(req_depot['facet_counts']['facet_fields']['docType_s'])
    for i in range(0, limit) :
        if int(i) % 2 ==0 :
            type_doc.append(req_depot['facet_counts']['facet_fields']['docType_s'][i])
        else :
            nb_depot.append(req_depot['facet_counts']['facet_fields']['docType_s'][i])
    df = pd.DataFrame(
   {
       "Types de documents": type_doc,
       "Nombre": nb_depot,
   }
    )
    df.drop(df.loc[df["Nombre"] == 0].index, inplace=True)
    df=df.set_index("Types de documents")
    df = df.sort_values(by=['Nombre'], ascending = False)
    st.bar_chart(df[['Nombre']])
    st.dataframe(df, width = 500)

portail = st.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
repartition_depot(portail)
