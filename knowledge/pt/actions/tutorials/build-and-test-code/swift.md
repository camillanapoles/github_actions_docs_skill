---
title: Construção e teste Swift
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Swift.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/swift
captured: '2026-10-13'
section: Tutorials / Build and test code
---

# Construção e teste Swift { #building-and-testing-swift }

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Swift._

## Introdução { #introduction }

Este guia mostra como criar e testar um pacote do Swift.

Os executores hospedados do GitHub contam com um cache de ferramentas com ferramentas pré-instaladas, e os executores do Ubuntu e do macOS incluem as dependências para compilar pacotes Swift. Para ver a lista completa de softwares atualizados e as versões pré-instaladas do Swift e do Xcode, consulte [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos { #prerequisites }

Você já deve estar familiarizado com a sintaxe YAML e como ela é usada com GitHub Actions. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md).

Recomendamos que você tenha uma compreensão básica dos pacotes Swift. Para obter mais informações, consulte [Pacotes do Swift](https://developer.apple.com/documentation/xcode/swift-packages) na documentação do desenvolvedor da Apple.

## Usando um modelo de workflow do Swift { #using-a-swift-workflow-template }

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para Swift que deve funcionar para a maioria dos projetos Swift. As seções subsequentes deste guia fornecem exemplos de como personalizar esse modelo de workflow.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um workflow" mostra uma seleção de modelos de workflow recomendados. Pesquise por "swift".

5. Filtre a seleção de fluxos de trabalho clicando em **Integração contínua**.

6. No fluxo de trabalho "Swift", clique em **Configurar**.

7. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere o ramo no qual o fluxo de trabalho será executado.

8. Clique em **Confirmar alterações**.

   O `swift.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Especificando uma versão do Swift { #specifying-a-swift-version }

Para usar uma versão pré-instalada específica do Swift em um executor hospedado no GitHub, use a ação `swift-actions/setup-swift`. Essa ação localiza uma versão específica do Swift do cache de ferramentas no executor e adiciona os binários necessários a `PATH`. Estas alterações persistirão para o restante de um trabalho. Para obter mais informações, consulte a ação [`swift-actions/setup-swift`](https://github.com/marketplace/actions/setup-swift).

Se você estiver usando um executor auto-hospedado, precisará instalar as versões desejadas do Swift e adicioná-las a `PATH`.

Os exemplos abaixo demonstram o uso da ação `swift-actions/setup-swift`.

### Usando várias versões do Swift { #using-multiple-swift-versions }

Você pode configurar seu trabalho para usar várias versões do Swift em uma matriz.

```yaml copy

```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub. { #this-workflow-uses-actions-that-are-not-certified-by-github }
# São fornecidas por terceiros e regidas por { #they-are-provided-by-a-third-party-and-are-governed-by }
# termos de serviço, política de privacidade e suporte separados { #separate-terms-of-service-privacy-policy-and-support }
# online. { #documentation }

# O GitHub recomenda fixar ações em um SHA de commit. { #github-recommends-pinning-actions-to-a-commit-sha }
# Para obter uma versão mais recente, você precisará atualizar o SHA. { #to-get-a-newer-version-you-will-need-to-update-the-sha }
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso. { #you-can-also-reference-a-tag-or-branch-but-the-action-may-change-without-warning }

name: Swift

on: [push]

jobs:
  build:
    name: Swift ${{ matrix.swift }} on ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest]
        swift: ["5.2", "5.3"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: swift-actions/setup-swift@65540b95f51493d65f5e59e97dcef9629ddf11bf
        with:
          swift-version: ${{ matrix.swift }}
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

```
### Usando uma única versão específica do Swift { #using-a-single-specific-swift-version }

Você pode configurar seu trabalho para usar uma só versão específica do Swift, como `5.3.3`.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub. { #this-workflow-uses-actions-that-are-not-certified-by-github-1 }
# São fornecidas por terceiros e regidas por { #they-are-provided-by-a-third-party-and-are-governed-by-1 }
# termos de serviço, política de privacidade e suporte separados { #separate-terms-of-service-privacy-policy-and-support-1 }
# online. { #documentation-1 }
steps:
  - uses: swift-actions/setup-swift@65540b95f51493d65f5e59e97dcef9629ddf11bf
    with:
      swift-version: "5.3.3"
  - name: Get swift version
    run: swift --version # Swift 5.3.3
```

```
## Criar e testar seu código { #building-and-testing-your-code }

Você pode usar os mesmos comandos usados localmente para criar e testar seu código usando o Swift. Este exemplo demonstra como usar `swift build` e `swift test` em um trabalho:

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub. { #this-workflow-uses-actions-that-are-not-certified-by-github-2 }
# São fornecidas por terceiros e regidas por { #they-are-provided-by-a-third-party-and-are-governed-by-2 }
# termos de serviço, política de privacidade e suporte separados { #separate-terms-of-service-privacy-policy-and-support-2 }
# online. { #documentation-2 }
steps:
  - uses: actions/checkout@v6
  - uses: swift-actions/setup-swift@65540b95f51493d65f5e59e97dcef9629ddf11bf
    with:
      swift-version: "5.3.3"
  - name: Build
    run: swift build
  - name: Run tests
    run: swift test
```
```
