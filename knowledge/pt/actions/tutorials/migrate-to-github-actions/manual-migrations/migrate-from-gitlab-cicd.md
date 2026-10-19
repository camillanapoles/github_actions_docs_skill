---
title: Migrando de CI/CD do GitLab para GitHub Actions
description: GitHub Actions e o GITLab CI/CD compartilham várias semelhanças de configuração, o que torna a migração para GitHub Actions relativamente simples.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-gitlab-cicd
captured: '2026-10-19'
section: Tutorials / Migrate to github actions / Manual migrations
---

# Migrando de CI/CD do GitLab para GitHub Actions

_GitHub Actions e o GITLab CI/CD compartilham várias semelhanças de configuração, o que torna a migração para GitHub Actions relativamente simples._

## Introdução

O GitLab CI/CD e GitHub Actions ambos permitem criar fluxos de trabalho que criam, testam, publicam, liberam e implantam código automaticamente. GitLab CI/CD e GitHub Actions compartilham algumas semelhanças na configuração do fluxo de trabalho:

* Os arquivos de configuração do fluxo de trabalho são gravados YAML e armazenados no repositório do código.
* Os fluxos de trabalho incluem um ou mais trabalhos.
* Os trabalhos incluem uma ou mais etapas ou comandos individuais.
* Os trabalhos podem ser executados em máquinas gerenciadas ou auto-hospedadas.

Há algumas diferenças e este guia mostrará as diferenças importantes para que você possa migrar seu fluxo de trabalho para GitHub Actions.

## Trabalhos

As tarefas no CI/CD do GitLab são muito parecidas com as tarefas em GitHub Actions. Em ambos os sistemas, os trabalhos têm as características a seguir:

* Os trabalhos contêm uma série de etapas ou scripts executados sequencialmente.
* Os trabalhos podem ser executados em máquinas separadas ou em contêineres separados.
* Por padrão, os trabalhos são executados em paralelo, mas podem ser configurados para serem executados sequencialmente.

Você pode executar um script ou um comando de shell em um trabalho. Na CI/CD do GitLab, as etapas de script são especificadas por meio da chave `script`. Em GitHub Actions, todos os scripts são especificados usando a `run` chave.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para trabalhos

```yaml
job1:
  variables:
    GIT_CHECKOUT: "true"
  script:
    - echo "Run your script here"
```

### Sintaxe do GitHub Actions para trabalhos

```yaml
jobs:
  job1:
    steps:
      - uses: actions/checkout@v6
      - run: echo "Run your script here"
```

## Executores

Os executores são máquinas nas quais os trabalhos são executados. Tanto o CI/CD do GitLab quanto o GitHub Actions oferecem opções gerenciadas e auto-hospedadas de executores. No GitLab CI/CD, `tags` são usados para executar jobs em diferentes plataformas, enquanto em GitHub Actions isso é feito com a chave `runs-on`.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para executores

```yaml
windows_job:
  tags:
    - windows
  script:
    - echo Hello, %USERNAME%!

linux_job:
  tags:
    - linux
  script:
    - echo "Hello, $USER!"
```

### Sintaxe do GitHub Actions para executores

```yaml
windows_job:
  runs-on: windows-latest
  steps:
    - run: echo Hello, %USERNAME%!

linux_job:
  runs-on: ubuntu-latest
  steps:
    - run: echo "Hello, $USER!"
```

Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on).

## Imagens do Docker

Tanto o GitLab CI/CD quanto GitHub Actions oferecem suporte à execução de tarefas em uma imagem Docker. No GitLab CI/CD, as imagens do Docker são definidas com a chave `image`, enquanto em GitHub Actions isso é feito com a chave `container`.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para imagens do Docker

```yaml
my_job:
  image: node:20-bookworm-slim
```

### GitHub Actions sintaxe para imagens do Docker

```yaml
jobs:
  my_job:
    container: node:20-bookworm-slim
```

Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontainer).

## Condição e sintaxe de expressão

A CI/CD do GitLab usa `rules` para determinar se um trabalho será executado para uma condição específica.
GitHub Actions usa a `if` palavra-chave para impedir que um trabalho seja executado, a menos que uma condição seja atendida.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para condições e expressões

```yaml
deploy_prod:
  stage: deploy
  script:
    - echo "Deploy to production server"
  rules:
    - if: '$CI_COMMIT_BRANCH == "master"'
```

### GitHub Actions sintaxe para condições e expressões

```yaml
jobs:
  deploy_prod:
    if: contains( github.ref, 'master')
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploy to production server"
```

Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md).

## Dependências entre trabalhos

Tanto o CI/CD do GitLab quanto GitHub Actions permitem que você defina dependências para um job. Em ambos os sistemas, os trabalhos são executados em paralelo por padrão, mas as dependências entre trabalhos em GitHub Actions podem ser especificadas explicitamente com a chave `needs`. A CI/CD do GitLab também tem um conceito de `stages`, em que os trabalhos em uma fase são executados simultaneamente, mas a próxima fase será iniciada quando todos os trabalhos da fase anterior tiverem sido concluídos. Você pode reproduzir este cenário em GitHub Actions com a tecla `needs`.

