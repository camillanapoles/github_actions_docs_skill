---
title: Migrando de Azure Pipelines para GitHub Actions
description: GitHub Actions e Azure Pipelines compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-azure-pipelines
captured: '2026-10-19'
section: Tutorials / Migrate to github actions / Manual migrations
---

# Migrando de Azure Pipelines para GitHub Actions

_GitHub Actions e Azure Pipelines compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples._

## Introdução

Azure Pipelines e GitHub Actions ambos permitem criar fluxos de trabalho que criam, testam, publicam, liberam e implantam código automaticamente. Azure Pipelines e GitHub Actions compartilham algumas semelhanças na configuração do fluxo de trabalho:

* Os arquivos de configuração do fluxo de trabalho são gravados YAML e armazenados no repositório do código.
* Os fluxos de trabalho incluem um ou mais trabalhos.
* Os trabalhos incluem uma ou mais etapas ou comandos individuais.
* É possível reutilizar e compartilhar novamente etapas ou tarefas com a comunidade.

Para saber mais, confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md).

## Principais diferenças

Ao migrar de Azure Pipelines, considere as seguintes diferenças:

* Azure Pipelines dá suporte a um editor clássico, que permite definir sua configuração de CI em um editor de interface gráfica em vez de criar a definição de pipeline em um arquivo YAML.
  GitHub Actions usa arquivos YAML para definir fluxos de trabalho e não dá suporte a um editor gráfico.
* Azure Pipelines permite omitir alguma estrutura em definições de trabalho. Por exemplo, se você tem apenas um único trabalho, não é necessário definir o trabalho. Você precisa definir apenas as etapas.
  GitHub Actions requer uma configuração explícita e a estrutura YAML não pode ser omitida.
* Azure Pipelines dá suporte a *stages* definidos no arquivo YAML, que pode ser usado para criar fluxos de trabalho de implantação.
  GitHub Actions exige que você separe estágios em arquivos de fluxo de trabalho YAML separados.
* Os agentes de build locais do Azure Pipelines podem ser selecionados com base em suas capacidades.               Os runners auto-hospedados do GitHub Actions podem ser selecionados com rótulos.

## Migrar tarefas e processos

Trabalhos e etapas em Azure Pipelines são muito semelhantes aos trabalhos e etapas em GitHub Actions. Em ambos os sistemas, os trabalhos têm as características a seguir:

* Os trabalhos contêm uma série de etapas executadas em sequência.
* Os trabalhos são executados em máquinas virtuais separadas ou em contêineres separados.
* Por padrão, os trabalhos são executados em paralelo, mas podem ser configurados para serem executados sequencialmente.

## Migrar etapas de script

Você pode executar um script ou um comando de shell como uma etapa em um fluxo de trabalho. Em Azure Pipelines, as etapas de script podem ser especificadas usando a chave `script` ou com as chaves `bash`, `powershell` ou `pwsh`. Os scripts também podem ser especificados como uma entrada para a [tarefa do Bash](https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/bash?view=azure-devops) ou a [tarefa do PowerShell](https://docs.microsoft.com/azure/devops/pipelines/tasks/utility/powershell?view=azure-devops).

Em GitHub Actions, todos os scripts são especificados usando a `run` chave. Para selecionar um shell específico, você pode especificar a chave `shell` ao fornecer o script. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsrun).

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe do Azure Pipelines para etapas de script

```yaml
jobs:
  - job: scripts
    pool:
      vmImage: 'windows-latest'
    steps:
      - script: echo "This step runs in the default shell"
      - bash: echo "This step runs in bash"
      - pwsh: Write-Host "This step runs in PowerShell Core"
      - task: PowerShell@2
        inputs:
          script: Write-Host "This step runs in PowerShell"
```

### GitHub Actions sintaxe para etapas do script

```yaml
jobs:
  scripts:
    runs-on: windows-latest
    steps:
      - run: echo "This step runs in the default shell"
      - run: echo "This step runs in bash"
        shell: bash
      - run: Write-Host "This step runs in PowerShell Core"
        shell: pwsh
      - run: Write-Host "This step runs in PowerShell"
        shell: powershell
```

## Diferenças na manipulação de erros de script

No Azure Pipelines, os scripts podem ser configurados para erro se uma saída é enviada para `stderr`.
GitHub Actions não dá suporte a essa configuração.

O GitHub Actions configura shells como "falha rápida" sempre que possível, que interrompe o script imediatamente caso um dos comandos em um script saia com um código de erro. Por outro lado, Azure Pipelines requer configuração explícita para sair imediatamente em um erro. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#exit-codes-and-error-action-preference).

## Diferenças no shell padrão no Windows

Em Azure Pipelines, o shell padrão para scripts em plataformas Windows é o shell command (*cmd.exe*). EmGitHub Actions, o shell padrão para scripts em plataformas Windows é o PowerShell. O PowerShell tem várias diferenças em comandos integrados, expansão de variáveis e controle de fluxo.

