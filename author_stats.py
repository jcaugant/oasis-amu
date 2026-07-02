from bs4 import BeautifulSoup as bs
import requests as rq
import streamlit as st
import pandas as pd

def stats_scrap(id) :
  api = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&rows=5000&wt=json&fq=authIdHal_s:{id}&fl=uri_s,publicationDate_s,submittedDate_s,label_s"
  req = rq.get(api).json()
  uri, submit_date, publish_date, consult, download, citation = [],[],[],[],[],[]
  for j in range(0,len(req['response']['docs'])):
    submit_date.append(req['response']['docs'][j]['submittedDate_s'])
    publish_date.append(req['response']['docs'][j]['publicationDate_s'])
    uri.append(req['response']['docs'][j]['uri_s'])
    citation.append(req['response']['docs'][j]['label_s'])
  columns = ["URI","Date de publication","Date de dépôt HAL","Consultations","Téléchargements","Citation"]
  df = pd.DataFrame(columns = columns)
  df['URI'], df['Date de publication'], df['Date de dépôt HAL'], df['Citation'] = uri, publish_date, submit_date, citation
# Scrapping
  for u in df['URI'] :
    req = rq.get(u)
    if req.status_code != 200:
        consult.append("None")
        download.append("None")
    else :
        pass
    print(req)
    soup = bs(req.content, 'html.parser')
    metrics = soup.find_all("div", {"class": "metrics-views"})
    for metric in metrics:
        spans = metric.find_all("span")

        valeur = spans[0].get_text(strip=True)
        label = spans[1].get_text(strip=True)

        if label == "Consultations":
            consult.append(valeur)

        elif label == "Téléchargements":
            download.append(valeur)

  df['Consultations'] = consult
  df['Téléchargements'] = download
  st.dataframe(df, width = 1500) 


idhal = st.text_input("Entrez l'IdHal de l'auteur", "")
stats_scrap(idhal)

