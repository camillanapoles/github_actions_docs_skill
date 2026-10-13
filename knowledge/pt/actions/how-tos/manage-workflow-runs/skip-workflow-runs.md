---
title: Ignorar execuções de fluxo de trabalho
description: Você pode ignorar as execuções de fluxo de trabalho disparadas pelos eventos push e pull_request incluindo um comando na mensagem de commit.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/skip-workflow-runs
captured: '2026-10-13'
section: How tos / Manage workflow runs
---

# Ignorar execuções de fluxo de trabalho

_Você pode ignorar as execuções de fluxo de trabalho disparadas pelos eventos push e pull_request incluindo um comando na mensagem de commit._

!!! note
    Se um fluxo de trabalho for ignorado devido à [filtragem de caminho](../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore), à [filtragem de branch](../../reference/workflows-and-actions/workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore) ou a uma mensagem do commit (veja abaixo), as verificações associadas a esse fluxo de trabalho permanecerão no estado “Pendente”. Uma solicitação de pull que exige que essas verificações sejam bem-sucedidas não poderá ser mesclada.

Os fluxos de trabalho que, de outra forma, seriam disparados por meio de `on: push` ou `on: pull_request` não serão disparados se você adicionar uma das seguintes cadeias de caracteres à mensagem de commit em um push ou ao commit HEAD de uma solicitação de pull:

* `[skip ci]`
* `[ci skip]`
* `[no ci]`
* `[skip actions]`
* `[actions skip]`

Como alternativa, você pode adicionar um trailer `skip-checks` à sua mensagem de commit. A seção de trailers deve ser incluída no final da mensagem do commit e ser precedida por duas linhas vazias. Se você já tem outros trailers em sua mensagem de commit, `skip-checks` deve ser o último. Você pode usar uma das seguintes opções:

* `skip-checks:true`
* `skip-checks: true`

Por padrão, o Git remove automaticamente novas linhas consecutivas. Para deixar a mensagem de commit exatamente como você a inseriu, use a opção `--cleanup=verbatim` no commit. Para obter mais informações, confira [`--cleanup=<mode>`](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---cleanupltmodegt) na documentação do Git.

Você não conseguirá mesclar o pull request se o repositório estiver configurado para exigir que verificações específicas sejam aprovadas primeiro. Para permitir que o merge do pull request, você pode fazer o push de um novo commit no pull request sem que a instrução seja ignorada na mensagem do commit.

!!! note
    As instruções para pular só se aplicam aos eventos `push` e `pull_request`. Por exemplo, a adição de `[skip ci]` a uma mensagem de commit não impedirá a execução de um fluxo de trabalho disparado com `on: pull_request_target`.

Ignorar as instruções só se aplica às execuções do(s) fluxo(s) de trabalho que serão acionadas pelo commit que contém as instruções de para ignorar. Você também pode desativar um fluxo de trabalho de execução. Para saber mais, confira [Desabilitar e habilitar um fluxo de trabalho](disable-and-enable-workflows.md).
