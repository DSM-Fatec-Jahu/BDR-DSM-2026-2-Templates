#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'

================================================================
 BDR (IBD015) — Aula 01 — Modelagem Conceitual (MER)
================================================================

Esta aula é 100% conceitual (anterior a SQL) — por isso este
ambiente NÃO sobe nenhum banco de dados. Você vai editar diagramas
Mermaid dentro de arquivos Markdown.

Onde trabalhar:
  sql/modelo-conceitual.md   <- sua entrega (edite este arquivo)
  documentacao/enunciado.md  <- enunciado completo da atividade

Como visualizar seu diagrama enquanto edita:
  1. Abra sql/modelo-conceitual.md
  2. Ctrl+Shift+V (ou Cmd+Shift+V no Mac) abre a pré-visualização
     Markdown, que já renderiza os blocos ```mermaid``` graças à
     extensão "Markdown Preview Mermaid Support".
  GitHub também renderiza Mermaid automaticamente ao visualizar o
  arquivo pelo navegador — útil para conferir antes do PR.

Como conferir sua entrega antes de abrir o Pull Request:
  python tests/regras_avaliacao.py

Como entregar:
  1. git add sql/modelo-conceitual.md
  2. git commit -m "Entrega Aula 01"
  3. git push origin entrega/<SEU-RA>-<seu-usuario-github>
  4. Abra um Pull Request no GitHub, do seu fork para o repositório
     de origem (branch main), preenchendo o template do PR.

Lembrete: o Pull Request NUNCA será mesclado — ele só existe para
disparar a correção automática e ficar visível para você e para o
professor. Veja o README.md desta pasta para todos os detalhes.

================================================================
EOF
