---
title: Implantando o PHP em Azure App Service
description: Saiba como implantar um projeto PHP para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/php-to-azure-app-service
captured: '2026-10-11'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantando o PHP em Azure App Service { #deploying-php-to-azure-app-service }

_Saiba como implantar um projeto PHP para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua)._

## Pré-requisitos { #prerequisites }

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

   Por exemplo, você pode usar o Azure CLI para criar um aplicativo Web Azure App Service com um runtime do PHP:

            ```bash copy
   az webapp create \
       --name MY_WEBAPP_NAME \
       --plan MY_APP_SERVICE_PLAN \
       --resource-group MY_RESOURCE_GROUP \
       --runtime "php|7.4"
   ```

   No comando acima, substitua os parâmetros por valores próprios, em que `MY_WEBAPP_NAME` é um novo nome para o aplicativo Web.

3. Configure um perfil de publicação do Azure e crie um segredo `AZURE_WEBAPP_PUBLISH_PROFILE`.

   Gere suas credenciais de implantação do Azure usando um perfil de publicação. Para obter mais informações, confira [Gerar credenciais de implantação](https://docs.microsoft.com/azure/app-service/deploy-github-actions?tabs=applevel#generate-deployment-credentials) na documentação do Azure.

   No seu repositório GitHub, crie um segredo chamado `AZURE_WEBAPP_PUBLISH_PROFILE` que contenha o conteúdo do perfil de publicação. Para obter mais informações sobre como criar segredos, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository).

4. Opcionalmente, configure um ambiente de implantação. Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../configure-and-manage-deployments/manage-environments.md).

## Criar o fluxo de trabalho { #creating-the-workflow }

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar e implantar um projeto PHP para Azure App Service quando há um push para o branch `main`.

Defina `AZURE_WEBAPP_NAME` na chave `env` de fluxo de trabalho como o nome do aplicativo Web que você criou. Se o caminho para seu projeto não for a raiz do repositório, altere `AZURE_WEBAPP_PACKAGE_PATH` para o caminho para o projeto. Se você usar uma versão do PHP diferente de `8.x`, altere `PHP_VERSION` para a versão usada.

Se você configurou um ambiente de implantação, altere o valor de `environment` para que ele seja o nome do seu ambiente. Se você não tiver configurado um ambiente ou se o fluxo de trabalho estiver em um repositório privado e você não usar o GitHub Enterprise Cloud, exclua a chave `environment`.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Build and deploy PHP app to Azure Web App

env:
  AZURE_WEBAPP_NAME: MY_WEBAPP_NAME   # set this to your application's name
  AZURE_WEBAPP_PACKAGE_PATH: '.'      # set this to the path to your web app project, defaults to the repository root
  PHP_VERSION: '8.x'                  # set this to the PHP version to use

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6

      - name: Setup PHP
        uses: shivammathur/setup-php@1f2e3d4c5b6a7f8e9d0c1b2a3e4f5d6c7b8a9e0f
        with:
          php-version: ${{ env.PHP_VERSION }}

      - name: Check if composer.json exists
        id: check_files
        uses: andstor/file-existence-action@2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b
        with:
          files: 'composer.json'

      - name: Get Composer Cache Directory
        id: composer-cache
        if: steps.check_files.outputs.files_exists == 'true'
        run: |
          echo "dir=$(composer config cache-files-dir)" >> $GITHUB_OUTPUT

      - name: Set up dependency caching for faster installs
        uses: actions/cache@v4
        if: steps.check_files.outputs.files_exists == 'true'
        with:
          path: ${{ steps.composer-cache.outputs.dir }}
          key: ${{ runner.os }}-composer-${{ hashFiles('**/composer.lock') }}
          restore-keys: |
            ${{ runner.os }}-composer-

      - name: Run composer install if composer.json exists
        if: steps.check_files.outputs.files_exists == 'true'
        run: composer validate --no-check-publish && composer install --prefer-dist --no-progress

      - name: Upload artifact for deployment job
        uses: actions/upload-artifact@v4
        with:
          name: php-app
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
          name: php-app

      - name: 'Deploy to Azure Web App'
        id: deploy-to-webapp
        uses: azure/webapps-deploy@85270a1854658d167ab239bce43949edb336fa7c
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          package: .
```

## Leitura adicional { #further-reading }

* Para o modelo de fluxo de trabalho original, confira [`azure-webapps-php.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/azure-webapps-php.yml) no repositório `starter-workflows` do GitHub Actions.
* A ação usada para implantar o aplicativo Web é a ação oficial Azure [`Azure/webapps-deploy`](https://github.com/Azure/webapps-deploy).
* Para obter mais exemplos de fluxos de trabalho GitHub Action que são implantados em Azure, consulte o repositório [actions-workflow-samples](https://github.com/Azure/actions-workflow-samples).
