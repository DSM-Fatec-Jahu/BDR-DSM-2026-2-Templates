# scripts/

Utilitários de **manutenção do próprio repositório de templates** — não
conteúdo pedagógico, não código que o aluno executa como parte de uma
atividade (isso vive em `templates/<alvo>/tests/`).

Nenhum script de manutenção foi necessário ainda (repositório com um único
template). Candidatos naturais para o futuro, conforme o número de
templates crescer:

- Um script que valide, para todo `templates/*/`, que a estrutura mínima
  obrigatória existe (`README.md`, `.devcontainer/`, `sql/`, `tests/`,
  `datasets/`, `documentacao/`) — útil como *lint* antes de publicar um
  novo alvo.
- Um script que gere o esqueleto de um novo `templates/<nome-do-alvo>/`
  seguindo a estrutura padrão automaticamente.
