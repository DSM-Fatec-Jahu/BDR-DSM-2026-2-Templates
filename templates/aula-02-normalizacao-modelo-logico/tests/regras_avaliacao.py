#!/usr/bin/env python3
"""Autograding da Aula 02 — Normalização e Modelo Lógico.

Valida a estrutura do arquivo `sql/modelo-logico.md` entregue pelo aluno:
não roda nenhum banco de dados (a aula ainda é anterior a SQL de verdade,
que só começa na Aula 03), só confere a existência/nomenclatura/cardinalidade
de tabelas e relacionamentos no(s) bloco(s) ```mermaid erDiagram```, e o
preenchimento mínimo das duas análises escritas (mapeamento de dependências
funcionais da Parte 1, justificativa da FK 1:1 da Parte 2).

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
    checar_entidade,
    checar_fk,
    checar_participacao,
    checar_pk,
    checar_relacionamento,
    montar_relatorio,
    parse_mermaid_er,
    relatorio_para_markdown,
)


def _extrair_secao(texto: str, inicio: str, fim: str | None) -> str:
    """Extrai o texto entre dois cabeçalhos `###`, removendo comentários HTML
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


def avaliar_parte_1(diagrama, texto_completo: str) -> list[Criterio]:
    c: list[Criterio] = []

    mapeamento = _extrair_secao(
        texto_completo,
        "### a) Mapeamento de dependências funcionais",
        "### b) Modelo lógico final (3FN)",
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

    c.append(checar_entidade(diagrama, "CLIENTES"))
    c.append(checar_pk(diagrama, "CLIENTES", "id_cliente"))

    c.append(checar_entidade(diagrama, "VEICULOS"))
    c.append(checar_pk(diagrama, "VEICULOS", "id_veiculo"))
    c.append(checar_fk(diagrama, "VEICULOS", "cliente_id"))
    c.append(
        checar_relacionamento(
            diagrama, "CLIENTES", "VEICULOS", "1:N",
            descricao="Cliente × Veículo é 1:N",
        )
    )

    c.append(checar_entidade(diagrama, "MECANICOS"))
    c.append(checar_pk(diagrama, "MECANICOS", "id_mecanico"))

    c.append(checar_entidade(diagrama, "SERVICOS"))
    c.append(checar_pk(diagrama, "SERVICOS", "id_servico"))

    c.append(checar_entidade(diagrama, "ORDENS_SERVICO"))
    c.append(checar_pk(diagrama, "ORDENS_SERVICO", "id_ordem"))
    c.append(checar_fk(diagrama, "ORDENS_SERVICO", "veiculo_id"))
    c.append(checar_fk(diagrama, "ORDENS_SERVICO", "mecanico_id"))
    c.append(
        checar_relacionamento(
            diagrama, "VEICULOS", "ORDENS_SERVICO", "1:N",
            descricao="Veículo × Ordem de Serviço é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "MECANICOS", "ORDENS_SERVICO", "1:N",
            descricao="Mecânico × Ordem de Serviço é 1:N",
        )
    )

    c.append(checar_entidade(diagrama, "ITENS_ORDEM_SERVICO"))
    c.append(checar_pk(diagrama, "ITENS_ORDEM_SERVICO", "ordem_id"))
    c.append(checar_pk(diagrama, "ITENS_ORDEM_SERVICO", "servico_id"))
    c.append(checar_fk(diagrama, "ITENS_ORDEM_SERVICO", "ordem_id"))
    c.append(checar_fk(diagrama, "ITENS_ORDEM_SERVICO", "servico_id"))
    c.append(checar_atributo_existe(diagrama, "ITENS_ORDEM_SERVICO", "quantidade"))
    c.append(
        checar_relacionamento(
            diagrama, "ORDENS_SERVICO", "ITENS_ORDEM_SERVICO", "1:N",
            descricao="Ordem de Serviço × Item é 1:N",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "SERVICOS", "ITENS_ORDEM_SERVICO", "1:N",
            descricao="Serviço × Item é 1:N",
        )
    )
    return c


def avaliar_parte_2(diagrama, texto_completo: str) -> list[Criterio]:
    c: list[Criterio] = []

    c.append(checar_entidade(diagrama, "HOSPEDES"))
    c.append(checar_pk(diagrama, "HOSPEDES", "id_hospede"))

    c.append(checar_entidade(diagrama, "RESERVAS"))
    c.append(checar_pk(diagrama, "RESERVAS", "id_reserva"))
    c.append(checar_fk(diagrama, "RESERVAS", "hospede_id"))
    c.append(
        checar_relacionamento(
            diagrama, "HOSPEDES", "RESERVAS", "1:N",
            descricao="Hóspede × Reserva é 1:N",
        )
    )
    c.append(
        checar_participacao(
            diagrama, "HOSPEDES", "RESERVAS", "RESERVAS", "total",
            descricao="Participação de `RESERVAS` é total (toda reserva pertence a um hóspede)",
        )
    )

    c.append(checar_entidade(diagrama, "QUARTOS"))
    c.append(checar_pk(diagrama, "QUARTOS", "id_quarto"))

    c.append(checar_entidade(diagrama, "RESERVAS_QUARTOS"))
    c.append(checar_pk(diagrama, "RESERVAS_QUARTOS", "reserva_id"))
    c.append(checar_pk(diagrama, "RESERVAS_QUARTOS", "quarto_id"))
    c.append(checar_fk(diagrama, "RESERVAS_QUARTOS", "reserva_id"))
    c.append(checar_fk(diagrama, "RESERVAS_QUARTOS", "quarto_id"))
    c.append(
        checar_atributo_existe(
            diagrama, "RESERVAS_QUARTOS", "valor_diaria_negociado",
            descricao="`RESERVAS_QUARTOS` tem o atributo do relacionamento `valor_diaria_negociado`",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "RESERVAS", "RESERVAS_QUARTOS", "1:N",
            descricao="Reserva × Reservas_Quartos é 1:N (resolve o N:M Reserva×Quarto)",
        )
    )
    c.append(
        checar_relacionamento(
            diagrama, "QUARTOS", "RESERVAS_QUARTOS", "1:N",
            descricao="Quarto × Reservas_Quartos é 1:N (resolve o N:M Reserva×Quarto)",
        )
    )

    c.append(checar_entidade(diagrama, "CARTOES_FIDELIDADE"))
    c.append(checar_fk(diagrama, "CARTOES_FIDELIDADE", "hospede_id"))
    c.append(
        checar_relacionamento(
            diagrama, "HOSPEDES", "CARTOES_FIDELIDADE", "1:1",
            descricao="Hóspede × Cartão Fidelidade é 1:1",
        )
    )
    c.append(
        checar_participacao(
            diagrama, "HOSPEDES", "CARTOES_FIDELIDADE", "HOSPEDES", "parcial",
            descricao="Participação de `HOSPEDES` é parcial (nem todo hóspede tem cartão)",
        )
    )
    c.append(
        checar_participacao(
            diagrama, "HOSPEDES", "CARTOES_FIDELIDADE", "CARTOES_FIDELIDADE", "total",
            descricao="Participação de `CARTOES_FIDELIDADE` é total (todo cartão pertence a um hóspede)",
        )
    )

    c.append(checar_entidade(diagrama, "DIARIAS"))
    c.append(checar_pk(diagrama, "DIARIAS", "reserva_id"))
    c.append(checar_pk(diagrama, "DIARIAS", "numero_diaria"))
    c.append(checar_fk(diagrama, "DIARIAS", "reserva_id"))
    c.append(
        checar_relacionamento(
            diagrama, "RESERVAS", "DIARIAS", "1:N",
            descricao="Reserva × Diária é 1:N (entidade fraca)",
        )
    )

    justificativa = _extrair_campo(texto_completo, "Justificativa")
    c.append(
        Criterio(
            "Justificativa da FK do relacionamento 1:1 tem no mínimo 30 caracteres",
            len(justificativa) >= 30,
            f"Justificativa tem {len(justificativa)} caractere(s) — a adequação "
            "do argumento (Critério 1/2 da Seção 8.1) é avaliada pelo professor, "
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
    parser.add_argument("--entrega", default=str(_AQUI.parents[1] / "sql" / "modelo-logico.md"))
    parser.add_argument("--saida-json", default=str(_AQUI.parents[1] / "resultado.json"))
    args = parser.parse_args()

    caminho_entrega = Path(args.entrega)
    if not caminho_entrega.exists():
        print(f"::error::Arquivo de entrega não encontrado: {caminho_entrega}")
        return 1

    texto = caminho_entrega.read_text(encoding="utf-8")
    diagrama = parse_mermaid_er(texto)

    criterios_p1 = avaliar_parte_1(diagrama, texto)
    criterios_p2 = avaliar_parte_2(diagrama, texto)

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
