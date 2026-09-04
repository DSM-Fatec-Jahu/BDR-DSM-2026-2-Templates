# Aula 03 — SQL e DDL: Definição de Estruturas

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Aula de origem:** [Aula 03 — SQL e DDL: Definição de Estruturas](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_03_SQL_DDL/)
**Atividade:** formativa (não compõe T1/P1/T2/P2 — ver `docs/estrategia-de-avaliacao.md` na raiz)

---

## Contextualização

Esta é a terceira atividade prática do semestre, e a primeira com **SQL de
verdade**. As Aulas 01 e 02 ficaram inteiramente no papel (MER conceitual,
depois modelo lógico); a Aula 03 transforma esse modelo em um banco de
dados real, usando os comandos `CREATE`, `ALTER` e `DROP` da DDL (Data
Definition Language). O cenário desta atividade — uma central de chamados
técnicos (helpdesk) — é original, mas pratica exatamente os mesmos
mecanismos do exemplo de e-commerce trabalhado passo a passo na aula.

## Objetivos e competências

Ao concluir esta atividade você terá praticado:

- Criar um banco de dados idempotente, com `CHARACTER SET`/`COLLATE`
  corretos para texto em português (Seção 4 da aula);
- Aplicar as 9 regras de nomenclatura da disciplina em tabelas de verdade,
  incluindo o caso mais sutil — FK pelo papel semântico, não pelo nome da
  tabela (Regra 7), quando duas colunas da mesma tabela referenciam a
  mesma tabela em papéis diferentes;
- Escolher tipos de dados corretos (`DECIMAL` para valores fracionários,
  `ENUM` para domínio fechado, `CHAR` vs `VARCHAR`, `DATETIME` para campos
  de log) e justificar a escolha;
- Aplicar `PRIMARY KEY` (simples e composta), `FOREIGN KEY` com `ON
  DELETE`/`ON UPDATE`, `UNIQUE` e `CHECK`;
- Modificar uma tabela já criada com `ALTER TABLE` (`ADD COLUMN`, `CHANGE
  COLUMN`, `ADD CONSTRAINT`).

## Requisitos

- Conta no GitHub, com fork deste repositório já criado (ver
  [README raiz](../../README.md) para o passo a passo completo de fork +
  Codespaces).
- Um Codespace (ou Dev Container local) usando o `.devcontainer/` desta
  pasta — ele já sobe um MariaDB 11.4 num container próprio, sem nenhuma
  instalação manual. Se preferir rodar 100% localmente sem Codespaces, você
  precisa de um MariaDB/MySQL acessível (ex.: XAMPP, como em sala) e do
  cliente `mysql` no PATH.

## Como executar

1. Abra esta pasta em um Codespace (botão **Code → Codespaces** no seu
   fork). A mensagem de boas-vindas explica os comandos básicos e as
   credenciais de conexão do MariaDB.
2. Edite [`sql/helpdesk.sql`](sql/helpdesk.sql) — é o único arquivo que
   você precisa alterar. O enunciado completo está em
   [`documentacao/enunciado.md`](documentacao/enunciado.md).
3. Teste seu script a qualquer momento rodando-o direto contra o MariaDB:

   ```bash
   mysql -h mariadb -u aluno -paluno < sql/helpdesk.sql
   ```

4. Antes de entregar, rode a correção localmente para conferir sua nota
   formativa (ela executa o mesmo script e confere a estrutura resultante):

   ```bash
   python tests/regras_avaliacao.py --host mariadb --user aluno --password aluno
   ```

## Entregável

Só o arquivo `sql/helpdesk.sql`, com a Parte 1 (`CREATE DATABASE` + 5
`CREATE TABLE`) e a Parte 2 (3 comandos `ALTER TABLE`) completas.

## Critérios de avaliação e correção automática

A correção automática roda no Pull Request **executando seu script contra
um MariaDB descartável** e conferindo a estrutura resultante via
`INFORMATION_SCHEMA` — não o texto do seu SQL. Isso significa que qualquer
abordagem válida que chegue ao mesmo schema é aceita (ordem de colunas,
nomes de `CONSTRAINT`, e comentários não são avaliados); os nomes de banco,
tabela e coluna pedidos no enunciado, porém, são exatos e obrigatórios —
é assim que o corretor localiza o que você criou. Se o script tiver um erro
de sintaxe, a correção mostra a mensagem exata do MariaDB em vez de uma
lista de critérios. Detalhes completos em
[`documentacao/enunciado.md`](documentacao/enunciado.md#critérios-de-avaliação).

O resultado aparece automaticamente como **comentário no seu Pull Request**
e como **resumo do job** na aba Actions — não existe painel externo.

## ⚠️ Sobre o Pull Request

A entrega é feita abrindo um **Pull Request do seu fork para este
repositório de origem**. Esse Pull Request **nunca será mesclado (merge)** —
ele existe só para disparar a correção automática e deixar sua entrega
registrada e visível para você e para o professor. Não espere (nem peça)
que o PR seja aceito. Veja o passo a passo completo de fork → branch → PR no
[README da raiz do repositório](../../README.md).
