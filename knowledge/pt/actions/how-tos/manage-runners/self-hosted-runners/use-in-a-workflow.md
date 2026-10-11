---
title: Usar os executores auto-hospedados em um fluxo de trabalho
description: Para usar executores auto-hospedados em um fluxo de trabalho, você pode usar rótulos ou grupos para especificar o executor para uma tarefa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Usar os executores auto-hospedados em um fluxo de trabalho { #using-self-hosted-runners-in-a-workflow }

_Para usar executores auto-hospedados em um fluxo de trabalho, você pode usar rótulos ou grupos para especificar o executor para uma tarefa._

## Exibindo executores disponíveis para um repositório { #viewing-available-runners-for-a-repository }

Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para o repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **(server) Runners**.
4. Clique na guia **Auto-hospedado** na parte superior da lista de executores.
5. Revise a lista de executores auto-hospedados disponíveis para o repositório. Essa lista inclui os executores auto-hospedados e os conjuntos de dimensionamento de executores criados com Actions Runner Controller. Para saber mais, confira [Controlador de Ações Runner](../../../concepts/runners/actions-runner-controller.md).
6. Opcionalmente, para copiar o rótulo de um corredor para usá-lo em um fluxo de trabalho, clique em (More options) à direita do corredor e clique em **Copiar rótulo**.

!!! note
    Os proprietários em nível de empresas e organizações, podem criar executores nesta página. Para criar um novo executor, clique em **Novo executor**, no canto superior direito da lista de executores, para adicionar executores ao repositório.

    Para obter mais informações, consulte [Gerenciar executores maiores](../larger-runners/manage-larger-runners.md) e [Adicionar executores auto-hospedados](add-runners.md).

## Usar etiquetas-padrão para rotear tarefas { #using-default-labels-to-route-jobs }

Um executor hospedado localmente recebe automaticamente determinados rótulos ao ser adicionado a GitHub Actions. Elas são usadas para indicar seu sistema operacional e sua plataforma de hardware:

* `self-hosted`: Rótulo padrão aplicado a executores auto-hospedados.
* `linux`, `windows` ou `macOS`: aplicado, dependendo do sistema operacional.
* `x64`, `ARM` ou `ARM64`: aplicado, dependendo da arquitetura de hardware.

Você pode usar o YAML do seu fluxo de trabalho para enviar trabalhos para uma combinação dessas etiquetas. Neste exemplo, um executor auto-hospedado que corresponde a todas as três etiquetas será elegível para executar a o trabalho:

```yaml
runs-on: [self-hosted, linux, ARM64]
```

* `self-hosted`: Execute esta tarefa em um servidor de execuções auto-hospedado.
* `linux` – Use apenas um executor baseado em Linux.
* `ARM64` – Use apenas um executor baseado no hardware ARM64.

Para criar corredores auto-hospedados individuais sem os rótulos padrão, passe o sinalizador `--no-default-labels` ao criar o corredor.

## Usar etiquetas personalizadas para rotear trabalhos { #using-custom-labels-to-route-jobs }

Você pode criar etiquetas personalizadas e atribuí-las aos seus executores auto-hospedados a qualquer momento. As etiquetas personalizadas permitem que você envie trabalhos para determinados tipos de executores auto-hospedados, com base no modo como como são rotulados.

Por exemplo, se você tiver um trabalho que exige um tipo específico de hardware de elementos gráficos, crie um rótulo personalizado chamado `gpu` e atribua-o aos executores que têm o hardware instalado. Um executor auto-hospedado que corresponde a todas as etiquetas atribuídas será elegível para executar o trabalho.

Este exemplo mostra um trabalho que combina etiquetas-padrão e etiquetas personalizadas:

```yaml
runs-on: [self-hosted, linux, x64, gpu]
```

* `self-hosted`: Execute esta tarefa em um servidor de execuções auto-hospedado.
* `linux` – Use apenas um executor baseado em Linux.
* `x64` – Use apenas um executor baseado no hardware x64.
* `gpu` – esse rótulo personalizado foi atribuído manualmente aos executores auto-hospedados com o hardware de GPU instalado.

Esses rótulos operam cumulativamente. Portanto, um executor auto-hospedado precisa ter todos os quatro rótulos para estar qualificado a processar o trabalho.

## Como usar grupos para rotear trabalhos { #using-groups-to-route-jobs }

Neste exemplo, foram adicionados executores a um grupo chamado `build-runners`. A chave `runs-on` envia o trabalho para qualquer executor disponível no grupo `build-runners`:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: build-runners
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

## Como usar rótulos e grupos para rotear trabalhos { #using-labels-and-groups-to-route-jobs }

Quando você combina grupos e rótulos, o executor deve atender aos dois requisitos para ser qualificado para executar o trabalho.

Neste exemplo, a `runs-on` chave combina `group` e `labels` , portanto, o trabalho é roteado para qualquer executor disponível dentro do grupo que também tenha um rótulo correspondente:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: ubuntu-runners
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```
