# Entrega — Aula 02 — Normalização e Modelo Lógico

> Sua entrega tem três arquivos nesta mesma pasta:
>
> - [`modelo-logico-parte1.dbml`](modelo-logico-parte1.dbml) — modelo final
>   (3FN) da Oficina Mecânica
> - [`modelo-logico-parte2.dbml`](modelo-logico-parte2.dbml) — modelo
>   lógico da Rede de Hotéis
> - Este arquivo (`modelo-logico.md`) — os dois campos de texto abaixo, que
>   não dá para representar em DBML
>
> Consulte o enunciado completo em
> [`documentacao/enunciado.md`](../documentacao/enunciado.md) antes de
> começar.
>
> **Nomenclatura:** toda PK segue `id_` + tabela no singular (Regra 5) e
> toda FK segue tabela-referenciada-no-singular + `_id` (Regra 6) — a
> correção automática espera exatamente esses nomes.

---

## Parte 1 — a) Mapeamento de dependências funcionais

> Mapeie as dependências da tabela desnormalizada em relação à chave
> composta `(id_ordem, cod_servico)`, seguindo o formato das Seções 4.2/5.2
> da aula (`X → Y`, indicando total/parcial/transitiva). Não esqueça das
> dependências transitivas "escondidas" dentro das parciais (veja o
> enunciado). O modelo final (item b) fica em
> [`modelo-logico-parte1.dbml`](modelo-logico-parte1.dbml).

<!--
Escreva aqui seu mapeamento de dependências. Exemplo do formato esperado
(não copie o conteúdo, só o formato):

(id_ordem, cod_servico) → quantidade    ✅ Depende da chave inteira
id_ordem                → data_servico  ⚠️  Dependência PARCIAL
...
-->

---

## Parte 2 — Justificativa da FK do relacionamento 1:1

> Em qual tabela você colocou a FK do relacionamento Hóspedes ×
> Cartões_Fidelidade, e por quê? Releia o Critério 1 (participação) e o
> Critério 2 (semântica) da Seção 8.1 antes de responder — inclua na sua
> resposta qual lado tem participação parcial (isso não dá para expressar
> em DBML, então só é conferido aqui no texto).

- **Justificativa:** <!-- explique em 2-4 frases -->
