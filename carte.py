import streamlit as st
import pandas as pd
import folium
import json
from streamlit_folium import folium_static
from connect_DB import ConnectAndQuery

def DfToGeoJson():
    params = {
        "dbname": "REFERENTIEL_MFPAI",
        "user": "postgres",
        "password": "ASB2101ab",
        "host": "localhost",
        "port": "5435"
    }
    requet = "SELECT * FROM \"FORMATION_ODS\".\"ODS_CENTRE_FP\";"

    # Gestion des erreurs de connexion et de requête
    try:
        df = ConnectAndQuery(requet, params)
        if df is not None and not df.empty:
            # Créer une liste pour stocker les objets Feature GeoJSON
            features = []

            # Itérer à travers les lignes du DataFrame et créer un objet Feature pour chaque ligne
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

            # Créer un objet FeatureCollection GeoJSON avec la liste des objets Feature
            geojson_data = {
                "type": "FeatureCollection",
                "features": features
            }

            # Convertir en une chaîne GeoJSON
            geojson_string = json.dumps(geojson_data)

                # Créer une carte centrée sur les coordonnées moyennes
            map = folium.Map(location=[14.7226354457889, -17.2948732116772], zoom_start=10)

            #dtJson = DfToGeoJson()
            if geojson_string is not None:

                # Charger les données GeoJSON
                geojson_data = json.loads(geojson_string)

                # Ajouter les données GeoJSON à la carte
                folium.GeoJson(geojson_data).add_to(map)

                # Afficher la carte
                st.write(map._repr_html_(), unsafe_allow_html=True)
            else:
                st.write("Erreurs sur les données")
                    
            # print(geojson_string)
            return geojson_string
        
        else:
            st.error("Aucune donnée disponible.")
            return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None


def afficher_carte_folium():
    # Coordonnées par défaut
    DEFAULT_LATITUDE = 14.7226354457889
    DEFAULT_LONGITUDE = -17.2948732116772

    # Entrée utilisateur pour les coordonnées
    latitude = st.number_input("Latitude:", value=DEFAULT_LATITUDE)
    longitude = st.number_input("Longitude:", value=DEFAULT_LONGITUDE)

    # Création de la carte
    st.subheader("Carte")
    my_map = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup='Votre emplacement').add_to(my_map)
    folium_static(my_map)


if __name__ == "__main__":
    DfToGeoJson()
    afficher_carte_folium()
