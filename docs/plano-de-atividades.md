# Plano de Atividades

Sugestões pedagógicas de aplicação para cada alvo processado — como
conduzir a atividade em sala (individual, dupla, equipe), variações para
desafio extra ou recuperação, e uso possível em monitoria.

---

## Aula 01 — Modelagem Conceitual (MER)

**Modalidade sugerida: individual.** Modelagem conceitual é uma habilidade
de raciocínio que se consolida melhor com prática individual repetida — em
dupla, é comum que um dos dois só acompanhe passivamente a decisão do
outro sobre cardinalidade/participação, justamente os pontos mais
propensos a erro individual que a Aula 01 quer treinar.

**Justificativa da escolha do conteúdo do template:** as duas partes da
atividade reaproveitam os **Exercícios de Fixação 1 e 4** da aula original
(não os Checkpoints 1-5, que já têm gabarito publicado no site em
`Aula_01_Gabarito.md` — usá-los tornaria a correção automática pouco
significativa, já que a resposta está a um clique de distância). Exercício
1 (clínica médica) cobre entidades/atributos/relacionamentos/cardinalidade
de forma auto-contida; Exercício 4 (generalização) cobre o mecanismo mais
complexo da aula. Juntos, tocam praticamente todos os objetivos de
aprendizagem listados na aula, sem depender de conteúdo que a aula ainda
não ensinou.

### Em sala (aula síncrona)

Sugestão de condução: depois da aula expositiva, reservar os últimos 20-30
minutos (ou uma aula de exercícios dedicada, se a carga horária permitir)
para os alunos começarem a Parte 1 (clínica médica) ainda com o professor
disponível para tirar dúvidas ao vivo — é o primeiro contato deles com
Codespaces + Pull Request neste semestre, então é esperado que a mecânica
de entrega (não o conteúdo de BD) gere as primeiras dúvidas.

### Desafio extra

Para alunos que terminam adiantado: pedir a modelagem do cenário de
streaming citado na Seção 9 da aula (prévia da Atividade T1 — músicas e
filmes, playlists mistas). **Atenção:** não formalizar isso como parte do
template de Aula 01 nem atribuir nota a ele — esse cenário é literalmente o
enunciado da Atividade T1 (avaliativa, Aula 05); adiantar todos os alunos
nele via "desafio extra" bagunçaria a curva de dificuldade real do T1
quando for aplicado oficialmente. Se usado, é só como conversa aberta em
sala, sem entrega formal.

### Recuperação

Para quem entrega abaixo do esperado na nota formativa: como a atividade
não tem peso na nota final, "recuperação" aqui significa revisão guiada,
não reentrega obrigatória. Sugestão: usar os Exercícios de Fixação 2 e 3
(ainda não usados por nenhum template) como material de reforço individual,
apontando o aluno para o Gabarito dos Checkpoints (que cobre casos
correlatos) como material de apoio.

### Monitoria

Os Exercícios de Fixação 2 (leitura de diagrama) e 3 (modelagem livre,
domínio à escolha do aluno) ficam disponíveis para uso em plantão de
monitoria — não fazem parte do template porque não são estruturalmente
fechados o suficiente para correção automática confiável (Exercício 3
explicitamente pede "escolha um sistema do cotidiano", sem entidades
fixas), mas são ótimos para verificação oral/manual em atendimento
individual.

---

## Aula 02 — Normalização e Modelo Lógico

**Modalidade sugerida: individual para a Parte 1, dupla para a Parte 2.** A
identificação de dependências funcionais (Parte 1) é, como a modelagem
conceitual da Aula 01, uma habilidade que se consolida com prática
individual repetida. Já a passagem ao modelo lógico (Parte 2) tem mais
"regras aplicáveis mecanicamente" do que julgamento aberto — funciona bem
em dupla, com um aluno propondo a regra e o outro conferindo contra a
Seção 8 da aula, especialmente na decisão de lado de FK do relacionamento
1:1, que é o ponto mais sutil da parte.

**Justificativa da escolha do conteúdo do template:** diferente da Aula 01
(cujos Exercícios de Fixação não tinham gabarito publicado), todos os
Checkpoints **e** todos os Exercícios de Fixação da Aula 02 têm resolução
publicada em `Aula_02_Gabarito.md` — usar qualquer um deles tornaria a
correção automática pouco significativa. Por isso o template usa dois
cenários originais (oficina mecânica na Parte 1, rede de hotéis na Parte
2), estruturalmente equivalentes aos exemplos guiados da aula (Seção 7 e
Checkpoint 6, respectivamente) mas sem resposta pronta disponível. Ver
`docs/decisoes-arquiteturais.md`, seção Aula 02, item 3.

### Em sala (aula síncrona)

Sugestão de condução: a Parte 1 (normalização) se beneficia de ser resolvida
"ao vivo" logo após a exposição da Seção 7 da aula (o exemplo passo a passo
do sistema de escola) — o cenário da oficina mecânica usa a mesma estrutura
de raciocínio, então os alunos conseguem espelhar o passo a passo recém-visto
sem precisar decorar nada novo. A Parte 2 fica melhor para uma segunda
sessão (ou para casa), depois que a Seção 8 completa (as quatro regras) já
foi vista — tentar fazer as duas partes na mesma aula tende a apressar
demais a parte mais sutil (decisão de lado de FK no 1:1).

### Desafio extra

