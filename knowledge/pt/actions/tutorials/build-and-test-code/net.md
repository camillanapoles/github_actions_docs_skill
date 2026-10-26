---
title: Criar e testar .NET
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto .NET.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/net
captured: '2026-10-26'
section: Tutorials / Build and test code
---

# Criar e testar .NET

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto .NET._

## Introdução

Este guia mostra como criar, testar e publicar um pacote no .NET.

Os executores hospedados do GitHub têm um cache de ferramentas com software pré-instalado, que inclui o SDK do .NET Core. Para ver a lista completa de programas de software atualizados e as versões pré-instaladas do SDK do .NET Core, consulte [software instalado nos executores hospedados do GitHub](../../concepts/runners/github-hosted-runners.md).

## Pré-requisitos

Você já deve estar familiarizado com a sintaxe YAML e como ela é usada com GitHub Actions. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md).

Recomendamos que você tenha um entendimento básico do .NET Core SDK. Para obter mais informações, confira [Introdução ao .NET](https://dotnet.microsoft.com/learn).

## Usando um modelo de fluxo de trabalho do .NET

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHubfornece um modelo de fluxo de trabalho para .NET que deve funcionar para a maioria dos projetos .NET. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "dotnet".

5. No fluxo de trabalho ".NET", clique em **Configurar**.

6. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão do .NET.

7. Clique em **Confirmar alterações**.

   O `dotnet.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Especificando uma versão do .NET

Para usar uma versão pré-instalada do SDK do .NET Core em um executor hospedado do GitHub, use a ação `setup-dotnet`. Essa ação localiza uma versão específica do .NET no cache de ferramentas em cada executor e adiciona os binários necessários a `PATH`. Estas alterações persistirão para o resto do trabalho.

A ação `setup-dotnet` é a maneira recomendada de usar o .NET com GitHub Actions, pois garante comportamento consistente em diferentes executores e versões diferentes do .NET. Se você estiver usando um executor auto-hospedado, precisará instalar o .NET e adicioná-lo a `PATH`. Para obter mais informações, consulte a ação [`setup-dotnet`](https://github.com/marketplace/actions/setup-net-core-sdk).

### Usar múltiplas versões do .NET

```yaml
name: dotnet package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: [ '3.1.x', '6.0.x' ]

    steps:
      - uses: actions/checkout@v6
      - name: Setup dotnet ${{ matrix.dotnet-version }}
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet-version }}
      # You can test your matrix by printing the current dotnet version
      - name: Display dotnet version
        run: dotnet --version
```

### Usar uma versão específica do .NET

Você pode configurar seu trabalho para usar uma versão específica do .NET, como `6.0.22`. Como alternativa, você pode usar a sintaxe da versão semântica para obter a última versão secundária. Este exemplo usa a versão mais recente do .NET 6.

```yaml
    - name: Setup .NET 6.x
      uses: actions/setup-dotnet@v4
      with:
        # Semantic version range syntax or exact version of a dotnet version
        dotnet-version: '6.x'
```

## Instalar dependências

Os executores hospedados do GitHub têm o gerenciador de pacotes NuGet instalado. Você pode usar o dotnet CLI para instalar dependências do registro do pacote NuGet antes de criar e testar seu código. Por exemplo, o YAML abaixo instala o pacote `Newtonsoft`.

```yaml
steps:
- uses: actions/checkout@v6
- name: Setup dotnet
  uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '6.0.x'
- name: Install dependencies
  run: dotnet add package Newtonsoft.Json --version 12.0.1
