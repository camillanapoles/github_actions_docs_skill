---
title: Como criar e testar projetos com o Go
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Go.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/go
captured: '2026-10-11'
section: GitHub Actions
---

# Como criar e testar projetos com o Go

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Go._

## Introdução

Este guia mostra como criar, testar e publicar um pacote Go.

Os executores hospedados do GitHub contam com um cache de ferramentas com software pré-instalado, que inclui as dependências necessárias para a linguagem Go. Para ver a lista completa de programas de software atualizados e as versões pré-instaladas do Go, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos

Você já deve estar familiarizado com a sintaxe YAML e como ela é usada com GitHub Actions. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md).

Recomendamos que você tenha um entendimento básico da linguagem Go. Para obter mais informações, confira [Introdução ao Go](https://golang.org/doc/tutorial/getting-started).

## Usando um modelo de fluxo de trabalho do Go

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho Go que deve funcionar para a maioria dos projetos Go. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "go".

5. Filtre a seleção de fluxos de trabalho clicando em **Integração contínua**.

6. No workflow "Go - by GitHub Actions", clique em **Configurar**.

   ![Captura de tela da página "Escolher um fluxo de trabalho". O botão "Configurar" no fluxo de trabalho "Go" é realçado com um contorno laranja.](/assets/images/help/actions/starter-workflow-go.png)

7. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão do Go.

8. Clique em **Confirmar alterações**.

   O `go.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Como especificar uma versão do Go

A maneira mais fácil de especificar uma versão go é usando a ação `setup-go` fornecida por GitHub. Para obter mais informações, confira a ação [`setup-go`](https://github.com/actions/setup-go/).

Para usar uma versão pré-instalada do Go em um runner hospedado no GitHub, passe a versão desejada na propriedade `go-version` da ação `setup-go`. Essa ação localiza uma versão específica do Go no cache de ferramentas em cada executor e adiciona os binários necessários a `PATH`. Estas alterações persistirão para o resto do trabalho.

A ação `setup-go` é a maneira recomendada de usar Go com GitHub Actions, pois ajuda a garantir um comportamento consistente entre diferentes executores e diferentes versões do Go. Se você estiver usando um executor auto-hospedado, precisará instalar o Go e adicioná-lo a `PATH`.

### Como usar várias versões do Go

```yaml copy
name: Go

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: [ '1.19', '1.20', '1.21.x' ]

    steps:
      - uses: actions/checkout@v6
      - name: Setup Go ${{ matrix.go-version }}
        uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go-version }}
      # You can test your matrix by printing the current Go version
      - name: Display Go version
        run: go version
```

### Como usar uma versão específica do Go

Você pode configurar o trabalho para usar uma versão específica do Go, como `1.20.8`. Como alternativa, você pode usar a sintaxe da versão semântica para obter a última versão secundária. Este exemplo usa a versão mais recente do patch do Go 1.21:

```yaml copy
      - name: Setup Go 1.21.x
        uses: actions/setup-go@v5
        with:
          # Semantic version range syntax or exact version of Go
          go-version: '1.21.x'
```

## Instalar dependências

Você pode usar `go get` para instalar dependências:

```yaml copy
    steps:
      - uses: actions/checkout@v6
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21.x'
      - name: Install dependencies
        run: |
          go get .
          go get example.com/octo-examplemodule
          go get example.com/octo-examplemodule@v1.3.4
```

### Memorizar dependências

Você pode armazenar em cache e restaurar as dependências usando a ação [`setup-go`](https://github.com/actions/setup-go). Por padrão, o cache é habilitado quando a ação `setup-go` é usada.

A ação `setup-go` procura o arquivo de dependência, `go.sum`, na raiz do repositório e usa o hash do arquivo de dependência como parte da chave de cache.

Use o parâmetro `cache-dependency-path` para casos em que vários arquivos de dependência são usados ou quando eles estão localizados em subdiretórios diferentes.

```yaml copy
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.17'
          cache-dependency-path: subdir/go.sum
```

Se houver uma necessidade específica ou precisar de controles mais precisos de cache, use a [ação `cache`](https://github.com/marketplace/actions/cache). Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

## Criar e testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código. Este fluxo de trabalho de exemplo demonstra como usar `go build` e `go test` em um trabalho:

```yaml copy
name: Go
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.21.x'
      - name: Install dependencies
        run: go get .
      - name: Build
        run: go build -v ./...
      - name: Test with the Go CLI
        run: go test
```

## Empacotar dados do fluxo de trabalho como artefatos

Após a conclusão de um fluxo de trabalho, você poderá fazer o upload dos artefatos resultantes para análise. Por exemplo, é possível que você precise salvar os arquivos de registro, os despejos de núcleo, os resultados de teste ou capturas de tela. O exemplo a seguir demonstra como você pode usar a ação `upload-artifact` para carregar os resultados do teste.

Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

```yaml copy
name: Upload Go test results

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: [ '1.19', '1.20', '1.21.x' ]

    steps:
      - uses: actions/checkout@v6
      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: ${{ matrix.go-version }}
      - name: Install dependencies
        run: go get .
      - name: Test with Go
        run: go test -json > TestResults-${{ matrix.go-version }}.json
      - name: Upload Go test results
        uses: actions/upload-artifact@v4
        with:
          name: Go-results-${{ matrix.go-version }}
          path: TestResults-${{ matrix.go-version }}.json
```
