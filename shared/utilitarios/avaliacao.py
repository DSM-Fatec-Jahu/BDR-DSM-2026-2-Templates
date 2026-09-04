"""Estruturas genéricas de relatório de correção automática.

Extraído de `mer_mermaid.py` ao processar a Aula 03 (primeiro alvo com um
segundo tipo de autograder — introspecção de banco real via
`mariadb_ddl.py` — que precisava exatamente do mesmo formato de relatório,
sem nenhum acoplamento ao parser de Mermaid). Qualquer autograder futuro
(`tests/regras_avaliacao.py` de um novo template) pode montar sua lista de
`Criterio` do jeito que fizer sentido para aquele alvo e reaproveitar
`montar_relatorio`/`relatorio_para_markdown` para chegar no mesmo formato de
JSON/Markdown que `.github/workflows/_autograding-reusable.yml` espera.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Criterio:
    nome: str
    passou: bool
    detalhe: str
    peso: float = 1.0


def montar_relatorio(criterios: list[Criterio]) -> dict:
    """Agrega uma lista de Criterio em um dict pronto para virar JSON e Markdown."""
    total_peso = sum(c.peso for c in criterios) or 1.0
    peso_obtido = sum(c.peso for c in criterios if c.passou)
    nota_10 = round((peso_obtido / total_peso) * 10, 2)
    return {
        "nota": nota_10,
        "aprovados": sum(1 for c in criterios if c.passou),
        "total_criterios": len(criterios),
        "criterios": [
            {"nome": c.nome, "passou": c.passou, "detalhe": c.detalhe, "peso": c.peso}
            for c in criterios
        ],
    }


def relatorio_para_markdown(titulo: str, relatorio: dict) -> str:
    linhas = [f"## {titulo}", "", f"**Nota (referência formativa):** {relatorio['nota']} / 10 "
              f"({relatorio['aprovados']}/{relatorio['total_criterios']} critérios atendidos)", ""]
    for c in relatorio["criterios"]:
        marca = "✅" if c["passou"] else "❌"
        linhas.append(f"- {marca} **{c['nome']}** — {c['detalhe']}")
    return "\n".join(linhas)
