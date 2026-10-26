---
title: Usando GitHub CLI em fluxos de trabalho
description: Você pode fazer o script com GitHub CLI em fluxos de trabalho GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-github-cli
captured: '2026-10-26'
section: How tos / Write workflows / Choose what workflows do
---

# Usando GitHub CLI em fluxos de trabalho

_Você pode fazer o script com GitHub CLI em fluxos de trabalho GitHub Actions._

!!! note
    Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

GitHub CLI está pré-instalado em todos os executores hospedados em GitHub. Para cada etapa que usa a GitHub CLI, você deve definir uma variável de ambiente denominada `GH_TOKEN` como um token com os escopos necessários.

Você pode executar qualquer comando de GitHub CLI. Por exemplo, este fluxo de trabalho usa o subcomando `gh issue comment` para adicionar um comentário quando um problema é aberto.

```yaml copy
name: Comment when opened
on:
  issues:
    types:
      - opened
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - run: gh issue comment $ISSUE --body "Thank you for opening this issue!"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE: ${{ github.event.issue.html_url }}
```

Você também pode executar chamadas de API por meio de GitHub CLI. Por exemplo, este fluxo de trabalho usa primeiro o subcomando `gh api` para consultar a API do GraphQL e analisar o resultado. Em seguida, ele armazena o resultado de uma variável de ambiente a qual pode acessar em uma etapa posterior. Na segunda etapa, ele usa o subcomando `gh issue create` para criar um problema que contém as informações da primeira etapa.

```yaml copy
name: Report remaining open issues
on:
  schedule:
    # Daily at 8:20 UTC
    - cron: '20 8 * * *'
jobs:
  track_pr:
    runs-on: ubuntu-latest
    steps:
      - run: |
          numOpenIssues="$(gh api graphql -F owner=$OWNER -F name=$REPO -f query='
            query($name: String!, $owner: String!) {
              repository(owner: $owner, name: $name) {
                issues(states:OPEN){
                  totalCount
                }
              }
            }
          ' --jq '.data.repository.issues.totalCount')"

          echo 'NUM_OPEN_ISSUES='$numOpenIssues >> $GITHUB_ENV
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OWNER: ${{ github.repository_owner }}
          REPO: ${{ github.event.repository.name }}
      - run: |
          gh issue create --title "Issue report" --body "$NUM_OPEN_ISSUES issues remaining" --repo $GITHUB_REPOSITORY
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
