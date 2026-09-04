# Guia do Professor

Documentação operacional deste repositório — como ele é organizado, como
adicionar uma nova atividade e como o autograding funciona por dentro.
Atualizado incrementalmente a cada novo alvo processado.

---

## Arquitetura do repositório

```
BDR-DSM-2026-2-Templates/
├── templates/<nome-do-alvo>/
│   ├── README.md                # contextualização, objetivos, entregável, critérios
│   ├── .devcontainer/            # ambiente Codespaces específico da atividade
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

## Como adicionar uma nova atividade (novo alvo)

Este repositório é alimentado **um alvo por vez**, nunca em lote — é a regra
de escopo que governa todo o processamento (ver o prompt operacional usado
para gerar este repositório). Para processar um novo alvo:

1. Peça explicitamente o alvo pelo identificador da aula/atividade (ex.:
   "Gere o template para a Aula 05").
2. O conteúdo de origem é lido em `BDR-DSM-2026-2` (mkdocs.yml + `docs/`),
   nunca alterado.
3. Um novo `templates/<nome-do-alvo>/` é criado seguindo a estrutura acima.
4. `docs/mapeamento.md` ganha uma nova entrada.
5. Os sete documentos editoriais em `docs/` (este guia incluído) são
   atualizados incrementalmente — nunca reescritos do zero.
6. Se a atividade compartilhar dataset/schema/script com um template já
   existente, o conteúdo comum vai para `shared/`, não é duplicado.

## Como usar Codespaces e Actions

- Cada `templates/<alvo>/.devcontainer/devcontainer.json` é independente —
  um aluno abre só a pasta do seu template e tudo que a atividade precisa já
  vem configurado (banco de dados quando aplicável, extensões de VS Code,
  mensagem de boas-vindas com os comandos básicos).
- O autograding é um workflow reaproveitável
  (`.github/workflows/_autograding-reusable.yml`, `workflow_call`) chamado
  por um workflow fino por alvo (`autograding-<alvo>.yml`), que só declara o
  gatilho `pull_request_target` com filtro de `paths` para a pasta daquele
  template. Ver `docs/decisoes-arquiteturais.md` para por que
  `pull_request_target` (não `pull_request`) é necessário aqui e por que
  isso é seguro mesmo com entregas sempre vindas de fork.
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
genérico em `shared/utilitarios/mer_mermaid.py` — para mudar um critério de
correção da Aula 01, edite a lista de critérios dentro do
`regras_avaliacao.py` daquele template (funções `avaliar_parte_1` /
`avaliar_parte_2`), não o parser compartilhado, a menos que a mudança deva
valer para todos os templates que o usam.

Para rodar a correção manualmente (fora do Actions), de dentro da pasta do
template:

```bash
python tests/regras_avaliacao.py --entrega solucao-professor/<gabarito>.md
```

Rodar contra o próprio gabarito antes de publicar o template para os alunos
é a forma mais rápida de pegar um critério mal calibrado.
