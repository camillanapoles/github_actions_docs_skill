---
title: Como executar trabalhos em executores maiores
description: Identifique os executor avançados disponíveis e, em seguida, direcione os trabalhos para os executores corretos usando grupos de executores e rótulos de fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/larger-runners/use-larger-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Como executar trabalhos em executores maiores

_Identifique os executor avançados disponíveis e, em seguida, direcione os trabalhos para os executores corretos usando grupos de executores e rótulos de fluxo de trabalho._

## Identificando os executores disponíveis para um repositório

Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para o repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-server" aria-label="server" role="img"><path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v4c0 .372-.116.717-.314 1 .198.283.314.628.314 1v4a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 12.75v-4c0-.358.109-.707.314-1a1.739 1.739 0 0 1-.314-1v-4C0 1.784.784 1 1.75 1ZM1.5 2.75v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm.25 5.75a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25ZM7 4.75A.75.75 0 0 1 7.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5A.75.75 0 0 1 7 4.75ZM7.75 10h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM3 4.75A.75.75 0 0 1 3.75 4h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 4.75ZM3.75 10h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path></svg> Runners**.
4. Revise a lista de executores disponíveis para o repositório.
5. Opcionalmente, para copiar o rótulo de um corredor para usá-lo em um fluxo de trabalho, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> à direita do corredor e clique em **Copiar rótulo**.

> \[!NOTE]
> Os proprietários em nível de empresas e organizações, podem criar executores nesta página. Para criar um novo executor, clique em **Novo executor**, no canto superior direito da lista de executores, para adicionar executores ao repositório.
>
> Para obter mais informações, consulte [Gerenciar executores maiores](manage-larger-runners.md) e [Adicionar executores auto-hospedados](../self-hosted-runners/add-runners.md).

## Direcionando corredores maiores em um fluxo de trabalho

Depois de identificar os executor avançados que deseja usar, você pode direcioná-los em seu fluxo de trabalho com grupos de executores, rótulos de fluxo de trabalho ou ambos. Use grupos de executores para rotear trabalhos para um conjunto de executores, rótulos de fluxo de trabalho para executores de destino com um rótulo específico ou ambos quando um trabalho deve corresponder às duas condições.

Se um administrador tiver desativado os executores padrão hospedados em GitHub, você poderá usar apenas grupos de executores.

### Segmentação por grupo de runners

Faça referência ao nome do grupo de runners no seu fluxo de trabalho. Use isto quando quiser encaminhar uma tarefa para qualquer executor disponível de um grupo específico.

<div class="ghd-tool linux">

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

</div>

<div class="ghd-tool windows">

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

</div>

<div class="ghd-tool mac">

Neste exemplo, a `runs-on` chave envia o trabalho para qualquer executor disponível no `macos-build-runners` grupo:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on:
      group: macos-build-runners
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

</div>

### Direcionamento por rótulo de fluxo de trabalho

Faça referência a um rótulo de fluxo de trabalho em seu fluxo de trabalho quando quiser rotear um trabalho para os executores que compartilham um rótulo específico.

Executor avançados são atribuídos automaticamente a um rótulo de workflow que corresponde ao nome do runner.

<div class="ghd-tool linux">

Neste exemplo, a chave `runs-on` envia o trabalho para qualquer executor disponível ao qual tenha sido atribuído o rótulo `ubuntu-24.04-16core`.

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

</div>

<div class="ghd-tool windows">

Neste exemplo, a chave `runs-on` envia o trabalho para qualquer executor disponível ao qual tenha sido atribuído o rótulo `windows-2022-16core`.

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      labels: windows-2022-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

</div>

<div class="ghd-tool mac">

Para macOS executores avançados, você pode usar tanto os rótulos de fluxo de trabalho definidos em GitHub quanto o rótulo de fluxo de trabalho atribuído automaticamente com base no nome executor avançado que você define quando o cria. Para obter uma lista dos rótulos de fluxo de trabalho do macOS disponíveis, consulte [Referência de executores avançados](../../../reference/runners/larger-runners.md#available-macos-larger-runners-and-labels).

Neste exemplo, a `runs-on` chave envia o trabalho para qualquer executor disponível que tenha recebido o `macos-26-xlarge` rótulo.

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on: macos-26-xlarge
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

</div>

### Usar rótulos e grupos para controlar onde os trabalhos são executados

Use tanto rótulos quanto grupos quando um trabalho precisar ser executado somente em runners de um grupo específico que também tenham um rótulo específico. O executor deve atender a ambos os requisitos para estar apto a executar a tarefa.

<div class="ghd-tool linux">

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

</div>

<div class="ghd-tool windows">

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

</div>

<div class="ghd-tool mac">

Neste exemplo, a `runs-on` chave combina `group` e `labels` , portanto, o trabalho é roteado para qualquer executor disponível dentro do grupo que também tenha um rótulo correspondente:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on:
      group: macos-runners
      labels: macos-26-xlarge
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

</div>

## Leitura adicional

Para obter detalhes de sintaxe da `runs-on` chave, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on).

Para obter especificações, rótulos, limitações e informações de solução de problemas, consulte [Referência de executores avançados](../../../reference/runners/larger-runners.md).
