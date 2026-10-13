---
title: Compilar e testar Java com o Gradle
description: Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Gradle.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/java-with-gradle
captured: '2026-10-13'
section: Tutorials / Build and test code
---

# Compilar e testar Java com o Gradle

_Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Gradle._

## Introdução

Este guia mostra como criar um fluxo de trabalho que executa a CI (integração contínua) para seu projeto de Java usando o sistema de build Gradle. O fluxo de trabalho que você criar permitirá que você veja quando commits em um pull request gerarão falhas de criação ou de teste em comparação com o seu branch-padrão. Essa abordagem pode ajudar a garantir que seu código seja sempre saudável. Você pode estender seu fluxo de trabalho de CI para armazenar arquivos em cache e carregar artefatos de uma execução de fluxo de trabalho.

Os executores hospedados do GitHub têm um cache de ferramentas com software pré-instalado, que inclui o JDKs (Kits de Desenvolvimento Java) e Gradle. Para obter uma lista de softwares e das versões pré-instaladas para JDK e Gradle, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos

Você deve estar familiarizado com YAML e a sintaxe para GitHub Actions. Para saber mais, veja:

* [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md)
* [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md)

Recomendamos que você tenha uma compreensão básica do Java e da estrutura Gradle. Para obter mais informações, consulte o [Manual do Usuário do Gradle](https://docs.gradle.org/current/userguide/userguide.html).

## Usando um modelo de fluxo de trabalho do Gradle

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para Gradle que deve funcionar para a maioria dos projetos Java com Gradle. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise "Java com Gradle".

5. No fluxo de trabalho "Java com Gradle", clique em **Configure**.
   Este fluxo de trabalho realiza as etapas a seguir:

6. Verifica uma cópia do repositório do projeto.

7. Define o Java JDK.

8. Configura o ambiente Gradle. A ação [`gradle/actions/setup-gradle`](https://github.com/gradle/actions) trata do estado de cache entre as execuções de fluxos de trabalho e fornece um resumo com detalhes de todas as execuções do Gradle.

9. A etapa “Compilar com o Gradle” executa a tarefa `build` usando o [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html).

10. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão do Java.

!!! note

    >
    > * Este modelo de fluxo de trabalho contém uma ação que não é certificada por GitHub. Elas são fornecidas por terceiros e regidas por termos de serviço, política de privacidade e documentação de suporte separados.
    > * Caso use ações de terceiros, você deverá usar uma versão especificada por um SHA de commit. Se a ação for revisada e você quiser usar a versão mais recente, será necessário atualizar o SHA. Você pode especificar uma versão fazendo referência a uma tag ou branch, mas a ação pode ser alterada sem aviso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#using-third-party-actions).

11. Clique em **Confirmar alterações**.

    O `gradle.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

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

O modelo de fluxo de trabalho executará a tarefa `build` por padrão. Na configuração-padrão do Gradle, este comando irá baixar dependências, criar classes, executar testes e classes de pacotes em seu formato distribuível, como, por exemplo, um arquivo JAR.

Se você usa comandos diferentes para criar seu projeto ou se você desejar usar uma atividade diferente, você poderá especificá-los. Por exemplo, você pode querer executar a tarefa `package` que está configurada no arquivo `ci.gradle`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
steps:
  - uses: actions/checkout@v6
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'

  - name: Setup Gradle
    uses: gradle/actions/setup-gradle@017a9effdb900e5b5b2fddfb590a105619dca3c3 # v4.4.2

  - name: Build with Gradle
    run: ./gradlew -b ci.gradle package
```

```
## Memorizar dependências

Suas dependências de build podem ser armazenadas em cache para acelerar as execuções dos seus fluxos de trabalho. Após uma execução bem-sucedida, `gradle/actions/setup-gradle` armazena em cache partes importantes do diretório base do usuário do Gradle. Em trabalhos futuros, o cache será restaurado para que os scripts de compilação não precisem ser recalculados e as dependências não precisem ser baixadas a partir de repositórios remotos de pacotes.

O cache é habilitado por padrão quando a ação `gradle/actions/setup-gradle` é usada. Para obter mais informações, consulte [`gradle/actions/setup-gradle`](https://github.com/gradle/actions/blob/main/setup-gradle/README.md#caching-build-state-between-jobs).

## Empacotar dados do fluxo de trabalho como artefatos

Depois que o build tiver sido bem-sucedido e seus testes tiverem sido aprovados, talvez você queira carregar os pacotes de Java resultantes como um artefato de build. Isso armazenará os pacotes criados como parte da execução do fluxo de trabalho e permitirá que você faça o download desses pacotes. Os artefatos podem ajudá-lo a testar e depurar os pull requests no seu ambiente local antes de serem mesclados. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

Em geral, o Gradle criará arquivos de saída como JARs, EARs ou WARs no diretório `build/libs`. Você pode carregar o conteúdo desse diretório usando a ação `upload-artifact`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
steps:
  - uses: actions/checkout@v6
  - uses: actions/setup-java@v4
    with:
      java-version: '17'
      distribution: 'temurin'

  - name: Setup Gradle
    uses: gradle/actions/setup-gradle@017a9effdb900e5b5b2fddfb590a105619dca3c3 # v4.4.2

  - name: Build with Gradle
    run: ./gradlew build

  - name: Upload build artifacts
    uses: actions/upload-artifact@v4
    with:
      name: Package
      path: build/libs
```
```
