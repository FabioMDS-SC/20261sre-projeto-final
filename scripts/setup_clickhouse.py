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
    """Tarefa 2.3: Tática de Heartbeat para validar saúde do serviço."""
    logger.info("Executando Heartbeat no ClickHouse...")
    client.command("SELECT 1")
    logger.info("Heartbeat OK: ClickHouse está acessível.")
    return True

def setup_clickhouse():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 8123))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DB", "northwind")

    try:
        # Cliente ClickHouse
        client = clickhouse_connect.get_client(host=host, port=port, username=user, password=password)

        # Validar conexão (Heartbeat)
        check_clickhouse_heartbeat(client)

        # Create Database
        client.command(f"CREATE DATABASE IF NOT EXISTS {database}")
        logger.info(f"Database '{database}' verificada/criada.")

        # Create Table: orders
        client.command(f"""
        CREATE TABLE IF NOT EXISTS {database}.orders (
            order_id Int64,
            customer_id String,
            employee_id Int64,
            order_date Date,
            required_date Date,
            shipped_date Nullable(Date),
            ship_via Int64,
            freight Float64,
            ship_name String,
            ship_address String,
            ship_city String,
            ship_region Nullable(String),
            ship_postal_code Nullable(String),
            ship_country String
        ) ENGINE = MergeTree()
        ORDER BY order_id
        """)
        logger.info("Tabela 'orders' verificada/criada.")

        # Create Table: order_details
        client.command(f"""
        CREATE TABLE IF NOT EXISTS {database}.order_details (
            order_id Int64,
            product_id Int64,
            unit_price Float64,
            quantity Int64,
            discount Float64
        ) ENGINE = MergeTree()
        ORDER BY (order_id, product_id)
        """)
        logger.info("Tabela 'order_details' verificada/criada.")

    except Exception as e:
        logger.critical(f"Falha no setup do ClickHouse: {str(e)}")

if __name__ == "__main__":
    setup_clickhouse()
