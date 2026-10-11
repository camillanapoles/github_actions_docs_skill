---
title: Migrating from Jenkins to GitHub Actions
description: GitHub Actions and Jenkins share multiple similarities, which makes migration to GitHub Actions relatively straightforward.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-jenkins.md
captured: '2026-10-11'
section: Tutorials / Migrate to github actions / Manual migrations
---

# Migrating from Jenkins to GitHub Actions

_GitHub Actions and Jenkins share multiple similarities, which makes migration to GitHub Actions relatively straightforward._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Introduction

Jenkins and GitHub Actions both allow you to create workflows that automatically build, test, publish, release, and deploy code. Jenkins and GitHub Actions share some similarities in workflow configuration:

* Jenkins creates workflows using _Declarative Pipelines_, which are similar to GitHub Actions workflow files.
* Jenkins uses _stages_ to run a collection of steps, while GitHub Actions uses jobs to group one or more steps or individual commands.
* Jenkins and GitHub Actions support container-based builds. For more information, see [Creating a Docker container action](../../use-containerized-services/create-a-docker-container-action.md).
* Steps or tasks can be reused and shared with the community.

For more information, see [Understanding GitHub Actions](../../../get-started/understand-github-actions.md).

## Key differences

* Jenkins has two types of syntax for creating pipelines: Declarative Pipeline and Scripted Pipeline. GitHub Actions uses YAML to create workflows and configuration files. For more information, see [Workflow syntax for GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md).
* Jenkins deployments are typically self-hosted, with users maintaining the servers in their own data centers. GitHub Actions offers a hybrid cloud approach by hosting its own runners that you can use to run jobs, while also supporting self-hosted runners. For more information, see [Self-hosted runners](../../../concepts/runners/self-hosted-runners.md).

## Comparing capabilities

### Distributing your builds

Jenkins lets you send builds to a single build agent, or you can distribute them across multiple agents. You can also classify these agents according to various attributes, such as operating system types.

