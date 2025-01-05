import os
import urllib3
from minio import Minio
from dotenv import load_dotenv

ENV_PATH = "../../.env"
load_dotenv(dotenv_path=ENV_PATH)
urllib3.disable_warnings()
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
SECRET_KEY = os.getenv("MINIO_SECRET_ACCESS_KEY")
URL = os.getenv("MINIO_URL")
TLS = os.getenv("MINIO_TLS")
BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
SOURCE_FILE = os.getenv("MINIO_SOURCE_FILE")
DEST_FILE = os.getenv("MINIO_DEST_FILE")

def main():
    client = Minio(endpoint=URL, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=TLS, cert_check= not TLS)
    if not client.bucket_exists(BUCKET_NAME):
        print("Bucket does not exist")
        return 0
    try:
        client.fput_object(BUCKET_NAME, DEST_FILE, SOURCE_FILE)
        print(f"File {SOURCE_FILE} uploaded to {URL}/{BUCKET_NAME}/{DEST_FILE}")
    except Exception as e:
        print(f"Error when uploading file to {URL}/{BUCKET_NAME}/{DEST_FILE}: {e}")

if __name__ == "__main__":
    main()