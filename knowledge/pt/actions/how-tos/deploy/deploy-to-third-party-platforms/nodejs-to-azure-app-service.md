---
title: Implantando Node.js em Azure App Service
description: Saiba como implantar um projeto de Node.js para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/nodejs-to-azure-app-service
captured: '2026-10-13'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantando Node.js em Azure App Service

_Saiba como implantar um projeto de Node.js para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua)._

## Pré-requisitos

Antes de criar seu fluxo de trabalho de GitHub Actions, primeiro você precisa concluir as etapas de configuração a seguir:

1. Criar um Plano do Serviço de Aplicativo do Azure.

   Por exemplo, você pode usar o CLI do Azure para criar um novo plano de App Service:

            ```bash copy
   az appservice plan create \
      --resource-group MY_RESOURCE_GROUP \
      --name MY_APP_SERVICE_PLAN \
      --is-linux
   ```

   No comando acima, substitua `MY_RESOURCE_GROUP` pelo grupo de recursos preexistente do Azure e `MY_APP_SERVICE_PLAN` por um novo nome para o Plano do Serviço de Aplicativo.

   Confira a documentação do Azure para obter mais informações sobre como usar a [CLI do Azure](https://docs.microsoft.com/cli/azure/):

   * Para autenticação, confira [Conectar-se com a CLI do Azure](https://docs.microsoft.com/cli/azure/authenticate-azure-cli).
   * Caso precise criar um grupo de recursos, confira [az group](https://docs.microsoft.com/cli/azure/group?view=azure-cli-latest#az_group_create).

2. Crie um aplicativo Web.

   Por exemplo, você pode usar o Azure CLI para criar um aplicativo Web Azure App Service com um runtime Node.js:

            ```bash copy
   az webapp create \
       --name MY_WEBAPP_NAME \
       --plan MY_APP_SERVICE_PLAN \
       --resource-group MY_RESOURCE_GROUP \
       --runtime "NODE|14-lts"
   ```

   No comando acima, substitua os parâmetros por valores próprios, em que `MY_WEBAPP_NAME` é um novo nome para o aplicativo Web.

3. Configure um perfil de publicação do Azure e crie um segredo `AZURE_WEBAPP_PUBLISH_PROFILE`.

   Gere suas credenciais de implantação do Azure usando um perfil de publicação. Para obter mais informações, confira [Gerar credenciais de implantação](https://docs.microsoft.com/azure/app-service/deploy-github-actions?tabs=applevel#generate-deployment-credentials) na documentação do Azure.

   No seu repositório GitHub, crie um segredo chamado `AZURE_WEBAPP_PUBLISH_PROFILE` que contenha o conteúdo do perfil de publicação. Para obter mais informações sobre como criar segredos, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository).

4. Opcionalmente, configure um ambiente de implantação. Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../configure-and-manage-deployments/manage-environments.md).

## Criar o fluxo de trabalho

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar, testar e implantar o projeto Node.js para Azure App Service quando houver um push para o branch `main`.

Defina `AZURE_WEBAPP_NAME` na chave `env` de fluxo de trabalho como o nome do aplicativo Web que você criou. Se o caminho para o projeto não for a raiz do repositório, altere `AZURE_WEBAPP_PACKAGE_PATH` para o caminho do seu projeto. Se você usar uma versão do Node.js diferente de `10.x`, altere `NODE_VERSION` para a versão usada.

Se você configurou um ambiente de implantação, altere o valor de `environment` para que ele seja o nome do seu ambiente. Se você não tiver configurado um ambiente ou se o fluxo de trabalho estiver em um repositório privado e você não usar o GitHub Enterprise Cloud, exclua a chave `environment`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

on:
  push:
    branches:
      - main

env:
  AZURE_WEBAPP_NAME: MY_WEBAPP_NAME   # set this to your application's name
  AZURE_WEBAPP_PACKAGE_PATH: '.'      # set this to the path to your web app project, defaults to the repository root
  NODE_VERSION: '14.x'                # set this to the node version to use

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v6

    - name: Set up Node.js
      uses: actions/setup-node@v7
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'

    - name: npm install, build, and test
      run: |
        npm install
        npm run build --if-present
        npm run test --if-present
    - name: Upload artifact for deployment job
      uses: actions/upload-artifact@v4
      with:
        name: node-app
        path: .

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'production'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}

    steps:
    - name: Download artifact from build job
      uses: actions/download-artifact@v5
      with:
        name: node-app

    - name: 'Deploy to Azure WebApp'
      id: deploy-to-webapp
      uses: azure/webapps-deploy@85270a1854658d167ab239bce43949edb336fa7c
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: ${{ env.AZURE_WEBAPP_PACKAGE_PATH }}
```

```
## Leitura adicional

* Para o modelo de fluxo de trabalho original, confira [`azure-webapps-node.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/azure-webapps-node.yml) no repositório `starter-workflows` do GitHub Actions.
* A ação usada para implantar o aplicativo Web é a ação oficial Azure [`Azure/webapps-deploy`](https://github.com/Azure/webapps-deploy).
* Para obter mais exemplos de fluxos de trabalho GitHub Action que são implantados em Azure, consulte o repositório [actions-workflow-samples](https://github.com/Azure/actions-workflow-samples).
* O Início rápido [Criar um aplicativo Web Node.js no Azure](https://docs.microsoft.com/azure/app-service/quickstart-nodejs) na documentação do aplicativo Web do Azure demonstra como usar o Visual Studio Code com a [extensão do Serviço de Aplicativo do Azure](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azureappservice).
