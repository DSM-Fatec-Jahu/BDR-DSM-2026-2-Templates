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

## Aula 02 — Normalização e Passagem ao Modelo Lógico Relacional

| Campo | Valor |
|---|---|
| **Fonte** | `docs/aulas/Aula_02_Normalizacao.md` + `docs/aulas/Aula_02_Gabarito.md` (repo de origem) |
| **Tema principal** | Normalização (1FN, 2FN, 3FN) e passagem do MER conceitual ao modelo lógico relacional |
| **Bloco/trilha** | Bloco 1 — Fundamentos e Modelagem ("Trilha do(a) Modelador(a) de Dados") |
| **Competências abordadas** | Identificar dependências funcionais (totais, parciais, transitivas); reconhecer anomalias de inserção/atualização/exclusão; aplicar 1FN/2FN/3FN progressivamente; aplicar as regras de passagem ao modelo lógico para relacionamentos 1:1, 1:N, N:M, entidades fracas e atributos multivalorados; justificar o lado da FK em um 1:1 (critérios de participação e semântica); usar chave substituta (`id_tabela`) em vez de chave natural |
| **SGBD utilizado** | Nenhum — ainda anterior a SQL de verdade (SQL só começa na Aula 03). Notação adotada: Crow's Foot, via Mermaid `erDiagram`, agora representando tabelas do modelo lógico (não mais entidades conceituais) |
| **Ferramentas** | Nenhuma ferramenta de SGBD; ambiente de edição de Markdown/Mermaid (VS Code + extensão de preview Mermaid) — mesmo `.devcontainer` sem banco de dados usado na Aula 01 |
| **Artefato gerado como template** | `templates/aula-02-normalizacao-modelo-logico/` — atividade formativa com 2 partes: (1) normalização de uma tabela desnormalizada de oficina mecânica até a 3FN, com mapeamento escrito de dependências funcionais; (2) passagem ao modelo lógico de um MER conceitual de rede de hotéis, cobrindo os quatro tipos de relacionamento (1:N, N:M com atributo, 1:1, entidade fraca). Cenários originais (não os Exercícios de Fixação da Seção 10, que já têm gabarito publicado em `Aula_02_Gabarito.md` — mesmo critério de exclusão já aplicado na Aula 01) |
| **Complexidade estimada** | Média. Primeira atividade a exigir análise de dependência funcional em duas camadas (parcial que esconde uma transitiva) e a decisão explícita de lado de FK em relacionamento 1:1 — mais denso que a Aula 01, mas sem ferramental novo |
| **Possibilidade de avaliação automática** | Sim, estrutural — reaproveita integralmente `shared/utilitarios/mer_mermaid.py` (mesmo parser da Aula 01, agora validado em um segundo template): existência de tabelas, nomenclatura de PK/FK (Regras 5/6), cardinalidade e participação de relacionamentos. O mapeamento de dependências funcionais (Parte 1a) e a justificativa da FK 1:1 (Parte 2) só têm o preenchimento mínimo checado automaticamente (tamanho de texto) — a correção de conteúdo é manual, mesmo padrão da "Justificativa da restrição da hierarquia" na Aula 01 |
| **Decisão arquitetural notável** | Sem `.devcontainer` com MariaDB, pelo mesmo motivo da Aula 01 (ainda não há SQL). Cenários (oficina mecânica, rede de hotéis) deliberadamente diferentes dos usados nos Checkpoints e Exercícios de Fixação da aula original, para que a correção automática não tenha uma resposta pronta a um clique de distância. Ver `docs/decisoes-arquiteturais.md` |

---

## Aula 03 — SQL e DDL: Definição de Estruturas

| Campo | Valor |
|---|---|
| **Fonte** | `docs/aulas/Aula_03_SQL_DDL.md` + `docs/aulas/Aula_03_Gabarito.md` (repo de origem) |
| **Tema principal** | DDL — `CREATE DATABASE`, `CREATE TABLE`, `ALTER TABLE`, `DROP`; tipos de dados; constraints (`PRIMARY KEY`, `FOREIGN KEY` com `ON DELETE`/`ON UPDATE`, `UNIQUE`, `CHECK`); diferenças MariaDB × MySQL × PostgreSQL |
| **Bloco/trilha** | Bloco 1 — Fundamentos e Modelagem (primeira aula do bloco de SQL de verdade) |
| **Competências abordadas** | Criar/alterar/remover estruturas de banco com DDL; aplicar as 9 regras de nomenclatura da disciplina em SQL real (incluindo a Regra 7 — FK pelo papel semântico); escolher tipos de dados corretos (`DECIMAL` vs `FLOAT`, `CHAR` vs `VARCHAR`, `DATETIME` vs `TIMESTAMP`, `ENUM`); aplicar `PRIMARY KEY` simples/composta, `FOREIGN KEY` com ações de integridade referencial, `UNIQUE`, `CHECK`; modificar tabela existente com `ALTER TABLE` |
| **SGBD utilizado** | MariaDB (primeiro alvo com SQL de verdade — a partir daqui volta a valer o padrão `.devcontainer` com MariaDB via `docker-compose.yml`). PostgreSQL aparece só como comparação conceitual no conteúdo da aula, sem exercício prático próprio — não é alvo de comparação explícita, então o template não sobe um segundo SGBD |
| **Ferramentas** | Cliente `mysql` (linha de comando); extensão VS Code `cweijan.vscode-mysql-client2` |
| **Artefato gerado como template** | `templates/aula-03-sql-ddl-estruturas/` — atividade formativa com um schema original de central de chamados técnicos (helpdesk): `CREATE DATABASE` idempotente + 5 `CREATE TABLE` (incluindo FK dupla por papel semântico e uma tabela N:M com atributo próprio) + 3 `ALTER TABLE`. Cenário inédito — nenhum dos 6 Checkpoints, 3 Exercícios de Fixação ou o exemplo de e-commerce da Seção 11 da aula original é reaproveitado (todos têm gabarito publicado em `Aula_03_Gabarito.md`) |
| **Complexidade estimada** | Média-alta. Primeiro template a exigir um ambiente com banco de dados real funcionando (Codespace + MariaDB) e a primeira correção automática que executa SQL de verdade, não só analisa texto |
| **Possibilidade de avaliação automática** | Sim, estrutural e via execução real — novo utilitário `shared/utilitarios/mariadb_ddl.py` roda o script entregue contra um MariaDB descartável e confere `INFORMATION_SCHEMA` (tabelas, colunas, PK, FK com `ON DELETE`/`ON UPDATE`, `UNIQUE`, `CHECK`, `ENUM`) — nunca compara o texto do SQL, para aceitar qualquer abordagem que chegue à mesma estrutura |
| **Decisão arquitetural notável** | Primeiro `.devcontainer` com MariaDB real do repositório (`docker-compose.yml`); o serviço MariaDB de autograding foi adicionado ao workflow reaproveitável único (`_autograding-reusable.yml`) em vez de duplicado num segundo workflow — ver `docs/decisoes-arquiteturais.md` |

---

*(Próximos alvos processados serão adicionados abaixo desta linha, em ordem cronológica de processamento.)*
