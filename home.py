import streamlit as st
import folium
import psycopg2
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px

# Connexion à la base de données PostgreSQL
def ConnectAndQuery(requet, params):
    try:
        connection = psycopg2.connect(
            dbname=params["dbname"],
            user=params["user"],
            password=params["password"],
            host=params["host"],
            port=params["port"]
        )
        cursor = connection.cursor()

        # Exécuter la requête
        cursor.execute(requet)

        # Récupérer les en-têtes de colonnes
        columns = [desc[0] for desc in cursor.description]

        # Récupérer les données
        rows = cursor.fetchall()

        # Créer un DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Fermer le curseur et la connexion
        cursor.close()
        connection.close()

        return df

    except (Exception, psycopg2.Error) as error:
        print("Erreur lors de la connexion à PostgreSQL:", error)


def DfToGeoJson():
    params = {
        "dbname": "REFERENTIEL_MFPAI",
        "user": "postgres",
        "password": "ASB2101ab",
        "host": "localhost",
        "port": "5435"
    }
    requet_centre = "SELECT * FROM \"FORMATION_ODS\".\"ODS_CENTRE_FP\";"

    try:
        df = ConnectAndQuery(requet_centre, params)
        if df is not None and not df.empty:
            features = []

            for _, row in df.iterrows():
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(row['LONGITUDE']), float(row['LATITUDE'])]
                    },
                    "properties": {
                        "ID_CENTRE_FP": row['ID_CENTRE_FP'],
                        "NOM_CENTRE": row['NOM_CENTRE'],
                        "NOM_POP": row['NOM_POP'],
                        "NOM_CHEF": row['NOM_CHEF']
                    }
                }
                features.append(feature)

            geojson_data = {
                "type": "FeatureCollection",
                "features": features
            }

            return (geojson_data, df)

        else:
            st.error("Aucune donnée disponible.")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None


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


    # DEFAULT_LATITUDE = 15.00
    # DEFAULT_LONGITUDE = -14.00

    # st.subheader("Carte des centres")
    # my_map = folium.Map(location=[DEFAULT_LATITUDE, DEFAULT_LONGITUDE], zoom_start=6)

    geojson_data, df = DfToGeoJson()

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

    
    # Créer une fonction pour générer la carte
    # Fonction pour créer la carte interactive
    # def create_map(data, location_column, popup_column):
    #     # Créer une carte centrée sur les coordonnées moyennes
    #     map = folium.Map(location=[data[location_column].mean(), data[location_column + 1].mean()], zoom_start=10)

    #     # Ajouter des marqueurs pour chaque ligne du DataFrame
    #     for index, row in data.iterrows():
    #         # Vérifier si le type de point est sélectionné dans la sidebar
    #         if show_centres and row['NOM_CENTRE'] != 'NaN':
    #             folium.Marker([row[location_column], row["LONGITUDE"]], popup=row[popup_column], icon=folium.Icon(color='blue')).add_to(map)
    #         if show_pop and row['NOM_POP'] != 'NaN':
    #             folium.Marker([row["LATUTUDE_POP"], row["LONGITUDE_POP"]], popup=row[popup_column], icon=folium.Icon(color='green')).add_to(map)

    #     # Afficher la carte
    #     st.write(map)

    # # Charger les données
    # data = df1

    # # Sidebar pour sélectionner le type de point à afficher
    # show_centres = st.sidebar.checkbox("Afficher les centres")
    # show_pop = st.sidebar.checkbox("Afficher les POP")

    # # Vérifier si au moins un type de point est sélectionné
    # if show_centres or show_pop:
    #     # Vérifier si les colonnes de coordonnées des centres et des POP sont présentes
    #     if 'LATITUDE' in data.columns and 'LONGITUDE' in data.columns and 'LATITUDE_POP' in data.columns and 'LONGITUDE_POP' in data.columns:
    #         # Créer la carte interactive
    #         create_map(data, 'LATITUDE', 'NOM_CENTRE')  # Pour les centres
    #         create_map(data, 'LATITUDE_POP', 'NOM_POP')  # Pour les POP
    #     else:
    #         st.error("Les colonnes de coordonnées ne sont pas présentes dans les données.")
    # else:
    #     st.warning("Veuillez sélectionner au moins un type de point à afficher dans la sidebar.")

    # if geojson_data is not None:
    #     folium.GeoJson(geojson_data).add_to(my_map)
    #     folium_static(my_map)
    # e1se1
    #     st.write("Erreur lors du chargement des données.")
    
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

    # with col1:
    #     st.subheader("Filiere par secteur")
    #     fig = px.bar(secteur_df, y="LB_FILIERE", x="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
    #     st.plotly_chart(fig, use_container_width=True, height=100)
        
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    with col1:
        # Créer une liste déroulante pour sélectionner la population (POP)
        selected_pop = st.selectbox("Sélectionner le POP", df['NOM_POP'].unique())

        # Filtrer les données en fonction de la population sélectionnée
        filtered_data = df[df['NOM_POP'] == selected_pop]

        # Créer la carte Folium
        m = folium.Map(location=[filtered_data['LATITUDE'].mean(), filtered_data['LONGITUDE'].mean()], zoom_start=12)

        # Ajouter les emplacements des centres sur la carte
        for index, row in filtered_data.iterrows():
            popup_text = f"<b>Nom du Centre:</b> {row['NOM_CENTRE']}<br><b>Nom du chef:</b> {row['NOM_CHEF']}<br><b>Nom du POP:</b> {row['NOM_POP']}<br>"
            folium.Marker(location=[row['LATITUDE'], row['LONGITUDE']], popup=folium.Popup(popup_text, max_width=300)).add_to(m)

        # Afficher la carte Folium dans Streamlit
        folium_static(m)

    with col2:
        # Liste déroulante pour sélectionner une POP
        selected_pop = st.selectbox("Sélectionnez une POP", df['NOM_POP'].unique())

        # Filtrer les centres en fonction de la POP sélectionnée
        filtered_centers = df[df['NOM_POP'] == selected_pop][['NOM_CENTRE', 'NOM_CHEF']]

        # Afficher la liste des centres correspondants avec le nom du chef
        st.write("Centres correspondants à la POP sélectionnée :")
        st.write(filtered_centers)



if __name__ == "__main__":
    accueil()
