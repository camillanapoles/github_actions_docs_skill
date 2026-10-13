---
title: Criar e testar o Ruby
description: É possível criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto do Ruby.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/ruby
captured: '2026-10-13'
section: Tutorials / Build and test code
---

# Criar e testar o Ruby

_É possível criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto do Ruby._

## Introdução

Este guia mostra como criar um fluxo de trabalho de integração contínua (CI) que compila e testa um aplicativo do Rubi. Se os seus testes do CI passarem, você pode querer implantar seu código ou publicar uma gem.

## Pré-requisitos

Recomendamos que você tenha um entendimento básico do Ruby, YAML, das opções de configuração do fluxo de trabalho e de como criar um arquivo do fluxo de trabalho. Para obter mais informações, consulte:

* [Aprender GitHub Actions](../../how-tos/write-workflows.md)
* [Ruby em 20 minutos](https://www.ruby-lang.org/en/documentation/quickstart/)

## Usando um modelo de fluxo de trabalho do Ruby

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para Ruby que deve funcionar para a maioria dos projetos ruby. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "ruby".

5. Filtre a seleção de fluxos de trabalho clicando em **Integração contínua**.

6. No fluxo de trabalho "Ruby", clique em **Configurar**.

7. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere as versões do Ruby que você deseja usar.

!!! note

   >
   > * Este modelo de fluxo de trabalho contém uma ação que não é certificada por GitHub. Elas são fornecidas por terceiros e regidas por termos de serviço, política de privacidade e documentação de suporte separados.
   > * Caso use ações de terceiros, você deverá usar uma versão especificada por um SHA de commit. Se a ação for revisada e você quiser usar a versão mais recente, será necessário atualizar o SHA. Você pode especificar uma versão fazendo referência a uma tag ou branch, mas a ação pode ser alterada sem aviso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#using-third-party-actions).

8. Clique em **Confirmar alterações**.

   O `ruby.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Especificar a versão do Ruby

A maneira mais fácil de especificar uma versão do Ruby é usando a ação `ruby/setup-ruby` fornecida pela organização Ruby no GitHub. A ação adiciona qualquer versão do Ruby compatível a `PATH` em cada trabalho executado em um fluxo de trabalho. Para obter mais informações e as versões disponíveis do Ruby, confira [`ruby/setup-ruby`](https://github.com/ruby/setup-ruby).

Usar a ação `ruby/setup-ruby` do Ruby é a maneira recomendada de usar Ruby com GitHub Actions porque garante um comportamento consistente entre diferentes corredores e versões diferentes do Ruby.

A ação `setup-ruby` usa uma versão do Ruby como entrada e configura essa versão no executor.

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
steps:
- uses: actions/checkout@v6
- uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
  with:
    ruby-version: '3.1' # Not needed with a .ruby-version file
- run: bundle install
- run: bundle exec rake
```

Como alternativa, você poderá fazer check-in de um arquivo `.ruby-version` na raiz do repositório e `setup-ruby` usará a versão definida nesse arquivo.

```
## Testar com versões múltiplas do Ruby

Você pode adicionar uma estratégia matriz para executar seu fluxo de trabalho com mais de uma versão do Ruby. Por exemplo, você pode testar seu código com as últimas versões de patch das versões 3.1, 3.0 e 2.7.

```yaml
strategy:
  matrix:
    ruby-version: ['3.1', '3.0', '2.7']
```

Cada versão do Ruby especificada na matriz `ruby-version` cria um trabalho que executa as mesmas etapas. O contexto `${{ matrix.ruby-version }}` é usado para acessar a versão da tarefa atual. Para saber mais sobre estratégias e contextos de matriz, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md) e [Referência de contextos](../../reference/workflows-and-actions/contexts.md).

O fluxo de trabalho totalmente modernizado com uma estratégia de matriz pode se parecer com isto:

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Ruby CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:

    runs-on: ubuntu-latest

    strategy:
      matrix:
        ruby-version: ['3.1', '3.0', '2.7']

    steps:
      - uses: actions/checkout@v6
      - name: Set up Ruby ${{ matrix.ruby-version }}
        uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: ${{ matrix.ruby-version }}
      - name: Install dependencies
        run: bundle install
      - name: Run tests
        run: bundle exec rake
```

```
## Instalar dependências com o Bundler

A ação `setup-ruby` instalará automaticamente o Bundler para você. A versão é determinada pelo arquivo `gemfile.lock`. Se nenhuma versão estiver presente no seu arquivo de bloqueio, será instalada a última versão compatível.

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
steps:
- uses: actions/checkout@v6
- uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
  with:
    ruby-version: '3.1'
- run: bundle install
```

```
### Memorizar dependências

As ações `setup-ruby` fornecem um método para lidar automaticamente com o cache dos seus gems entre as execuções.

Para habilitar o cache, defina o seguinte.

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
steps:
- uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
  with:
    bundler-cache: true
```

Isso vai configurar o empacotador para instalar os gems em `vendor/cache`. Para cada execução bem-sucedida do fluxo de trabalho, essa pasta será armazenada em cache por GitHub Actions e baixada novamente para execuções subsequentes do fluxo de trabalho. Um hash do `gemfile.lock` e a versão do Ruby são usados como a chave de cache. Se você instalar qualquer novo gem, ou mudar uma versão, o cache será invalidado e o bundler fará uma nova instalação.

**Como fazer o armazenamento em cache sem o setup-ruby**

Para maior controle sobre o cache, você pode usar a ação `actions/cache` diretamente. Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

```
steps:
- uses: actions/cache@v4
  with:
    path: vendor/bundle
    key: ${{ runner.os }}-gems-${{ hashFiles('**/Gemfile.lock') }}
    restore-keys: |
      ${{ runner.os }}-gems-
- name: Bundle install
  run: |
    bundle config path vendor/bundle
    bundle install --jobs 4 --retry 3
```

Se você estiver usando uma compilação de matriz, você vai querer incluir as variáveis da matriz na sua chave de cache. Por exemplo, se você tiver uma estratégia de matriz para diferentes versões do Ruby (`matrix.ruby-version`) e diferentes sistemas operacionais (`matrix.os`), as etapas de fluxo de trabalho poderão ter esta aparência:

```
steps:
- uses: actions/cache@v4
  with:
    path: vendor/bundle
    key: bundle-use-ruby-${{ matrix.os }}-${{ matrix.ruby-version }}-${{ hashFiles('**/Gemfile.lock') }}
    restore-keys: |
      bundle-use-ruby-${{ matrix.os }}-${{ matrix.ruby-version }}-
- name: Bundle install
  run: |
    bundle config path vendor/bundle
    bundle install --jobs 4 --retry 3
```

## Matriz que testa o seu código

O exemplo a seguir da matriz testa todas as versões estáveis e versões principais de MRI, JRuby e TruffleRuby no Ubuntu e no macOS.

```
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Matrix Testing

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}-latest
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu, macos]
        ruby: [2.5, 2.6, 2.7, head, debug, jruby, jruby-head, truffleruby, truffleruby-head]
    continue-on-error: ${{ endsWith(matrix.ruby, 'head') || matrix.ruby == 'debug' }}
    steps:
      - uses: actions/checkout@v6
      - uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: ${{ matrix.ruby }}
      - run: bundle install
      - run: bundle exec rake
```

```
## Fazer linting do seu código

O exemplo a seguir instala o `rubocop` e o usa para fazer lint de todos os arquivos. Para obter mais informações, confira [RuboCop](https://github.com/rubocop-hq/rubocop). Você pode [configurar o RuboCop](https://docs.rubocop.org/rubocop/configuration.html) para decidir as regras de linting específicas que serão usadas.

```
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Linting

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: '2.6'
      - run: bundle install
      - name: Rubocop
        run: rubocop -f github
```

Especificar `-f github` significa que a saída do RuboCop estará no formato de anotação de GitHub. Quaisquer erros de linting serão mostrados embutidos na guia **Arquivos alterados** da pull request que os apresenta.

```
## Publicar gems

Você pode configurar o seu fluxo de trabalho para publicar o seu pacote do Ruby em qualquer pacote de registro que você desejar quando os seus testes de CI passarem.

Você pode armazenar qualquer token de acesso ou credenciais necessárias para publicar seu pacote usando segredos do repositório. O exemplo a seguir cria e publica um pacote para `GitHub Package Registry` e `RubyGems`.

```
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Ruby Gem

on:
  # Manually publish
  workflow_dispatch:
  # Alternatively, publish whenever changes are merged to the `main` branch.
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    name: Build + Publish
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read

    steps:
      - uses: actions/checkout@v6
      - name: Set up Ruby 2.6
        uses: ruby/setup-ruby@ec02537da5712d66d4d50a0f33b7eb52773b5ed1
        with:
          ruby-version: '2.6'
      - run: bundle install

      - name: Publish to GPR
        run: |
          mkdir -p $HOME/.gem
          touch $HOME/.gem/credentials
          chmod 0600 $HOME/.gem/credentials
          printf -- "---\n:github: ${GEM_HOST_API_KEY}\n" > $HOME/.gem/credentials
          gem build *.gemspec
          gem push --KEY github --host https://rubygems.pkg.github.com/${OWNER} *.gem
        env:
          GEM_HOST_API_KEY: "Bearer ${{secrets.GITHUB_TOKEN}}"
          OWNER: ${{ github.repository_owner }}

      - name: Publish to RubyGems
        run: |
          mkdir -p $HOME/.gem
          touch $HOME/.gem/credentials
          chmod 0600 $HOME/.gem/credentials
          printf -- "---\n:rubygems_api_key: ${GEM_HOST_API_KEY}\n" > $HOME/.gem/credentials
          gem build *.gemspec
          gem push *.gem
        env:
          GEM_HOST_API_KEY: "${{secrets.RUBYGEMS_AUTH_TOKEN}}"
```
```
