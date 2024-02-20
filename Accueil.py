import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static


df = pd.read_csv("data/ods_centre.csv", encoding="utf-8")
df1 = pd.read_csv("data/apprenant.csv", encoding= "utf-8")
df2 = pd.read_csv("data/formateur.csv", encoding= "utf-8")

def config_map(df):

    # Définition du centre de la carte (latitude, longitude et zoom) en fonction  de la moyenne des données
    map_center = [df['LATITUDE'].mean(), df['LONGITUDE'].mean()]

    #Création de la carte
    m = folium.Map(location=map_center, zoom_start=8)

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
                popup=folium.Popup(popup_html),
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
                popup=folium.Popup(popup_html),
                icon=folium.Icon(color='green')
            ).add_to(m)

    # Ajouter le style CSS pour rendre la carte responsive
    st.markdown(
        """
        <style>
        .fullScreenFrame {
            width: 100%;
            padding-top: 56.25%;
            position: relative;
        }
        .fullScreenFrame iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Afficher la carte dans Streamlit
    folium_static(m)


# Fonction d'affichage des centres en fonction des pop
def centre_pop(df):
    # Créer une liste déroulante pour sélectionner la population (POP)
    selected_pop = st.selectbox("Sélectionner le POP", df['NOM_POP'].unique())
    
    # Filtrer les données en fonction de la population sélectionnée
    filtered_data = df[df['NOM_POP'] == selected_pop]

    
    
    centers_string = ", ".join(filtered_data['NOM_CENTRE'])
    # Boucler à travers les éléments de la liste et les ajouter comme des éléments de liste à la liste HTML
    st.markdown(
        f"<h3 style='font-size: 20px; color: #007bff; font-weight: bold;'>Centres de formation et Lycée Technique rattachés au POP  :  {centers_string}</h3>",
        unsafe_allow_html=True
    )

    # Créer la carte Folium
    m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=10)

    # Ajouter les emplacements des centres sur la carte
    for index, row in filtered_data.iterrows():
        popup_text = f"<b>Nom du Centre:</b> {row['NOM_CENTRE']}<br><b>Nom du chef:</b> {row['NOM_CHEF']}<br><b>Nom du POP:</b> {row['NOM_POP']}<br>"
        folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=100), icon=folium.Icon(color='blue')).add_to(m)
    popup_text = f"<b>Nom du POP:</b> {filtered_data.iloc[0]['NOM_POP']}"
    folium.Marker(location=[filtered_data.iloc[0]['LATITUDE_POP'], 
                            filtered_data.iloc[0]['LONGITUDE_POP']], 
                            popup=folium.Popup(popup_text, max_width=100), 
                            icon=folium.Icon(color='green')
                            ).add_to(m)

    # Afficher la carte Folium dans Streamlit
    folium_static(m)

# Fonction principale pour gérer la navigation
def main():

    st.subheader("""
    """)
    #st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")
    st.title(":bar_chart: **Ministère de la Formation Professionnelle, de l'Apprentissat et de l’Insertion (MFPAI)**")
    #st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    
    st.subheader("""
             **Application web dédiée à l’analyse et au reporting des indicateurs sur les apprentissages, des formations, etc**
    """)
    st.write("------------------------------------------")

    df = pd.read_csv("data/ods_centre.csv", encoding="utf-8")
    df1 = pd.read_csv("data/apprenant.csv", encoding= "utf-8")
    df2 = pd.read_csv("data/formateur.csv", encoding= "utf-8")

    # 1. Répartition par centre de formation
    nbre_centre = df['NOM_CENTRE'].nunique()
    nbre_pop = df['NOM_POP'].nunique()
    nbre_app = df1['ID_DIM_APPRENANT'].nunique()
    nbre_form = df2['ID_DIM_FORMATEUR'].nunique()

    # Création d'une disposition en grille pour les cartes
    col1, col2 = st.columns(2)

    # # Getting the min and max
    # startDate = pd.to_datetime(df["DT_INSERTION"]).min()
    # endDate = pd.to_datetime(df["DT_INSERTION"]).max()

    # with col1:
    #     st.date_input("Date de Début", startDate)

    # with col2:
    #     st.date_input("Date de dernier mise à jour", endDate)
    
    # Carte 1 : Nombre de centres de formation
    with col1:
        #st.write("-------------------")
        st.markdown("<h3 style='color: #ff5733; text-align: center;'>Nombre d'apprennant</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 30px; text-align: center;'><span style='color: #007bff; font-weight: bold;'>{nbre_app}</span></p>", unsafe_allow_html=True)
        st.write("-------------------")
        st.markdown("<h3 style='color: #ff5733; text-align: center;'>Nombre de centre de formation</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 30px; text-align: center;'><span style='color: #007bff; font-weight: bold;'>{nbre_centre}</span></p>", unsafe_allow_html=True)

    with col2:
        #st.write("-------------------")
        st.markdown("<h3 style='color: #ff5733; text-align: center;'>Nombre de formateur</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 30px; text-align: center;'><span style='color: #007bff; font-weight: bold;'>{nbre_form}</span></p>", unsafe_allow_html=True)
        st.write("-------------------")
        st.markdown("<h3 style='color: #ff5733; text-align: center;'>Nombre de POP</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 30px; text-align: center;'><span style='color: #007bff; font-weight: bold;'>{nbre_pop}</span></p>", unsafe_allow_html=True)

    
    # Affichage de la carte
    config_map(df)

    df["DT_INSERTION"] = pd.to_datetime(df["DT_INSERTION"])
    st.write("------------------------------------------")
    
    st.subheader("Liste des centre de formation")
    st.write(df.iloc[:,:8])

    st.write("------------------------------------------")
    # Affichage des centres en fonction des pop
    centre_pop(df)

    st.write("------------------------------------------")


if __name__ == "__main__":
    main()
