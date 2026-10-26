---
title: Usar executores hospedados no GitHub
description: Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners
captured: '2026-10-26'
section: How tos / Manage runners / Github hosted runners
---

# Usar executores hospedados no GitHub

_Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub._

## Usando um executor hospedado em GitHub

Para usar um GitHubexecutor hospedado, crie um trabalho e use `runs-on` para especificar o tipo de executor que processará o trabalho, como `ubuntu-latest`, `windows-latest`ou `macos-latest`. Para obter a lista completa de tipos de executores, consulte [Referência de executores hospedados pelo GitHub](../../../reference/runners/github-hosted-runners.md#supported-runners-and-hardware-resources). Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para uso em fluxos de trabalho no repositório. Para obter mais informações, consulte [Exibindo os executores disponíveis para um repositório](#viewing-available-runners-for-a-repository).

Quando o trabalho é iniciado, GitHub provisiona automaticamente uma nova VM para esse trabalho. Todas as etapas da tarefa são executadas na VM, permitindo que as etapas dessa tarefa compartilhem informações usando o sistema de arquivos do executor. Você pode executar fluxos de trabalho diretamente na VM ou em um contêiner do Docker. Quando o trabalho for concluído, a VM será desativada automaticamente.

O diagrama a seguir demonstra como dois trabalhos em um fluxo de trabalho são executados em dois executores hospedados diferentes GitHub.

![Diagrama de um fluxo de trabalho que consiste em dois trabalhos. Um trabalho é executado no Ubuntu e o outro no Windows.](https://docs.github.com/assets/images/help/actions/overview-github-hosted-runner.png)

O fluxo de trabalho de exemplo a seguir tem dois trabalhos, nomeados `Run-npm-on-Ubuntu` e `Run-PSScriptAnalyzer-on-Windows`. Quando esse fluxo de trabalho é disparado, GitHub provisiona uma nova máquina virtual para cada trabalho.

* O trabalho nomeado `Run-npm-on-Ubuntu` é executado em uma VM Linux, porque o trabalho `runs-on:` especifica `ubuntu-latest`.
* O trabalho nomeado `Run-PSScriptAnalyzer-on-Windows` é executado em uma VM do Windows, porque o trabalho `runs-on:` especifica `windows-latest`.

```yaml copy
name: Run commands on different operating systems
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  Run-npm-on-Ubuntu:
    name: Run npm on Ubuntu
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm help

  Run-PSScriptAnalyzer-on-Windows:
    name: Run PSScriptAnalyzer on Windows
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install PSScriptAnalyzer module
        shell: pwsh
        run: |
          Set-PSRepository PSGallery -InstallationPolicy Trusted
          Install-Module PSScriptAnalyzer -ErrorAction Stop
      - name: Get list of rules
        shell: pwsh
        run: |
          Get-ScriptAnalyzerRule
```

Enquanto a tarefa é executada, os logs e a saída podem ser visualizados na UI GitHub:

![Captura de tela da execução de um fluxo de trabalho. As etapas para o trabalho "Executar PSScriptAnalyzer no Windows" são exibidas.](https://docs.github.com/assets/images/help/repository/actions-runner-output.png)

O aplicativo de executor do GitHub Actions tem código aberto. Você pode contribuir e apresentar problemas no repositório do [executor](https://github.com/actions/runner).

## Exibindo executores disponíveis para um repositório

Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para o repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **(server) Runners**.
4. Revise a lista de executores hospedados no GitHub disponíveis para o repositório.
5. Opcionalmente, para copiar o rótulo de um corredor para usá-lo em um fluxo de trabalho, clique em (More options) à direita do corredor e clique em **Copiar rótulo**.

!!! note
    Os proprietários em nível de empresas e organizações, podem criar executores nesta página. Para criar um novo executor, clique em **Novo executor**, no canto superior direito da lista de executores, para adicionar executores ao repositório.

    Para obter mais informações, consulte [Gerenciar executores maiores](../larger-runners/manage-larger-runners.md) e [Adicionar executores auto-hospedados](../self-hosted-runners/add-runners.md).
