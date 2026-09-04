# Enunciado — Atividade da Aula 02 — Normalização e Modelo Lógico

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Baseado em:** [Aula 02 — Normalização e Passagem ao Modelo Lógico Relacional](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_02_Normalizacao/) (Seções 2 a 8)

---

## Objetivo

Praticar os dois processos centrais da Aula 02: **normalizar** uma tabela
desnormalizada até a 3ª Forma Normal (identificando dependências parciais e
transitivas pelo caminho), e fazer a **passagem de um MER conceitual ao
modelo lógico relacional**, aplicando as regras de cada tipo de
relacionamento (1:1, 1:N, N:M, entidade fraca).

Como na Aula 01, esta atividade já é sobre **modelo lógico** — toda chave
primária segue `id_` + tabela no singular (Regra 5) e toda chave estrangeira
segue tabela-referenciada-no-singular + `_id` (Regra 6), exatamente como a
Seção 8 da aula formaliza. Ainda não existe SQL de verdade (isso começa na
Aula 03) — a entrega continua em Mermaid `erDiagram`, mas agora representando
tabelas já no modelo lógico, não mais entidades conceituais.

## O que entregar

Edite **[`sql/modelo-logico.md`](../sql/modelo-logico.md)** — ele já tem a
estrutura das duas partes abaixo, com um esqueleto mínimo em cada bloco
`mermaid` e campos de texto para as análises escritas. Substitua os
esqueletos e preencha os campos.

### Parte 1 — Normalização até a 3FN — Oficina Mecânica

Uma oficina mecânica registra suas ordens de serviço na tabela abaixo
(**não normalizada** — uma linha por item de serviço dentro da ordem):

| id_ordem | data_servico | placa_veiculo | modelo_veiculo | categoria_veiculo | cliente_cpf | cliente_nome | cliente_telefone | mecanico_matricula | mecanico_nome | mecanico_especialidade | cod_servico | descricao_servico | valor_servico | quantidade |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-04-02 | ABC1D23 | Onix | Hatch | 111.222.333-44 | Marcos Vidal | (14) 99111-2222 | M-045 | Renata Costa | Motor | S01 | Troca de óleo | 120.00 | 1 |
| 1 | 2026-04-02 | ABC1D23 | Onix | Hatch | 111.222.333-44 | Marcos Vidal | (14) 99111-2222 | M-045 | Renata Costa | Motor | S03 | Alinhamento | 90.00 | 1 |
| 2 | 2026-04-03 | XYZ9K88 | HB20 | Hatch | 555.666.777-88 | Juliana Prado | (14) 98222-3333 | M-012 | Diego Farias | Elétrica | S01 | Troca de óleo | 120.00 | 1 |

A chave primária composta desta tabela é `(id_ordem, cod_servico)`, já que
uma ordem de serviço pode ter vários serviços, e o mesmo código de serviço
(ex.: `S01`, troca de óleo) se repete em várias ordens diferentes.

**a) Mapeie as dependências funcionais** desta tabela em relação à chave
composta `(id_ordem, cod_servico)`, seguindo o formato usado nas Seções 4.2
e 5.2 da aula (`X → Y`, indicando se é total/parcial/transitiva). Preste
atenção especial: existe mais de um "nível" de dependência parcial aqui —
alguns atributos dependem só de `id_ordem`, mas dentro desses já existe uma
dependência transitiva escondida (pense em `placa_veiculo` e no que
depende *dela*, não diretamente de `id_ordem`; o mesmo vale para
`cliente_cpf` e para `mecanico_matricula`).

**b) Aplique 1FN → 2FN → 3FN** e entregue o modelo lógico final (tabelas,
PKs, FKs) como um `erDiagram`. Sua entrega precisa conter, no mínimo, seis
tabelas: `CLIENTES`, `VEICULOS`, `MECANICOS`, `SERVICOS`, `ORDENS_SERVICO` e
`ITENS_ORDEM_SERVICO`. Lembre-se: **toda PK criada por você é `id_tabela`**
(Regra 5, Seção 8.6 da aula) — `placa_veiculo`, `cliente_cpf` e
`mecanico_matricula` continuam existindo nas tabelas correspondentes, mas
como atributos comuns (com `UNIQUE`), não como chave primária.

