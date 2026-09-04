# Relatório Executivo

Contadores agregados do repositório de templates, atualizados a cada alvo
processado, e roadmap futuro.

---

## Contadores atuais

| Métrica | Valor |
|---|---|
| **Alvos analisados** | 2 (Aula 01, Aula 02) |
| **Templates criados** | 2 — `templates/aula-01-modelagem-conceitual-mer/`, `templates/aula-02-normalizacao-modelo-logico/` |
| **Projetos integradores criados** | 0 |
| **SGBDs utilizados nos templates** | Nenhum ainda em uso real (Aulas 01 e 02 são pré-SQL). MariaDB é o padrão definido para quando o primeiro alvo com SQL for processado (a partir da Aula 03) |
| **Templates com correção automática** | 2/2 (100%) — correção estrutural via parser Mermaid próprio, sem execução de banco |
| **Utilitários compartilhados em `shared/`** | 1 — `shared/utilitarios/mer_mermaid.py` (parser/validador de `erDiagram`, agora reaproveitado por dois templates sem nenhuma alteração de código — validação do roadmap traçado após a Aula 01) |
| **Repositório privado de notas (`BDR-DSM-2026-2-Notas`) configurado** | Pendente — depende de ação manual do professor (ver `docs/guia-professor.md`) |

---

## Roadmap futuro

### Curto prazo — próximos alvos naturais do Bloco 1

- ✅ **Aula 02 — Normalização**: processada. Confirmou que
  `shared/utilitarios/mer_mermaid.py` se sustenta fora do caso original
  sem nenhuma alteração de código — só o roteiro de critérios
  (`tests/regras_avaliacao.py`) muda por template. Ver
  `docs/decisoes-arquiteturais.md`, seção Aula 02.
- **Aula 03 — SQL DDL**: primeiro alvo com SQL de verdade — primeiro
  template a de fato precisar do `.devcontainer` com MariaDB no padrão
  descrito no processo de geração deste repositório. Validará também se o
  padrão de correção automática "estrutura de tabela, não string exata"
  funciona bem para DDL real (existência de tabela/coluna/PK/FK/constraint
  via `INFORMATION_SCHEMA`, não diff de texto).
- **Aula 05 — Atividade T1 (Modelagem de Streaming)**: primeiro alvo
  avaliativo de peso — primeiro teste real do mecanismo de repositório
  privado individual descrito em `docs/estrategia-de-avaliacao.md` (ainda
  não implementado, só documentado).

### Médio prazo

- Consolidar em `shared/` um segundo utilitário: validador de `CREATE
  TABLE` real (parsing de DDL MariaDB via `INFORMATION_SCHEMA`, não regex),
  quando o Bloco 1 tiver templates suficientes com SQL para justificar a
  generalização.
- Primeira entrada em `docs/projetos-integradores.md` com um projeto de
  porte médio de fato definido (provavelmente o T1).
- Avaliar, com dados reais de uso (uma vez que `BDR-DSM-2026-2-Notas`
  estiver recebendo entregas), se o formato do payload agregado (Fase 5B)
  atende ao que o professor precisa consultar, ou se precisa de campos
  adicionais.

### Longo prazo — evolução do repositório e da disciplina sem GitHub Classroom

- Se o volume de PRs simultâneos crescer (turmas maiores, múltiplos
  alvos abertos ao mesmo tempo), reavaliar se o workflow reaproveitável
  único (`_autograding-reusable.yml`) ainda escala bem ou se vale
  segmentar por bloco da disciplina.
- Considerar automatizar a checagem cruzada RA/usuário-GitHub (hoje é
  conferência manual do professor contra uma planilha externa) com um
  segundo repositório de "roster" privado, se o volume de divergências de
  identificação no PR (sinalizadas automaticamente pelo workflow) se
  mostrar frequente na prática.
- Sem GitHub Classroom, a disciplina depende inteiramente da robustez
  deste repositório e do repositório de notas — vale revisar
  periodicamente (a cada bloco concluído) se algum recurso do GitHub
  mudou de comportamento (ex.: mudanças de política sobre `GITHUB_TOKEN`
  em PRs de fork) que exija ajuste na Decisão Arquitetural nº 5 da Aula 01
  (`pull_request_target`).

---

*(Cada novo alvo processado atualiza os contadores acima; o roadmap é
revisado, não apenas anexado, para não acumular itens já resolvidos.)*
