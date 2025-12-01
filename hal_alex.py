import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

def compar_id(id) :
    struct_hal, struct_oa = [],[]
    id = int(id)
    info_hal = f"https://api.archives-ouvertes.fr/ref/structure/?wt=json&q=docid:%22{id}%22&fl=ror_s,label_s"
    try :
        req = rq.get(info_hal).json()
        ror = req['response']['docs'][0]['ror_s'][0]
        name = req['response']['docs'][0]['label_s']
        st.write(f"Votre structure est le/la {name} et son ROR est {ror}")
    except :
        st.write("Erreur : numéro de structure incorrect ou ror inexistant")
    api_hal = f"https://api.archives-ouvertes.fr/ref/structure/?wt=json&q=parentDocid_i:%22{id}%22&rows=300&fl=label_s&fq=valid_s:%22VALID%22"
    req_hal = rq.get(api_hal).json()
    for i in range(len(req_hal['response']['docs'])):
        struct_hal.append(req_hal['response']['docs'][i]['label_s'])
    struct_hal.sort()
    api_oa = f"https://api.openalex.org/institutions/{ror}"
    req_oa = rq.get(api_oa).json()
    for j in range(len(req_oa['associated_institutions'])):
        struct_oa.append(req_oa['associated_institutions'][j]['display_name'])
    struct_oa.sort()
    col1, col2= st.columns(2)
    with col1:
        df1 = pd.DataFrame(struct_hal, columns=["Référencées dans HAL"])
        st.dataframe(df1)
    with col2:
        df2 = pd.DataFrame(struct_oa, columns=["Référencées dans OpenAlex"])
        st.dataframe(df2)

portail = st.text_input("Entrez le numéro HAL de la structure à analyser", "")
if portail == "":
  st.write("Pas de numéro HAL renseigné")
else :
  compar_id(portail)
