---
title: Implantar no Google Kubernetes Engine
description: Saiba como implantar um projeto no Google Kubernetes Engine (GKE) como parte de um fluxo de trabalho de CD (implantação contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/google-kubernetes-engine
captured: '2026-10-13'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantar no Google Kubernetes Engine { #deploying-to-google-kubernetes-engine }

_Saiba como implantar um projeto no Google Kubernetes Engine (GKE) como parte de um fluxo de trabalho de CD (implantação contínua)._

## Pré-requisitos { #prerequisites }

Antes de prosseguir com a criação do fluxo de trabalho, você precisará concluir as etapas a seguir para seu projeto do Kubernetes. Este guia pressupõe que a raiz do seu projeto já tenha um `Dockerfile` e um arquivo de configuração de Implantação do Kubernetes.

### Criando um cluster do GKE { #creating-a-gke-cluster }

Para criar o cluster do GKE, primeiro, você precisará se autenticar usando a CLI do `gcloud`. Para obter mais informações sobre esta etapa, veja os artigos a seguir:

* [`gcloud auth login`](https://cloud.google.com/sdk/gcloud/reference/auth/login)
* [
  `gcloud` CLI](https://cloud.google.com/sdk/gcloud/reference)
* [
  `gcloud` CLI e Cloud SDK](https://cloud.google.com/sdk/gcloud#the_gcloud_cli_and_cloud_sdk)

Por exemplo:

```shell copy
$ gcloud container clusters create $GKE_CLUSTER \
    --project=$GKE_PROJECT \
    --zone=$GKE_ZONE
```

### Habilitar as APIs { #enabling-the-apis }

Habilite as APIs do Motor Kubernetes e do Registro de Contêineres. Por exemplo:

```shell copy
$ gcloud services enable \
    containerregistry.googleapis.com \
    container.googleapis.com
```

### Configurar uma conta de serviço e armazenar as suas credenciais { #configuring-a-service-account-and-storing-its-credentials }

Este procedimento demonstra como criar a conta de serviço para sua integração com o GKE. Ele explica como criar a conta, adicionar funções a ela, recuperar suas chaves e armazená-las como um segredo de repositório criptografado codificado em base64 chamado `GKE_SA_KEY`.

1. Crie uma nova conta de serviço:

            ```shell copy
   gcloud iam service-accounts create $SA_NAME
            ```

2. Recupere o endereço de email da conta de serviço que você acabou de criar:

            ```shell copy
   gcloud iam service-accounts list
            ```

3. Adicionar funções à conta de serviço.

!!! note

   > Aplique funções mais restritivas de acordo com seus requisitos.

            ```shell copy
   gcloud projects add-iam-policy-binding $GKE_PROJECT \
     --member=serviceAccount:$SA_EMAIL \
     --role=roles/container.admin
   gcloud projects add-iam-policy-binding $GKE_PROJECT \
     --member=serviceAccount:$SA_EMAIL \
     --role=roles/storage.admin
   gcloud projects add-iam-policy-binding $GKE_PROJECT \
     --member=serviceAccount:$SA_EMAIL \
     --role=roles/container.clusterViewer
            ```

4. Faça o download do arquivo chave do JSON para a conta de serviço:

            ```shell copy
   gcloud iam service-accounts keys create key.json --iam-account=$SA_EMAIL
            ```

5. Armazene a chave da conta de serviço como um segredo chamado `GKE_SA_KEY`:

            ```shell copy
   export GKE_SA_KEY=$(cat key.json | base64)
            ```

   Para saber mais sobre como armazenar um segredo, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md).

### Armazenando o nome do seu projeto { #storing-your-project-name }

Armazene o nome do projeto como um segredo chamado `GKE_PROJECT`. Para saber mais sobre como armazenar um segredo, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md).

### (Opcional) Configurar kustomize { #optional-configuring-kustomize }

Kustomize é uma ferramenta opcional usada para gerenciar especificações do YAML. Depois que você criar um arquivo `kustomization`, o fluxo de trabalho abaixo poderá ser usado para definir dinamicamente os campos da imagem e encaminhar o resultado para `kubectl`. Para obter mais informações, confira [Uso do Kustomize](https://github.com/kubernetes-sigs/kustomize#usage).

### (Opcional) Configure um ambiente de implantação { #optional-configure-a-deployment-environment }

Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../configure-and-manage-deployments/manage-environments.md).

## Criar o fluxo de trabalho { #creating-the-workflow }

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho a seguir mostra como criar uma imagem de contêiner e enviá-la ao GCR. Em seguida, ele usa as ferramentas do Kubernetes (como `kubectl` e `kustomize`) para baixar a imagem para a implantação no cluster.

Na chave `env`, altere o valor de `GKE_CLUSTER` para o nome do seu cluster, `GKE_ZONE` para sua zona de cluster, `DEPLOYMENT_NAME` para o nome da sua implementação e `IMAGE` para o nome da sua imagem.

Se você configurou um ambiente de implantação, altere o valor de `environment` para que ele seja o nome do seu ambiente. Se você não tiver configurado um ambiente ou se o fluxo de trabalho estiver em um repositório privado e você não usar o GitHub Enterprise Cloud, exclua a chave `environment`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub. { #this-workflow-uses-actions-that-are-not-certified-by-github }
# São fornecidas por terceiros e regidas por { #they-are-provided-by-a-third-party-and-are-governed-by }
# termos de serviço, política de privacidade e suporte separados { #separate-terms-of-service-privacy-policy-and-support }
# online. { #documentation }

# O GitHub recomenda fixar ações em um SHA de commit. { #github-recommends-pinning-actions-to-a-commit-sha }
# Para obter uma versão mais recente, você precisará atualizar o SHA. { #to-get-a-newer-version-you-will-need-to-update-the-sha }
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso. { #you-can-also-reference-a-tag-or-branch-but-the-action-may-change-without-warning }

name: Build and Deploy to GKE

on:
  push:
    branches:
      - main

env:
  PROJECT_ID: ${{ secrets.GKE_PROJECT }}
  GKE_CLUSTER: cluster-1    # Add your cluster name here.
  GKE_ZONE: us-central1-c   # Add your cluster zone here.
  DEPLOYMENT_NAME: gke-test # Add your deployment name here.
  IMAGE: static-site

jobs:
  setup-build-publish-deploy:
    name: Setup, Build, Publish, and Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout
      uses: actions/checkout@v6

    # Setup gcloud CLI
    - uses: google-github-actions/setup-gcloud@1bee7de035d65ec5da40a31f8589e240eba8fde5
      with:
        service_account_key: ${{ secrets.GKE_SA_KEY }}
        project_id: ${{ secrets.GKE_PROJECT }}

    # Configure Docker to use the gcloud command-line tool as a credential
    # helper for authentication
    - run: |-
        gcloud --quiet auth configure-docker

    # Get the GKE credentials so we can deploy to the cluster
    - uses: google-github-actions/get-gke-credentials@db150f2cc60d1716e61922b832eae71d2a45938f
      with:
        cluster_name: ${{ env.GKE_CLUSTER }}
        location: ${{ env.GKE_ZONE }}
        credentials: ${{ secrets.GKE_SA_KEY }}

    # Build the Docker image
    - name: Build
      run: |-
        docker build \
          --tag "gcr.io/$PROJECT_ID/$IMAGE:$GITHUB_SHA" \
          --build-arg GITHUB_SHA="$GITHUB_SHA" \
          --build-arg GITHUB_REF="$GITHUB_REF" \
          .

    # Push the Docker image to Google Container Registry
    - name: Publish
      run: |-
        docker push "gcr.io/$PROJECT_ID/$IMAGE:$GITHUB_SHA"

    # Set up kustomize
    - name: Set up Kustomize
      run: |-
        curl -sfLo kustomize https://github.com/kubernetes-sigs/kustomize/releases/download/v3.1.0/kustomize_3.1.0_linux_amd64
        chmod u+x ./kustomize

    # Deploy the Docker image to the GKE cluster
    - name: Deploy
      run: |-
        ./kustomize edit set image gcr.io/PROJECT_ID/IMAGE:TAG=gcr.io/$PROJECT_ID/$IMAGE:$GITHUB_SHA
        ./kustomize build . | kubectl apply -f -
        kubectl rollout status deployment/$DEPLOYMENT_NAME
        kubectl get services -o wide
```

```
## Leitura adicional { #further-reading }

Para mais informações sobre as ferramentas usadas nesses exemplos, consulte a documentação a seguir:

* Para ver o modelo completo do fluxo de trabalho, confira o [Fluxo de Trabalho "Construção e Implantação no GKE"](https://github.com/actions/starter-workflows/blob/main/deployments/google.yml).
* O mecanismo de personalização YAML do Kubernetes: [Kustomize](https://kustomize.io/).
* [Como implantar um aplicativo Web conteinerizado](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app) na documentação do Mecanismo de Kubernetes do Google.
