# Guia do Professor

Documentação operacional deste repositório — como ele é organizado, como
adicionar uma nova atividade e como o autograding funciona por dentro.
Atualizado incrementalmente a cada novo alvo processado.

---

## Arquitetura do repositório

```
BDR-DSM-2026-2-Templates/
├── .devcontainer/
│   └── <nome-do-alvo>/            # ambiente Codespaces específico da atividade
│       ├── devcontainer.json      # "name" aqui é o que aparece no seletor do GitHub
│       ├── boas-vindas.sh
│       └── docker-compose.yml     # só nos alvos com banco de dados real (Aula 03+)
├── templates/<nome-do-alvo>/
│   ├── README.md                # contextualização, objetivos, entregável, critérios
│   ├── sql/                      # o que o aluno edita (nome mantido por convenção — ver nota abaixo)
│   ├── tests/                    # script(s) de correção automática (rodam local e no Actions)
│   ├── datasets/                 # dados de apoio, se a atividade precisar
│   ├── documentacao/             # enunciado completo da atividade
│   └── solucao-professor/        # gabarito — NUNCA commitado (.gitignore), só local
├── projetos/                     # templates de projetos integradores maiores
├── shared/                       # datasets/schemas/utilitários reaproveitados entre templates
├── docs/                         # esta documentação editorial
├── scripts/                      # utilitários de manutenção do repositório (não pedagógicos)
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        ├── _autograding-reusable.yml   # lógica de correção reaproveitável (workflow_call)
        └── autograding-<alvo>.yml      # um "caller" fino por alvo, com o path filter
```

> 📌 **Nota sobre a pasta `sql/`:** o nome é mantido em todo template, mesmo
> quando a atividade é puramente conceitual e não produz nenhum arquivo
> `.sql` de verdade (caso da Aula 01, que entrega um `.md` com diagramas
> Mermaid). Isso mantém a navegação previsível entre templates e simplifica
> qualquer automação futura que precise localizar "a pasta de trabalho do
> aluno" por convenção. Cada template explica no seu próprio `README.md` o
> que de fato vive ali.

> 📌 **Nota sobre `.devcontainer/<nome-do-alvo>/` viver na raiz, não dentro
> de `templates/<nome-do-alvo>/`:** o GitHub só oferece o seletor nativo
> "qual configuração de Codespace usar" quando todas as configurações do
> repositório vivem sob um único `.devcontainer/` na raiz, cada uma em sua
> própria subpasta (`.devcontainer/<nome>/devcontainer.json`). Configs
> espalhadas em subpastas do repositório (o layout antigo,
> `templates/<alvo>/.devcontainer/`) não aparecem nesse seletor — o GitHub
> simplesmente não as escaneia. Por isso todo novo alvo com ambiente próprio
> precisa da config em `.devcontainer/<nome-do-alvo>/`, nunca dentro de
> `templates/<nome-do-alvo>/`. Ver seção "Como usar Codespaces e Actions"
> abaixo para o que cada `devcontainer.json` precisa declarar para abrir já
> na pasta certa.

## Como adicionar uma nova atividade (novo alvo)

Este repositório é alimentado **um alvo por vez**, nunca em lote — é a regra
de escopo que governa todo o processamento (ver o prompt operacional usado
para gerar este repositório). Para processar um novo alvo:

1. Peça explicitamente o alvo pelo identificador da aula/atividade (ex.:
   "Gere o template para a Aula 05").
2. O conteúdo de origem é lido em `BDR-DSM-2026-2` (mkdocs.yml + `docs/`),
   nunca alterado.
