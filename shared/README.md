# shared/

Datasets, schemas, scripts de carga, testes, exemplos e utilitários
reaproveitados por **mais de um** template. Nada aqui é específico de uma
única aula — se só um template usa, o conteúdo mora dentro da pasta desse
template, não aqui (ver `docs/guia-professor.md`).

| Subpasta | Conteúdo | Status |
|---|---|---|
| `utilitarios/` | Código Python reaproveitável entre templates | Em uso — `mer_mermaid.py` (parser/validador de diagramas `erDiagram` Mermaid, usado pelo autograding da Aula 01) |
| `datasets/` | Dados fictícios (nunca reais/sensíveis) usados por mais de um template | Reservado — sem conteúdo ainda |
| `schemas/` | Definições de schema (DDL) reaproveitadas entre templates | Reservado — sem conteúdo ainda (primeiro uso esperado a partir da Aula 03) |
| `carga/` | Scripts de carga/seed de dados | Reservado — sem conteúdo ainda |
| `testes/` | Casos de teste/fixtures reaproveitáveis | Reservado — sem conteúdo ainda |
| `exemplos/` | Exemplos de referência reaproveitados em mais de um template | Reservado — sem conteúdo ainda |

As pastas "reservadas" existem desde já na estrutura do repositório para
que a convenção de onde colocar conteúdo compartilhado já esteja clara
quando o primeiro caso de reaproveitamento aparecer — evita a tentação de
duplicar dentro de `templates/<alvo>/` "só por enquanto".
