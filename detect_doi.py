import requests as rq
import pandas as pd
import streamlit as st

fichier = st.file_uploader("Ajoutez un fichier à analyser")
if fichier is not None:
  df = pd.read_csv(fichier)
  list_doi, list_result, list_hal = [], [], []
  for i in range(0, len(df['doi'])):
    doi = df['doi'][i]
    list_doi.append(doi)
    try :
      url = f"https://api.archives-ouvertes.fr/search/?q=*:*&wt=json&fl=submitType_s,halId_s&fq=doiId_s:{doi}"
      req = rq.get(url)
      req = req.json()
      result = req['response']['docs'][0]['submitType_s']
      hal_id = req['response']['docs'][0]['halId_s']
      list_result.append(result)
      list_hal.append(hal_id)
    except :
      result = "Pas dans HAL"
      hal_id = " "
      list_result.append(result)
      list_hal.append(hal_id)
                

  df_hal = pd.DataFrame(
    {
    "DOI": list_doi,
    "Type de dépôts": list_result,
    "Identifiant HAL" : list_hal,
    }
    )
    st.dataframe(df_hal)
  else :
    st.write("Ajoutez un fichier au format .csv comprenant la liste de vos DOI dans une seule colonne appelée doi")