Abaixo, há um exemplo da sintaxe para cada sistema. Os fluxos de trabalho começam com dois trabalhos chamados `build_a` e `build_b` em execução em paralelo e, quando esses trabalhos forem concluídos, outro trabalho chamado `test_ab` será executado. Por fim, quando `test_ab` é concluído, o trabalho `deploy_ab` será executado.

### Sintaxe de CI/CD do GitLab para dependências entre trabalhos

```yaml
stages:
  - build
  - test
  - deploy

build_a:
  stage: build
  script:
    - echo "This job will run first."

build_b:
  stage: build
  script:
    - echo "This job will run first, in parallel with build_a."

test_ab:
  stage: test
  script:
    - echo "This job will run after build_a and build_b have finished."

deploy_ab:
  stage: deploy
  script:
    - echo "This job will run after test_ab is complete"
```

### GitHub Actions sintaxe para dependências entre trabalhos

```yaml
jobs:
  build_a:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This job will be run first."

  build_b:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This job will be run first, in parallel with build_a"

  test_ab:
    runs-on: ubuntu-latest
    needs: [build_a,build_b]
    steps:
      - run: echo "This job will run after build_a and build_b have finished"

  deploy_ab:
    runs-on: ubuntu-latest
    needs: [test_ab]
    steps:
      - run: echo "This job will run after test_ab is complete"
```

Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds).

## Agendar fluxos de trabalho

Tanto o CI/CD do GitLab quanto GitHub Actions permitem que você execute fluxos de trabalho em um intervalo específico. No GitLab CI/CD, os agendamentos de pipeline são configurados pela interface do usuário, enquanto em GitHub Actions você pode acionar um fluxo de trabalho em um intervalo programado com a chave "on".

Para saber mais, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).

## Variáveis e segredos

O GitLab CI/CD e GitHub Actions permitem definir variáveis no arquivo de configuração do pipeline ou do fluxo de trabalho e criar segredos usando a interface do usuário do GitLab ou do GitHub.

Para saber mais, confira [Armazenar informações em variáveis](../../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md) e [Segredos](../../../concepts/security/secrets.md).

## Armazenamento em cache

O GitLab CI/CD e GitHub Actions fornece um método no arquivo de configuração para armazenar em cache manualmente arquivos de fluxo de trabalho.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para cacheamento

```yaml
image: node:latest

cache:
  key: $CI_COMMIT_REF_SLUG
  paths:
    - .npm/

before_script:
  - npm ci --cache .npm --prefer-offline

test_async:
  script:
    - node ./specs/start.js ./specs/async.spec.js
```

### GitHub Actions sintaxe para armazenamento em cache

```yaml
jobs:
  test_async:
    runs-on: ubuntu-latest
    steps:
    - name: Cache node modules
      uses: actions/cache@v4
      with:
        path: ~/.npm
        key: v1-npm-deps-${{ hashFiles('**/package-lock.json') }}
        restore-keys: v1-npm-deps-
```

## Artifacts

Tanto o GitLab CI/CD quanto GitHub Actions podem fazer upload de arquivos e diretórios criados por um job como artefatos. No GitHub Actions, os artefatos podem ser usados para fazer persistir dados em vários trabalhos.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para artefatos

```yaml
script:
artifacts:
  paths:
    - math-homework.txt
```

### GitHub Actions sintaxe para artefatos

```yaml
- name: Upload math result for job 1
  uses: actions/upload-artifact@v4
  with:
    name: homework
    path: math-homework.txt
```

Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../store-and-share-data.md).

## Bancos de dados e contêineres de serviço

Ambos os sistemas permitem que você inclua contêineres adicionais para bases de dados, memorização ou outras dependências.

No GitLab CI/CD, um contêiner para o trabalho é especificado com a `image` chave, enquanto GitHub Actions usa a `container` chave. Nos dois sistemas, contêineres de serviço adicionais são especificados com a chave `services`.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe de CI/CD do GitLab para bancos de dados e contêineres de serviço

```yaml
container-job:
  variables:
    POSTGRES_PASSWORD: postgres
    # The hostname used to communicate with the
    # PostgreSQL service container
    POSTGRES_HOST: postgres
    # The default PostgreSQL port
    POSTGRES_PORT: 5432
  image: node:20-bookworm-slim
  services:
    - postgres
  script:
    # Performs a clean installation of all dependencies
    # in the `package.json` file
    - npm ci
    # Runs a script that creates a PostgreSQL client,
    # populates the client with data, and retrieves data
    - node client.js
  tags:
    - docker
```

### GitHub Actions sintaxe para bancos de dados e contêineres de serviço

```yaml
jobs:
  container-job:
    runs-on: ubuntu-latest
    container: node:20-bookworm-slim

    services:
      postgres:
        image: postgres
        env:
          POSTGRES_PASSWORD: postgres

    steps:
      - name: Check out repository code
        uses: actions/checkout@v6

      # Performs a clean installation of all dependencies
      # in the `package.json` file
      - name: Install dependencies
        run: npm ci

      - name: Connect to PostgreSQL
        # Runs a script that creates a PostgreSQL client,
        # populates the client with data, and retrieves data
        run: node client.js
        env:
          # The hostname used to communicate with the
          # PostgreSQL service container
          POSTGRES_HOST: postgres
          # The default PostgreSQL port
          POSTGRES_PORT: 5432
```

Para saber mais, confira [Comunicar-se com os contêineres de serviço do Docker](../../use-containerized-services/use-docker-service-containers.md).