Similarly, GitHub Actions can send jobs to GitHub-hosted or self-hosted runners, and you can use labels to classify runners according to various attributes. For more information, see [Understanding GitHub Actions](../../../get-started/understand-github-actions.md#runners#runners) and [Self-hosted runners](../../../concepts/runners/self-hosted-runners.md).

### Using sections to organize pipelines

Jenkins splits its Declarative Pipelines into multiple sections. Similarly, GitHub Actions organizes its workflows into separate sections. The table below compares Jenkins sections with the GitHub Actions workflow.

| Jenkins Directives | GitHub Actions |
| --- | --- |
| [`agent`](https://jenkins.io/doc/book/pipeline/syntax/#agent) | [`jobs.<job_id>.runs-on`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on)   [`jobs.<job_id>.container`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontainer) |
| [`post`](https://jenkins.io/doc/book/pipeline/syntax/#post) | None |
| [`stages`](https://jenkins.io/doc/book/pipeline/syntax/#stages) | [`jobs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobs) |
| [`steps`](https://jenkins.io/doc/book/pipeline/syntax/#steps) | [`jobs.<job_id>.steps`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps) |

## Using directives

Jenkins uses directives to manage _Declarative Pipelines_. These directives define the characteristics of your workflow and how it will execute. The table below demonstrates how these directives map to concepts within GitHub Actions.

| Jenkins Directives | GitHub Actions |
| --- | --- |
| [`environment`](https://jenkins.io/doc/book/pipeline/syntax/#environment) | [`jobs.<job_id>.env`](../../../reference/workflows-and-actions/workflow-syntax.md#env)   [`jobs.<job_id>.steps[*].env`](/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsenv) |
| [`options`](https://jenkins.io/doc/book/pipeline/syntax/#options) | [`jobs.<job_id>.strategy`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategy)   [`jobs.<job_id>.strategy.fail-fast`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategyfail-fast)   [`jobs.<job_id>.timeout-minutes`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idtimeout-minutes) |
| [`parameters`](https://jenkins.io/doc/book/pipeline/syntax/#options) | [`inputs`](../../../reference/workflows-and-actions/metadata-syntax.md#inputs)   [`outputs`](../../../reference/workflows-and-actions/metadata-syntax.md#outputs-for-docker-container-and-javascript-actions) |
| [`triggers`](https://jenkins.io/doc/book/pipeline/syntax/#triggers) | [`on`](../../../reference/workflows-and-actions/workflow-syntax.md#on)   [`on.<event_name>.types`](../../../reference/workflows-and-actions/workflow-syntax.md#onevent_nametypes)   [`on.<push\>.<branches\|tags>`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushbranchestagsbranches-ignoretags-ignore)   [`on.<pull_request\>.<branches\>`](../../../reference/workflows-and-actions/workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore)   [`on.<push\|pull_request>.paths`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore) |
| [`triggers { upstreamprojects() }`](https://jenkins.io/doc/book/pipeline/syntax/#triggers) | [`jobs.<job_id>.needs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds) |
| [Jenkins cron syntax](https://jenkins.io/doc/book/pipeline/syntax/#cron-syntax) | [`on.schedule`](../../../reference/workflows-and-actions/workflow-syntax.md#onschedule) |
| [`stage`](https://jenkins.io/doc/book/pipeline/syntax/#stage) | [`jobs.<job_id>`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_id)   [`jobs.<job_id>.name`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idname) |
| [`tools`](https://jenkins.io/doc/book/pipeline/syntax/#tools) | [Specifications for GitHub-hosted runners](../../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images) |
| [`input`](https://jenkins.io/doc/book/pipeline/syntax/#input) | [`inputs`](../../../reference/workflows-and-actions/metadata-syntax.md#inputs) |
| [`when`](https://jenkins.io/doc/book/pipeline/syntax/#when) | [`jobs.<job_id>.if`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif) |

## Using sequential stages

### Parallel job processing

Jenkins can run the `stages` and `steps` in parallel, while GitHub Actions currently only runs jobs in parallel.

| Jenkins Parallel | GitHub Actions |
| --- | --- |
| [`parallel`](https://jenkins.io/doc/book/pipeline/syntax/#parallel) | [`jobs.<job_id>.strategy.max-parallel`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymax-parallel) |

### Matrix

Both GitHub Actions and Jenkins let you use a matrix to define various system combinations.

| Jenkins | GitHub Actions |
| --- | --- |
| [`axis`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-axes) | [`strategy/matrix`](../../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md#about-matrix-strategies)   [`context`](../../../reference/workflows-and-actions/contexts.md) |
| [`stages`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-stages) | [`steps-context`](../../../reference/workflows-and-actions/contexts.md#steps-context) |
| [`excludes`](https://jenkins.io/doc/book/pipeline/syntax/#matrix-stages) | None |

### Using steps to execute tasks

Jenkins groups `steps` together in `stages`. Each of these steps can be a script, function, or command, among others. Similarly, GitHub Actions uses `jobs` to execute specific groups of `steps`.

| Jenkins | GitHub Actions |
| --- | --- |
| [`steps`](https://jenkins.io/doc/book/pipeline/syntax/#steps) | [`jobs.<job_id>.steps`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps) |

## Examples of common tasks

### Scheduling a pipeline to run with `cron`

#### Jenkins pipeline with `cron`

```yaml
pipeline {
  agent any
  triggers {
    cron('H/15 * * * 1-5')
  }
}
```

#### GitHub Actions workflow with `cron`

```yaml
on:
  schedule:
    - cron: '*/15 * * * 1-5'
```

For more information about `schedule` events and accepted cron syntax, see [Events that trigger workflows](../../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule#schedule).

### Configuring environment variables in a pipeline

#### Jenkins pipeline with an environment variable

```yaml
pipeline {
  agent any
  environment {
    MAVEN_PATH = '/usr/local/maven'
  }
}
```

#### GitHub Actions workflow with an environment variable

```yaml
jobs:
  maven-build:
    env:
      MAVEN_PATH: '/usr/local/maven'
```

### Building from upstream projects

#### Jenkins pipeline that builds from an upstream project

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

#### GitHub Actions workflow that builds from an upstream project

```yaml
jobs:
  job1:
  job2:
    needs: job1
  job3:
    needs: [job1, job2]
```

### Building with multiple operating systems

#### Jenkins pipeline that builds with multiple operating systems

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

#### GitHub Actions workflow that builds with multiple operating systems

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
