---
title: Criar uma ação da CLI de terceiros
description: Saiba como desenvolver uma ação para configurar uma CLI nos executores GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/create-a-cli-action
captured: '2026-10-11'
section: GitHub Actions
---

# Criar uma ação da CLI de terceiros

_Saiba como desenvolver uma ação para configurar uma CLI nos executores GitHub Actions._

## Introdução

Você pode escrever uma ação para oferecer uma forma de os usuários acessarem seus servidores por meio de um ambiente de CLI já configurado em GitHub Actions runners.

Sua ação deve:

* Ser simples para os usuários especificarem a versão da CLI a ser instalada
* Ser compatível com vários sistemas operacionais
* Executar de maneira eficiente para minimizar o tempo de execução e os custos associados
* Trabalhar entre executores hospedados em GitHub e auto-hospedados
* Alavancar ferramentas da comunidade quando possível

Este artigo irá demonstrar como escrever uma ação que recupera uma versão específica da sua CLI, como instalá-la, adicioná-la ao caminho e (opcionalmente), armazená-la em cache. Em geral, esse tipo de ação (uma ação que configura uma ferramenta) é chamado `setup-$TOOL`.

## Pré-requisitos

Você deve ter um entendimento de como escrever uma ação personalizada. Para saber mais, confira [Como gerenciar ações personalizadas](manage-custom-actions.md).

## Exemplo

O script a seguir demonstra como você pode obter uma versão especificada pelo usuário como entrada, fazer o download e extrair a versão específica da sua CLI e, em seguida, adicionar a CLI ao caminho.

GitHub fornece [`actions/toolkit`](https://github.com/actions/toolkit), que é um conjunto de pacotes que ajuda você a criar ações. Este exemplo usa os pacotes [`actions/core`](https://github.com/actions/toolkit/tree/main/packages/core) e [`actions/tool-cache`](https://github.com/actions/toolkit/tree/main/packages/tool-cache).

```javascript copy
const core = require('@actions/core');
const tc = require('@actions/tool-cache');

async function setup() {
  // Get version of tool to be installed
  const version = core.getInput('version');

  // Download the specific version of the tool, e.g. as a tarball
  const pathToTarball = await tc.downloadTool(getDownloadURL());

  // Extract the tarball onto the runner
  const pathToCLI = await tc.extractTar(pathToTarball);

  // Expose the tool by adding it to the PATH
  core.addPath(pathToCLI)
}

module.exports = setup
```

Para usar esse script, substitua `getDownloadURL` por uma função que baixa a CLI. Você também precisará criar um arquivo de metadados de ações (`action.yml`) que aceite uma entrada `version` e que execute esse script. Para obter detalhes completos sobre como criar uma ação, confira [Criando uma ação de JavaScript](../../tutorials/create-actions/create-a-javascript-action.md).

## Leitura adicional

Este padrão é usado em várias ações. Para mais exemplos, consulte:

* [`ruby/setup-ruby`](https://github.com/ruby/setup-ruby)
* [`google-github-actions/setup-gcloud`](https://github.com/google-github-actions/setup-gcloud)
* [`hashicorp/setup-terraform`](https://github.com/hashicorp/setup-terraform)
