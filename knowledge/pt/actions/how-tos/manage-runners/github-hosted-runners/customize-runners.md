---
title: Personalizando executores hospedados no GitHub
description: Você pode instalar software adicional em executores hospedados em GitHub como parte do fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/customize-runners
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners
---

# Personalizando executores hospedados no GitHub

_Você pode instalar software adicional em executores hospedados em GitHub como parte do fluxo de trabalho._

Se você precisar de pacotes de software adicionais nos runners hospedados em GitHub, poderá criar um job que instale esses pacotes como parte do seu fluxo de trabalho.

Para ver os pacotes que já estão instalados por padrão, confira [Executores hospedados no GitHub](../../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

Este guia demonstra como criar um trabalho que instala software adicional em um executor hospedado em GitHub.

## Instalando software nos executores do Ubuntu

O exemplo a seguir demonstra como instalar um pacote `apt` como parte de um trabalho.

```yaml
name: Build on Ubuntu
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Install jq tool
        run: |
          sudo apt-get update
          sudo apt-get install jq
```

!!! note
    Sempre execute `sudo apt-get update` antes de instalar um pacote. Caso o índice `apt` esteja obsoleto, esse comando busca e indexa novamente todos os pacotes disponíveis, o que ajuda a evitar falhas de instalação do pacote.

## Instalando o software nos executores do macOS

O exemplo a seguir demonstra como instalar pacotes de Brew e cascas como parte de um trabalho.

```yaml
name: Build on macOS
on: push

jobs:
  build:
    runs-on: macos-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Install GitHub CLI
        run: |
          brew update
          brew install gh
      - name: Install Microsoft Edge
        run: |
          brew update
          brew install --cask microsoft-edge
```

## Instalando software em executores do Windows

O exemplo a seguir demonstra como usar o [Chocolatey](https://community.chocolatey.org/packages) para instalar a GitHub CLI como parte de um trabalho.

```yaml
name: Build on Windows
on: push
jobs:
  build:
    runs-on: windows-latest
    steps:
      - run: choco install gh
      - run: gh version
```
