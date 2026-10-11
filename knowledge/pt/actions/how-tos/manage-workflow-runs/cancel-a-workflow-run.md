---
title: Cancelar a execução do fluxo de trabalho
description: Você pode cancelar uma execução de fluxo de trabalho que está em andamento, incluindo todas as tarefas e etapas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/cancel-a-workflow-run
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Cancelar a execução do fluxo de trabalho

_Você pode cancelar uma execução de fluxo de trabalho que está em andamento, incluindo todas as tarefas e etapas._

## Cancelar a execução do fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções do fluxo de trabalho, clique no nome da execução `queued` ou `in progress` que deseja cancelar.
5. No canto superior direito do fluxo de trabalho, clique em **Cancelar fluxo de trabalho**.

![Captura de tela que mostra o resumo de um fluxo de trabalho que está em execução no momento. O botão "Cancelar fluxo de trabalho" está realçado com um contorno laranja escuro.](/assets/images/help/repository/cancel-check-suite-updated.png)

## Próximas etapas

Para saber mais sobre o processo GitHub usa para cancelar uma execução de fluxo de trabalho, bem como as maneiras pelas quais você pode liberar recursos relacionados, consulte [Referência de cancelamento de fluxo de trabalho](../../reference/workflows-and-actions/workflow-cancellation.md).
