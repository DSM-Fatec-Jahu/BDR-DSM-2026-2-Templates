# datasets/

Esta pasta existe para manter a estrutura padrão de todo template deste
repositório (`sql/`, `tests/`, `datasets/`, `documentacao/`,
`solucao-professor/`), mas **fica vazia de propósito** nesta atividade.

A Aula 01 é modelagem conceitual pura — não há dados para carregar em banco
nenhum, porque não existe banco de dados nesta etapa da disciplina (isso só
começa na Aula 03, DDL). Os "dados" desta atividade são os dois enunciados
de texto em [`../documentacao/enunciado.md`](../documentacao/enunciado.md).

Se uma aula futura de modelagem lógica ou DDL precisar de um dataset comum
(por exemplo, um CSV usado tanto no template de DML quanto no de consultas),
ele deve morar em `shared/datasets/`, não ser duplicado aqui — ver
`docs/guia-professor.md` na raiz do repositório.
