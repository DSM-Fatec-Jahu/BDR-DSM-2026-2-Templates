-- =============================================================================
-- Entrega — Aula 03 — SQL e DDL: Definição de Estruturas
-- Schema: helpdesk_ti — Central de Chamados Técnicos
-- =============================================================================
-- Consulte o enunciado completo em ../documentacao/enunciado.md antes de
-- começar. Este arquivo já traz a Parte 1a (CREATE DATABASE) pronta e o
-- esqueleto mínimo de cada tabela da Parte 1b — complete as colunas,
-- constraints e os comandos ALTER TABLE da Parte 2.
--
-- Nomenclatura (regras da disciplina): snake_case, tabelas no plural, PK
-- `id_tabela` (Regra 5), FK `tabela_id` ou papel semântico (Regra 6/7),
-- toda tabela com criado_em/atualizado_em/deletado_em (Regra 9).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Parte 1a — CREATE DATABASE
-- -----------------------------------------------------------------------------
DROP DATABASE IF EXISTS helpdesk_ti;

CREATE DATABASE IF NOT EXISTS helpdesk_ti
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE helpdesk_ti;

-- -----------------------------------------------------------------------------
-- Parte 1b — CREATE TABLE
-- -----------------------------------------------------------------------------

-- TODO: complete as colunas e constraints de "usuarios".
-- Representa tanto clientes quanto técnicos (o papel vem da FK que
-- referencia esta tabela, não de uma coluna aqui).
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- TODO: nome, email (UNIQUE), cpf (UNIQUE), telefone (opcional),
    -- e os três campos de log da Regra 9.

    CONSTRAINT pk_usuario PRIMARY KEY (id_usuario)
);

-- TODO: complete "categorias_chamado" (id_categoria_chamado PK, nome
-- UNIQUE, descricao, ativa, + campos de log).
CREATE TABLE IF NOT EXISTS categorias_chamado (
    id_categoria_chamado BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    CONSTRAINT pk_categoria_chamado PRIMARY KEY (id_categoria_chamado)
);

-- TODO: complete "chamados". Atenção especial à Regra 7: cliente_id e
-- tecnico_responsavel_id referenciam a MESMA tabela (usuarios), com papéis
-- diferentes e ON DELETE diferentes (ver enunciado).
CREATE TABLE IF NOT EXISTS chamados (
    id_chamado BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- TODO: cliente_id (FK usuarios, RESTRICT), tecnico_responsavel_id
    -- (FK usuarios, opcional, SET NULL), categoria_id (FK
    -- categorias_chamado, RESTRICT), titulo, descricao, prioridade (ENUM),
    -- status (ENUM), data_abertura, data_fechamento, CHECK de datas,
    -- + campos de log.

    CONSTRAINT pk_chamado PRIMARY KEY (id_chamado)
);

-- TODO: complete "interacoes_chamado" (1:N a partir de chamados).
CREATE TABLE IF NOT EXISTS interacoes_chamado (
    id_interacao BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    -- TODO: chamado_id (FK chamados, CASCADE), autor_id (FK usuarios,
    -- RESTRICT), mensagem, + campos de log.

    CONSTRAINT pk_interacao PRIMARY KEY (id_interacao)
);

-- TODO: complete "tecnicos_chamados" — resolve o N:M entre chamados e
-- usuarios (papel: técnicos colaboradores), com atributo próprio
-- (horas_dedicadas) e PK composta.
CREATE TABLE IF NOT EXISTS tecnicos_chamados (
    chamado_id BIGINT UNSIGNED NOT NULL,
    tecnico_id BIGINT UNSIGNED NOT NULL,

    -- TODO: horas_dedicadas (DECIMAL, CHECK >= 0), + campos de log,
    -- + as duas FKs (chamado_id CASCADE, tecnico_id RESTRICT).

    CONSTRAINT pk_tecnico_chamado PRIMARY KEY (chamado_id, tecnico_id)
);

-- -----------------------------------------------------------------------------
-- Parte 2 — ALTER TABLE
-- -----------------------------------------------------------------------------

-- TODO (a): adicione a coluna sla_horas (INT UNSIGNED, opcional) em chamados.

-- TODO (b): renomeie a coluna titulo para assunto em chamados, mantendo o
-- tipo VARCHAR(255).

-- TODO (c): adicione um CHECK garantindo que sla_horas, quando informado,
-- seja maior que zero.
