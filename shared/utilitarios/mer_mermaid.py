"""Parser e validador estrutural para diagramas ``erDiagram`` do Mermaid.

Usado pelos scripts de autograding (`tests/regras_avaliacao.py` de cada
template de modelagem conceitual/lógica) para verificar a ENTREGA do aluno
sem exigir texto idêntico ao gabarito — checamos existência de entidades,
nomenclatura de PK/FK (Regras 5 e 6 da disciplina) e cardinalidade dos
relacionamentos, não a redação exata do rótulo do relacionamento.

Reaproveitável por qualquer aula futura que peça um `erDiagram` Mermaid como
entrega (Aula 02, Aula 05 — T1 Streaming, Aula 08, etc.): a aula específica
só precisa fornecer seu próprio dicionário de regras e chamar `validar()`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

_ENTITY_START = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\{\s*$")
_ENTITY_END = re.compile(r"^\s*\}\s*$")
_ATTRIBUTE = re.compile(
    r"^\s*(?P<tipo>[A-Za-z][A-Za-z0-9_()]*)\s+(?P<nome>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<chaves>[A-Za-z, ]*)$"
)
_RELACIONAMENTO = re.compile(
    r'^\s*(?P<a>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<tok_a>[|o}][|o{}])--(?P<tok_b>[|o{}][|o{}])\s*'
    r'(?P<b>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*"(?P<label>[^"]*)"\s*$'
)

# token de cardinalidade Crow's Foot -> (mínimo, máximo) lido do lado em que aparece
# máximo 'N' representa "muitos". Ver Aula 01, Seção 4.1/4.2.
_TOKENS: dict[str, tuple[int, str]] = {
    "||": (1, "1"),
    "o|": (0, "1"),
    "|o": (0, "1"),
    "o{": (0, "N"),
    "}o": (0, "N"),
    "|{": (1, "N"),
    "}|": (1, "N"),
}


@dataclass
class Atributo:
    tipo: str
    nome: str
    pk: bool = False
    fk: bool = False


@dataclass
class Relacionamento:
    entidade_a: str
    entidade_b: str
    min_a: int
    max_a: str
    min_b: int
    max_b: str
    label: str

    @property
    def classe_cardinalidade(self) -> str:
        """Classifica em '1:1', '1:N' ou 'N:M', ignorando o lado (ordem)."""
        lados = sorted([self.max_a, self.max_b])
        if lados == ["1", "1"]:
            return "1:1"
        if lados == ["1", "N"]:
            return "1:N"
        return "N:M"

    def envolve(self, x: str, y: str) -> bool:
        par = {self.entidade_a.upper(), self.entidade_b.upper()}
        return par == {x.upper(), y.upper()}

    def lado_de(self, entidade: str) -> Optional[tuple[int, str]]:
        """Retorna (min, max) do lado onde `entidade` aparece (participação dela)."""
        if entidade.upper() == self.entidade_a.upper():
            return (self.min_a, self.max_a)
        if entidade.upper() == self.entidade_b.upper():
            return (self.min_b, self.max_b)
        return None


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


def _extrair_blocos_mermaid(texto: str) -> list[str]:
    """Extrai o conteúdo de todo bloco ```mermaid ... ``` que contenha erDiagram."""
    blocos = re.findall(r"```mermaid\s*\n(.*?)```", texto, flags=re.DOTALL)
    return [b for b in blocos if "erDiagram" in b]


def parse_mermaid_er(texto: str) -> DiagramaParseado:
    """Faz o parse de todos os blocos ``erDiagram`` encontrados em `texto`.

    Várias entidades/relacionamentos podem estar espalhados em blocos
    mermaid diferentes dentro do mesmo arquivo Markdown — todos são unidos
    num único `DiagramaParseado`.
    """
    diagrama = DiagramaParseado()
    for bloco in _extrair_blocos_mermaid(texto):
        entidade_atual: Optional[str] = None
        for linha_bruta in bloco.splitlines():
            linha = linha_bruta.strip()
            if not linha or linha == "erDiagram":
                continue

            if entidade_atual is None:
                m_rel = _RELACIONAMENTO.match(linha)
                if m_rel:
                    tok_a = m_rel.group("tok_a")
                    tok_b = m_rel.group("tok_b")
                    if tok_a not in _TOKENS or tok_b not in _TOKENS:
                        diagrama.erros.append(f"Token de cardinalidade não reconhecido: '{linha}'")
                        continue
                    min_a, max_a = _TOKENS[tok_a]
                    min_b, max_b = _TOKENS[tok_b]
                    diagrama.relacionamentos.append(
                        Relacionamento(
                            entidade_a=m_rel.group("a"),
                            entidade_b=m_rel.group("b"),
                            min_a=min_a,
                            max_a=max_a,
                            min_b=min_b,
                            max_b=max_b,
                            label=m_rel.group("label"),
                        )
                    )
                    continue

                m_start = _ENTITY_START.match(linha)
                if m_start:
                    entidade_atual = m_start.group(1).upper()
                    diagrama.entidades.setdefault(entidade_atual, [])
                    continue

                # linha de entidade sem chaves, ex.: "MEDICOS }o--o{ ESPECIALIDADES : ..."
                # já tratada acima; qualquer outra coisa aqui é ignorada silenciosamente
                # (comentários, linhas em branco extras etc.)
                continue

            if _ENTITY_END.match(linha):
                entidade_atual = None
                continue

            m_attr = _ATTRIBUTE.match(linha)
            if m_attr:
                chaves = m_attr.group("chaves").upper()
                diagrama.entidades[entidade_atual].append(
                    Atributo(
                        tipo=m_attr.group("tipo"),
                        nome=m_attr.group("nome"),
                        pk="PK" in chaves,
                        fk="FK" in chaves,
                    )
                )
            else:
                diagrama.erros.append(
                    f"Linha não reconhecida dentro de {entidade_atual}: '{linha}'"
                )

    return diagrama


@dataclass
class Criterio:
    nome: str
    passou: bool
    detalhe: str
    peso: float = 1.0


def checar_entidade(diagrama: DiagramaParseado, nome: str, *, descricao: Optional[str] = None) -> Criterio:
    nome_exibicao = descricao or f"Entidade `{nome}` presente"
    if diagrama.tem_entidade(nome):
        return Criterio(nome_exibicao, True, f"Entidade `{nome}` encontrada no diagrama.")
    return Criterio(nome_exibicao, False, f"Não foi encontrada nenhuma entidade chamada `{nome}` em um bloco ```mermaid erDiagram```.")


def checar_pk(diagrama: DiagramaParseado, entidade: str, pk_esperada: str) -> Criterio:
    nome_criterio = f"`{entidade}` tem PK `{pk_esperada}` (Regra 5)"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Entidade `{entidade}` não existe no diagrama.")
    pks = [a for a in atrs if a.pk]
    if not pks:
        return Criterio(nome_criterio, False, f"Nenhum atributo de `{entidade}` está marcado como PK.")
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
        return Criterio(nome_criterio, False, f"Entidade `{entidade}` não existe no diagrama.")
    if any(a.fk and a.nome.lower() == fk_esperada.lower() for a in atrs):
        return Criterio(nome_criterio, True, f"FK `{fk_esperada}` encontrada em `{entidade}`.")
    fks = [a.nome for a in atrs if a.fk]
    detalhe = f"`{entidade}` tem FKs {fks} mas não `{fk_esperada}`." if fks else f"`{entidade}` não tem nenhuma FK marcada."
    return Criterio(nome_criterio, False, detalhe)


def checar_atributo_existe(diagrama: DiagramaParseado, entidade: str, nome_atributo: str, *, descricao: Optional[str] = None) -> Criterio:
    nome_criterio = descricao or f"`{entidade}` tem atributo `{nome_atributo}`"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Entidade `{entidade}` não existe no diagrama.")
    if any(a.nome.lower() == nome_atributo.lower() for a in atrs):
        return Criterio(nome_criterio, True, f"Atributo `{nome_atributo}` encontrado em `{entidade}`.")
    return Criterio(nome_criterio, False, f"Atributo `{nome_atributo}` não encontrado em `{entidade}`.")


def checar_atributos_extras(diagrama: DiagramaParseado, entidade: str, minimo: int, *, descricao: Optional[str] = None) -> Criterio:
    """Verifica se a entidade tem ao menos `minimo` atributos além de PK/FK herdada."""
    nome_criterio = descricao or f"`{entidade}` tem ao menos {minimo} atributo(s) próprio(s)"
    atrs = diagrama.entidade(entidade)
    if atrs is None:
        return Criterio(nome_criterio, False, f"Entidade `{entidade}` não existe no diagrama.")
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
        return Criterio(nome_criterio, False, f"Não foi encontrado nenhum relacionamento entre `{entidade_a}` e `{entidade_b}`.")
    if rel.classe_cardinalidade == cardinalidade_esperada:
        return Criterio(nome_criterio, True, f"Relacionamento `{entidade_a}`–`{entidade_b}` é {rel.classe_cardinalidade}, como esperado.")
    return Criterio(
        nome_criterio, False,
        f"Relacionamento `{entidade_a}`–`{entidade_b}` encontrado, mas com cardinalidade {rel.classe_cardinalidade} (esperado {cardinalidade_esperada}).",
    )


def checar_participacao(
    diagrama: DiagramaParseado,
    entidade_a: str,
    entidade_b: str,
    entidade_avaliada: str,
    participacao_esperada: str,  # "total" ou "parcial"
    *,
    descricao: Optional[str] = None,
) -> Criterio:
    nome_criterio = descricao or f"Participação de `{entidade_avaliada}` em `{entidade_a}`–`{entidade_b}` é {participacao_esperada}"
    rel = diagrama.relacionamento_entre(entidade_a, entidade_b)
    if rel is None:
        return Criterio(nome_criterio, False, f"Não foi encontrado nenhum relacionamento entre `{entidade_a}` e `{entidade_b}`.")
    lado = rel.lado_de(entidade_avaliada)
    if lado is None:
        return Criterio(nome_criterio, False, f"`{entidade_avaliada}` não faz parte do relacionamento encontrado.")
    minimo, _ = lado
    real = "total" if minimo == 1 else "parcial"
    if real == participacao_esperada:
        return Criterio(nome_criterio, True, f"Participação de `{entidade_avaliada}` é {real}, como esperado.")
    return Criterio(nome_criterio, False, f"Participação de `{entidade_avaliada}` encontrada como {real} (esperado {participacao_esperada}).")


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
