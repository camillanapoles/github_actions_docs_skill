---
title: Referência de cancelamento de fluxo de trabalho
description: Encontre informações sobre as etapas que GitHub executa para cancelar uma execução de um fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/workflow-cancellation
captured: '2026-10-11'
section: Reference / Workflows and actions
---

# Referência de cancelamento de fluxo de trabalho { #workflow-cancellation-reference }

_Encontre informações sobre as etapas que GitHub executa para cancelar uma execução de um fluxo de trabalho._

Ao cancelar uma execução de fluxo de trabalho, você pode estar executando outro software que utiliza recursos relacionados à execução do fluxo de trabalho. Para ajudá-lo a liberar recursos relacionados à execução do fluxo de trabalho, pode ajudar a entender as etapas GitHub executadas para cancelar uma execução de fluxo de trabalho.

1. Para cancelar a execução de fluxo de trabalho, o servidor avalia novamente as condições `if` para todas as tarefas em execução atualmente. Se a condição for avaliada como `true`, o trabalho não será cancelado. Por exemplo, a condição `if: always()` será avaliada como true e o trabalho continuará sendo executado. Quando não há nenhuma condição, isso é equivalente à condição `if: success()`, que só é executada se a etapa anterior foi concluída com sucesso.
2. Para trabalhos que precisam ser cancelados, o servidor envia uma mensagem de cancelamento para todas as máquinas executoras com trabalhos que precisam ser cancelados.
3. Para os trabalhos que continuam sendo executados, o servidor re-avalia as condições `if` para as etapas não concluídas. Se a condição for avaliada como `true`, a etapa continuará sendo executada. Você pode usar a expressão `cancelled` para aplicar uma verificação de status `cancelled()`. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md#cancelled).
4. Para etapas que precisam ser canceladas, a máquina do runner envia `SIGINT/Ctrl-C` para o processo de entrada da etapa (`node` para ações JavaScript, `docker` para ações de contêiner e `bash/cmd/pwd` quando se usa `run` em uma etapa). Se o processo não for encerrado em até 7.500 ms, o executor enviará `SIGTERM/Ctrl-Break` ao processo e aguardará 2.500 ms para que o processo seja encerrado. Se o processo ainda estiver em execução, o corredor finalizará abruptamente a árvore do processo.
5. Após o período de tempo limite de cancelamento de 5 minutos, o servidor encerrará à força todos os trabalhos e etapas marcadas para cancelamento que ainda estão em execução.
