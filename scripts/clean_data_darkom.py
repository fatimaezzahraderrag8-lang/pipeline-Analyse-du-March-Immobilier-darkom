#charge library et fonction:
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys
import matplotlib.pyplot as plt
sys.path.append(r"c:\pipeline  Analyse du Marché Immobilier darkom.ma\scripts")
from fonction_outlier import *
from fonction_categorie_prix import categorize_price
from fonction_categorie_surface import categorize_surface
#connexion:
load_dotenv()  # installer .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL)
print("conexion ok")
df=pd.read_sql("select * from staging.darkom_annonces_raw",engine)
#correction types de données:
df['date_publication']=pd.to_datetime(df['date_publication'],errors='coerce')
df['nb_salles_bain']=pd.to_numeric(df['nb_salles_bain'],errors='coerce')
df['nb_chambres']=pd.to_numeric(df['nb_chambres'],errors='coerce')
df['etage']=pd.to_numeric(df['etage'],errors='coerce')
#supprimer doubllonts:
df=df.drop_duplicates()
#les valeur null 
df = df.fillna({'date_publication':df['date_publication'].ffill(),
          'annee_construction':df['annee_construction'].bfill()     
})     
df = df.fillna({
    'quartier':df['quartier'].mode()[0],
    'type_bien':df['type_bien'].mode()[0],
    'transaction':df['transaction'].mode()[0]
    })
df=df.fillna({
    'nb_chambres':df['nb_chambres'].median(),
    'nb_salles_bain':df['nb_salles_bain'].median(),
    'etage':df['etage'].median()
})
#graph prix 
plt.figure(figsize=(10,5))
plt.plot(df["prix"].values)
plt.title("prix distribution")
plt.xlabel("Index")
plt.ylabel("prix")
plt.grid()
plt.show()
# applique la fonction
df = detect_outliers_grouped(
    df,
    "prix",
    ["nb_chambres", "surface"]
)
# supprimer outliers:
df = df[df["outlier"] == False]
# supprimer colonne
df = df.drop("outlier", axis=1)
#Standardisation des données
df["ville"]=df["ville"].str.strip().str.lower().replace("casa","casablanca")
df["type_bien"]=df["type_bien"].str.strip().str.lower()
unique=df["ville"].unique()
print(unique)
###Feature Engineering
df["prix_m2"] = df["prix"] / df["surface"]
df["age_bien"] = 2026 - df["annee_construction"]
#applique fonction categorie prix:
df["categorie_prix"] = df["prix"].apply(categorize_price)
#applique fonction categorie surface:
df['categorie_surface'] = df['surface'].apply(categorize_surface)
df["annee"] = df["date_publication"].dt.year
df["mois"] = df["date_publication"].dt.month
df["trimestre"] = df["date_publication"].dt.quarter
#save csv 
df.to_sql(
    "darkom_annonces_clean",
    engine,
    schema="clean",
    if_exists="replace",
    index=False
)