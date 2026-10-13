---
title: Publicando pacotes de Java com o Maven
description: Neste tutorial, você aprenderá a usar o Maven para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/publish-packages/publish-java-packages-with-maven
captured: '2026-10-11'
section: Tutorials / Publish packages
---

# Publicando pacotes de Java com o Maven { #publishing-java-packages-with-maven }

_Neste tutorial, você aprenderá a usar o Maven para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua)._

## Introdução { #introduction }

Este guia mostra como criar um fluxo de trabalho que publica pacotes Java no GitHub Packages e no Maven Central Repository. Com um único fluxo de trabalho, você pode publicar pacotes em um único repositório ou em vários repositórios.

> [!WARNING] Os exemplos usados neste guia referem-se ao serviço OSSRH herdado. Consulte [Publicação](https://central.sonatype.org/faq/what-is-different-between-central-portal-and-legacy-ossrh/#publishing) na documentação do Repositório Central do Maven.

## Pré-requisitos { #prerequisites }

Recomendamos que você tenha um entendimento básico dos arquivos de fluxo de trabalho e das opções de configuração. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Para obter mais informações sobre como criar um fluxo de trabalho de CI para seu projeto de Java com o Maven, consulte [Compilar e testar Java com o Maven](../build-and-test-code/java-with-maven.md).

Você também pode achar útil ter um entendimento básico do seguinte:

* [Trabalhando com o repositório do Apache Maven](https://docs.github.com/pt/packages/working-with-a-github-packages-registry/working-with-the-apache-maven-registry)
* [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md)
* [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
* [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md)

## Sobre a configuração do pacote { #about-package-configuration }

Os campos `groupId` e `artifactId` do arquivo *pom.xml* criam um identificador exclusivo para o pacote que os registros usam para vincular seu pacote a um registro. Para obter mais informações, confira [Guia para upload de artefatos no Central Repository](https://maven.apache.org/repository/guide-central-repository-upload.html) na documentação do Apache Maven.

> [!WARNING] Seu pacote Apache Maven deve seguir a convenção de nomenclatura, portanto, o campo `artifactId` deve conter apenas letras minúsculas, dígitos ou hifens. Para obter mais informações, confira [Convenção de nomenclatura das coordenadas Maven](https://maven.apache.org/guides/mini/guide-naming-conventions.html) na documentação do maven.apache.org. Se você usar letras maiúsculas no nome do artefato, obterá uma resposta *422 Unprocessable Entity*.

O arquivo *pom.xml* também contém a configuração dos repositórios de gerenciamento de distribuição nos quais o Maven implantará os pacotes. Cada repositório deve ter um nome e uma URL de implementação. A autenticação para esses repositórios pode ser configurada no arquivo *.m2/settings.xml* no diretório inicial do usuário que executa o Maven.

Use a ação `setup-java` para configurar o repositório de implantação, bem como a autenticação para esse repositório. Para obter mais informações, confira [`setup-java`](https://github.com/actions/setup-java).

## Publicar pacotes no Repositório Central do Maven { #publishing-packages-to-the-maven-central-repository }

Cada vez que você criar uma nova versão, você poderá acionar um fluxo de trabalho para publicar o seu pacote. O fluxo de trabalho no exemplo abaixo é executado quando o evento `release` é disparado com o tipo `created`. O fluxo de trabalho publica o pacote no Repositório Central Maven se o teste de CI for aprovado. Para saber mais sobre o evento `release`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#release).

Neste fluxo de trabalho, você pode usar a ação `setup-java`. Essa ação instala a versão fornecida do JDK no `PATH`, mas também configura um *settings.xml* do Maven para pacotes de publicação. Por padrão, o arquivo de configurações será configurado para GitHub Packages, mas ele pode ser configurado para implantar em outro registro de pacote, como o Repositório Central do Maven. Se você já tiver um repositório de gerenciamento de distribuição configurado no *pom.xml*, especifique essa `id` durante a invocação da ação `setup-java`.

Por exemplo, se você estiver fazendo a implantação no Maven Central Repository por meio do projeto de hospedagem do OSSRH, o *pom.xml* poderá especificar um repositório de gerenciamento de distribuição com a `id` igual a `ossrh`.

```xml copy
<project ...>
  ...
  <distributionManagement>
    <repository>
      <id>ossrh</id>
      <name>Central Repository OSSRH</name>
      <url>https://oss.sonatype.org/service/local/staging/deploy/maven2/</url>
    </repository>
  </distributionManagement>
</project>
```

Com essa configuração, você pode criar um fluxo de trabalho que publica seu pacote no Maven Central Repository especificando o gerenciamento do repositório `id` para a ação `setup-java`. Você também deverá fornecer variáveis de ambiente que contenham o nome de usuário e senha para fazer a autenticação no repositório.

Na etapa de implementação, você deverá definir as variáveis de ambiente para o nome de usuário com o qual deseja fazer a autenticação no repositório e para um segredo que você configurou com a senha ou token para autenticação. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

```yaml copy
name: Publish package to the Maven Central Repository
on:
  release:
    types: [created]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Set up Maven Central Repository
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'
          server-id: ossrh
          server-username: MAVEN_USERNAME
          server-password: MAVEN_PASSWORD
      - name: Publish package
        run: mvn --batch-mode deploy
        env:
          MAVEN_USERNAME: ${{ secrets.OSSRH_USERNAME }}
          MAVEN_PASSWORD: ${{ secrets.OSSRH_TOKEN }}
```

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Configura o JDK Java e também configura o arquivo maven *settings.xml* para adicionar autenticação para o repositório `ossrh` usando as variáveis de ambiente `MAVEN_USERNAME` e `MAVEN_PASSWORD`.
3. Executa o comando `mvn --batch-mode deploy` a ser publicado no repositório `ossrh`. A variável de ambiente `MAVEN_USERNAME` será definida com o conteúdo do segredo `OSSRH_USERNAME`, e a variável de ambiente `MAVEN_PASSWORD` será definida com o conteúdo do segredo `OSSRH_TOKEN`.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Publicando pacotes para GitHub Packages { #publishing-packages-to-github-packages }

Cada vez que você criar uma nova versão, você poderá acionar um fluxo de trabalho para publicar o seu pacote. O fluxo de trabalho no exemplo abaixo é executado quando o evento `release` é disparado com o tipo `created`. O fluxo de trabalho publica o pacote para GitHub Packages se os testes de CI forem aprovados. Para saber mais sobre o evento `release`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#release).

Neste fluxo de trabalho, você pode usar a ação `setup-java`. Esta ação instala a versão especificada do JDK em `PATH` e também configura um *settings.xml* do Maven para publicar o pacote em GitHub Packages. O *settings.xml* gerado define a autenticação para um servidor com a `id``github`, usando a variável de ambiente `GITHUB_ACTOR` como nome de usuário e a variável de ambiente `GITHUB_TOKEN` como senha. A variável de ambiente `GITHUB_TOKEN` recebe o valor do segredo especial `GITHUB_TOKEN`.

O segredo `GITHUB_TOKEN` é definido como um token de acesso para o repositório sempre que um trabalho em um fluxo de trabalho é iniciado. Você deve definir as permissões desse token de acesso no arquivo de fluxo de trabalho para permitir acesso de leitura à permissão `contents` e acesso de gravação à permissão `packages`. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md).

Para um projeto baseado em Maven, você pode usar essas configurações criando um repositório de distribuição no arquivo *pom.xml* com um `id` de `github` que aponta para seu endpoint GitHub Packages.

Por exemplo, se sua organização for chamada de "octocat" e seu repositório for denominado "hello-world", a GitHub Packages configuração em *pom.xml* será semelhante ao exemplo abaixo.

```xml copy
<project ...>
  ...
  <distributionManagement>
    <repository>
      <id>github</id>
      <name>GitHub Packages</name>
      <url>https://maven.pkg.github.com/octocat/hello-world</url>
    </repository>
  </distributionManagement>
</project>
```

Com essa configuração, você pode criar um fluxo de trabalho que publique seu pacote em GitHub Packages usando o *settings.xml* gerado automaticamente.

```yaml copy
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
      - name: Publish package
        run: mvn --batch-mode deploy
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Configura o JDK Java e também configura automaticamente o arquivo Maven *settings.xml* para adicionar autenticação ao repositório Maven `github` para usar a variável de ambiente `GITHUB_TOKEN`.
3. Executa o comando `mvn --batch-mode deploy` para publicação no GitHub Packages. A variável de ambiente `GITHUB_TOKEN` será definida com o conteúdo do segredo `GITHUB_TOKEN`. A chave `permissions` especifica o acesso concedido ao `GITHUB_TOKEN`.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Publicação de pacotes no repositório Maven Central e GitHub Packages { #publishing-packages-to-the-maven-central-repository-and-github-packages }

Você pode publicar seus pacotes no Maven Central Repository e GitHub Packages usando a ação `setup-java` para cada repositório.

Verifique se o arquivo *pom.xml* inclui um repositório de gerenciamento de distribuição tanto para o seu repositório GitHub quanto para o provedor do Repositório Central do Maven. Por exemplo, se você implantar no Repositório Central por meio do projeto de hospedagem OSSRH, talvez você queira especificá-lo em um repositório de gerenciamento de distribuição com `id` definido como `ossrh`, e talvez queira especificar GitHub Packages em um repositório de gerenciamento de distribuição com `id` definido como `github`.

```yaml copy
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
      - name: Set up Java for publishing to Maven Central Repository
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'
          server-id: ossrh
          server-username: MAVEN_USERNAME
          server-password: MAVEN_PASSWORD
      - name: Publish to the Maven Central Repository
        run: mvn --batch-mode deploy
        env:
          MAVEN_USERNAME: ${{ secrets.OSSRH_USERNAME }}
          MAVEN_PASSWORD: ${{ secrets.OSSRH_TOKEN }}
      - name: Set up Java for publishing to GitHub Packages
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'
      - name: Publish to GitHub Packages
        run: mvn --batch-mode deploy
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Esse fluxo de trabalho chama a ação `setup-java` duas vezes. Sempre que a ação `setup-java` for executada, ela substituirá o arquivo *settings.xml* do Maven para publicação de pacotes. Para autenticação no repositório, o arquivo *settings.xml* referencia o repositório de gerenciamento de distribuição `id`, bem como o nome de usuário e a senha.

Este fluxo de trabalho realiza as etapas a seguir:

1. Verifica uma cópia do repositório do projeto.
2. Chama `setup-java` pela primeira vez. Isso configura o arquivo  *settings.xml* do Maven para o repositório `ossrh` e define as opções de autenticação para variáveis de ambiente definidas na próxima etapa.
3. Executa o comando `mvn --batch-mode deploy` a ser publicado no repositório `ossrh`. A variável de ambiente `MAVEN_USERNAME` será definida com o conteúdo do segredo `OSSRH_USERNAME`, e a variável de ambiente `MAVEN_PASSWORD` será definida com o conteúdo do segredo `OSSRH_TOKEN`.
4. Chama `setup-java` pela segunda vez. Isso configura automaticamente o arquivo *settings.xml* do Maven para GitHub Packages.
5. Executa o comando `mvn --batch-mode deploy` para publicação no GitHub Packages. A variável de ambiente `GITHUB_TOKEN` será definida com o conteúdo do segredo `GITHUB_TOKEN`. A chave `permissions` especifica o acesso concedido ao `GITHUB_TOKEN`.

   Para saber mais sobre como usar segredos em seu fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).
