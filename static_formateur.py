import streamlit as st
from connect_DB import  ConnectAndQuery
import plotly.express as px
import pandas as pd


def static_formateur():

    df2 = pd.read_csv("formateur.csv")
    # 1. Répartition par centre de formation
    nbre_formateur = df2['ID_FORMATEUR'].nunique()
    
    st.write("nombre de formateur : ", nbre_formateur)
    st.write(df2)

    col1, col2 = st.columns((1, 1)) 

    df2["DT_INSERTION"] = pd.to_datetime(df2["DT_INSERTION"])

    # Getting the min and max
    startDate = pd.to_datetime(df2["DT_INSERTION"]).min()
    endDate = pd.to_datetime(df2["DT_INSERTION"]).max()  # Correction de la valeur de endDate, max() au lieu de min()

    with col1:
        st.date_input("Start Date", startDate)

    st.markdown("&nbsp;" * 10)

    with col2:
        st.date_input("End Date", endDate)

    # with col1:
    #     st.subheader("Filiere par secteur")
    #     fig = px.bar(secteur_df2, y="LB_FILIERE", x="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
    #     st.plotly_chart(fig, use_container_width=True, height=100)
        
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    with col1:
        # Création du graphique interactif avec Plotly Express
        fig = px.bar(df2['STATUS'].value_counts(), 
                    x=df2['STATUS'].value_counts().index, 
                    y=df2['STATUS'].value_counts(),
                    labels={'x': 'Status', 'y': "Nombre de formateur"},
                    title='Répartition des formateurs par status',
                    color=df2['STATUS'].value_counts().index)
        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)

    with col2:
        #st.title('Répartition des formateur par sexe')
        # Création du graphique interactif avec Plotly Express
        fig = px.pie(df2['SEXE'].value_counts(), 
                    names=df2['SEXE'].value_counts().index, 
                    values=df2['SEXE'].value_counts(),
                    title='Répartition des formateur par sexe',
                    hole=0.5,
                    color=df2['SEXE'].unique(),  # Utilisation des couleurs définies
                    color_discrete_map={k: c for k, c in zip(df2['SEXE'].unique(), couleurs)})  # Attribution des couleurs

        # Personnalisation du graphique
        fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

    with col1:
        #st.title('Répartition des formateur par Diplôme')
        # Création du graphique interactif avec Plotly Express
        fig = px.bar(df2['GRADE_ECHELON'].value_counts(), 
                    x=df2['GRADE_ECHELON'].value_counts().index, 
                    y=df2['GRADE_ECHELON'].value_counts(),
                    labels={'x': 'Grade', 'y': "Nombre d'formateur"},
                    title='Répartition des formateur par diplôme',
                    color=df2['GRADE_ECHELON'].unique(),  # Utilisation des couleurs définies
                    color_discrete_map={k: c for k, c in zip(df2['GRADE_ECHELON'].unique(), couleurs)})  # Attribution des couleurs
        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)

   

    
    # Création du graphique interactif avec Plotly Express
    fig = px.bar(df2['CATEGORIE'].value_counts(), 
                y=df2['CATEGORIE'].value_counts().index,  # Inversion de x et y pour afficher horizontalement
                x=df2['CATEGORIE'].value_counts(),
                labels={'x': "Nombre de formateur", 'y': 'Catégorie'},
                title='Répartition des formateur par Centre de formation',
                color=df2['CATEGORIE'].unique(),  # Utilisation des couleurs définies
                color_discrete_map={k: c for k, c in zip(df2['CATEGORIE'].unique(), couleurs)}) 

    # Supprimer la légende
    fig.update_layout(showlegend=False)

    # Affichage du graphique interactif dans Streamlit
    st.plotly_chart(fig)


    # Liste déroulante pour sélectionner la répartition
    repartition_selectionnee = st.selectbox("Sélectionnez une répartition :", ["Catégorie", "Status", "Grade/Echelon", "Centre de formation"])

    # Afficher les statistiques en fonction de la répartition sélectionnée
    if repartition_selectionnee == "Catégorie":
        fig = px.bar(df2, x='CATEGORIE', color="CATEGORIE", title='Répartition par catégorie')
    elif repartition_selectionnee == "Status":
        fig = px.bar(df2, x='STATUS', color="STATUS", title='Répartition par Status')
    elif repartition_selectionnee == "Grade/Echelon":
        fig = px.bar(df2, x='GRADE_ECHELON', color="GRADE_ECHELON",title='Répartition par Grade/Echelon')
    elif repartition_selectionnee == "Centre de formation":
        fig = px.bar(df2, x='NOM_CENTRE', color="NOM_CENTRE",title='Répartition par Centre de formation')
    
    # # Afficher les statistiques
    # st.write(stats)
    # Afficher le diagramme en barres  
    st.plotly_chart(fig, use_container_width=True)

    col6, col7 = st.columns((1, 1)) 

    # with col6:
    #     # Afficher le diagramme interactif en barres des secteurs en fonction des Centre de formations
    #     st.subheader("Secteurs en fonction des Centre de formations")
    #     fig = px.histogram(df2, x='LB_FILIERE', color='LB_SECTEUR', title='Secteurs en fonction des Centre de formations')
    #     st.plotly_chart(fig, use_container_width=True)

    # with col7:
    #     # Afficher le diagramme interactif en barres de la répartition des diplômes des formateur
    #     st.subheader("Répartition des diplômes des formateur")
    #     fig = px.histogram(df2, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition des diplômes des formateur')
    #     st.plotly_chart(fig, use_container_width=True)

    with col6:
        # Afficher le diagramme interactif circulaire de la répartition des formateur par sexe
        st.subheader("Répartition des formateur par Département")
        fig = px.pie(df2, names='DEPARTEMENT', title='Répartition des formateur par Département')
        st.plotly_chart(fig, use_container_width=True)
   
    with col7:
        # Afficher le diagramme interactif en barres du nombre d'formateur par Centre de formation
        st.subheader("Nombre de formateur par Région")
        fig = px.histogram(df2, x='REGION', color="REGION", title='Nombre d\'formateur par Région')
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    static_formateur()