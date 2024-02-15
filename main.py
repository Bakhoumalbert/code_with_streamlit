import streamlit as st
from dashboard import Dashboard
from static_formateur import static_formateur
from static_apprenant import static_apprenant
from home import accueil


# Fonction pour afficher la troisième page
def page_3():
    st.title("Page 3")
    st.write("Contenu de la troisième page")


# Fonction principale pour gérer la navigation
def main():

    st.set_page_config(page_title='Reporting MFPAI',  layout='wide', page_icon=":bar_chart:")
    st.sidebar.title("Menu de navigation")
    pages = {
        "Accueil": accueil,
        "Statistique des apprenants": static_apprenant,
        "Statistique des formateurs": static_formateur,
        "Page 3": page_3
    }
    selection = st.sidebar.radio("", list(pages.keys()), index=0)

    page = pages[selection]
    page()

    st.markdown(
        """
        <style>
        .sidebar .block-container {
            display: flex;
            flex-direction: row;
            justify-content: space-around;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
