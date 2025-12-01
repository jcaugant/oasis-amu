import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

portail = st.text_input("Entrez le code de votre structure", "")
if portail == "" :
  st.markdown(''' Veuillez renseigner le code de votre collection ou portail comme indiqué dans [Aurehal](https://aurehal.archives-ouvertes.fr/structure/index)''')
link = st.sidebar.checkbox('Ne pas compter les notices avec lien Open-Access')
liste_hal = []
url_total = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&fq=publicationDateY_i:2025&fq=structId_i:{portail}&wt=json"
url_file = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&fq=publicationDateY_i:2025&fq=structId_i:{portail}&wt=json&fq=submitType_s:file"
if link:
  url_notice = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&rows=10000&fq=publicationDateY_i:2025&fq=structId_i:{portail}&wt=json&fq=(submitType_s:notice%20NOT%20openAccess_bool:(true))&fl=halId_s"
else :
  url_notice = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&rows=10000&fq=publicationDateY_i:2025&fq=structId_i:{portail}&wt=json&fq=submitType_s:notice&fl=halId_s"
req_file, req_notice, req_total = rq.get(url_file), rq.get(url_notice), rq.get(url_total)
req_file, req_notice, req_total = req_file.json(), req_notice.json(), req_total.json()
try :
  file, notice, total = req_file['response']['numFound'], req_notice['response']['numFound'], req_total['response']['numFound']
  for i in range(0, notice) :
    halid = req_notice['response']['docs'][i]['halId_s']
    halid= "https://amu.hal.science/"+halid
    liste_hal.append(halid)
  st.write(f"Pour l'année 2025, votre structure a déposé {file} documents avec texte intégral et {notice} notices")
  # st.write(f"Votre pourcentage de publications avec texte intégral déposées dans HAL pour l'année 2025 est donc de : ", int((file/total)*100), "%")
  st.write("Votre pourcentage de publications avec texte intégral déposées dans HAL pour l'année 2025 est donc de : ")
  pourcent = int((file/total)*100)
  st.subheader(f"{pourcent}%")
  st.write("Vous trouverez la liste ci-dessous des notices HAL pour lesquelles le texte intégral est manquant")
  df = pd.DataFrame(liste_hal, columns=["Identifiant HAL"])
  st.dataframe(df)
except :
  st.write("L'identifiant renseigné semble incorrect, veuillez vérifier ou contacter le gestionnaire de votre portail ou de votre collection")
