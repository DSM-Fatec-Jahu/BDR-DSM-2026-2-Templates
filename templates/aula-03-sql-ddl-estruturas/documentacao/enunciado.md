# Enunciado — Atividade da Aula 03 — SQL e DDL: Definição de Estruturas

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Baseado em:** [Aula 03 — SQL e DDL: Definição de Estruturas](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_03_SQL_DDL/) (Seções 1 a 8)

---

## Objetivo

Esta é a primeira atividade da disciplina com SQL de verdade: sair do
modelo lógico (Aula 02) e **criar o banco de dados de verdade**, aplicando
as 9 regras de nomenclatura, os tipos de dados corretos e as constraints de
integridade (`PRIMARY KEY`, `FOREIGN KEY` com `ON DELETE`/`ON UPDATE`,
`UNIQUE`, `CHECK`) vistas nas Seções 1 a 8 da aula.

O cenário desta atividade — uma **central de chamados técnicos
(helpdesk)** — é original: não é o exemplo de e-commerce trabalhado passo a
passo na aula (Seção 11), nem nenhum dos 6 Checkpoints ou dos 3 Exercícios
de Fixação da Seção 12 (todos já têm gabarito publicado em
[`Aula_03_Gabarito.md`](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_03_Gabarito/)
no repositório de conteúdo). Ele foi desenhado, porém, para exercitar
exatamente os mesmos mecanismos: `CREATE DATABASE` idempotente, FK pelo
papel semântico (Regra 7, igual ao par `cliente_id`/`funcionario_id` da
Seção 6.5), relacionamento N:M com atributo próprio, `CHECK`, e `ALTER
TABLE`.

## Como a correção funciona (importante ler antes de começar)

Diferente das Aulas 01 e 02, a correção automática desta atividade **executa
seu script de verdade** contra um MariaDB descartável e confere a
**estrutura resultante** via `INFORMATION_SCHEMA` — não compara o texto do
seu SQL com um gabarito. Duas consequências práticas:

- **Os nomes de banco, tabela e coluna pedidos abaixo são exatos e
  obrigatórios** — é assim que o corretor localiza o que você criou. Nomes
  de `CONSTRAINT` (ex.: `pk_usuario`, `fk_chamado_cliente`) **não** são
  verificados pelo nome — só o efeito (qual coluna é PK, para onde aponta
  a FK, qual o `ON DELETE`) importa, então pode nomeá-los como quiser,
  desde que siga o padrão da disciplina.
- Se o script tiver um erro de sintaxe e parar no meio, a correção reporta
  o erro exato do MariaDB (mesma mensagem que você veria rodando localmente)
  em vez de uma lista de critérios — corrija a sintaxe e rode de novo.

## O que entregar

Edite **[`sql/helpdesk.sql`](../sql/helpdesk.sql)** — um único script `.sql`
com as duas partes abaixo, executado de cima para baixo em uma única sessão
(mesmo padrão do script completo da Seção 11 da aula).

### Parte 1 — `CREATE DATABASE` e `CREATE TABLE`

**a) Banco de dados.** Crie o banco `helpdesk_ti`, seguindo exatamente o
padrão da Seção 4.5 da aula: idempotente (`IF NOT EXISTS`), com
`CHARACTER SET utf8mb4` e `COLLATE utf8mb4_unicode_ci`.

**b) Tabelas.** Crie as cinco tabelas abaixo, com todas as colunas, PKs, FKs
e constraints descritas. **Toda tabela leva os três campos de log da Regra
9** (`criado_em`, `atualizado_em`, `deletado_em`), mesmo quando não
mencionados explicitamente na lista de colunas abaixo.

1. **`usuarios`** — representa tanto clientes quanto técnicos do suporte; o
   papel de cada pessoa é definido por qual FK a referencia, não por uma
   coluna própria (mesma lógica da tabela `pessoas` da Seção 6.2 da aula).
   - `id_usuario` — PK (Regra 5)
   - `nome` — texto, obrigatório
   - `email` — texto, obrigatório, **único**
   - `cpf` — 11 caracteres fixos (apenas dígitos), obrigatório, **único**
   - `telefone` — 11 caracteres fixos, opcional

2. **`categorias_chamado`** — domínio fechado de categorias (ex.: "Rede",
   "Hardware", "Software").
   - `id_categoria_chamado` — PK
   - `nome` — texto, obrigatório, **único**
   - `descricao` — texto livre, opcional
   - `ativa` — indica se a categoria ainda pode ser usada em novos
     chamados; obrigatório, padrão verdadeiro

3. **`chamados`** — o chamado técnico em si. **Aplique aqui a Regra 7**: as
   colunas `cliente_id` e `tecnico_responsavel_id` referenciam a **mesma**
   tabela `usuarios`, mas em papéis diferentes — nomeie pelo papel, não
   repita `usuario_id` duas vezes.
   - `id_chamado` — PK
   - `cliente_id` — FK para `usuarios` (papel: quem abriu o chamado),
     obrigatório; se o cliente for removido, o chamado não pode ficar
     "órfão" — bloqueie a remoção (`ON DELETE RESTRICT`)
   - `tecnico_responsavel_id` — FK para `usuarios` (papel: técnico
     designado), **opcional** (um chamado pode estar sem técnico atribuído
     ainda); se o técnico for removido do sistema, o chamado deve
     simplesmente ficar sem responsável, não ser bloqueado nem apagado
     (`ON DELETE SET NULL`)
   - `categoria_id` — FK para `categorias_chamado`, obrigatório, bloqueia
     remoção da categoria em uso (`ON DELETE RESTRICT`)
   - `titulo` — texto curto, obrigatório (esta coluna será renomeada na
     Parte 2 — crie-a como `titulo` mesmo assim)
   - `descricao` — texto livre, obrigatório
   - `prioridade` — um destes quatro valores, exatamente:
     `baixa`, `media`, `alta`, `critica` — obrigatório, padrão `media`
   - `status` — um destes cinco valores, exatamente: `aberto`,
     `em_andamento`, `resolvido`, `fechado`, `cancelado` — obrigatório,
     padrão `aberto`
   - `data_abertura` — data e hora, obrigatório, padrão o momento da
     inserção
   - `data_fechamento` — data e hora, opcional
   - **CHECK**: se `data_fechamento` estiver preenchida, ela não pode ser
     anterior a `data_abertura`

