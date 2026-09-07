# Aula 02 — Normalização e Modelo Lógico

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Aula de origem:** [Aula 02 — Normalização e Passagem ao Modelo Lógico Relacional](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_02_Normalizacao/)
**Atividade:** formativa (não compõe T1/P1/T2/P2 — ver `docs/estrategia-de-avaliacao.md` na raiz)

---

## Contextualização

Esta é a segunda atividade prática do semestre, ligada à Aula 02. Se a
Aula 01 tratou de representar o mundo real em um MER conceitual, a Aula 02
cobre os dois processos que levam esse diagrama até um conjunto de tabelas
de verdade: a **normalização** (eliminar dependências parciais e
transitivas até a 3FN) e a **passagem ao modelo lógico** (traduzir cada
tipo de relacionamento do MER em tabelas, PKs e FKs). Ainda não existe SQL
de verdade aqui — isso começa na Aula 03 — mas o resultado desta atividade
já é exatamente o que vira `CREATE TABLE` na aula seguinte.

## Objetivos e competências

Ao concluir esta atividade você terá praticado:

- Identificar dependências funcionais — totais, parciais e transitivas —
  em uma tabela desnormalizada, inclusive cadeias de dependência transitiva
  "escondidas" dentro de uma dependência parcial;
- Aplicar 1FN, 2FN e 3FN progressivamente para chegar a um conjunto de
  tabelas sem redundância;
- Aplicar as quatro regras de passagem do MER ao modelo lógico (1:N, N:M
  com atributo de relacionamento, 1:1 com decisão de onde colocar a FK, e
  entidade fraca);
- Justificar a escolha do lado da FK em um relacionamento 1:1 usando os
  critérios de participação e semântica da Seção 8.1;
- Seguir a convenção de chave substituta (`id_tabela`) mesmo quando a
  tabela original usa um identificador de negócio (placa, CPF, matrícula)
  como uma das colunas.

## Requisitos

- Conta no GitHub, com fork deste repositório já criado (ver
  [README raiz](../../README.md) para o passo a passo completo de fork +
  Codespaces).
- Nenhum software local é necessário — o ambiente todo roda pelo Codespace
  configurado em [`.devcontainer/aula-02-normalizacao-modelo-logico/`](../../.devcontainer/aula-02-normalizacao-modelo-logico/)
  (na raiz do repositório, não dentro desta pasta). Se preferir rodar
  localmente, basta Python 3.10+ (só para rodar o autograder opcionalmente;
  nenhuma dependência externa é instalada, o script usa apenas biblioteca
  padrão).

## Como executar

1. No seu fork, clique em **Code → aba Codespaces → Create codespace on
   main**. Como o repositório tem uma aula por configuração, o GitHub
   pergunta qual usar — escolha **"BDR — Aula 02 — Normalização e Modelo
   Lógico"** (se o botão não perguntar nada, use "..." → "New with
   options..."). O Codespace já abre **direto nesta pasta**, com este
   `README.md` e o `documentacao/enunciado.md` abertos automaticamente — não
   precisa navegar pelo repositório.
2. Edite [`sql/modelo-logico.md`](sql/modelo-logico.md) — é o único
   arquivo que você precisa alterar. O enunciado completo está em
   [`documentacao/enunciado.md`](documentacao/enunciado.md).
3. Visualize seu diagrama com `Ctrl+Shift+V` (preview Markdown) enquanto
   edita, ou olhando o arquivo pela interface do GitHub (que também
   renderiza Mermaid nativamente).
4. Antes de entregar, rode a correção localmente para conferir sua nota
   formativa:

   ```bash
   python tests/regras_avaliacao.py
   ```

## Entregável

Só o arquivo `sql/modelo-logico.md`, com as duas partes preenchidas
(mapeamento de dependências + modelo lógico da Oficina Mecânica;
modelo lógico + justificativa da Rede de Hotéis).

## Critérios de avaliação e correção automática

A correção automática roda no Pull Request e confere **estrutura**, não
texto exato: existência das tabelas exigidas, nomenclatura de PK/FK
(Regras 5 e 6 da disciplina), cardinalidade e participação de cada
relacionamento, e o preenchimento mínimo das duas análises escritas (o
mapeamento de dependências funcionais da Parte 1 e a justificativa da FK
1:1 da Parte 2 — a qualidade do argumento em si é revisada pelo professor).
O rótulo do relacionamento (o verbo) não é validado — só a estrutura
importa. Detalhes completos em
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
