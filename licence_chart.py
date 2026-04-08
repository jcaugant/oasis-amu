import streamlit as st
import requests as rq, json, pandas as pd
from datetime import datetime

def licence(col,year) :
    licence, nb_licence = [],[]
    url = f"https://api.archives-ouvertes.fr/search/?q=*%3A*&fq=publicationDateY_i:{year}&fq=structId_i:{col}&wt=json&fq=submitType_s:file&indent=true&facet=true&facet.field=fileLicenses_s"
    req = rq.get(url).json()
    limit = len(req['facet_counts']['facet_fields']['fileLicenses_s'])
    for i in range(0, limit) :
        if int(i) % 2 ==0 :
            if req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://about.hal.science/hal-authorisation-v1/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "Autorisation HAL"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by-nc-nd/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY-NC-ND"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by-nc/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY-NC"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://hal.science/licences/copyright/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "Copyright"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by-nc-sa/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY-NC-SA"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by-sa/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY-SA"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://creativecommons.org/licenses/by-nd/4.0/" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "CC-BY-ND"
            elif req['facet_counts']['facet_fields']['fileLicenses_s'][i] == "https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf" :
                req['facet_counts']['facet_fields']['fileLicenses_s'][i] = "Etalab"   

            licence.append(req['facet_counts']['facet_fields']['fileLicenses_s'][i])
        else :
            nb_licence.append(req['facet_counts']['facet_fields']['fileLicenses_s'][i])
    df = pd.DataFrame(
   {
       "Licence": licence,
       "Nombre de dépôts": nb_licence,
   }
    )
    df.drop(df.loc[df["Nombre de dépôts"] == 0].index, inplace=True)
    df=df.set_index("Licence")
    df = df.sort_values(by=['Nombre de dépôts'], ascending = False)
    st.bar_chart(df[['Nombre de dépôts']])
    
portail = st.text_input("Entrez le code de la structure à analyser", "")
year = st.selectbox(
'Sélectionnez une année',
(2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
licence(portail,year)
