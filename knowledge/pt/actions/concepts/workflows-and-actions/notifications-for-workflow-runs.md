---
title: Notificações para execuções de fluxo de trabalho
description: Você pode se inscrever para receber notificações sobre as execuções do fluxo de trabalho que você iniciar.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/notifications-for-workflow-runs
captured: '2026-10-19'
section: Concepts / Workflows and actions
---

# Notificações para execuções de fluxo de trabalho

_Você pode se inscrever para receber notificações sobre as execuções do fluxo de trabalho que você iniciar._

Se você habilitar notificações por email ou web para GitHub Actions, receberá uma notificação quando qualquer fluxo de trabalho que você tiver disparado for concluído. A notificação incluirá o status da execução do fluxo de trabalho (incluindo execuções bem-sucedidas, com falhas, neutras e canceladas). Também pode optar por receber uma notificação apenas quando a execução de um fluxo de trabalho falhar. Para obter mais informações sobre como habilitar ou desabilitar as notificações, confira [Sobre notificações](https://docs.github.com/pt/subscriptions-and-notifications/concepts/about-notifications).

As notificações de fluxos de trabalho agendados são enviadas ao usuário que inicialmente criou o fluxo de trabalho.

* Se um usuário diferente atualizar a sintaxe cron, no evento `schedule` do arquivo de fluxo de trabalho, as notificações subsequentes serão enviadas a esse usuário em vez disso.
* Se um fluxo de trabalho agendado for desabilitado e, em seguida, reativado, as notificações serão enviadas ao usuário que reativou o fluxo de trabalho em vez do usuário que modificou a sintaxe cron pela última vez.

Você também pode visualizar o status do fluxo de trabalho executado na aba Ações de um repositório. Para saber mais, confira [Gerenciar fluxos de trabalho](../../how-tos/manage-workflow-runs.md).
