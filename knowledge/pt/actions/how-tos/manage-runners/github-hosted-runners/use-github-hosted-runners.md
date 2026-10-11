---
title: Usar executores hospedados no GitHub
description: Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Usar executores hospedados no GitHub

_Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub._

## Usando um executor hospedado em GitHub

Para usar um GitHubexecutor hospedado, crie um trabalho e use `runs-on` para especificar o tipo de executor que processará o trabalho, como `ubuntu-latest`, `windows-latest`ou `macos-latest`. Para obter a lista completa de tipos de executores, consulte [Referência de executores hospedados pelo GitHub](../../../reference/runners/github-hosted-runners.md#supported-runners-and-hardware-resources). Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para uso em fluxos de trabalho no repositório. Para obter mais informações, consulte [Exibindo os executores disponíveis para um repositório](#viewing-available-runners-for-a-repository).

Quando o trabalho é iniciado, GitHub provisiona automaticamente uma nova VM para esse trabalho. Todas as etapas da tarefa são executadas na VM, permitindo que as etapas dessa tarefa compartilhem informações usando o sistema de arquivos do executor. Você pode executar fluxos de trabalho diretamente na VM ou em um contêiner do Docker. Quando o trabalho for concluído, a VM será desativada automaticamente.

O diagrama a seguir demonstra como dois trabalhos em um fluxo de trabalho são executados em dois executores hospedados diferentes GitHub.

![Diagrama de um fluxo de trabalho que consiste em dois trabalhos. Um trabalho é executado no Ubuntu e o outro no Windows.](/assets/images/help/actions/overview-github-hosted-runner.png)

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

![Captura de tela da execução de um fluxo de trabalho. As etapas para o trabalho "Executar PSScriptAnalyzer no Windows" são exibidas.](/assets/images/help/repository/actions-runner-output.png)

O aplicativo de executor do GitHub Actions tem código aberto. Você pode contribuir e apresentar problemas no repositório do [executor](https://github.com/actions/runner).

## Exibindo executores disponíveis para um repositório

Se você tiver `repo: write` acesso a um repositório, poderá exibir uma lista dos executores disponíveis para o repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-server" aria-label="server" role="img"><path d="M1.75 1h12.5c.966 0 1.75.784 1.75 1.75v4c0 .372-.116.717-.314 1 .198.283.314.628.314 1v4a1.75 1.75 0 0 1-1.75 1.75H1.75A1.75 1.75 0 0 1 0 12.75v-4c0-.358.109-.707.314-1a1.739 1.739 0 0 1-.314-1v-4C0 1.784.784 1 1.75 1ZM1.5 2.75v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25H1.75a.25.25 0 0 0-.25.25Zm.25 5.75a.25.25 0 0 0-.25.25v4c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25v-4a.25.25 0 0 0-.25-.25ZM7 4.75A.75.75 0 0 1 7.75 4h4.5a.75.75 0 0 1 0 1.5h-4.5A.75.75 0 0 1 7 4.75ZM7.75 10h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM3 4.75A.75.75 0 0 1 3.75 4h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 4.75ZM3.75 10h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path></svg> Runners**.
4. Revise a lista de executores hospedados no GitHub disponíveis para o repositório.
5. Opcionalmente, para copiar o rótulo de um corredor para usá-lo em um fluxo de trabalho, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> à direita do corredor e clique em **Copiar rótulo**.

> \[!NOTE]
> Os proprietários em nível de empresas e organizações, podem criar executores nesta página. Para criar um novo executor, clique em **Novo executor**, no canto superior direito da lista de executores, para adicionar executores ao repositório.
>
> Para obter mais informações, consulte [Gerenciar executores maiores](../larger-runners/manage-larger-runners.md) e [Adicionar executores auto-hospedados](../self-hosted-runners/add-runners.md).