3. Um novo `templates/<nome-do-alvo>/` é criado seguindo a estrutura acima.
4. Uma nova `.devcontainer/<nome-do-alvo>/` é criada **na raiz do
   repositório** (nunca dentro de `templates/<nome-do-alvo>/`) — ver a nota
   acima sobre por que o local importa. No mínimo:
   - `devcontainer.json` com um `"name"` descritivo (é o texto que aparece
     no seletor do GitHub) e `workspaceFolder` apontando para
     `/workspace/templates/<nome-do-alvo>` — use `workspaceMount` (Aulas
     01/02) se não precisar de banco, ou `dockerComposeFile` + `service`
     (Aula 03+) se precisar. Isso garante que o Codespace já abre direto na
     pasta do aluno, sem precisar de `cd` manual.
   - `boas-vindas.sh`, referenciado em `postCreateCommand` por **caminho
     absoluto** (`/workspace/.devcontainer/<nome-do-alvo>/boas-vindas.sh`) —
     caminho relativo não funciona aqui porque o `postCreateCommand` roda
     com `workspaceFolder` (a pasta do template) como diretório atual, não
     a pasta do `.devcontainer`.
   - `postAttachCommand` abrindo automaticamente `documentacao/enunciado.md`
     e `README.md` (caminhos relativos a `workspaceFolder`, então já
     resolvem certo) — é o que faz o enunciado aparecer sozinho assim que o
     Codespace conecta, sem o aluno precisar procurar.
5. `docs/mapeamento.md` ganha uma nova entrada.
6. Os sete documentos editoriais em `docs/` (este guia incluído) são
   atualizados incrementalmente — nunca reescritos do zero.
7. Se a atividade compartilhar dataset/schema/script com um template já
   existente, o conteúdo comum vai para `shared/`, não é duplicado.

## Como usar Codespaces e Actions

