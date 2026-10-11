---
title: Exibindo logs de expressão de condição de tarefa
description: Aprenda como acessar e interpretar os logs de avaliação de expressões para condições de nível de tarefa if em GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/view-job-condition-logs
captured: '2026-10-11'
section: How tos / Monitor workflows
---

# Exibindo logs de expressão de condição de tarefa

_Aprenda como acessar e interpretar os logs de avaliação de expressões para condições de nível de tarefa if em GitHub Actions._

Quando a condição `if` de um trabalho é avaliada, GitHub Actions registra a avaliação da expressão para ajudar você a entender o resultado. Isso é útil para depurar tanto o motivo pelo qual uma tarefa foi ignorada quanto o motivo pelo qual uma tarefa foi executada quando você esperava que ela fosse ignorada.

## Acessando registros de expressões

1. Navegue até o resumo da execução do fluxo de trabalho.
2. Clique na tarefa.
3. Clique em **(gear icon)**.
4. Selecione **Baixar arquivo de log**.
5. Extraia o arquivo ZIP e abra o `JOB-NAME/system.txt` arquivo.

## Noções básicas sobre a saída do log

O log do sistema mostra a avaliação da expressão:

```text
Evaluating: (success() && ((github.repository == 'octo-org/octo-repo-prod')))
Expanded: (true && (('my-username/octo-repo-prod' == 'octo-org/octo-repo-prod')))
Result: false
```

| Linha | Description |
| --- | --- |
| **Avaliar** | A expressão original `if` do seu arquivo de fluxo de trabalho. |
| **Expanded** | A expressão com valores de contexto substituídos. Isso mostra exatamente quais valores foram usados no runtime. |
| **Resultado** | O resultado final da avaliação (`true` ou `false`). |

Neste exemplo, a linha expandida revela que `github.repository` foi `'my-username/octo-repo-prod'` (não `'octo-org/octo-repo-prod'`), o que fez com que a condição fosse avaliada como `false`.

!!! note
    Os logs de expressões estão disponíveis apenas para condições em `if` nível de tarefa. Para condições em nível de etapa, você pode ativar o registro de depuração para visualizar a avaliação da expressão nos logs de tarefas. Para saber mais, confira [Habilitando o log de depuração](enable-debug-logging.md).
