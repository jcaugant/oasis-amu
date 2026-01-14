import streamlit as st
import pandas as pd
import requests as rq

def struct_clean(col):
  valid, old, unknown = [],[],[]
  url = f"https://api.archives-ouvertes.fr/ref/structure/?q=parentDocid_i:{col}&fl=name_s&wt=json&indent=true&group=true&group.field=valid_s&group.limit=300"
  req = rq.get(url).json()
  for i in range(0, len(req['grouped']['valid_s']['groups'][0]['doclist']['docs'])):
    val = req['grouped']['valid_s']['groups'][0]['doclist']['docs'][i]['name_s']
    valid.append(val)
  for j in range(0, len(req['grouped']['valid_s']['groups'][1]['doclist']['docs'])):
    val = req['grouped']['valid_s']['groups'][1]['doclist']['docs'][j]['name_s']
    old.append(val)
  for k in range(0, len(req['grouped']['valid_s']['groups'][2]['doclist']['docs'])):
    val = req['grouped']['valid_s']['groups'][2]['doclist']['docs'][k]['name_s']
    unknown.append(val)
  df_valid = pd.Dataframe(columns = ['Structure'])

  
portail = st.text_input("Entrez le numéro d'identifiant du portail ou de la collection à analyser", "")
struct_clean(portail)
