import streamlit as st

# Fonctions pour les différentes pages
def accueil():
    st.write("Page d'accueil")

def Dashboard():
    st.write("Page de Dashboard")

def page_2():
    st.write("Page 2")

def page_3():
    st.write("Page 3")

def main():
    st.title("Menu de navigation")  # Titre de la page

    # Barre de navigation
    nav_bar = st.columns(4)  # Diviser la barre de navigation en 4 colonnes
    nav_bar[0].write("")  # Espace vide pour l'alignement
    nav_bar[1].write("Accueil")  # Lien vers la page d'accueil
    nav_bar[2].write("Dashboard")  # Lien vers le Dashboard
    nav_bar[3].write("Page 2")  # Lien vers la page 2

    # Sélection de la page à afficher
    page_selection = st.radio("Aller à", ["Accueil", "Dashboard", "Page 2"])

    # Affichage de la page sélectionnée
    if page_selection == "Accueil":
        accueil()
    elif page_selection == "Dashboard":
        Dashboard()
    elif page_selection == "Page 2":
        page_2()

if __name__ == "__main__":
    main()
