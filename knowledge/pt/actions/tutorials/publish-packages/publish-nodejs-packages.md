---
title: Publicar pacotes do Node.js
description: Neste tutorial, você aprenderá a publicar pacotes do Node.js em um registro como parte do fluxo de trabalho de CI (integração contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/publish-packages/publish-nodejs-packages
captured: '2026-10-11'
section: GitHub Actions
---

# Publicar pacotes do Node.js

_Neste tutorial, você aprenderá a publicar pacotes do Node.js em um registro como parte do fluxo de trabalho de CI (integração contínua)._

## Introdução

Este guia mostra como criar um fluxo de trabalho que publica pacotes Node.js nos registros GitHub Packages e npm após a aprovação nos testes de integração contínua (CI).

## Pré-requisitos

Recomendamos que você tenha um entendimento básico das opções de configuração do fluxo de trabalho e de como criar um arquivo do fluxo de trabalho. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Para obter mais informações sobre como criar um fluxo de trabalho de CI para seu projeto do Node.js, consulte [Criar e testar Node.js](../build-and-test-code/nodejs.md).

Você também pode achar útil ter um entendimento básico do seguinte:

* [Trabalhando com o repositório npm](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-npm-registry)
* [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md)
* [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
* [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md)

## Sobre a configuração do pacote

Os campos `name` e `version` no arquivo `package.json` criam um identificador exclusivo usados pelos registros para vincular pacotes a registros. Você pode adicionar um resumo para a página de listagem de pacotes ao incluir um campo de `description` no arquivo `package.json`. Para obter mais informações, consulte [Criar um arquivo package.json](https://docs.npmjs.com/creating-a-package-json-file) e [Criar módulos do Node.js](https://docs.npmjs.com/creating-node-js-modules) na documentação do npm.

Quando um arquivo `.npmrc` local existe e possui um valor especificado para `registry`, o comando `npm publish` utiliza o registro configurado no arquivo `.npmrc`. Você pode usar a ação `setup-node` para criar um arquivo `.npmrc` local no executor que configura o registro e o escopo padrão. A ação `setup-node` também aceita um token de autenticação como entrada, usado para acessar registros privados ou publicar pacotes de nós. Para obter mais informações, confira [`setup-node`](https://github.com/actions/setup-node/).

Você pode especificar a versão do Node.js instalada no executor usando a ação `setup-node`.

Se você adicionar etapas ao seu fluxo de trabalho para configurar os campos `publishConfig` no arquivo `package.json`, você não precisará especificar a URL do registro usando a ação `setup-node`, mas não poderá publicar o pacote em mais de um registro. Para obter mais informações, consulte [publishConfig](https://docs.npmjs.com/cli/v9/configuring-npm/package-json#publishconfig) na documentação do npm.

## Publicar pacotes no registro npm

Cada vez que você publicar uma nova versão, poderá acionar um fluxo de trabalho para publicar o seu pacote. O processo no exemplo a seguir é executado quando o evento de lançamento do tipo `published` é disparado. Se os testes de CI forem aprovados, o processo carregará o pacote no registro npm. Para saber mais, confira [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).

Para executar operações autenticadas para o registro npm em seu fluxo de trabalho, você precisará armazenar seu token de autenticação npm como um segredo. Por exemplo, crie um segredo do repositório chamado `NPM_TOKEN`. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

Por padrão, o npm usa o campo `name` do arquivo `package.json` para determinar o nome do pacote publicado. Ao publicar em um namespace global, você precisa incluir apenas o nome do pacote. Por exemplo, você publicaria um pacote nomeado `my-package` para `https://www.npmjs.com/package/my-package`.

Se você estiver publicando um pacote que inclui um prefixo de escopo, inclua o escopo no nome do arquivo `package.json`. Por exemplo, se o prefixo do escopo do npm for "octocat" e o nome do pacote for "hello-world", o campo `name` no seu arquivo `package.json` deverá ser `@octocat/hello-world`. Se o seu pacote npm usar um prefixo de escopo e for público, você deverá usar a opção `npm publish --access public`. Essa é uma opção que o npm requer para impedir que alguém publique um pacote privado de forma não intencional.

Se você quiser publicar seu pacote com proveniência, inclua a flag `--provenance` no comando `npm publish`. Isso permite que você estabeleça publicamente e de forma verificável onde e como seu pacote foi criado, o que aumenta a segurança da cadeia de fornecedores para as pessoas que consomem seu pacote. Para obter mais informações, consulte [Geração de declarações de procedência](https://docs.npmjs.com/generating-provenance-statements) na documentação do npm.

Este exemplo armazena o segredo `NPM_TOKEN` na variável de ambiente `NODE_AUTH_TOKEN`. Quando a ação `setup-node` cria um arquivo `.npmrc`, ele faz referência ao token da variável de ambiente `NODE_AUTH_TOKEN`.

```yaml copy
name: Publish Package to npmjs
on:
  release:
    types: [published]
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v6
      # Setup .npmrc file to publish to npm
      - uses: actions/setup-node@v7
        with:
          node-version: '20.x'
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

No exemplo acima, a ação `setup-node` cria um arquivo `.npmrc` no executor com os seguintes tipos de conteúdo:

```shell
//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}
registry=https://registry.npmjs.org/
always-auth=true
```

Observe que você precisa definir o `registry-url` para `https://registry.npmjs.org/` no `setup-node` para configurar corretamente suas credenciais.

## Publicando pacotes para GitHub Packages

Cada vez que você publicar uma nova versão, poderá acionar um fluxo de trabalho para publicar o seu pacote. O processo no exemplo a seguir é executado quando o evento de lançamento do tipo `published` é disparado. Se os testes de CI forem aprovados, o processo carregará o pacote para GitHub Packages. Para saber mais, confira [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).

### Configurar o repositório de destino

Vincular seu pacote a GitHub Packages usando a chave `repository` é opcional. Se você optar por não fornecer a `repository` chave em seu `package.json` arquivo, o pacote não será vinculado a um repositório quando ele for publicado, mas você poderá optar por conectar o pacote a um repositório posteriormente.

Se você fornecer a chave `repository` em seu arquivo `package.json`, o repositório especificado nessa chave será usado como registro npm de destino para GitHub Packages. Por exemplo, publicar os resultados abaixo `package.json` em um pacote nomeado `my-package` publicado no `octocat/my-other-repo`GitHub repositório.

```json
{
  "name": "@octocat/my-package",
  "repository": {
    "type": "git",
    "url": "https://github.com/octocat/my-other-repo.git"
  }
}
```

### Efetuar a autenticação no repositório de destino

Para executar operações autenticadas no GitHub Packages registro em seu fluxo de trabalho, você pode usar o `GITHUB_TOKEN`. O segredo `GITHUB_TOKEN` é definido como um token de acesso para o repositório sempre que um trabalho em um fluxo de trabalho é iniciado. Você deve definir as permissões desse token de acesso no arquivo de fluxo de trabalho para permitir acesso de leitura à permissão `contents` e acesso de gravação à permissão `packages`. Para saber mais, confira [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md).

Se você quiser publicar seu pacote em um repositório diferente, deve usar um personal access token (classic) que tenha permissão de gravação nos pacotes do repositório de destino. Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) e [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

### Exemplo de fluxo de trabalho

Este exemplo armazena o segredo `GITHUB_TOKEN` na variável de ambiente `NODE_AUTH_TOKEN`. Quando a ação `setup-node` cria um arquivo `.npmrc`, ele faz referência ao token da variável de ambiente `NODE_AUTH_TOKEN`.

```yaml copy
name: Publish package to GitHub Packages
on:
  release:
    types: [published]
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      # Setup .npmrc file to publish to GitHub Packages
      - uses: actions/setup-node@v7
        with:
          node-version: '20.x'
          registry-url: 'https://npm.pkg.github.com'
          # Defaults to the user or organization that owns the workflow file
          scope: '@octocat'
      - run: npm ci
      - run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

A ação `setup-node` cria um arquivo `.npmrc` no executor. Quando você usa a entrada `scope` para a ação `setup-node`, o arquivo `.npmrc` inclui o prefixo de escopo. Por padrão, a ação `setup-node` define o escopo no arquivo `.npmrc` para a conta que contém esse arquivo de fluxo de trabalho.

```shell
//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}
@octocat:registry=https://npm.pkg.github.com
always-auth=true
```

## Publicar pacotes usando o Yarn

Se você usar o gerenciador de pacotes Yarn, você poderá instalar e publicar pacotes usando o Yarn.

```yaml copy
name: Publish Package to npmjs
on:
  release:
    types: [published]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      # Setup .npmrc file to publish to npm
      - uses: actions/setup-node@v7
        with:
          node-version: '20.x'
          registry-url: 'https://registry.npmjs.org'
          # Defaults to the user or organization that owns the workflow file
          scope: '@octocat'
      - run: yarn
      - run: yarn npm publish // for Yarn version 1, use `yarn publish` instead
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

Para autenticar com o registro durante a publicação, verifique se o token de autenticação também está definido no arquivo `yarnrc.yml`. Para obter mais informações, confira o artigo [Configurações](https://yarnpkg.com/configuration/yarnrc#npmAuthToken) na documentação do Yarn.
