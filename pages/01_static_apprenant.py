import streamlit as st
import pandas as pd
import plotly.express as px
from Accueil import authentification

df1 = st.session_state.df1 = pd.read_csv("data/apprenant.csv", encoding= "utf-8")

def static_apprenant():
    st.title("Statistiques des apprenants")
    st.subheader("Cette page représente les statisques sur les apprenants")

    # Affichage du nombre d'apprenant
    nbre_app = df1['ID_DIM_APPRENANT'].nunique()
    st.markdown(f"<h3 style='color: #ff5733;'>Nombre d'apprennant : <span style='color: #007bff; font-weight: bold;'>{nbre_app}</span></h3>", unsafe_allow_html=True)    
        
    st.write(df1.iloc[:,:10])

    st.write("----------------")

    col1,_ ,col2 = st.columns((3, 0.2, 3)) 

    df1["DT_INSERTION"] = pd.to_datetime(df1["DT_INSERTION"])

    # Getting the min and max
    startDate = pd.to_datetime(df1["DT_INSERTION"]).min()
    endDate = pd.to_datetime(df1["DT_INSERTION"]).max()  # Correction de la valeur de endDate, max() au lieu de min()

    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    with col1:
        st.date_input("Start Date", startDate)
        # Création du graphique interactif avec Plotly Express
        fig = px.bar(df1['LB_SECTEUR'].value_counts(), 
                    x=df1['LB_SECTEUR'].value_counts().index, 
                    y=df1['LB_SECTEUR'].value_counts(),
                    labels={'x': 'Secteur', 'y': "Nombre d'apprenants"},
                    title='Répartition des apprenants par secteur',
                    color=df1['LB_SECTEUR'].value_counts().index)
        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig)

    with col2:
        st.date_input("End Date", endDate)
        # Affichage de la répartition des apprenants par sexe

        fig = px.pie(df1['SEXE'].value_counts(), 
                names=df1['SEXE'].value_counts().index, 
                values=df1['SEXE'].value_counts(),
                title='Répartition des apprenants par sexe',
                hole=0.5,
                color=df1['SEXE'].unique(),  # Utilisation des couleurs définies
                color_discrete_map={k: c for k, c in zip(df1['SEXE'].unique(), couleurs)})  # Attribution des couleurs
                # Personnalisation du graphique
        fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

        # Affichage du graphique interactif dans Streamlit
        st.plotly_chart(fig, use_container_width=True)



    # with col1:
    #     st.subheader("Filiere par secteur")
    #     fig = px.bar(secteur_df1, y="LB_FILIERE", x="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
    #     st.plotly_chart(fig, use_container_width=True, height=100)
        
    # Définition des couleurs pour les barres du graphique


    st.write("----------------")
    #st.title('Répartition des apprenants par Diplôme')
    # Création du graphique interactif avec Plotly Express
    fig = px.bar(df1['LB_DIPLOME'].value_counts(), 
                x=df1['LB_DIPLOME'].value_counts().index, 
                y=df1['LB_DIPLOME'].value_counts(),
                labels={'x': 'Diplôme', 'y': "Nombre d'apprenants"},
                title='Répartition des apprenants par diplôme',
                color=df1['LB_DIPLOME'].unique(),  # Utilisation des couleurs définies
                color_discrete_map={k: c for k, c in zip(df1['LB_DIPLOME'].unique(), couleurs)})  # Attribution des couleurs
    # Affichage du graphique interactif dans Streamlit
    st.plotly_chart(fig)

    st.write("----------------")
    # Création du graphique interactif avec Plotly Express
    fig = px.bar(df1['LB_FILIERE'].value_counts(), 
                y=df1['LB_FILIERE'].value_counts().index,  # Inversion de x et y pour afficher horizontalement
                x=df1['LB_FILIERE'].value_counts(),
                labels={'x': "Nombre d'apprenants", 'y': 'Filière'},
                title='Répartition des apprenants par filière',
                color=df1['LB_FILIERE'].unique(),  # Utilisation des couleurs définies
                color_discrete_map={k: c for k, c in zip(df1['LB_FILIERE'].unique(), couleurs)}) 

    # Supprimer la légende
    fig.update_layout(showlegend=False)

    # Affichage du graphique interactif dans Streamlit
    st.plotly_chart(fig)

    st.write("----------------")
    # Liste déroulante pour sélectionner la répartition
    repartition_selectionnee = st.selectbox("Sélectionnez une répartition :", ["Diplôme", "Genre", "Secteur d'activité", "Filière"])

    # Afficher les statistiques en fonction de la répartition sélectionnée
    if repartition_selectionnee == "Diplôme":
        fig = px.bar(df1, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition par diplôme')
    elif repartition_selectionnee == "Genre":
        fig = px.bar(df1, x='SEXE', color="SEXE", title='Répartition par genre')
    elif repartition_selectionnee == "Secteur d'activité":
        fig = px.bar(df1, x='LB_SECTEUR', color="LB_SECTEUR",title='Répartition par secteur d\'activité')
    elif repartition_selectionnee == "Filière":
        fig = px.bar(df1, x='LB_FILIERE', color="LB_FILIERE",title='Répartition par filière')
    
    # Afficher le diagramme en barres  
    st.plotly_chart(fig, use_container_width=True)

    col6, _,col7 = st.columns((3,0.2, 3)) 

    with col6:
        st.write("----------------")
        # Calcul des valeurs pour le diagramme circulaire
        secteurs_counts = df1.groupby('LB_FILIERE')['LB_SECTEUR'].value_counts().reset_index(name='count')
        # Création du graphique circulaire avec Plotly Express
        fig = px.pie(secteurs_counts, values='count', names='LB_SECTEUR', title='Répartition des secteurs par filière')
        # Affichage du graphique interactif dans Streamlit avec une largeur de conteneur automatique
        st.plotly_chart(fig, use_container_width=True)
    with col7:
        st.write("----------------")
        # Afficher le diagramme interactif en barres de la répartition des diplômes des apprenants
        fig = px.histogram(df1, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition des diplômes des apprenants')
        st.plotly_chart(fig, use_container_width=True)
    
if __name__ == "__main__":
    
    authenticated = False
    
    # Authentification
    if not authenticated:
        authenticated = authentification()
    else:
        static_apprenant()
    