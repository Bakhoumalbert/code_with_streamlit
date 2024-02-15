import psycopg2
import pandas as pd

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

requet_formateur = "SELECT * FROM \"FORMATION_PROF_DWH\".\"DIM_FORMATEUR\";"

params = {
        "dbname": "REFERENTIEL_MFPAI",
        "user": "postgres",
        "password": "ASB2101ab",
        "host": "localhost",
        "port": "5435"
    }
df = ConnectAndQuery(requet_formateur, params)

print(df)
