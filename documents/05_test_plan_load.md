# Relatório de Testes de Carga e Performance

Este documento detalha os resultados dos testes de requisitos não funcionais (RNF) realizados no pipeline Northwind.

## 1. Ambiente de Teste
- **Infraestrutura:** Docker Compose (ClickHouse, MinIO, Streamlit).
- **Ferramentas:** k6 (UI), Python psutil (Ingestão).
- **Data do Teste:** 20 de Maio de 2026.

## 2. Resultados por Requisito

### RNF-01: Completude (Adequação Funcional)
- **Objetivo:** 100% dos registros válidos carregados.
- **Resultado:** 100.000 / 100.000 registros.
- **Status:** ✅ PASS

### RNF-02: Tempo de Resposta (Eficiência)
- **Objetivo:** Processamento de 100k linhas < 60 segundos.
- **Resultado:** 7.62 segundos.
- **Status:** ✅ PASS

### RNF-03: Consumo de Recursos (Eficiência)
- **Objetivo:** Uso de RAM < 1GB.
- **Resultado:** Pico de 180.94 MB.
- **Status:** ✅ PASS

### RNF-05: Estética de Interface (Usabilidade)
- **Objetivo:** Tempo de carregamento inicial da UI < 5 segundos.
- **Resultado:** 9.61 ms (p95) via k6.
- **Status:** ✅ PASS

## 3. Scripts de Teste Utilizados
- **UI Test:** `tests/load_test_ui.js` (k6)
- **Ingestion Test:** `tests/load_test_ingestion.py` (Custom Python)

## 4. Conclusão
O sistema atende a todos os requisitos não funcionais de performance e escalabilidade definidos na especificação ISO 25010 para a carga de trabalho de 100k linhas. A arquitetura de processamento em chunks (DuckDB + ClickHouse) demonstrou alta eficiência e baixo consumo de memória.
