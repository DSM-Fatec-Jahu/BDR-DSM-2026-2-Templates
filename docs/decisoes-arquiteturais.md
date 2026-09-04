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

---

## Aula 02 — Normalização e Modelo Lógico

### 1. Reaproveitamento integral do `shared/utilitarios/mer_mermaid.py`, sem nenhuma alteração no parser

O roadmap traçado ao processar a Aula 01 (`docs/relatorio-executivo.md`)
previa a Aula 02 como "primeiro uso real" do parser compartilhado por um
segundo template, para validar se ele se sustentava fora do caso original.
Confirmado: o parser de `erDiagram` foi usado sem nenhuma mudança de
código — as únicas adições feitas para a Aula 02 foram no roteiro de
critérios (`tests/regras_avaliacao.py` deste template), não no parser em
si. O único ponto de atenção foi a semântica dos tokens de cardinalidade
Crow's Foot (`_TOKENS` em `mer_mermaid.py`): o token adjacente ao *nome* de
uma entidade no texto do diagrama determina a participação **dessa mesma**
entidade (não da outra ponta do relacionamento) — confirmado testando o
gabarito deste template contra o autograder antes de publicar (ver Seção 4
abaixo).

### 2. Sem `.devcontainer` com MariaDB, mesmo motivo da Aula 01

A Aula 02 continua anterior a qualquer SQL de verdade — o resultado da
atividade é um modelo lógico em Mermaid, não uma tabela criada em banco.
O `.devcontainer/devcontainer.json` deste template é praticamente idêntico
ao da Aula 01 (mesma imagem Python, mesmas extensões de Mermaid). O padrão
MariaDB só entra a partir da Aula 03 (DDL).

### 3. Dois cenários próprios (oficina mecânica, rede de hotéis), não os Checkpoints/Exercícios da aula original

Mesmo critério de exclusão já aplicado na Decisão 3 da Aula 01: os 6
Checkpoints da Aula 02 têm gabarito publicado em `Aula_02_Gabarito.md`, e
os 3 Exercícios de Fixação da Seção 10 **também** têm gabarito publicado
no mesmo arquivo (diferente da Aula 01, cujos Exercícios de Fixação não
tinham gabarito público — por isso puderam ser reaproveitados). Como
nenhum exercício da Aula 02 ficou "livre" de gabarito público, o template
usa dois cenários inéditos, escritos especificamente para esta atividade:

- **Parte 1 (normalização):** oficina mecânica, com uma tabela
  desnormalizada que tem duas camadas de dependência (parcial de
  `id_ordem`, com uma transitiva escondida dentro dela — via
  `placa_veiculo`, `cliente_cpf` e `mecanico_matricula`), estruturalmente
  equivalente ao exemplo passo a passo da própria Seção 7 da aula (sistema
  de escola), mas em outro domínio.
- **Parte 2 (modelo lógico):** rede de hotéis, cobrindo deliberadamente os
  quatro tipos de relacionamento da Seção 8 num único cenário coerente —
  1:N (Hóspede×Reserva), N:M com atributo do relacionamento
  (Reserva×Quarto, `valor_diaria_negociado`), 1:1 com decisão de lado de FK
  (Hóspede×Cartão_Fidelidade) e entidade fraca (Diária, dependente de
  Reserva) — mesma estrutura de composição usada no Checkpoint 6 da aula
  original (e-sports), mas em outro domínio, para preservar o valor
  pedagógico sem repetir um cenário com gabarito já público.

### 4. Validação do gabarito contra o autograder antes de publicar

Como recomendado em `docs/guia-professor.md`, o gabarito
(`solucao-professor/modelo-logico-gabarito.md`) foi rodado contra
`tests/regras_avaliacao.py` antes deste template ser considerado pronto —
resultado: 53/53 critérios atendidos (10/10 em ambas as partes). Essa
rodada foi o que revelou a necessidade de escolher os tokens de
cardinalidade corretos para expressar "participação total de
`CARTOES_FIDELIDADE`, participação parcial de `HOSPEDES`" no relacionamento
1:1 (ver Decisão 1 acima) — um erro fácil de cometer ao escrever o
`erDiagram` manualmente, e que só o teste automatizado contra o próprio
gabarito pegou antes de chegar ao aluno.

