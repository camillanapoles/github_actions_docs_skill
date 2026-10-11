---
title: Usar os executores auto-hospedados em um fluxo de trabalho
description: Para usar executores auto-hospedados em um fluxo de trabalho, você pode usar rótulos ou grupos para especificar o executor para uma tarefa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/use-in-a-workflow
captured: '2026-10-11'
section: GitHub Actions
---

# Usar os executores auto-hospedados em um fluxo de trabalho

_Para usar executores auto-hospedados em um fluxo de trabalho, você pode usar rótulos ou grupos para especificar o executor para uma tarefa._

## Exibindo executores disponíveis para um repositório

Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para o repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-server" aria-label="server" role="img"><path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v4c0 .372-.116.717-.314 1 .198.283.314.628.314 1v4a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 12.75v-4c0-.358.109-.707.314-1a1.739 1.739 0 0 1-.314-1v-4C0 1.784.784 1 1.75 1ZM1.5 2.75v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm.25 5.75a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25ZM7 4.75A.75.75 0 0 1 7.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5A.75.75 0 0 1 7 4.75ZM7.75 10h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM3 4.75A.75.75 0 0 1 3.75 4h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 4.75ZM3.75 10h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path></svg> Runners**.
4. Clique na guia **Auto-hospedado** na parte superior da lista de executores.
5. Revise a lista de executores auto-hospedados disponíveis para o repositório. Essa lista inclui os executores auto-hospedados e os conjuntos de dimensionamento de executores criados com Actions Runner Controller. Para saber mais, confira [Controlador de Ações Runner](../../../concepts/runners/actions-runner-controller.md).
6. Opcionalmente, para copiar o rótulo de um corredor para usá-lo em um fluxo de trabalho, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> à direita do corredor e clique em **Copiar rótulo**.

> \[!NOTE]
> Os proprietários em nível de empresas e organizações, podem criar executores nesta página. Para criar um novo executor, clique em **Novo executor**, no canto superior direito da lista de executores, para adicionar executores ao repositório.
>
> Para obter mais informações, consulte [Gerenciar executores maiores](../larger-runners/manage-larger-runners.md) e [Adicionar executores auto-hospedados](add-runners.md).

## Usar etiquetas-padrão para rotear tarefas

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

## Usar etiquetas personalizadas para rotear trabalhos

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

## Como usar grupos para rotear trabalhos

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

## Como usar rótulos e grupos para rotear trabalhos

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
