---
title: Executando variações de tarefas em um workflow
description: Crie uma matriz para definir as variações de cada trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations
captured: '2026-10-19'
section: How tos / Write workflows / Choose what workflows do
---

# Executando variações de tarefas em um workflow

_Crie uma matriz para definir as variações de cada trabalho._

## Sobre estratégias de matriz

Uma estratégia de matriz permite que você use variáveis em uma única definição de trabalho para criar automaticamente várias execuções de trabalho baseadas nas combinações das variáveis. Por exemplo, você pode usar uma estratégia de matriz para testar seu código em várias versões de um idioma ou em vários sistemas operacionais.

## Como adicionar uma estratégia de matriz ao seu trabalho de fluxo de trabalho

Use `jobs.<job_id>.strategy.matrix` para definir uma matriz de diferentes configurações de trabalho. Dentro de sua matriz, defina uma ou mais variáveis seguidas por uma matriz de valores. Por exemplo, a matriz a seguir tem uma variável chamada `version` com o valor `[10, 12, 14]` e uma variável chamada `os` com o valor `[ubuntu-latest, windows-latest]`:

```yaml
jobs:
  example_matrix:
    strategy:
      matrix:
        version: [10, 12, 14]
        os: [ubuntu-latest, windows-latest]
```

Um trabalho será executado para cada combinação possível das variáveis. Neste exemplo, o fluxo de trabalho executará seis trabalhos, um para cada combinação das variáveis `os` e `version`.

A matriz acima criará os trabalhos na ordem a seguir.

* `{version: 10, os: ubuntu-latest}`
* `{version: 10, os: windows-latest}`
* `{version: 12, os: ubuntu-latest}`
* `{version: 12, os: windows-latest}`
* `{version: 14, os: ubuntu-latest}`
* `{version: 14, os: windows-latest}`

Para obter informações de referência e exemplos, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrix).

## Usar contextos para criar matrizes

Para criar matrizes com informações sobre execuções de fluxo de trabalho, variáveis, ambientes de executor, trabalhos e etapas, acesse contextos usando a `${{ <context> }}` sintaxe de expressão. Para obter mais informações sobre contextos, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md).

Por exemplo, o workflow a seguir é acionado no evento `repository_dispatch` e usa informações do payload do evento para construir a matriz. Quando um evento de expedição de repositório é criado com um conteúdo como o abaixo, a variável da matriz `version` terá um valor de `[12, 14, 16]`. Para obter mais informações sobre o gatilho `repository_dispatch`, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md#repository_dispatch).

```json
{
  "event_type": "test",
  "client_payload": {
    "versions": [12, 14, 16]
  }
}
```

```yaml
on:
  repository_dispatch:
    types:
      - test

jobs:
  example_matrix:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: ${{ github.event.client_payload.versions }}
    steps:
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.version }}
```

## Expandir ou adicionar configurações de matriz

Para expandir as configurações de matriz existentes ou para adicionar novas configurações, use `jobs.<job_id>.strategy.matrix.include`. O valor de `include` é uma lista de objetos.

Por exemplo, considere a matriz a seguir.

```yaml
strategy:
  matrix:
    fruit: [apple, pear]
    animal: [cat, dog]
    include:
      - color: green
      - color: pink
        animal: cat
      - fruit: apple
        shape: circle
      - fruit: banana
      - fruit: banana
        animal: cat
```

Isso resultará em seis trabalhos com as combinações de matriz a seguir.

* `{fruit: apple, animal: cat, color: pink, shape: circle}`
* `{fruit: apple, animal: dog, color: green, shape: circle}`
* `{fruit: pear, animal: cat, color: pink}`
* `{fruit: pear, animal: dog, color: green}`
* `{fruit: banana}`
* `{fruit: banana, animal: cat}`

Cada entrada `include` foi aplicada das maneiras a seguir.

* `{color: green}` será adicionado a todas as combinações de matriz originais porque ele pode ser adicionado sem substituir nenhuma parte das combinações originais.
* `{color: pink, animal: cat}` adiciona `color:pink` apenas às combinações de matriz originais que incluem `animal: cat`. Isso substitui o `color: green` que foi adicionado pela entrada anterior `include`.
* `{fruit: apple, shape: circle}` adiciona `shape: circle` apenas às combinações de matriz originais que incluem `fruit: apple`.
* O `{fruit: banana}` não pode ser adicionado a nenhuma combinação de matriz original sem substituir um valor, portanto, ele é adicionado como uma combinação de matriz adicional.
* O `{fruit: banana, animal: cat}` não pode ser adicionado a nenhuma combinação de matriz original sem substituir um valor, portanto, ele é adicionado como uma combinação de matriz adicional. Ele não adiciona à combinação de matriz `{fruit: banana}` porque essa combinação não era uma das combinações de matriz originais.

