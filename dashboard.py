import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
import psycopg2
warnings.filterwarnings("ignore")

def Dashboard():

    # Informations de connexion à la base de données PostgreSQL
    dbname = "REFERENTIEL_MFPAI"
    user = "postgres"
    password = "ASB2101ab"
    host = "localhost"  # ou l'adresse IP de votre serveur PostgreSQL
    port = "5435"  # port par défaut de PostgreSQL

    # Connexion à la base de données PostgreSQL
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()

    # Exemple : exécuter une requête SELECT
    cursor.execute("SELECT * FROM \"FORMATION_PROF_DWH\".\"DIM_APPRENANT\";")
    # Récupérer les en-têtes de colonnes
    columns = [desc[0] for desc in cursor.description]

    # Récupérer les données
    rows = cursor.fetchall()

    # Créer un DataFrame
    df1 = pd.DataFrame(rows, columns=columns)

    #st.set_page_config(page_title="MFPAI Reporting", page_icon=":bar_chart:", layout="wide")

    # st.title(":bar_chart: Application Reporting MFPAI")
    # st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    fl = st.file_uploader(":file_folder: Télécharger un fichier", type=["csv", "txt", "xlsx", "xls"])

    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(fl, encoding="ISO-8859-1")  # Utilisation de l'objet file uploader directement pour lire le fichier
    else:
        os.chdir(r"C:\Users\Bakhoum\Desktop\S5\Stage\Documents_MFPAI\Données\scripts-jupiter")
        df = pd.read_csv("rep_apprenant.csv", encoding="ISO-8859-1", sep="|")

    col1, col2 = st.columns((2))  # Correction de la syntaxe pour définir le nombre de colonnes

    df["DT_INSERTION"] = pd.to_datetime(df1["DT_INSERTION"])

    # Getting the min and max
    startDate = pd.to_datetime(df1["DT_INSERTION"]).min()
    endDate = pd.to_datetime(df1["DT_INSERTION"]).max()  # Correction de la valeur de endDate, max() au lieu de min()

    with col1:
        date1 = st.date_input("Start Date", startDate)

    with col2:
        date2 = st.date_input("End Date", endDate)

    df = df1[(df1["DT_INSERTION"] >= pd.Timestamp(date1)) & (df1["DT_INSERTION"] <= pd.Timestamp(date2))].copy()  # Utilisation de pd.Timestamp pour convertir les dates

    st.sidebar.header("Choisissez votre filtre : ")
    centre = st.sidebar.multiselect("Centre de Formation", df1["NOM_CENTRE"].unique())
    # statut = st.sidebar.selectbox("Statut", ["En attente", "Validé", "Refusé"])

    if not centre:
        df2 = df1.copy()
    else:
        df2 = df1[df1["NOM_CENTRE"].isin(centre)]

    # Filtrage par secteur
    secteur = st.sidebar.multiselect("Secteur", df2["LB_SECTEUR"].unique())
    if not secteur:
        df3 = df2.copy()
    else:
        df3 = df2[df2["LB_SECTEUR"].isin(secteur)]

    # Filtrage par filière
    filiere = st.sidebar.multiselect("Filiere", df3["LB_FILIERE"].unique())
    if not filiere:
        df4 = df3.copy()
    else:
        df4 = df3[df3["LB_FILIERE"].isin(filiere)]

    # Filtrage de la base de données sur Centre, secteur et filiere
    if not centre and not secteur and filiere:
        filtered_df = df3[df3["LB_FILIERE"].isin(filiere)]
    elif not secteur and not filiere:
        filtered_df = df3[df3["NOM_CENTRE"].isin(centre)]
    elif not centre and not filiere:
        filtered_df = df3[df3["LB_SECTEUR"].isin(secteur)]
    elif centre and secteur:
        filtered_df = df3[df3["NOM_CENTRE"].isin(centre) & df3["LB_SECTEUR"].isin(secteur)]
    elif secteur and filiere:
        filtered_df = df3[df3["LB_SECTEUR"].isin(secteur) & df3["LB_FILIERE"].isin(filiere)]
    elif centre and filiere:
        filtered_df = df3[df3["NOM_CENTRE"].isin(centre) & df3["LB_FILIERE"].isin(filiere)]
    elif centre:
        filtered_df = df3[df3["NOM_CENTRE"].isin(centre)]
    else:
        filtered_df = df3[df3["NOM_CENTRE"].isin(centre) & df3["LB_SECTEUR"].isin(secteur) & df3["LB_FILIERE"].isin(filiere)]

    secteur_df = filtered_df.groupby(by=["LB_SECTEUR"], as_index=False)["LB_FILIERE"].sum()

    with col1:
        st.subheader("Filiere par secteur")
        fig = px.bar(secteur_df, x="LB_FILIERE", y="LB_SECTEUR", text="LB_FILIERE", template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height=100)

    with col2:
        st.subheader("Fiiere par secteur")
        fig = px.pie(filtered_df, values="LB_FILIERE", names="LB_SECTEUR", hole=0.5)
        fig.update_traces(textinfo="label+percent", insidetextorientation="radial")
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    Dashboard()
