---
title: Cancelar a execução do fluxo de trabalho
description: Você pode cancelar uma execução de fluxo de trabalho que está em andamento, incluindo todas as tarefas e etapas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/cancel-a-workflow-run
captured: '2026-10-11'
section: GitHub Actions
---

# Cancelar a execução do fluxo de trabalho

_Você pode cancelar uma execução de fluxo de trabalho que está em andamento, incluindo todas as tarefas e etapas._

## Cancelar a execução do fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções do fluxo de trabalho, clique no nome da execução `queued` ou `in progress` que deseja cancelar.
5. No canto superior direito do fluxo de trabalho, clique em **Cancelar fluxo de trabalho**.

![Captura de tela que mostra o resumo de um fluxo de trabalho que está em execução no momento. O botão "Cancelar fluxo de trabalho" está realçado com um contorno laranja escuro.](/assets/images/help/repository/cancel-check-suite-updated.png)

## Próximas etapas

Para saber mais sobre o processo GitHub usa para cancelar uma execução de fluxo de trabalho, bem como as maneiras pelas quais você pode liberar recursos relacionados, consulte [Referência de cancelamento de fluxo de trabalho](../../reference/workflows-and-actions/workflow-cancellation.md).
