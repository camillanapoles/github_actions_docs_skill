---
title: Executar trabalhos em um contêiner
description: Use um contêiner para executar as etapas de um trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-where-workflows-run/run-jobs-in-a-container
captured: '2026-10-13'
section: How tos / Write workflows / Choose where workflows run
---

# Executar trabalhos em um contêiner { #running-jobs-in-a-container }

_Use um contêiner para executar as etapas de um trabalho._

## Visão geral { #overview }

Use `jobs.<job_id>.container` para criar um contêiner e executar as etapas de um trabalho que ainda não especificam um contêiner. Se você tiver etapas que usam ações de script e de contêiner, as ações de contêiner serão executadas como contêineres irmãos na mesma rede e com as mesmas montagens de volume.

Se você não definir um `container`, todas as etapas serão executadas diretamente no host especificado por `runs-on`, a menos que uma etapa se refira a uma ação configurada para ser executada em um contêiner.

!!! note
    O shell padrão para etapas `run` dentro de um contêiner é `sh` em vez de `bash`. Isso pode ser substituído por [`jobs.<job_id>.defaults.run`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_iddefaultsrun) ou por [`jobs.<job_id>.steps[*].shell`](/pt/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell).

### Exemplo: Executar um trabalho dentro de um contêiner { #example-running-a-job-within-a-container }

```yaml copy
name: CI
on:
  push:
    branches: [ main ]
jobs:
  container-test-job:
    runs-on: ubuntu-latest
    container:
      image: node:18
      env:
        NODE_ENV: development
      ports:
        - 80
      volumes:
        - my_docker_volume:/volume_mount
      options: --cpus 1
    steps:
      - name: Check for dockerenv file
        run: (ls /.dockerenv && echo Found dockerenv) || (echo No dockerenv)
```

Quando você especifica apenas uma imagem de contêiner, pode omitir a palavra-chave `image`.

```yaml
jobs:
  container-test-job:
    runs-on: ubuntu-latest
    container: node:18
```

### Instruções e sobreposições do Dockerfile { #dockerfile-instructions-and-overrides }

Um Dockerfile contém instruções e argumentos que definem o conteúdo e o comportamento de inicialização de um contêiner do Docker. Para obter mais informações sobre as instruções às quais o Docker dá suporte, confira [Referência do Dockerfile](https://docs.docker.com/engine/reference/builder/) na documentação do Docker.

Algumas instruções do Docker interagem com GitHub Actions, e o arquivo de metadados de uma ação pode substituir algumas instruções do Docker. Verifique se você está familiarizado com a forma como seu Dockerfile interage com GitHub Actions para evitar comportamentos inesperados.

Para obter informações de referência, confira [Suporte do Dockerfile para GitHub Actions](../../../reference/workflows-and-actions/dockerfile-support.md).

## Definindo a imagem do contêiner { #defining-the-container-image }

Use `jobs.<job_id>.container.image` para definir a imagem do Docker a ser usada como o contêiner para executar a ação. O valor pode ser o nome da imagem do Docker Hub ou um nome de registro.

!!! note
    O Docker Hub normalmente impõe limites de taxa em operações de push e pull, o que afetará os trabalhos em executores auto-hospedados. No entanto, executores hospedados pelo GitHub não estão sujeitos a esses limites com base em um contrato entre o GitHub e o Docker.

## Definindo credenciais para o registro de um contêiner { #defining-credentials-for-a-container-registry }

Se o registro de contêiner da imagem exigir autenticação para efetuar pull da imagem, use `jobs.<job_id>.container.credentials` para definir um `map` do `username` e da `password`. As credenciais são os mesmos valores que você fornecerá ao comando [`docker login`](https://docs.docker.com/engine/reference/commandline/login/).

### Exemplo: Definindo credenciais para o registro de um contêiner { #example-defining-credentials-for-a-container-registry }

```yaml
container:
  image: ghcr.io/owner/image
  credentials:
     username: ${{ github.actor }}
     password: ${{ secrets.github_token }}
```

## Usando variáveis de ambiente com um contêiner { #using-environment-variables-with-a-container }

Use `jobs.<job_id>.container.env` para definir um `map` das variáveis de ambiente no contêiner.

## Expondo portas de rede em um contêiner { #exposing-network-ports-on-a-container }

Use `jobs.<job_id>.container.ports` para definir uma `array` das portas a serem expostas no contêiner.

## Montando volumes em um contêiner { #mounting-volumes-in-a-container }

Use `jobs.<job_id>.container.volumes` para definir uma `array` de volumes para uso do contêiner. É possível usar volumes para compartilhar dados entre serviços ou outras etapas em um trabalho. Você pode especificar volumes de nome Docker, volumes Docker anônimos ou vincular montagens no host.

Para especificar um volume, especifique o caminho de origem e destino:

`<source>:<destinationPath>`.

`<source>` é um nome de volume ou um caminho absoluto no computador host, e `<destinationPath>` é um caminho absoluto no contêiner.

### Exemplo: Montando volumes em um contêiner { #example-mounting-volumes-in-a-container }

```yaml
volumes:
  - my_docker_volume:/volume_mount
  - /data/my_data
  - /source/directory:/destination/directory
```

## Definindo opções de recurso de contêiner { #setting-container-resource-options }

Use `jobs.<job_id>.container.options` para configurar opções adicionais de recurso de contêiner do Docker. Para ver uma lista de opções, confira [Opções de `docker create`](https://docs.docker.com/engine/reference/commandline/create/#options).

!!! warning
    As opções `--network` e `--entrypoint` não têm suporte.
