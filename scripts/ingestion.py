import os
import duckdb
import clickhouse_connect
from dotenv import load_dotenv
import time
from datetime import datetime
import json

load_dotenv()

def run_ingestion():
    # Configurações
    ch_host = os.getenv("CLICKHOUSE_HOST", "localhost")
    ch_port = int(os.getenv("CLICKHOUSE_PORT", 8123))
    ch_user = os.getenv("CLICKHOUSE_USER", "default")
    ch_pass = os.getenv("CLICKHOUSE_PASSWORD", "")
    ch_db = os.getenv("CLICKHOUSE_DB", "northwind")
    
    csv_dir = "dados_northwind"
    
    # Cliente ClickHouse
    client = clickhouse_connect.get_client(host=ch_host, port=ch_port, username=ch_user, password=ch_pass)

    # Inicializar DuckDB
    con = duckdb.connect(database=':memory:')

    print(f"🚀 Iniciando ingestão de CSVs para a tabela {ch_db}.ingestion...")

    for file_name in os.listdir(csv_dir):
        if file_name.endswith(".csv"):
            file_path = os.path.join(csv_dir, file_name)
            print(f"📄 Processando arquivo: {file_name}")

            # Usar DuckDB para ler o CSV e converter cada linha em um objeto JSON
            # A query abaixo transforma as colunas do CSV em uma struct e depois em JSON string
            query = f"""
                SELECT 
                    current_timestamp as ingestion_timestamp,
                    CAST(to_json(t) AS TEXT) as data,
                    '{file_name}' as tag
                FROM read_csv_auto('{file_path}') t
            """
            
            df = con.execute(query).df()
            
            # Inserir no ClickHouse
            client.insert_df(f"{ch_db}.ingestion", df)
            
            print(f"✅ {len(df)} linhas inseridas de {file_name}")

    print("🏁 Ingestão concluída!")

if __name__ == "__main__":
    run_ingestion()
