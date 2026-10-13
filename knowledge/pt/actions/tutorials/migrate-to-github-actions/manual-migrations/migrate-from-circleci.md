---
title: Migrando do CircleCI para o GitHub Actions
description: GitHub Actions e CircleCI compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-circleci
captured: '2026-10-13'
section: Tutorials / Migrate to github actions / Manual migrations
---

# Migrando do CircleCI para o GitHub Actions

_GitHub Actions e CircleCI compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples._

## Introdução

O CircleCI e GitHub Actions ambos permitem que você crie fluxos de trabalho que compilem, testem, publiquem, liberem e implantem código automaticamente. CircleCI e GitHub Actions compartilham algumas semelhanças na configuração do fluxo de trabalho:

* Os arquivos de configuração do fluxo de trabalho são gravados no YAML e armazenados no repositório.
* Os fluxos de trabalho incluem um ou mais trabalhos.
* Os trabalhos incluem uma ou mais etapas ou comandos individuais.
* É possível reutilizar e compartilhar novamente etapas ou tarefas com a comunidade.

Para saber mais, confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md).

## Principais diferenças

Ao fazer a migração do CircleCI, considere as seguintes diferenças:

* O paralelismo do teste automático do CircleCI agrupa automaticamente os testes de acordo com regras especificadas pelo usuário ou com informações históricas de temporização. Essa funcionalidade não está integrada ao GitHub Actions.
* As ações que são executadas em contêineres Docker são sensíveis a problemas de permissões, uma vez que os contêineres têm um mapeamento diferente de usuários. Você pode evitar muitos desses problemas não usando a instrução `USER` no *Dockerfile*. Para obter mais informações sobre o sistema de arquivos do Docker nos executores hospedados do GitHub, consulte [Referência de executores hospedados pelo GitHub](../../../reference/runners/github-hosted-runners.md#docker-container-filesystem).

## Migrar fluxos de trabalho e tarefas

O CircleCI define `workflows` no arquivo *config.yml*, que permite configurar mais de um fluxo de trabalho.
GitHub requer um arquivo de fluxo de trabalho por fluxo de trabalho e, como consequência, não exige que você declare `workflows`. Será necessário criar um arquivo de fluxo de trabalho para cada fluxo de trabalho configurado em *config.yml*.

Tanto o CircleCI quanto GitHub Actions configuram `jobs` no arquivo de configuração usando sintaxe semelhante. Se você configurar dependências entre jobs usando `requires` em seu fluxo de trabalho do CircleCI, poderá usar a sintaxe equivalente GitHub Actions`needs`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds).

## Migrar orbes para ações

O CircleCI e GitHub Actions fornece um mecanismo para reutilizar e compartilhar tarefas em um fluxo de trabalho. O CircleCI usa um conceito chamado orbs, escrito em YAML, para fornecer tarefas que as pessoas podem reutilizar em um fluxo de trabalho.
GitHub Actions tem componentes reutilizáveis poderosos e flexíveis chamados ações, que você cria com arquivos JavaScript ou imagens do Docker. Você pode criar ações escrevendo código personalizado que interage com seu repositório da maneira que desejar, incluindo a integração com GitHubAPIs e qualquer API de terceiros publicamente disponível. Por exemplo, uma ação pode publicar módulos npm, enviar alertas de SMS quando problemas urgentes surgirem ou implantar o código pronto para produção. Para saber mais, confira [Reutilização de automações](../../../how-tos/reuse-automations.md).

O CircleCI pode reutilizar partes dos fluxos de trabalho com âncoras e aliases YAML.
GitHub Actions dá suporte a âncoras YAML e aliases para reutilização e também fornece matrizes para executar trabalhos com configurações diferentes. Para obter mais informações sobre matrizes, confira [Executando variações de tarefas em um workflow](../../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md).

## Usar imagens do Docker

Tanto o CircleCI quanto o GitHub Actions oferecem suporte à execução de etapas em uma imagem Docker.

O CircleCI fornece um conjunto de imagens pré-construídas com dependências comuns. Essas imagens têm o `USER` definido como `circleci`, o que faz com que as permissões entrem em conflito com GitHub Actions.

Recomendamos que você deixe de usar as imagens pré-configuradas do CircleCI ao migrar para GitHub Actions. Em muitos casos, você pode usar ações para instalar as dependências adicionais de que você precisa.

