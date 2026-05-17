# Northwind Modern Data Pipeline

Este projeto implementa um pipeline de dados moderno para o dataset Northwind, utilizando uma arquitetura local escalável e de alta performance.

## 🚀 Stack Tecnológica

- **Object Storage:** MinIO (S3-compatible)
- **Banco OLAP:** ClickHouse
- **Ingestão/ETL:** Python & DuckDB
- **Transformação:** dbt (data build tool)
- **Dashboard:** Streamlit
- **Infraestrutura:** Docker & Docker Compose

## 🏗️ Arquitetura (RM-ODP)

A arquitetura do sistema é baseada no framework RM-ODP, organizada em camadas:

1.  **Camada Bronze (Raw):** Arquivos CSV brutos no MinIO.
2.  **Camada Silver (Staging):** Dados validados e tipados no ClickHouse.
3.  **Camada Gold (Analytics):** Tabelas agregadas e modelos de negócio via dbt.

Para mais detalhes, consulte a [Documentação de Arquitetura](documents/03_architecture.md).

## 📄 Documentação do Projeto

- [01. Requisitos Funcionais](documents/01_functional_requirements.md) - Definição em sintaxe EARS e priorização MoSCoW.
- [02. Requisitos Não Funcionais](documents/02_non_functional_requirements.md) - Atributos de qualidade (ISO 25010) e SLIs/SLOs.
- [03. Arquitetura do Sistema](documents/03_architecture.md) - Visões RM-ODP e ADRs.

## 🛠️ Como Executar (Em breve)

O ambiente é orquestrado via Docker Compose. As instruções de configuração e execução serão adicionadas conforme a implementação do pipeline avançar.

---

## 📊 Modelo de Dados

O projeto foca no processamento de `Orders` e `Order Details` para gerar insights de vendas.

### Tabelas Principais (ClickHouse)
- `orders`: Cabeçalho dos pedidos, particionado por mês.
- `order_details`: Detalhes dos itens vendidos, com compressão colunar.
