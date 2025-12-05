import streamlit as st

pages = {
    "Auteurs": [
        st.Page("list_authors.py", title="Auteurs d'une structure"),
    ],
    "Bonus AMU": [
        st.Page("bonus_stats.py", title = "Pourcentage de dépôts dans HAL"),
    ],
    "Codes et Logiciels": [
        st.Page("code_stats.py", title="Evolution des dépôts"),
        st.Page("code_lang.py", title="Répartition des dépôts par langage"),
    ],
    "Dépôts": [
        st.Page("col_stats.py", title="Evolution des dépôts"),
        st.Page("col_chart.py", title=" Répartition des dépôts par type"),
        st.Page("project_chart.py", title=" Répartition des projets ANR et ERC"),
        st.Page("detect_false.py", title="Détection des doublons"),
        st.Page("detect_doi.py", title="Détection par liste de DOI"),
    ],
    "Structures": [
        st.Page("hal_alex.py", title = "Comparaison structures HAL/OpenAlex"),
        st.Page("struct_list.py", title = "Liste des identifiants d'une structure"),
    ],
    "Script partagés": [
        st.Page("script_gg.py", title = "Script Guillaume Godet"),
    ]
}

pg = st.navigation(pages)
pg.run()