Para obter referência e configurações de exemplo, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrixinclude).

## Excluindo configurações de matriz

Para remover configurações específicas definidas na matriz, use `jobs.<job_id>.strategy.matrix.exclude`.

Por exemplo, o fluxo de trabalho a seguir executará nove trabalhos: um trabalho para cada uma das 12 configurações, menos o trabalho excluído correspondente `{os: macos-latest, version: 12, environment: production}`e os dois trabalhos excluídos correspondentes `{os: windows-latest, version: 16}`.

```yaml
strategy:
  matrix:
    os: [macos-latest, windows-latest]
    version: [12, 14, 16]
    environment: [staging, production]
    exclude:
      - os: macos-latest
        version: 12
        environment: production
      - os: windows-latest
        version: 16
runs-on: ${{ matrix.os }}
```

Para obter informações de referência, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrixexclude)

## Usar uma saída para definir duas matrizes

Você pode usar a saída de um trabalho para definir matrizes para vários trabalhos.

Por exemplo, o fluxo de trabalho a seguir demonstra como definir uma matriz de valores em um trabalho, usar essa matriz em um segundo trabalho para produzir artefatos e então consumir esses artefatos em um terceiro trabalho. Cada artefato está associado a um valor da matriz.

```yaml copy
name: shared matrix
on:
  push:
  workflow_dispatch:

jobs:
  define-matrix:
    runs-on: ubuntu-latest

    outputs:
      colors: ${{ steps.colors.outputs.colors }}

    steps:
      - name: Define Colors
        id: colors
        run: |
          echo 'colors=["red", "green", "blue"]' >> "$GITHUB_OUTPUT"

  produce-artifacts:
    runs-on: ubuntu-latest
    needs: define-matrix
    strategy:
      matrix:
        color: ${{ fromJSON(needs.define-matrix.outputs.colors) }}

    steps:
      - name: Define Color
        env:
          color: ${{ matrix.color }}
        run: |
          echo "$color" > color
      - name: Produce Artifact
        uses: actions/upload-artifact@v4
        with:
          name: ${{ matrix.color }}
          path: color

  consume-artifacts:
    runs-on: ubuntu-latest
    needs:
    - define-matrix
    - produce-artifacts
    strategy:
      matrix:
        color: ${{ fromJSON(needs.define-matrix.outputs.colors) }}

    steps:
    - name: Retrieve Artifact
      uses: actions/download-artifact@v5
      with:
        name: ${{ matrix.color }}

    - name: Report Color
      run: |
        cat color
```

## Tratamento de falhas

Para controlar como as falhas de trabalho são tratadas, use `jobs.<job_id>.strategy.fail-fast` e `jobs.<job_id>.continue-on-error`.

Você pode usar `jobs.<job_id>.strategy.fail-fast` e `jobs.<job_id>.continue-on-error` juntos. Por exemplo, o fluxo de trabalho a seguir iniciará quatro trabalhos. Para cada trabalho, `continue-on-error` é determinado pelo valor de `matrix.experimental`. Se qualquer um dos trabalhos com `continue-on-error: false` falhar, todos os trabalhos que estiverem em andamento ou na fila serão cancelados. Se o trabalho com `continue-on-error: true` falhar, os outros trabalhos não serão afetados.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      fail-fast: true
      matrix:
        version: [6, 7, 8]
        experimental: [false]
        include:
          - version: 9
            experimental: true
```

Para obter informações de referência, confira [`jobs.<job_id>.strategy.fail-fast`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategyfail-fast) e [`jobs.<job_id>.continue-on-error`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontinue-on-error).

## Como definir o número máximo de trabalhos simultâneos

Para definir o número máximo de trabalhos que podem ser executados simultaneamente com uma estratégia de trabalho `matrix`, use `jobs.<job_id>.strategy.max-parallel`.

Por exemplo, o fluxo de trabalho a seguir executará no máximo dois trabalhos por vez, mesmo que haja executores disponíveis para executar todos os seis trabalhos ao mesmo tempo.

```yaml
jobs:
  example_matrix:
    strategy:
      max-parallel: 2
      matrix:
        version: [10, 12, 14]
        os: [ubuntu-latest, windows-latest]
```

Para obter informações de referência, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymax-parallel).
