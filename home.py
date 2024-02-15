import streamlit as st
# import folium
import json
import psycopg2
import pandas as pd
from streamlit_folium import folium_static
from dashboard import Dashboard
import matplotlib.pyplot as plt
import seaborn as sns
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
    requet_apprenant = "SELECT * FROM \"FORMATION_PROF_DWH\".\"DIM_APPRENANT\";"


    try:
        df1 = ConnectAndQuery(requet_apprenant, params)


    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

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

            return (geojson_data, df, df1)

        else:
            st.error("Aucune donnée disponible.")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None


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

    geojson_data, df1, df = DfToGeoJson()


    # 1. Répartition par centre de formation
    nbre_centre = df1['NOM_CENTRE'].nunique()
    nbre_apprenant = df['ID_APPRENANT'].nunique()
    nbre_filiere = df['ID_FILIERE'].nunique()
    nbre_diplome = df['ID_DIPLOME'].nunique()

    # Création d'une disposition en grille pour les cartes
    col1, col2, col3, col4 = st.columns(4)

    # Carte 1 : Nombre de centres de formation
    with col1:
        st.write("Nombre de centres de formation")
        st.write(nbre_centre)

    # Carte 2 : Nombre total d'apprenants
    with col2:
        st.write("Nombre total d'apprenants")
        st.write(nbre_apprenant)

    # Carte 3 : Nombre total de filières
    with col3:
        st.write("Nombre total de filières")
        st.write(nbre_filiere)

    # Carte 4 : Nombre total de diplômes
    with col4:
        st.write("Nombre total de diplômes")
        st.write(nbre_diplome)


    st.write(df)
    # Créer une carte centrée sur les coordonnées moyennes
    # map1 = folium.Map(location=[df1.iloc[:, 4].mean(), df1.iloc[:, 5].mean()], zoom_start=7)
    # map2 = folium.Map(location=[df1.iloc[:, 6].mean(), df1.iloc[:, 7].mean()], zoom_start=7)

    # # Ajouter des marqueurs pour chaque ligne du DataFrame sur la carte map1
    # for index, row in df1.iterrows():
    #     popup_text = f"<b>Nom du Centre:</b> {row.iloc[1]}<br><b>Nom du chef:</b> {row.iloc[2]}<br><b>Nom du POP:</b> {row.iloc[3]}<br>"
    #     folium.Marker([row.iloc[4], row.iloc[5]], popup=folium.Popup(popup_text, max_width=300)).add_to(map1)

    # # Ajouter des marqueurs pour chaque ligne du DataFrame sur la carte map2
    # for index, row in df1.iterrows():
    #     popup_text = f"<b>Nom du Centre:</b> {row.iloc[1]}<br><b>Nom du chef:</b> {row.iloc[2]}<br><b>Nom du POP:</b> {row.iloc[3]}<br>"
    #     folium.Marker([row.iloc[6], row.iloc[7]], popup=folium.Popup(popup_text, max_width=300)).add_to(map2)

    # # Ajouter une légende pour différencier les deux types de points
    # folium.LayerControl().add_to(map1)
    # folium.LayerControl().add_to(map2)

    # # Afficher la carte avec Streamlit
    # folium_static(map1)
    # folium_static(map2)

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
        date1 = st.date_input("Start Date", startDate)

    st.markdown("&nbsp;" * 10)

    with col2:
        date2 = st.date_input("End Date", endDate)

    # with col1:
    #     st.subheader("Filiere par secteur")
    #     fig = px.bar(secteur_df, y="LB_FILIERE", x="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
    #     st.plotly_chart(fig, use_container_width=True, height=100)
        
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    with col1:
        # Création du graphique interactif avec Plotly Express
        fig = px.bar(df['LB_SECTEUR'].value_counts(), 
                    x=df['LB_SECTEUR'].value_counts().index, 
                    y=df['LB_SECTEUR'].value_counts(),
                    labels={'x': 'Secteur', 'y': "Nombre d'apprenants"},
                    title='Répartition des apprenants par secteur',
                    color=df['LB_SECTEUR'].value_counts().index)
        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)

    with col2:
        #st.title('Répartition des apprenants par sexe')
        # Création du graphique interactif avec Plotly Express
        fig = px.pie(df['SEXE'].value_counts(), 
                    names=df['SEXE'].value_counts().index, 
                    values=df['SEXE'].value_counts(),
                    title='Répartition des apprenants par sexe',
                    hole=0.5,
                    color=df['SEXE'].unique(),  # Utilisation des couleurs définies
                    color_discrete_map={k: c for k, c in zip(df['SEXE'].unique(), couleurs)})  # Attribution des couleurs

        # Personnalisation du graphique
        fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        #st.title('Répartition des apprenants par Diplôme')
        # Création du graphique interactif avec Plotly Express
        fig = px.bar(df['LB_DIPLOME'].value_counts(), 
                    x=df['LB_DIPLOME'].value_counts().index, 
                    y=df['LB_DIPLOME'].value_counts(),
                    labels={'x': 'Diplôme', 'y': "Nombre d'apprenants"},
                    title='Répartition des apprenants par diplôme',
                    color=df['LB_DIPLOME'].unique(),  # Utilisation des couleurs définies
                    color_discrete_map={k: c for k, c in zip(df['LB_DIPLOME'].unique(), couleurs)})  # Attribution des couleurs
        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)

   

    
    # Création du graphique interactif avec Plotly Express
    fig = px.bar(df['LB_FILIERE'].value_counts(), 
                y=df['LB_FILIERE'].value_counts().index,  # Inversion de x et y pour afficher horizontalement
                x=df['LB_FILIERE'].value_counts(),
                labels={'x': "Nombre d'apprenants", 'y': 'Filière'},
                title='Répartition des apprenants par filière',
                color=df['LB_FILIERE'].unique(),  # Utilisation des couleurs définies
                color_discrete_map={k: c for k, c in zip(df['LB_FILIERE'].unique(), couleurs)}) 

    # Supprimer la légende
    fig.update_layout(showlegend=False)

    # Affichage du graphique interactif dans Streamlit
    st.plotly_chart(fig)


    # Liste déroulante pour sélectionner la répartition
    repartition_selectionnee = st.selectbox("Sélectionnez une répartition :", ["Diplôme", "Genre", "Secteur d'activité", "Filière"])

    # Afficher les statistiques en fonction de la répartition sélectionnée
    if repartition_selectionnee == "Diplôme":
        fig = px.bar(df, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition par diplôme')
    elif repartition_selectionnee == "Genre":
        fig = px.bar(df, x='SEXE', color="SEXE", title='Répartition par genre')
    elif repartition_selectionnee == "Secteur d'activité":
        fig = px.bar(df, x='LB_SECTEUR', color="LB_SECTEUR",title='Répartition par secteur d\'activité')
    elif repartition_selectionnee == "Filière":
        fig = px.bar(df, x='LB_FILIERE', color="LB_FILIERE",title='Répartition par filière')
    
    # # Afficher les statistiques
    # st.write(stats)
    # Afficher le diagramme en barres  
    st.plotly_chart(fig, use_container_width=True)

    col6, col7 = st.columns((1, 1)) 

    with col6:
        # Afficher le diagramme interactif en barres des secteurs en fonction des filières
        st.subheader("Secteurs en fonction des filières")
        fig = px.histogram(df, x='LB_FILIERE', color='LB_SECTEUR', title='Secteurs en fonction des filières')
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        # Afficher le diagramme interactif en barres de la répartition des diplômes des apprenants
        st.subheader("Répartition des diplômes des apprenants")
        fig = px.histogram(df, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition des diplômes des apprenants')
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        # Afficher le diagramme interactif circulaire de la répartition des apprenants par sexe
        st.subheader("Répartition des apprenants par secteur")
        fig = px.pie(df, names='LB_SECTEUR', title='Répartition des apprenants par sexe')
        st.plotly_chart(fig, use_container_width=True)
    with col7:
        # Afficher le diagramme interactif en barres du nombre d'apprenants par filière
        st.subheader("Nombre d'apprenants par filière")
        fig = px.histogram(df, x='LB_FILIERE', color="LB_FILIERE", title='Nombre d\'apprenants par filière')
        st.plotly_chart(fig, use_container_width=True)



# Fonction pour afficher la première page
def page_1():
    st.title("Page 1")
    st.write("Contenu de la première page")

# Fonction pour afficher la deuxième page
def page_2():
    st.title("Page 2")
    st.write("Contenu de la deuxième page")

# Fonction pour afficher la troisième page
def page_3():
    st.title("Page 3")
    st.write("Contenu de la troisième page")

# Fonction principale pour gérer la navigation
def main():

    st.set_page_config(page_title='SWAST - Handover Delays',  layout='wide', page_icon=":bar_chart:")
    st.sidebar.title("Menu de navigation")
    pages = {
        "Accueil": accueil,
        "Page 1": Dashboard,
        "Page 2": page_2,
        "Page 3": page_3
    }
    selection = st.sidebar.radio("Aller à", list(pages.keys()), index=0)

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
