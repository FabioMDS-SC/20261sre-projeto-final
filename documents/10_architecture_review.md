# 10. Architectural Review & Implementation Roadmap

**Data:** 18 de Maio de 2026  
**Avaliador:** QA Agent (Quinn)  
**Metodologia:** Táticas Arquiteturais de Len Bass (4ª Edição)

## 1. Resumo da Avaliação

Esta revisão analisa a aderência do pipeline Northwind aos atributos de qualidade (QA) através das táticas arquiteturais recomendadas. O sistema apresenta uma base sólida em **Modificabilidade** e **Segurança**, mas requer intervenções em **Disponibilidade**, **Desempenho** e **Testabilidade**.

### Matriz de Maturidade (Bass Tactics)

| Atributo | Tática Avaliada | Status | Gap Identificado |
| :--- | :--- | :--- | :--- |
| **Disponibilidade** | Retry / Fault Tolerance | 🔴 Crítico | Scripts de ingestão sem tratamento de exceção ou reconexão. |
| **Modificabilidade** | Schema-on-read | 🟢 Forte | Camada Bronze em JSON garante desacoplamento total. |
| **Desempenho** | Batch / Resource Mgmt | 🟡 Alerta | Risco de estouro de memória (RNF-03) em arquivos grandes. |
| **Segurança** | Limit Exposure | 🟢 Forte | Segredos isolados em `.env` e rede Docker interna. |
| **Testabilidade** | Test Components | 🔴 Crítico | Ausência total de testes automatizados para scripts Python. |
| **Usabilidade** | Predictable Response | 🟢 Forte | Streamlit provê feedback rápido e interface clara. |

---

## 2. Plano de Implementação (Waves)

Para mitigar os riscos identificados, as melhorias serão executadas em três ondas (Waves) de desenvolvimento:

### 🌊 Wave 1: Estabilidade e Resiliência (Disponibilidade)
**Objetivo:** Garantir que o pipeline sobreviva a falhas intermitentes.
- **Tarefa 1.1:** Implementar tática de **Retry** com backoff exponencial na conexão com ClickHouse e MinIO no `ingestion.py`.
- **Tarefa 1.2:** Adicionar tratamento de exceções robusto para capturar erros de I/O e formato de arquivo.
- **Tarefa 1.3:** Validar integridade básica do CSV antes do processamento (RNF-09).

### 🌊 Wave 2: Performance e Monitoramento (Desempenho & Manutenibilidade)
**Objetivo:** Cumprir os SLOs de memória e garantir visibilidade estruturada.
- **Tarefa 2.1:** Refatorar o motor de ingestão (DuckDB) para operar em **Chunks**, garantindo que o uso de RAM nunca exceda 1GB (RNF-03).
- **Tarefa 2.2:** Substituir `print()` por **Structured Logging (JSON)** em todos os scripts Python para conformidade com o RNF-10.
- **Tarefa 2.3:** Implementar tática de **Heartbeat** no script de setup para validar saúde dos serviços antes de iniciar a carga.

### 🌊 Wave 3: Qualidade e Governança (Testabilidade)
**Objetivo:** Automatizar a validação técnica e garantir zero regressão.
- **Tarefa 3.1:** Criar suite de **Testes Unitários** (Pytest) para os módulos de transformação de dados.
- **Tarefa 3.2:** Implementar **Testes de Integração** que verifiquem o fluxo MinIO -> ClickHouse em ambiente de teste.
- **Tarefa 3.3:** Configurar gating de qualidade (pre-commit hooks) para garantir que segredos nunca sejam comitados (RNF-08).

---

## 3. Conclusão Técnica

A arquitetura atual é funcional mas "frágil" operacionalmente. A transição para um modelo resiliente (Wave 1) e escalável (Wave 2) é mandatória para suportar o volume de dados da Northwind em produção. A Wave 3 consolidará a maturidade do projeto, permitindo evoluções seguras.

**Aprovação QA:** ⚠️ CONCERNS (Aguardando execução da Wave 1)
