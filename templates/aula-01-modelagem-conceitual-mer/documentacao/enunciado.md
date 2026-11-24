# Enunciado — Atividade da Aula 01 — Modelagem Conceitual (MER)

**Disciplina:** Banco de Dados — Relacional (IBD015) · Fatec Jahu · DSM · 2º Semestre/2026
**Baseado em:** [Aula 01 — Revisão de Modelagem de Dados (Conceitual)](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_01_Revisao_Modelagem_Conceitual/) (Exercícios de Fixação 1 e 4)

---

## Objetivo

Praticar os conceitos centrais da Aula 01 — entidades, atributos,
relacionamentos, cardinalidade, participação e o mecanismo de
generalização/especialização — construindo dois modelos MER completos, em
DBML (a linguagem por trás do [dbdiagram.io](https://dbdiagram.io)),
exatamente a notação Crow's Foot vista na aula, só que como texto em vez de
desenho à mão.

Esta é a **primeira** atividade prática do semestre. Ainda não existe SQL
neste momento da disciplina — a modelagem conceitual é intencionalmente
independente de SGBD. Você já vai perceber, porém, que os nomes de chave
primária e estrangeira seguem as mesmas convenções que serão formalizadas na
Aula 03 (Regras 5 e 6): isso é proposital, para que você já construa o
hábito desde o primeiro modelo.

## O que entregar

Três arquivos, todos dentro de `sql/`:

- **[`modelo-conceitual-parte1.dbml`](../sql/modelo-conceitual-parte1.dbml)**
  — MER da Clínica Médica (Parte 1)
- **[`modelo-conceitual-parte2.dbml`](../sql/modelo-conceitual-parte2.dbml)**
  — Generalização de Pessoas (Parte 2)
- **[`modelo-conceitual.md`](../sql/modelo-conceitual.md)** — só o campo de
  texto "Restrição da hierarquia" da Parte 2 (obrigatoriedade/exclusividade
  não são coisas que dá para expressar em DBML)

Os três já vêm com um esqueleto mínimo — substitua pelo seu modelo completo.

**Como visualizar enquanto edita:** cole o conteúdo do `.dbml` em
[dbdiagram.io](https://dbdiagram.io) (botão "New Diagram" → cole no editor à
esquerda) — o diagrama aparece renderizado à direita em tempo real, e dá
para exportar como imagem quando terminar. O que vale como entrega é o
arquivo `.dbml` no seu fork, não o que fica salvo no site (dbdiagram.io não
precisa de conta para isso).

### Parte 1 — MER da Clínica Médica

> *"Uma clínica médica cadastra seus pacientes e médicos. Um médico pode ter
> várias especialidades. Os pacientes podem agendar consultas com os
> médicos. Cada consulta ocorre em uma data e horário específicos e gera um
> prontuário com o diagnóstico e a prescrição."*

Identifique as entidades, atributos e relacionamentos (com cardinalidade e
participação) descritos nesse enunciado, e escreva o modelo em DBML
correspondente. Pense com cuidado em dois pontos que costumam gerar dúvida:

- A relação entre Médico e Especialidade — um médico pode ter *várias*
  especialidades. Que tipo de cardinalidade é essa? (dica: em DBML isso é
  um `Ref:` com o operador `<>`.)
- A relação entre Consulta e Prontuário — cada consulta *gera* um
  prontuário. Prontuário é uma entidade separada de Consulta, ou deveria ser
  fundida a ela? Se for separada, qual a cardinalidade entre as duas?

Sua entrega precisa conter, no mínimo, as tabelas `pacientes`, `medicos`,
`especialidades`, `consultas` e `prontuarios`.

### Parte 2 — Generalização de Pessoas

> Entidades: **Aluno**, **Professor** e **Funcionário Administrativo** — todos
> de uma faculdade.

Proponha uma superclasse que reúna os atributos comuns às três, mantendo em
cada subclasse só os atributos exclusivos dela. Siga a **Estratégia 2**
(Seção 8.7 da aula: uma tabela para a superclasse + uma tabela por
subclasse, cada subclasse com PK própria que também é FK única para a
superclasse).

**Para a correção automática funcionar, use exatamente estes nomes:**
`pessoas` (superclasse), `alunos`, `professores`,
`funcionarios_administrativos`.

Depois de montar o diagrama, preencha o campo **Restrição da hierarquia** no
mesmo arquivo, indicando se a hierarquia é Total ou Parcial, Exclusiva ou
Sobreposta, e **justificando** sua escolha (pense em casos reais: uma pessoa
pode ser aluno e funcionário administrativo ao mesmo tempo? pode existir uma
pessoa cadastrada que ainda não é nenhuma das três?). Não existe uma única
resposta certa aqui — o que importa é a coerência entre a escolha e a
justificativa.

## Critérios de avaliação

A correção automática (veja `tests/regras_avaliacao.py`, disparada pelo
Pull Request) confere **estrutura**, não redação exata:

- Existência de cada tabela exigida;
- Nomenclatura de chave primária (`id_` + tabela no singular — Regra 5) e
  chave estrangeira (tabela referenciada no singular + `_id` — Regra 6);
- Cardinalidade correta de cada relacionamento (1:1, 1:N ou N:M);
- Presença e tamanho mínimo dos campos de texto (Obrigatoriedade,
  Exclusividade, Justificativa) da Parte 2 — a adequação da escolha ao
  enunciado, incluindo a participação da hierarquia, é revisada manualmente
  pelo professor, não pelo script (DBML não consegue expressar a
  participação do lado "um" de uma relação como uma constraint de schema).

O comentário (`//`) que você escolhe para cada `Ref:` **não** é validado
automaticamente — use-o como quiser para documentar a relação.

## Como entregar

1. Edite os três arquivos (`sql/modelo-conceitual-parte1.dbml`,
   `sql/modelo-conceitual-parte2.dbml`, `sql/modelo-conceitual.md`) dentro
   do seu fork.
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

Releia a [Aula 01](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/aulas/Aula_01_Revisao_Modelagem_Conceitual/),
em especial a Seção 10.1 (Método das quatro perguntas) e a Seção 8 (Generalização/Especialização) — os dois exemplos guiados da Seção 10.1 (ficha de
empréstimo e nota fiscal) usam exatamente o mesmo raciocínio que você precisa
aplicar aqui. Persistindo a dúvida, procure o professor pelo canal de contato
indicado no README raiz deste repositório.
