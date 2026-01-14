import streamlit as st
import pandas as pd
import requests as rq

def struct_clean(col):
  valid, old, unknown = [],[],[]
  url = f"https://api.archives-ouvertes.fr/ref/structure/?q=parentDocid_i:{col}&fl=name_s&wt=json&indent=true&group=true&group.field=valid_s&group.limit=300"
  req = rq.get(url).json()
  valid = len(req['grouped']['valid_s']['groups'][0]['doclist']['docs'])
  old = len(req['grouped']['valid_s']['groups'][1]['doclist']['docs'])
  unknown = len(req['grouped']['valid_s']['groups'][2]['doclist']['docs'])
  st.write(valid, old, unknown)




portail = st.text_input("Entrez le numéro d'identifiant du portail ou de la collection à analyser", "")
struct_clean(portail)
