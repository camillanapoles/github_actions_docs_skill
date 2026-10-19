---
title: Implantando no Azure Kubernetes Service
description: Saiba como implantar um projeto no serviço Azure Kubernetes (AKS) como parte de um fluxo de trabalho de implantação contínua (CD).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/azure-kubernetes-service
captured: '2026-10-19'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantando no Azure Kubernetes Service

_Saiba como implantar um projeto no serviço Azure Kubernetes (AKS) como parte de um fluxo de trabalho de implantação contínua (CD)._

## Pré-requisitos

Antes de criar seu fluxo de trabalho de GitHub Actions, primeiro você precisa concluir as etapas de configuração a seguir:

1. Crie um cluster AKS de destino e um ACR (Azure Container Registry). Para obter mais informações, consulte [Quickstart: Implantar um cluster aks usando o portal Azure - Azure Kubernetes Service](https://docs.microsoft.com/azure/aks/kubernetes-walkthrough-portal) e [Quickstart - Criar registro no portal - Azure Container Registry](https://docs.microsoft.com/azure/container-registry/container-registry-get-started-portal) na documentação do Azure.

1. Crie um segredo chamado `AZURE_CREDENTIALS` para armazenar suas credenciais de Azure. Para obter mais informações sobre como encontrar essas informações e estruturar o segredo, consulte [a documentação da ação `Azure/login`](https://github.com/Azure/login#configure-a-service-principal-with-a-secret).

## Criar o fluxo de trabalho

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar e implantar um projeto para Azure Kubernetes Service quando o código é enviado por push para o repositório.

Abaixo da chave `env` de fluxo de trabalho, altere os seguintes valores:
* `AZURE_CONTAINER_REGISTRY` para o nome do registro de contêiner
* `PROJECT_NAME` para o nome do projeto
* `RESOURCE_GROUP` para o grupo de recursos que contém o cluster do AKS
* `CLUSTER_NAME` para o nome do cluster do AKS

Esse fluxo de trabalho usa o mecanismo de renderização `helm` para a ação [`azure/k8s-bake`](https://github.com/Azure/k8s-bake). Se você usar o mecanismo de renderização `helm`, altere o valor de `CHART_PATH` para o caminho para o arquivo do Helm. Altere `CHART_OVERRIDE_PATH` para uma matriz de caminhos de arquivo de substituição. Se você usar outro mecanismo de renderização, atualize os parâmetros de entrada enviados para a ação `azure/k8s-bake`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Build and deploy to Azure Kubernetes Service

env:
  AZURE_CONTAINER_REGISTRY: MY_REGISTRY_NAME # set this to the name of your container registry
  PROJECT_NAME: MY_PROJECT_NAME              # set this to your project's name
  RESOURCE_GROUP: MY_RESOURCE_GROUP          # set this to the resource group containing your AKS cluster
  CLUSTER_NAME: MY_CLUSTER_NAME              # set this to the name of your AKS cluster
  REGISTRY_URL: MY_REGISTRY_URL              # set this to the URL of your registry
  # If you bake using helm:
  CHART_PATH: MY_HELM_FILE                   # set this to the path to your helm file
  CHART_OVERRIDE_PATH: MY_OVERRIDE_FILES     # set this to an array of override file paths

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v6

    - name: Azure Login
      uses: azure/login@14a755a4e2fd6dff25794233def4f2cf3f866955
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}

    - name: Build image on ACR
      uses: azure/CLI@61bb69d64d613b52663984bf12d6bac8fd7b3cc8
      with:
        azcliversion: 2.29.1
        inlineScript: |
          az configure --defaults acr=${{ env.AZURE_CONTAINER_REGISTRY }}
          az acr build -t -t ${{ env.REGISTRY_URL }}/${{ env.PROJECT_NAME }}:${{ github.sha }}

    - name: Gets K8s context
      uses: azure/aks-set-context@94ccc775c1997a3fcfbfbce3c459fec87e0ab188
      with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
          resource-group: ${{ env.RESOURCE_GROUP }}
          cluster-name: ${{ env.CLUSTER_NAME }}
      id: login

    - name: Configure deployment
      uses: azure/k8s-bake@61041e8c2f75c1f01186c8f05fb8b24e1fc507d8
      with:
        renderEngine: 'helm'
        helmChart: ${{ env.CHART_PATH }}
        overrideFiles: ${{ env.CHART_OVERRIDE_PATH }}
        overrides: |
          replicas:2
        helm-version: 'latest'
      id: bake

    - name: Deploys application
      uses: Azure/k8s-deploy@dd4bbd13a5abd2fc9ca8bdcb8aee152bb718fa78
      with:
        manifests: ${{ steps.bake.outputs.manifestsBundle }}
        images: |
          ${{ env.AZURE_CONTAINER_REGISTRY }}.azurecr.io/${{ env.PROJECT_NAME }}:${{ github.sha }}
        imagepullsecrets: |
          ${{ env.PROJECT_NAME }}
```

```
## Leitura adicional

* Para o modelo de fluxo de trabalho original, confira [`azure-kubernetes-service.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/azure-kubernetes-service.yml) no repositório `starter-workflows` do GitHub Actions.
* As ações usadas neste fluxo de trabalho são as ações oficiais do Azure [`Azure/login`](https://github.com/Azure/login), [`Azure/aks-set-context`](https://github.com/Azure/aks-set-context), [`Azure/CLI`](https://github.com/Azure/CLI), [`Azure/k8s-bake`](https://github.com/Azure/k8s-bake) e [`Azure/k8s-deploy`](https://github.com/Azure/k8s-deploy).
* Para obter mais exemplos de fluxos de trabalho GitHub Action que são implantados em Azure, consulte o repositório [actions-workflow-samples](https://github.com/Azure/actions-workflow-samples).
