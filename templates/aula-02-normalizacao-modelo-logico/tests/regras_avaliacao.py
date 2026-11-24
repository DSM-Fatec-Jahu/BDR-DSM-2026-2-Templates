#!/usr/bin/env python3
"""Autograding da Aula 02 — Normalização e Modelo Lógico.

Valida a estrutura de dois arquivos `.dbml` entregues pelo aluno (Parte 1 e
Parte 2) e os campos de texto em `sql/modelo-logico.md`: não roda nenhum
banco de dados (a aula ainda é anterior a SQL de verdade, que só começa na
Aula 03), só confere a existência/nomenclatura/cardinalidade de tabelas e
relacionamentos nos arquivos `.dbml`, e o preenchimento mínimo das duas
análises escritas (mapeamento de dependências funcionais da Parte 1,
justificativa da FK 1:1 da Parte 2).

Uso:
    python regras_avaliacao.py [--entrega CAMINHO] [--saida-json CAMINHO]

`--entrega` aponta para o arquivo `.md`; os dois arquivos `.dbml` são
derivados automaticamente do mesmo nome-base (`<nome>-parte1.dbml` /
`<nome>-parte2.dbml`, na mesma pasta) — ver comentário equivalente em
`tests/regras_avaliacao.py` da Aula 01.

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
    checar_entidade,
    checar_fk,
    checar_participacao_fk,
    checar_pk,
    checar_relacionamento,
    montar_relatorio,
    parse_dbml_er,
    relatorio_para_markdown,
)


def _extrair_secao(texto: str, inicio: str, fim: str | None) -> str:
    """Extrai o texto entre dois cabeçalhos `##`, removendo comentários HTML
    e cercas de bloco de código, para medir se o aluno escreveu algo."""
    padrao = re.escape(inicio) + r"(.*?)" + (re.escape(fim) if fim else r"\Z")
    m = re.search(padrao, texto, flags=re.DOTALL)
    if not m:
        return ""
    trecho = m.group(1)
    trecho = re.sub(r"<!--.*?-->", "", trecho, flags=re.DOTALL)
    trecho = re.sub(r"```[a-z]*\n?", "", trecho)
    trecho = re.sub(r"^>.*$", "", trecho, flags=re.MULTILINE)  # citações de instrução
    return trecho.strip()


def _extrair_campo(texto: str, rotulo: str) -> str:
    m = re.search(rf"\*\*{re.escape(rotulo)}:\*\*\s*(.*)", texto)
    if not m:
        return ""
    valor = m.group(1)
    valor = re.sub(r"<!--.*?-->", "", valor, flags=re.DOTALL)
    return valor.strip()


def avaliar_parte_1(diagrama, texto_md: str) -> list[Criterio]:
    c: list[Criterio] = []

    mapeamento = _extrair_secao(
        texto_md,
        "## Parte 1 — a) Mapeamento de dependências funcionais",
        "## Parte 2",
    )
    c.append(
        Criterio(
            "Mapeamento de dependências funcionais preenchido (mín. 80 caracteres)",
            len(mapeamento) >= 80,
            f"Texto encontrado tem {len(mapeamento)} caractere(s) — a correção "
            "do CONTEÚDO do mapeamento é feita manualmente pelo professor; "
            "esta checagem só confere se você de fato escreveu uma análise.",
        )
    )

    c.append(checar_entidade(diagrama, "clientes"))
    c.append(checar_pk(diagrama, "clientes", "id_cliente"))

    c.append(checar_entidade(diagrama, "veiculos"))
    c.append(checar_pk(diagrama, "veiculos", "id_veiculo"))
    c.append(checar_fk(diagrama, "veiculos", "cliente_id"))
    c.append(
        checar_relacionamento(
            diagrama, "clientes", "veiculos", "1:N",
            descricao="Cliente × Veículo é 1:N",
        )
    )

    c.append(checar_entidade(diagrama, "mecanicos"))
    c.append(checar_pk(diagrama, "mecanicos", "id_mecanico"))

    c.append(checar_entidade(diagrama, "servicos"))
    c.append(checar_pk(diagrama, "servicos", "id_servico"))

    c.append(checar_entidade(diagrama, "ordens_servico"))
    c.append(checar_pk(diagrama, "ordens_servico", "id_ordem"))
    c.append(checar_fk(diagrama, "ordens_servico", "veiculo_id"))
    c.append(checar_fk(diagrama, "ordens_servico", "mecanico_id"))
    c.append(
        checar_relacionamento(
            diagrama, "veiculos", "ordens_servico", "1:N",
            descricao="Veículo × Ordem de Serviço é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "mecanicos", "ordens_servico", "1:N",
            descricao="Mecânico × Ordem de Serviço é 1:N",
        )
    )

    c.append(checar_entidade(diagrama, "itens_ordem_servico"))
    c.append(checar_pk(diagrama, "itens_ordem_servico", "ordem_id"))
    c.append(checar_pk(diagrama, "itens_ordem_servico", "servico_id"))
    c.append(checar_fk(diagrama, "itens_ordem_servico", "ordem_id"))
    c.append(checar_fk(diagrama, "itens_ordem_servico", "servico_id"))
    c.append(checar_atributo_existe(diagrama, "itens_ordem_servico", "quantidade"))
    c.append(
        checar_relacionamento(
            diagrama, "ordens_servico", "itens_ordem_servico", "1:N",
            descricao="Ordem de Serviço × Item é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "servicos", "itens_ordem_servico", "1:N",
            descricao="Serviço × Item é 1:N",
        )
    )
    return c


def avaliar_parte_2(diagrama, texto_md: str) -> list[Criterio]:
    c: list[Criterio] = []

    c.append(checar_entidade(diagrama, "hospedes"))
    c.append(checar_pk(diagrama, "hospedes", "id_hospede"))

    c.append(checar_entidade(diagrama, "reservas"))
    c.append(checar_pk(diagrama, "reservas", "id_reserva"))
    c.append(checar_fk(diagrama, "reservas", "hospede_id"))
    c.append(
        checar_relacionamento(
            diagrama, "hospedes", "reservas", "1:N",
            descricao="Hóspede × Reserva é 1:N",
        )
    )
    c.append(
        checar_participacao_fk(
            diagrama, "reservas", "hospede_id", "total",
            descricao="Participação de `reservas` é total (toda reserva pertence a um hóspede)",
        )
    )

    c.append(checar_entidade(diagrama, "quartos"))
    c.append(checar_pk(diagrama, "quartos", "id_quarto"))

    c.append(checar_entidade(diagrama, "reservas_quartos"))
    c.append(checar_pk(diagrama, "reservas_quartos", "reserva_id"))
    c.append(checar_pk(diagrama, "reservas_quartos", "quarto_id"))
    c.append(checar_fk(diagrama, "reservas_quartos", "reserva_id"))
    c.append(checar_fk(diagrama, "reservas_quartos", "quarto_id"))
    c.append(
        checar_atributo_existe(
            diagrama, "reservas_quartos", "valor_diaria_negociado",
            descricao="`reservas_quartos` tem o atributo do relacionamento `valor_diaria_negociado`",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "reservas", "reservas_quartos", "1:N",
            descricao="Reserva × Reservas_Quartos é 1:N (resolve o N:M Reserva×Quarto)",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "quartos", "reservas_quartos", "1:N",
            descricao="Quarto × Reservas_Quartos é 1:N (resolve o N:M Reserva×Quarto)",
        )
    )

    c.append(checar_entidade(diagrama, "cartoes_fidelidade"))
    c.append(checar_fk(diagrama, "cartoes_fidelidade", "hospede_id"))
    c.append(
        checar_relacionamento(
            diagrama, "hospedes", "cartoes_fidelidade", "1:1",
            descricao="Hóspede × Cartão Fidelidade é 1:1",
        )
    )
    c.append(
        checar_participacao_fk(
            diagrama, "cartoes_fidelidade", "hospede_id", "total",
            descricao="Participação de `cartoes_fidelidade` é total (todo cartão pertence a um hóspede)",
        )
    )
    # A participação de HOSPEDES nessa relação (nem todo hóspede tem cartão)
    # é do lado referenciado ("um") — não representável em DBML (ver
    # docstring de mer_dbml.py). Só é conferida na Justificativa escrita.

    c.append(checar_entidade(diagrama, "diarias"))
    c.append(checar_pk(diagrama, "diarias", "reserva_id"))
    c.append(checar_pk(diagrama, "diarias", "numero_diaria"))
    c.append(checar_fk(diagrama, "diarias", "reserva_id"))
    c.append(
        checar_relacionamento(
            diagrama, "reservas", "diarias", "1:N",
            descricao="Reserva × Diária é 1:N (entidade fraca)",
        )
    )

    justificativa = _extrair_campo(texto_md, "Justificativa")
    c.append(
        Criterio(
            "Justificativa da FK do relacionamento 1:1 tem no mínimo 30 caracteres",
            len(justificativa) >= 30,
            f"Justificativa tem {len(justificativa)} caractere(s) — a adequação "
            "do argumento (Critério 1/2 da Seção 8.1, incluindo qual lado tem "
            "participação parcial) é avaliada pelo professor, esta checagem só "
            "confere se você de fato argumentou.",
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
    parser.add_argument("--entrega", default=str(base / "modelo-logico.md"))
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
        "Entrega (.md)": entrega_md,
    }
    for rotulo, caminho in caminhos.items():
        if not caminho.exists():
            print(f"::error::Arquivo de entrega não encontrado ({rotulo}): {caminho}")
            return 1

    diagrama_1 = parse_dbml_er(entrega_parte1.read_text(encoding="utf-8"))
    diagrama_2 = parse_dbml_er(entrega_parte2.read_text(encoding="utf-8"))
    texto_md = entrega_md.read_text(encoding="utf-8")

    criterios_p1 = avaliar_parte_1(diagrama_1, texto_md)
    criterios_p2 = avaliar_parte_2(diagrama_2, texto_md)

    relatorio_p1 = montar_relatorio(criterios_p1)
    relatorio_p2 = montar_relatorio(criterios_p2)
    relatorio_geral = montar_relatorio(criterios_p1 + criterios_p2)

    md = [
        "# Resultado da correção automática — Aula 02",
        "",
        "> Atividade **formativa** (não compõe T1/P1/T2/P2 — ver "
        "`docs/estrategia-de-avaliacao.md`). Este relatório é feedback para "
        "você revisar seu modelo antes da aula seguinte.",
        "",
        relatorio_para_markdown("Parte 1 — Normalização (Oficina Mecânica)", relatorio_p1),
        "",
        relatorio_para_markdown("Parte 2 — Modelo Lógico (Rede de Hotéis)", relatorio_p2),
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