Para alunos que terminam adiantado: pedir para redesenhar a Parte 1
(oficina mecânica) assumindo que um mesmo veículo pode ter mais de um
proprietário ao longo do tempo (ex.: veículo vendido de um cliente para
outro) — isso quebra a suposição implícita de que `VEICULOS.cliente_id` é
suficiente, e exige perceber que a posse de um veículo é, na verdade, um
relacionamento histórico (N:M temporal entre CLIENTES e VEICULOS), não um
atributo fixo do veículo. Não formalizar isso como parte obrigatória do
template — é um bom gancho para apresentar informalmente o conceito de
"relacionamento com validade temporal", tema que a disciplina não cobre
formalmente neste bloco.

### Recuperação

Para quem entrega abaixo do esperado na nota formativa: como a atividade
não tem peso na nota final, "recuperação" aqui significa revisão guiada.
Sugestão: usar os 6 Checkpoints da própria Aula 02 (que já têm gabarito
publicado em `Aula_02_Gabarito.md`) como material de reforço individual —
diferente do template, aqui o gabarito público é uma vantagem, não um
problema, porque o objetivo passa a ser conferência, não avaliação.

### Monitoria

Os 3 Exercícios de Fixação da Seção 10 (identificação de violações,
normalização completa de um cenário de pedidos, passagem ao modelo lógico
de uma biblioteca) ficam disponíveis para atendimento individual em
monitoria — têm gabarito publicado, então servem bem para o aluno conferir
sozinho depois de tentar, sem depender de horário de atendimento.

---

---

## Aula 03 — SQL e DDL: Definição de Estruturas

**Modalidade sugerida: individual.** É a primeira vez que o aluno interage
com um banco de dados de verdade rodando (Codespace + MariaDB); erros de
sintaxe e de ambiente (esquecer `USE`, esquecer `;`, digitar um tipo
inexistente) fazem parte do aprendizado esperado desta aula, e resolver
esses erros sozinho — lendo a mensagem do MariaDB, que a própria correção
automática reproduz literalmente — é uma habilidade que se perde em dupla
(um dos dois tende a "dirigir" o teclado enquanto o outro só acompanha).

**Justificativa da escolha do conteúdo do template:** como nas Aulas 01 e
02, nenhum Checkpoint, Exercício de Fixação ou o exemplo de e-commerce da
Seção 11 foi reaproveitado (todos têm gabarito publicado). O cenário de
central de chamados técnicos (helpdesk) foi desenhado para cobrir a mesma
superfície de mecanismos do exemplo original — FK pelo papel semântico
(Regra 7), N:M com atributo próprio, `CHECK`, as três variações de `ON
DELETE` — em um domínio inédito. Ver `docs/decisoes-arquiteturais.md`,
seção Aula 03, item 6.

### Em sala (aula síncrona)

Sugestão de condução: como é a primeira atividade com ambiente de banco de
dados real, reservar tempo de aula para o passo "abrir o Codespace e
esperar o MariaDB subir" antes mesmo de começar a Parte 1 — é comum que
essa primeira conexão gere dúvidas sobre host/porta/usuário que não têm
relação com DDL em si, mas que bloqueiam o aluno se não forem resolvidas
logo. Depois disso, a Parte 1 (schema completo) se beneficia de ser
resolvida tabela por tabela, testando cada `CREATE TABLE` isoladamente
antes de passar para a próxima — em vez de escrever o script inteiro e só
então testar, estratégia que dificulta isolar em qual tabela está o erro
de sintaxe.

### Desafio extra

Para alunos que terminam adiantado: pedir para adicionar uma tabela
`avaliacoes_chamado` (1:1 com `chamados`, entidade fraca — só existe depois
que o chamado é fechado), com uma nota de 1 a 5 e um comentário opcional do
cliente, e um `CHECK` garantindo que só é possível avaliar um chamado com
`status = 'fechado'` teria que ser feito em nível de aplicação, não de
`CHECK` (que não enxerga outras linhas) — bom gancho para apresentar
informalmente por que `CHECK` não substitui um `TRIGGER` (tema fora do
escopo formal desta aula). Não formalizar como parte obrigatória do
template.

### Recuperação

Para quem entrega abaixo do esperado na nota formativa: como a atividade
não tem peso na nota final, "recuperação" aqui significa revisão guiada.
Sugestão: usar o Exercício 2 da própria Aula 03 (sistema de biblioteca, com
gabarito publicado em `Aula_03_Gabarito.md`) como material de reforço
individual — o aluno reescreve o schema sozinho e só depois confere contra
o gabarito público, prática de "fechar o ciclo" sem depender de
atendimento.

### Monitoria

Os 6 Checkpoints da Aula 03 (nomenclatura, `CREATE DATABASE`, tipos de
dados, `CREATE TABLE`/constraints, `ALTER TABLE`, `DROP` e ordem de
exclusão) ficam disponíveis para atendimento individual em monitoria — como
já têm gabarito publicado, servem bem para o aluno testar hipóteses e
conferir sozinho, especialmente o Checkpoint 6 (ordem de `DROP` com FKs),
que o template desta atividade não cobre por não ser estruturalmente
verificável do mesmo jeito (a tabela deixa de existir depois do `DROP`, o
que dificulta uma checagem via `INFORMATION_SCHEMA` tão direta quanto as
demais).

---

*(Cada novo alvo processado ganha uma seção própria acima desta linha.)*
