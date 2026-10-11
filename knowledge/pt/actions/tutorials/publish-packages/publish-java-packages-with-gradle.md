---
title: Publicando pacotes Java com o Gradle
description: Neste tutorial, você aprenderá a usar o Gradle para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/publish-packages/publish-java-packages-with-gradle
captured: '2026-10-11'
section: Tutorials / Publish packages
---

# Publicando pacotes Java com o Gradle

_Neste tutorial, você aprenderá a usar o Gradle para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua)._

## Introdução

Este guia mostra como criar um fluxo de trabalho que publica pacotes Java no GitHub Packages e no Maven Central Repository. Com um único fluxo de trabalho, você pode publicar pacotes em um único repositório ou em vários repositórios.

> [!WARNING] Os exemplos usados neste guia referem-se ao serviço OSSRH herdado. Consulte [Publicação](https://central.sonatype.org/faq/what-is-different-between-central-portal-and-legacy-ossrh/#publishing) na documentação do Repositório Central do Maven.

## Pré-requisitos

Recomendamos que você tenha um entendimento básico dos arquivos de fluxo de trabalho e das opções de configuração. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Para obter mais informações sobre como criar um fluxo de trabalho de CI para seu projeto de Java com o Gradle, consulte [Compilar e testar Java com o Gradle](../build-and-test-code/java-with-gradle.md).

Você também pode achar útil ter um entendimento básico do seguinte:

* [Trabalhando com o repositório do Apache Maven](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-apache-maven-registry)
* [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md)
* [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
* [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md)

## Sobre a configuração do pacote

Os campos `groupId` e `artifactId` da seção `MavenPublication` do arquivo *build.gradle* criam um identificador exclusivo para o pacote que os registros usam para vincular seu pacote a um registro. Isso é semelhante aos campos `groupId` e `artifactId` do arquivo *pom.xml* do Maven. Para obter mais informações, confira o [Plug-in do Maven Publish](https://docs.gradle.org/current/userguide/publishing_maven.html) na documentação do Gradle.

O arquivo *build.gradle* também contém a configuração para os repositórios de gerenciamento de distribuição nos quais o Gradle publicará os pacotes. Cada repositório deve ter um nome, uma URL de implementação e e credenciais para autenticação.

## Publicar pacotes no Repositório Central do Maven

Cada vez que você criar uma nova versão, você poderá acionar um fluxo de trabalho para publicar o seu pacote. O fluxo de trabalho no exemplo abaixo é executado quando o evento `release` é disparado com o tipo `created`. O fluxo de trabalho publica o pacote no Repositório Central Maven se o teste de CI for aprovado. Para saber mais sobre o evento `release`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#release).

Você pode definir um novo repositório do Maven no bloco de publicação do arquivo *build.gradle* que aponta para o repositório de pacotes. Por exemplo, se você estiver fazendo a implantação no Maven Central Repository por meio do projeto de hospedagem do OSSRH, o *build.gradle* poderá especificar um repositório com o nome `"OSSRH"`.

```groovy copy
plugins {
  ...
  id 'maven-publish'
}

publishing {
  ...

  repositories {
    maven {
      name = "OSSRH"
      url = "https://oss.sonatype.org/service/local/staging/deploy/maven2/"
      credentials {
        username = System.getenv("MAVEN_USERNAME")
        password = System.getenv("MAVEN_PASSWORD")
      }
    }
  }
}
```

Com essa configuração, você pode criar um fluxo de trabalho que publica seu pacote no Maven Central Repository executando o comando `gradle publish`. Na etapa de implementação, você deverá definir variáveis de ambiente para o nome de usuário e senha ou token usado para fazer a autenticação no repositório do Maven. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

```yaml copy

# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Publish package to the Maven Central Repository
on:
  release:
    types: [created]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@017a9effdb900e5b5b2fddfb590a105619dca3c3 # v4.4.2

      - name: Publish package
        run: ./gradlew publish
        env:
          MAVEN_USERNAME: ${{ secrets.OSSRH_USERNAME }}
          MAVEN_PASSWORD: ${{ secrets.OSSRH_TOKEN }}
```

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Define o Java JDK.
3. Configura o ambiente Gradle. A ação [`gradle/actions/setup-gradle`](https://github.com/gradle/actions) trata do estado de cache entre as execuções de fluxos de trabalho e fornece um resumo com detalhes de todas as execuções do Gradle.
4. Executar a tarefa `publish` do Gradle para publicar no repositório Maven `OSSRH`. A variável de ambiente `MAVEN_USERNAME` será definida com o conteúdo do segredo `OSSRH_USERNAME`, e a variável de ambiente `MAVEN_PASSWORD` será definida com o conteúdo do segredo `OSSRH_TOKEN`.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Publicando pacotes para GitHub Packages

Cada vez que você criar uma nova versão, você poderá acionar um fluxo de trabalho para publicar o seu pacote. O fluxo de trabalho no exemplo abaixo é executado quando o evento `release` é disparado com o tipo `created`. O fluxo de trabalho publica o pacote para GitHub Packages se os testes de CI forem aprovados. Para saber mais sobre o evento `release`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#release).

Você pode definir um novo repositório Maven no bloco de publicação do *build.gradle* que aponta para GitHub Packages. Nessa configuração do repositório, também é possível aproveitar as variáveis de ambiente definidas na execução do fluxo de trabalho de CI. Use a variável de ambiente `GITHUB_ACTOR` como um nome de usuário e defina a variável de ambiente `GITHUB_TOKEN` com o segredo `GITHUB_TOKEN`.

O segredo `GITHUB_TOKEN` é definido como um token de acesso para o repositório sempre que um trabalho em um fluxo de trabalho é iniciado. Você deve definir as permissões desse token de acesso no arquivo de fluxo de trabalho para permitir acesso de leitura à permissão `contents` e acesso de gravação à permissão `packages`. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md).

Por exemplo, se sua organização for chamada de "octocat" e seu repositório for denominado "hello-world", a GitHub Packages configuração em *build.gradle* será semelhante ao exemplo abaixo.

```groovy copy
plugins {
  ...
  id 'maven-publish'
}

publishing {
  ...

  repositories {
    maven {
      name = "GitHubPackages"
      url = "https://maven.pkg.github.com/octocat/hello-world"
      credentials {
        username = System.getenv("GITHUB_ACTOR")
        password = System.getenv("GITHUB_TOKEN")
      }
    }
  }
}
```

Com essa configuração, você pode criar um fluxo de trabalho que publica seu pacote em GitHub Packages executando o comando `gradle publish`.

```yaml copy

# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Publish package to GitHub Packages
on:
  release:
    types: [created]
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'
      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@017a9effdb900e5b5b2fddfb590a105619dca3c3 # v4.4.2

      - name: Publish package
        run: ./gradlew publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Define o Java JDK.
3. Configura o ambiente Gradle. A ação [`gradle/actions/setup-gradle`](https://github.com/gradle/actions) trata do estado de cache entre as execuções de fluxos de trabalho e fornece um resumo com detalhes de todas as execuções do Gradle.
4. Executa a tarefa `publish` do Gradle para publicar em GitHub Packages. A variável de ambiente `GITHUB_TOKEN` será definida com o conteúdo do segredo `GITHUB_TOKEN`. A chave `permissions` especifica o acesso que o segredo `GITHUB_TOKEN` permitirá.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Publicação de pacotes no repositório Maven Central e GitHub Packages

Você pode publicar seus pacotes no Repositório Central do Maven e GitHub Packages configurando cada um em seu arquivo *build.gradle* .

Verifique se o arquivo *build.gradle* inclui um repositório para seu GitHub repositório e seu provedor de Repositório Central do Maven.

Por exemplo, se você fizer a implantação no Central Repository por meio do projeto de hospedagem do OSSRH, o ideal será especificá-lo em um repositório de gerenciamento de distribuição com o `name` definido como `OSSRH`. Se você implantar no GitHub Packages, talvez seja interessante especificá-lo em um repositório de gerenciamento de distribuição com `name` definido como `GitHubPackages`.

Se o nome da sua organização for "octocat" e o nome do seu repositório for "hello-world", a configuração contida em *build.gradle* será semelhante ao exemplo abaixo.

```groovy copy
plugins {
  ...
  id 'maven-publish'
}

publishing {
  ...

  repositories {
    maven {
      name = "OSSRH"
      url = "https://oss.sonatype.org/service/local/staging/deploy/maven2/"
      credentials {
        username = System.getenv("MAVEN_USERNAME")
        password = System.getenv("MAVEN_PASSWORD")
      }
    }
    maven {
      name = "GitHubPackages"
      url = "https://maven.pkg.github.com/octocat/hello-world"
      credentials {
        username = System.getenv("GITHUB_ACTOR")
        password = System.getenv("GITHUB_TOKEN")
      }
    }
  }
}
```

Com essa configuração, você pode criar um fluxo de trabalho que publica seu pacote no Repositório Central do Maven e GitHub Packages executando o `gradle publish` comando.

```yaml copy

# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Publish package to the Maven Central Repository and GitHub Packages
on:
  release:
    types: [created]
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v6
      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'
      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@017a9effdb900e5b5b2fddfb590a105619dca3c3 # v4.4.2

      - name: Publish package
        run: ./gradlew publish
        env:
          MAVEN_USERNAME: ${{ secrets.OSSRH_USERNAME }}
          MAVEN_PASSWORD: ${{ secrets.OSSRH_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Define o Java JDK.
3. Configura o ambiente Gradle. A ação [`gradle/actions/setup-gradle`](https://github.com/gradle/actions) trata do estado de cache entre as execuções de fluxos de trabalho e fornece um resumo com detalhes de todas as execuções do Gradle.
4. Executa a tarefa `publish` do Gradle para publicar no repositório Maven `OSSRH` e no GitHub Packages. A variável de ambiente `MAVEN_USERNAME` será definida com o conteúdo do segredo `OSSRH_USERNAME`, e a variável de ambiente `MAVEN_PASSWORD` será definida com o conteúdo do segredo `OSSRH_TOKEN`. A variável de ambiente `GITHUB_TOKEN` será definida com o conteúdo do segredo `GITHUB_TOKEN`. A chave `permissions` especifica o acesso que o segredo `GITHUB_TOKEN` permitirá.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).
