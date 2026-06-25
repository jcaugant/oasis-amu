from bs4 import BeautifulSoup as bs
import requests as rq
import streamlit as st

def stats_scrap(id) :
  api = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&rows=5000&wt=json&fq=authIdHal_s:{id}&fl=uri_s,publicationDate_s,submittedDate_s"
  req = rq.get(api).json()
  submit_date, publish_date, consult, download = [],[],[],[]
  st.write(req)

idhal = st.text_input("Entrez l'IdHal de l'auteur", "")
stats_scrap(idhal)

