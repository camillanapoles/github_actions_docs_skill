---
title: Aprovando e mantendo ações
description: Você pode aproveitar a automação e as melhores práticas de código aberto para liberar e manter ações automatizadas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions
captured: '2026-10-19'
section: How tos / Create and publish actions
---

# Aprovando e mantendo ações

_Você pode aproveitar a automação e as melhores práticas de código aberto para liberar e manter ações automatizadas._

## Introdução

Depois de criar uma ação, você irá continuar lançando novas funcionalidades enquanto trabalha com contribuições da comunidade. Este tutorial descreve um processo de exemplo que você pode seguir para liberar e manter ações em código aberto. O exemplo:

* Utiliza GitHub Actions para integração contínua, atualização de dependências, gerenciamento de lançamentos e automação de tarefas.
* Fornece confiança por meio de testes automatizados e cria selos.
* Indica como a ação pode ser usada, de preferência como parte de um fluxo de trabalho mais amplo.
* Sinaliza que tipo de contribuições da comunidade você recebe. (Por exemplo, problemas, pull requests ou relatórios de vulnerabilidade.)

Para ver um exemplo aplicado desse processo, confira [actions/javascript-action](https://github.com/actions/javascript-action).

## Desenvolver e lançar ações

Nesta seção, discutiremos um processo de exemplo para desenvolver e liberar ações e mostrar como usar GitHub Actions para automatizar o processo.

### Sobre ações do JavaScript

As ações do JavaScript são repositórios do Node.js com metadados. No entanto, as ações do JavaScript têm propriedades adicionais comparadas aos projetos tradicionais do Node.js:

* Os pacotes dependentes recebem commit ao lado do código, normalmente em uma forma compilada e minificada. Isto significa que as criações automatizadas e as contribuições seguras da comunidade são importantes.

* As versões marcadas podem ser publicadas diretamente em GitHub Marketplace e consumidas por fluxos de trabalho em GitHub.

* Muitas ações usam GitHubAPIs e APIs de terceiros, portanto, incentivamos testes de ponta a ponta robustos.

### Configurando GitHub Actions fluxos de trabalho

Para dar suporte ao processo de desenvolvedor na próxima seção, adicione dois GitHub Actions fluxos de trabalho ao repositório:

1. Adicione um fluxo de trabalho que é disparado quando um commit é enviado por push para um branch de recursos ou para `main` ou quando uma solicitação de pull é criada. Configure o fluxo de trabalho para executar seus testes de unidade e integração. Para ver um exemplo, confira [este fluxo de trabalho](https://github.com/actions/javascript-action/blob/main/.github/workflows/ci.yml).
2. Adicione um fluxo de trabalho que é acionado quando uma versão é publicada ou editada. Configure o fluxo de trabalho para garantir que as tags semânticas estejam prontas. Use uma ação como [JasonEtco/build-and-tag-action](https://github.com/JasonEtco/build-and-tag-action) para compilar e empacotar o arquivo JavaScript e de metadados e forçar o push das tags semânticas principal, secundário e de patch. Para obter mais informações sobre tags semânticas, confira [Sobre o controle de versão semântico](https://docs.npmjs.com/about-semantic-versioning).

!!! note

   > Se você habilitar versões imutáveis para o seu repositório, não poderá usar esta ação para forçar o envio de tags associadas a versões em GitHub. Para saber como gerenciar suas versões com versões imutáveis, confira [Como usar versões e marcas imutáveis para gerenciar as versões da sua ação](using-immutable-releases-and-tags-to-manage-your-actions-releases.md).

### Exemplo do processo de desenvolvedor

Aqui está um processo de exemplo que você pode seguir para executar testes automaticamente, criar uma versão, publicar em GitHub Marketplace e publicar sua ação.

1. Faça o trabalho de recurso nas ramificações por fluxo do GitHub. Para obter mais informações, confira [fluxo de GitHub](https://docs.github.com/pt/get-started/using-github/github-flow).
   * Sempre que um commit é enviado por push para o branch de recurso, seu fluxo de trabalho de teste irá executar os testes automaticamente.

2. Crie solicitações de pull para o branch `main` a fim de iniciar a discussão e a revisão, mesclando-as quando estiverem prontas.

   * Quando um pull request é aberto, seja em um branch ou bifurcação, seu fluxo de trabalho de testes executará novamente os testes, desta vez com o commit do merge.

   * **Observação:** por motivos de segurança, os fluxos de trabalho disparados por `pull_request` por meio de forks têm permissões `GITHUB_TOKEN` restritas e não têm acesso aos segredos. Se os testes ou outros fluxos de trabalho disparados após a solicitação de pull exigirem acesso aos segredos, considere o uso de outro evento, como um [gatilho manual](../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch) ou um [`pull_request_target`](../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target). Para obter mais informações, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull-request-events-for-forked-repositories).

3. Crie uma versão semântica marcada.
   Você também pode publicar em GitHub Marketplace com uma simples caixa de seleção.
   Para obter mais informações, consulte [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release) e [Publicar ações no GitHub Marketplace](publish-in-github-marketplace.md#publishing-an-action).

   * Quando uma versão é publicada ou editada, seu fluxo de trabalho de versão cuidará automaticamente da compilação e ajuste das tags.

   * Recomendamos criar versões usando tags com controle de versão semântico (por exemplo, `v1.1.3`) e manter as tags de principal (`v1`) e secundário (`v1.1`) atuais com o último commit apropriado. Para obter mais informações, confira [Como gerenciar ações personalizadas](manage-custom-actions.md#using-release-management-for-actions) e [Sobre o controle de versão semântico](https://docs.npmjs.com/about-semantic-versioning).

### Resultados

Ao contrário de algumas outras estratégias de gerenciamento de versão automatizadas, esse processo intencionalmente não faz commit das dependências no branch `main`, apenas para os commits de versão marcados. Ao fazer isso, você incentiva os usuários da sua ação a referenciar os `sha`s ou as tags nomeadas e ajuda a garantir a segurança das solicitações de pull de terceiros fazendo o build por conta própria durante uma versão.

Usar versões semânticas significa que os usuários das suas ações podem fixar os seus fluxos de trabalho a uma versão e saber que podem continuar recebendo a última estabilidade recursos não relevantes, dependendo de seu nível de conforto.

## Trabalhando com a comunidade

GitHubfornece ferramentas e guias para ajudá-lo a trabalhar com a comunidade código aberto. Aqui estão algumas ferramentas que recomendamos a criação de uma comunicação bidirecional saudável. Ao fornecer os seguintes sinais à comunidade, você incentiva outras pessoas a usar, modificar e contribuir para sua ação:

* Mantenha um `README` com muitos exemplos de uso e diretrizes. Para obter mais informações, confira [Sobre o arquivo README do repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).
* Inclua uma notificação de status do fluxo de trabalho no arquivo `README`. Para obter mais informações, confira [Adicionar um selo de status de fluxo de trabalho](../monitor-workflows/add-a-status-badge.md). Visite também [shields.io](https://shields.io/) para saber mais sobre outros selos que você pode adicionar.
* Adicione arquivos de integridade da comunidade, como `CODE_OF_CONDUCT`, `CONTRIBUTING` e `SECURITY`. Para obter mais informações, confira [Como criar um arquivo padrão de integridade da comunidade](https://docs.github.com/pt/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file#supported-file-types).
* Mantenha os problemas atuais utilizando ações como [actions/stale](https://github.com/actions/stale).
* Use os recursos de segurança de GitHub para se comunicar sobre vulnerabilidades e como corrigi-las. Para obter mais informações, consulte [Referência de uso seguro](../../reference/security/secure-use.md#protecting-actions-youve-created).

## Leitura adicional

Os exemplos em que os padrões similares são empregados incluem:

* [github/super-linter](https://github.com/github/super-linter)
* [octokit/request-action](https://github.com/octokit/request-action)
* [actions/javascript-action](https://github.com/actions/javascript-action)
