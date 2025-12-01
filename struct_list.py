import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

def liste_id(id):
    struct_hal, l_idref, l_isni, l_ror, l_wikidata = [],[],[],[],[]
    id = int(id)
    try :
        api = f"https://api.archives-ouvertes.fr/ref/structure/?wt=json&rows=1000&q=parentDocid_i:%22{id}%22&q=valid_s:%22VALID%22&fl=label_s,idref_s,isni_s,ror_s,rnsr_s,wikidata_s"
        req = rq.get(api).json()
    except :
        st.write("Erreur sur le numéro HAL renseigné")
    for i in range(len(req['response']['docs'])):
        struct_hal.append(req['response']['docs'][i]['label_s'])
        try :
            idref = req['response']['docs'][i]['idref_s']
        except :
            idref = "Pas d'Idref renseigné"
        l_idref.append(idref)
        try :
            isni = req['response']['docs'][i]['isni_s']
        except :
            isni = "Pas d'Isni renseigné"
        l_isni.append(isni)
        try :
            ror = req['response']['docs'][i]['ror_s']
        except :
            ror = "Pas de ROR renseigné"
        l_ror.append(ror)
        try :
            wikidata = req['response']['docs'][i]['wikidata_s']
        except :
            wikidata = "Pas d'identifiant Wikidata renseigné"
        l_wikidata.append(wikidata)
    columns=["Structures","IdRef","ISNI","ROR","Wikidata"]
    df = pd.DataFrame(columns=columns)
    df["Structures"] = struct_hal
    df["IdRef"] = l_idref
    df["ISNI"] = l_isni
    df["ROR"] = l_ror
    df["Wikidata"] = l_wikidata
    st.dataframe(df)
    count_struc = len(df['Structures'])
    count_idref = len(df.loc[(df["IdRef"]=="Pas d'Idref renseigné")])
    count_isni = len(df.loc[(df["ISNI"]=="Pas d'Isni renseigné")])
    count_ror = len(df.loc[(df["ROR"]=="Pas de ROR renseigné")])
    count_wiki = len(df.loc[(df["Wikidata"]=="Pas d'identifiant Wikidata renseigné")])
    st.write(f"Pour vos {count_struc} sous-structures, vous avez {count_idref} IdRef, {count_isni} ISNI, {count_ror} ROR et {count_wiki} identifiants Wikidata non renseignés dans HAL")

portail = st.text_input("Entrez le numéro HAL de la structure à analyser", "")
if portail == "":
  st.write("Pas de numéro HAL renseigné")
else :
  liste_id(portail)    
