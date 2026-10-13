---
title: Automatizando a migração com o importador de GitHub Actions
description: Use o GitHub Actions Importer para planejar e automatizar sua migração para o GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/use-github-actions-importer
captured: '2026-10-13'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Automatizando a migração com o importador de GitHub Actions

_Use o GitHub Actions Importer para planejar e automatizar sua migração para o GitHub Actions._

## Sobre o GitHub Actions Importer

Você pode usar GitHub Actions Importer para planejar e migrar automaticamente seus pipelines compatíveis com CI/CD para GitHub Actions.

O GitHub Actions Importer é distribuído como um contêiner do Docker e usa uma extensão da [CLI do GitHub](https://cli.github.com) para interagir com o contêiner.

Qualquer fluxo de trabalho convertido pelo GitHub Actions Importer deve ser inspecionado quanto à exatidão antes de ser usado como uma carga de trabalho de produção. A meta é alcançar uma taxa de conversão de 80% para cada fluxo de trabalho, no entanto, a taxa de conversão real dependerá da composição de cada pipeline individual convertido.

## Plataformas de CI com suporte

É possível usar o GitHub Actions Importer para migrar das seguintes plataformas:

* Azure DevOps
* Bamboo
* Bitbucket Pipelines
* CircleCI
* GitLab (nuvem e auto-hospedado)
* Jenkins
* Travis CI

## Pré-requisitos

O GitHub Actions Importer tem os seguintes requisitos:

* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.
  * A [CLI do GitHub](https://cli.github.com) está instalada.

!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Instalação da extensão da CLI do GitHub Actions Importer

1. Instale a extensão da CLI do GitHub Actions Importer:

            ```bash copy
   gh extension install github/gh-actions-importer
   ```

1. Verifique se a extensão foi instalada:

            ```bash
   $ gh actions-importer -h
   Options:
     -?, -h, --help  Show help and usage information

   Commands:
     update     Update to the latest version of GitHub Actions Importer.
     version    Display the version of GitHub Actions Importer.
     configure  Start an interactive prompt to configure credentials used to authenticate with your CI server(s).
     audit      Plan your CI/CD migration by analyzing your current CI/CD footprint.
     forecast   Forecast GitHub Actions usage from historical pipeline utilization.
     dry-run    Convert a pipeline to a GitHub Actions workflow and output its yaml file.
     migrate    Convert a pipeline to a GitHub Actions workflow and open a pull request with the changes.
   ```

### Atualização da CLI do GitHub Actions Importer

Execute regularmente o comando `update` para garantir que você esteja executando a versão mais recente do GitHub Actions Importer:

```bash
gh actions-importer update
```

### Autenticação na linha de comando

Você deve configurar credenciais para permitir que o GitHub Actions Importer se comunique com o GitHub e com seu servidor de CI atual. É possível configurar essas credenciais usando variáveis de ambiente ou um arquivo `.env.local`. As variáveis de ambiente podem ser configuradas em um prompt interativo executando o seguinte comando:

```bash
gh actions-importer configure
```

## Uso da CLI do GitHub Actions Importer

Use os subcomandos de `gh actions-importer` para iniciar a migração para o GitHub Actions, incluindo `audit`, `forecast`, `dry-run` e `migrate`.

### Auditoria de pipelines de CI existentes

O subcomando `audit` pode ser usado para analisar seu volume de CI/CD atual, a fim de ajudar no planejamento da migração de CI/CD. Essa análise pode ser usada no planejamento de uma linha do tempo de migração para o GitHub Actions.

Para executar uma auditoria, use o seguinte comando a fim de determinar as opções disponíveis:

```bash
$ gh actions-importer audit -h
Description:
  Plan your CI/CD migration by analyzing your current CI/CD footprint.

[...]

Commands:
  azure-devops  An audit will output a list of data used in an Azure DevOps instance.
  bamboo        An audit will output a list of data used in a Bamboo instance.
  circle-ci     An audit will output a list of data used in a CircleCI instance.
  gitlab        An audit will output a list of data used in a GitLab instance.
  jenkins       An audit will output a list of data used in a Jenkins instance.
  travis-ci     An audit will output a list of data used in a Travis CI instance.
```

### Previsão de uso

O subcomando `forecast` examina o uso histórico de pipelines para criar uma previsão de uso do GitHub Actions.

Para executar uma previsão, use o seguinte comando para determinar as opções disponíveis:

```bash
$ gh actions-importer forecast -h
Description:
  Forecasts GitHub Actions usage from historical pipeline utilization.

[...]

Commands:
  azure-devops  Forecasts GitHub Actions usage from historical Azure DevOps pipeline utilization.
  bamboo        Forecasts GitHub Actions usage from historical Bamboo pipeline utilization.
  jenkins       Forecasts GitHub Actions usage from historical Jenkins pipeline utilization.
  gitlab        Forecasts GitHub Actions usage from historical GitLab pipeline utilization.
  circle-ci     Forecasts GitHub Actions usage from historical CircleCI pipeline utilization.
  travis-ci     Forecasts GitHub Actions usage from historical Travis CI pipeline utilization.
  github        Forecasts GitHub Actions usage from historical GitHub pipeline utilization.
```

### Teste do processo de migração

O subcomando `dry-run` pode ser usado para converter um pipeline em seu equivalente do GitHub Actions e, em seguida, gravar o fluxo de trabalho no sistema de arquivos local.

Para executar uma simulação, use o seguinte comando a fim de determinar as opções disponíveis:

```bash
$ gh actions-importer dry-run -h
Description:
  Convert a pipeline to a GitHub Actions workflow and output its yaml file.

[...]

Commands:
  azure-devops  Convert an Azure DevOps pipeline to a GitHub Actions workflow and output its yaml file.
  bamboo        Convert a Bamboo pipeline to GitHub Actions workflows and output its yaml file.
  circle-ci     Convert a CircleCI pipeline to GitHub Actions workflows and output the yaml file(s).
  gitlab        Convert a GitLab pipeline to a GitHub Actions workflow and output the yaml file.
  jenkins       Convert a Jenkins job to a GitHub Actions workflow and output its yaml file.
  travis-ci     Convert a Travis CI pipeline to a GitHub Actions workflow and output its yaml file.
```

### Migrar um pipeline para o GitHub Actions

O subcomando `migrate` pode ser usado para converter um pipeline em seu GitHub Actions equivalente e, em seguida, criar uma solicitação de pull com o conteúdo.

Para executar uma migração, use o seguinte comando a fim de determinar as opções disponíveis:

```bash
$ gh actions-importer migrate -h
Description:
  Convert a pipeline to a GitHub Actions workflow and open a pull request with the changes.

[...]

Commands:
  azure-devops  Convert an Azure DevOps pipeline to a GitHub Actions workflow and open a pull request with the changes.
  bamboo        Convert a Bamboo pipeline to GitHub Actions workflows and open a pull request with the changes.
  circle-ci     Convert a CircleCI pipeline to GitHub Actions workflows and open a pull request with the changes.
  gitlab        Convert a GitLab pipeline to a GitHub Actions workflow and open a pull request with the changes.
  jenkins       Convert a Jenkins job to a GitHub Actions workflow and open a pull request with the changes.
  travis-ci     Convert a Travis CI pipeline to a GitHub Actions workflow and open a pull request with the changes.
```

## Como executar migrações de autoatendimento com IssueOps

Você pode usar GitHub Actions e GitHub Issues para executar comandos da CLI de GitHub Actions Importer. Isso permite que você migre seus fluxos de trabalho de CI/CD sem instalar software em seu computador local. Essa abordagem é especialmente útil para organizações que desejam habilitar migrações de autoatendimento para GitHub Actions. Após a configuração do IssueOps, os usuários poderão abrir um issue com o modelo relevante para migrar pipelines para GitHub Actions.

Para obter mais informações sobre como configurar migrações de autoatendimento com IssueOps, confira o repositório de modelos [`actions/importer-issue-ops`](https://github.com/actions/importer-issue-ops).

## Uso do repositório de laboratórios do GitHub Actions Importer

O repositório de laboratórios do GitHub Actions Importer contém roteiros de aprendizagem específicos da plataforma que ensinam como usar o GitHub Actions Importer e abordar migrações para GitHub Actions. Você pode usar esse repositório para saber como usar GitHub Actions Importer para planejar, prever e automatizar sua migração para GitHub Actions.

Para saber mais, consulte o [repositório de labs GitHub Actions Importer](https://github.com/actions/importer-labs/tree/main#readme).

## Aviso legal

Partes foram adaptadas do https://github.com/github/gh-actions-importer/ de acordo com a licença MIT:

```text
MIT License

Copyright (c) 2022 GitHub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
