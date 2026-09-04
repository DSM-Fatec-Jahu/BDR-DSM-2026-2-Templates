# Aula 01 — Modelagem Conceitual (MER)

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Aula de origem:** [Aula 01 — Revisão de Modelagem de Dados (Conceitual)](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_01_Revisao_Modelagem_Conceitual/)
**Atividade:** formativa (não compõe T1/P1/T2/P2 — ver `docs/estrategia-de-avaliacao.md` na raiz)

---

## Contextualização

Esta é a primeira atividade prática do semestre, ligada à Aula 01. Antes de
qualquer linha de SQL, a disciplina começa pela **modelagem conceitual**: a
etapa de representar o mundo real através de um Modelo
Entidade-Relacionamento (MER), independente de SGBD. Você vai treinar
exatamente isso aqui, usando a notação Crow's Foot em diagramas Mermaid
`erDiagram` — a mesma notação usada na aula e a mesma que ferramentas de
mercado como dbdiagram.io e MySQL Workbench usam.

## Objetivos e competências

Ao concluir esta atividade você terá praticado:

- Identificar entidades, atributos e relacionamentos a partir de uma
  descrição textual de regras de negócio;
- Aplicar corretamente cardinalidade (1:1, 1:N, N:M) e participação
  (total/parcial);
- Reconhecer quando um relacionamento N:M precisa de tratamento especial
  (Médico × Especialidade);
- Aplicar o mecanismo de generalização/especialização (superclasse +
  subclasses, Estratégia 2 — uma tabela por subclasse com FK única para a
  superclasse) e justificar o tipo de restrição da hierarquia;
- Seguir, desde o primeiro modelo, as convenções de nomenclatura de PK/FK
  que serão formalizadas na Aula 03.

## Requisitos

- Conta no GitHub, com fork deste repositório já criado (ver
  [README raiz](../../README.md) para o passo a passo completo de fork +
  Codespaces).
- Nenhum software local é necessário — o ambiente todo roda pelo
  Codespace configurado em `.devcontainer/`. Se preferir rodar localmente,
  basta Python 3.10+ (só para rodar o autograder opcionalmente; nenhuma
  dependência externa é instalada, o script usa apenas biblioteca padrão).

## Como executar

1. Abra esta pasta em um Codespace (botão **Code → Codespaces** no seu
   fork, ou `code .` se estiver usando o VS Code local com a extensão Dev
   Containers). A mensagem de boas-vindas explica os comandos básicos.
2. Edite [`sql/modelo-conceitual.md`](sql/modelo-conceitual.md) — é o único
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

Só o arquivo `sql/modelo-conceitual.md`, com as duas partes preenchidas
(Clínica Médica e Generalização de Pessoas).

## Critérios de avaliação e correção automática

A correção automática roda no Pull Request e confere **estrutura**, não
texto exato: existência das entidades exigidas, nomenclatura de PK/FK
(Regras 5 e 6 da disciplina), cardinalidade e participação de cada
relacionamento. O rótulo do relacionamento (o verbo) não é validado — só a
estrutura importa. Detalhes completos em
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
