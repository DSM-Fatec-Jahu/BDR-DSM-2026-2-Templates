# datasets/

Esta pasta existe para manter a estrutura padrão de todo template deste
repositório (`sql/`, `tests/`, `datasets/`, `documentacao/`,
`solucao-professor/`), mas **fica vazia de propósito** nesta atividade.

A Aula 03 é sobre **criar a estrutura** (DDL) — `CREATE DATABASE`,
`CREATE TABLE`, `ALTER TABLE`. Não há nenhum dado para carregar ainda: isso
começa na Aula 04 (DML — `INSERT`, `UPDATE`, `DELETE`), quando as tabelas
criadas aqui poderiam, em tese, ganhar linhas de verdade.

Se uma aula futura de DML ou consultas precisar de um dataset comum (por
exemplo, um schema ou massa de dados fictícia reaproveitada entre vários
templates), ele deve morar em `shared/datasets/` ou `shared/schemas/`, não
ser duplicado aqui — ver `docs/guia-professor.md` na raiz do repositório.
