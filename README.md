# Northwind Modern Data Pipeline

Este projeto implementa um pipeline de dados moderno para o dataset Northwind, utilizando uma arquitetura local escalável e de alta performance baseada na metodologia Medallion (Bronze, Silver, Gold).

## 🚀 Como Executar

### 1. Subir a Infraestrutura
Certifique-se de ter o Docker e Docker Compose instalados e execute:
```bash
docker-compose up -d --build
```

### 2. Configurar o Ambiente e Ingestão
Execute o script de setup automático dentro do container da aplicação:
```bash
docker exec -it app-northwind ./setup.sh
```
Este comando irá:
- Criar os buckets no MinIO e subir os CSVs originais.
- Criar a tabela `ingestion` (Bronze) no ClickHouse.
- Executar a ingestão dos dados brutos em formato JSON via DuckDB.
- Rodar as transformações dbt (Silver e Gold).

### 3. Acessar o Dashboard
O dashboard Streamlit estará disponível em:
👉 [http://localhost:8501](http://localhost:8501)

## 🏗️ Arquitetura de Dados (Medallion)

1.  **Bronze (Raw JSON)**: Dados brutos ingeridos via DuckDB diretamente dos CSVs para a tabela `ingestion` no ClickHouse, preservando o formato original em JSON para máxima resiliência e rastreabilidade.
2.  **Silver (Staging)**: Modelos dbt (`stg_orders`, `stg_order_details`) que extraem e tipam os dados do JSON usando funções nativas do ClickHouse.
3.  **Gold (Analytics)**: Visão consolidada (`fct_sales`) pronta para consumo pelo dashboard, com KPIs pré-calculados.

## 🛠️ Stack Tecnológica
- **Object Storage**: MinIO (S3-compatible).
- **Banco de Dados**: ClickHouse (OLAP/Analytics).
- **ETL/Ingestão**: Python 3.11 & DuckDB.
- **Transformação**: dbt-clickhouse.
- **Visualização**: Streamlit & Plotly.
- **Infraestrutura**: Docker & Docker Compose.

## 📄 Documentação do Projeto

- [01. Requisitos Funcionais](documents/01_functional_requirements.md) - Definição em sintaxe EARS e priorização MoSCoW.
- [02. Requisitos Não Funcionais](documents/02_non_functional_requirements.md) - Atributos de qualidade (ISO 25010) e SLIs/SLOs.
- [03. Arquitetura do Sistema](documents/03_architecture.md) - Visões RM-ODP e ADRs.
- [08. Design do Sistema](documents/08_system_design.md) - Detalhes da implementação e infraestrutura.
- [10. Revisão de Arquitetura & Roadmap](documents/10_architecture_review.md) - Avaliação ATAM e Táticas de Len Bass.
