# Project Instructions (GEMINI.md)

Este arquivo contém as convenções, regras de arquitetura e fluxos de trabalho do projeto **20261sre-projeto-final**.

## Visão Geral do Projeto
- **Nome:** 20261sre-projeto-final
- **Contexto:** Modernização do pipeline de dados Northwind utilizando uma Modern Data Stack local (MinIO, ClickHouse, dbt).

## Convenções
- **Linguagem Principal:** Python 3.x (ETL e Ingestão).
- **Banco de Dados:** ClickHouse (OLAP/Analytics).
- **Armazenamento de Objetos:** MinIO (S3-compatible).
- **Transformação de Dados:** dbt (data build tool).
- **Visualização:** Streamlit.
- **Ambiente:** Docker & Docker Compose.

## Fluxos de Trabalho
- **Desenvolvimento:** Pesquisa -> Estratégia -> Execução.
- **Requisitos:** Seguir as diretrizes de EARS para RFs e ISO 25010 para RNFs.
- **Arquitetura:** Baseada no framework RM-ODP.
- **Commits:** Mensagens claras e concisas, preferencialmente em português.

## Documentação Técnica
- [Requisitos Funcionais](documents/01_functional_requirements.md)
- [Requisitos Não Funcionais](documents/02_non_functional_requirements.md)
- [Arquitetura do Sistema](documents/03_architecture.md)
