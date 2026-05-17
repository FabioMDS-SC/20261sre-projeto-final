import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import glob

load_dotenv()

def setup_minio():
    endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    bucket_raw = os.getenv("MINIO_BUCKET_RAW", "raw")
    bucket_processed = os.getenv("MINIO_BUCKET_PROCESSED", "processed")

    # Connect to MinIO (ensure use_ssl is False for local dev)
    s3 = boto3.resource('s3',
                        endpoint_url=f"http://{endpoint}",
                        aws_access_key_id=access_key,
                        aws_secret_access_key=secret_key,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')

    # Create buckets if they don't exist
    for bucket_name in [bucket_raw, bucket_processed]:
        bucket = s3.Bucket(bucket_name)
        if bucket.creation_date:
            print(f"Bucket '{bucket_name}' já existe.")
        else:
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso.")

    # Upload local CSVs to MinIO 'raw' bucket
    csv_files = glob.glob("dados_northwind/*.csv")
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        print(f"Enviando {file_name} para MinIO...")
        s3.Bucket(bucket_raw).upload_file(file_path, file_name)
        print(f"{file_name} enviado.")

if __name__ == "__main__":
    setup_minio()
