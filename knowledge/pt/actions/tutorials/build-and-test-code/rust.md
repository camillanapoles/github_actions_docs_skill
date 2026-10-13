---
title: Como criar e testar o Rust
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do Rust.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/rust
captured: '2026-10-13'
section: Tutorials / Build and test code
---

# Como criar e testar o Rust { #building-and-testing-rust }

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do Rust._

## Introdução { #introduction }

Este guia mostra como criar, testar e publicar um pacote do Rust.

Os executores hospedados do GitHub contam com um cache de ferramentas com software pré-instalado, que inclui as dependências necessárias para a linguagem Rust. Para ver a lista completa de programas de software atualizados e as versões pré-instaladas do Rust, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos { #prerequisites }

Você já deve estar familiarizado com a sintaxe YAML e como ela é usada com GitHub Actions. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md).

Recomendamos que você tenha um entendimento básico da linguagem Rust. Para ver mais informações, confira [Introdução ao Rust](https://www.rust-lang.org/learn).

## Como usar um modelo de fluxo de trabalho do Rust { #using-a-rust-workflow-template }

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho do Rust que deve funcionar para a maioria dos projetos básicos do Rust. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise por "Rust".

5. Filtre a seleção de fluxos de trabalho clicando em **Integração contínua**.

6. No fluxo de trabalho "Rust – by GitHub Actions", clique em **Configurar**.

   ![Captura de tela da página "Escolher um fluxo de trabalho". O botão "Configurar" no fluxo de trabalho "Rust" é realçado com um contorno laranja.](https://docs.github.com/assets/images/help/actions/starter-workflow-rust.png)

7. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão do Rust.

8. Clique em **Confirmar alterações**.

   O `rust.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Como especificar uma versão do Rust { #specifying-a-rust-version }

Os executores hospedados do GitHub incluem uma versão recente do conjunto de ferramentas da linguagem Rust. Você pode usar o rustup para informar a versão instalada em um executador, substituir a versão e instalar diferentes cadeias de ferramentas. Para obter mais informações, confira [The rustup book](https://rust-lang.github.io/rustup/).

Este exemplo mostra as etapas que você pode usar para configurar o ambiente do executor para usar a compilação noturna do Rust e reportar a versão.

```yaml copy
      - name: Temporarily modify the rust toolchain version
        run: rustup override set nightly
      - name: Output rust version for educational purposes
        run: rustup --version
```

### Memorizar dependências { #caching-dependencies }

Você pode armazenar em cache e restaurar as dependências usando a ação Armazenar em cache. Este exemplo pressupõe que o repositório contém um arquivo `Cargo.lock`.

```yaml copy
      - name: Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            target
          key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

Se você tiver requisitos personalizados ou precisar de controles mais refinados para o cache, explore outras opções de configuração para a [ação `cache`](https://github.com/marketplace/actions/cache). Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

## Criar e testar seu código { #building-and-testing-your-code }

Você pode usar os mesmos comandos usados localmente para criar e testar seu código. Este fluxo de trabalho de exemplo demonstra como usar `cargo build` e `cargo test` em um trabalho:

```yaml copy
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        BUILD_TARGET: [release] # refers to a cargo profile
    outputs:
      release_built: ${{ steps.set-output.outputs.release_built }}
    steps:
      - uses: actions/checkout@v6
      - name: Build binaries in "${{ matrix.BUILD_TARGET }}" mode
        run: cargo build --profile ${{ matrix.BUILD_TARGET }}
      - name: Run tests in "${{ matrix.BUILD_TARGET }}" mode
        run: cargo test --profile ${{ matrix.BUILD_TARGET }}
```

A palavra-chave `release` usada neste exemplo corresponde a um perfil de carga. Você pode usar qualquer [perfil](https://doc.rust-lang.org/cargo/reference/profiles.html) definido no arquivo `Cargo.toml`.

## Como publicar seu pacote ou biblioteca em crates.io { #publishing-your-package-or-library-to-cratesio }

Depois de configurar o fluxo de trabalho para criar e testar seu código, use um segredo para fazer logon em [crates.io](https://crates.io/) e publicar seu pacote.

```yaml copy
      - name: Login into crates.io
        run: cargo login ${{ secrets.CRATES_IO }}
      - name: Build binaries in "release" mode
        run: cargo build -r
      - name: "Package for crates.io"
        run: cargo package # publishes a package as a tarball
      - name: "Publish to crates.io"
        run: cargo publish # publishes your crate as a library that can be added as a dependency
```

Se houver erros ao compilar e empacotar o crate, verifique os metadados no manifesto, arquivo `Cargo.toml`, confira [O formato de manifesto](https://doc.rust-lang.org/cargo/reference/manifest.html). Você também deve verificar seu arquivo `Cargo.lock`, veja [Cargo.toml vs Cargo.lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html).

## Empacotar dados do fluxo de trabalho como artefatos { #packaging-workflow-data-as-artifacts }

Após a conclusão de um fluxo de trabalho, você pode carregar os artefatos resultantes para análise ou para usar em outro fluxo de trabalho. Você pode adicionar essas etapas de exemplo ao fluxo de trabalho para carregar um aplicativo para uso por outro fluxo de trabalho.

```yaml copy
      - name: Upload release artifact
        uses: actions/upload-artifact@v4
        with:
          name: <my-app>
          path: target/${{ matrix.BUILD_TARGET }}/<my-app>
```

Para usar o artefato carregado em um trabalho diferente, verifique se os fluxos de trabalho têm as permissões certas para o repositório. Confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../authenticate-with-github_token.md). Você pode usar essas etapas de exemplo para baixar o aplicativo criado no fluxo de trabalho anterior e publicá-lo.GitHub

```yaml copy
      - uses: actions/checkout@v6
      - name: Download release artifact
        uses: actions/download-artifact@v5
        with:
          name: <my-app>
          path: ./<my-app>
      - name: Publish built binary to GitHub releases
      - run: |
          gh release create --generate-notes ./<my-app>/<my-project>#<my-app>
```
