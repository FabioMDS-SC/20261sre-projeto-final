import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import glob
import logging
import time
from tenacity import retry, stop_after_attempt, wait_exponential

# Configuração de Logging conforme RNF-10 (Wave 2.2)
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

load_dotenv()

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
def check_minio_heartbeat(s3_client):
    """Tarefa 2.3: Tática de Heartbeat para validar saúde do serviço."""
    logger.info("Executando Heartbeat no MinIO...")
    s3_client.list_buckets()
    logger.info("Heartbeat OK: MinIO está acessível.")
    return True

def setup_minio():
    endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    bucket_raw = os.getenv("MINIO_BUCKET_RAW", "raw")
    bucket_processed = os.getenv("MINIO_BUCKET_PROCESSED", "processed")

    try:
        # Inicialização do Cliente
        s3 = boto3.resource('s3',
                            endpoint_url=f"http://{endpoint}",
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key,
                            config=Config(signature_version='s3v4'),
                            region_name='us-east-1')
        
        # Validar conexão (Heartbeat)
        check_minio_heartbeat(s3.meta.client)

        # Criar buckets
        for bucket_name in [bucket_raw, bucket_processed]:
            bucket = s3.Bucket(bucket_name)
            try:
                s3.meta.client.head_bucket(Bucket=bucket_name)
                logger.info(f"Bucket '{bucket_name}' já existe.")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == '404':
                    s3.create_bucket(Bucket=bucket_name)
                    logger.info(f"Bucket '{bucket_name}' criado com sucesso.")
                else:
                    raise e

        # Upload dos CSVs
        csv_files = glob.glob("dados_northwind/*.csv")
        if not csv_files:
            logger.warning("Nenhum arquivo CSV encontrado em dados_northwind/.")
        
        for file_path in csv_files:
            file_name = os.path.basename(file_path)
            try:
                logger.info(f"Enviando {file_name} para MinIO...")
                s3.Bucket(bucket_raw).upload_file(file_path, file_name)
                logger.info(f"Sucesso: {file_name} enviado para bucket {bucket_raw}.")
            except Exception as e:
                logger.error(f"Erro ao enviar {file_name}: {str(e)}")

    except Exception as e:
        logger.critical(f"Falha no setup do MinIO: {str(e)}")

if __name__ == "__main__":
    setup_minio()
