---
title: Implantação em um ambiente específico
description: Especifique um ambiente de implantação em seu fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/deploy-to-environment
captured: '2026-10-13'
section: How tos / Write workflows / Choose what workflows do
---

# Implantação em um ambiente específico { #deploying-to-a-specific-environment }

_Especifique um ambiente de implantação em seu fluxo de trabalho._

## Pré-requisitos { #prerequisites }

Você precisa criar um ambiente antes de poder usá-lo em um fluxo de trabalho. Confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md#creating-an-environment).

## Usar um ambiente em um fluxo de trabalho { #using-an-environment-in-a-workflow }

1. Abra o arquivo do fluxo de trabalho que deseja editar.

2. Use a seguinte sintaxe para adicionar uma chave [`jobs.<job_id>.environment`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idenvironment) ao fluxo de trabalho:

            ```yaml copy
   jobs:
     JOB-ID:
       environment: ENVIRONMENT-NAME
            ```

   O trabalho escolhido agora estará sujeito a todas as regras configuradas para o ambiente especificado.

3. Opcionalmente, especifique uma URL de implantação para o ambiente usando a seguinte sintaxe:

            ```yaml copy
   jobs:
     JOB-ID:
       environment:
           name: ENVIRONMENT-NAME
           url: URL
            ```

   A URL especificada será exibida:

   * Na página de implantações do repositório
   * No grafo de visualização do fluxo de trabalho em execução
   * (Se uma solicitação de pull disparar o fluxo de trabalho) Como um botão "Exibir implantação" na linha do tempo da solicitação de pull

4. Opcionalmente, impeça que um objeto de implantação seja criado adicionando a `deployment` propriedade. Quando configurado como `false`, o job ainda tem acesso a segredos e variáveis de ambiente, mas nenhuma implantação GitHub é criada:

            ```yaml copy
   jobs:
     JOB-ID:
       environment:
           name: ENVIRONMENT-NAME
           deployment: false
            ```

   Isso é útil para trabalhos de CI ou de teste que precisam de segredos de ambiente, mas não estão realmente implantando nada. Para obter mais informações, consulte [Implantando com GitHub Actions](../../deploy/configure-and-manage-deployments/control-deployments.md#using-environments-without-deployments).
