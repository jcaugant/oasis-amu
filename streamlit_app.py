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
}

pg = st.navigation(pages)
pg.run()
