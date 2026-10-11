---
title: Compilar e testar aplicativos Xamarin
description: Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu aplicativo Xamarin.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/xamarin-apps
captured: '2026-10-11'
section: GitHub Actions
---

# Compilar e testar aplicativos Xamarin

_Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu aplicativo Xamarin._

## Introdução

Este guia mostra como criar um fluxo de trabalho que executa a CI (integração contínua) para seu projeto de Xamarin. O fluxo de trabalho que você criar permitirá que você veja quando commits em um pull request gerarão falhas de criação ou de teste em comparação com o seu branch-padrão. Essa abordagem pode ajudar a garantir que seu código seja sempre saudável.

Para obter uma lista completa das versões do SDK do Xamarin disponíveis nos runners do macOS hospedados em GitHub Actions, consulte o arquivo README da versão do macOS que você deseja usar no [repositório Runner ImagesGitHub Actions](https://github.com/actions/runner-images/tree/main/images/macos).

## Pré-requisitos

Recomendamos que você tenha uma compreensão básica de Xamarin, .NET Core SDK, YAML, opções de configuração de fluxo de trabalho e como criar um arquivo de fluxo de trabalho. Para saber mais, veja:

* [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md)
* [Introdução ao .NET](https://dotnet.microsoft.com/learn)
* [Saiba mais sobre o Xamarin](https://dotnet.microsoft.com/learn/xamarin)

## Criando aplicativos Xamarin.iOS

O exemplo a seguir demonstra como alterar as versões padrão do SDK do Xamarin e construir um aplicativo Xamarin.iOS.

```yaml
name: Build Xamarin.iOS app

on: [push]

jobs:
  build:

    runs-on: macos-latest

    steps:
    - uses: actions/checkout@v6
    - name: Set default Xamarin SDK versions
      run: |
        $VM_ASSETS/select-xamarin-sdk-v2.sh --mono=6.12 --ios=14.10

    - name: Set default Xcode 12.3
      run: |
        XCODE_ROOT=/Applications/Xcode_12.3.0.app
        echo "MD_APPLE_SDK_ROOT=$XCODE_ROOT" >> $GITHUB_ENV
        sudo xcode-select -s $XCODE_ROOT

    - name: Setup .NET Core SDK 5.0.x
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '5.0.x'

    - name: Install dependencies
      run: nuget restore <sln_file_path>

    - name: Build
      run: msbuild <csproj_file_path> /p:Configuration=Debug /p:Platform=iPhoneSimulator /t:Rebuild
```

## Desenvolvendo aplicativos Xamarin.Android

O exemplo a seguir demonstra como alterar as versões padrão do SDK Xamarin e criar um Xamarin. Aplicativo Android.

```yaml
name: Build Xamarin.Android app

on: [push]

jobs:
  build:

    runs-on: macos-latest

    steps:
    - uses: actions/checkout@v6
    - name: Set default Xamarin SDK versions
      run: |
        $VM_ASSETS/select-xamarin-sdk-v2.sh --mono=6.10 --android=10.2

    - name: Setup .NET Core SDK 5.0.x
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '5.0.x'

    - name: Install dependencies
      run: nuget restore <sln_file_path>

    - name: Build
      run: msbuild <csproj_file_path> /t:PackageForAndroid /p:Configuration=Debug
```

## Especificando uma versão .NET

Para usar uma versão pré-instalada do SDK do .NET Core em um executor hospedado do GitHub, use a ação `setup-dotnet`. Essa ação localiza uma versão específica de .NET do cache de ferramentas em cada executor e adiciona os binários necessários a `PATH`. Estas alterações persistirão para o resto do trabalho.

A ação `setup-dotnet` é a maneira recomendada de usar o .NET com GitHub Actions, pois garante comportamento consistente em diferentes executores e versões diferentes do .NET. Se você estiver usando um executor auto-hospedado, deverá instalar .NET e adicioná-lo a `PATH`. Para obter mais informações, confira a ação [`setup-dotnet`](https://github.com/marketplace/actions/setup-net-core-sdk).
