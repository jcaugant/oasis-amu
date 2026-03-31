import streamlit as st
import pandas as pd
import requests as rq
from datetime import datetime

def listing(struct,year_s, year_e) :
  url = f"https://api.archives-ouvertes.fr/search/?q=*:*&rows=0&wt=json&facet=true&facet.query=structHasAuthIdHal_fs&facet.field=structHasAuthIdHal_fs&facet.prefix={struct}_FacetSep_&facet.mincount=1&facet.limit=8000&fq=publicationDateY_i:[{year_s} TO {year_e}]"
  data = rq.get(url).json()
  facets = data["facet_counts"]["facet_fields"]["structHasAuthIdHal_fs"]
  rows = []

  for i in range(0, len(facets), 2):
    value = facets[i]
    count = facets[i + 1]

    parts = (
        value.replace("_JoinSep_", "_FacetSep_")
             .split("_FacetSep_")
    )

    rows.append({
        "struct_id": parts[0],
        "structure": parts[1],
        "idhal": parts[2],
        "auteur": parts[3],
        "nb_documents": count
    })
  df = pd.DataFrame(rows)
  st.dataframe(df, width = 1500) 

struct = st.text_input("Entrez le numéro HAL de votre structure ", "")
year_s = st.selectbox(
'Sélectionnez une année de début de recherche',
(2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026))
year_e = st.selectbox(
'Sélectionnez une année de fin de recherche',
(2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026))
listing(struct,year_s, year_e)
st.text("Outil développé par Théo Rousselle (INIST-CNRS) et intégré par Julien Caugant (AMU)")





