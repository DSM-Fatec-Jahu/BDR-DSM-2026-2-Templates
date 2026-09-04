# Decisões Arquiteturais

Justificativa de decisões técnicas específicas tomadas ao processar cada
alvo — em especial as que se desviam do padrão genérico descrito no
processo de geração deste repositório, para que o professor possa revisar e
corrigir o raciocínio se discordar.

---

## Aula 01 — Modelagem Conceitual (MER)

### 1. Sem `.devcontainer` com MariaDB

O padrão deste repositório é todo template trazer MariaDB via
`docker-compose.yml` no `.devcontainer`. A Aula 01 **não segue esse
padrão**: o `.devcontainer/devcontainer.json` do template sobe só uma
imagem Python simples, sem nenhum serviço de banco de dados.

**Motivo:** a Aula 01 é conceitual, anterior a qualquer SQL na disciplina —
não existe nenhuma tabela real para criar, nenhuma query para rodar. Subir
um container MariaDB que nenhum artefato da atividade toca seria ruído
(tempo de build do Codespace maior, credenciais exibidas sem uso) e, mais
importante, incoerente com "fidelidade ao plano de ensino": a sala de aula
real da Aula 01 também não usa banco de dados nenhum, é modelagem em
diagrama. A partir da Aula 03 (DDL), o padrão MariaDB volta a valer.

### 2. Entrega em Markdown + Mermaid, não em `.sql` ou `.dbml`

A entrega (`sql/modelo-conceitual.md`) é um arquivo Markdown com blocos
` ```mermaid erDiagram ` — não um arquivo `.sql` (não existe SQL ainda) nem
`.dbml` (formato usado depois, na `Pratica_Modelagem_dbdiagram.md`, mas que
exige conta em dbdiagram.io para visualizar). Mermaid renderiza nativamente
tanto no preview do VS Code (com a extensão instalada no devcontainer)
quanto na própria interface do GitHub ao visualizar o arquivo — nenhuma
ferramenta externa, nenhuma conta necessária. É também a notação e a
sintaxe exatas já usadas em todos os exemplos da Aula 01, reduzindo a
distância entre "o que o aluno leu" e "o que o aluno precisa produzir".

### 3. Escolha dos Exercícios de Fixação 1 e 4 como base da atividade (não os Checkpoints)

A Aula 01 tem 5 Checkpoints com resolução já publicada em
`Aula_01_Gabarito.md` no repositório de conteúdo, e 5 Exercícios de Fixação
sem gabarito publicado. Usar um Checkpoint como atividade avaliada tornaria
a correção automática pouco significativa — a resposta estaria a um clique
de distância no próprio site da disciplina. Os Exercícios 1 (clínica
médica) e 4 (generalização de Pessoas) foram escolhidos por serem
simultaneamente **sem gabarito público** e **estruturalmente fechados o
suficiente para correção automática confiável** (ao contrário do Exercício
3, que pede "escolha um sistema do cotidiano" — sem estrutura fixa para
validar). Ver `docs/plano-de-atividades.md` para a justificativa pedagógica
completa e o motivo de os Exercícios 2 e 3 terem ficado reservados para uso
em monitoria em vez de entrarem no template.

### 4. Nomes de entidade fixos exigidos na Parte 2 (`PESSOAS`, `ALUNOS`, `PROFESSORES`, `FUNCIONARIOS_ADMINISTRATIVOS`)

O enunciado original do Exercício 4 pede "proponha o nome da superclasse" —
livre por natureza. O template da Parte 2, porém, **exige nomes de entidade
específicos** para que a correção automática consiga localizar as entidades
certas por nome. Isso restringe um grau de liberdade do enunciado original,
mas o grau de liberdade pedagógico real (decidir *quais* atributos são
comuns vs. exclusivos, e qual a restrição da hierarquia) continua
inteiramente livre — só o rótulo da caixa é fixo, não o raciocínio.
Documentado explicitamente no enunciado (`documentacao/enunciado.md`) para
não pegar o aluno de surpresa.

### 5. `pull_request_target` em vez de `pull_request` no workflow de autograding

Todo aluno entrega via fork + PR (modelo obrigatório deste repositório).
Workflows disparados por `pull_request` a partir de um fork **sempre**
recebem um `GITHUB_TOKEN` somente-leitura — não é uma configuração, é um
comportamento de segurança fixo do GitHub, e com ele seria impossível
comentar no PR ou aplicar label.

`pull_request_target` resolve isso rodando com o token do repositório de
origem (leitura/escrita) e, criticamente, **sempre usa o arquivo de
workflow da branch base** — o conteúdo do fork não pode alterar a lógica do
autograding, mesmo que o aluno edite os arquivos `.yml`. O risco clássico
de `pull_request_target` é quando o workflow faz checkout do código do PR
e **executa** esse código (instala dependências do PR, roda testes do PR,
etc.) — nesse caso, um PR malicioso poderia rodar código arbitrário com o
token de escrita. **Isso não se aplica aqui**: o único conteúdo do fork que
este workflow lê é o arquivo de entrega (`sql/modelo-conceitual.md`), e ele
é tratado estritamente como **texto**, interpretado por um parser
regex-based que nós escrevemos e controlamos
(`shared/utilitarios/mer_mermaid.py`) — nenhum comando do PR é executado,
nenhum `pip install` a partir de arquivo do PR, nenhum `eval`. O checkout
usa `persist-credentials: false` como camada adicional de precaução.

### 6. Workflow reaproveitável (`workflow_call`) em vez de um workflow monolítico por aula

`.github/workflows/_autograding-reusable.yml` concentra toda a lógica
(rodar o script de correção, comentar no PR, rotular, montar e despachar o
payload agregado); cada aula ganha só um workflow "fino"
(`autograding-aula-01.yml`) com o gatilho `pull_request_target` + filtro de
`paths` + os 4 inputs que variam por template. Isso evita duplicar ~150
linhas de YAML a cada nova aula processada — só o script Python de regras
(`tests/regras_avaliacao.py`) muda de fato entre templates.

### 7. Painel agregado (Fase 5B) via `repository_dispatch`, não artifact

O resumo agregado por aluno/nota nunca é persistido neste repositório
público (regra obrigatória — Fase 5B). O envio usa `repository_dispatch`
para um repositório privado externo (`BDR-DSM-2026-2-Notas`), autenticado
por um PAT armazenado como secret (`NOTAS_REPO_TOKEN`). Se o secret não
estiver configurado, o step falha de forma graciosa (aviso, não erro) —
a correção individual do aluno no PR continua funcionando normalmente,
só o painel do professor fica sem aquele registro até o secret ser
configurado (ver `docs/guia-professor.md`, seção de configuração manual).
