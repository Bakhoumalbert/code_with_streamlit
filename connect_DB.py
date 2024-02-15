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

            df.to_csv('data/ods_centre.csv', index=False)
            return (geojson_data, df)


        else:
            print("Aucune donnée disponible.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None


requet_formateur = "SELECT * FROM \"FORMATION_PROF_DWH\".\"DIM_FORMATEUR\";"
requet_apprenant = "SELECT * FROM \"FORMATION_PROF_DWH\".\"DIM_APPRENANT\";"
requet_centre = "SELECT * FROM \"FORMATION_ODS\".\"ODS_CENTRE_FP\";"


params = {
        "dbname": "REFERENTIEL_MFPAI",
        "user": "postgres",
        "password": "ASB2101ab",
        "host": "localhost",
        "port": "5435"
    }
    
try:
    df = ConnectAndQuery(requet_centre, params)
    df.to_csv('data/ods_centre.csv', index=False)
    df1 = ConnectAndQuery(requet_apprenant, params)
    df1.to_csv('data/apprenant.csv', index=False)
    df2 = ConnectAndQuery(requet_formateur, params)
    df2.to_csv('data/formateur.csv', index=False)

except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")
