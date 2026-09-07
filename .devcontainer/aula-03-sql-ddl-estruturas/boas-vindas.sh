#!/usr/bin/env bash
set -euo pipefail

cat <<'EOF'

================================================================
 BDR (IBD015) — Aula 03 — SQL e DDL: Definição de Estruturas
================================================================

Esta é a primeira atividade com SQL de verdade — o ambiente já
sobe um MariaDB (mesma versão de referência da aula, via XAMPP
em sala) num container separado, chamado "mariadb".

Credenciais de conexão:
  Host:     mariadb        (de dentro deste container; use
                            127.0.0.1 se conectar do seu
                            computador local via túnel do
                            Codespace)
  Porta:    3306
  Usuário:  aluno
  Senha:    aluno
  Database: atividade       (já existe, mas a Parte 1 desta
                             atividade pede que você crie o SEU
                             PRÓPRIO banco — "aluno" tem
                             privilégio para isso, ver
                             documentacao/enunciado.md)
  Root:     usuário root, senha root (fallback, raramente
                             necessário)

Onde trabalhar:
  sql/helpdesk.sql            <- sua entrega (edite este arquivo)
  documentacao/enunciado.md   <- enunciado completo da atividade

Como testar seu script manualmente:
  mysql -h mariadb -u aluno -paluno < sql/helpdesk.sql

Como conferir sua entrega antes de abrir o Pull Request (roda o
script de verdade contra o MariaDB e confere a estrutura):
  python tests/regras_avaliacao.py --host mariadb --user aluno --password aluno

Extensão "MySQL" (cweijan.vscode-mysql-client2) já está instalada
para você navegar pelo schema visualmente, se preferir.

Como entregar:
  1. git add sql/helpdesk.sql
  2. git commit -m "Entrega Aula 03"
  3. git push origin entrega/<SEU-RA>-<seu-usuario-github>
  4. Abra um Pull Request no GitHub, do seu fork para o repositório
     de origem (branch main), preenchendo o template do PR.

Lembrete: o Pull Request NUNCA será mesclado — ele só existe para
disparar a correção automática e ficar visível para você e para o
professor. Veja o README.md desta pasta para todos os detalhes.

================================================================
EOF
