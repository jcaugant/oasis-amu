import streamlit as st
import pandas as pd
import requests as rq

def struct_clean(col):
  valid, old, unknown = [],[],[]
  url = f"https://api.archives-ouvertes.fr/ref/structure/?q=parentDocid_i:{col}&fl=name_s&wt=json&indent=true&group=true&group.field=valid_s&group.limit=300"
  req = rq.get(url).json()
  for i in range(len(req['grouped']['valid_s']['groups'][0]['doclist']['docs'])):
    value = req['grouped']['valid_s']['groups'][0]['doclist']['docs'][i]['names_s']
    valid.append(value)
  for j in range(len(req['grouped']['valid_s']['groups'][1]['doclist']['docs'])):
    value = req['grouped']['valid_s']['groups'][1]['doclist']['docs'][i]['names_s']
    old.append(value)
  for k in range(len(req['grouped']['valid_s']['groups'][2]['doclist']['docs'])):
    value = req['grouped']['valid_s']['groups'][2]['doclist']['docs'][i]['names_s']
    unknown.append(value)
  st.write(valid, old, unknown)




portail = st.text_input("Entrez le numéro d'identifiant du portail ou de la collection à analyser", "")
struct_clean(portail)