---

## Aula 03 — SQL e DDL: Definição de Estruturas

### 1. Primeiro `.devcontainer` com MariaDB real (`docker-compose.yml`)

Como antecipado nas Decisões 1 (Aula 01) e 2 (Aula 02), o padrão MariaDB via
`docker-compose.yml` volta a valer a partir daqui — é a primeira aula com
SQL de verdade. O `.devcontainer` sobe dois serviços: `mariadb` (imagem
oficial `mariadb:11.4`, a LTS mais recente disponível no momento do
processamento) e `workspace` (a imagem Python já usada nos templates
anteriores, para manter `python tests/regras_avaliacao.py` funcionando sem
instalação adicional). O volume do repositório inteiro é montado em
`/workspace` e `workspaceFolder` aponta para a subpasta deste template
dentro desse mount — replica o mesmo comportamento efetivo do
`devcontainer.json` simples (sem compose) das Aulas 01/02, em que o
workspace "aberto" por padrão é a pasta do template, mas o restante do
repositório (em especial `shared/`) continua acessível por caminho
relativo, porque `tests/regras_avaliacao.py` depende disso.

### 2. Usuário `aluno` recebe `GRANT ALL PRIVILEGES ON *.*`, não só sobre `atividade`

A imagem oficial do MariaDB, quando configurada com `MARIADB_USER`/
`MARIADB_PASSWORD`/`MARIADB_DATABASE`, concede a esse usuário privilégio
só sobre o banco indicado em `MARIADB_DATABASE` (aqui, `atividade`, mantido
por seguir literalmente a Fase 4 do processo de geração deste repositório).
Mas a Parte 1 desta atividade pede exatamente um `CREATE DATABASE` **novo**
(`helpdesk_ti`), e o usuário `aluno` precisa conseguir criar (e recriar,
idempotentemente) esse banco. A solução foi um script em
`.devcontainer/init-db/00-privilegios.sql`, montado em
`/docker-entrypoint-initdb.d/` (mecanismo padrão da imagem oficial do
MariaDB para rodar SQL na primeira inicialização), concedendo `GRANT ALL
PRIVILEGES ON *.*` a `aluno`. O banco `atividade` continua existindo e
acessível (é só o "database de boas-vindas" da imagem), mas não é usado
pelo enunciado desta atividade.

### 3. Serviço MariaDB adicionado ao workflow reaproveitável único, não duplicado

`_autograding-reusable.yml` (Decisão 6 da Aula 01) ganhou um bloco
`services: mariadb: ...` no nível do job, sempre presente — mesmo quando o
alvo que disparou o workflow (Aulas 01/02) não usa banco nenhum. A
alternativa considerada foi criar um segundo arquivo reaproveitável
(`_autograding-reusable-mariadb.yml`) só para templates com banco, mas isso
duplicaria as ~150 linhas de lógica de comentário/rotulagem/payload
agregado (Fase 5B) que já existem no arquivo único — exatamente a
duplicação que a Decisão 6 da Aula 01 queria evitar. O custo aceito é um
container de serviço MariaDB subindo (poucos segundos, com healthcheck) em
**todo** PR de **todo** template, mesmo nos que não o usam; nenhum script de
correção das Aulas 01/02 lê as variáveis de ambiente de conexão
(`DB_HOST`/`DB_PORT`/`DB_USER`/`DB_PASSWORD`, também adicionadas ao passo
"Rodar correção automática"), então o comportamento delas não muda. Em CI,
o serviço usa só o usuário `root` (sem a complicação do `GRANT` do
`.devcontainer` local) — o runner do GitHub Actions não é compartilhado
entre execuções, então não há necessidade da mesma separação de privilégio
usada no ambiente de desenvolvimento.

### 4. `shared/utilitarios/avaliacao.py` — extração das estruturas genéricas de relatório

