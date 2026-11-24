#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'

================================================================
 BDR (IBD015) — Aula 01 — Modelagem Conceitual (MER)
================================================================

Esta aula é 100% conceitual (anterior a SQL) — por isso este
ambiente NÃO sobe nenhum banco de dados. Você vai editar modelos em
DBML, a linguagem por trás do dbdiagram.io.

Onde trabalhar:
  sql/modelo-conceitual-parte1.dbml   <- sua entrega (Parte 1)
  sql/modelo-conceitual-parte2.dbml   <- sua entrega (Parte 2)
  sql/modelo-conceitual.md            <- sua entrega (texto da Parte 2)
  documentacao/enunciado.md           <- enunciado completo da atividade

Como visualizar seu diagrama enquanto edita:
  1. Abra um arquivo .dbml — a extensão "dbdiagram" já dá highlight
     de sintaxe e um preview de ERD dentro do próprio VS Code.
  2. Ou cole o conteúdo do arquivo em https://dbdiagram.io (New
     Diagram > editor à esquerda) para visualizar e exportar a
     imagem — não precisa de conta. O que vale como entrega é o
     arquivo .dbml no seu fork, não o que fica salvo no site.

Como conferir sua entrega antes de abrir o Pull Request:
  python tests/regras_avaliacao.py

Como entregar:
  1. git add sql/modelo-conceitual-parte1.dbml sql/modelo-conceitual-parte2.dbml sql/modelo-conceitual.md
  2. git commit -m "Entrega Aula 01"
  3. git push origin entrega/<SEU-RA>-<seu-usuario-github>
  4. Abra um Pull Request no GitHub, do seu fork para o repositório
     de origem (branch main), preenchendo o template do PR.

Lembrete: o Pull Request NUNCA será mesclado — ele só existe para
disparar a correção automática e ficar visível para você e para o
professor. Veja o README.md desta pasta para todos os detalhes.

================================================================
EOF
