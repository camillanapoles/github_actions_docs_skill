---
title: Comentar sobre um problema quando uma etiqueta é adicionada
description: Você pode usar GitHub Actions para comentar automaticamente sobre problemas quando um rótulo específico é aplicado.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/manage-your-work/add-comments-with-labels
captured: '2026-10-11'
section: Tutorials / Manage your work
---

# Comentar sobre um problema quando uma etiqueta é adicionada { #commenting-on-an-issue-when-a-label-is-added }

_Você pode usar GitHub Actions para comentar automaticamente sobre problemas quando um rótulo específico é aplicado._

## Introdução { #introduction }

Este tutorial demonstra como usar o GitHub CLI para comentar em uma issue quando um rótulo específico é adicionado. Por exemplo, quando o rótulo `help wanted` é adicionado a um problema, você pode adicionar um comentário para incentivar os colaboradores a trabalhar no problema. Para obter mais informações sobre GitHub CLI, confira [Usando GitHub CLI em fluxos de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md).

No tutorial, primeiro, você criará um arquivo de fluxo de trabalho que usa o comando `gh issue comment` para comentar em um problema. Então, você personalizará o fluxo de trabalho para atender às suas necessidades.

## Criar o fluxo de trabalho { #creating-the-workflow }

1. Escolha um repositório onde você deseja aplicar este fluxo de trabalho de gerenciamento de projetos. Você pode usar um repositório existente ao qual você tem acesso de gravação ou criar um novo repositório. Para saber mais sobre como criar um repositório, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

2. No repositório, crie um arquivo chamado `.github/workflows/YOUR_WORKFLOW.yml`, substituindo `YOUR_WORKFLOW` por um nome de sua escolha. Este é um arquivo do fluxo de trabaho. Para saber mais sobre como criar arquivos no GitHub, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

3. Copie o seguinte conteúdo YAML para o arquivo do fluxo de trabalho.

            ```yaml copy
   name: Add comment
   on:
     issues:
       types:
         - labeled
   jobs:
     add-comment:
       if: github.event.label.name == 'help wanted'
       runs-on: ubuntu-latest
       permissions:
         issues: write
       steps:
         - name: Add comment
           run: gh issue comment "$NUMBER" --body "$BODY"
           env:
             GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
             GH_REPO: ${{ github.repository }}
             NUMBER: ${{ github.event.issue.number }}
             BODY: >
               This issue is available for anyone to work on.
               **Make sure to reference this issue in your pull request.**
               :sparkles: Thank you for your contribution! :sparkles:
            ```

4. Personalize os parâmetros no seu arquivo do fluxo de trabalho:
   * Substitua `help wanted` em `if: github.event.label.name == 'help wanted'` pelo rótulo no qual deseja trabalhar. Caso deseje trabalhar em mais de um rótulo, separe as condições com `||`. Por exemplo, `if: github.event.label.name == 'bug' || github.event.label.name == 'fix me'` adicionará um comentário sempre que os rótulos `bug` ou `fix me` forem adicionados a um problema.
   * Altere o valor de `BODY` para o comentário que deseja adicionar. O markdown com estilo GitHub é suportado. Para saber mais sobre markdown, confira [Sintaxe básica de escrita e formatação](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

5. Faça o commit do arquivo de fluxo de trabalho para o branch padrão do seu repositório. Para saber mais, confira [Criar novos arquivos](https://docs.github.com/pt/repositories/working-with-files/managing-files/creating-new-files).

## Testar o fluxo de trabalho { #testing-the-workflow }

Toda vez que um problema no repositório for identificado, esse fluxo de trabalho será executado. Se o rótulo adicionado for um dos rótulos especificados no arquivo de fluxo de trabalho, o comando `gh issue comment` adicionará o comentário especificado ao problema.

Teste seu fluxo de trabalho aplicando a sua etiqueta especificada a um problema.

1. Abra um problema no seu repositório. Para saber mais, confira [Criar um problema](https://docs.github.com/pt/issues/tracking-your-work-with-issues/using-issues/creating-an-issue).
2. Etiquete o problema com a etiqueta especificada no seu arquivo de fluxo de trabalho. Para saber mais, confira [Gerenciar etiquetas](https://docs.github.com/pt/issues/using-labels-and-milestones-to-track-work/managing-labels#applying-a-label).
3. Para ver a execução do fluxo de trabalho acionada etiquetando o problema, veja o histórico de execuções do seu fluxo de trabalho. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).
4. Quando o fluxo de trabalho é concluído, o problema que você etiquetou deve ter um comentário adicionado.

## Próximas etapas { #next-steps }

* Para saber mais sobre outras coisas que você pode fazer com a CLI GitHub, como editar comentários existentes, visite o [GitHub Manual da CLI](https://cli.github.com/manual/).
