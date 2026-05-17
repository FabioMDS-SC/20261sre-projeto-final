# Skill: elicit_rnf

## Quando usar
Quando o usuário pedir RNFs e já existir `specs/00_problem.md` e/ou `documents/01_functional_requirements.md`.

## Entrada
- `specs/00_problem.md` (obrigatório)
- `documents/01_functional_requirements.md` (opcional)

## Passos
1. Ler stakeholders e fluxos críticos do problema.
2. Mapear cada fluxo aos 8 atributos da ISO 25010:
   - Adequação Funcional
   - Eficiência de Desempenho
   - Compatibilidade
   - Usabilidade
   - Confiabilidade
   - Segurança
   - Manutenibilidade
   - Portabilidade
3. Para cada atributo, propor 1 a 3 RNFs com SLI (Service Level Indicator) mensurável.
4. Marcar prioridade MoSCoW (Must have, Should have, Could have, Won't have).
5. Listar premissas e fontes de medição.

## Saída
Arquivo `documents/02_non_functional_requirements.md` com:
- Seção por atributo ISO 25010.
- IDs RNF-NN únicos.
- Tabela final consolidada com (ID, Atributo, SLI, SLO, Fonte, Prioridade).

## Critérios de Aceitação
- 8 atributos cobertos.
- Todo RNF tem unidade e janela de medição.
- Nenhum RNF aspiracional ("ser confiável" é proibido).

## Anti-padrões
- RNF sem unidade ou sem janela.
- Atributo ISO 25010 ausente.
- Resposta com código Python pronto.
