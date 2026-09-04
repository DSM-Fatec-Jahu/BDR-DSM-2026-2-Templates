# shared/

Datasets, schemas, scripts de carga, testes, exemplos e utilitários
reaproveitados por **mais de um** template. Nada aqui é específico de uma
única aula — se só um template usa, o conteúdo mora dentro da pasta desse
template, não aqui (ver `docs/guia-professor.md`).

| Subpasta | Conteúdo | Status |
|---|---|---|
| `utilitarios/` | Código Python reaproveitável entre templates | Em uso — `avaliacao.py` (estruturas genéricas `Criterio`/`montar_relatorio`/`relatorio_para_markdown`, extraídas de `mer_mermaid.py` ao processar a Aula 03 para serem compartilhadas por qualquer autograder); `mer_mermaid.py` (parser/validador de diagramas `erDiagram` Mermaid, usado pelo autograding das Aulas 01 e 02); `mariadb_ddl.py` (executor + introspector de DDL real via `INFORMATION_SCHEMA`, usado a partir da Aula 03 — primeiro template com SQL de verdade) |
| `datasets/` | Dados fictícios (nunca reais/sensíveis) usados por mais de um template | Reservado — sem conteúdo ainda |
| `schemas/` | Definições de schema (DDL) reaproveitadas entre templates | Reservado — sem conteúdo ainda (a Aula 03 tem SQL de verdade, mas o schema `helpdesk_ti` é específico dessa atividade — vive em `templates/aula-03-sql-ddl-estruturas/`, não aqui) |
| `carga/` | Scripts de carga/seed de dados | Reservado — sem conteúdo ainda |
| `testes/` | Casos de teste/fixtures reaproveitáveis | Reservado — sem conteúdo ainda |
| `exemplos/` | Exemplos de referência reaproveitados em mais de um template | Reservado — sem conteúdo ainda |

As pastas "reservadas" existem desde já na estrutura do repositório para
que a convenção de onde colocar conteúdo compartilhado já esteja clara
quando o primeiro caso de reaproveitamento aparecer — evita a tentação de
duplicar dentro de `templates/<alvo>/` "só por enquanto".