- Cada `.devcontainer/<alvo>/devcontainer.json` é independente e vive na
  raiz do repositório (não dentro de `templates/<alvo>/` — ver nota na
  seção anterior). Como todas as configs ficam sob o mesmo `.devcontainer/`
  raiz, o GitHub detecta que há mais de uma e, ao criar um Codespace, mostra
  um seletor nativo com o `"name"` de cada `devcontainer.json` (ex.: "BDR —
  Aula 01 — Modelagem Conceitual (MER)") — o aluno escolhe a aula
  correspondente e tudo que a atividade precisa já vem configurado (banco de
  dados quando aplicável, extensões de VS Code, mensagem de boas-vindas com
  os comandos básicos). A partir da Aula 03, "banco de dados quando
  aplicável" passa a significar um `docker-compose.yml` com um serviço
  MariaDB de verdade — ver `docs/decisoes-arquiteturais.md`, seção Aula 03.
- **Onde aparece esse seletor:** no repositório (ou fork), botão **Code →
  aba Codespaces → "Create codespace on main"**. Se o botão rápido não
  perguntar nada, use o menu **"..." → "New with options..."** — essa tela
  tem um campo **Dev container configuration** listando as aulas
  disponíveis pelo nome. Ela só existe porque os `devcontainer.json` estão
  centralizados em `.devcontainer/` na raiz; se um novo alvo for criado no
  layout antigo (`templates/<alvo>/.devcontainer/`), o seletor não vai
  listá-lo.
- **O que o aluno vê ao conectar:** cada `devcontainer.json` define
  `workspaceFolder` apontando para `/workspace/templates/<alvo>/` (via
  `workspaceMount` nos alvos sem banco, ou via o mount do
  `docker-compose.yml` nos alvos com banco) — então o terminal e o
  explorador de arquivos já abrem dentro da pasta certa, sem precisar de
  `cd`. O `postAttachCommand` abre automaticamente `documentacao/enunciado.md`
  e `README.md` assim que o editor conecta, então o enunciado completo da
  atividade aparece sozinho, sem o aluno precisar procurar pela árvore de
  pastas do repositório inteiro.
- O autograding é um workflow reaproveitável
  (`.github/workflows/_autograding-reusable.yml`, `workflow_call`) chamado
  por um workflow fino por alvo (`autograding-<alvo>.yml`), que só declara o
  gatilho `pull_request_target` com filtro de `paths` para a pasta daquele
  template. Ver `docs/decisoes-arquiteturais.md` para por que
  `pull_request_target` (não `pull_request`) é necessário aqui e por que
  isso é seguro mesmo com entregas sempre vindas de fork. Esse mesmo
  workflow reaproveitável já sobe um serviço MariaDB descartável (usado só
  pelos templates que executam SQL — Aula 03 em diante; os demais o
  ignoram).
- O resumo agregado (Fase 5B) é enviado, via `repository_dispatch`, a um
  repositório **privado** separado (`BDR-DSM-2026-2-Notas`) — nunca
  persistido neste repositório público, nem como artifact do Actions.

### Configuração manual necessária (uma vez, feita pelo professor)

1. Criar o repositório privado `BDR-DSM-2026-2-Notas` (mesma conta/organização).
2. Gerar um **Personal Access Token (fine-grained)** com permissão
   `Contents: Read and write` (ou, no mínimo, permissão para disparar
   `repository_dispatch`) restrito ao repositório `BDR-DSM-2026-2-Notas`.
3. Cadastrar esse token como secret **`NOTAS_REPO_TOKEN`** em
   `BDR-DSM-2026-2-Templates` → Settings → Secrets and variables → Actions.
4. Desmarcar a flag **"Template repository"** nas configurações deste
   repositório (Settings → General) — o fluxo de entrega é fork, não "Use
   this template". Ver `docs/estrategia-github-education.md`.
5. Sem o secret configurado, o autograding continua funcionando
   normalmente para o aluno (comentário + job summary no PR) — só o envio
   ao painel consolidado do professor é pulado, com um aviso (`::warning::`)
   visível na aba Actions.

## Como adicionar datasets compartilhados

Datasets, schemas de carga ou scripts usados por mais de um template vão em
`shared/` (`datasets/`, `schemas/`, `carga/`, `testes/`, `exemplos/`,
`utilitarios/`), nunca duplicados dentro de `templates/<alvo>/datasets/`.
Todo dado é fictício, gerado proceduralmente — nunca dado real ou sensível.
O template referencia o conteúdo de `shared/` por caminho relativo
(`../../../shared/...`) a partir da sua própria pasta.

## Como corrigir e personalizar critérios de avaliação

Cada template tem seu próprio script em `tests/`, que define as regras de
correção daquele alvo especificamente (por exemplo,
`templates/aula-01-modelagem-conceitual-mer/tests/regras_avaliacao.py`).
Templates baseados em diagramas Mermaid reaproveitam o parser/validador
genérico em `shared/utilitarios/mer_mermaid.py`; templates com SQL de
verdade (Aula 03 em diante) reaproveitam `shared/utilitarios/mariadb_ddl.py`
(executa o script do aluno e introspecciona `INFORMATION_SCHEMA`). Ambos
compartilham o formato de relatório de `shared/utilitarios/avaliacao.py`
(`Criterio`, `montar_relatorio`, `relatorio_para_markdown`). Para mudar um
critério de correção de um alvo específico, edite a lista de critérios
dentro do `regras_avaliacao.py` daquele template (funções `avaliar_parte_1`
/ `avaliar_parte_2`), não os utilitários compartilhados, a menos que a
mudança deva valer para todos os templates que os usam.

Para rodar a correção manualmente (fora do Actions), de dentro da pasta do
template:

```bash
# Templates baseados em Mermaid (Aulas 01/02):
python tests/regras_avaliacao.py --entrega solucao-professor/<gabarito>.md

# Templates com SQL de verdade (Aula 03+) — aponte para um MariaDB
# acessível (o do .devcontainer, ou um XAMPP local, como na Aula 03):
python tests/regras_avaliacao.py --entrega solucao-professor/<gabarito>.sql \
    --host 127.0.0.1 --user root --password <senha-do-seu-mariadb>
```

Rodar contra o próprio gabarito antes de publicar o template para os alunos
é a forma mais rápida de pegar um critério mal calibrado — no caso de
templates com banco, também é a forma de garantir que o próprio gabarito
executa sem erro de sintaxe no MariaDB.
