---
title: Adicionando etiquetas a problemas
description: Você pode usar GitHub Actions para rotular problemas automaticamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/manage-your-work/add-labels-to-issues
captured: '2026-10-13'
section: Tutorials / Manage your work
---

# Adicionando etiquetas a problemas { #adding-labels-to-issues }

_Você pode usar GitHub Actions para rotular problemas automaticamente._

## Introdução { #introduction }

Este tutorial demonstra como usar o GitHub CLI fluxo de trabalho para rotular problemas recém-abertos ou reabertos. Por exemplo, você pode adicionar o rótulo `triage` sempre que um problema é aberto ou reaberto. Em seguida, veja todos os problemas que precisam ser triados, filtrando pelos problemas com o rótulo `triage`.

O GitHub CLI permite que você use facilmente a API GitHub em um fluxo de trabalho.

No tutorial, primeiro você criará um arquivo de fluxo de trabalho que usa o GitHub CLI. Então, você personalizará o fluxo de trabalho para atender às suas necessidades.

## Criar o fluxo de trabalho { #creating-the-workflow }

1. Escolha um repositório onde você deseja aplicar este fluxo de trabalho de gerenciamento de projetos. Você pode usar um repositório existente ao qual você tem acesso de gravação ou criar um novo repositório. Para saber mais sobre como criar um repositório, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

2. No repositório, crie um arquivo chamado `.github/workflows/YOUR_WORKFLOW.yml`, substituindo `YOUR_WORKFLOW` por um nome de sua escolha. Este é um arquivo do fluxo de trabaho. Para saber mais sobre como criar arquivos no GitHub, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

3. Copie o seguinte conteúdo YAML para o arquivo do fluxo de trabalho.

            ```yaml copy
   name: Label issues
   on:
     issues:
       types:
         - reopened
         - opened
   jobs:
     label_issues:
       runs-on: ubuntu-latest
       permissions:
         issues: write
       steps:
         - run: gh issue edit "$NUMBER" --add-label "$LABELS"
           env:
             GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             GH_REPO: ${{ github.repository }}
             NUMBER: ${{ github.event.issue.number }}
             LABELS: triage
            ```

4. Personalize os valores `env` no seu arquivo de fluxo de trabalho:
   * Os valores `GH_TOKEN`, `GH_REPO` e `NUMBER` são configurados automaticamente usando os contextos `github` e `secrets`. Não é necessário alterar esses padrões.
   * Altere o valor de `LABELS` para a lista de rótulos que deseja adicionar ao problema. O(s) rótulo(s) deve(m) existir em seu repositório. Separe etiquetas múltiplas com vírgulas. Por exemplo, `help wanted,good first issue`. Para saber mais sobre rótulos, confira [Gerenciar etiquetas](https://docs.github.com/pt/issues/using-labels-and-milestones-to-track-work/managing-labels).

5. Faça o commit do arquivo de fluxo de trabalho para o branch padrão do seu repositório. Para saber mais, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

## Testar o fluxo de trabalho { #testing-the-workflow }

Toda vez que um problema no seu repositório for aberto ou reaberto, esse fluxo de trabalho adicionará as etiquetas que você especificou ao problema.

Teste o seu fluxo de trabalho criando um problema no seu repositório.

1. Crie um problema no seu repositório. Para saber mais, confira [Criar um problema](https://docs.github.com/pt/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).
2. Para ver a execução do fluxo de trabalho que foi acionada criando o problema, veja o histórico de execuções do seu fluxo de trabalho. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).
3. Quando o fluxo de trabalho é concluído, o problema que você criou deve ter as etiquetas especificadas adicionadas.

## Próximas etapas { #next-steps }

* Para saber mais sobre outras ações que você pode realizar com o GitHub CLI, consulte o [manual do GitHub CLI](https://cli.github.com/manual/).
* Para saber mais sobre diferentes eventos que podem disparar seu fluxo de trabalho, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#issues).
* [Search GitHub](https://github.com/search?q=path%3A.github%2Fworkflows+gh+issue+edit\&type=code) para obter exemplos de fluxos de trabalho usando `gh issue edit`.