```

### Memorizar dependências

Você pode armazenar em cache dependências do NuGet para fluxos de trabalho futuros usando a entrada opcional `cache`. O cache requer um arquivo `packages.lock.json`. Se a ação não conseguir encontrar um arquivo de bloqueio correspondente, ela falhará.

Antes de habilitar cache:

1. No diretório que contém seu projeto ou solução, gere os arquivos de bloqueio localmente.

            ```shell
   dotnet restore --use-lock-file
   ```

2. Faça commit dos arquivos `packages.lock.json` gerados no repositório para que eles fiquem disponíveis quando o fluxo de trabalho for executado.

Para obter mais informações, consulte [Como bloquear dependências](https://learn.microsoft.com/nuget/consume-packages/package-references-in-project-files#locking-dependencies) na documentação do NuGet.

Por padrão, `setup-dotnet` procura um arquivo de bloqueio na raiz do repositório. Use `cache-dependency-path` para especificar arquivos de bloqueio em subdiretórios ou vários arquivos de bloqueio. O exemplo a seguir armazena em cache a pasta NuGet `global-packages` usando arquivos de bloqueio em todo o repositório e, em seguida, restaura as dependências no modo bloqueado.

Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

```yaml
steps:
- uses: actions/checkout@v6
- name: Setup dotnet
  uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '6.x'
    cache: true
    cache-dependency-path: '**/packages.lock.json'
- name: Restore dependencies
  run: dotnet restore --locked-mode
```

!!! note
    Dependendo do número de dependências, pode ser mais rápido usar o cache de dependências. "Os desenvolvedores de projetos com muitas dependências grandes poderão observar um aumento no desempenho, pois isso reduz o tempo necessário para fazer o download." Os projetos com menos dependências podem não ver um aumento significativo no desempenho e até mesmo ver um ligeiro diminuir devido à forma como o NuGet instala dependências armazenadas em cache. O desempenho varia de projeto para projeto.

## Criar e testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código. Este exemplo demonstra como usar `dotnet build` e `dotnet test` em um trabalho:

```yaml
steps:
- uses: actions/checkout@v6
- name: Setup dotnet
  uses: actions/setup-dotnet@v4
  with:
    dotnet-version: '6.0.x'
- name: Install dependencies
  run: dotnet restore
- name: Build
  run: dotnet build --no-restore
- name: Test with the dotnet CLI
  run: dotnet test --no-build
```

## Empacotar dados do fluxo de trabalho como artefatos

Após a conclusão de um fluxo de trabalho, você poderá fazer o upload dos artefatos resultantes para análise. Por exemplo, é possível que você precise salvar os arquivos de registro, os despejos de núcleo, os resultados de teste ou capturas de tela. O exemplo a seguir demonstra como você pode usar a ação `upload-artifact` para carregar os resultados do teste.

Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

```yaml
name: dotnet package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        dotnet-version: [ '3.1.x', '6.0.x' ]

    steps:
      - uses: actions/checkout@v6
      - name: Setup dotnet
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ matrix.dotnet-version }}
      - name: Install dependencies
        run: dotnet restore
      - name: Test with dotnet
        run: dotnet test --no-restore --logger trx --results-directory "TestResults-${{ matrix.dotnet-version }}"
      - name: Upload dotnet test results
        uses: actions/upload-artifact@v4
        with:
          name: dotnet-results-${{ matrix.dotnet-version }}
          path: TestResults-${{ matrix.dotnet-version }}
        # Use always() to always run this step to publish test results when there are test failures
        if: ${{ always() }}
```

## Publicar nos registros do pacote

É possível configurar o seu fluxo de trabalho para publicar o pacote .NET em um registro de pacotes quando os testes de CI são aprovados. Você pode usar segredos do repositório para armazenar quaisquer tokens ou credenciais necessárias para publicar seu binário. O exemplo a seguir cria e publica um pacote para GitHub Packages usando `dotnet core cli`.

```yaml
name: Upload dotnet package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '6.0.x' # SDK Version to use.
          source-url: https://nuget.pkg.github.com/<owner>/index.json
        env:
          NUGET_AUTH_TOKEN: ${{secrets.GITHUB_TOKEN}}
      - run: dotnet build --configuration Release <my project>
      - name: Create the package
        run: dotnet pack --configuration Release <my project>
      - name: Publish the package to GPR
        run: dotnet nuget push <my project>/bin/Release/*.nupkg
```