`Criterio`, `montar_relatorio` e `relatorio_para_markdown` viviam dentro de
`mer_mermaid.py`, mas não têm nenhuma dependência de Mermaid — são só o
formato de relatório que `_autograding-reusable.yml` espera. O novo
autograder desta aula (`shared/utilitarios/mariadb_ddl.py` +
`tests/regras_avaliacao.py` deste template) precisava exatamente da mesma
estrutura, sem precisar depender do parser de Mermaid para ganhar acesso a
ela. Extraídas para `shared/utilitarios/avaliacao.py`; `mer_mermaid.py`
passou a importar de lá (reexportando os três nomes, para não quebrar o
`import` já existente em `tests/regras_avaliacao.py` das Aulas 01/02). Os
dois autograders existentes foram rodados de novo contra seus gabaritos
depois da extração (mesmo resultado de antes — 36/36 e 53/53 critérios) para
confirmar que o refactor não alterou nenhum comportamento.

### 5. `shared/utilitarios/mariadb_ddl.py` usa o cliente `mysql` via `subprocess`, não um driver Python

Mesma filosofia "sem dependência externa" de `mer_mermaid.py` (documentada
implicitamente pelo `README.md` da Aula 02: "nenhuma dependência externa é
instalada"). Em vez de instalar `mysql-connector-python` ou `PyMySQL` via
`pip`, o módulo chama o cliente `mysql` de linha de comando (já presente
nos runners `ubuntu-latest` do GitHub Actions, e garantido por uma etapa
`apt-get install mariadb-client` de segurança no workflow) — tanto para
executar o script `.sql` inteiro do aluno quanto para consultar
`INFORMATION_SCHEMA` (modo `-N -B`, saída tabulada sem cabeçalho, fácil de
parsear com `str.split("\t")`). Evita expandir a superfície de dependências
do repositório por causa de um único template.

### 6. Cenário original (central de chamados técnicos) em vez do e-commerce da Seção 11 ou dos Checkpoints/Exercícios

Mesmo critério de exclusão já aplicado nas Aulas 01 e 02: o exemplo de
e-commerce construído passo a passo na Seção 11 da aula, os 6 Checkpoints e
os 3 Exercícios de Fixação da Seção 12 têm todos resolução publicada em
`Aula_03_Gabarito.md` — usar qualquer um deles tornaria a correção
automática pouco significativa. O cenário de helpdesk foi desenhado para
cobrir a mesma superfície de mecanismos do exemplo original: FK pelo papel
semântico (`cliente_id`/`tecnico_responsavel_id` → `usuarios`, equivalente a
`cliente_id`/`funcionario_id` → `pessoas` da Seção 6.5), relacionamento N:M
com atributo próprio (`tecnicos_chamados.horas_dedicadas`, equivalente a
`itens_pedidos.preco_unitario`), `ENUM` de domínio fechado, `CHECK`
envolvendo duas colunas da mesma linha, e as três variações de `ON DELETE`
(`CASCADE`, `RESTRICT`, `SET NULL`) — sem reaproveitar nenhum nome de
tabela, coluna ou domínio de negócio já usado no material original ou nos
templates das Aulas 01/02.

### 7. Duas partes no relatório (`parte_1`/`parte_2`), não três

O enunciado tem três seções pedagógicas distintas (banco, tabelas, `ALTER
TABLE`), mas o formato de relatório que `_autograding-reusable.yml` monta
(`relatorioParte("Parte 1", ...)` / `relatorioParte("Parte 2", ...)`) está
fixado em duas partes. Em vez de generalizar esse trecho de JavaScript para
um número variável de partes (mudança de maior risco no arquivo
compartilhado, sem necessidade concreta ainda), a Parte 1 do enunciado
(`CREATE DATABASE` + `CREATE TABLE`) e a "Parte 1b" pedagógica (tabelas)
foram fundidas num único `parte_1` no relatório, com `parte_2` reservada
para os três `ALTER TABLE`. Se um alvo futuro precisar de três ou mais
partes de fato independentes, aí sim vale generalizar o workflow
reaproveitável — não antes.
