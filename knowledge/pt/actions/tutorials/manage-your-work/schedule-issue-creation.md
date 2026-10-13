---
title: Agendar a criação de problemas
description: Você pode usar o GitHub Actions para criar um problema regularmente para itens como reuniões diárias ou revisões trimestrais.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/manage-your-work/schedule-issue-creation
captured: '2026-10-13'
section: Tutorials / Manage your work
---

# Agendar a criação de problemas { #scheduling-issue-creation }

_Você pode usar o GitHub Actions para criar um problema regularmente para itens como reuniões diárias ou revisões trimestrais._

## Introdução { #introduction }

Este tutorial demonstra como usar a GitHub CLI para criar um problema regularmente. Por exemplo, você pode criar um problema toda semana para usar como agenda para uma reunião de equipe. Para obter mais informações sobre GitHub CLI, confira [Usando GitHub CLI em fluxos de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md).

No tutorial, primeiro você criará um arquivo de fluxo de trabalho que usa o GitHub CLI. Então, você personalizará o fluxo de trabalho para atender às suas necessidades.

## Criar o fluxo de trabalho { #creating-the-workflow }

1. Escolha um repositório onde você deseja aplicar este fluxo de trabalho de gerenciamento de projetos. Você pode usar um repositório existente ao qual você tem acesso de gravação ou criar um novo repositório. Para saber mais sobre como criar um repositório, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

2. No repositório, crie um arquivo chamado `.github/workflows/YOUR_WORKFLOW.yml`, substituindo `YOUR_WORKFLOW` por um nome de sua escolha. Este é um arquivo do fluxo de trabaho. Para saber mais sobre como criar arquivos no GitHub, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

3. Copie o seguinte conteúdo YAML para o arquivo do fluxo de trabalho.

            ```yaml copy
   name: Weekly Team Sync
   on:
     schedule:
       - cron: 20 07 * * 1

   jobs:
     create_issue:
       name: Create team sync issue
       runs-on: ubuntu-latest
       permissions:
         issues: write
       steps:
         - name: Create team sync issue
           run: |
             if [[ $CLOSE_PREVIOUS == true ]]; then
               previous_issue_number=$(gh issue list \
                 --label "$LABELS" \
                 --json number \
                 --jq '.[0].number')
               if [[ -n $previous_issue_number ]]; then
                 gh issue close "$previous_issue_number"
                 gh issue unpin "$previous_issue_number"
               fi
             fi
             new_issue_url=$(gh issue create \
               --title "$TITLE" \
               --assignee "$ASSIGNEES" \
               --label "$LABELS" \
               --body "$BODY")
             if [[ $PINNED == true ]]; then
               gh issue pin "$new_issue_url"
             fi
           env:
             GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             GH_REPO: ${{ github.repository }}
             TITLE: Team sync
             ASSIGNEES: monalisa,doctocat,hubot
             LABELS: weekly sync,docs-team
             BODY: |
               ### Agenda

               - [ ] Start the recording
               - [ ] Check-ins
               - [ ] Discussion points
               - [ ] Post the recording

               ### Discussion Points
               Add things to discuss below

               - [Work this week](https://github.com/orgs/github/projects/3)
             PINNED: false
             CLOSE_PREVIOUS: false
            ```

4. Personalize os parâmetros no seu arquivo do fluxo de trabalho:
   * Altere o valor de `on.schedule` para determinar quando deseja executar esse fluxo de trabalho. No exemplo acima, o fluxo de trabalho será executado todas as segundas às 7h20 UTC. Para saber mais sobre os fluxos de trabalho agendados, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).
   * Altere o valor de `ASSIGNEES` na lista de nomes de usuário do GitHub que você deseja atribuir ao problema.
   * Altere o valor de `LABELS` para a lista de rótulos que você deseja aplicar ao problema.
   * Altere o valor de `TITLE` para o título que você deseja que o problema tenha.
   * Altere o valor de `BODY` para o texto desejado no corpo do problema. O caractere `|` permite que você use um valor de várias linhas para esse parâmetro.
   * Caso deseje fixar esse problema no seu repositório, defina `PINNED` como `true`. Para saber mais sobre os problemas fixados, confira [Fixar um problema no repositório](https://docs.github.com/pt/issues/tracking-your-work-with-issues/administering-issues/pinning-an-issue-to-your-repository).
   * Caso deseje fechar o problema anterior gerado por esse fluxo de trabalho sempre que um problema é criado, defina `CLOSE_PREVIOUS` como `true`. O fluxo de trabalho fechará o problema mais recente que tem os rótulos definidos no campo `labels`. Para evitar o fechamento do problema errado, use uma etiqueta exclusiva ou uma combinação de etiquetas.

5. Faça o commit do arquivo de fluxo de trabalho para o branch padrão do seu repositório. Para saber mais, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

## Resultados esperados { #expected-results }

Com base no parâmetro `schedule` (por exemplo, todas as segundas-feiras às 7h20 UTC), o fluxo de trabalho criará um problema com os destinatários, os rótulos, o título e o corpo especificados. Se você definir `PINNED` como `true`, o fluxo de trabalho fixará o problema no seu repositório. Se você definir `CLOSE_PREVIOUS` como true, o fluxo de trabalho fechará o problema mais recente com os rótulos correspondentes.

!!! note
    O evento `schedule` pode ser atrasado durante períodos de cargas altas de execuções de fluxo de trabalho do GitHub Actions. Os tempos de carregamento altos incluem o início de cada hora. Se a carga for suficientemente alta o suficiente, alguns trabalhos enfileirados talvez sejam descartados. Para diminuir a probabilidade de atraso, agende o fluxo de trabalho para ser executado em uma parte diferente da hora.

Você pode visualizar o histórico de execução do fluxo de trabalho para revisar a execução periódica deste fluxo. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).

## Próximas etapas { #next-steps }

* Para saber mais sobre outras coisas que você pode fazer com o GitHub CLImodelo de problema, como usar um modelo de problema, consulte a [`gh issue create` documentação](https://cli.github.com/manual/gh_issue_create).
* [Pesquise o GitHub Marketplace](https://github.com/marketplace?category=\&type=actions\&verification=\&query=schedule+issue) para obter ações relacionadas a problemas agendados.