Se você estiver rodando um comando simples, talvez seja possível executar um script do shell de comandos no PowerShell sem nenhuma alteração. Mas, na maioria dos casos, você precisará atualizar seu script com a sintaxe do PowerShell ou instruir GitHub Actions a executar o script com o shell de comando em vez do PowerShell. Faça isso especificando `shell` como `cmd`.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe do Azure Pipelines usando CMD por padrão

```yaml
jobs:
  - job: run_command
    pool:
      vmImage: 'windows-latest'
    steps:
      - script: echo "This step runs in CMD on Windows by default"
```

### GitHub Actions sintaxe para especificar o CMD

```yaml
jobs:
  run_command:
    runs-on: windows-latest
    steps:
      - run: echo "This step runs in PowerShell on Windows by default"
      - run: echo "This step runs in CMD on Windows explicitly"
        shell: cmd
```

Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsshell).

## Migração de condicionais e sintaxe de expressão

Azure Pipelines e GitHub Actions podem executar etapas condicionalmente. Em Azure Pipelines, expressões condicionais são especificadas usando a chave `condition`. Em GitHub Actions, expressões condicionais são especificadas usando a `if` chave.

Azure Pipelines usa funções dentro de expressões para executar etapas condicionalmente. Por outro lado, o GitHub Actions usa uma notação de infixo. Por exemplo, você deve substituir a função `eq` no Azure Pipelines pelo operador `==` em GitHub Actions.

Abaixo, há um exemplo da sintaxe para cada sistema.

### sintaxe Azure Pipelines para expressões condicionais

```yaml
jobs:
  - job: conditional
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - script: echo "This step runs with str equals 'ABC' and num equals 123"
        condition: and(eq(variables.str, 'ABC'), eq(variables.num, 123))
```

### GitHub Actions sintaxe para expressões condicionais

```yaml
jobs:
  conditional:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This step runs with str equals 'ABC' and num equals 123"
        if: ${{ env.str == 'ABC' && env.num == 123 }}
```

Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md).

## Dependências entre trabalhos

Tanto o Azure Pipelines quanto o GitHub Actions permitem que você defina dependências para uma tarefa. Em ambos os sistemas, os trabalhos são executados em paralelo por padrão, mas as dependências do trabalho podem ser especificadas explicitamente. Em Azure Pipelines, isso é feito com a chave `dependsOn`. Em GitHub Actions, isso é feito com a tecla `needs`.

Abaixo, há um exemplo da sintaxe para cada sistema. Os fluxos de trabalho iniciam um primeiro trabalho chamado `initial` e, quando esse trabalho for concluído, dois trabalhos chamados `fanout1` e `fanout2` serão executados. Por fim, quando esses trabalhos forem concluídos, o trabalho `fanin` será executado.

### A sintaxe do Azure Pipelines para dependências entre tarefas

```yaml
jobs:
  - job: initial
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - script: echo "This job will be run first."
  - job: fanout1
    pool:
      vmImage: 'ubuntu-latest'
    dependsOn: initial
    steps:
      - script: echo "This job will run after the initial job, in parallel with fanout2."
  - job: fanout2
    pool:
      vmImage: 'ubuntu-latest'
    dependsOn: initial
    steps:
      - script: echo "This job will run after the initial job, in parallel with fanout1."
  - job: fanin
    pool:
      vmImage: 'ubuntu-latest'
    dependsOn: [fanout1, fanout2]
    steps:
      - script: echo "This job will run after fanout1 and fanout2 have finished."
```

### GitHub Actions sintaxe para dependências entre trabalhos

```yaml
jobs:
  initial:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This job will be run first."
  fanout1:
    runs-on: ubuntu-latest
    needs: initial
    steps:
      - run: echo "This job will run after the initial job, in parallel with fanout2."
  fanout2:
    runs-on: ubuntu-latest
    needs: initial
    steps:
      - run: echo "This job will run after the initial job, in parallel with fanout1."
  fanin:
    runs-on: ubuntu-latest
    needs: [fanout1, fanout2]
    steps:
      - run: echo "This job will run after fanout1 and fanout2 have finished."
```

Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds).

## Migrar tarefas para ações

Azure Pipelines usa *tasks*, que são componentes de aplicativo que podem ser reutilizados em vários fluxos de trabalho.
GitHub Actions usa *ações*, que podem ser usadas para executar tarefas e personalizar seu fluxo de trabalho. Em ambos os sistemas, é possível especificar o nome da tarefa ou ação a executar, junto com quaisquer entradas necessárias como pares chave/valor.

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe do Azure Pipelines para tarefas

```yaml
jobs:
  - job: run_python
    pool:
      vmImage: 'ubuntu-latest'
    steps:
      - task: UsePythonVersion@0
        inputs:
          versionSpec: '3.7'
          architecture: 'x64'
      - script: python script.py
```

### GitHub Actions sintaxe para ações

```yaml
jobs:
  run_python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.7'
          architecture: 'x64'
      - run: python script.py
```

Você pode encontrar ações que você pode usar em [GitHub Marketplace](https://github.com/marketplace?type=actions)seu fluxo de trabalho ou pode criar suas próprias ações. Para saber mais, confira [Reutilização de automações](../../../how-tos/reuse-automations.md).
