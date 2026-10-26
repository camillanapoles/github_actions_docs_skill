---
title: Migrando do Jenkins para o GitHub Actions
description: GitHub Actions e Jenkins compartilham várias semelhanças, o que torna a migração para GitHub Actions relativamente simples.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-jenkins
captured: '2026-10-26'
section: Tutorials / Migrate to github actions / Manual migrations
---

# Migrando do Jenkins para o GitHub Actions

_GitHub Actions e Jenkins compartilham várias semelhanças, o que torna a migração para GitHub Actions relativamente simples._

## Introdução

O Jenkins e GitHub Actions ambos permitem criar fluxos de trabalho que criam, testam, publicam, liberam e implantam código automaticamente. Jenkins e GitHub Actions compartilham algumas semelhanças na configuração do fluxo de trabalho:

* O Jenkins cria fluxos de trabalho usando *Pipelines Declarativos*, que são semelhantes aos GitHub Actions arquivos de fluxo de trabalho.
* O Jenkins usa *estágios* para executar uma coleção de etapas, enquanto GitHub Actions usa trabalhos para agrupar uma ou mais etapas ou comandos individuais.
* Jenkins e GitHub Actions oferecem suporte a compilações baseadas em contêineres. Para saber mais, confira [Criando uma ação de contêiner do Docker](../../use-containerized-services/create-a-docker-container-action.md).
* É possível reutilizar e compartilhar novamente etapas ou tarefas com a comunidade.

Para saber mais, confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md).

## Principais diferenças

* O Jenkins tem dois tipos de sintaxe para a criação de pipelines: Declarative Pipeline e Scripted Pipeline.
  GitHub Actions usa YAML para criar fluxos de trabalho e arquivos de configuração. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md).
* As implementações do Jenkins são tipicamente auto-hospedadas, com usuários mantendo os servidores em seus próprios centros de dados.
  GitHub Actions oferece uma abordagem de nuvem híbrida hospedando seus próprios corredores que você pode usar para executar trabalhos, ao mesmo tempo em que dá suporte a corredores auto-hospedados. Para saber mais, confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md).

## Comparar recursos

### Distribuir suas criações

O Jenkins permite que se envie criações para um único agente de criação, ou você pode distribuí-las entre vários agentes. Você também pode classificar esses agentes de acordo com vários atributos, como, por exemplo, tipos de sistema operacional.

Da mesma forma, GitHub Actions pode enviar trabalhos para executores hospedados no GitHub ou auto-hospedados, e pode usar rótulos para classificar os executores de acordo com vários atributos. Para saber mais, confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md#runners) e [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md).

### Usar seções para organizar pipelines

O Jenkins divide seus Declarative Pipelines em múltiplas seções. Da mesma forma, GitHub Actions organiza seus fluxos de trabalho em seções separadas. A tabela a seguir compara as seções do Jenkins com o GitHub Actions fluxo de trabalho.

