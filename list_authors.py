import streamlit as st
import pandas as pd
import requests as rq
from datetime import datetime

def listing_auteurs(mail) :
  api = f"https://api.archives-ouvertes.fr/ref/author/?q=*%3A*&rows=6000&wt=json&fq=emailDomain_s:%22{mail}%22&fl=firstName_s,lastName_s,*Id_s,idHal_s"
  req = rq.get(api).json()
  auteurs_n, auteurs_p, arxiv, google, idref, isni, orcid, viaf,idhal = [],[],[],[],[],[],[],[],[]
  for i in range(len(req['response']['docs'])) :
    auteurs_n.append(req['response']['docs'][i]['lastName_s'])
    auteurs_p.append(req['response']['docs'][i]['firstName_s'])
    try :
        arxiv.append(req['response']['docs'][i]['arxivId_s'][0])
    except :
        arxiv.append("Pas d'identifiant ArXiV")
    try :
        google.append(req['response']['docs'][i]['google scholarId_s'][0])
    except :
        google.append("Pas d'identifiant GoogleScholar")
    try :
        idref.append(req['response']['docs'][i]['idrefId_s'][0])
    except :
        idref.append("Pas d'identifiant IdRef")
    try :
        isni.append(req['response']['docs'][i]['isniId_s'][0])
    except :
        isni.append("Pas d'identifiant ISNI")
    try :
        orcid.append(req['response']['docs'][i]['orcidId_s'][0])
    except :
        orcid.append("Pas d'identifiant Orcid")
    try :
        viaf.append(req['response']['docs'][i]['viafId_s'][0])
    except :
        viaf.append("Pas d'identifiant Viaf")
    try :
        idhal.append(req['response']['docs'][i]['idHal_s'])
    except :
        idhal.append("Pas d'IdHal activé")
      
  df = pd.DataFrame(columns = ['Nom Auteur','Prénom Auteur','IdHal','Orcid','ID Google Scholar','IDREF','ISNI','VIAF','ID ArXiV'])
  df['Nom Auteur'] = auteurs_n
  df['Prénom Auteur'] = auteurs_p
  df['IdHal'] = idhal
  df['ID ArXiV'] = arxiv
  df['ID Google Scholar'] = google
  df['IDREF'] = idref
  df['ISNI'] = isni
  df['Orcid'] = orcid
  df['VIAF'] = viaf
  st.dataframe(df, width = 1500) 

mail = st.text_input("Entrez le domaine de l'adresse de courriel ", "")
listing_auteurs(mail)