### Parte 2 — Passagem ao Modelo Lógico — Rede de Hotéis

Uma rede de hotéis tem o seguinte MER conceitual:

- `Hospedes` (1) — `Reservas` (N): um hóspede faz várias reservas ao longo
  do tempo; toda reserva pertence a exatamente um hóspede (participação
  **total** de Reservas — não existe reserva sem hóspede).
- `Reservas` (N) — `Quartos` (M): uma reserva pode incluir mais de um
  quarto (ex.: uma família reservando dois quartos conectados), e um quarto
  aparece em várias reservas ao longo do tempo — com um atributo do próprio
  relacionamento, `valor_diaria_negociado` (o preço fechado pode variar por
  reserva, por causa de promoções ou negociação direta).
- `Hospedes` (1) — `Cartoes_Fidelidade` (1): um hóspede pode vincular um
  cartão fidelidade (participação **parcial** de Hóspedes — nem todo
  hóspede tem cartão; participação **total** de Cartões_Fidelidade — todo
  cartão vinculado pertence a exatamente um hóspede).
- `Diarias` é uma entidade fraca que só existe dentro de uma `Reserva` —
  cada diária é identificada por um `numero_diaria` que só é único *dentro*
  da reserva à qual pertence (representa o valor cobrado em cada noite de
  uma estadia).

Escreva o modelo lógico completo (tabelas, colunas, PKs e FKs) aplicando as
regras de passagem da Seção 8 da aula a cada um dos quatro relacionamentos
acima, como um `erDiagram`. Depois, preencha o campo de justificativa
pedido no arquivo de entrega, explicando **em qual tabela você colocou a FK
do relacionamento 1:1** (Hóspedes × Cartões_Fidelidade) e por quê — reveja
o Critério 1 e o Critério 2 da Seção 8.1 antes de responder.

## Critérios de avaliação

A correção automática (veja `tests/regras_avaliacao.py`, disparada pelo
Pull Request) confere **estrutura**, não redação exata:

- Existência de cada entidade exigida em ambas as partes;
- Nomenclatura de chave primária (`id_` + tabela no singular — Regra 5) e
  chave estrangeira (tabela referenciada no singular + `_id` — Regra 6);
- Cardinalidade correta de cada relacionamento (1:1, 1:N ou N:M) e
  participação correta (total/parcial) onde isso é pedido explicitamente
  (Parte 2 — Hóspedes × Cartões_Fidelidade);
- Presença e tamanho mínimo do mapeamento de dependências funcionais
  (Parte 1a) e da justificativa da FK do 1:1 (Parte 2) — a **qualidade**
  da análise escrita é revisada manualmente pelo professor, o script só
  confere se você de fato escreveu algo substancial, não se está "certo".

O rótulo (verbo) que você escolhe para cada relacionamento **não** é
validado automaticamente — escolha o que descreve melhor o negócio.

## Como entregar

1. Edite `sql/modelo-logico.md` dentro do seu fork.
2. (Opcional, mas recomendado) rode `python tests/regras_avaliacao.py`
   dentro da pasta deste template para conferir sua entrega antes de
   enviar.
3. Commit, push da sua branch `entrega/<RA>-<usuario-github>` e abertura de
   Pull Request para o repositório de origem.

**O Pull Request nunca será mesclado** — ele existe só para disparar a
correção automática e registrar sua entrega. Veja o
[`README.md`](../README.md) deste template e o
[`README.md`](../../../README.md) da raiz do repositório para o passo a
passo completo.

## Se algo não estiver claro

Releia a [Aula 02](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_02_Normalizacao/),
em especial a Seção 7 (Exemplo Completo de Normalização — Passo a Passo,
sistema de escola) e a Seção 8 (Passagem do Modelo Conceitual ao Modelo
Lógico) — os dois exemplos guiados dessas seções usam exatamente o mesmo
raciocínio que você precisa aplicar aqui. Persistindo a dúvida, procure o
professor pelo canal de contato indicado no README raiz deste repositório.
