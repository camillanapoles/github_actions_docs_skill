---
title: Definindo um shell padrão e diretório de trabalho
description: Defina as configurações padrão que serão aplicadas a todos os trabalhos no fluxo de trabalho ou todas as etapas de um trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/set-default-values-for-jobs
captured: '2026-10-11'
section: GitHub Actions
---

# Definindo um shell padrão e diretório de trabalho

_Defina as configurações padrão que serão aplicadas a todos os trabalhos no fluxo de trabalho ou todas as etapas de um trabalho._

## Visão geral

Use `defaults` para criar um `map` com as configurações padrão que se aplicarão a todas as tarefas do fluxo de trabalho. Você também pode definir configurações padrão que estão disponíveis apenas para uma tarefa. Para obter mais informações, confira [`jobs.<job_id>.defaults`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_iddefaults).

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## Definindo o shell padrão e diretório de trabalho

Você pode usar `defaults.run` para fornecer as opções `shell` e `working-directory` padrão para todas as etapas do [`run`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsrun) em um fluxo de trabalho. Você também pode definir configurações padrão para `run` as quais só estão disponíveis para um trabalho. Para obter mais informações, confira [`jobs.<job_id>.defaults.run`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_iddefaultsrun). Você não pode usar contextos ou expressões nesta palavra-chave.

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

### Exemplo: Defina o shell padrão e o diretório de trabalho

```yaml
defaults:
  run:
    shell: bash
    working-directory: ./scripts
```

## Definindo os valores padrão para um trabalho específico

Use `jobs.<job_id>.defaults` para criar um `map` das configurações padrão que será aplicado a todas as etapas do trabalho. Você também pode definir as configurações-padrão para todo o fluxo de trabalho. Para obter mais informações, confira [`defaults`](../../../reference/workflows-and-actions/workflow-syntax.md#defaults).

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## Definindo o shell padrão e o diretório de trabalho para uma tarefa

Use `jobs.<job_id>.defaults.run` para fornecer o `shell` e o `working-directory` padrão para todas as etapas `run` do trabalho.

Você pode fornecer as opções `shell` e `working-directory` padrão para todas as etapas [`run`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsrun) de um trabalho. Também pode definir as configurações padrão para `run` em todo o fluxo de trabalho. Para obter mais informações, consulte [`defaults.run`](../../../reference/workflows-and-actions/workflow-syntax.md#defaultsrun).

Esses podem ser substituídos nos níveis `jobs.<job_id>.defaults.run` e `jobs.<job_id>.steps[*].run`.

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

### Exemplo: definindo as opções padrão da etapa `run` para um trabalho

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash
        working-directory: ./scripts
```
