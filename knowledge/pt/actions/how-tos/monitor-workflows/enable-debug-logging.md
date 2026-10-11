---
title: Habilitando o log de depuração
description: Se os logs do fluxo de trabalho não fornecerem detalhes suficientes para diagnosticar o motivo pelo qual um fluxo de trabalho, um trabalho ou uma etapa não está funcionando como esperado, habilite o log de depuração adicional.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/enable-debug-logging
captured: '2026-10-11'
section: How tos / Monitor workflows
---

# Habilitando o log de depuração

_Se os logs do fluxo de trabalho não fornecerem detalhes suficientes para diagnosticar o motivo pelo qual um fluxo de trabalho, um trabalho ou uma etapa não está funcionando como esperado, habilite o log de depuração adicional._

Esses logs extras são habilitados pela definição de segredos ou variáveis no repositório que contém o fluxo de trabalho. Portanto, os mesmos requisitos de permissão são aplicáveis:

* Para criar segredos ou variáveis em GitHub para um repositório de organização, você deve ter `write` acesso. Para um repositório de conta pessoal, você deve ser um colaborador do repositório.
* Para criar segredos ou variáveis para um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para criar segredos ou variáveis para um ambiente em um repositório de uma organização, é necessário ter acesso `admin`. Para saber mais sobre os ambientes, confira [Gerenciar ambientes para implantação](../deploy/configure-and-manage-deployments/manage-environments.md).
* Os proprietários "Gerenciar variáveis de ações da organização" ou "Gerenciar segredos de ações da organização" podem criar segredos ou variáveis no nível da organização.

Para obter mais informações sobre como definir segredos e variáveis, consulte [Usar segredos em ações do GitHub](../write-workflows/choose-what-workflows-do/use-secrets.md) e [Armazenar informações em variáveis](../write-workflows/choose-what-workflows-do/use-variables.md).

Além disso, qualquer pessoa que tenha acesso para executar um fluxo de trabalho pode habilitar o log de diagnóstico do executor e o log de depuração de etapas para uma nova execução do fluxo de trabalho. Para saber mais, confira [Reexecutando fluxos de trabalho e tarefas](../manage-workflow-runs/re-run-workflows-and-jobs.md).

## Habilitar log de diagnóstico do runner

O log de diagnóstico do executor fornece arquivos de log adicionais que contêm informações sobre como um executor está executando um trabalho. Dois arquivos de log extras foram adicionados ao arquivo de log:

* O log de processo do runner, que inclui informações sobre a coordenação e a configuração de runners para executar trabalhos.
* O log de processo do worker, que registra em log a execução de um trabalho.

1. Para habilitar o log de diagnósticos do executor, defina o seguinte segredo ou váriável no repositório que contém o fluxo de trabalho: `ACTIONS_RUNNER_DEBUG` como `true`. Se o segredo e a variável estiverem definidos, o valor do segredo terá precedência sobre a variável.
2. Para baixar os logs de diagnóstico do runner, baixe o arquivo de log da execução de fluxo de trabalho. Os logs de diagnóstico do executor estão contidos na pasta `runner-diagnostic-logs`. Para obter mais informações sobre como baixar logs, consulte [Usando registros de execução de fluxo de trabalho](use-workflow-run-logs.md#downloading-logs).

## Habilitar log de depuração da etapa

O log de depuração da etapa aumenta o detalhamento dos logs de um trabalho durante e depois da execução dele.

1. Para habilitar o log de depuração em etapas, defina o seguinte segredo ou variável no repositório que contém o fluxo de trabalho: `ACTIONS_STEP_DEBUG` como `true`. Se o segredo e a variável estiverem definidos, o valor do segredo terá precedência sobre a variável.
2. Depois que o segredo ou a variável são definidos, mais eventos de depuração são mostrados nos logs de etapas. Para saber mais, confira [Usando registros de execução de fluxo de trabalho](use-workflow-run-logs.md#viewing-logs-to-diagnose-failures).

Você também pode usar o contexto `runner.debug` para executar etapas condicionalmente somente quando o registro em log de depuração estiver ativado. Para saber mais, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md#runner-context).
