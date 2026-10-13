---
title: Fechar questões inativas
description: Você pode usar o GitHub Actions para comentar ou fechar problemas inativos por um determinado período de tempo.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/manage-your-work/close-inactive-issues
captured: '2026-10-11'
section: Tutorials / Manage your work
---

# Fechar questões inativas { #closing-inactive-issues }

_Você pode usar o GitHub Actions para comentar ou fechar problemas inativos por um determinado período de tempo._

## Introdução { #introduction }

Este tutorial demonstra como usar a [ação `actions/stale`](https://github.com/marketplace/actions/close-stale-issues) para comentar e fechar problemas que estiveram inativos por um determinado período de tempo. Por exemplo, você pode comentar se um problema está inativo por 30 dias para incentivar os participantes a agir. Em seguida, se nenhuma atividade adicional ocorrer após 14 dias, você poderá fechar a questão.

No tutorial, primeiro, você criará um arquivo de fluxo de trabalho que usa a [ação `actions/stale`](https://github.com/marketplace/actions/close-stale-issues). Então, você personalizará o fluxo de trabalho para atender às suas necessidades.

## Criar o fluxo de trabalho { #creating-the-workflow }

1. Escolha um repositório onde você deseja aplicar este fluxo de trabalho de gerenciamento de projetos. Você pode usar um repositório existente ao qual você tem acesso de gravação ou criar um novo repositório. Para saber mais sobre como criar um repositório, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

2. No repositório, crie um arquivo chamado `.github/workflows/YOUR_WORKFLOW.yml`, substituindo `YOUR_WORKFLOW` por um nome de sua escolha. Este é um arquivo do fluxo de trabaho. Para saber mais sobre como criar arquivos no GitHub, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

3. Copie o seguinte conteúdo YAML para o arquivo do fluxo de trabalho.

            ```yaml copy
   name: Close inactive issues
   on:
     schedule:
       - cron: "30 1 * * *"

   jobs:
     close-issues:
       runs-on: ubuntu-latest
       permissions:
         issues: write
         pull-requests: write
       steps:
         - uses: actions/stale@v10
           with:
             days-before-issue-stale: 30
             days-before-issue-close: 14
             stale-issue-label: "stale"
             stale-issue-message: "This issue is stale because it has been open for 30 days with no activity."
             close-issue-message: "This issue was closed because it has been inactive for 14 days since being marked as stale."
             days-before-pr-stale: -1
             days-before-pr-close: -1
             repo-token: ${{ secrets.GITHUB_TOKEN }}
            ```

4. Personalize os parâmetros no seu arquivo do fluxo de trabalho:
   * Altere o valor de `on.schedule` para determinar quando deseja executar esse fluxo de trabalho. No exemplo acima, o fluxo de trabalho será executado todos os dias à 1:30 UTC. Para saber mais sobre fluxos de trabalho agendados, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).
   * Altere o valor de `days-before-issue-stale` para o número de dias sem atividade antes que a ação `actions/stale` rotule um problema. Se você nunca quiser que essa ação rotule problemas, defina esse valor como `-1`.
   * Altere o valor de `days-before-issue-close` para o número de dias sem atividade antes que a ação `actions/stale` feche um problema. Se você nunca quiser que essa ação feche problemas, defina esse valor como `-1`.
   * Altere o valor de `stale-issue-label` para o rótulo que deseja aplicar aos problemas inativos durante o tempo especificado por `days-before-issue-stale`.
   * Altere o valor de `stale-issue-message` para o comentário que deseja adicionar aos problemas rotulados pela ação `actions/stale`.
   * Altere o valor de `close-issue-message` para o comentário que deseja adicionar aos problemas fechados pela ação `actions/stale`.

5. Faça o commit do arquivo de fluxo de trabalho para o branch padrão do seu repositório. Para saber mais, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

## Resultados esperados { #expected-results }

Com base no parâmetro `schedule` (por exemplo, todos os dias à 1h30 UTC), o fluxo de trabalho encontrará os problemas inativos durante o período de tempo especificado e adicionará o comentário e o rótulo especificados. Além disso, o seu fluxo de trabalho fechará quaisquer problemas etiquetados anteriormente se nenhuma atividade adicional tiver ocorrido pelo período de tempo especificado.

!!! note
    O evento `schedule` pode ser atrasado durante períodos de cargas altas de execuções de fluxo de trabalho do GitHub Actions. Os tempos de carregamento altos incluem o início de cada hora. Se a carga for suficientemente alta o suficiente, alguns trabalhos enfileirados talvez sejam descartados. Para diminuir a probabilidade de atraso, agende o fluxo de trabalho para ser executado em uma parte diferente da hora.

Você pode visualizar o histórico de execução do fluxo de trabalho para revisar a execução periódica deste fluxo. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).

Este fluxo de trabalho só irá etiquetar e/ou fechar 30 problemas de cada vez para evitar exceder um limite de taxa. Você pode definir isso com a configuração `operations-per-run`. Para obter mais informações, confira a [documentação da ação `actions/stale`](https://github.com/marketplace/actions/close-stale-issues).

## Próximas etapas { #next-steps }

* Para descobrir outras coisas que você pode fazer com a ação `actions/stale`, como fechar solicitações de pull inativas, ignorar problemas com determinados rótulos ou marcos ou verificar apenas problemas com determinados rótulos, confira a [documentação da ação `actions/stale`](https://github.com/marketplace/actions/close-stale-issues).
* [Search GitHub](https://github.com/search?q=%22uses%3A+actions%2Fstale%22\&type=code) para obter exemplos de fluxos de trabalho usando essa ação.
