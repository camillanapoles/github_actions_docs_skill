---
title: Implantando o Docker no Serviço de Aplicativo do Azure
description: Saiba como implantar um contêiner do Docker para Serviço de Aplicativo do Azure como parte de seus fluxos de trabalho de CD (implantação contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/docker-to-azure-app-service
captured: '2026-10-11'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantando o Docker no Serviço de Aplicativo do Azure { #deploying-docker-to-azure-app-service }

_Saiba como implantar um contêiner do Docker para Serviço de Aplicativo do Azure como parte de seus fluxos de trabalho de CD (implantação contínua)._

## Pré-requisitos { #prerequisites }

Antes de criar seu GitHub Actions fluxo de trabalho, primeiro você precisará concluir as seguintes etapas de instalação:

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

   Por exemplo, você pode usar o CLI do Azure para criar um aplicativo Web Serviço de Aplicativo do Azure:

            ```shell copy
   az webapp create \
       --name MY_WEBAPP_NAME \
       --plan MY_APP_SERVICE_PLAN \
       --resource-group MY_RESOURCE_GROUP \
       --deployment-container-image-name nginx:latest
   ```

   No comando acima, substitua os parâmetros por valores próprios, em que `MY_WEBAPP_NAME` é um novo nome para o aplicativo Web.

3. Configure um perfil de publicação do Azure e crie um segredo `AZURE_WEBAPP_PUBLISH_PROFILE`.

   Gere suas credenciais de implantação do Azure usando um perfil de publicação. Para obter mais informações, confira [Gerar credenciais de implantação](https://docs.microsoft.com/azure/app-service/deploy-github-actions?tabs=applevel#generate-deployment-credentials) na documentação do Azure.

   No seu repositório GitHub, crie um segredo chamado `AZURE_WEBAPP_PUBLISH_PROFILE` que contenha o conteúdo do perfil de publicação. Para obter mais informações sobre como criar segredos, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository).

4. Defina as credenciais de registro para o seu aplicativo web.

   Crie um personal access token (classic) com os escopos `repo` e `read:packages`. Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

   Defina `DOCKER_REGISTRY_SERVER_URL` como `https://ghcr.io`, `DOCKER_REGISTRY_SERVER_USERNAME` como o nome de usuário do GitHub ou a organização que possui o repositório, e `DOCKER_REGISTRY_SERVER_PASSWORD` como seu personal access token obtido acima. Isso fornecerá credenciais do seu aplicativo web para que ele possa puxar a imagem do contêiner depois que seu fluxo de trabalho fizer push de uma imagem recém-criada para o registro. Você pode fazer isso com o seguinte comando CLI do Azure:

            ```shell
    az webapp config appsettings set \
        --name MY_WEBAPP_NAME \
        --resource-group MY_RESOURCE_GROUP \
        --settings DOCKER_REGISTRY_SERVER_URL=https://ghcr.io DOCKER_REGISTRY_SERVER_USERNAME=MY_REPOSITORY_OWNER DOCKER_REGISTRY_SERVER_PASSWORD=MY_PERSONAL_ACCESS_TOKEN
   ```

5. Opcionalmente, configure um ambiente de implantação. Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../configure-and-manage-deployments/manage-environments.md).

## Criar o fluxo de trabalho { #creating-the-workflow }

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar e implantar um contêiner do Docker para Serviço de Aplicativo do Azure quando há um push para o branch `main`.

Defina `AZURE_WEBAPP_NAME` na chave `env` de fluxo de trabalho como o nome do aplicativo Web que você criou.

Se você configurou um ambiente de implantação, altere o valor de `environment` para que ele seja o nome do seu ambiente. Se você não tiver configurado um ambiente ou se o fluxo de trabalho estiver em um repositório privado e você não usar o GitHub Enterprise Cloud, exclua a chave `environment`.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Build and deploy a container to an Azure Web App

env:
  AZURE_WEBAPP_NAME: MY_WEBAPP_NAME   # set this to your application's name

on:
  push:
    branches:
      - main

permissions:
  contents: 'read'
  packages: 'write'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b

      - name: Log in to GitHub container registry
        uses: docker/login-action@8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Lowercase the repo name
        run: echo "REPO=${GITHUB_REPOSITORY,,}" >>${GITHUB_ENV}

      - name: Build and push container image to registry
        uses: docker/build-push-action@9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f
        with:
          push: true
          tags: ghcr.io/${{ env.REPO }}:${{ github.sha }}
          file: ./Dockerfile

  deploy:
    runs-on: ubuntu-latest

    needs: build

    environment:
      name: 'production'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}

    steps:
      - name: Lowercase the repo name
        run: echo "REPO=${GITHUB_REPOSITORY,,}" >>${GITHUB_ENV}

      - name: Deploy to Azure Web App
        id: deploy-to-webapp
        uses: azure/webapps-deploy@85270a1854658d167ab239bce43949edb336fa7c
        with:
          app-name: ${{ env.AZURE_WEBAPP_NAME }}
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
          images: 'ghcr.io/${{ env.REPO }}:${{ github.sha }}'
```

## Leitura adicional { #further-reading }

* Para o modelo de fluxo de trabalho original, consulte [`azure-container-webapp.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/azure-container-webapp.yml) no GitHub Actions`starter-workflows` repositório.
* A ação usada para implantar o aplicativo Web é a ação oficial Azure [`Azure/webapps-deploy`](https://github.com/Azure/webapps-deploy).
* Para obter mais exemplos de fluxos de trabalho GitHub Action que são implantados em Azure, consulte o repositório [actions-workflow-samples](https://github.com/Azure/actions-workflow-samples).
