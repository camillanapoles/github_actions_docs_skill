---
title: Concorrência
description: Saiba mais sobre como executar fluxos de trabalho e trabalhos ao mesmo tempo.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/concurrency
captured: '2026-10-26'
section: Concepts / Workflows and actions
---

# Concorrência

_Saiba mais sobre como executar fluxos de trabalho e trabalhos ao mesmo tempo._

Por padrão, GitHub Actions permite que vários trabalhos no mesmo fluxo de trabalho, várias execuções de fluxo de trabalho no mesmo repositório e várias execuções de fluxo de trabalho na conta do proprietário de um repositório ocorram simultaneamente. Isso significa que várias instâncias do mesmo fluxo de trabalho ou trabalho podem ser executadas ao mesmo tempo, executando as mesmas etapas.

GitHub Actions também permite desabilitar a execução simultânea. Isso pode ser útil para controlar os recursos da sua conta ou organização em situações em que a execução de vários fluxos de trabalho ou trabalhos ao mesmo tempo possa causar conflitos ou consumir mais minutos e armazenamento do Actions do que o esperado. Por exemplo, talvez você queira impedir a execução simultânea de várias implantações ou cancelar linters que verificam commits desatualizados.

Quando você limita a simultaneidade, por padrão, apenas uma execução pode estar pendente em um grupo de simultaneidade. Qualquer execução pendente adicional cancela a anterior. Se você precisar que execuções ocorram de forma sequencial sem serem canceladas, poderá optar por usar a fila, o que permite que várias execuções aguardem na fila e sejam realizadas em ordem.

Para começar a controlar a simultaneidade em seus próprios fluxos de trabalho com a palavra-chave `concurrency`, confira [Controlar a simultaneidade de fluxos de trabalho e tarefas](../../how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency.md).
