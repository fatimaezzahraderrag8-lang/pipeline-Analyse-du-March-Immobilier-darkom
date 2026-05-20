import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
df = pd.read_csv("c:/pipeline  Analyse du Marché Immobilier darkom.ma/data_source/darkom-annonces.csv")
load_dotenv()  # installer .env
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"
engine = create_engine(DATABASE_URL)
print("conexion ok")
df.to_sql(
    "darkom_annonces_raw",
    engine,
    schema="staging",
    if_exists="replace",
    index=False
)
print("Data raw loaded successfully")