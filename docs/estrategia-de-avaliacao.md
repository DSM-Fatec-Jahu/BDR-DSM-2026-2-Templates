# Estratégia de Avaliação

## Duas categorias de atividade neste repositório

### 1. Atividades formativas (aulas, laboratórios, desafios de prática)

Modelo padrão deste repositório: fork público + Pull Request + correção
automática visível no próprio PR (ver `docs/estrategia-github-education.md`).
Servem para o aluno praticar e receber feedback imediato — **não** compõem
diretamente a fórmula oficial de nota da disciplina
(`Nota Final = (T1 + P1 + T2 + P2) × 1 + R`, ver `index.md` do repositório
de conteúdo). A exposição de soluções entre colegas nos PRs é um trade-off
aceito aqui, porque o objetivo é prática, não seleção.

A **Aula 01** (`templates/aula-01-modelagem-conceitual-mer/`) é o primeiro
exemplo desse modelo: nota formativa de 0 a 10, calculada pela proporção de
critérios estruturais atendidos, sem peso na nota final.

### 2. Atividades avaliativas de peso na nota (T1, P1, T2, P2, R)

Essas **não** devem usar o repositório público como mecanismo de entrega —
a visibilidade entre colegas que é aceitável para prática formativa deixa
de ser aceitável quando a nota individual e a integridade da avaliação
estão em jogo. Mecanismo a adotar quando essas atividades forem
processadas como alvo (T1 — Modelagem de Streaming, na Aula 05; P1; T2 — na
Aula 17; P2; R):

- Repositório **privado individual**, criado sob demanda por aluno (ou por
  dupla/equipe, conforme a atividade), com o aluno convidado como
  colaborador.
- O mesmo padrão de `.devcontainer` + Actions do template correspondente é
  reaproveitado dentro desse repositório privado — só a visibilidade muda.
- Avaliações **teóricas** (P1, P2) provavelmente não se beneficiam do
  mesmo mecanismo de PR + autograding — são provas individuais, com
  formato a definir quando esses alvos forem processados.

Este documento será expandido com o mecanismo concreto (criação do
repositório privado, automação ou processo manual) quando a primeira
atividade avaliativa de peso (T1, Aula 05) for processada como alvo.

## Avaliação diagnóstica e formativa

As duas primeiras camadas de verificação de aprendizado já embutidas nas
aulas do repositório de conteúdo — `<quiz>` de fixação e flashcards
colapsáveis (`??? question`) — são **diagnósticas/formativas por natureza**:
o site é estático, sem login nem banco de dados, então nenhum resultado de
quiz ou flashcard é persistido. Servem para autoavaliação do aluno durante
a leitura, não para nota. Os templates deste repositório complementam essa
camada com uma atividade prática que *é* corrigida (ainda que
formativamente) e cujo resultado fica registrado no histórico do PR.

## Desafios extras

Nenhum desafio extra foi ainda definido para a Aula 01 — o conteúdo da
aula (modelagem conceitual pura) já é coberto integralmente pelas duas
partes do template. Um desafio extra natural para revisão futura seria
pedir ao aluno para modelar o cenário de streaming citado na Seção 9 da
aula (prévia da Atividade T1) — mas isso pertenceria ao **projeto
integrador da Aula 05**, não a um desafio extra da Aula 01, para não
antecipar uma atividade avaliativa de peso. Ver `docs/plano-de-atividades.md`.

## Limitações da correção automatizada

O autograder desta aula (`shared/utilitarios/mer_mermaid.py` +
`tests/regras_avaliacao.py` de cada template) verifica **estrutura**:
existência de entidades, nomenclatura de PK/FK, cardinalidade e
participação de relacionamentos. Ele explicitamente **não** valida:

- o rótulo/verbo escolhido para um relacionamento (múltiplas redações
  corretas são aceitas);
- a adequação semântica de uma escolha de modelagem que tem mais de uma
  resposta defensável (ex.: o tipo de restrição da hierarquia de
  generalização na Parte 2 — o script só confere se o aluno *decidiu e
  justificou*, não se a decisão é a "certa", porque nesse caso específico
  mais de uma resposta é defensável dependendo da interpretação do
  enunciado);
- qualidade da escrita, clareza do diagrama, ou nomes de entidade/atributo
  que fujam ligeiramente da convenção mas sejam defensáveis.

A nota automática é **referência formativa** — a avaliação final de
qualidade pedagógica de uma entrega continua sendo prerrogativa do
professor.
