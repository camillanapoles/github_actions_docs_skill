---
title: Escolhendo o executor para um trabalho
description: Defina o tipo de máquina que processará um trabalho no seu fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
captured: '2026-10-11'
section: How tos / Write workflows / Choose where workflows run
---

# Escolhendo o executor para um trabalho

_Defina o tipo de máquina que processará um trabalho no seu fluxo de trabalho._

## Visão geral

Use `jobs.<job_id>.runs-on` para definir o tipo de computador no qual o trabalho será executado.

* A máquina de destino pode ser um [GitHubrunner](#choosing-github-hosted-runners) hospedado, [executor avançado](#choosing-runners-in-a-group), ou um [runner auto-hospedado](#choosing-self-hosted-runners).

* Você pode selecionar os executores com base nos rótulos atribuídos a eles, em sua participação em um grupo ou em uma combinação desses critérios.

* Você pode fornecer `runs-on` como:
  * Uma única string
  * Uma única variável que contém uma cadeia de caracteres
  * Uma matriz de cadeias de caracteres, variáveis que contêm cadeias de caracteres ou uma combinação de ambas
  * um par de `key: value` usando as chaves `group` ou `labels`

* Se você especificar uma matriz de cadeias de caracteres ou variáveis, o fluxo de trabalho será executado em qualquer executor que corresponda a todos os valores `runs-on` especificados. Por exemplo, aqui o trabalho só será executado em um executor auto-hospedado que tenha os rótulos `linux`, `x64` e `gpu`:

        ```yaml
  runs-on: [self-hosted, linux, x64, gpu]
  ```

  Para obter mais informações, confira [Como escolher executores auto-hospedados](#choosing-self-hosted-runners).

* Você pode misturar cadeias de caracteres e variáveis em uma matriz. Por exemplo:

        ```yaml
  on:
    workflow_dispatch:
      inputs:
        chosen-os:
          required: true
          type: choice
          options:
          - Ubuntu
          - macOS

  jobs:
    test:
      runs-on: [self-hosted, "${{ inputs.chosen-os }}"]
      steps:
      - run: echo Hello world!
  ```

* Se você quiser executar seu fluxo de trabalho em vários computadores, use [`jobs.<job_id>.strategy`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategy).

!!! note
    Aspas não são necessárias em torno de cadeias de caracteres simples como`self-hosted`, mas são necessárias para expressões como`"${{ inputs.chosen-os }}"` .

## Escolhendo executores hospedados em GitHub

Se você usar um runner hospedado em GitHub, cada tarefa será executada em uma nova instância de uma imagem do runner especificada por `runs-on`.

O valor de runs-on, quando você estiver usando um runner hospedado pelo GitHub, é um rótulo de um fluxo de trabalho ou o nome de um grupo de executores. Os rótulos dos executores padrão hospedados em GitHub são exibidos nas tabelas a seguir.

Para saber mais, confira [Executores hospedados no GitHub](../../../concepts/runners/github-hosted-runners.md).

### Executores padrão hospedados GitHubpara repositórios públicos

Para repositórios públicos, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados com as especificações associadas.
Com exceção dos executores de CPU única, cada executor hospedado por GitHub é uma nova máquina virtual (VM) hospedada por GitHub. Processos de CPU única são hospedados em um contêiner em uma VM compartilhada—consulte [Referência de executores hospedados pelo GitHub](../../../reference/runners/github-hosted-runners.md#single-cpu-runners). O uso dos executores hospedados padrão GitHubé gratuito e ilimitado em repositórios públicos.

| **Máquina virtual/contêiner** | **Processador (CPU)** | **Memória (RAM)** | **Armazenamento (SSD)** | **Arquitetura** | **Rótulo do fluxo de trabalho** |
|-----------------------------|---------------------|-----------------|-----------------------|---------------|-------------------------------|
| Linux                         | 1                     | 5 GB              | 14 GB                   | x64             |                                 |
            `[ubuntu-slim](https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md)`
Linux

4

16 GB

14 GB

x64

```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-VS2026-Readme.md">windows-2025-vs2026</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td>arm64</td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-VS2026-Arm64-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

### Executores hospedados padrão GitHubpara  privados

Para  privados, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados em máquinas virtuais com as especificações associadas. Esses executores usam a alocação de minutos gratuitos da sua GitHub conta e, posteriormente, são cobrados a taxas por minuto de uso. Confira [Precificação do executor de ações](https://docs.github.com/pt/billing/reference/actions-runner-pricing).

| **Máquina virtual** | **Processador (CPU)** | **Memória (RAM)** | **Armazenamento (SSD)** | **Arquitetura** | **Rótulo do fluxo de trabalho** |
|-------------------|---------------------|-----------------|-----------------------|---------------|-------------------------------|
| Linux               | 1                     | 5 GB              | 14 GB                   | x64             |                                 |
            `[ubuntu-slim](https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md)`
Linux

2

8 GB

14 GB

x64

```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-VS2026-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

Além dos executores padrão hospedados em GitHub, GitHub oferece aos clientes dos planos GitHub Team e GitHub Enterprise Cloud uma variedade de máquinas virtuais gerenciadas com recursos avançados, como, por exemplo, mais núcleos e espaço em disco, máquinas com GPU e máquinas com arquitetura ARM. Para saber mais, confira [Executores avançados](../../../concepts/runners/larger-runners.md).

!!! note
    As imagens do executor `-latest` são as imagens estáveis mais recentes fornecidas pelo GitHub, e podem não ser a versão mais recente do sistema operacional disponível junto ao fornecedor do sistema operacional.

    [!WARNING]
    As imagens beta e preteridas são fornecidas “no estado em que se encontram”, “com todas as falhas” e “conforme disponível” e são excluídas do contrato de nível de serviço e da garantia. As imagens beta podem não estar cobertas pelo suporte ao cliente.

#### Exemplo: Especificar um sistema operacional

```yaml
runs-on: ubuntu-latest
```

Para saber mais, confira [Executores hospedados no GitHub](../../../concepts/runners/github-hosted-runners.md).

## Escolhendo executores auto-hospedados

Para especificar um executor auto-hospedado para uma tarefa, configure `runs-on` no arquivo do fluxo de trabalho utilizando rótulos do executor auto-hospedado.

Os executores auto-hospedados podem ter o rótulo `self-hosted`. Ao configurar um corredor auto-hospedado, por padrão, incluiremos o rótulo `self-hosted`. Você pode passar o sinalizador `--no-default-labels` para impedir que o rótulo auto-hospedado seja aplicado. Rótulos podem ser usados para criar opções de segmentação para os executores, como sistema operacional ou arquitetura. Recomendamos fornecer uma matriz de rótulos que comece com `self-hosted` (isso deve ser listado primeiro) e depois inclua rótulos adicionais, conforme necessário. Quando você especifica um array de rótulos, os trabalhos serão enfileirados em executores que possuem todos os rótulos que você especificou.

> [!NOTE] Actions Runner Controller não dá suporte ao `self-hosted` rótulo.

#### Exemplo: Usando etiquetas para seleção do executor

```yaml
runs-on: [self-hosted, linux]
```

Para saber mais, confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md) e [Usar os executores auto-hospedados em um fluxo de trabalho](../../manage-runners/self-hosted-runners/use-in-a-workflow.md).

## Escolher executores em um grupo

Você pode usar `runs-on` para direcionar grupos de executores para que o trabalho seja executado em qualquer executor que seja membro desse grupo. Para um controle mais granular, você também pode combinar grupos de executores com rótulos.

Os grupos de executores só podem ter [executor avançados](../../../concepts/runners/larger-runners.md) ou [executores auto-hospedados](../../manage-runners/self-hosted-runners.md) como membros.

#### Exemplo: usar grupos para controlar onde os trabalhos são executados

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

#### Exemplo: combinar grupos e rótulos

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
