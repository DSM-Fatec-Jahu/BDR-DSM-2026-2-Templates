# Mapeamento de Alvos Processados

Registro incremental de cada aula/atividade do repositório de origem
([`BDR-DSM-2026-2`](https://github.com/DSM-Fatec-Jahu/BDR-DSM-2026-2)) já
transformada em template neste repositório. Atualizado a cada novo alvo
processado — nunca reescrito do zero.

---

## Aula 01 — Revisão de Modelagem de Dados (Conceitual)

| Campo | Valor |
|---|---|
| **Fonte** | `docs/aulas/Aula_01_Revisao_Modelagem_Conceitual.md` + `docs/aulas/Aula_01_Gabarito.md` (repo de origem) |
| **Tema principal** | Modelo Entidade-Relacionamento (MER) — modelagem conceitual, independente de SGBD |
| **Bloco/trilha** | Bloco 1 — Fundamentos e Modelagem ("Trilha do(a) Modelador(a) de Dados") |
| **Competências abordadas** | Diferenciar dado/informação/conhecimento; identificar entidades, atributos e relacionamentos; aplicar cardinalidade e participação; reconhecer auto-relacionamento e relacionamento ternário; aplicar o método das "quatro perguntas" (entidade vs. atributo); aplicar generalização/especialização (superclasse/subclasse, herança, restrições total/parcial × exclusiva/sobreposta) |
| **SGBD utilizado** | Nenhum — aula 100% conceitual, anterior a qualquer SQL (SQL só começa na Aula 03). Notação adotada: Crow's Foot, via Mermaid `erDiagram` |
| **Ferramentas** | Nenhuma ferramenta de SGBD; ambiente de edição de Markdown/Mermaid (VS Code + extensão de preview Mermaid) |
| **Artefato gerado como template** | `templates/aula-01-modelagem-conceitual-mer/` — atividade formativa com 2 partes (MER de clínica médica; generalização de Pessoas em Aluno/Professor/Funcionário Administrativo), baseada nos Exercícios de Fixação 1 e 4 da aula original (não nos Checkpoints, que já têm gabarito publicado no site) |
| **Complexidade estimada** | Baixa-média. Conteúdo é só leitura/interpretação de enunciado + desenho de diagrama; a complexidade está em decidir corretamente cardinalidade/participação/generalização, não em ferramental |
| **Possibilidade de avaliação automática** | Sim, estrutural — parser de `erDiagram` Mermaid próprio (`shared/utilitarios/mer_mermaid.py`) confere existência de entidades, nomenclatura de PK/FK (Regras 5/6) e cardinalidade/participação de relacionamentos, sem exigir texto idêntico ao gabarito. A adequação da justificativa de restrição da hierarquia (Parte 2) é revisada manualmente pelo professor — não é um julgamento binário automatizável |
| **Decisão arquitetural notável** | Sem `.devcontainer` com MariaDB (não haveria uso — nenhum SQL é executado nesta aula). Ver `docs/decisoes-arquiteturais.md` |

---

*(Próximos alvos processados serão adicionados abaixo desta linha, em ordem cronológica de processamento.)*
