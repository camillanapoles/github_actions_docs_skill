---
title: Passando informações entre tarefas
description: Você pode definir saídas para passar informações de um trabalho para outro.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs
captured: '2026-10-26'
section: How tos / Write workflows / Choose what workflows do
---

# Passando informações entre tarefas

_Você pode definir saídas para passar informações de um trabalho para outro._

## Como definir e usar saídas de trabalho

1. Abra o arquivo de fluxo de trabalho que contém o trabalho do qual você deseja obter saídas.

2. Use a sintaxe `jobs.<job_id>.outputs` para definir as saídas do trabalho. Por exemplo, o trabalho a seguir define as saídas `output1` e `output2`, que são mapeadas para os resultados de `step1` e `step2`, respectivamente:

            ```yaml
   jobs:
     job1:
       runs-on: ubuntu-latest
       outputs:
         output1: ${{ steps.step1.outputs.test }}
         output2: ${{ steps.step2.outputs.test }}
       steps:
         - id: step1
           run: echo "test=hello" >> "$GITHUB_OUTPUT"
         - id: step2
           run: echo "test=world" >> "$GITHUB_OUTPUT"
   ```

3. Em um trabalho separado onde deseja acessar essas saídas, use a sintaxe `jobs.<job_id>.needs` para torná-lo dependente do trabalho original. Por exemplo, o seguinte trabalho verifica se `job1` está concluído antes da execução:

            ```yaml
   jobs:
     # Assume job1 is defined as above
     job2:
       runs-on: ubuntu-latest
       needs: job1
   ```

4. Para acessar as saídas de um trabalho dependente, use a sintaxe `needs.<job_id>.outputs.<output_name>`. Por exemplo, o seguinte trabalho acessa as saídas `output1` e `output2` definidas em `job1`:

            ```yaml
   jobs:
     # Assume job1 is defined as above
     job2:
       runs-on: ubuntu-latest
       needs: job1
       steps:
         - env:
             OUTPUT1: ${{needs.job1.outputs.output1}}
             OUTPUT2: ${{needs.job1.outputs.output2}}
           run: echo "$OUTPUT1 $OUTPUT2"
   ```

## Próximas etapas

Para saber mais sobre saídas de trabalho e o contexto de `needs`, confira as seguintes seções de [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs):

* [`jobs.<job_id>.outputs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs)
* [`jobs.<job_id>.needs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds)

Para saber mais sobre como passar saídas de trabalho de um fluxo de trabalho para outro, consulte a seguinte seção de [Reutilizar fluxos de trabalho](../../reuse-automations/reuse-workflows.md):

* [Usando saídas de um fluxo de trabalho reutilizável](../../reuse-automations/reuse-workflows.md#using-outputs-from-a-reusable-workflow)
