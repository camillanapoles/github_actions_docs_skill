---
title: Publicando imagens do Docker
description: Neste tutorial, você aprenderá a publicar imagens do Docker em um registro, como Docker Hub ou GitHub Packages, como parte do fluxo de trabalho de CI (integração contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/publish-packages/publish-docker-images
captured: '2026-10-11'
section: Tutorials / Publish packages
---

# Publicando imagens do Docker

_Neste tutorial, você aprenderá a publicar imagens do Docker em um registro, como Docker Hub ou GitHub Packages, como parte do fluxo de trabalho de CI (integração contínua)._

## Introdução

Este guia mostra como criar um fluxo de trabalho que executa um build do Docker e, em seguida, publica imagens do Docker para Docker Hub ou GitHub Packages. Com um único fluxo de trabalho, você pode publicar imagens em um único registro ou em vários registros.

!!! note
    Se você quiser fazer push para outro registro Docker de terceiros, o exemplo na seção [Publicando imagens no GitHub Packages](#publishing-images-to-github-packages) poderá servir como um bom modelo.

## Pré-requisitos

Recomendamos que você tenha um entendimento básico das opções de configuração do fluxo de trabalho e de como criar um arquivo do fluxo de trabalho. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Você também pode achar útil ter um entendimento básico do seguinte:

* [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
* [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md)
* [Trabalhando com o registro de contêiner](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

## Sobre a configuração da imagem

Este guia pressupõe que você tenha uma definição completa para uma imagem do Docker armazenada em um GitHub repositório. Por exemplo, seu repositório precisa conter um *Dockerfile* e todos os outros arquivos necessários para executar um build do Docker para criar uma imagem.

Você pode usar chaves de anotação pré-definidas para adicionar metadados, incluindo uma descrição, uma licença e um repositório de origem à imagem de contêiner. Para obter mais informações, consulte [Trabalhando com o registro de contêiner](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-container-registry#labelling-container-images).

Neste guia, usaremos a ação `build-push-action` do Docker para compilar a imagem do Docker e efetuar push dela para um ou mais registros do Docker. Para obter mais informações, confira [`build-push-action`](https://github.com/marketplace/actions/build-and-push-docker-images).

## Publicando imagens no Docker Hub

!!! note
    O Docker Hub normalmente impõe limites de taxa em operações de push e pull, o que afetará os trabalhos em executores auto-hospedados. No entanto, executores hospedados pelo GitHub não estão sujeitos a esses limites com base em um contrato entre o GitHub e o Docker.

Você pode acionar um fluxo de trabalho para publicar sua imagem sempre que criar uma nova versão no GitHub. O fluxo de trabalho no exemplo abaixo é executado quando o evento `release` é disparado com o tipo de atividade `published`.

No exemplo de fluxo de trabalho abaixo, usamos as ações do Docker `login-action` e `build-push-action` para criar a imagem do Docker e, se o build for bem-sucedido, efetuar push da imagem compilada para Docker Hub.

Para enviar por push para Docker Hub, você precisará ter uma conta Docker Hub e ter um repositório Docker Hub criado. Para obter mais informações, consulte [Envio de uma imagem de contêiner do Docker para o Docker Hub](https://docs.docker.com/docker-hub/quickstart/#step-3-build-and-push-an-image-to-docker-hub) na documentação do Docker.

As opções de `login-action` necessárias para Docker Hub são:

* `username` e `password`: este é seu nome de usuário e senha Docker Hub. Recomendamos armazenar seu nome de usuário e senha Docker Hub como segredos para que eles não sejam expostos no arquivo de fluxo de trabalho. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

A opção `metadata-action` necessária para Docker Hub é:

* `images`: o namespace e o nome da imagem do Docker que você está compilando/enviando por push para o Docker Hub.

As opções de `build-push-action` necessárias para Docker Hub são:

* `tags`: a marca da nova imagem no formato `DOCKER-HUB-NAMESPACE/DOCKER-HUB-REPOSITORY:VERSION`. Você pode definir uma única tag, conforme mostrado abaixo, ou especificar várias tags em uma lista.
* `push`: se isso for definido como `true`, a imagem será enviada por push para o registro se for compilada com sucesso.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Publish Docker image

on:
  release:
    types: [published]

jobs:
  push_to_registry:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
      attestations: write
      id-token: write
    steps:
      - name: Check out the repo
        uses: actions/checkout@v6

      - name: Log in to Docker Hub
        uses: docker/login-action@f4ef78c080cd8ba55a85445d5b36e214a81df20a
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
        with:
          images: my-docker-hub-namespace/my-docker-hub-repository

      - name: Build and push Docker image
        id: push
        uses: docker/build-push-action@3b5e8027fcad23fda98b2e3ac259d8d67585f671
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      - name: Generate artifact attestation
        uses: actions/attest@v4
        with:
          subject-name: index.docker.io/my-docker-hub-namespace/my-docker-hub-repository
          subject-digest: ${{ steps.push.outputs.digest }}
          push-to-registry: true
```

O fluxo de trabalho acima verifica o repositório do GitHub usa o `login-action` para registrar em log no Registro e, em seguida, usa a ação do `build-push-action` para: criar uma imagem do Docker baseada no `Dockerfile` do repositório; envie por push a imagem par o Docker Hub e aplique a marcação à imagem.

Na última etapa, gera um atestado de artefato para a imagem, o que aumenta a segurança da cadeia de fornecedores. Para saber mais, confira [Usar atestados de artefatos para estabelecer a procedência de compilações](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md).

## Publicando imagens para GitHub Packages

Você pode acionar um fluxo de trabalho para publicar sua imagem sempre que criar uma nova versão no GitHub. O fluxo de trabalho no exemplo abaixo é executado quando uma alteração é enviada por push para o branch `release`.

No fluxo de trabalho de exemplo abaixo, usamos as ações Docker `login-action`, , `metadata-action`,  e `build-push-action` para criar a imagem do Docker e, se o build for bem-sucedido, enviar a imagem construída para GitHub Packages.

As opções `login-action` necessárias para GitHub Packages são:

* `registry`: deve ser definido como `ghcr.io`.
* `username`: você pode usar o `${{ github.actor }}` contexto para usar automaticamente o nome de usuário do usuário que disparou a execução do fluxo de trabalho. Para saber mais, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md#github-context).
* `password`: use o segredo `GITHUB_TOKEN` gerado automaticamente para a senha. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md).

A `metadata-action` opção necessária para GitHub Packages é:

* `images`: o namespace e o nome da imagem do Docker que está sendo construída.

As opções necessárias para `build-push-action` são GitHub Packages:

* `context`: define o contexto do build como o conjunto de arquivos localizado no caminho especificado.
* `push`: se definido como `true`, a imagem será enviada por push para o Registro se for criada com êxito.
* `tags` e `labels`: eles são preenchidos pela saída de `metadata-action`.

!!! note
    * Esse fluxo de trabalho usa ações que não são certificadas por GitHub. Elas são fornecidas por terceiros e regidar por termos de serviço, política de privacidade e documentação de suporte separados.
    * GitHub recomenda fixar ações em um SHA de confirmação. Para obter uma versão mais recente, você precisará atualizar o SHA. Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

```yaml annotate copy
#
name: Create and publish a Docker image

# Configures this workflow to run every time a change is pushed to the branch called `release`.
on:
  push:
    branches: ['release']

# Defines two custom environment variables for the workflow. These are used for the Container registry domain, and a name for the Docker image that this workflow builds.
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

# There is a single job in this workflow. It's configured to run on the latest available version of Ubuntu.
jobs:
  build-and-push-image:
    runs-on: ubuntu-latest
    # Sets the permissions granted to the `GITHUB_TOKEN` for the actions in this job.
    permissions:
      contents: read
      packages: write
      attestations: write
      id-token: write
      #
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      # Uses the `docker/login-action` action to log in to the Container registry registry using the account and password that will publish the packages. Once published, the packages are scoped to the account defined here.
      - name: Log in to the Container registry
        uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      # This step uses [docker/metadata-action](https://github.com/docker/metadata-action#about) to extract tags and labels that will be applied to the specified image. The `id` "meta" allows the output of this step to be referenced in a subsequent step. The `images` value provides the base name for the tags and labels.
      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
      # This step uses the `docker/build-push-action` action to build the image, based on your repository's `Dockerfile`. If the build succeeds, it pushes the image to GitHub Packages.
      # It uses the `context` parameter to define the build's context as the set of files located in the specified path. For more information, see [Usage](https://github.com/docker/build-push-action#usage) in the README of the `docker/build-push-action` repository.
      # It uses the `tags` and `labels` parameters to tag and label the image with the output from the "meta" step.
      - name: Build and push Docker image
        id: push
        uses: docker/build-push-action@f2a1d5e99d037542a71f64918e516c093c6f3fc4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

      # This step generates an artifact attestation for the image, which is an unforgeable statement about where and how it was built. It increases supply chain security for people who consume the image. For more information, see [Using artifact attestations to establish provenance for builds](https://docs.github.com/pt/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds).
      - name: Generate artifact attestation
        uses: actions/attest@v4
        with:
          subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME}}
          subject-digest: ${{ steps.push.outputs.digest }}
          push-to-registry: true

```

O fluxo de trabalho acima é acionado por um push para o branch da "versão". Ele verifica o repositório GitHub e usa o `login-action` para fazer logon no Container registry. Em seguida, extrai etiquetas e tags para a imagem do Docker. Por fim, ele usa a ação `build-push-action` para criar a imagem e publicá-la no Container registry.

## Publicando imagens em Docker Hub e GitHub Packages

Em um fluxo de trabalho individual, você pode publicar sua imagem do Docker em vários registros usando as ações `login-action` e `build-push-action` para cada registro.

O fluxo de trabalho de exemplo a seguir usa as etapas das seções anteriores (Publicando imagens no [Docker Hub](#publishing-images-to-docker-hub) e Publicando imagens em [GitHub Packages](#publishing-images-to-github-packages)) para criar um único fluxo de trabalho que faz push para ambos os registros.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Publish Docker image

on:
  release:
    types: [published]

jobs:
  push_to_registries:
    name: Push Docker image to multiple registries
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    steps:
      - name: Check out the repo
        uses: actions/checkout@v6

      - name: Log in to Docker Hub
        uses: docker/login-action@f4ef78c080cd8ba55a85445d5b36e214a81df20a
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Log in to the Container registry
        uses: docker/login-action@65b78e6e13532edd9afa3aa52ac7964289d1a9c1
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata (tags, labels) for Docker
        id: meta
        uses: docker/metadata-action@9ec57ed1fcdbf14dcef7dfbe97b2010124a938b7
        with:
          images: |
            my-docker-hub-namespace/my-docker-hub-repository
            ghcr.io/${{ github.repository }}

      - name: Build and push Docker images
        id: push
        uses: docker/build-push-action@3b5e8027fcad23fda98b2e3ac259d8d67585f671
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

O fluxo de trabalho acima faz check-out do repositório do GitHub repository, usa `login-action` duas vezes para fazer logon nos dois registros e gera marcas e rótulos com a ação `metadata-action`.
Em seguida, a ação `build-push-action` cria e envia por push a imagem do Docker para o Docker Hub e o Container registry.

!!! note
    Ao realizar o push para múltiplos registries:

    * Os resumos de imagem podem ser diferentes entre os registros, dificultando a verificação de atestado.
    * Para manter um resumo consistente e permitir que um único atestado verifique todas as cópias, envie por push para um registro primeiro e use uma ferramenta como [`crane copy`](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_copy.md) para replicar a imagem em outros locais.
    * Se você optar por compilar e enviar para cada repositório separadamente, deverá gerar um atestado distinto para cada um, para garantir que seus artefatos permaneçam verificáveis.

## Atividade prática

Pratique a publicação de imagens Docker com o exercício [Publicação de Imagens Docker](https://github.com/skills/publish-docker-images)GitHub Skills.

Neste exercício, você aprenderá a:

* Autentique-se em GitHub Packages usando o `GITHUB_TOKEN`.
* Criar e publicar imagens de contêiner no Container registry (`ghcr.io`).
* Use ações oficiais do Docker, como `docker/login-action`, `docker/build-push-action`e `docker/setup-buildx-action`.
* Gere marcações automaticamente com `docker/metadata-action` baseado em ramificações, pull requests e versões.
* Crie funcionalidades, pull requests e versões com o versionamento de contêiner apropriado.
