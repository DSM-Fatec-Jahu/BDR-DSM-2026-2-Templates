#!/usr/bin/env python3
"""Autograding da Aula 01 — Modelagem Conceitual (MER).

Valida a estrutura do arquivo `sql/modelo-conceitual.md` entregue pelo aluno:
não roda nenhum banco de dados (a aula é 100% conceitual, anterior ao SQL),
só confere a existência/nomenclatura/cardinalidade de entidades e
relacionamentos no(s) bloco(s) ```mermaid erDiagram```.

Uso:
    python regras_avaliacao.py [--entrega CAMINHO] [--saida-json CAMINHO]

Import de `shared/utilitarios/mer_mermaid.py`: este script espera que a raiz
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

from utilitarios.mer_mermaid import (  # noqa: E402
    Criterio,
    checar_atributo_existe,
    checar_atributos_extras,
    checar_entidade,
    checar_fk,
    checar_participacao,
    checar_pk,
    checar_relacionamento,
    montar_relatorio,
    parse_mermaid_er,
    relatorio_para_markdown,
)

SUBCLASSES_PARTE_2 = ["ALUNOS", "PROFESSORES", "FUNCIONARIOS_ADMINISTRATIVOS"]


def _extrair_campo(texto: str, rotulo: str) -> str:
    m = re.search(rf"\*\*{re.escape(rotulo)}:\*\*\s*(.*)", texto)
    if not m:
        return ""
    valor = m.group(1)
    valor = re.sub(r"<!--.*?-->", "", valor, flags=re.DOTALL)
    return valor.strip()


def avaliar_parte_1(diagrama) -> list[Criterio]:
    c: list[Criterio] = []
    c.append(checar_entidade(diagrama, "PACIENTES"))
    c.append(checar_pk(diagrama, "PACIENTES", "id_paciente"))
    c.append(checar_entidade(diagrama, "MEDICOS"))
    c.append(checar_pk(diagrama, "MEDICOS", "id_medico"))
    c.append(checar_entidade(diagrama, "ESPECIALIDADES"))
    c.append(
        checar_relacionamento(
            diagrama, "MEDICOS", "ESPECIALIDADES", "N:M",
            descricao="Médico × Especialidade é N:M (um médico pode ter várias especialidades)",
        )
    )
    c.append(checar_entidade(diagrama, "CONSULTAS"))
    c.append(checar_fk(diagrama, "CONSULTAS", "paciente_id"))
    c.append(checar_fk(diagrama, "CONSULTAS", "medico_id"))
    c.append(
        checar_relacionamento(
            diagrama, "PACIENTES", "CONSULTAS", "1:N",
            descricao="Paciente × Consulta é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "MEDICOS", "CONSULTAS", "1:N",
            descricao="Médico × Consulta é 1:N",
        )
    )
    c.append(checar_entidade(diagrama, "PRONTUARIOS"))
    c.append(
        checar_relacionamento(
            diagrama, "CONSULTAS", "PRONTUARIOS", "1:1",
            descricao="Consulta × Prontuário é 1:1 (cada consulta gera um prontuário)",
        )
    )
    return c


def avaliar_parte_2(diagrama, texto_completo: str) -> list[Criterio]:
    c: list[Criterio] = []
    c.append(checar_entidade(diagrama, "PESSOAS", descricao="Superclasse `PESSOAS` presente"))
    c.append(checar_pk(diagrama, "PESSOAS", "id_pessoa"))

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
                diagrama, "PESSOAS", sub, "1:1",
                descricao=f"`PESSOAS`–`{sub}` é 1:1 (Estratégia 2, Seção 8.7)",
            )
        )
        c.append(
            checar_participacao(
                diagrama, "PESSOAS", sub, sub, "parcial",
                descricao=f"`{sub}` participa de forma parcial em `PESSOAS`–`{sub}` (nem toda pessoa é dessa subclasse)",
            )
        )

    obrigatoriedade = _extrair_campo(texto_completo, "Obrigatoriedade")
    exclusividade = _extrair_campo(texto_completo, "Exclusividade")
    justificativa = _extrair_campo(texto_completo, "Justificativa")

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--entrega", default=str(_AQUI.parents[1] / "sql" / "modelo-conceitual.md"))
    parser.add_argument("--saida-json", default=str(_AQUI.parents[1] / "resultado.json"))
    args = parser.parse_args()

    caminho_entrega = Path(args.entrega)
    if not caminho_entrega.exists():
        print(f"::error::Arquivo de entrega não encontrado: {caminho_entrega}")
        return 1

    texto = caminho_entrega.read_text(encoding="utf-8")
    diagrama = parse_mermaid_er(texto)

    criterios_p1 = avaliar_parte_1(diagrama)
    criterios_p2 = avaliar_parte_2(diagrama, texto)

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
    if diagrama.erros:
        md.append("")
        md.append("### ⚠️ Linhas não reconhecidas pelo parser")
        md.append(
            "Essas linhas dentro de um bloco `erDiagram` não bateram com a "
            "sintaxe esperada (atributo `TIPO nome [PK][, FK]` ou "
            "relacionamento `A ||--o{ B : \"rotulo\"`). Se for um erro de "
            "sintaxe do seu diagrama, corrija-o:"
        )
        for e in diagrama.erros:
            md.append(f"- {e}")

    saida_md = "\n".join(md)
    print(saida_md)

    resultado_json = {
        "parte_1": relatorio_p1,
        "parte_2": relatorio_p2,
        "geral": relatorio_geral,
        "erros_parser": diagrama.erros,
    }
    Path(args.saida_json).write_text(json.dumps(resultado_json, ensure_ascii=False, indent=2), encoding="utf-8")

    step_summary = __import__("os").environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(saida_md + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
