import os
import urllib3
from minio import Minio
from dotenv import load_dotenv
import pandas as pd
import copy

ENV_PATH = "../../.env"
load_dotenv(dotenv_path=ENV_PATH)
urllib3.disable_warnings()
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
URL = os.getenv("MINIO_URL")
TLS = os.getenv("MINIO_TLS")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
INGEST_SOURCE_FILE = "car.data"
INGEST_DEST_FILE = "../../data/processed/data.csv"
INGEST_INDEX_LABEL = "index"
INGEST_SEP = "\t"

def main():
    client = Minio(endpoint=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=TLS, cert_check= not TLS)
    if not client.bucket_exists(BUCKET_NAME):
        print("Bucket does not exist")
        return 0
    try:
        res=client.get_object(BUCKET_NAME, INGEST_SOURCE_FILE)
        data = copy.deepcopy(res.data.decode("utf-8"))
        data = pd.DataFrame([row.split(",") for row in data.splitlines()])
        data.to_csv(INGEST_DEST_FILE, index_label=INGEST_INDEX_LABEL, sep=INGEST_SEP)
        print(f"File {INGEST_SOURCE_FILE} downloaded and converted to {INGEST_DEST_FILE}")
    except Exception as e:
        print(f"Error when downloading file from {URL}/{BUCKET_NAME}/{INGEST_SOURCE_FILE}: {e}")

if __name__ == "__main__":
    main()