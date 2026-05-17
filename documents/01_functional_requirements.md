# Requisitos Funcionais (RF)

Este documento descreve as funcionalidades do sistema de processamento de pedidos Northwind, seguindo a sintaxe EARS, a metodologia MoSCoW e os critérios SMART.

## 1. Ingestão e Carga
| ID | Título | Requisito (EARS) | Prioridade |
|:---|:---|:---|:---|
| **RF-01** | Carga de Dados Históricos | O sistema deve ingerir dados históricos e diários de pedidos (`Orders` e `Order Details`) a partir de arquivos CSV para o banco de dados ClickHouse. | Must-have |
| **RF-02** | Automação de Ingestão | Quando um novo arquivo CSV for detectado no diretório de entrada, o sistema deve iniciar automaticamente o processo de ETL. | Should-have |
| **RF-05** | Garantia de Idempotência | O sistema deve garantir a idempotência do processamento, não gerando duplicidade de registros caso o mesmo arquivo seja reprocessado. | Must-have |
| **RF-11** | Arquivamento de Processados | Quando o processamento de um arquivo CSV for concluído com sucesso, o sistema deve mover o arquivo para um diretório de arquivos processados. | Should-have |

## 2. Transformação e Integridade
| ID | Título | Requisito (EARS) | Prioridade |
|:---|:---|:---|:---|
| **RF-03** | Consistência Referencial | Enquanto o processo de ETL estiver em execução, o sistema deve garantir a integridade referencial lógica entre as tabelas `orders` e `order_details`. | Must-have |
| **RF-04** | Tratamento de Erros de Formato | Se um campo obrigatório no CSV estiver mal formatado ou nulo, o sistema deve registrar o erro e prosseguir com o processamento das demais linhas. | Must-have |
| **RF-09** | Validação de Esquema | O sistema deve validar se o cabeçalho do arquivo CSV corresponde ao esquema esperado antes de iniciar a carga. | Should-have |

## 3. Monitoramento e Observabilidade
| ID | Título | Requisito (EARS) | Prioridade |
|:---|:---|:---|:---|
| **RF-06** | Logs de Execução | O sistema deve registrar logs detalhando a quantidade de linhas lidas, transformadas e carregadas com sucesso em cada execução. | Must-have |
| **RF-08** | Retentativas de Conexão | Se a conexão com o ClickHouse falhar durante a gravação, o sistema deve realizar até 3 re-tentativas automáticas. | Should-have |
| **RF-10** | Log de Auditoria | O sistema deve manter um log de auditoria registrando o nome do arquivo, carimbo de tempo (início/fim) e status final. | Should-have |
| **RF-12** | Alerta de Falha Crítica | Se o processo de ETL abortar após todas as re-tentativas, o sistema deve registrar um log de nível CRITICAL descrevendo a causa da interrupção. | Should-have |

## 4. Visualização
| ID | Título | Requisito (EARS) | Prioridade |
|:---|:---|:---|:---|
| **RF-07** | Dashboard de Vendas | O dashboard Streamlit deve exibir o volume total de pedidos e a lista de produtos mais vendidos com base nos dados do ClickHouse. | Implementado | Must-have |

---

## Detalhamento dos Requisitos (Padrão Skill)

- **RF-01: Carga de Dados Históricos** - O sistema deve ingerir dados históricos e diários de pedidos (`Orders` e `Order Details`) a partir de arquivos CSV para o banco de dados ClickHouse.
- **RF-02: Automação de Ingestão** - Quando um novo arquivo CSV for detectado no diretório de entrada, o sistema deve iniciar automaticamente o processo de ETL.
- **RF-03: Consistência Referencial** - Enquanto o processo de ETL estiver em execução, o sistema deve garantir a integridade referencial lógica entre as tabelas `orders` e `order_details`.
- **RF-04: Tratamento de Erros de Formato** - Se um campo obrigatório no CSV estiver mal formatado ou nulo, o sistema deve registrar o erro e prosseguir com o processamento das demais linhas.
- **RF-05: Garantia de Idempotência** - O sistema deve garantir a idempotência do processamento, não gerando duplicidade de registros caso o mesmo arquivo seja reprocessado.
- **RF-06: Logs de Execução** - O sistema deve registrar logs detalhando a quantidade de linhas lidas, transformadas e carregadas com sucesso em cada execução.
- **RF-07: Dashboard de Vendas** - O dashboard Streamlit deve exibir o volume total de pedidos e a lista de produtos mais vendidos com base nos dados do ClickHouse.
- **RF-08: Retentativas de Conexão** - Se a conexão com o ClickHouse falhar durante a gravação, o sistema deve realizar até 3 re-tentativas automáticas.
- **RF-09: Validação de Esquema** - O sistema deve validar se o cabeçalho do arquivo CSV corresponde ao esquema esperado antes de iniciar a carga.
- **RF-10: Log de Auditoria** - O sistema deve manter um log de auditoria registrando o nome do arquivo, carimbo de tempo (início/fim) e status final de cada carga.
- **RF-11: Arquivamento de Processados** - Quando o processamento de um arquivo CSV for concluído com sucesso, o sistema deve mover o arquivo para um diretório de arquivos processados.
- **RF-12: Alerta de Falha Crítica** - Se o processo de ETL abortar após todas as re-tentativas, o sistema deve registrar um log de nível CRITICAL descrevendo a causa da interrupção.

---

## Legenda MoSCoW
- **Must-have:** Requisitos vitais para o sucesso do projeto.
- **Should-have:** Requisitos importantes, mas não vitais.
- **Could-have:** Requisitos desejáveis, mas que podem ser postergados.
- **Won't-have:** Requisitos que não serão implementados nesta fase.
