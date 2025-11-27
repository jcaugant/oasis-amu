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
