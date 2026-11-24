-- =============================================================================
-- Entrega — Aula 03 — SQL e DDL: Definição de Estruturas
-- Schema: helpdesk_ti — Central de Chamados Técnicos
-- =============================================================================
-- Consulte o enunciado completo em ../documentacao/enunciado.md ANTES de
-- começar — é lá que estão as colunas, tipos e constraints de cada tabela.
-- Este arquivo só aponta em que ordem escrever as coisas; o conteúdo de
-- cada CREATE TABLE é seu.
--
-- Nomenclatura (regras da disciplina): snake_case, tabelas no plural, PK
-- `id_tabela` (Regra 5), FK `tabela_id` ou papel semântico (Regra 6/7),
-- toda tabela com criado_em/atualizado_em/deletado_em (Regra 9).
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Parte 1a — CREATE DATABASE
-- -----------------------------------------------------------------------------
-- TODO: DROP DATABASE IF EXISTS + CREATE DATABASE IF NOT EXISTS helpdesk_ti,
-- com CHARACTER SET e COLLATE corretos (enunciado, Parte 1a).

-- -----------------------------------------------------------------------------
-- Parte 1b — CREATE TABLE
-- -----------------------------------------------------------------------------

-- TODO: CREATE TABLE usuarios (enunciado, Parte 1b item 1).

-- TODO: CREATE TABLE categorias_chamado (enunciado, Parte 1b item 2).

-- TODO: CREATE TABLE chamados (enunciado, Parte 1b item 3 — atenção à
-- Regra 7: cliente_id e tecnico_responsavel_id referenciam a MESMA tabela).

-- TODO: CREATE TABLE interacoes_chamado (enunciado, Parte 1b item 4).

-- TODO: CREATE TABLE tecnicos_chamados (enunciado, Parte 1b item 5 — N:M
-- com atributo próprio e PK composta).

-- -----------------------------------------------------------------------------
-- Parte 2 — ALTER TABLE
-- -----------------------------------------------------------------------------

-- TODO (a): ALTER TABLE chamados — adicione sla_horas (enunciado, Parte 2a).

-- TODO (b): ALTER TABLE chamados — renomeie titulo para assunto (enunciado, Parte 2b).

-- TODO (c): ALTER TABLE chamados — adicione o CHECK de sla_horas (enunciado, Parte 2c).
