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
# connexxion
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL)
print("Connexion OK")

# create tables
try:
    with engine.begin() as conn:
        conn.execute(text(""" drop schema if exists bi_schema cascade; """))
        conn.execute(text("""create schema bi_schema;"""))
        # dim temps
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bi_schema.dim_temps (
                date_id SERIAL PRIMARY KEY,
                date_publication DATE,
                trimestre INT,
                mois INT,
                annee INT
            );
        """))
        # dim localisation
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bi_schema.dim_localisation (
                localisation_id SERIAL PRIMARY KEY,
                ville VARCHAR(100),
                quartier VARCHAR(150)
            );
        """))
        # dim bien
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bi_schema.dim_bien (
                bien_id SERIAL PRIMARY KEY,
                type_bien VARCHAR(100),
                transaction VARCHAR(50),
                categorie_prix VARCHAR(50),
                categorie_surface VARCHAR(50)
            );
        """))
        # dim_caracteristiques
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bi_schema.dim_caracteristiques (
                caracteristique_id SERIAL PRIMARY KEY,
                nb_chambres INT,
                nb_salles_bain INT,
                etage INT
            );
        """))
        # fact table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bi_schema.fact_annonces (
                fact_annonce_id SERIAL PRIMARY KEY,

                date_id INT REFERENCES bi_schema.dim_temps(date_id),

                localisation_id INT REFERENCES bi_schema.dim_localisation(localisation_id),

                bien_id INT REFERENCES bi_schema.dim_bien(bien_id),

                caracteristique_id INT REFERENCES bi_schema.dim_caracteristiques(caracteristique_id),

                prix NUMERIC,
                surface NUMERIC,
                prix_m2 NUMERIC,
                age_bien NUMERIC
            );
        """))

    print("Tables created successfully")

except Exception as e:
    print("Error :", e)