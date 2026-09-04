"""Executor e introspector de DDL real contra um servidor MariaDB.

Usado pelo autograding de qualquer template a partir da Aula 03 (primeiro
alvo com SQL de verdade — ver `docs/decisoes-arquiteturais.md`): roda o
script `.sql` entregue pelo aluno contra um MariaDB descartável (container
de serviço no GitHub Actions, ou o do `.devcontainer` ao testar localmente)
e confere a **estrutura** resultante via `INFORMATION_SCHEMA` — existência
de tabela/coluna, PK, FK (com `ON DELETE`/`ON UPDATE`), `UNIQUE` e `CHECK` —
nunca comparação de texto do script em si, para não travar em abordagens
diferentes que cheguem ao mesmo schema.

Depende só do cliente `mysql` de linha de comando (biblioteca padrão do
Python via `subprocess` — nenhum pacote pip como `mysql-connector-python` é
instalado), mesma filosofia de "sem dependência externa" já usada em
`mer_mermaid.py`.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class ConexaoMariaDB:
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = "root"

    def _base_cmd(self) -> list[str]:
        # Sempre usa a forma longa `--password=` (mesmo vazia): a forma curta
        # `-p` sem valor colado imediatamente após faz o cliente `mysql`
        # entrar em modo interativo de prompt de senha, travando o processo.
        return [
            "mysql",
            f"--host={self.host}",
            f"--port={self.port}",
            f"--user={self.user}",
            f"--password={self.password}",
            "--protocol=tcp",
            "--connect-timeout=10",
        ]

    def rodar_script(self, caminho_sql: str) -> subprocess.CompletedProcess:
        """Executa um arquivo `.sql` inteiro (pode conter CREATE DATABASE,
        múltiplos CREATE TABLE, ALTER TABLE etc.) numa única sessão."""
        with open(caminho_sql, "rb") as f:
            return subprocess.run(
                self._base_cmd(),
                stdin=f,
                capture_output=True,
                text=True,
                timeout=120,
            )

    def query(self, sql: str) -> list[list[str]]:
        """Roda uma consulta e devolve as linhas como listas de strings
        (`-N -B` = sem cabeçalho, separado por tab)."""
        resultado = subprocess.run(
            [*self._base_cmd(), "-N", "-B", "-e", sql],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if resultado.returncode != 0:
            raise RuntimeError(f"Falha ao consultar MariaDB: {resultado.stderr.strip()}")
        linhas = [l for l in resultado.stdout.splitlines() if l != ""]
        return [linha.split("\t") for linha in linhas]


def database_existe(conexao: ConexaoMariaDB, nome_banco: str) -> bool:
    linhas = conexao.query(
        f"SELECT SCHEMA_NAME FROM information_schema.SCHEMATA "
        f"WHERE SCHEMA_NAME = '{nome_banco}';"
    )
    return len(linhas) > 0


def database_charset_collation(conexao: ConexaoMariaDB, nome_banco: str) -> Optional[tuple[str, str]]:
    linhas = conexao.query(
        "SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME "
        "FROM information_schema.SCHEMATA "
        f"WHERE SCHEMA_NAME = '{nome_banco}';"
    )
    if not linhas:
        return None
    return (linhas[0][0], linhas[0][1])


def tabela_existe(conexao: ConexaoMariaDB, banco: str, tabela: str) -> bool:
    linhas = conexao.query(
        "SELECT TABLE_NAME FROM information_schema.TABLES "
        f"WHERE TABLE_SCHEMA = '{banco}' AND TABLE_NAME = '{tabela}';"
    )
    return len(linhas) > 0


@dataclass
class ColunaInfo:
    data_type: str
    column_type: str
    is_nullable: bool
    column_default: Optional[str]
    extra: str


def coluna_info(conexao: ConexaoMariaDB, banco: str, tabela: str, coluna: str) -> Optional[ColunaInfo]:
    linhas = conexao.query(
        "SELECT DATA_TYPE, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA "
        "FROM information_schema.COLUMNS "
        f"WHERE TABLE_SCHEMA = '{banco}' AND TABLE_NAME = '{tabela}' AND COLUMN_NAME = '{coluna}';"
    )
    if not linhas:
        return None
    data_type, column_type, is_nullable, column_default, extra = linhas[0]
    return ColunaInfo(
        data_type=data_type,
        column_type=column_type,
        is_nullable=(is_nullable.upper() == "YES"),
        column_default=column_default if column_default != "NULL" else None,
        extra=extra,
    )


def colunas_pk(conexao: ConexaoMariaDB, banco: str, tabela: str) -> list[str]:
    linhas = conexao.query(
        "SELECT k.COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE k "
        "JOIN information_schema.TABLE_CONSTRAINTS t "
        "  ON t.CONSTRAINT_SCHEMA = k.CONSTRAINT_SCHEMA AND t.CONSTRAINT_NAME = k.CONSTRAINT_NAME "
        "  AND t.TABLE_NAME = k.TABLE_NAME "
        f"WHERE k.TABLE_SCHEMA = '{banco}' AND k.TABLE_NAME = '{tabela}' "
        "  AND t.CONSTRAINT_TYPE = 'PRIMARY KEY' "
        "ORDER BY k.ORDINAL_POSITION;"
    )
    return [l[0] for l in linhas]


@dataclass
class FKInfo:
    referenced_table: str
    referenced_column: str
    delete_rule: str
    update_rule: str


def fk_info(conexao: ConexaoMariaDB, banco: str, tabela: str, coluna: str) -> Optional[FKInfo]:
    linhas = conexao.query(
        "SELECT k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME, "
        "       r.DELETE_RULE, r.UPDATE_RULE "
        "FROM information_schema.KEY_COLUMN_USAGE k "
        "JOIN information_schema.REFERENTIAL_CONSTRAINTS r "
        "  ON r.CONSTRAINT_SCHEMA = k.CONSTRAINT_SCHEMA AND r.CONSTRAINT_NAME = k.CONSTRAINT_NAME "
        f"WHERE k.TABLE_SCHEMA = '{banco}' AND k.TABLE_NAME = '{tabela}' "
        f"  AND k.COLUMN_NAME = '{coluna}' AND k.REFERENCED_TABLE_NAME IS NOT NULL;"
    )
    if not linhas:
        return None
    referenced_table, referenced_column, delete_rule, update_rule = linhas[0]
    return FKInfo(
        referenced_table=referenced_table,
        referenced_column=referenced_column,
        delete_rule=delete_rule,
        update_rule=update_rule,
    )


def unique_existe(conexao: ConexaoMariaDB, banco: str, tabela: str, colunas: list[str]) -> bool:
    """Confere se existe uma constraint UNIQUE cobrindo exatamente este
    conjunto de colunas (ordem não importa)."""
    linhas = conexao.query(
        "SELECT t.CONSTRAINT_NAME, k.COLUMN_NAME "
        "FROM information_schema.TABLE_CONSTRAINTS t "
        "JOIN information_schema.KEY_COLUMN_USAGE k "
        "  ON k.CONSTRAINT_SCHEMA = t.CONSTRAINT_SCHEMA AND k.CONSTRAINT_NAME = t.CONSTRAINT_NAME "
        "  AND k.TABLE_NAME = t.TABLE_NAME "
        f"WHERE t.TABLE_SCHEMA = '{banco}' AND t.TABLE_NAME = '{tabela}' "
        "  AND t.CONSTRAINT_TYPE = 'UNIQUE';"
    )
    grupos: dict[str, list[str]] = {}
    for nome_constraint, coluna in linhas:
        grupos.setdefault(nome_constraint, []).append(coluna)
    alvo = sorted(c.lower() for c in colunas)
    return any(sorted(c.lower() for c in cols) == alvo for cols in grupos.values())


def check_existe(conexao: ConexaoMariaDB, banco: str, tabela: str, *, contendo: Optional[str] = None) -> bool:
    """Confere se existe ao menos uma constraint CHECK na tabela — opcionalmente
    exigindo que a cláusula mencione uma substring (ex.: o nome de uma coluna),
    sem exigir a expressão exata (várias formas de escrever o mesmo CHECK são
    aceitas — ex.: `x > 0` e `0 < x`)."""
    linhas = conexao.query(
        "SELECT cc.CHECK_CLAUSE FROM information_schema.CHECK_CONSTRAINTS cc "
        "JOIN information_schema.TABLE_CONSTRAINTS t "
        "  ON t.CONSTRAINT_SCHEMA = cc.CONSTRAINT_SCHEMA AND t.CONSTRAINT_NAME = cc.CONSTRAINT_NAME "
        f"WHERE cc.CONSTRAINT_SCHEMA = '{banco}' AND t.TABLE_NAME = '{tabela}';"
    )
    if not linhas:
        return False
    if contendo is None:
        return True
    contendo_lower = contendo.lower()
    return any(contendo_lower in linha[0].lower() for linha in linhas)


def coluna_e_enum_com_valores(coluna: ColunaInfo, valores_esperados: list[str]) -> bool:
    """Confere se COLUMN_TYPE é um ENUM contendo todos os valores esperados
    (ex.: `enum('aberto','em_andamento',...)`, case-insensitive)."""
    tipo = coluna.column_type.lower()
    if not tipo.startswith("enum("):
        return False
    return all(f"'{v.lower()}'" in tipo for v in valores_esperados)
