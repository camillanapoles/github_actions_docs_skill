---
title: Integração contínua
description: Você pode criar fluxos de trabalho personalizados de integração contínua (CI) diretamente no seu repositório GitHub com GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/get-started/continuous-integration
captured: '2026-10-13'
section: Get started
---

# Integração contínua

_Você pode criar fluxos de trabalho personalizados de integração contínua (CI) diretamente no seu repositório GitHub com GitHub Actions._

## Sobre integração contínua

A integração contínua (CI, Continuous Integration) é uma prática de software que exige commits frequentes de códigos para um repositório compartilhado. Fazer commits de códigos com frequência detecta erros com mais antecedência e reduz a quantidade de código necessária para depuração quando os desenvolvedores chegam à origem de um erro. As atualizações frequentes de código também facilitam a fusão de alterações entre os integrantes de uma equipe de desenvolvimento de software. Esta é uma ótima notícia para os desenvolvedores, que podem passar mais tempo na escrita de código e se preocupar menos com erros de depuração ou conflitos de mesclagem.

Ao fazer commit do código no repositório, você pode compilar e testar o código de maneira contínua para garantir que o commit não introduza erros. Seus testes podem incluir linters de código (que verificam formatação de estilo), verificações de segurança, cobertura de código, testes funcionais e outras verificações personalizadas.

Para compilar e testar seu código, é necessário usar um servidor. Você pode criar e testar atualizações no local antes de fazer push do código para um repositório, ou pode usar um servidor de CI que verifica os novos commits de código em um repositório.

## Sobre a integração contínua usando GitHub Actions

A CI usando GitHub Actions oferece fluxos de trabalho que podem compilar o código no seu repositório e executar seus testes. Os fluxos de trabalho podem ser executados em GitHubmáquinas virtuais hospedadas ou em máquinas que você mesmo hospeda. Para saber mais, confira [Executores hospedados no GitHub](../concepts/runners/github-hosted-runners.md) e [Executores auto-hospedados](../concepts/runners/self-hosted-runners.md).

Você pode configurar seu fluxo de trabalho de CI para ser executado quando ocorrer um evento GitHub (por exemplo, quando um novo código é enviado ao seu repositório), em uma programação definida ou quando ocorrer um evento externo usando o webhook repository_dispatch.

GitHub executa seus testes de CI e fornece os resultados de cada teste no pull request, para que você veja se a alteração na sua ramificação introduz um erro. Quando todos os testes de CI em um fluxo de trabalho forem aprovados, as alterações que passaram por push estarão prontas para a revisão de um integrante da equipe ou para o merge. Se algum teste falhar, uma de suas alterações pode ter causado a falha.

Quando você configura a CI em seu repositório, GitHub analisa o código em seu repositório e recomenda fluxos de trabalho de CI com base no idioma e na estrutura em seu repositório. Por exemplo, se você usar [Node.js](https://nodejs.org/en/), GitHub sugerirá um modelo de fluxo de trabalho que instala seus pacotes de Node.js e executa seus testes. Você pode usar o modelo de fluxo de trabalho de CI sugerido, GitHubpersonalizar o modelo de fluxo de trabalho sugerido ou criar seu próprio arquivo de fluxo de trabalho personalizado para executar seus testes de CI.

Além de ajudá-lo a configurar fluxos de trabalho de CI para seu projeto, você pode usar GitHub Actions para criar fluxos de trabalho em todo o ciclo de vida de desenvolvimento de software. Por exemplo, você pode usar ações para implantar, criar pacotes ou lançar uma versão do seu projeto. Para saber mais, confira [Escrevendo fluxos de trabalho](../how-tos/write-workflows.md).

Para ver uma definição de termos comuns, confira [Noções básicas sobre GitHub Actions](understand-github-actions.md).

## Próximas etapas

GitHub oferece modelos de fluxo de trabalho de CI para uma variedade de linguagens e estruturas. Para obter tutoriais sobre como configurar a integração contínua com esses modelos, consulte [Criar e testar seu código](../tutorials/build-and-test-code.md).
