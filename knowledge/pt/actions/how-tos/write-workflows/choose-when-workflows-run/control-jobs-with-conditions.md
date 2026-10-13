---
title: Usando condições para controlar a execução do trabalho
description: Impeça que um trabalho seja executado a menos que suas condições sejam atendidas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions
captured: '2026-10-11'
section: How tos / Write workflows / Choose when workflows run
---

# Usando condições para controlar a execução do trabalho { #using-conditions-to-control-job-execution }

_Impeça que um trabalho seja executado a menos que suas condições sejam atendidas._

Use o condicional `jobs.<job_id>.if` para impedir que um trabalho seja executado, a não ser que uma condição seja atendida. Você pode usar qualquer contexto e expressão compatível para criar uma condicional. Para obter mais informações sobre quais contextos têm suporte nessa chave, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#context-availability).

### Exemplo: somente executar o trabalho para um repositório específico { #example-only-run-job-for-a-specific-repository }

Este exemplo usa `if` para controlar quando o trabalho `production-deploy` pode ser executado. Ele só será executado se o repositório for chamado `octo-repo-prod` e estiver na organização `octo-org`. Caso contrário, o trabalho será marcado como *ignorado*.

```yaml copy
name: example-workflow
on: [push]
jobs:
  production-deploy:
    if: ${{ github.repository == 'octo-org/octo-repo-prod' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
```

Tarefas ignoradas exibem a mensagem "Essa verificação foi ignorada".

!!! note
    Um trabalho ignorado relatará o respectivo status como "Success". Ele não impedirá a mesclagem de uma solicitação de pull, mesmo que seja uma verificação necessária.

Para depurar por que uma tarefa foi ignorada ou executada inesperadamente, você pode visualizar os registros de expressão de condição da tarefa. Para saber mais, confira [Exibindo logs de expressão de condição de tarefa](../../monitor-workflows/view-job-condition-logs.md).