4. **`interacoes_chamado`** — o histórico de mensagens trocadas em um
   chamado (1:N: um chamado tem várias interações).
   - `id_interacao` — PK
   - `chamado_id` — FK para `chamados`, obrigatório; remover o chamado
     remove suas interações (`ON DELETE CASCADE`)
   - `autor_id` — FK para `usuarios` (cliente ou técnico que escreveu),
     obrigatório, bloqueia remoção do autor (`ON DELETE RESTRICT`)
   - `mensagem` — texto livre, obrigatório

5. **`tecnicos_chamados`** — resolve o relacionamento **N:M**: mais de um
   técnico pode colaborar no mesmo chamado, e um técnico colabora em vários
   chamados ao longo do tempo. Tem um atributo próprio do relacionamento.
   - `chamado_id` + `tecnico_id` — **chave primária composta**
   - `chamado_id` — FK para `chamados`, `ON DELETE CASCADE`
   - `tecnico_id` — FK para `usuarios`, `ON DELETE RESTRICT`
   - `horas_dedicadas` — valor decimal com casas exatas (nunca
     `FLOAT`/`DOUBLE` — Seção 5.2 da aula), obrigatório, padrão `0`
   - **CHECK**: `horas_dedicadas` nunca pode ser negativo

### Parte 2 — `ALTER TABLE`

Depois de criar as tabelas acima, adicione ao final do mesmo script três
comandos `ALTER TABLE` sobre `chamados`:

**a)** Adicione a coluna `sla_horas`, um inteiro sem sinal, **opcional**
(prazo máximo de atendimento em horas — nem todo chamado tem SLA definido).

**b)** Renomeie a coluna `titulo` para `assunto`, mantendo o mesmo tipo
(`VARCHAR(255)`) e obrigatoriedade.

**c)** Adicione uma constraint `CHECK` garantindo que, quando `sla_horas`
for informado, ele seja maior que zero (lembre-se: como a coluna é opcional,
o `CHECK` precisa aceitar explicitamente o caso `NULL` — mesmo padrão do
Checkpoint 5 da aula).

## Critérios de avaliação

A correção automática (`tests/regras_avaliacao.py`, disparada pelo Pull
Request) executa seu script contra um MariaDB descartável e confere:

- Existência do banco `helpdesk_ti` com `utf8mb4`/`utf8mb4_unicode_ci`;
- Existência de cada tabela e de suas colunas de log (Regra 9);
- Nomenclatura e composição de cada chave primária (Regra 5), incluindo a
  PK composta de `tecnicos_chamados`;
- Cada chave estrangeira: tabela/coluna referenciada e a ação `ON
  DELETE` correta (Regra 6/7) — a Regra 7 é conferida explicitamente nas
  duas FKs de `chamados` para `usuarios`;
- As constraints `UNIQUE` pedidas (email/cpf de `usuarios`, nome de
  `categorias_chamado`);
- Os `ENUM` de `prioridade` e `status` com exatamente os valores pedidos;
- O tipo `DECIMAL` de `horas_dedicadas` (nunca `FLOAT`/`DOUBLE`);
- As três constraints `CHECK` pedidas (existência e menção à coluna
  correta — não a expressão exata, para aceitar formas equivalentes de
  escrever a mesma condição);
- Os três resultados do `ALTER TABLE` da Parte 2.

**O que não é avaliado automaticamente:** nomes de `CONSTRAINT`, comentários
no código, ordem das colunas dentro de cada tabela, e qualquer decisão de
estilo que não afete a estrutura resultante no banco.

## Como entregar

1. Edite `sql/helpdesk.sql` dentro do seu fork.
2. Rode `python tests/regras_avaliacao.py --host mariadb --user aluno
   --password aluno` (dentro do Codespace) para conferir sua entrega antes
   de enviar — veja `.devcontainer/boas-vindas.sh` para o comando completo.
3. Commit, push da sua branch `entrega/<RA>-<usuario-github>` e abertura de
   Pull Request para o repositório de origem.

**O Pull Request nunca será mesclado** — ele existe só para disparar a
correção automática e registrar sua entrega. Veja o
[`README.md`](../README.md) deste template e o
[`README.md`](../../../README.md) da raiz do repositório para o passo a
passo completo.

## Se algo não estiver claro

Releia a [Aula 03](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_03_SQL_DDL/),
em especial a Seção 6 (o exemplo guiado de e-commerce, com a mesma lógica de
FK por papel semântico que você precisa aplicar em `chamados`) e a Seção 8
(`ALTER TABLE`). Persistindo a dúvida, procure o professor pelo canal de
contato indicado no README raiz deste repositório.
