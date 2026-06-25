from bs4 import BeautifulSoup as bs
import requests as rq
import streamlit as st

def stats_scrap(id) :
  api = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&rows=5000&wt=json&fq=authIdHal_s:{id}&fl=uri_s,publicationDate_s,submittedDate_s"
  req = rq.get(api).json()
  uri, submit_date, publish_date, consult, download = [],[],[],[],[]
  for j in range(0,len(req['response']['docs'])):
    submit_date.append(req['response']['docs'][j]['submittedDate_s'])
    publish_date.append(req['response']['docs'][j]['publicationDate_s'])
    uri.append(req['response']['docs'][j]['uri_s'])

columns = ["URI","Date de publication","Date de dépôt HAL","Consultations","Téléchargements"]
df = pd.DataFrame(columns = columns)
df['URI'], df['Date de publication'], df['Date de dépôt HAL'] = uri, publish_date, submit_date
st.dataframe(df, width = 1500) 


idhal = st.text_input("Entrez l'IdHal de l'auteur", "")
stats_scrap(idhal)

