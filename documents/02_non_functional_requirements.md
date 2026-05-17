# Requisitos Não Funcionais (RNF)

Este documento define os requisitos de qualidade do sistema seguindo a norma ISO 25010.

## 1. Adequação Funcional
- **RNF-01 (Completude):** 100% dos registros válidos presentes nos arquivos CSV devem ser carregados no ClickHouse.
  - **SLI:** Razão entre registros no ClickHouse e registros válidos no CSV.
  - **SLO:** 100% por carga.
  - **Prioridade:** Must have.

## 2. Eficiência de Desempenho
- **RNF-02 (Tempo de Resposta):** O processamento de um arquivo de 100 mil linhas não deve exceder 60 segundos.
  - **SLI:** Tempo total de execução do script de ETL.
  - **SLO:** < 60s para 100k linhas.
  - **Prioridade:** Should have.
- **RNF-03 (Consumo de Recursos):** O uso de memória RAM pelo processo de ETL não deve ultrapassar 1GB, utilizando processamento por chunks.
  - **SLI:** Pico de uso de memória (RSS) durante a execução.
  - **SLO:** < 1024 MB.
  - **Prioridade:** Must have.

## 3. Compatibilidade
- **RNF-04 (Coexistência):** O sistema deve ser executado de forma isolada em ambiente de containers (Docker/Codespaces) sem conflitos de porta.
  - **SLI:** Sucesso na inicialização do ambiente via `docker-compose`.
  - **SLO:** 100% de sucesso.
  - **Prioridade:** Must have.

## 4. Usabilidade
- **RNF-05 (Estética de Interface):** O dashboard Streamlit deve carregar os componentes visuais iniciais em menos de 5 segundos.
  - **SLI:** Tempo de carregamento da página (First Contentful Paint).
  - **SLO:** < 5s.
  - **Prioridade:** Should have.

## 5. Confiabilidade
- **RNF-06 (Disponibilidade):** O banco de dados ClickHouse deve estar disponível para consultas durante o horário comercial.
  - **SLI:** Uptime do container ClickHouse.
  - **SLO:** 99.9% (mensal).
  - **Prioridade:** Must have.
- **RNF-07 (Tolerância a Falhas):** Em caso de falha de rede, o sistema deve realizar re-tentativas automáticas de conexão. (Ver RF-08).
  - **SLI:** Taxa de sucesso de re-tentativas.
  - **SLO:** > 90%.
  - **Prioridade:** Should have.

## 6. Segurança
- **RNF-08 (Confidencialidade):** Nenhuma credencial de banco de dados ou chaves de API devem estar expostas no código fonte ou logs.
  - **SLI:** Quantidade de segredos detectados por ferramentas de scan (ex: gitleaks).
  - **SLO:** 0.
  - **Prioridade:** Must have.
- **RNF-09 (Integridade):** O sistema deve validar o checksum ou tamanho do arquivo CSV antes de iniciar a ingestão para garantir que não houve corrupção no transporte.
  - **SLI:** Taxa de arquivos corrompidos processados.
  - **SLO:** 0%.
  - **Prioridade:** Could have.

## 7. Manutenibilidade
- **RNF-10 (Analisabilidade):** Logs do sistema devem seguir um formato estruturado (JSON) para facilitar a análise via ferramentas de monitoramento.
  - **SLI:** Porcentagem de logs em formato JSON.
  - **SLO:** 100%.
  - **Prioridade:** Should have.

## 8. Portabilidade
- **RNF-11 (Instalabilidade):** O tempo total para subir o ambiente completo (ClickHouse, Dashboard, ETL) a partir de um `git clone` não deve exceder 5 minutos.
  - **SLI:** Tempo total de `docker-compose up`.
  - **SLO:** < 300s.
  - **Prioridade:** Should have.

---

## Tabela Consolidada (Matriz RNF)

| ID | Atributo | SLI | SLO | Fonte | Prioridade |
|:---|:---|:---|:---|:---|:---|
| RNF-01 | Adequação | Taxa de carga | 100% | Logs ETL | Must |
| RNF-02 | Performance | Tempo de ETL | < 60s/100k | Logs ETL | Should |
| RNF-03 | Performance | Uso de RAM | < 1GB | OS Metrics | Must |
| RNF-04 | Compatibilidade | Sucesso docker | 100% | CI/CD | Must |
| RNF-05 | Usabilidade | Tempo Load UI | < 5s | Browser DevTools | Should |
| RNF-06 | Confiabilidade | Uptime DB | 99.9% | Healthcheck | Must |
| RNF-08 | Segurança | Secrets em log | 0 | Static Scan | Must |
| RNF-10 | Manutenibilidade | Logs JSON | 100% | Arquivos de Log | Should |
| RNF-11 | Portabilidade | Tempo de Setup | < 5min | Manual/CLI | Should |
