import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static


def config_map(df):

    
    # Coordonnées centrales pour centrer la carte
    map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]

    # Création de la carte
    m = folium.Map(location=map_center, zoom_start=6.5)

    # Ajout des marqueurs pour les centres et les POP en fonction des options sélectionnées

    option = st.selectbox('Afficher les éléments :', ['Tout afficher', 'Centres de Formation', 'POP'])

    # Mise à jour des cases à cocher en fonction de la sélection dans la liste déroulante
    if option == 'Tout afficher':
        show_centers = True
        show_pops = True
    elif option == 'Centres de Formation':
        show_centers = True
        show_pops = False
    elif option == 'POP':
        show_centers = False
        show_pops = True
    if show_centers:
        for _, row in df.iterrows():
            popup_html = f"""
                <h4>{row['NOM_CENTRE']}</h4>
                <p><b>Nom du chef:</b> {row['NOM_CHEF']}</p>
                <p><b>Nom du POP:</b> {row['NOM_POP']}</p>
            """
            folium.Marker(
                location=[row['LATITUDE'], row['LONGITUDE']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue')
            ).add_to(m)

    if show_pops:
        for _, row in df.iterrows():
            popup_html = f"""
                <h4>{row['NOM_POP']}</h4>
                <p><b>Nom du centre associé:</b> {row['NOM_CENTRE']}</p>
                <p><b>Nom du chef:</b> {row['NOM_CHEF']}</p>
            """
            folium.Marker(
                location=[row['LATITUDE_POP'], row['LONGITUDE_POP']],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='green')
            ).add_to(m)
    # Affichage de la carte dans Streamlit
    folium_static(m)
    

# Fonction pour afficher la page d'accueil
def accueil():

    # st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")

    st.title(":bar_chart: Application Reporting MFPAI")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    st.write("""
        Cette application vous permet de visualiser différentes données.
        Utilisez le menu de navigation pour sélectionner la page que vous souhaitez afficher.
    """)


    df = pd.read_csv("ods_centre.csv")

    # Affichage de la carte
    config_map(df)

    st.write("Liste des apprenants")
    st.write(df)
    # 1. Répartition par centre de formation
    nbre_centre = df['NOM_CENTRE'].nunique()
    nbre_pop = df['NOM_POP'].nunique()

    # Création d'une disposition en grille pour les cartes
    col1, col2 = st.columns(2)

    # Carte 1 : Nombre de centres de formation
    with col1:
        st.write("Nombre de centres de formation")
        st.write(nbre_centre)

    # Carte 2 : Nombre total d'apprenants
    with col2:
        st.write("Nombre total de POP")
        st.write(nbre_pop)
    
    col1, col2 = st.columns((1, 1)) 

    df["DT_INSERTION"] = pd.to_datetime(df["DT_INSERTION"])

    # Getting the min and max
    startDate = pd.to_datetime(df["DT_INSERTION"]).min()
    endDate = pd.to_datetime(df["DT_INSERTION"]).max()  # Correction de la valeur de endDate, max() au lieu de min()

    with col1:
        st.date_input("Start Date", startDate)

    # st.markdown("&nbsp;" * 10)

    with col2:
        st.date_input("End Date", endDate)
     
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    # Créer une liste déroulante pour sélectionner la population (POP)
    selected_pop = st.selectbox("Sélectionner le POP", df['NOM_POP'].unique())

    # Filtrer les données en fonction de la population sélectionnée
    filtered_data = df[df['NOM_POP'] == selected_pop]

    # Créer la carte Folium
    m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=10)

    # Ajouter les emplacements des centres sur la carte
    for index, row in filtered_data.iterrows():
        popup_text = f"<b>Nom du Centre:</b> {row['NOM_CENTRE']}<br><b>Nom du chef:</b> {row['NOM_CHEF']}<br><b>Nom du POP:</b> {row['NOM_POP']}<br>"
        folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=100)).add_to(m)

    # Afficher la carte Folium dans Streamlit
    folium_static(m)


    # Liste déroulante pour sélectionner une POP
    selected_pop = st.selectbox("Sélectionnez une POP", df['NOM_POP'].unique())

    # Filtrer les centres en fonction de la POP sélectionnée
    filtered_centers = df[df['NOM_POP'] == selected_pop][['NOM_CENTRE', 'NOM_CHEF']]

    # Afficher la liste des centres correspondants avec le nom du chef
    st.write("Centres correspondants à la POP sélectionnée :")
    st.write(filtered_centers)



if __name__ == "__main__":
    accueil()
