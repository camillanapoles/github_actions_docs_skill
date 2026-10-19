---
title: Criar e testar Node.js
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto Node.js.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/nodejs
captured: '2026-10-19'
section: Tutorials / Build and test code
---

# Criar e testar Node.js

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto Node.js._

## Introdução

Este guia mostra como criar um fluxo de trabalho de integração contínua (CI) que cria e testa o código Node.js. Se o seu teste de CI for aprovado, é possível que você deseje publicar seu código ou um pacote.

## Pré-requisitos

Recomendamos que você tenha um entendimento básico do Node.js, YAML, das opções de configuração do fluxo de trabalho e de como criar um arquivo do fluxo de trabalho. Para saber mais, veja:

* [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md)
* [Introdução ao Node.js](https://nodejs.org/learn/getting-started/introduction-to-nodejs)

## Usando um modelo de fluxo de trabalho do Node.js

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para Node.js que deve funcionar para a maioria dos projetos Node.js. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "Node.js".

5. Filtre a seleção de fluxos de trabalho clicando em **Integração contínua**.

6. No fluxo de trabalho "Node.js", clique em **Configurar**.

7. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere as versões do Node que você deseja usar.

8. Clique em **Confirmar alterações**.

   O `node.js.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Especificar a versão do Node.js

A maneira mais fácil de especificar uma versão Node.js é usando a ação `setup-node` fornecida por GitHub. Para obter mais informações, confira [`setup-node`](https://github.com/actions/setup-node/).

A ação `setup-node` usa uma versão do Node.js como entrada e configura essa versão no executor. A ação `setup-node` localiza uma versão específica do Node.js no cache de ferramentas em cada executor e adiciona os binários necessários a `PATH`, que é persistente no restante do trabalho. Usar a ação `setup-node` é a maneira recomendada de usar Node.js porque GitHub Actions garante um comportamento consistente entre diferentes corredores e versões diferentes de Node.js. Se você estiver usando um executor auto-hospedado, precisará instalar o Node.js e adicioná-lo a `PATH`.

O modelo de fluxo de trabalho inclui uma estratégia de matriz que cria e testa seu código com as versões do Node.js listadas no `node-version`. O "x" no número da versão é um caractere curinga que corresponde à última versão secundária e de patch disponível para uma versão. Cada versão do Node.js especificada na matriz `node-version` cria um trabalho que executa as mesmas etapas.

Cada tarefa pode acessar o valor definido na matriz `node-version` usando o contexto `matrix`. A ação `setup-node` usa o contexto como a entrada de `node-version`. A ação `setup-node` configura cada trabalho com uma versão diferente do Node.js antes de compilar e testar o código. Para saber mais sobre estratégias e contextos de matriz, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrix) e [Referência de contextos](../../reference/workflows-and-actions/contexts.md).

```yaml copy
strategy:
  matrix:
    node-version: ['18.x', '20.x']

steps:
- uses: actions/checkout@v6
- name: Use Node.js ${{ matrix.node-version }}
  uses: actions/setup-node@v7
  with:
    node-version: ${{ matrix.node-version }}
```

Como alternativa, você pode criar e fazes testes com versões exatas do Node.js.

```yaml copy
strategy:
  matrix:
    node-version: ['10.17.0', '17.9.0']
```

Você também pode criar e testar usando uma versão única do Node.js.

```yaml copy
name: Node.js CI

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
      - name: Use Node.js
        uses: actions/setup-node@v7
        with:
          node-version: '20.x'
      - run: npm ci
      - run: npm run build --if-present
      - run: npm test
```

Se você não especificar uma versão Node.js, GitHub usará a versão de Node.js padrão do ambiente.
Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Instalar dependências

Os executores hospedados do GitHub têm gerenciadores de dependência npm e Yarn instalados. Você pode usar o npm e o Yarn para instalar dependências no seu fluxo de trabalho antes de criar e testar seu código. Os runners hospedados em Windows e Linux GitHubtambém têm Grunt, Gulp e Bower instalados.

Você também pode armazenar dependências em cache para acelerar seu fluxo de trabalho. Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

### Exemplo de uso do npm

Este exemplo instala as versões no arquivo `package-lock.json` ou `npm-shrinkwrap.json` e impede atualizações no arquivo de bloqueio. O uso de `npm ci` geralmente é mais rápido do que a execução de `npm install`. Para obter mais informações, confira [`npm ci`](https://docs.npmjs.com/cli/ci.html) e [Apresentação do `npm ci` para builds mais rápidos e confiáveis](https://blog.npmjs.org/post/171556855892/introducing-npm-ci-for-faster-more-reliable).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    node-version: '20.x'
- name: Install dependencies
  run: npm ci
```

O uso de `npm install` instala as dependências definidas no arquivo `package.json`. Para obter mais informações, consulte [`npm install`](https://docs.npmjs.com/cli/install).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    node-version: '20.x'
- name: Install dependencies
  run: npm install
```

### Exemplo usando Yarn

Este exemplo instala as dependências definidas no arquivo `yarn.lock` e impede atualizações no arquivo `yarn.lock`. Para obter mais informações, consulte [`yarn install`](https://yarnpkg.com/en/docs/cli/install).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    node-version: '20.x'
- name: Install dependencies
  run: yarn --frozen-lockfile
```

Como alternativa, você pode instalar as dependências definidas no arquivo `package.json`.

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    node-version: '20.x'
- name: Install dependencies
  run: yarn
```

### Exemplo usando um registro privado e criando o arquivo .npmrc

Você pode usar a ação `setup-node` para criar um arquivo `.npmrc` local no executor que configura o registro e o escopo padrão. A ação `setup-node` também aceita um token de autenticação como entrada, usado para acessar registros privados ou publicar pacotes de nós. Para obter mais informações, confira [`setup-node`](https://github.com/actions/setup-node/).

Para efetuar a autenticação com seu registro privado, você precisará armazenar seu token de autenticação npm como um segredo. Por exemplo, crie um segredo do repositório chamado `NPM_TOKEN`. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

No exemplo abaixo, o segredo `NPM_TOKEN` armazena o token de autenticação do npm. A ação `setup-node` configura o arquivo `.npmrc` para ler o token de autenticação do npm por meio da variável de ambiente `NODE_AUTH_TOKEN`. Ao usar a ação `setup-node` para criar um arquivo `.npmrc`, você precisará definir a variável de ambiente `NODE_AUTH_TOKEN` com o segredo que contém o token de autenticação do npm.

Antes de instalar as dependências, use a ação `setup-node` para criar o arquivo `.npmrc`. A ação tem dois parâmetros de entrada. O parâmetro `node-version` define a versão do Node.js, e o parâmetro `registry-url` define o registro padrão. Se o registro de pacote usa escopos, é preciso usar o parâmetro `scope`. Para obter mais informações, consulte [`npm-scope`](https://docs.npmjs.com/misc/scope).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    always-auth: true
    node-version: '20.x'
    registry-url: https://registry.npmjs.org
    scope: '@octocat'
- name: Install dependencies
  run: npm ci
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

O exemplo acima cria um arquivo `.npmrc` com o seguinte conteúdo:

```shell
//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}
@octocat:registry=https://registry.npmjs.org/
always-auth=true
```

### Exemplo de dependências de cache

Você pode armazenar em cache e restaurar as dependências usando a ação [`setup-node`](https://github.com/actions/setup-node).

O exemplo a seguir armazena dependências do npm.

```yaml copy
steps:
- uses: actions/checkout@v6
- uses: actions/setup-node@v7
  with:
    node-version: '20'
    cache: 'npm'
- run: npm install
- run: npm test
```

O exemplo a seguir armazena dependências para o Yarn.

```yaml copy
steps:
- uses: actions/checkout@v6
- uses: actions/setup-node@v7
  with:
    node-version: '20'
    cache: 'yarn'
- run: yarn
- run: yarn test
```

O exemplo a seguir armazena dependências para pnpm (v6.10+).

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# NOTE: pnpm caching support requires pnpm version >= 6.10.0

steps:
- uses: actions/checkout@v6
- uses: pnpm/action-setup@0609f0983b7a228f052f81ef4c3d6510cae254ad
  with:
    version: 6.10.0
- uses: actions/setup-node@v7
  with:
    node-version: '20'
    cache: 'pnpm'
- run: pnpm install
- run: pnpm test
```

Se houver uma necessidade específica ou precisar de controles mais precisos de cache, use a [ação `cache`](https://github.com/marketplace/actions/cache). Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

```
## Criar e testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código. Por exemplo, se você executar `npm run build` para executar as etapas de build definidas no arquivo `package.json` e `npm test` para executar o conjunto de testes, adicionará esses comandos ao arquivo de fluxo de trabalho.

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Use Node.js
  uses: actions/setup-node@v7
  with:
    node-version: '20.x'
- run: npm install
- run: npm run build --if-present
- run: npm test
```

## Empacotar dados do fluxo de trabalho como artefatos

Você pode salvar artefatos das suas etapas de criação e teste para serem visualizados após a conclusão de um trabalho. Por exemplo, é possível que você precise salvar os arquivos de registro, os despejos de núcleo, os resultados de teste ou capturas de tela. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

## Publicar nos registros do pacote

Você pode configurar o seu fluxo de trabalho para publicar o seu pacote Node.js em um pacote de registro após os seus testes de CI serem aprovados. Para obter mais informações sobre publicação no npm e GitHub Packages, consulte [Publicar pacotes do Node.js](../publish-packages/publish-nodejs-packages.md).
