# Estratégia GitHub Education — sem GitHub Classroom

## O fim do GitHub Classroom

O GitHub Classroom foi **descontinuado em 28 de agosto de 2026** — site,
APIs e serviços relacionados desativados. Contas e repositórios já
existentes não foram afetados, mas nenhum recurso novo depende dele. Este
projeto foi desenhado desde o início para **não depender de nenhum recurso
nativo do Classroom**: sem `classroom.yml`, sem `autograding.json`, sem
barra de pontos nativa, sem fluxo de aceite de assignment. Toda a
distribuição de atividades, correção automática e organização de turma é
construída com recursos padrão do GitHub — fork, Pull Request, GitHub
Actions, Codespaces — que continuam disponíveis independentemente do que
acontece com ferramentas educacionais dedicadas.

## Papel de cada peça

| Peça | Papel |
|---|---|
| `BDR-DSM-2026-2` | Repositório de **conteúdo** — aulas publicadas via MkDocs. Autoridade pedagógica; nunca alterado por este projeto. |
| `BDR-DSM-2026-2-Templates` (este repo) | Repositório de **prática** — um template por aula/atividade, público, aberto a fork livre. |
| **Codespaces** | Ambiente de execução — cada template configura o que precisa (banco, extensões) via `.devcontainer`, sem instalação local. |
| **GitHub Actions** | Motor de correção automática — roda no Pull Request do aluno, comenta e rotula, sem infraestrutura própria. |
| `BDR-DSM-2026-2-Notas` (privado, externo a este repo) | Painel consolidado do professor — recebe só o resumo agregado (Fase 5B), nunca dados brutos de entrega. |

## O modelo de entrega: fork + Pull Request

Sem Classroom, não existe mais o fluxo "aceitar assignment → repositório
individual criado automaticamente". O modelo adotado é:

1. Aluno faz fork de `BDR-DSM-2026-2-Templates` para a própria conta.
2. Cria branch `entrega/<RA>-<usuario-github>` dentro do fork.
3. Resolve a atividade na pasta do template correspondente.
4. Commit + push da branch no próprio fork.
5. Abre Pull Request do fork para a branch principal do repositório de
   origem — isso dispara o autograding (`pull_request_target` com filtro de
   `paths`).
6. **O Pull Request nunca é mesclado.** Serve só como mecanismo de entrega e
   gatilho de correção. Isso está documentado no README raiz e no README de
   cada template, para nenhum aluno esperar aceite.

## Por que o repositório é público

Um repositório **privado** só pode ser bifurcado por quem já é colaborador
convidado — isso reintroduziria a necessidade de gerenciar uma lista de
acesso manualmente, exatamente o que o fim do Classroom tirou de cena (o
Classroom automatizava esse convite). Manter o repositório **público**:

- preserva a simplicidade do fork livre, sem gestão de acesso;
- mantém GitHub Actions gratuito e ilimitado, independente do número de
  alunos;
- tem como trade-off aceito a exposição de soluções entre colegas nos Pull
  Requests — aceitável para conteúdo formativo (aulas, laboratórios,
  desafios de prática).

Atividades avaliativas de peso na nota (T1, P1, T2, P2, R) **não** seguem
esse modelo aberto — ver `docs/estrategia-de-avaliacao.md` para o mecanismo
separado (repositório privado individual sob demanda).

## Pendência manual: desmarcar "Template repository"

Nas configurações deste repositório (Settings → General → Template
repository), a flag deve ficar **desmarcada**. Ela existiria para o fluxo
"Use this template" (que cria um repositório novo e desconectado por
aluno) — mas o fluxo adotado aqui é fork, que precisa que o repositório seja
tratado como um repositório normal, bifurcável, não como um template do
GitHub. Este é um passo manual, fora do escopo de qualquer arquivo deste
repositório — precisa ser feito uma vez pelo professor diretamente na
interface do GitHub.

## Mapeamento usuário-GitHub ↔ aluno

Sem roster automático do Classroom, o mapeamento é resolvido por dois
mecanismos combinados:

1. **Branch de entrega no padrão `entrega/<RA>-<usuario-github>`** — o RA
   sempre viaja com a submissão, mesmo que o aluno erre o campo de texto do
   PR.
2. **`.github/PULL_REQUEST_TEMPLATE.md`** exige RA, nome completo e usuário
   GitHub em campos estruturados, parseados pelo workflow de autograding
   (`.github/workflows/_autograding-reusable.yml`) para montar o resumo
   enviado à Fase 5B. O workflow cruza o usuário informado no corpo do PR
   com o autor real do PR (`context.payload.pull_request.user.login`) e
   sinaliza divergência, sem bloquear a correção.

Como camada extra de segurança contra erro de digitação, o professor mantém
uma planilha de cadastro (RA, nome, usuário GitHub) coletada uma vez no
início do semestre, usada só para conferência cruzada manual — essa
planilha não faz parte deste repositório.
