# Skill: Elicitação de Requisitos Funcionais (RF)

Esta habilidade orienta a identificação, documentação e validação das funcionalidades que o sistema deve executar para atender aos objetivos de negócio.

## 🎯 Objetivo
Garantir que todos os requisitos funcionais sejam capturados de forma clara, sem ambiguidades, e que estejam diretamente ligados à necessidade de modernização do pipeline de dados (Northwind).

## 🛠️ Metodologia de Elicitação
1.  **Identificação de Atores:** Quem ou o que interage com o sistema (ex: Engenharia de Dados, analistas, ClickHouse, MinIO/S3).
2.  **Definição de Escopo:** O que o sistema deve e não deve fazer.
3.  **Processo Iterativo:**
    *   **Descoberta:** Questionar o propósito de cada funcionalidade.
    *   **Classificação:** Agrupar requisitos por módulo (Ingestão, Transformação, Carga, Monitoramento).
    *   **Priorização:** Utilizar técnica **MoSCoW** (Must-have, Should-have, Could-have, Won't-have).
    *   **Validação:** Verificar se o requisito é testável e necessário.

## 📝 Diretrizes de Escrita
Cada requisito deve seguir os critérios **SMART** (Específico, Mensurável, Alcançável, Relevante e Temporal) e ser redigido utilizando a sintaxe **EARS** (Easy Approach to Requirements Syntax):

- **Ubíquo:** "O [sistema] deve [ação]." (Sempre acontece)
- **Orientado a Eventos:** "Quando [evento], o [sistema] deve [ação]."
- **Orientado a Estado:** "Enquanto [estado], o [sistema] deve [ação]."
- **Comportamento Indesejado:** "Se [condição indesejada], o [sistema] deve [ação]."
- **Funcionalidade Opcional:** "Onde [recurso incluído], o [sistema] deve [ação]."

## 🤖 Instruções para o Agente
Ao atuar com esta skill:
1.  **Sugira requisitos implícitos** baseados em boas práticas de engenharia de dados (ex: logs de auditoria, tratamento de arquivos corrompidos, idempotência).
2.  **Formate os requisitos** seguindo o padrão: `RF-XX: [Título] - [Requisito em EARS]`.
3.  **Garanta a rastreabilidade** inicial para a Matriz de Rastreabilidade (RTM).
4.  **Mantenha a consistência** com os requisitos já existentes em `documents/01_functional_requirements.md`.

## 📋 Checklist de Qualidade
- [ ] O requisito descreve o que o sistema faz, não como ele faz?
- [ ] Existe alguma contradição com outros RFs ou RNFs?
- [ ] O requisito é atômico?
- [ ] O critério de aceitação está claro?
- [ ] Está classificado corretamente no MoSCoW?

## Saída
Arquivo `documents/01_functional_requirements.md` com a lista de RFs, descrição detalhada e prioridade.
