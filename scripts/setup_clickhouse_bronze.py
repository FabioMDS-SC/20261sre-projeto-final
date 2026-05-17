import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

def setup_clickhouse_bronze():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 8123))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DB", "northwind")

    client = clickhouse_connect.get_client(host=host, port=port, username=user, password=password)

    # Create Database
    client.command(f"CREATE DATABASE IF NOT EXISTS {database}")
    print(f"Database '{database}' verificada/criada.")

    # Create Table: ingestion (Bronze Layer)
    # Using JSON type (available in newer ClickHouse versions) or String for max compatibility
    # Given the request for jsonb style, we'll use the 'String' type which ClickHouse handles 
    # well with JSON functions, or the 'JSON' object type if enabled.
    # To ensure stability, we'll use String and treat it as JSON in queries.
    
    client.command(f"""
    CREATE TABLE IF NOT EXISTS {database}.ingestion (
        ingestion_timestamp DateTime64(3),
        data String,
        tag String
    ) ENGINE = MergeTree()
    ORDER BY (tag, ingestion_timestamp)
    """)
    print("Tabela 'ingestion' (Bronze) verificada/criada.")

if __name__ == "__main__":
    setup_clickhouse_bronze()
