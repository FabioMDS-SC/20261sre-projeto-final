# Problema: Processamento de Pedidos Northwind

## Contexto do Negócio
A Northwind Traders precisa modernizar seu processamento de dados para lidar com o volume crescente de transações. O objetivo é ingerir dados históricos e diários de pedidos (Orders e Order Details) em um banco analítico de alta performance (**ClickHouse**) para permitir análises em tempo real e dashboards interativos.

### Requisitos Mandatórios do ETL
- **Confiabilidade:** O processo deve garantir que todos os pedidos sejam processados corretamente.
- **Idempotência:** Reprocessar arquivos CSV não deve gerar duplicidade nas tabelas de destino.
- **Observabilidade:** Logs claros sobre a quantidade de linhas lidas, transformadas e carregadas.
- **Resiliência:** Tratamento de erros em campos mal formatados ou nulos no CSV original.
- **Integridade:** Garantir a consistência entre as tabelas `orders` e `order_details` (integridade referencial lógica).

---

## Canvas de Modelagem do Problema

### 1. Stakeholders
- **Gestão de Vendas (Northwind):** Necessitam de visão clara do volume de pedidos e produtos mais vendidos.
- **Engenharia de Dados:** Responsáveis por manter o pipeline entre o Data Lake (MinIO/S3) e o DW (ClickHouse).
- **Analistas de Negócio:** Consumidores finais dos dashboards em Streamlit.
- **SRE / DevOps:** Focados na estabilidade do ambiente (Codespaces/Containers) e monitoramento do ClickHouse.

### 2. Fluxos Críticos
- **Carga de Dados Históricos:** Processamento inicial dos arquivos CSV do Northwind.
- **Sincronização de Tabelas:** Garantir que detalhes de pedidos (`order_details`) estejam vinculados a pedidos existentes (`orders`).
- **Atualização do Dashboard:** Garantir que o Streamlit reflita o estado mais recente do banco analítico.

### 3. Modos de Falha
- **Tipagem Inconsistente no CSV:** Datas em formatos inesperados ou valores nulos em campos obrigatórios.
- **Duplicidade em Cargas Parciais:** Falha ao tentar inserir dados que já foram parcialmente carregados em uma tentativa anterior.
- **Estouro de Memória no ETL:** Processamento de arquivos muito grandes sem chunking adequado em Python.
- **Indisponibilidade do ClickHouse/MinIO:** O pipeline tenta gravar em serviços fora do ar.

### 4. Riscos Sistêmicos
- **Descompasso entre Pedidos e Itens:** Perder a rastreabilidade de quais produtos pertencem a quais pedidos.
- **Decisões baseadas em Dados Defasados:** Falha no pipeline que mantém o dashboard com dados antigos por horas.
- **Vulnerabilidades de Segurança:** Credenciais de acesso ao S3/ClickHouse expostas em logs ou código.
- **Gargalos de Performance:** Consultas lentas no dashboard por falta de indexação ou particionamento correto no ClickHouse.
