---
title: Criar e testar PowerShell
description: Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do PowerShell.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/powershell
captured: '2026-10-11'
section: GitHub Actions
---

# Criar e testar PowerShell

_Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do PowerShell._

## Introdução

Este guia mostra como usar PowerShell para CI. Ele descreve como usar o Pester, instalar dependências, testar seu módulo e publicar no Galeria do PowerShell.

GitHubOs executores hospedados têm um cache de ferramentas com software pré-instalado, que inclui PowerShell e Pester.

Para ver a lista completa de softwares atualizados e as versões pré-instaladas do PowerShell and Pester, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos

Você deve estar familiarizado com YAML e a sintaxe para GitHub Actions. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Recomendamos que você tenha um entendimento básico de PowerShell e Pester. Para obter mais informações, consulte:

* [Introdução ao PowerShell](https://docs.microsoft.com/powershell/scripting/learn/ps101/01-getting-started)
* [Pester](https://pester.dev)

## Adicionar um fluxo de trabalho ao Pester

Para automatizar o seu teste com PowerShell e Pester, você pode adicionar um fluxo de trabalho que é executado toda vez que uma alteração é carregada no seu repositório. No exemplo a seguir, `Test-Path` é usado para verificar se um arquivo chamado `resultsfile.log` está presente.

Este exemplo de arquivo de fluxo de trabalho precisa ser adicionado ao diretório `.github/workflows/` do repositório:

```yaml
name: Test PowerShell on Ubuntu
on: push

jobs:
  pester-test:
    name: Pester test
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Perform a Pester test from the command-line
        shell: pwsh
        run: Test-Path resultsfile.log | Should -Be $true
      - name: Perform a Pester test from the Tests.ps1 file
        shell: pwsh
        run: |
          Invoke-Pester Unit.Tests.ps1 -Passthru
```

* `shell: pwsh` – Configura o trabalho para usar o PowerShell ao executar os comandos `run`.

* `run: Test-Path resultsfile.log` – Verifique se um arquivo chamado `resultsfile.log` está presente no diretório raiz do repositório.

* `Should -Be $true` – Usa o Pester para definir um resultado esperado. Se o resultado for inesperado, ele GitHub Actions sinaliza isso como um teste com falha. Por exemplo:

  ![Captura de tela de uma falha na execução do fluxo de trabalho para um teste do Pester. Relatórios de testes dizem: "Esperava-se $true, mas foi obtido $false" e "Erro: o processo foi concluído com o código de saída 1."](/assets/images/help/repository/actions-failed-pester-test-updated.png)

* `Invoke-Pester Unit.Tests.ps1 -Passthru` – Usa o Pester para executar testes definidos em um arquivo chamado `Unit.Tests.ps1`. Por exemplo, para executar o mesmo teste descrito acima, o `Unit.Tests.ps1` conterá o seguinte:

        ```powershell
  Describe "Check results file is present" {
      It "Check results file is present" {
          Test-Path resultsfile.log | Should -Be $true
      }
  }
  ```

## Locais de módulos do PowerShell

A tabela abaixo descreve os locais de vários módulos do PowerShell em cada runner hospedado em GitHub.

<div class="ghd-tool rowheaders">

|                                           | Ubuntu                                           | macOS                                             | Windows                                               |
| ----------------------------------------- | ------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------- |
| **Módulos do sistema do PowerShell**      | `/opt/microsoft/powershell/7/Modules/*`          | `/usr/local/microsoft/powershell/7/Modules/*`     | `C:\program files\powershell\7\Modules\*`             |
| **Módulos de complementos do PowerShell** | `/usr/local/share/powershell/Modules/*`          | `/usr/local/share/powershell/Modules/*`           | `C:\Modules\*`                                        |
| **Módulos instalados pelo usuário**       | `/home/runner/.local/share/powershell/Modules/*` | `/Users/runner/.local/share/powershell/Modules/*` | `C:\Users\runneradmin\Documents\PowerShell\Modules\*` |

</div>

> \[!NOTE]
> Nos runners do Ubuntu, os módulos Azure PowerShell são armazenados em `/usr/share/` em vez do local padrão dos módulos complementares do PowerShell (ou seja, `/usr/local/share/powershell/Modules/`).

## Instalar dependências

GitHubOs executores hospedados têm o PowerShell 7 e o Pester instalados. Você pode usar `Install-Module` para instalar dependências adicionais do Galeria do PowerShell antes de compilar e testar seu código.

> \[!NOTE]
> Os pacotes pré-instalados (como o Pester) usados pelos runners hospedados por GitHub são atualizados regularmente e podem introduzir alterações significativas. Como resultado, recomendamos que você sempre especifique as versões de pacote necessárias usando `Install-Module` com `-MaximumVersion`.

Você também pode armazenar dependências em cache para acelerar seu fluxo de trabalho. Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

Por exemplo, o seguinte trabalho instala os módulos `SqlServer` e `PSScriptAnalyzer`:

```yaml
jobs:
  install-dependencies:
    name: Install dependencies
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install from PSGallery
        shell: pwsh
        run: |
          Set-PSRepository PSGallery -InstallationPolicy Trusted
          Install-Module SqlServer, PSScriptAnalyzer
```

> \[!NOTE]
> Por padrão, nenhum repositório é confiável pelo PowerShell. Ao instalar módulos do Galeria do PowerShell, você deve definir explicitamente a política de instalação para `PSGallery` para `Trusted`.

### Memorizar dependências

Você pode armazenar as dependências do PowerShell em cache usando uma chave exclusiva, o que permite restaurar as dependências em fluxos de trabalho futuros com a ação [`cache`](https://github.com/marketplace/actions/cache). Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

O PowerShell armazena suas dependências em diferentes locais, dependendo do sistema operacional do executor. Por exemplo, a `path` localização usada no exemplo do Ubuntu a seguir será diferente em um sistema operacional Windows.

```yaml
steps:
  - uses: actions/checkout@v6
  - name: Setup PowerShell module cache
    id: cacher
    uses: actions/cache@v4
    with:
      path: "~/.local/share/powershell/Modules"
      key: ${{ runner.os }}-SqlServer-PSScriptAnalyzer
  - name: Install required PowerShell modules
    if: steps.cacher.outputs.cache-hit != 'true'
    shell: pwsh
    run: |
      Set-PSRepository PSGallery -InstallationPolicy Trusted
      Install-Module SqlServer, PSScriptAnalyzer -ErrorAction Stop
```

## Testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código.

### Usar o PSScriptAnalyzer para verificar código

O exemplo a seguir instala `PSScriptAnalyzer` e o usa para fazer lint de todos os arquivos `ps1` no repositório. Para obter mais informações, consulte [PSScriptAnalyzer no GitHub](https://github.com/PowerShell/PSScriptAnalyzer).

```yaml
  lint-with-PSScriptAnalyzer:
    name: Install and run PSScriptAnalyzer
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install PSScriptAnalyzer module
        shell: pwsh
        run: |
          Set-PSRepository PSGallery -InstallationPolicy Trusted
          Install-Module PSScriptAnalyzer -ErrorAction Stop
      - name: Lint with PSScriptAnalyzer
        shell: pwsh
        run: |
          Invoke-ScriptAnalyzer -Path *.ps1 -Recurse -Outvariable issues
          $errors   = $issues.Where({$_.Severity -eq 'Error'})
          $warnings = $issues.Where({$_.Severity -eq 'Warning'})
          if ($errors) {
              Write-Error "There were $($errors.Count) errors and $($warnings.Count) warnings total." -ErrorAction Stop
          } else {
              Write-Output "There were $($errors.Count) errors and $($warnings.Count) warnings total."
          }
```

## Empacotar dados do fluxo de trabalho como artefatos

Você pode fazer o upload de artefatos para visualização após a conclusão de um fluxo de trabalho. Por exemplo, é possível que você precise salvar os arquivos de registro, os despejos de núcleo, os resultados de teste ou capturas de tela. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

O exemplo a seguir demonstra como usar a ação `upload-artifact` para arquivar os resultados do teste recebidos de `Invoke-Pester`. Para obter mais informações, confira a [ação `upload-artifact`](https://github.com/actions/upload-artifact).

```yaml
name: Upload artifact from Ubuntu

on: [push]

jobs:
  upload-pester-results:
    name: Run Pester and upload results
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Test with Pester
        shell: pwsh
        run: Invoke-Pester Unit.Tests.ps1 -Passthru | Export-CliXml -Path Unit.Tests.xml
      - name: Upload test results
        uses: actions/upload-artifact@v4
        with:
          name: ubuntu-Unit-Tests
          path: Unit.Tests.xml
    if: ${{ always() }}
```

A função `always()` configura o trabalho para continuar o processamento mesmo se houver falhas de teste. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../reference/workflows-and-actions/expressions.md#always).

## Publicando no Galeria do PowerShell

Você pode configurar seu fluxo de trabalho para publicar o módulo do PowerShell no Galeria do PowerShell quando os testes de CI forem aprovados. Você pode usar segredos para armazenar quaisquer tokens ou credenciais necessárias para publicar seu pacote. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

O exemplo a seguir cria um pacote e usa `Publish-Module` para publicá-lo no Galeria do PowerShell:

```yaml
name: Publish PowerShell Module

on:
  release:
    types: [created]

jobs:
  publish-to-gallery:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Build and publish
        env:
          NUGET_KEY: ${{ secrets.NUGET_KEY }}
        shell: pwsh
        run: |
          ./build.ps1 -Path /tmp/samplemodule
          Publish-Module -Path /tmp/samplemodule -NuGetApiKey $env:NUGET_KEY -Verbose
```