Para saber mais sobre o sistema de arquivos do Docker, confira [Referência de executores hospedados pelo GitHub](../../../reference/runners/github-hosted-runners.md#docker-container-filesystem).

Para obter mais informações sobre as ferramentas e os pacotes disponíveis nas imagens de executores hospedados no GitHub, consulte [Executores hospedados no GitHub](../../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Usar variáveis e segredos

CircleCI e GitHub Actions oferecem suporte à definição de variáveis no arquivo de configuração e à criação de segredos usando a interface do usuário do CircleCI ou de GitHub.

Para saber mais, confira [Referência de variáveis](../../../reference/workflows-and-actions/variables.md#default-environment-variables) e [Usar segredos em ações do GitHub](../../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Armazenamento em cache

CircleCI e GitHub Actions fornecem um método para armazenar arquivos em cache manualmente no arquivo de configuração.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe do CircleCI para cache

```yaml
- restore_cache:
    keys:
      - v1-npm-deps-{{ checksum "package-lock.json" }}
      - v1-npm-deps-
```

### A sintaxe do GitHub Actions para cache

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: v1-npm-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: v1-npm-deps-
```

O GitHub Actions não tem um equivalente ao cache de camadas do Docker (ou DLC) do CircleCI.

## Persistência de dados entre tarefas

Tanto o CircleCI quanto o GitHub Actions fornecem mecanismos para suportar dados entre trabalhos.

Abaixo há um exemplo na sintaxe de configuração do GitHub Actions e do CircleCI.

### Sintaxe do CircleCI para persistir dados entre trabalhos

```yaml
- persist_to_workspace:
    root: workspace
    paths:
      - math-homework.txt

...

- attach_workspace:
    at: /tmp/workspace
```

### Sintaxe do GitHub Actions para persistir dados entre trabalhos

```yaml
- name: Upload math result for job 1
  uses: actions/upload-artifact@v4
  with:
    name: homework
    path: math-homework.txt

...

- name: Download math result for job 1
  uses: actions/download-artifact@v5
  with:
    name: homework
```

Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../store-and-share-data.md).

## Usar bancos de dados e contêineres de serviço

Ambos os sistemas permitem que você inclua contêineres adicionais para bases de dados, memorização ou outras dependências.

No CircleCI, a primeira imagem listada no *config.yaml* é a imagem principal primária usada para executar comandos.
GitHub Actions usa seções explícitas: use `container` para o contêiner primário e liste contêineres adicionais em `services`.

Abaixo há um exemplo na sintaxe de configuração do GitHub Actions e do CircleCI.

### Sintaxe do CircleCI para usar bancos de dados e contêineres de serviço

```yaml
---
version: 2.1

jobs:

  ruby-26:
    docker:
      - image: circleci/ruby:2.6.3-node-browsers-legacy
        environment:
          PGHOST: localhost
          PGUSER: administrate
          RAILS_ENV: test
      - image: postgres:10.1-alpine
        environment:
          POSTGRES_USER: administrate
          POSTGRES_DB: ruby26
          POSTGRES_PASSWORD: ""

    working_directory: ~/administrate

    steps:
      - checkout

      # Bundle install dependencies
      - run: bundle install --path vendor/bundle

      # Wait for DB
      - run: dockerize -wait tcp://localhost:5432 -timeout 1m

      # Setup the environment
      - run: cp .sample.env .env

      # Setup the database
      - run: bundle exec rake db:setup

      # Run the tests
      - run: bundle exec rake

workflows:
  version: 2
  build:
    jobs:
      - ruby-26
...

- attach_workspace:
    at: /tmp/workspace
```

### Sintaxe do GitHub Actions para o uso de bancos de dados e contêineres de serviço

<!-- markdownlint-disable search-replace -->

```yaml
name: Containers

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    container: circleci/ruby:2.6.3-node-browsers-legacy

    env:
      PGHOST: postgres
      PGUSER: administrate
      RAILS_ENV: test

    services:
      postgres:
        image: postgres:10.1-alpine
        env:
          POSTGRES_USER: administrate
          POSTGRES_DB: ruby25
          POSTGRES_PASSWORD: ""
        ports:
          - 5432:5432
        # Add a health check
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
      # This Docker file changes sets USER to circleci instead of using the default user, so we need to update file permissions for this image to work on GH Actions.
      # See https://docs.github.com/actions/using-github-hosted-runners/about-github-hosted-runners#docker-container-filesystem

      - name: Setup file system permissions
        run: sudo chmod -R 777 $GITHUB_WORKSPACE /github /__w/_temp
      - uses: actions/checkout@v6
      - name: Install dependencies
        run: bundle install --path vendor/bundle
      - name: Setup environment configuration
        run: cp .sample.env .env
      - name: Setup database
        run: bundle exec rake db:setup
      - name: Run tests
        run: bundle exec rake
```

<!-- markdownlint-enable search-replace -->

Para saber mais, confira [Comunicar-se com os contêineres de serviço do Docker](../../use-containerized-services/use-docker-service-containers.md).

## Exemplo completo

Abaixo, há um exemplo concreto. No lado esquerdo, é mostrado o *config.yml* real do CircleCI para o repositório [thoughtbot/administrator](https://github.com/thoughtbot/administrate). À direita é mostrado o GitHub Actions equivalente correspondente.

### Exemplo completo do CircleCI

```yaml
---
version: 2.1

commands:
  shared_steps:
    steps:
      - checkout

      # Restore Cached Dependencies
      - restore_cache:
          name: Restore bundle cache
          key: administrate-{{ checksum "Gemfile.lock" }}

      # Bundle install dependencies
      - run: bundle install --path vendor/bundle

      # Cache Dependencies
      - save_cache:
          name: Store bundle cache
          key: administrate-{{ checksum "Gemfile.lock" }}
          paths:
            - vendor/bundle

      # Wait for DB
      - run: dockerize -wait tcp://localhost:5432 -timeout 1m

      # Setup the environment
      - run: cp .sample.env .env

      # Setup the database
      - run: bundle exec rake db:setup

      # Run the tests
      - run: bundle exec rake

default_job: &default_job
  working_directory: ~/administrate
  steps:
    - shared_steps
    # Run the tests against multiple versions of Rails
    - run: bundle exec appraisal install
    - run: bundle exec appraisal rake

jobs:
  ruby-25:
    <<: *default_job
    docker:
      - image: circleci/ruby:2.5.0-node-browsers
        environment:
          PGHOST: localhost
          PGUSER: administrate
          RAILS_ENV: test
      - image: postgres:10.1-alpine
        environment:
          POSTGRES_USER: administrate
          POSTGRES_DB: ruby25
          POSTGRES_PASSWORD: ""

  ruby-26:
    <<: *default_job
    docker:
      - image: circleci/ruby:2.6.3-node-browsers-legacy
        environment:
          PGHOST: localhost
          PGUSER: administrate
          RAILS_ENV: test
      - image: postgres:10.1-alpine
        environment:
          POSTGRES_USER: administrate
          POSTGRES_DB: ruby26
          POSTGRES_PASSWORD: ""

workflows:
  version: 2
  multiple-rubies:
    jobs:
      - ruby-26
      - ruby-25
```

### Exemplo completo para GitHub Actions

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Containers

on: [push]

jobs:
  build:

    strategy:
      matrix:
        ruby: ['2.5', '2.6.3']

    runs-on: ubuntu-latest

    env:
      PGHOST: localhost
      PGUSER: administrate
      RAILS_ENV: test

    services:
      postgres:
        image: postgres:10.1-alpine
        env:
          POSTGRES_USER: administrate
          POSTGRES_DB: ruby25
          POSTGRES_PASSWORD: ""
        ports:
          - 5432:5432
        # Add a health check
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
      - uses: actions/checkout@v6
      - name: Setup Ruby
        uses: eregon/use-ruby-action@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: ${{ matrix.ruby }}
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: vendor/bundle
          key: administrate-${{ matrix.image }}-${{ hashFiles('Gemfile.lock') }}
      - name: Install postgres headers
        run: |
          sudo apt-get update
          sudo apt-get install libpq-dev
      - name: Install dependencies
        run: bundle install --path vendor/bundle
      - name: Setup environment configuration
        run: cp .sample.env .env
      - name: Setup database
        run: bundle exec rake db:setup
      - name: Run tests
        run: bundle exec rake
      - name: Install appraisal
        run: bundle exec appraisal install
      - name: Run appraisal
        run: bundle exec appraisal rake
```
```
