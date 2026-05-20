import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
# load env
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL)
print("Connexion OK")
# load data
df=pd.read_sql("select * from clean.darkom_annonces_clean",engine)
# insert dim_localisation
localisation_df = df[['ville', 'quartier']].drop_duplicates()
localisation_df.to_sql(
    "dim_localisation",
    engine,
    schema="bi_schema",
    if_exists="append",
    index=False
)
print("dim_localisation inserted")
# insert dim_temps
df['date_publication'] = pd.to_datetime(df['date_publication'])
temps_df = pd.DataFrame({
    'date_publication': df['date_publication'],
    'trimestre': df['date_publication'].dt.quarter,
    'mois': df['date_publication'].dt.month,
    'annee': df['date_publication'].dt.year
}).drop_duplicates()
temps_df.to_sql(
    "dim_temps",
    engine,
    schema="bi_schema",
    if_exists="append",
    index=False
)
print("dim_temps inserted")
# insert dim_bien
bien_df = df[[
    'type_bien',
    'transaction',
    'categorie_prix',
    'categorie_surface'
]].drop_duplicates()
bien_df.to_sql(
    "dim_bien",
    engine,
    schema="bi_schema",
    if_exists="append",
    index=False
)
print("dim_bien insert")
#insert caracteristique
car_df = df[[
    'nb_chambres',
    'nb_salles_bain',
    'etage'
]].drop_duplicates()
car_df.to_sql(
    "dim_caracteristiques",
    engine,
    schema="bi_schema",
    if_exists="append",
    index=False
)
print("dim_caracteristiques insert")
#===========
# load dimention
dim_temps = pd.read_sql(
    "SELECT * FROM bi_schema.dim_temps",
    engine
)
dim_localisation = pd.read_sql(
    "SELECT * FROM bi_schema.dim_localisation",
    engine
)
dim_bien = pd.read_sql(
    "SELECT * FROM bi_schema.dim_bien",
    engine
)
dim_car = pd.read_sql(
    "SELECT * FROM bi_schema.dim_caracteristiques",
    engine
)
# convertir dates
df['date_publication'] = pd.to_datetime(df['date_publication'])
dim_temps['date_publication'] = pd.to_datetime(dim_temps['date_publication'])

# merge
df = df.merge(
    dim_temps,
    on='date_publication',
    how='left'
)
# merge dim_localisation
df = df.merge(
    dim_localisation,
    on=['ville', 'quartier'],
    how='left'
)
# merge dim_bien
df = df.merge(
    dim_bien,
    on=[
        'type_bien',
        'transaction',
        'categorie_prix',
        'categorie_surface'
    ],
    how='left'
)
# merge dim_caracteristique
df = df.merge(
    dim_car,
    on=[
        'nb_chambres',
        'nb_salles_bain',
        'etage'
    ],
    how='left'
)
#create fact_tabe data frame
fact_df = df[[
    'date_id',
    'localisation_id',
    'bien_id',
    'caracteristique_id',
    'prix',
    'surface',
    'prix_m2',
    'age_bien'
]].drop_duplicates()
# insert fact_table
fact_df.to_sql(
    "fact_annonces",
    engine,
    schema="bi_schema",
    if_exists="append",
    index=False
)
print("fact_annonces insert successfully")