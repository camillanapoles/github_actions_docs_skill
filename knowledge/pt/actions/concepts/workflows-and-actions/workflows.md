---
title: Fluxos de trabalho
description: Obtenha uma visão geral de alto nível dos fluxos de GitHub Actions trabalho, incluindo gatilhos, sintaxe e recursos avançados.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/workflows
captured: '2026-10-19'
section: Concepts / Workflows and actions
---

# Fluxos de trabalho

_Obtenha uma visão geral de alto nível dos fluxos de GitHub Actions trabalho, incluindo gatilhos, sintaxe e recursos avançados._

## Sobre fluxos de trabalho

Um **fluxo de trabalho** é um processo automatizado configurável que executará um ou mais trabalhos. Os fluxos de trabalho são definidos por um arquivo YAML verificado no seu repositório e será executado quando acionado por um evento no repositório, ou eles podem ser acionados manualmente ou de acordo com um cronograma definido.

Os fluxos de trabalho são definidos no diretório `.github/workflows` de um repositório. Um repositório pode ter vários fluxos de trabalho, cada um dos quais pode executar um conjunto diferente de tarefas, como:

* Como criar e testar pull requests
* Como implantar seu aplicativo sempre que uma versão for criada
* Como adicionar um rótulo sempre que um novo problema for aberto

## Noções básicas do fluxo de trabalho

Um fluxo de trabalho precisa conter os seguintes componentes básicos:

1. Um ou mais *eventos* que acionarão o fluxo de trabalho.
2. Um ou mais *tarefas*, cada uma sendo executada em uma máquina *runner* e realizando uma série de uma ou mais *etapas*.
3. Cada etapa pode executar um script que você define ou executa uma ação, que é uma extensão reutilizável que pode simplificar seu fluxo de trabalho.

Para obter mais informações sobre esses componentes básicos, confira [Noções básicas sobre GitHub Actions](../../get-started/understand-github-actions.md#the-components-of-github-actions).

![Diagrama de um evento que dispara o Executor 1 para executar o Trabalho 1, que dispara o Executor 2 para executar o Trabalho 2. Cada um dos trabalhos é dividido em várias etapas.](https://docs.github.com/assets/images/help/actions/overview-actions-simple.png)

## Gatilhos do fluxo de trabalho

Os acionadores de fluxo de trabalho são eventos que fazem com que um fluxo de trabalho seja executado. Esses eventos podem ser:

* Eventos que ocorrem no repositório do fluxo de trabalho
* Eventos que ocorrem fora de GitHub e acionam um evento `repository_dispatch` em GitHub
* Horários agendados
* Manual

Por exemplo, você pode configurar o fluxo de trabalho para executar quando um push é feito no branch padrão do seu repositório, quando uma versão é criada, ou quando um problema é aberto.

Os gatilhos de fluxo de trabalho são definidos com a chave `on`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#on).

As etapas a seguir ocorrem para acionar a execução de um fluxo de trabalho:

1. Um evento ocorre no seu repositório. O evento tem um SHA de commit associado e um ref de Git.
2. GitHub procura no diretório `.github/workflows` na raiz do seu repositório por arquivos de fluxo de trabalho que estão presentes no commit SHA associado ou na Git ref do evento.
3. A execução de um fluxo de trabalho é disparada para todos os fluxos de trabalho que têm valores `on:` correspondentes ao evento de gatilho. Alguns eventos também exigem que o arquivo do fluxo de trabalho esteja presente no branch padrão do repositório para ser executado.

Cada execução de fluxo de trabalho usará a versão do fluxo de trabalho presente no commit SHA ou na referência do Git associados ao evento. Quando um fluxo de trabalho é executado, GitHub define as `GITHUB_SHA` variáveis de ambiente (commit SHA) e `GITHUB_REF` (Git ref) no ambiente do executor. Para saber mais, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

Para saber mais, confira [Acionando um fluxo de trabalho](../../how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow.md).

## Próximas etapas

Para criar seu primeiro fluxo de trabalho, confira [Criando um exemplo de fluxo de trabalho](../../tutorials/create-an-example-workflow.md).
