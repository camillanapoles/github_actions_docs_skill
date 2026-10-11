---
title: Como executar scripts antes ou depois de um trabalho
description: Os scripts podem ser executado automaticamente em um executor autohospedado, diretamente antes ou depois de um trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/run-scripts
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Como executar scripts antes ou depois de um trabalho

_Os scripts podem ser executado automaticamente em um executor autohospedado, diretamente antes ou depois de um trabalho._

## Sobre os scripts pré e pós-trabalho

Você pode executar scripts automaticamente em um executor auto-hospedado, antes da execução de um trabalho ou após a conclusão da execução dele. Use esses scripts para dar suporte aos requisitos do trabalho, como a criação ou a destruição de um ambiente de executor ou a limpeza de diretórios. Use também esses scripts para acompanhar a telemetria de como os executores são usados.

Os scripts personalizados são disparados automaticamente quando uma variável de ambiente específica é definida no executor: a variável de ambiente precisa conter o caminho absoluto para o script. Para obter mais informações, confira [Como disparar os scripts](#triggering-the-scripts) abaixo.

Há suporte para as seguintes linguagens de script:

* **Bash**: usa `bash` e pode usar `sh` como alternativa. É executado por meio de `-e {pathtofile}`.
* **PowerShell**: usa `pwsh` e pode usar `powershell` como alternativa. É executado por meio de `-command \". '{pathtofile}'\"`.

## Como escrever os scripts

Seus scripts personalizados podem usar os seguintes recursos:

* **Variáveis**: os scripts têm acesso às variáveis padrão. O conteúdo completo do evento de webhook pode ser encontrado em `GITHUB_EVENT_PATH`. Para saber mais, confira [Referência de variáveis](../../../reference/workflows-and-actions/variables.md#default-environment-variables).
* **Comandos de fluxo de trabalho**: os scripts podem usar comandos de fluxo de trabalho. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-commands.md). Os scripts também podem usar arquivos de ambiente. Para obter mais informações, confira [Arquivos de ambiente](../../../reference/workflows-and-actions/workflow-commands.md#environment-files).

Seus arquivos de script precisam usar uma extensão de arquivo para a linguagem relevante, como `.sh` ou `.ps1`, para serem executados com êxito.

!!! note
    Evite usar seus scripts para exibir informações confidenciais no console, pois qualquer pessoa com acesso de leitura ao repositório poderá ver a saída nos logs da interface do usuário.

### Como tratar os códigos de saída

Para scripts de pré-trabalho, o código de saída `0` indica que o script foi concluído com sucesso e o trabalho continuará sendo executado. Se houver outro código de saída, o trabalho não será executado e será marcado como com falha. Para ver os resultados dos scripts de pré-trabalho, verifique se há entradas `Set up runner` nos logs. Para obter mais informações sobre como verificar os logs, confira [Usando registros de execução de fluxo de trabalho](../../monitor-workflows/use-workflow-run-logs.md#viewing-logs-to-diagnose-failures).

Não há suporte para a configuração [`continue-on-error`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontinue-on-error) para uso por esses scripts.

## Acionando os scripts

Os scripts personalizados precisam estar localizados no executor, mas não precisam ser armazenados no diretório do aplicativo `actions-runner`. Os scripts são executados no contexto de segurança da conta de serviço que executa o serviço de executor.

!!! note
    Os scripts disparados são processados de maneira síncrona, ou seja, bloquearão a execução do trabalho enquanto estiverem em execução.

Os scripts são executados automaticamente quando o executor tem as seguintes variáveis de ambiente que contêm um caminho absoluto para o script:

* `ACTIONS_RUNNER_HOOK_JOB_STARTED`: o script definido nessa variável de ambiente é disparado quando um trabalho é atribuído a um executor, mas antes do trabalho começar a ser executado.
* `ACTIONS_RUNNER_HOOK_JOB_COMPLETED`: o script definido nessa variável de ambiente é disparado no final do trabalho, após a execução de todas as etapas definidas no fluxo de trabalho.

Para definir essas variáveis de ambiente, você pode adicioná-las ao sistema operacional ou adicioná-las a um arquivo chamado `.env` no diretório do aplicativo do executor auto-hospedado (ou seja, o diretório no qual você baixou e descompactou o software executor). Observe que qualquer alteração no arquivo `.env` exigirá a reinicialização do executor.
Por exemplo, a seguinte entrada `.env` fará com que o executor execute automaticamente um script, salvo como `/opt/runner/cleanup_script.sh` no computador executor, antes de cada tarefa ser executada:

```bash
ACTIONS_RUNNER_HOOK_JOB_STARTED=/opt/runner/cleanup_script.sh
```

!!! note
    O script definido em `ACTIONS_RUNNER_HOOK_JOB_COMPLETED` é executado no final do trabalho, antes da conclusão do trabalho. Isso o torna inadequado para casos de uso que podem interromper um executor, como excluir o computador executor como parte de uma implementação de dimensionamento automático.

## Solução de problemas

### Permissão negada

Se você receber um erro de "permissão negada" ao tentar executar um script, verifique se o script é executável. Por exemplo, em um terminal no Linux ou no macOS, você pode usar o seguinte comando para tornar um arquivo executável.

```bash
chmod +x PATH/TO/FILE
```

Para obter informações sobre como usar fluxos de trabalho para executar scripts, confira [Adicionar scripts ao seu fluxo de trabalho](../../write-workflows/choose-what-workflows-do/add-scripts.md).

### Sem configuração de tempo limite

Atualmente, não há nenhuma configuração de tempo limite disponível para os scripts executados por `ACTIONS_RUNNER_HOOK_JOB_STARTED` ou `ACTIONS_RUNNER_HOOK_JOB_COMPLETED`. Como resultado, você pode considerar a adição de tratamento do tempo limite ao script.

### Examinar o log de execução do fluxo de trabalho

Para confirmar se os scripts estão em execução, você pode revisar os logs desse trabalho. Os scripts serão listados em etapas separadas para `Set up runner` ou `Complete runner`, dependendo do variável de ambiente que dispara o script. Para obter mais informações sobre como verificar os logs, confira [Usando registros de execução de fluxo de trabalho](../../monitor-workflows/use-workflow-run-logs.md#viewing-logs-to-diagnose-failures).
