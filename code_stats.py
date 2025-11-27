def evolution_depot(col, annee_d, annee_f) :
    nb_code, date_hal = [], []
    annee_d, annee_f = int(annee_d), int(annee_f)
    for year in range(annee_d, annee_f+1) : 
        for month in range(1, 13) : 
            url_code = f"https://api.archives-ouvertes.fr/search/{col}/?rows=0&fq=submittedDateY_i:{year}&fq=submittedDateM_i:{month}&fq=docType_s:SOFTWARE"
            req_code= rq.get(url_code)
            req_code = req_code.json()
            code = req_code['response']['numFound']
            Hdate = f"{year}-{month}"
            date_format = "%Y-%m"
            date = datetime.strptime(Hdate, date_format)
            nb_code.append(code)
            date_hal.append(date)
    df = pd.DataFrame(
   {
       "Dates": date_hal,
       "Nombre de codes": nb_code,
   }
    )
    df=df.set_index("Dates")
    st.line_chart(df[['Nombre de codes']])
    st.dataframe(df, width = 500)

analyse = st.sidebar.selectbox(
    'Sélectionnez l\'indicateur que vous souhaitez afficher',
    ('Choix','Evolution des dépôts de codes dans un portail ou une collection', 'Répartition des dépôts de codes par langage'))

if analyse == 'Choix' :
    st.write('Sélectionnez dans la barre latérale quels indicateurs vous souhaitez afficher')

if analyse == 'Evolution des dépôts de codes dans un portail ou une collection' :
    portail = st.sidebar.text_input("Entrez l'acronyme du portail ou de la collection à analyser", "")
    year_s = st.sidebar.selectbox(
    'Sélectionnez une année de départ',
    (2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024))
    year_e = st.sidebar.selectbox(
    'Sélectionnez une année de fin',
    (2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025))
    evolution_depot(portail,year_s,year_e)
