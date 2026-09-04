# Projetos Integradores

Mapeamento de quais conceitos, uma vez cobertos por um alvo processado,
servem de base para projetos maiores — classificados como **pequeno**
(ex.: um exercício de consolidação de 1-2 aulas), **médio** (integra um
bloco inteiro da disciplina) ou **semestral** (integra múltiplos blocos ou
múltiplas disciplinas, caso do T2 interdisciplinar).

Templates de projeto propriamente ditos, quando gerados, vivem em
`projetos/` na raiz deste repositório (ver `projetos/README.md`) — este
documento só rastreia a relação entre conceitos de aula e esses projetos,
não duplica o conteúdo deles.

---

## Aula 01 — Modelagem Conceitual (MER)

A Aula 01 sozinha não gera um projeto integrador — ela é a base conceitual
de que **todo** projeto de modelagem na disciplina depende. Duas conexões
diretas já visíveis a partir do conteúdo processado até agora:

| Projeto associado | Porte | Como a Aula 01 alimenta |
|---|---|---|
| **Atividade T1 — Modelagem de Sistema de Streaming** (Aula 05, ainda não processada como alvo) | Médio | O enunciado do T1 é literalmente prefigurado na Seção 9 da Aula 01 ("Exemplo Prático — Sistema de Streaming, prévia do T1") — músicas e filmes com generalização/especialização, playlists mistas. A técnica de generalização praticada na Parte 2 do template da Aula 01 (Pessoas → Aluno/Professor/Funcionário Administrativo) é diretamente aplicável ao par Música/Filme sob uma superclasse Conteúdo. |
| **Projeto integrador semestral** (natureza ainda a definir — depende de quais aulas de Bloco 3/4 forem processadas) | Semestral | Qualquer projeto de banco de dados completo, de qualquer domínio, começa pela etapa de modelagem conceitual ensinada aqui. A Aula 01 é pré-requisito transversal, não específico a um domínio. |

## Aula 02 — Normalização e Modelo Lógico

Assim como a Aula 01, a Aula 02 sozinha não gera um projeto integrador —
mas ela fecha o pré-requisito conceitual completo (MER + normalização +
modelo lógico) do qual qualquer projeto de modelagem da disciplina
depende. Uma conexão direta:

| Projeto associado | Porte | Como a Aula 02 alimenta |
|---|---|---|
| **Atividade T1 — Modelagem de Sistema de Streaming** (Aula 05, ainda não processada como alvo) | Médio | O T1 pede um MER completo *e* sua passagem ao modelo lógico normalizado — não só o diagrama conceitual da Aula 01. A Parte 2 do template da Aula 02 (rede de hotéis) pratica exatamente o tipo de decisão que o T1 vai exigir num domínio diferente: relacionamento N:M com atributo próprio (Reserva×Quarto ↔ Playlist×Música/Filme do T1) e decisão de lado de FK em 1:1. |
| **Projeto integrador semestral** (natureza ainda a definir — depende de quais aulas de Bloco 3/4 forem processadas) | Semestral | Qualquer projeto de banco de dados completo, de qualquer domínio, precisa passar por normalização antes do `CREATE TABLE`. A Aula 02, como a Aula 01, é pré-requisito transversal, não específico a um domínio. |

## Padrão a seguir quando um projeto integrador for de fato processado

Quando `T1 — Modelagem Streaming` (ou outro projeto) for solicitado como
alvo, este documento deve ganhar uma entrada própria explicando: quais
aulas/templates anteriores ele integra, o porte (pequeno/médio/semestral),
e a relação com as competências oficiais da disciplina listadas na Ementa
(`index.md` do repositório de conteúdo). O template do projeto em si vai
para `projetos/<nome-do-projeto>/`, seguindo a mesma estrutura padrão de
`templates/` (Fase 2), mas fora dessa pasta para deixar claro que é maior
em escopo que uma atividade de aula única.

---

*(Nenhum projeto integrador foi processado como alvo até o momento — esta
seção será expandida quando isso acontecer.)*
