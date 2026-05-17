# 03. Arquitetura do Sistema (RM-ODP)

Este documento descreve a arquitetura do pipeline de processamento de pedidos Northwind utilizando os cinco pontos de vista do framework RM-ODP, focado em uma infraestrutura Local com Banco OLAP e Object Storage.

## 1. Enterprise Viewpoint (Ponto de Vista de Negócio)
- **Propósito:** Modernizar a ingestão de pedidos da Northwind utilizando uma arquitetura analítica moderna rodando localmente (Codespaces/Docker).
- **Objetivo:** Processar grandes volumes de pedidos com alta performance (RNF-02) e garantir a integridade analítica para tomada de decisão.
- **Stakeholders:** Gestão de Vendas, Engenharia de Dados, Analistas de Negócio e SRE/DevOps.
- **Processo de Negócio:** Depósito de arquivos CSV no Object Storage local (MinIO) -> Ingestão automatizada (RF-02) -> Carga no Banco OLAP (ClickHouse) -> Transformação e agregação (dbt) -> Dashboard Interativo (Streamlit).

## 2. Information Viewpoint (Ponto de Vista de Informação)
- **Foco:** Ciclo de vida dos dados analíticos e camadas de dados.
- **Camada Bronze (Ingestion/Raw):** Tabela `ingestion` no ClickHouse. Armazena os dados brutos dos CSVs em formato JSON, acompanhados de um timestamp de ingestão e o nome do arquivo de origem (`tag`). Isso permite reconstruir qualquer dado a partir da origem sem perda de informação.
- **Camada Silver (Staging):** Dados extraídos do JSON via dbt, tipados e limpos em tabelas relacionais.
- **Camada Gold (Analytics):** Visões agregadas e tabelas de fatos/dimensões transformadas via SQL.
- **Metadados:** Logs de execução (RF-06), logs de auditoria (RF-10) e métricas de performance (SLIs).

## 3. Computational Viewpoint (Ponto de Vista Computacional)
- **Foco:** Decomposição funcional e interações entre componentes.
- **Serviço de Ingestão:** Script Python que utiliza DuckDB como motor de leitura para extrair dados do MinIO e realizar o "push" para o ClickHouse, garantindo idempotência (RF-05).
- **Banco OLAP:** ClickHouse responsável pelo armazenamento colunar e execução de consultas analíticas de baixa latência.
- **Motor de Transformação:** dbt (data build tool) para versionamento de modelos SQL e garantia de qualidade.
- **Interface de Dashboard:** Streamlit conectado ao ClickHouse para exibição de KPIs de vendas em tempo real.

## 4. Engineering Viewpoint (Ponto de Vista de Engenharia)
- **Foco:** Infraestrutura local via Docker.
- **Object Storage Local:** MinIO (API compatível com S3) rodando em container para simular ambiente de nuvem.
- **Banco Analítico:** ClickHouse configurado com volumes persistentes para garantir durabilidade.
- **Orquestrador:** Docker Compose gerenciando a rede interna e a comunicação entre os serviços.
- **Gerenciamento de Segredos:** Variáveis de ambiente (`.env`) para proteger credenciais de acesso (RNF-08).

## 5. Technology Viewpoint (Ponto de Vista de Tecnologia)
- **Stack Tecnológica Local:**
    - **Object Storage:** MinIO (Porta 9000/9001).
    - **Banco OLAP:** ClickHouse (Portas 8123/9004).
    - **Ingestão/ETL:** Python 3.x, DuckDB e Boto3.
    - **Transformação:** dbt-clickhouse.
    - **Visualização:** Streamlit (Porta 8501).
    - **Automação:** Scripts Python (`scripts/setup_minio.py` e `scripts/setup_clickhouse.py`) orquestrados por `setup.sh`.
    - **Infraestrutura:** Docker & Docker Compose.

---

## 🏗️ Architecture Decision Records (ADRs)

### ADR 001: ClickHouse como Banco OLAP
- **Contexto:** Necessidade de performance analítica superior para consultas em grandes volumes de registros.
- **Decisão:** Utilizar ClickHouse em vez de bancos transacionais tradicionais.
- **Consequências:** Ganho massivo em velocidade de agregação e compressão de dados (RNF-02), exigindo modelagem colunar.

### ADR 002: MinIO para Simular Object Storage Local
- **Contexto:** Garantir que o pipeline seja compatível com padrões de nuvem (S3) rodando localmente.
- **Decisão:** Utilizar MinIO.
- **Consequências:** Facilidade de migração para AWS S3 no futuro e desacoplamento entre a origem do arquivo e o processamento.

### ADR 003: DuckDB como Motor de Ingestão
- **Contexto:** Necessidade de ler arquivos CSV de forma eficiente e carregar no ClickHouse sem estourar a memória (RNF-03).
- **Decisão:** Utilizar DuckDB para processamento intermediário e integração com ClickHouse.
- **Consequências:** Redução drástica no tempo de ingestão e consumo otimizado de recursos computacionais.

### ADR 004: dbt para Camada de Transformação
- **Contexto:** Necessidade de versionar, testar e documentar as transformações SQL.
- **Decisão:** Utilizar dbt.
- **Consequências:** Melhor governança de dados, documentação automática e linhagem de dados clara.
