#!/usr/bin/env python3
"""Autograding da Aula 03 — SQL e DDL: Definição de Estruturas.

Diferente das Aulas 01 e 02 (que validam um `.md` com Mermaid via regex),
esta é a primeira atividade com SQL de verdade: o script entregue
(`sql/helpdesk.sql`) é EXECUTADO contra um MariaDB descartável, e a correção
confere a **estrutura resultante** via `INFORMATION_SCHEMA` — nunca o texto
do script em si — para aceitar qualquer abordagem que chegue ao mesmo
schema (ordem diferente de colunas, nomes de constraint diferentes desde
que a nomenclatura das Regras 5/6/9 seja seguida, etc.).

Uso:
    python regras_avaliacao.py [--entrega CAMINHO] [--saida-json CAMINHO]
                                [--host H] [--port P] [--user U] [--password S]

Import de `shared/utilitarios/`: ver comentário equivalente em
`tests/regras_avaliacao.py` da Aula 02 — o workflow de autograding configura
a raiz do repo como `shared` no PYTHONPATH.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_AQUI = Path(__file__).resolve()
# tests/regras_avaliacao.py -> tests/ -> <template>/ -> templates/ -> <raiz do repo>/shared
_SHARED = _AQUI.parents[3] / "shared"
if _SHARED.exists() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from utilitarios.avaliacao import Criterio, montar_relatorio, relatorio_para_markdown  # noqa: E402
from utilitarios.mariadb_ddl import (  # noqa: E402
    ConexaoMariaDB,
    check_existe,
    coluna_e_enum_com_valores,
    coluna_info,
    colunas_pk,
    database_charset_collation,
    database_existe,
    fk_info,
    tabela_existe,
    unique_existe,
)

BANCO = "helpdesk_ti"


def avaliar_parte_1(conexao: ConexaoMariaDB) -> list[Criterio]:
    """Parte 1 — CREATE DATABASE + CREATE TABLE (schema completo)."""
    c: list[Criterio] = []

    c.append(
        Criterio(
            f"Banco `{BANCO}` existe",
            database_existe(conexao, BANCO),
            f"Esperado `CREATE DATABASE` (idempotente) chamado exatamente `{BANCO}`.",
        )
    )

    charset_collation = database_charset_collation(conexao, BANCO)
    if charset_collation:
        charset, collation = charset_collation
        c.append(
            Criterio(
                "Banco usa CHARACTER SET utf8mb4",
                charset == "utf8mb4",
                f"Charset encontrado: `{charset}` (Seção 4.3 — sempre utf8mb4, nunca utf8).",
            )
        )
        c.append(
            Criterio(
                "Banco usa COLLATE utf8mb4_unicode_ci",
                collation == "utf8mb4_unicode_ci",
                f"Collation encontrada: `{collation}` (Seção 4.4 — recomendada para português).",
            )
        )
    else:
        c.append(Criterio("Banco usa CHARACTER SET utf8mb4", False, "Banco não existe — não foi possível conferir."))
        c.append(Criterio("Banco usa COLLATE utf8mb4_unicode_ci", False, "Banco não existe — não foi possível conferir."))

    # ---- usuarios ----
    c.append(_checar_tabela(conexao, "usuarios"))
    c.append(_checar_pk(conexao, "usuarios", ["id_usuario"]))
    c.append(_checar_unique(conexao, "usuarios", ["email"], descricao="`usuarios.email` é UNIQUE"))
    c.append(_checar_unique(conexao, "usuarios", ["cpf"], descricao="`usuarios.cpf` é UNIQUE"))
    c.extend(_checar_campos_log(conexao, "usuarios"))

    # ---- categorias_chamado ----
    c.append(_checar_tabela(conexao, "categorias_chamado"))
    c.append(_checar_pk(conexao, "categorias_chamado", ["id_categoria_chamado"]))
    c.append(_checar_unique(conexao, "categorias_chamado", ["nome"], descricao="`categorias_chamado.nome` é UNIQUE"))

    # ---- chamados ----
    c.append(_checar_tabela(conexao, "chamados"))
    c.append(_checar_pk(conexao, "chamados", ["id_chamado"]))
    c.append(
        _checar_fk(
            conexao, "chamados", "cliente_id", "usuarios", "id_usuario",
            delete_esperado="RESTRICT",
            descricao="`chamados.cliente_id` referencia `usuarios` (papel: cliente — Regra 7) com ON DELETE RESTRICT",
        )
    )
    c.append(
        _checar_fk(
            conexao, "chamados", "tecnico_responsavel_id", "usuarios", "id_usuario",
            delete_esperado="SET NULL",
            descricao="`chamados.tecnico_responsavel_id` referencia `usuarios` (papel: técnico — Regra 7) com ON DELETE SET NULL",
        )
    )
    c.append(
        _checar_fk(
            conexao, "chamados", "categoria_id", "categorias_chamado", "id_categoria_chamado",
            delete_esperado="RESTRICT",
            descricao="`chamados.categoria_id` referencia `categorias_chamado` com ON DELETE RESTRICT",
        )
    )
    info_prioridade = coluna_info(conexao, BANCO, "chamados", "prioridade")
    c.append(
        Criterio(
            "`chamados.prioridade` é ENUM com os 4 valores esperados",
            info_prioridade is not None
            and coluna_e_enum_com_valores(info_prioridade, ["baixa", "media", "alta", "critica"]),
            f"Tipo encontrado: `{info_prioridade.column_type if info_prioridade else '(coluna não existe)'}`.",
        )
    )
    info_status = coluna_info(conexao, BANCO, "chamados", "status")
    c.append(
        Criterio(
            "`chamados.status` é ENUM com os 5 valores esperados",
            info_status is not None
            and coluna_e_enum_com_valores(
                info_status, ["aberto", "em_andamento", "resolvido", "fechado", "cancelado"]
            ),
            f"Tipo encontrado: `{info_status.column_type if info_status else '(coluna não existe)'}`.",
        )
    )
    c.extend(_checar_campos_log(conexao, "chamados"))

    # ---- interacoes_chamado ----
    c.append(_checar_tabela(conexao, "interacoes_chamado"))
    c.append(_checar_pk(conexao, "interacoes_chamado", ["id_interacao"]))
    c.append(
        _checar_fk(
            conexao, "interacoes_chamado", "chamado_id", "chamados", "id_chamado",
            delete_esperado="CASCADE",
            descricao="`interacoes_chamado.chamado_id` referencia `chamados` com ON DELETE CASCADE",
        )
    )
    c.append(
        _checar_fk(
            conexao, "interacoes_chamado", "autor_id", "usuarios", "id_usuario",
            delete_esperado="RESTRICT",
            descricao="`interacoes_chamado.autor_id` referencia `usuarios` com ON DELETE RESTRICT",
        )
    )

    # ---- tecnicos_chamados (N:M com atributo) ----
    c.append(_checar_tabela(conexao, "tecnicos_chamados"))
    c.append(_checar_pk(conexao, "tecnicos_chamados", ["chamado_id", "tecnico_id"]))
    c.append(
        _checar_fk(
            conexao, "tecnicos_chamados", "chamado_id", "chamados", "id_chamado",
            delete_esperado="CASCADE",
            descricao="`tecnicos_chamados.chamado_id` referencia `chamados` com ON DELETE CASCADE",
        )
    )
    c.append(
        _checar_fk(
            conexao, "tecnicos_chamados", "tecnico_id", "usuarios", "id_usuario",
            delete_esperado="RESTRICT",
            descricao="`tecnicos_chamados.tecnico_id` referencia `usuarios` com ON DELETE RESTRICT",
        )
    )
    info_horas = coluna_info(conexao, BANCO, "tecnicos_chamados", "horas_dedicadas")
    c.append(
        Criterio(
            "`tecnicos_chamados.horas_dedicadas` é DECIMAL",
            info_horas is not None and info_horas.data_type.lower() == "decimal",
            f"Tipo encontrado: `{info_horas.column_type if info_horas else '(coluna não existe)'}` — nunca FLOAT/DOUBLE (Seção 5.2).",
        )
    )
    c.append(
        Criterio(
            "`tecnicos_chamados` tem CHECK envolvendo `horas_dedicadas`",
            check_existe(conexao, BANCO, "tecnicos_chamados", contendo="horas_dedicadas"),
            "Esperado um CHECK garantindo horas_dedicadas >= 0.",
        )
    )

    return c


def avaliar_parte_2(conexao: ConexaoMariaDB) -> list[Criterio]:
    """Parte 2 — ALTER TABLE em `chamados`."""
    c: list[Criterio] = []

    info_sla = coluna_info(conexao, BANCO, "chamados", "sla_horas")
    c.append(
        Criterio(
            "(a) `chamados.sla_horas` foi adicionada como INT UNSIGNED NULL",
            info_sla is not None
            and info_sla.data_type.lower() == "int"
            and "unsigned" in info_sla.column_type.lower()
            and info_sla.is_nullable,
            f"Coluna encontrada: `{info_sla.column_type if info_sla else '(não existe)'}`"
            f"{' NULL' if info_sla and info_sla.is_nullable else ' NOT NULL' if info_sla else ''}.",
        )
    )

    info_titulo = coluna_info(conexao, BANCO, "chamados", "titulo")
    info_assunto = coluna_info(conexao, BANCO, "chamados", "assunto")
    c.append(
        Criterio(
            "(b) Coluna `titulo` foi renomeada para `assunto` (mesmo tipo VARCHAR(255))",
            info_titulo is None
            and info_assunto is not None
            and info_assunto.column_type.lower() == "varchar(255)",
            "`titulo` não deve mais existir; `assunto` deve existir como VARCHAR(255)."
            f" Encontrado: titulo={'existe' if info_titulo else 'não existe'},"
            f" assunto={info_assunto.column_type if info_assunto else 'não existe'}.",
        )
    )

    c.append(
        Criterio(
            "(c) CHECK adicionado envolvendo `sla_horas`",
            check_existe(conexao, BANCO, "chamados", contendo="sla_horas"),
            "Esperado um CHECK garantindo sla_horas IS NULL OR sla_horas > 0, adicionado via ALTER TABLE.",
        )
    )

    return c


# --- helpers ---------------------------------------------------------------

def _checar_tabela(conexao: ConexaoMariaDB, tabela: str) -> Criterio:
    existe = tabela_existe(conexao, BANCO, tabela)
    return Criterio(
        f"Tabela `{tabela}` existe",
        existe,
        f"Tabela `{tabela}` {'encontrada' if existe else 'NÃO encontrada'} em `{BANCO}`.",
    )


def _checar_pk(conexao: ConexaoMariaDB, tabela: str, colunas_esperadas: list[str]) -> Criterio:
    encontradas = colunas_pk(conexao, BANCO, tabela)
    nome_criterio = f"`{tabela}` tem PK ({', '.join(f'`{c}`' for c in colunas_esperadas)}) — Regra 5"
    ok = sorted(c.lower() for c in encontradas) == sorted(c.lower() for c in colunas_esperadas)
    detalhe = f"PK encontrada: {encontradas or '(nenhuma)'}."
    return Criterio(nome_criterio, ok, detalhe)


def _checar_fk(
    conexao: ConexaoMariaDB,
    tabela: str,
    coluna: str,
    tabela_referenciada: str,
    coluna_referenciada: str,
    *,
    delete_esperado: str,
    descricao: str,
) -> Criterio:
    info = fk_info(conexao, BANCO, tabela, coluna)
    if info is None:
        return Criterio(descricao, False, f"Nenhuma FOREIGN KEY encontrada em `{tabela}.{coluna}`.")
    ok = (
        info.referenced_table.lower() == tabela_referenciada.lower()
        and info.referenced_column.lower() == coluna_referenciada.lower()
        and info.delete_rule.upper() == delete_esperado.upper()
    )
    detalhe = (
        f"Encontrado: REFERENCES {info.referenced_table}({info.referenced_column}) "
        f"ON DELETE {info.delete_rule} ON UPDATE {info.update_rule}."
    )
    return Criterio(descricao, ok, detalhe)


def _checar_unique(conexao: ConexaoMariaDB, tabela: str, colunas: list[str], *, descricao: str) -> Criterio:
    ok = unique_existe(conexao, BANCO, tabela, colunas)
    return Criterio(descricao, ok, "UNIQUE " + ("encontrada." if ok else "NÃO encontrada com exatamente essas colunas."))


def _checar_campos_log(conexao: ConexaoMariaDB, tabela: str) -> list[Criterio]:
    """Regra 9 — toda tabela tem criado_em, atualizado_em, deletado_em."""
    resultado = []
    for coluna, nullable_esperado in (
        ("criado_em", False),
        ("atualizado_em", False),
        ("deletado_em", True),
    ):
        info = coluna_info(conexao, BANCO, tabela, coluna)
        nome = f"`{tabela}.{coluna}` presente (Regra 9)"
        if info is None:
            resultado.append(Criterio(nome, False, f"Coluna `{coluna}` não encontrada em `{tabela}`."))
            continue
        ok = info.data_type.lower() == "datetime" and info.is_nullable == nullable_esperado
        resultado.append(
            Criterio(
                nome, ok,
                f"Tipo: {info.column_type}, nullable: {info.is_nullable} "
                f"(esperado: DATETIME, nullable={nullable_esperado}).",
            )
        )
    return resultado


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser()
    parser.add_argument("--entrega", default=str(_AQUI.parents[1] / "sql" / "helpdesk.sql"))
    parser.add_argument("--saida-json", default=str(_AQUI.parents[1] / "resultado.json"))
    parser.add_argument("--host", default=os.environ.get("DB_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("DB_PORT", "3306")))
    parser.add_argument("--user", default=os.environ.get("DB_USER", "root"))
    parser.add_argument("--password", default=os.environ.get("DB_PASSWORD", "root"))
    args = parser.parse_args()

    caminho_entrega = Path(args.entrega)
    if not caminho_entrega.exists():
        print(f"::error::Arquivo de entrega não encontrado: {caminho_entrega}")
        return 1

    conexao = ConexaoMariaDB(host=args.host, port=args.port, user=args.user, password=args.password)

    # Sempre parte de um banco limpo — evita "sucesso" por resíduo de uma
    # execução anterior contra o mesmo servidor.
    conexao.query(f"DROP DATABASE IF EXISTS {BANCO};")

    execucao = conexao.rodar_script(args.entrega)

    if execucao.returncode != 0:
        erro = Criterio(
            "Script executa sem erros no MariaDB",
            False,
            "O script parou com um erro antes de terminar — corrija a sintaxe e tente de novo. "
            f"Mensagem do MariaDB:\n```\n{execucao.stderr.strip()}\n```",
        )
        relatorio_erro = montar_relatorio([erro])
        resultado_json = {
            "parte_1": relatorio_erro,
            "parte_2": montar_relatorio([erro]),
            "geral": relatorio_erro,
        }
        md = [
            "# Resultado da correção automática — Aula 03",
            "",
            relatorio_para_markdown("Execução do script", relatorio_erro),
        ]
        saida_md = "\n".join(md)
        print(saida_md)
        Path(args.saida_json).write_text(json.dumps(resultado_json, ensure_ascii=False, indent=2), encoding="utf-8")
        step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if step_summary:
            with open(step_summary, "a", encoding="utf-8") as f:
                f.write(saida_md + "\n")
        return 0

    criterios_p1 = avaliar_parte_1(conexao)
    criterios_p2 = avaliar_parte_2(conexao)

    relatorio_p1 = montar_relatorio(criterios_p1)
    relatorio_p2 = montar_relatorio(criterios_p2)
    relatorio_geral = montar_relatorio(criterios_p1 + criterios_p2)

    md = [
        "# Resultado da correção automática — Aula 03",
        "",
        "> Atividade **formativa** (não compõe T1/P1/T2/P2 — ver "
        "`docs/estrategia-de-avaliacao.md`). A correção roda seu script de "
        "verdade contra um MariaDB descartável e confere a estrutura "
        "resultante — não o texto do seu SQL.",
        "",
        relatorio_para_markdown("Parte 1 — CREATE DATABASE e CREATE TABLE", relatorio_p1),
        "",
        relatorio_para_markdown("Parte 2 — ALTER TABLE", relatorio_p2),
        "",
        f"## Nota geral: {relatorio_geral['nota']} / 10 "
        f"({relatorio_geral['aprovados']}/{relatorio_geral['total_criterios']} critérios)",
    ]

    saida_md = "\n".join(md)
    print(saida_md)

    resultado_json = {
        "parte_1": relatorio_p1,
        "parte_2": relatorio_p2,
        "geral": relatorio_geral,
    }
    Path(args.saida_json).write_text(json.dumps(resultado_json, ensure_ascii=False, indent=2), encoding="utf-8")

    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(saida_md + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
