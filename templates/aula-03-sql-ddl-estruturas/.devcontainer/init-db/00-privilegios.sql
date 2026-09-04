-- Executado automaticamente pelo container oficial do MariaDB na primeira
-- inicialização (arquivos em /docker-entrypoint-initdb.d/ rodam nessa hora).
--
-- Por padrão, MARIADB_USER só recebe privilégios sobre MARIADB_DATABASE
-- ("atividade"). Esta atividade, porém, pede que o próprio aluno escreva um
-- CREATE DATABASE (Parte 1 — Seção 4 da aula), então o usuário "aluno"
-- precisa de privilégio para criar/remover QUALQUER database, não só
-- "atividade". Ver docs/decisoes-arquiteturais.md.
GRANT ALL PRIVILEGES ON *.* TO 'aluno'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
