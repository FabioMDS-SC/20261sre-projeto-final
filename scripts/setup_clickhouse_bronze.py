import os
import clickhouse_connect
from dotenv import load_dotenv
import logging
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
def check_clickhouse_heartbeat(client):
    """Tarefa 2.3: Tática de Heartbeat."""
    client.command("SELECT 1")
    return True

def setup_clickhouse_bronze():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 8123))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DB", "northwind")

    try:
        client = clickhouse_connect.get_client(host=host, port=port, username=user, password=password)
        check_clickhouse_heartbeat(client)

        client.command(f"CREATE DATABASE IF NOT EXISTS {database}")
        logger.info(f"Database '{database}' verificada/criada.")

        client.command(f"""
        CREATE TABLE IF NOT EXISTS {database}.ingestion (
            ingestion_timestamp DateTime64(3),
            data String,
            tag String
        ) ENGINE = MergeTree()
        ORDER BY (tag, ingestion_timestamp)
        """)
        logger.info("Tabela 'ingestion' (Bronze) verificada/criada.")

    except Exception as e:
        logger.critical(f"Falha no setup da camada Bronze: {str(e)}")

if __name__ == "__main__":
    setup_clickhouse_bronze()
