"""Parser e validador estrutural para diagramas em DBML (dbdiagram.io).

Usado pelos scripts de autograding (`tests/regras_avaliacao.py` de cada
template de modelagem conceitual/lógica) para verificar a ENTREGA do aluno
sem exigir texto idêntico ao gabarito — checamos existência de tabelas,
nomenclatura de PK/FK (Regras 5, 6 e 7 da disciplina) e cardinalidade dos
relacionamentos, não a redação exata de comentários.

Substitui `mer_mermaid.py` (usado até a Aula 03/2026): a atividade passou a
pedir um arquivo `.dbml` "de verdade" (a linguagem por trás do
dbdiagram.io), colável direto no site para visualização/exportação, em vez
de um bloco ```mermaid erDiagram``` dentro de um Markdown.

Diferença estrutural importante em relação ao parser antigo: DBML só
consegue expressar formalmente a participação (obrigatória/opcional) do
lado que GUARDA a chave estrangeira — via `not null` na coluna FK. Não
existe, em DBML nem em SQL, uma forma de expressar "nem toda linha do lado
'um' tem uma linha correspondente do lado 'muitos'" como uma constraint de
schema (isso é regra de negócio, não estrutura). Por isso este módulo só
oferece `checar_participacao_fk`, que audita a nulidade da COLUNA FK — e
não tenta reconstruir a checagem de participação do lado referenciado que
o parser de Mermaid fazia lendo o símbolo Crow's Foot (aquilo era só uma
anotação de desenho, não algo garantido pelo schema). Quando uma atividade
depende de avaliar a participação do lado "um" (ex.: "nem todo hóspede tem
cartão fidelidade"), isso é responsabilidade do campo de justificativa
escrita, sempre revisado manualmente pelo professor.

Reaproveitável por qualquer aula futura que peça um `.dbml` como entrega: a
aula específica só precisa fornecer seu próprio roteiro de critérios e
chamar `parse_dbml_er()`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

from .avaliacao import Criterio, montar_relatorio, relatorio_para_markdown  # noqa: F401  (reexportado)

_TABLE_START = re.compile(r"^\s*[Tt]able\s+([A-Za-z_][A-Za-z0-9_]*)\s*\{?\s*(//.*)?$")
_BLOCK_END = re.compile(r"^\s*\}\s*$")
_ATTRIBUTE = re.compile(
    r"^\s*(?P<nome>[A-Za-z_][A-Za-z0-9_]*)\s+(?P<tipo>[A-Za-z][A-Za-z0-9_()]*)"
    r"\s*(?:\[(?P<config>[^\]]*)\])?\s*(//.*)?$"
)
_REF = re.compile(
    r'^\s*[Rr]ef(?:\s+[A-Za-z_][A-Za-z0-9_]*)?\s*:\s*'
    r'(?P<tabela_a>[A-Za-z_][A-Za-z0-9_]*)\.(?P<coluna_a>[A-Za-z_][A-Za-z0-9_]*)\s*'
    r'(?P<op><>|<|>|-)\s*'
    r'(?P<tabela_b>[A-Za-z_][A-Za-z0-9_]*)\.(?P<coluna_b>[A-Za-z_][A-Za-z0-9_]*)\s*(//.*)?$'
)
_LINHA_IGNORAVEL = re.compile(r"^\s*(//.*)?$")  # em branco ou comentário puro
_ABRE_BLOCO_GENERICO = re.compile(r"^\s*(Project|Note|Enum|TableGroup)\b.*\{\s*(//.*)?$", re.IGNORECASE)


@dataclass
class Atributo:
    tipo: str
    nome: str
    pk: bool = False
    fk: bool = False
    nullable: bool = True


@dataclass
class Relacionamento:
    entidade_a: str
    entidade_b: str
    coluna_a: str
    coluna_b: str
    operador: str  # '<', '>', '-' ou '<>'

    @property
    def classe_cardinalidade(self) -> str:
        if self.operador == "-":
            return "1:1"
        if self.operador == "<>":
            return "N:M"
        return "1:N"

    def envolve(self, x: str, y: str) -> bool:
        par = {self.entidade_a.upper(), self.entidade_b.upper()}
        return par == {x.upper(), y.upper()}


@dataclass
class DiagramaParseado:
    entidades: dict[str, list[Atributo]] = field(default_factory=dict)
    relacionamentos: list[Relacionamento] = field(default_factory=list)
    erros: list[str] = field(default_factory=list)

    def entidade(self, nome: str) -> Optional[list[Atributo]]:
        return self.entidades.get(nome.upper())

    def tem_entidade(self, nome: str) -> bool:
        return nome.upper() in self.entidades

    def atributo(self, entidade: str, nome_atributo: str) -> Optional[Atributo]:
        atrs = self.entidade(entidade) or []
        for a in atrs:
            if a.nome.upper() == nome_atributo.upper():
                return a
        return None

    def relacionamento_entre(self, a: str, b: str) -> Optional[Relacionamento]:
        for r in self.relacionamentos:
            if r.envolve(a, b):
                return r
        return None


def _marcar_fk(diagrama: DiagramaParseado, tabela: str, coluna: str) -> None:
    """Marca `coluna` como FK em `tabela`, se a tabela/coluna existir no diagrama.

    Um Ref pode vir ANTES do bloco Table correspondente no arquivo — por
    isso o atributo pode ainda não existir quando o Ref é processado; a
    marcação de FK é reaplicada em uma segunda passada (ver `parse_dbml_er`).
    """
    atrs = diagrama.entidades.get(tabela.upper())
    if not atrs:
        return
    for a in atrs:
        if a.nome.upper() == coluna.upper():
            a.fk = True


def parse_dbml_er(texto: str) -> DiagramaParseado:
    """Faz o parse de um arquivo `.dbml` (ou de blocos ```dbml``` dentro de um
    Markdown — linhas de cerca de código são ignoradas por não baterem com
    nenhum padrão reconhecido fora de um bloco `Table`)."""
    diagrama = DiagramaParseado()
    refs_pendentes: list[tuple[str, str, str]] = []  # (tabela, coluna, lado) só para reaplicar fk

    entidade_atual: Optional[str] = None
    dentro_bloco_generico = 0  # Project/Note/Enum/TableGroup — ignorados por completo

    for linha_bruta in texto.splitlines():
        linha = linha_bruta.strip()

        if dentro_bloco_generico:
            if _BLOCK_END.match(linha):
                dentro_bloco_generico -= 1
            elif linha.endswith("{"):
                dentro_bloco_generico += 1
            continue

        if entidade_atual is None:
            if _LINHA_IGNORAVEL.match(linha) or linha.startswith("```"):
                continue

            if _ABRE_BLOCO_GENERICO.match(linha):
                dentro_bloco_generico += 1
                continue

            m_ref = _REF.match(linha)
            if m_ref:
                tabela_a, coluna_a = m_ref.group("tabela_a"), m_ref.group("coluna_a")
                tabela_b, coluna_b = m_ref.group("tabela_b"), m_ref.group("coluna_b")
                op = m_ref.group("op")
                diagrama.relacionamentos.append(
                    Relacionamento(
                        entidade_a=tabela_a, entidade_b=tabela_b,
                        coluna_a=coluna_a, coluna_b=coluna_b, operador=op,
                    )
                )
                # Convenção: quem guarda a FK é o lado "muitos" — o esquerdo
                # em '>' e '-' (referencia o direito), o direito em '<'
                # (equivalente a "B > A" escrito na ordem inversa). '<>' não
                # marca FK nenhuma — é N:M conceitual, sem coluna física.
                if op in (">", "-"):
                    refs_pendentes.append((tabela_a, coluna_a, "fk"))
                elif op == "<":
                    refs_pendentes.append((tabela_b, coluna_b, "fk"))
                continue

            m_start = _TABLE_START.match(linha)
            if m_start:
                entidade_atual = m_start.group(1).upper()
                diagrama.entidades.setdefault(entidade_atual, [])
                continue

            # Linha fora de qualquer bloco reconhecido (cerca de código,
            # texto solto) — ignorada silenciosamente.
            continue

        if _BLOCK_END.match(linha):
            entidade_atual = None
            continue

        if _LINHA_IGNORAVEL.match(linha):
            continue

        m_attr = _ATTRIBUTE.match(linha)
        if m_attr:
            config = (m_attr.group("config") or "").lower()
            configs = [c.strip() for c in config.split(",") if c.strip()]
            pk = any(c in ("pk", "primary key") for c in configs)
            not_null = any(c in ("not null", "notnull") for c in configs)
            diagrama.entidades[entidade_atual].append(
                Atributo(
                    tipo=m_attr.group("tipo"),
                    nome=m_attr.group("nome"),
                    pk=pk,
                    nullable=not (pk or not_null),
                )
            )
        else:
            diagrama.erros.append(f"Linha não reconhecida dentro de Table {entidade_atual}: '{linha}'")

    for tabela, coluna, _lado in refs_pendentes:
        _marcar_fk(diagrama, tabela, coluna)

    return diagrama


def checar_entidade(diagrama: DiagramaParseado, nome: str, *, descricao: Optional[str] = None) -> Criterio:
    nome_exibicao = descricao or f"Tabela `{nome}` presente"
    if diagrama.tem_entidade(nome):
        return Criterio(nome_exibicao, True, f"Tabela `{nome}` encontrada no diagrama.")
    return Criterio(nome_exibicao, False, f"Não foi encontrado nenhum `Table {nome}` no `.dbml`.")


def checar_pk(diagrama: DiagramaParseado, entidade: str, pk_esperada: str) -> Criterio:
    nome_criterio = f"`{entidade}` tem PK `{pk_esperada}` (Regra 5)"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Tabela `{entidade}` não existe no diagrama.")
    pks = [a for a in atrs if a.pk]
    if not pks:
        return Criterio(nome_criterio, False, f"Nenhuma coluna de `{entidade}` está marcada `[pk]`.")
    nomes_pk = ", ".join(f"`{a.nome}`" for a in pks)
    if any(a.nome.lower() == pk_esperada.lower() for a in pks):
        return Criterio(nome_criterio, True, f"PK `{pk_esperada}` encontrada em `{entidade}`.")
    return Criterio(
        nome_criterio, False,
        f"`{entidade}` tem PK ({nomes_pk}) mas não `{pk_esperada}` — lembre da Regra 5 (`id_` + nome da tabela no singular).",
    )


def checar_fk(diagrama: DiagramaParseado, entidade: str, fk_esperada: str) -> Criterio:
    nome_criterio = f"`{entidade}` tem FK `{fk_esperada}` (Regra 6/7)"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Tabela `{entidade}` não existe no diagrama.")
    if any(a.fk and a.nome.lower() == fk_esperada.lower() for a in atrs):
        return Criterio(nome_criterio, True, f"FK `{fk_esperada}` encontrada em `{entidade}` (via `Ref:`).")
    fks = [a.nome for a in atrs if a.fk]
    if any(a.nome.lower() == fk_esperada.lower() for a in atrs):
        detalhe = f"A coluna `{fk_esperada}` existe em `{entidade}`, mas nenhum `Ref:` a referencia como FK."
    else:
        detalhe = f"`{entidade}` tem FKs {fks} mas não `{fk_esperada}`." if fks else f"`{entidade}` não tem nenhuma FK (nenhum `Ref:` aponta para uma coluna sua)."
    return Criterio(nome_criterio, False, detalhe)


def checar_atributo_existe(diagrama: DiagramaParseado, entidade: str, nome_atributo: str, *, descricao: Optional[str] = None) -> Criterio:
    nome_criterio = descricao or f"`{entidade}` tem atributo `{nome_atributo}`"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Tabela `{entidade}` não existe no diagrama.")
    if any(a.nome.lower() == nome_atributo.lower() for a in atrs):
        return Criterio(nome_criterio, True, f"Atributo `{nome_atributo}` encontrado em `{entidade}`.")
    return Criterio(nome_criterio, False, f"Atributo `{nome_atributo}` não encontrado em `{entidade}`.")


def checar_atributos_extras(diagrama: DiagramaParseado, entidade: str, minimo: int, *, descricao: Optional[str] = None) -> Criterio:
    """Verifica se a entidade tem ao menos `minimo` atributos além de PK/FK herdada."""
    nome_criterio = descricao or f"`{entidade}` tem ao menos {minimo} atributo(s) próprio(s)"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Tabela `{entidade}` não existe no diagrama.")
    proprios = [a for a in atrs if not (a.pk and a.fk)]
    if len(proprios) >= minimo:
        return Criterio(nome_criterio, True, f"`{entidade}` tem {len(proprios)} atributo(s) além da chave herdada.")
    return Criterio(nome_criterio, False, f"`{entidade}` tem só {len(proprios)} atributo(s) próprio(s); esperado ao menos {minimo}.")


def checar_relacionamento(
    diagrama: DiagramaParseado,
    entidade_a: str,
    entidade_b: str,
    cardinalidade_esperada: str,
    *,
    descricao: Optional[str] = None,
) -> Criterio:
    nome_criterio = descricao or f"Relacionamento `{entidade_a}`–`{entidade_b}` é {cardinalidade_esperada}"
    rel = diagrama.relacionamento_entre(entidade_a, entidade_b)
    if rel is None:
        return Criterio(nome_criterio, False, f"Não foi encontrado nenhum `Ref:` entre `{entidade_a}` e `{entidade_b}`.")
    if rel.classe_cardinalidade == cardinalidade_esperada:
        return Criterio(nome_criterio, True, f"Relacionamento `{entidade_a}`–`{entidade_b}` é {rel.classe_cardinalidade}, como esperado.")
    return Criterio(
        nome_criterio, False,
        f"Relacionamento `{entidade_a}`–`{entidade_b}` encontrado, mas com cardinalidade {rel.classe_cardinalidade} (esperado {cardinalidade_esperada}).",
    )


def checar_participacao_fk(
    diagrama: DiagramaParseado,
    entidade: str,
    coluna_fk: str,
    participacao_esperada: str,  # "total" ou "parcial"
    *,
    descricao: Optional[str] = None,
) -> Criterio:
    """Participação de `entidade` (o lado que GUARDA a FK) na relação, lida
    da nulidade de `coluna_fk`: `not null` = total, nullable = parcial.

    Só faz sentido para o lado que guarda a chave estrangeira — o lado
    referenciado ("um") não tem essa informação representável em DBML (ver
    docstring do módulo).
    """
    nome_criterio = descricao or f"Participação de `{entidade}` via `{coluna_fk}` é {participacao_esperada}"
    atr = diagrama.atributo(entidade, coluna_fk)
    if atr is None:
        return Criterio(nome_criterio, False, f"Coluna `{coluna_fk}` não encontrada em `{entidade}`.")
    real = "parcial" if atr.nullable else "total"
    if real == participacao_esperada:
        return Criterio(nome_criterio, True, f"`{entidade}.{coluna_fk}` é {'nullable' if atr.nullable else 'not null'} — participação {real}, como esperado.")
    return Criterio(
        nome_criterio, False,
        f"`{entidade}.{coluna_fk}` é {'nullable' if atr.nullable else 'not null'} — participação {real} (esperado {participacao_esperada}).",
    )
