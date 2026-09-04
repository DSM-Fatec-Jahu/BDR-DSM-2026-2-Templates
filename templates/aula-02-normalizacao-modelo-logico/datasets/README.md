# datasets/

Esta pasta existe para manter a estrutura padrão de todo template deste
repositório (`sql/`, `tests/`, `datasets/`, `documentacao/`,
`solucao-professor/`), mas **fica vazia de propósito** nesta atividade.

A Aula 02 trabalha sobre tabelas descritas em texto/Markdown (a tabela
desnormalizada da Parte 1, o enunciado do MER conceitual da Parte 2) — não
há nenhum banco de dados para carregar dados ainda, porque a disciplina só
começa a rodar SQL de verdade na Aula 03 (DDL). Os "dados" desta atividade
estão em [`../documentacao/enunciado.md`](../documentacao/enunciado.md).

Se uma aula futura de modelo lógico ou DDL precisar de um dataset comum
(por exemplo, um CSV usado tanto no template de DML quanto no de consultas),
ele deve morar em `shared/datasets/`, não ser duplicado aqui — ver
`docs/guia-professor.md` na raiz do repositório.
