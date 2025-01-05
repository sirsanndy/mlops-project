import os
import urllib3
from minio import Minio
from dotenv import load_dotenv
import pandas as pd
import copy
from sqlalchemy import create_engine

ENV_PATH = "../../.env"
load_dotenv(dotenv_path=ENV_PATH)


USR = os.getenv("POSTGRES_USER")
USR_PWD = os.getenv("POSTGRES_PASSWORD")
HST = os.getenv("POSTGRES_HOST")
PRT = os.getenv("POSTGRES_PORT")
DB = os.getenv("POSTGRES_DATABASE")
URL = f"postgresql://{USR}:{USR_PWD}@{HST}:{PRT}/{DB}"

INGEST_DEST_FILE = "../../data/processed/car_postgres.csv"
INGEST_INDEX_LABEL = "index"
INGEST_SEP = "\t"

def main():
    try:
        engine = create_engine(URL)
        query = "SELECT * FROM car"
        data = pd.read_sql_query(query, engine)
        data.to_csv(INGEST_DEST_FILE, index_label=INGEST_INDEX_LABEL, sep=INGEST_SEP)
        print(f"Ingesting data from Postgres {URL} downloaded and converted to {INGEST_DEST_FILE}")
    except Exception as e:
        print(f"Error when downloading file from {URL}: {e}")

if __name__ == "__main__":
    main()