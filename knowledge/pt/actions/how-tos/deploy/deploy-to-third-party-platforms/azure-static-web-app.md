---
title: Fazendo a implantação nos Aplicativos Web Estáticos do Azure
description: Saiba como implantar um aplicativo web no Azure Static Web App como parte de seus fluxos de trabalho de implantação contínua (CD).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/azure-static-web-app
captured: '2026-10-19'
section: How tos / Deploy / Deploy to third party platforms
---

# Fazendo a implantação nos Aplicativos Web Estáticos do Azure

_Saiba como implantar um aplicativo web no Azure Static Web App como parte de seus fluxos de trabalho de implantação contínua (CD)._

## Pré-requisitos

Antes de criar seu fluxo de trabalho de GitHub Actions, primeiro você precisa concluir as etapas de configuração a seguir:

1. Crie um aplicativo Web estático Azure usando a opção 'Outros' para a origem da implantação. Para obter mais informações, consulte [Quickstart: Criando seu primeiro site estático no portal Azure](https://docs.microsoft.com/azure/static-web-apps/get-started-portal) na documentação do Azure.

1. Crie um segredo chamado `AZURE_STATIC_WEB_APPS_API_TOKEN` com o valor do token de implantação do aplicativo Web estático. Para obter mais informações sobre como encontrar seu token de implantação, consulte [Redefinir tokens de implantação no Azure Static Web Apps](https://docs.microsoft.com/azure/static-web-apps/deployment-token-management) na documentação do Azure.

## Criar o fluxo de trabalho

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar e implantar um aplicativo Web estático Azure quando há um push para o branch `main` ou quando uma solicitação de pull direcionada `main` é aberta, sincronizada ou reaberta. O fluxo de trabalho também destrói a implantação de pré-produção correspondente quando uma solicitação de pull direcionada a `main` é fechada.

Abaixo da chave `env` de fluxo de trabalho, altere os seguintes valores:
* `APP_LOCATION` para o local do código do cliente
* `API_LOCATION` para o local do código-fonte da API. Se `API_LOCATION` não for relevante, você poderá excluir a variável e as linhas em que ela é usada.
* `OUTPUT_LOCATION` para o local da saída de build do código do cliente

Para obter mais informações sobre esses valores, consulte [Configuração do build para Azure Static Web Apps](https://docs.microsoft.com/azure/static-web-apps/build-configuration?tabs=github-actions) na documentação do Azure.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Deploy web app to Azure Static Web Apps

env:
  APP_LOCATION: "/" # location of your client code
  API_LOCATION: "api" # location of your api source code - optional
  OUTPUT_LOCATION: "build" # location of client code build output

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

permissions:
  issues: write
  contents: read
  pull-requests: write

jobs:
  build_and_deploy:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy
    steps:
      - uses: actions/checkout@v6
        with:
          submodules: true
      - name: Build And Deploy
        uses: Azure/static-web-apps-deploy@1a947af9992250f3bc2e68ad0754c0b0c11566c9
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: ${{ env.APP_LOCATION }}
          api_location: ${{ env.API_LOCATION }}
          output_location: ${{ env.OUTPUT_LOCATION }}

  close_pull_request:
    if: github.event_name == 'pull_request' && github.event.action == 'closed'
    runs-on: ubuntu-latest
    name: Close Pull Request
    steps:
      - name: Close Pull Request
        uses: Azure/static-web-apps-deploy@1a947af9992250f3bc2e68ad0754c0b0c11566c9
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          action: "close"
```

```
## Leitura adicional

* Para o modelo de fluxo de trabalho original, confira [`azure-staticwebapp.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/azure-staticwebapp.yml) no repositório `starter-workflows` do GitHub Actions.
* A ação usada para implantar o aplicativo Web é a ação oficial Azure [`Azure/static-web-apps-deploy`](https://github.com/Azure/static-web-apps-deploy).
* Para obter mais exemplos de fluxos de trabalho GitHub Action que são implantados em Azure, consulte o repositório [actions-workflow-samples](https://github.com/Azure/actions-workflow-samples).
