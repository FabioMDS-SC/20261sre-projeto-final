import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

def setup_clickhouse():
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = int(os.getenv("CLICKHOUSE_PORT", 8123))
    user = os.getenv("CLICKHOUSE_USER", "default")
    password = os.getenv("CLICKHOUSE_PASSWORD", "")
    database = os.getenv("CLICKHOUSE_DB", "northwind")

    client = clickhouse_connect.get_client(host=host, port=port, username=user, password=password)

    # Create Database
    client.command(f"CREATE DATABASE IF NOT EXISTS {database}")
    print(f"Database '{database}' verificada/criada.")

    # Create Table: orders
    # Engine MergeTree optimized for analytics
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
    print("Tabela 'orders' verificada/criada.")

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
    print("Tabela 'order_details' verificada/criada.")

if __name__ == "__main__":
    setup_clickhouse()