| Diretivas do Jenkins | GitHub Actions |
| --- | --- |
| [`agent`](https://jenkins.io/doc/book/pipeline/syntax/#agent) | [`jobs.<job_id>.runs-on`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on) <br> [`jobs.<job_id>.container`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontainer) |
| [`post`](https://jenkins.io/doc/book/pipeline/syntax/#post) | Nenhum |
| [`stages`](https://jenkins.io/doc/book/pipeline/syntax/#stages) | [`jobs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobs) |
| [`steps`](https://jenkins.io/doc/book/pipeline/syntax/#steps) | [`jobs.<job_id>.steps`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps) |

## Uso de diretivas

O Jenkins usa diretivas para gerenciar os *Pipelines Declarativos*. Essas diretivas definem as características do seu fluxo de trabalho e como ele será executado. A tabela a seguir demonstra como essas diretivas correspondem a conceitos em GitHub Actions.

| Diretivas do Jenkins | GitHub Actions |
| --- | --- |
| [`environment`](https://jenkins.io/doc/book/pipeline/syntax/#environment) | [`jobs.<job_id>.env`](../../../reference/workflows-and-actions/workflow-syntax.md#env) <br> [`jobs.<job_id>.steps[*].env`](/pt/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsenv) |
| [`options`](https://jenkins.io/doc/book/pipeline/syntax/#options) | [`jobs.<job_id>.strategy`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategy) <br> [`jobs.<job_id>.strategy.fail-fast`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategyfail-fast) <br> [`jobs.<job_id>.timeout-minutes`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idtimeout-minutes) |
| [`parameters`](https://jenkins.io/doc/book/pipeline/syntax/#options) | [`inputs`](../../../reference/workflows-and-actions/metadata-syntax.md#inputs) <br> [`outputs`](../../../reference/workflows-and-actions/metadata-syntax.md#outputs-for-docker-container-and-javascript-actions) |
| [`triggers`](https://jenkins.io/doc/book/pipeline/syntax/#triggers) | [`on`](../../../reference/workflows-and-actions/workflow-syntax.md#on) <br> [`on.<event_name>.types`](../../../reference/workflows-and-actions/workflow-syntax.md#onevent_nametypes) <br> [`on.<push>.<branches\|tags>`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushbranchestagsbranches-ignoretags-ignore) <br> [`on.<pull_request>.<branches>`](../../../reference/workflows-and-actions/workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore) <br> [`on.<push\|pull_request>.paths`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore) |
| [`triggers { upstreamprojects() }`](https://jenkins.io/doc/book/pipeline/syntax/#triggers) | [`jobs.<job_id>.needs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds) |
| [Sintaxe cron do Jenkins](https://jenkins.io/doc/book/pipeline/syntax/#cron-syntax) | [`on.schedule`](../../../reference/workflows-and-actions/workflow-syntax.md#onschedule) |
| [`stage`](https://jenkins.io/doc/book/pipeline/syntax/#stage) | [`jobs.<job_id>`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_id) <br> [`jobs.<job_id>.name`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idname) |
| [`tools`](https://jenkins.io/doc/book/pipeline/syntax/#tools) |  |
| [Especificações para GitHubrunners hospedados](../../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images) |  |
| [`input`](https://jenkins.io/doc/book/pipeline/syntax/#input) | [`inputs`](../../../reference/workflows-and-actions/metadata-syntax.md#inputs) |
| [`when`](https://jenkins.io/doc/book/pipeline/syntax/#when) | [`jobs.<job_id>.if`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif) |

## Usar estágios sequenciais

### Processamento paralelo do trabalho

Jenkins pode executar o `stages` e `steps` em paralelo.
GitHub Actions executa trabalhos em paralelo e também pode executar etapas simultaneamente em um trabalho usando a sintaxe de nível de etapa. Para obter mais informações, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsbackground).

| Jenkins em paralelo | GitHub Actions |
| --- | --- |
| [`parallel`](https://jenkins.io/doc/book/pipeline/syntax/#parallel) | [`jobs.<job_id>.strategy.max-parallel`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymax-parallel) |

### Matriz

Tanto GitHub Actions quanto Jenkins permitem que você use uma matriz para definir várias combinações do sistema.

| Jenkins | GitHub Actions |
| --- | --- |
| [`axis`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-axes) | [`strategy/matrix`](../../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md#about-matrix-strategies) <br> [`context`](../../../reference/workflows-and-actions/contexts.md) |
| [`stages`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-stages) | [`steps-context`](../../../reference/workflows-and-actions/contexts.md#steps-context) |
| [`excludes`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-stages) | Nenhum |

### Usar passos para executar tarefas

O Jenkins agrupa as `steps` em `stages`. Cada uma dessas etapas pode ser um script, função ou comando, entre outros. Da mesma forma, GitHub Actions usa `jobs` para executar grupos específicos de `steps`.

| Jenkins | GitHub Actions |
| --- | --- |
| [`steps`](https://jenkins.io/doc/book/pipeline/syntax/#steps) | [`jobs.<job_id>.steps`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps) |

## Exemplos de tarefas comuns

### Como agendar um pipeline para ser executado com o `cron`

#### Pipeline do Jenkins com `cron`

```yaml
pipeline {
  agent any
  triggers {
    cron('H/15 * * * 1-5')
  }
}
```

#### GitHub Actions fluxo de trabalho com `cron`

```yaml
on:
  schedule:
    - cron: '*/15 * * * 1-5'
```

Para obter mais informações sobre eventos `schedule` e a sintaxe cron aceita, consulte [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).

### Configurar variáveis de ambiente em um pipeline

#### Pipeline do Jenkins com uma variável de ambiente

```yaml
pipeline {
  agent any
  environment {
    MAVEN_PATH = '/usr/local/maven'
  }
}
```

#### GitHub Actions fluxo de trabalho com uma variável de ambiente

```yaml
jobs:
  maven-build:
    env:
      MAVEN_PATH: '/usr/local/maven'
```

### Criar projetos projetos de upstream

#### Pipeline do Jenkins baseado em um projeto upstream

```yaml
pipeline {
  triggers {
    upstream(
      upstreamProjects: 'job1,job2',
      threshold: hudson.model.Result.SUCCESS
    )
  }
}
```

#### GitHub Actions fluxo de trabalho criado a partir de um projeto de origem

```yaml
jobs:
  job1:
  job2:
    needs: job1
  job3:
    needs: [job1, job2]
```

### Criar com vários sistemas operacionais

#### Pipeline do Jenkins baseado em vários sistemas operacionais

```yaml
pipeline {
  agent none
  stages {
    stage('Run Tests') {
      matrix {
        axes {
          axis {
            name: 'PLATFORM'
            values: 'macos', 'linux'
          }
        }
        agent { label "${PLATFORM}" }
        stages {
          stage('test') {
            tools { nodejs "node-20" }
            steps {
              dir("scripts/myapp") {
                sh(script: "npm install -g bats")
                sh(script: "bats tests")
              }
            }
          }
        }
      }
    }
  }
}
```

#### GitHub Actions fluxo de trabalho criado com vários sistemas operacionais

```yaml
name: demo-workflow
on:
  push:
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [macos-latest, ubuntu-latest]
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: 20
      - run: npm install -g bats
      - run: bats tests
        working-directory: ./scripts/myapp
```
