---
title: Usar GITHUB_TOKEN para autenticação em fluxos de trabalho
description: Saiba como usar a autenticação GITHUB_TOKEN em nome de GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/authenticate-with-github_token
captured: '2026-10-13'
section: Tutorials
---

# Usar GITHUB_TOKEN para autenticação em fluxos de trabalho

_Saiba como usar a autenticação GITHUB_TOKEN em nome de GitHub Actions._

Este tutorial orienta você sobre como usar a `GITHUB_TOKEN` autenticação em GitHub Actions fluxos de trabalho, incluindo exemplos para passar o token para ações, fazer solicitações de API e configurar permissões para automação segura.

Para obter informações de referência, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions).

## Como usar o `GITHUB_TOKEN` em um fluxo de trabalho

Você pode usar o `GITHUB_TOKEN` ao usar a sintaxe padrão para referenciar segredos: `${{ secrets.GITHUB_TOKEN }}`. Exemplos de como usar o `GITHUB_TOKEN` token incluem passar o token como uma entrada para uma ação ou usá-lo para fazer uma solicitação de API autenticada GitHub .

!!! important
    Uma ação pode acessar o `GITHUB_TOKEN` por meio do contexto `github.token`, mesmo que o fluxo de trabalho não transmita `GITHUB_TOKEN` explicitamente para a ação. Como uma boa prática de segurança, você deve sempre garantir que as ações tenham apenas o acesso mínimo necessário limitando as permissões concedidas ao `GITHUB_TOKEN`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions).

### Exemplo 1: passagem do `GITHUB_TOKEN` como entrada

Este exemplo de fluxo de trabalho usa a [CLI do GitHub](../how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md), que requer o `GITHUB_TOKEN` como o valor para o parâmetro de entrada `GH_TOKEN`:

```yaml copy
name: Open new issue
on: workflow_dispatch

jobs:
  open-issue:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - run: |
          gh issue --repo ${{ github.repository }} \
            create --title "Issue title" --body "Issue body"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Exemplo 2: chamando a API REST

Use o `GITHUB_TOKEN` para fazer chamadas à API autenticadas. Este fluxo de trabalho de exemplo cria um problema usando a GitHub API REST:

```yaml
name: Create issue on commit

on: [ push ]

jobs:
  create_issue:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Create issue using REST API
        run: |
          curl --request POST \
          --url https://api.github.com/repos/${{ github.repository }}/issues \
          --header 'authorization: Bearer ${{ secrets.GITHUB_TOKEN }}' \
          --header 'content-type: application/json' \
          --data '{
            "title": "Automated issue for commit: ${{ github.sha }}",
            "body": "This issue was automatically created by the GitHub Action workflow **${{ github.workflow }}**. \n\n The commit hash was: _${{ github.sha }}_."
            }' \
          --fail
```

## Como modificar as permissões para o `GITHUB_TOKEN`

Use chave `permissions` nos arquivos de fluxo de trabalho para modificar as permissões do `GITHUB_TOKEN` em um fluxo de trabalho inteiro ou em trabalhos individuais. Isso permite que você configure as permissões mínimas necessárias para um fluxo de trabalho ou trabalho. Como uma boa prática de segurança, você deve conceder ao `GITHUB_TOKEN` o acesso menos necessário.

Para ver a lista de permissões disponíveis para uso e seus nomes parametrizados, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions).

Os dois exemplos de fluxos de trabalho já apresentados neste artigo mostram a chave `permissions` sendo usada no nível do trabalho.

## Conceder permissões adicionais

Se você precisar de um token que exija permissões que não estejam disponíveis no `GITHUB_TOKEN`, crie um GitHub App e gere um token de acesso de instalação no seu fluxo de trabalho. Para saber mais, confira [Fazer solicitações de API autenticadas com um aplicativo GitHub em um fluxo de trabalho GitHub Actions](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow). Como alternativa, você pode criar um personal access token, armazená-lo como um segredo em seu repositório e usar o token em seu fluxo de trabalho com a `${{ secrets.SECRET_NAME }}` sintaxe. Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) e [Usar segredos em ações do GitHub](../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Próximas etapas

* [GITHUB_TOKEN](../concepts/security/github_token.md)
* [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions)
