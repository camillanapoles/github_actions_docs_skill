---
title: Compilar e testar Java com o Maven
description: Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Maven.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/java-with-maven
captured: '2026-10-26'
section: Tutorials / Build and test code
---

# Compilar e testar Java com o Maven

_Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Maven._

## Introdução

Este guia mostra como criar um fluxo de trabalho que executa a CI (integração contínua) para seu projeto de Java usando a ferramenta de gerenciamento de projeto de software Maven. O fluxo de trabalho que você criar permitirá que você veja quando commits em um pull request gerarão falhas de criação ou de teste em comparação com o seu branch-padrão. Essa abordagem pode ajudar a garantir que seu código seja sempre saudável. Você pode estender seu fluxo de trabalho de CI para arquivos de cache e enviar artefatos a partir da execução de um fluxo de trabalho.

GitHubOs servidores de execução hospedados têm um cache de ferramentas com software pré-instalado, que inclui Java Development Kits (JDKs) e Maven. Para obter uma lista de softwares e as versões pré-instaladas para JDK e Maven, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos

Você deve estar familiarizado com YAML e a sintaxe para GitHub Actions. Para saber mais, veja:

* [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md)
* [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md)

Recomendamos que você tenha uma compreensão básica do Java e da estrutura maven. Para obter mais informações, confira o [Guia de Introdução do Maven](https://maven.apache.org/guides/getting-started/index.html) na documentação do Maven.

## Usando um modelo de fluxo de trabalho do Maven

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para o Maven que deve funcionar para a maioria dos projetos Java com Maven. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "Java com Maven".

5. No fluxo de trabalho "Java com Maven", clique em **Configure**.

6. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão do Java.

7. Clique em **Confirmar alterações**.

   O `maven.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

### Como especificar a versão e a arquitetura da JVM

O modelo de fluxo de trabalho configura o `PATH` para conter OpenJDK 8 para a plataforma x64. Se você quiser usar uma versão diferente do Java, ou escolher uma arquitetura diferente (`x64` ou `x86`), você pode usar a ação `setup-java` para escolher um ambiente de execução Java diferente.

Por exemplo, para usar a versão 11 do JDK fornecida pelo Adoptium para a plataforma x64, você poderá usar a ação `setup-java` e configurar os parâmetros `java-version`, `distribution` e `architecture` para `'11'`, `'temurin'` e `x64`.

```yaml copy
steps:
  - uses: actions/checkout@v6
  - name: Set up JDK 11 for x64
    uses: actions/setup-java@v4
    with:
      java-version: '11'
      distribution: 'temurin'
      architecture: x64
```

Para obter mais informações, confira a ação [`setup-java`](https://github.com/actions/setup-java).

## Criar e testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código.

O modelo de fluxo de trabalho executará o destino `package` por padrão. Na configuração-padrão do Maven, este comando fará o download das dependências, criará classes, executará testes e classes de pacotes em seu formato distribuível, como, por exemplo, um arquivo JAR.

Se você usa comandos diferentes para criar seu projeto ou se desejar usar um alvo diferente, você poderá especificá-los. Por exemplo, você pode querer executar o alvo `verify` configurado em um arquivo `pom-ci.xml`.

```yaml copy
steps:
  - uses: actions/checkout@v6
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'
  - name: Run the Maven verify phase
    run: mvn --batch-mode --update-snapshots verify
```

## Memorizar dependências

Você pode armazenar as suas dependências para acelerar as execuções do seu fluxo de trabalho. Após uma execução bem-sucedida, seu repositório Maven local será armazenado em um cache. Para os fluxos de trabalho futuros, a cache será restaurada para que as dependências não precisem ser baixadas dos repositórios remotos do Maven. Você pode armazenar as dependências em cache simplesmente usando a [ação `setup-java`](https://github.com/marketplace/actions/setup-java-jdk) ou use a [ação `cache`](https://github.com/actions/cache) para uma configuração personalizada e mais avançada.

```yaml copy
steps:
  - uses: actions/checkout@v6
  - name: Set up JDK 17
    uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'
      cache: maven
  - name: Build with Maven
    run: mvn --batch-mode --update-snapshots verify
```

Esse fluxo de trabalho salvará o conteúdo do repositório do Maven local, localizado no `.m2` diretório do diretório base do executor. A chave de cache será o conteúdo em hash do `pom.xml`, ou seja, as alterações feitas no `pom.xml` invalidarão o cache.

## Empacotar dados do fluxo de trabalho como artefatos

Depois que o build tiver sido bem-sucedido e seus testes tiverem sido aprovados, talvez você queira carregar os pacotes de Java resultantes como um artefato de build. Isso armazenará os pacotes criados como parte da execução do fluxo de trabalho e permitirá que você faça o download desses pacotes. Os artefatos podem ajudá-lo a testar e depurar os pull requests no seu ambiente local antes de serem mesclados. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

Em geral, o Maven criará arquivos de saída como JARs, EARs ou WARs no diretório `target`. Para fazer o upload como artefatos, você pode copiá-los em um novo diretório que contém artefatos a serem subidos. Por exemplo, você pode criar um diretório chamado `staging`. Em seguida, você pode carregar o conteúdo desse diretório usando a ação `upload-artifact`.

```yaml copy
steps:
  - uses: actions/checkout@v6
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'
  - run: mvn --batch-mode --update-snapshots verify
  - run: mkdir staging && cp target/*.jar staging
  - uses: actions/upload-artifact@v4
    with:
      name: Package
      path: staging
```
