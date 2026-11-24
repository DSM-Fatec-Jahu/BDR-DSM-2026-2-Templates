#!/usr/bin/env python3
"""Autograding da Aula 01 — Modelagem Conceitual (MER).

Valida a estrutura de dois arquivos `.dbml` entregues pelo aluno (Parte 1 e
Parte 2) e o campo de texto em `sql/modelo-conceitual.md` (Parte 2): não
roda nenhum banco de dados (a aula é 100% conceitual, anterior ao SQL), só
confere a existência/nomenclatura/cardinalidade de tabelas e relacionamentos
nos arquivos `.dbml`.

Uso:
    python regras_avaliacao.py [--entrega CAMINHO] [--saida-json CAMINHO]

`--entrega` aponta para o arquivo `.md` (só o campo de texto da Parte 2); os
dois arquivos `.dbml` são derivados automaticamente do mesmo nome-base
(`<nome>-parte1.dbml` / `<nome>-parte2.dbml`, na mesma pasta) — é assim que
`sql/modelo-conceitual.md` vira `sql/modelo-conceitual-parte1.dbml` etc.
Isso mantém a interface de linha de comando compatível com
`.github/workflows/autograding-aula-01.yml`, que só conhece um único
caminho de entrega. Use `--entrega-parte1`/`--entrega-parte2` para
sobrescrever a derivação automática, se precisar.

Import de `shared/utilitarios/mer_dbml.py`: este script espera que a raiz
do repositório esteja em `PYTHONPATH` como `shared` (é isso que o workflow
`.github/workflows/_autograding-reusable.yml` configura). Rodando localmente
de dentro da pasta do template, ajuste o `sys.path` manualmente se necessário
(ver comentário abaixo).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_AQUI = Path(__file__).resolve()
# tests/regras_avaliacao.py -> tests/ -> <template>/ -> templates/ -> <raiz do repo>/shared
_SHARED = _AQUI.parents[3] / "shared"
if _SHARED.exists() and str(_SHARED) not in sys.path:
    sys.path.insert(0, str(_SHARED))

from utilitarios.mer_dbml import (  # noqa: E402
    Criterio,
    checar_atributo_existe,
    checar_atributos_extras,
    checar_entidade,
    checar_fk,
    checar_pk,
    checar_relacionamento,
    montar_relatorio,
    parse_dbml_er,
    relatorio_para_markdown,
)

SUBCLASSES_PARTE_2 = ["alunos", "professores", "funcionarios_administrativos"]


def _extrair_campo(texto: str, rotulo: str) -> str:
    m = re.search(rf"\*\*{re.escape(rotulo)}:\*\*\s*(.*)", texto)
    if not m:
        return ""
    valor = m.group(1)
    valor = re.sub(r"<!--.*?-->", "", valor, flags=re.DOTALL)
    return valor.strip()


def avaliar_parte_1(diagrama) -> list[Criterio]:
    c: list[Criterio] = []
    c.append(checar_entidade(diagrama, "pacientes"))
    c.append(checar_pk(diagrama, "pacientes", "id_paciente"))
    c.append(checar_entidade(diagrama, "medicos"))
    c.append(checar_pk(diagrama, "medicos", "id_medico"))
    c.append(checar_entidade(diagrama, "especialidades"))
    c.append(
        checar_relacionamento(
            diagrama, "medicos", "especialidades", "N:M",
            descricao="Médico × Especialidade é N:M (um médico pode ter várias especialidades)",
        )
    )
    c.append(checar_entidade(diagrama, "consultas"))
    c.append(checar_fk(diagrama, "consultas", "paciente_id"))
    c.append(checar_fk(diagrama, "consultas", "medico_id"))
    c.append(
        checar_relacionamento(
            diagrama, "pacientes", "consultas", "1:N",
            descricao="Paciente × Consulta é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "medicos", "consultas", "1:N",
            descricao="Médico × Consulta é 1:N",
        )
    )
    c.append(checar_entidade(diagrama, "prontuarios"))
    c.append(
        checar_relacionamento(
            diagrama, "consultas", "prontuarios", "1:1",
            descricao="Consulta × Prontuário é 1:1 (cada consulta gera um prontuário)",
        )
    )
    return c


def avaliar_parte_2(diagrama, texto_md: str) -> list[Criterio]:
    c: list[Criterio] = []
    c.append(checar_entidade(diagrama, "pessoas", descricao="Superclasse `pessoas` presente"))
    c.append(checar_pk(diagrama, "pessoas", "id_pessoa"))

    for sub in SUBCLASSES_PARTE_2:
        c.append(checar_entidade(diagrama, sub))
        c.append(checar_pk(diagrama, sub, "id_pessoa"))
        c.append(checar_fk(diagrama, sub, "id_pessoa"))
        c.append(
            checar_atributos_extras(
                diagrama, sub, 1,
                descricao=f"`{sub}` tem ao menos 1 atributo exclusivo além da chave herdada",
            )
        )
        c.append(
            checar_relacionamento(
                diagrama, "pessoas", sub, "1:1",
                descricao=f"`pessoas`–`{sub}` é 1:1 (Estratégia 2, Seção 8.7)",
            )
        )

    # A participação da SUPERCLASSE nessa relação (nem toda pessoa é dessa
    # subclasse) não é algo que um Ref de DBML consiga expressar — não existe
    # constraint de schema para "nem toda linha do lado 'um' tem uma linha
    # correspondente do lado 'muitos'" (ver docstring de mer_dbml.py). Por
    # isso essa decisão só é avaliada pelos campos de texto abaixo.
    obrigatoriedade = _extrair_campo(texto_md, "Obrigatoriedade")
    exclusividade = _extrair_campo(texto_md, "Exclusividade")
    justificativa = _extrair_campo(texto_md, "Justificativa")

    c.append(
        Criterio(
            "Campo Obrigatoriedade preenchido (Total ou Parcial)",
            bool(re.search(r"\btotal\b|\bparcial\b", obrigatoriedade, re.IGNORECASE)),
            f"Valor encontrado: '{obrigatoriedade}'." if obrigatoriedade else "Campo vazio.",
        )
    )
    c.append(
        Criterio(
            "Campo Exclusividade preenchido (Exclusiva ou Sobreposta)",
            bool(re.search(r"\bexclusiva\b|\bsobreposta\b", exclusividade, re.IGNORECASE)),
            f"Valor encontrado: '{exclusividade}'." if exclusividade else "Campo vazio.",
        )
    )
    c.append(
        Criterio(
            "Justificativa da restrição tem no mínimo 30 caracteres",
            len(justificativa) >= 30,
            f"Justificativa tem {len(justificativa)} caractere(s) — "
            "a adequação da escolha ao enunciado é avaliada pelo professor, "
            "esta checagem só confere se você de fato argumentou.",
        )
    )
    return c


def main() -> int:
    # Windows abre stdout em cp1252 por padrão, que não tem ✅/❌/⚠️ — força UTF-8
    # (irrelevante no runner do GitHub Actions, que já roda em UTF-8).
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    base = _AQUI.parents[1] / "sql"
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrega", default=str(base / "modelo-conceitual.md"))
    parser.add_argument("--entrega-parte1", default=None, help="sobrescreve a derivação automática a partir de --entrega")
    parser.add_argument("--entrega-parte2", default=None, help="sobrescreve a derivação automática a partir de --entrega")
    parser.add_argument("--saida-json", default=str(_AQUI.parents[1] / "resultado.json"))
    args = parser.parse_args()

    entrega_md = Path(args.entrega)
    entrega_parte1 = Path(args.entrega_parte1) if args.entrega_parte1 else entrega_md.with_name(f"{entrega_md.stem}-parte1.dbml")
    entrega_parte2 = Path(args.entrega_parte2) if args.entrega_parte2 else entrega_md.with_name(f"{entrega_md.stem}-parte2.dbml")

    caminhos = {
        "Parte 1 (.dbml)": entrega_parte1,
        "Parte 2 (.dbml)": entrega_parte2,
        "Restrição da hierarquia (.md)": entrega_md,
    }
    for rotulo, caminho in caminhos.items():
        if not caminho.exists():
            print(f"::error::Arquivo de entrega não encontrado ({rotulo}): {caminho}")
            return 1

    diagrama_1 = parse_dbml_er(caminhos["Parte 1 (.dbml)"].read_text(encoding="utf-8"))
    diagrama_2 = parse_dbml_er(caminhos["Parte 2 (.dbml)"].read_text(encoding="utf-8"))
    texto_md = caminhos["Restrição da hierarquia (.md)"].read_text(encoding="utf-8")

    criterios_p1 = avaliar_parte_1(diagrama_1)
    criterios_p2 = avaliar_parte_2(diagrama_2, texto_md)

    relatorio_p1 = montar_relatorio(criterios_p1)
    relatorio_p2 = montar_relatorio(criterios_p2)
    relatorio_geral = montar_relatorio(criterios_p1 + criterios_p2)

    md = [
        "# Resultado da correção automática — Aula 01",
        "",
        "> Atividade **formativa** (não compõe T1/P1/T2/P2 — ver "
        "`docs/estrategia-de-avaliacao.md`). Este relatório é feedback para "
        "você revisar seu modelo antes da aula seguinte.",
        "",
        relatorio_para_markdown("Parte 1 — Clínica Médica", relatorio_p1),
        "",
        relatorio_para_markdown("Parte 2 — Generalização de Pessoas", relatorio_p2),
        "",
        f"## Nota geral: {relatorio_geral['nota']} / 10 "
        f"({relatorio_geral['aprovados']}/{relatorio_geral['total_criterios']} critérios)",
    ]
    erros = diagrama_1.erros + diagrama_2.erros
    if erros:
        md.append("")
        md.append("### ⚠️ Linhas não reconhecidas pelo parser")
        md.append(
            "Essas linhas dentro de um `Table { ... }` não bateram com a "
            "sintaxe esperada (`tipo nome [pk][, not null]`). Se for um erro "
            "de sintaxe do seu `.dbml`, corrija-o:"
        )
        for e in erros:
            md.append(f"- {e}")

    saida_md = "\n".join(md)
    print(saida_md)

    resultado_json = {
        "parte_1": relatorio_p1,
        "parte_2": relatorio_p2,
        "geral": relatorio_geral,
        "erros_parser": erros,
    }
    Path(args.saida_json).write_text(json.dumps(resultado_json, ensure_ascii=False, indent=2), encoding="utf-8")

    step_summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(saida_md + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
