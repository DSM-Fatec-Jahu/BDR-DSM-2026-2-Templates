# templates-BDR — BDR-DSM-2026-2-Templates

Repositório de **templates práticos e autocontidos** para a disciplina
Banco de Dados — Relacional (IBD015), Fatec Jahu, DSM, 2º Semestre/2026.
Cada aula/atividade do repositório de conteúdo
([`BDR-DSM-2026-2`](https://github.com/DSM-Fatec-Jahu/BDR-DSM-2026-2),
publicado via MkDocs) que tem uma atividade prática associada ganha aqui uma
pasta em `templates/`, pronta para rodar em **GitHub Codespaces** e corrigida
automaticamente via **GitHub Actions** — sem depender do GitHub Classroom
(descontinuado em 28/08/2026; ver `docs/estrategia-github-education.md`).

> Este repositório **não substitui** o site de aulas — ele é só o espaço de
> prática. Leia a aula correspondente no site antes de abrir o template.

---

## Alvos disponíveis

| Aula/Atividade | Template | Status |
|---|---|---|
| Aula 01 — Modelagem Conceitual (MER) | [`templates/aula-01-modelagem-conceitual-mer/`](templates/aula-01-modelagem-conceitual-mer/) | ✅ Disponível |
| Aula 02 — Normalização e Modelo Lógico | [`templates/aula-02-normalizacao-modelo-logico/`](templates/aula-02-normalizacao-modelo-logico/) | ✅ Disponível |

*(Tabela atualizada a cada novo alvo processado.)*

---

## Como entregar uma atividade — passo a passo

### 1. Fork

Clique em **Fork** no canto superior direito deste repositório, criando uma
cópia na sua própria conta GitHub.

### 2. Abrir o Codespace

No **seu fork**, clique em **Code → Codespaces → Create codespace on main**.
Aguarde o ambiente subir — cada template configura seu próprio
`.devcontainer`, já com tudo que a atividade específica precisa (as
credenciais de conexão de banco, quando a atividade usa um, aparecem na
mensagem de boas-vindas do terminal). Uma alternativa ao Codespaces é clonar
o fork localmente e abrir a pasta com a extensão **Dev Containers** do VS
Code.

### 3. Criar sua branch de entrega

Dentro do Codespace (ou do seu clone local), crie uma branch com o padrão:

```
entrega/<RA>-<usuario-github>
```

Exemplo: `entrega/2026001-joaosilva`.

### 4. Resolver a atividade

Abra a pasta do template correspondente (`templates/<nome-do-alvo>/`) e siga
o `README.md` dela — cada template documenta exatamente o que editar e como
rodar a correção localmente antes de entregar.

### 5. Commit, push e Pull Request

```bash
git add templates/<nome-do-alvo>/...
git commit -m "Entrega <nome-do-alvo>"
git push origin entrega/<RA>-<usuario-github>
```

No GitHub, abra um **Pull Request do seu fork para a branch principal deste
repositório de origem** (`BDR-DSM-2026-2-Templates`, não o seu fork).
Preencha o template do PR com RA, nome completo e usuário GitHub — o
autograding usa esses campos para identificar sua entrega.

### 6. Ver o resultado da correção

A correção automática roda assim que o PR é aberto (e de novo a cada push
na mesma branch). O resultado aparece:

- como **comentário automático** no próprio Pull Request;
- como **resumo do job** na aba **Actions** do seu PR.

Não existe painel externo para o aluno — é sempre ali, no PR.

### ⚠️ O Pull Request nunca será mesclado

O PR é só o mecanismo de entrega e disparo da correção. **Nenhum PR de aluno
será aceito (merge)** neste repositório — nem mesmo os que passam em todos
os critérios. Isso é esperado e não é um problema: sua entrega já está
registrada e visível no histórico do PR, RA e nota incluídos, para o
professor conferir depois.

---

## Sobre visibilidade e privacidade

Este repositório é **público** — é o que permite fork livre por qualquer
aluno, sem gestão manual de lista de acesso, e Actions gratuito e ilimitado
independente do número de alunos. Isso significa que **Pull Requests e seus
comentários de correção ficam visíveis para toda a turma** (e para qualquer
pessoa na internet). Para as atividades formativas (aulas, laboratórios,
desafios de prática) esse é um trade-off aceito. Atividades avaliativas de
peso na nota (T1, P1, T2, P2, R) seguem uma estratégia à parte — ver
`docs/estrategia-de-avaliacao.md`.

---

## Estrutura do repositório

```
BDR-DSM-2026-2-Templates/
├── templates/<nome-do-alvo>/   # um template por aula/atividade
├── projetos/                   # templates de projetos integradores (quando existirem)
├── shared/                     # datasets, schemas e utilitários reaproveitados entre templates
├── docs/                       # documentação editorial (guia do professor, estratégias, decisões)
├── scripts/                    # utilitários de manutenção do próprio repositório
└── .github/                    # workflows de autograding e template de Pull Request
```

Documentação completa da arquitetura, de como adicionar uma nova atividade e
de como o autograding funciona por dentro: [`docs/guia-professor.md`](docs/guia-professor.md).

---

## Dúvidas

Abra uma *Issue* neste repositório, ou use o canal de contato indicado no
[site da disciplina](https://dsm-fatec-jahu.github.io/BDR-DSM-2026-2/).
