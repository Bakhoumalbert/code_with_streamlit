import streamlit as st
from static_formateur import static_formateur
from static_apprenant import static_apprenant
from home import accueil
import streamlit as st
import folium
import pandas as pd
from streamlit_folium import folium_static


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

      
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    # with col1:
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.bar(df2['STATUS'].value_counts(), 
    #                 x=df2['STATUS'].value_counts().index, 
    #                 y=df2['STATUS'].value_counts(),
    #                 labels={'x': 'Status', 'y': "Nombre de formateur"},
    #                 title='Répartition des formateurs par status',
    #                 color=df2['STATUS'].value_counts().index)
    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig)

    # with col2:
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.pie(df2['SEXE'].value_counts(), 
    #                 names=df2['SEXE'].value_counts().index, 
    #                 values=df2['SEXE'].value_counts(),
    #                 title='Répartition des formateur par sexe',
    #                 hole=0.5,
    #                 color=df2['SEXE'].unique(),  # Utilisation des couleurs définies
    #                 color_discrete_map={k: c for k, c in zip(df2['SEXE'].unique(), couleurs)})  # Attribution des couleurs

    #     # Personnalisation du graphique
    #     fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig, use_container_width=True)

    # with col1:
    #     #st.title('Répartition des formateur par Diplôme')
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.bar(df2['GRADE_ECHELON'].value_counts(), 
    #                 x=df2['GRADE_ECHELON'].value_counts().index, 
    #                 y=df2['GRADE_ECHELON'].value_counts(),
    #                 labels={'x': 'Grade', 'y': "Nombre d'formateur"},
    #                 title='Répartition des formateur par diplôme',
    #                 color=df2['GRADE_ECHELON'].unique(),  # Utilisation des couleurs définies
    #                 color_discrete_map={k: c for k, c in zip(df2['GRADE_ECHELON'].unique(), couleurs)})  # Attribution des couleurs
    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig)

   

    
    # # Création du graphique interactif avec Plotly Express
    # fig = px.bar(df2['CATEGORIE'].value_counts(), 
    #             y=df2['CATEGORIE'].value_counts().index,  # Inversion de x et y pour afficher horizontalement
    #             x=df2['CATEGORIE'].value_counts(),
    #             labels={'x': "Nombre de formateur", 'y': 'Catégorie'},
    #             title='Répartition des formateur par Centre de formation',
    #             color=df2['CATEGORIE'].unique(),  # Utilisation des couleurs définies
    #             color_discrete_map={k: c for k, c in zip(df2['CATEGORIE'].unique(), couleurs)}) 

    # # Supprimer la légende
    # fig.update_layout(showlegend=False)

    # # Affichage du graphique interactif dans Streamlit
    # st.plotly_chart(fig)


    # # Liste déroulante pour sélectionner la répartition
    # repartition_selectionnee = st.selectbox("Sélectionnez une répartition :", ["Catégorie", "Status", "Grade/Echelon", "Centre de formation"])

    # # Afficher les statistiques en fonction de la répartition sélectionnée
    # if repartition_selectionnee == "Catégorie":
    #     fig = px.bar(df2, x='CATEGORIE', color="CATEGORIE", title='Répartition par catégorie')
    # elif repartition_selectionnee == "Status":
    #     fig = px.bar(df2, x='STATUS', color="STATUS", title='Répartition par Status')
    # elif repartition_selectionnee == "Grade/Echelon":
    #     fig = px.bar(df2, x='GRADE_ECHELON', color="GRADE_ECHELON",title='Répartition par Grade/Echelon')
    # elif repartition_selectionnee == "Centre de formation":
    #     fig = px.bar(df2, x='NOM_CENTRE', color="NOM_CENTRE",title='Répartition par Centre de formation')
    
    # # # Afficher les statistiques
    # # st.write(stats)
    # # Afficher le diagramme en barres  
    # st.plotly_chart(fig, use_container_width=True)

    # col6, col7 = st.columns((1, 1)) 

    # # with col6:
    # #     # Afficher le diagramme interactif en barres des secteurs en fonction des Centre de formations
    # #     st.subheader("Secteurs en fonction des Centre de formations")
    # #     fig = px.histogram(df2, x='LB_FILIERE', color='LB_SECTEUR', title='Secteurs en fonction des Centre de formations')
    # #     st.plotly_chart(fig, use_container_width=True)

    # # with col7:
    # #     # Afficher le diagramme interactif en barres de la répartition des diplômes des formateur
    # #     st.subheader("Répartition des diplômes des formateur")
    # #     fig = px.histogram(df2, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition des diplômes des formateur')
    # #     st.plotly_chart(fig, use_container_width=True)

    # with col6:
    #     # Afficher le diagramme interactif circulaire de la répartition des formateur par sexe
    #     st.subheader("Répartition des formateur par Département")
    #     fig = px.pie(df2, names='DEPARTEMENT', title='Répartition des formateur par Département')
    #     st.plotly_chart(fig, use_container_width=True)
   
    # with col7:
    #     # Afficher le diagramme interactif en barres du nombre d'formateur par Centre de formation
    #     st.subheader("Nombre de formateur par Région")
    #     fig = px.histogram(df2, x='REGION', color="REGION", title='Nombre d\'formateur par Région')
    #     st.plotly_chart(fig, use_container_width=True)

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
    
def static_apprenant():

    st.title("Statistiques des apprenants")
    st.write("Cette page représente les statisques sur les apprenants")
    
    df1 = pd.read_csv("apprenant.csv")

    st.write(df1)

    col1, col2 = st.columns((1, 1)) 

    df1["DT_INSERTION"] = pd.to_datetime(df1["DT_INSERTION"])

    # Getting the min and max
    startDate = pd.to_datetime(df1["DT_INSERTION"]).min()
    endDate = pd.to_datetime(df1["DT_INSERTION"]).max()  # Correction de la valeur de endDate, max() au lieu de min()

    with col1:
        st.date_input("Start Date", startDate)

    st.markdown("&nbsp;" * 10)

    with col2:
        st.date_input("End Date", endDate)

    # with col1:
    #     st.subheader("Filiere par secteur")
    #     fig = px.bar(secteur_df1, y="LB_FILIERE", x="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
    #     st.plotly_chart(fig, use_container_width=True, height=100)
        
    # Définition des couleurs pour les barres du graphique
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    # with col1:
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.bar(df1['LB_SECTEUR'].value_counts(), 
    #                 x=df1['LB_SECTEUR'].value_counts().index, 
    #                 y=df1['LB_SECTEUR'].value_counts(),
    #                 labels={'x': 'Secteur', 'y': "Nombre d'apprenants"},
    #                 title='Répartition des apprenants par secteur',
    #                 color=df1['LB_SECTEUR'].value_counts().index)
    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig)

    # with col2:
    #     #st.title('Répartition des apprenants par sexe')
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.pie(df1['SEXE'].value_counts(), 
    #                 names=df1['SEXE'].value_counts().index, 
    #                 values=df1['SEXE'].value_counts(),
    #                 title='Répartition des apprenants par sexe',
    #                 hole=0.5,
    #                 color=df1['SEXE'].unique(),  # Utilisation des couleurs définies
    #                 color_discrete_map={k: c for k, c in zip(df1['SEXE'].unique(), couleurs)})  # Attribution des couleurs

    #     # Personnalisation du graphique
    #     fig.update_traces(textinfo="label+percent", insidetextorientation="radial")

    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig, use_container_width=True)

    # with col1:
    #     #st.title('Répartition des apprenants par Diplôme')
    #     # Création du graphique interactif avec Plotly Express
    #     fig = px.bar(df1['LB_DIPLOME'].value_counts(), 
    #                 x=df1['LB_DIPLOME'].value_counts().index, 
    #                 y=df1['LB_DIPLOME'].value_counts(),
    #                 labels={'x': 'Diplôme', 'y': "Nombre d'apprenants"},
    #                 title='Répartition des apprenants par diplôme',
    #                 color=df1['LB_DIPLOME'].unique(),  # Utilisation des couleurs définies
    #                 color_discrete_map={k: c for k, c in zip(df1['LB_DIPLOME'].unique(), couleurs)})  # Attribution des couleurs
    #     # Affichage du graphique interactif dans Streamlit
    #     st.plotly_chart(fig)
    
    # # Création du graphique interactif avec Plotly Express
    # fig = px.bar(df1['LB_FILIERE'].value_counts(), 
    #             y=df1['LB_FILIERE'].value_counts().index,  # Inversion de x et y pour afficher horizontalement
    #             x=df1['LB_FILIERE'].value_counts(),
    #             labels={'x': "Nombre d'apprenants", 'y': 'Filière'},
    #             title='Répartition des apprenants par filière',
    #             color=df1['LB_FILIERE'].unique(),  # Utilisation des couleurs définies
    #             color_discrete_map={k: c for k, c in zip(df1['LB_FILIERE'].unique(), couleurs)}) 

    # # Supprimer la légende
    # fig.update_layout(showlegend=False)

    # # Affichage du graphique interactif dans Streamlit
    # st.plotly_chart(fig)


    # # Liste déroulante pour sélectionner la répartition
    # repartition_selectionnee = st.selectbox("Sélectionnez une répartition :", ["Diplôme", "Genre", "Secteur d'activité", "Filière"])

    # # Afficher les statistiques en fonction de la répartition sélectionnée
    # if repartition_selectionnee == "Diplôme":
    #     fig = px.bar(df1, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition par diplôme')
    # elif repartition_selectionnee == "Genre":
    #     fig = px.bar(df1, x='SEXE', color="SEXE", title='Répartition par genre')
    # elif repartition_selectionnee == "Secteur d'activité":
    #     fig = px.bar(df1, x='LB_SECTEUR', color="LB_SECTEUR",title='Répartition par secteur d\'activité')
    # elif repartition_selectionnee == "Filière":
    #     fig = px.bar(df1, x='LB_FILIERE', color="LB_FILIERE",title='Répartition par filière')
    
    # # # Afficher les statistiques
    # # st.write(stats)
    # # Afficher le diagramme en barres  
    # st.plotly_chart(fig, use_container_width=True)

    # col6, col7 = st.columns((1, 1)) 

    # with col6:
    #     # Calcul des valeurs pour le diagramme circulaire
    #     secteurs_counts = df1.groupby('LB_FILIERE')['LB_SECTEUR'].value_counts().reset_index(name='count')
    #     # Création du graphique circulaire avec Plotly Express
    #     fig = px.pie(secteurs_counts, values='count', names='LB_SECTEUR', title='Répartition des secteurs par filière')
    #     # Affichage du graphique interactif dans Streamlit avec une largeur de conteneur automatique
    #     st.plotly_chart(fig, use_container_width=True)
    # with col7:
    #     # Afficher le diagramme interactif en barres de la répartition des diplômes des apprenants
    #     fig = px.histogram(df1, x='LB_DIPLOME', color="LB_DIPLOME", title='Répartition des diplômes des apprenants')
    #     st.plotly_chart(fig, use_container_width=True)
    
    # # Afficher le diagramme interactif en barres du nombre d'apprenants par filière
    # fig = px.histogram(df1, x='LB_FILIERE', color="LB_FILIERE", title='Nombre d\'apprenants par filière')
    # st.plotly_chart(fig, use_container_width=True)
    


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
