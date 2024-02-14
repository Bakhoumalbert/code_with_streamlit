import streamlit as st
import folium
from streamlit_folium import folium_static


def main():
    st.title("Application de Carte avec Streamlit")

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
    main()
