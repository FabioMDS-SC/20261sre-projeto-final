#!/bin/bash

echo "🚀 Iniciando setup do ambiente Northwind..."

# Rodar setup do MinIO
echo "📦 Configurando buckets no MinIO e subindo CSVs..."
python scripts/setup_minio.py

# Rodar setup do ClickHouse (Bronze)
echo "🗄️ Configurando tabela de ingestão (Bronze) no ClickHouse..."
python scripts/setup_clickhouse_bronze.py

# Executar Ingestão
echo "📥 Executando ingestão de dados..."
python scripts/ingestion.py

# Executar Transformações dbt
echo "🏗️ Executando transformações dbt (Silver e Gold)..."
cd northwind_transformations
dbt run --profiles-dir .
cd ..

echo "✅ Setup concluído com sucesso! O dashboard Streamlit está pronto."
