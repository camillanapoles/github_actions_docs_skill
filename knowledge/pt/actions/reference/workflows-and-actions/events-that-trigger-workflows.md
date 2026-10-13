---
title: Eventos que disparam fluxos de trabalho
description: Você pode configurar seus fluxos de trabalho para serem executados quando uma atividade GitHub específica ocorrer, em um horário agendado ou quando ocorrer um evento fora dele GitHub .
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/events-that-trigger-workflows
captured: '2026-10-13'
section: Reference / Workflows and actions
---

# Eventos que disparam fluxos de trabalho { #events-that-trigger-workflows }

_Você pode configurar seus fluxos de trabalho para serem executados quando uma atividade GitHub específica ocorrer, em um horário agendado ou quando ocorrer um evento fora dele GitHub ._

## Sobre eventos que acionam fluxos de trabalho { #about-events-that-trigger-workflows }

Os acionadores de fluxo de trabalho são eventos que fazem com que um fluxo de trabalho seja executado. Para obter mais informações sobre como usar gatilhos de fluxo de trabalho, confira [Acionando um fluxo de trabalho](../../how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow.md).

Alguns eventos têm vários tipos de atividades. Para esses eventos, você pode especificar quais tipos de atividade ativarão a execução de um fluxo de trabalho. Para obter mais informações sobre o que significa cada tipo de atividade, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads).

!!! note
    Nem todos os eventos de webhook disparam fluxos de trabalho.

Assim como os fluxos de trabalho GitHub Actions, agentic workflows podem ser disparados por eventos do repositório e agendamentos. Para ver um exemplo, confira [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

## `branch_protection_rule`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`branch_protection_rule`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#branch_protection_rule) | - `created`<br>- `edited`<br>- `deleted` | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#branch_protection_rule). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando as regras de proteção de branch no repositório do fluxo de trabalho são alteradas. Para obter mais informações sobre as regras de proteção do branch, confira [Sobre branches protegidos](https://docs.github.com/pt/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches). Para obter informações sobre as APIs da regra de proteção de ramificação, confira [Branches](https://docs.github.com/pt/graphql/reference/branches#object-branchprotectionrule)" na documentação da API do GraphQL ou [Pontos de extremidade da API REST para ramificações e suas configurações](https://docs.github.com/pt/rest/branches).

Por exemplo, você poderá executar um fluxo de trabalho quando uma regra de proteção de branch for `created` ou `deleted`:

```yaml
on:
  branch_protection_rule:
    types: [created, deleted]
```

## `check_run`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`check_run`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#check_run) | - `created`<br>- `rerequested`<br>- `completed`<br>- `requested_action` | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#check_run). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Para evitar fluxos de trabalho recursivos, esse evento não dispara fluxos de trabalho se o conjunto de verificações da verificação foi criado por GitHub Actions ou se o SHA principal do conjunto de verificações está associado com GitHub Actions.

Executa o fluxo de trabalho quando ocorre a atividade relacionada a uma execução de verificação. Uma execução de verificação é um teste individual que faz parte de um conjunto de verificações. Para obter mais informações, confira [Como usar a API REST para interagir com verificações](https://docs.github.com/pt/rest/guides/using-the-rest-api-to-interact-with-checks). Para obter informações sobre as APIs de execução de verificação, confira [Verificações](https://docs.github.com/pt/graphql/reference/checks#object-checkrun) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para execuções de verificação](https://docs.github.com/pt/rest/checks/runs)."

Por exemplo, você poderá executar um fluxo de trabalho quando uma execução de verificação for `rerequested` ou `completed`.

```yaml
on:
  check_run:
    types: [rerequested, completed]
```

## `check_suite`

| Carga de evento webhook                                               | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|---------------------------------------------------------------------|------------------|------------------------------|-------------|
| [`check_suite`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#check_suite) | - `completed`      | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#check_suite). Embora apenas o tipo de atividade `completed` seja compatível, a especificação do tipo de atividade manterá o fluxo de trabalho específico se mais tipos de atividade forem adicionados no futuro. Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Para evitar fluxos de trabalho recursivos, esse evento não dispara fluxos de trabalho se o conjunto de verificações foi criado por GitHub Actions ou se o SHA de cabeça do conjunto de verificações está associado a GitHub Actions.

Executa o fluxo de trabalho quando ocorre a atividade do conjunto de verificações. Um conjunto de verificações é uma coleção das execuções de verificação criadas para um commit específico. O conjunto de verificações resumem o status e a conclusão das execuções de verificação que estão no conjunto. Para obter mais informações, confira [Como usar a API REST para interagir com verificações](https://docs.github.com/pt/rest/guides/using-the-rest-api-to-interact-with-checks). Para obter informações sobre as APIs do conjunto de verificação, confira [Verificações](https://docs.github.com/pt/graphql/reference/checks#object-checksuite) na documentação da API do GraphQL ou [Endpoints da API REST para conjuntos de verificações](https://docs.github.com/pt/rest/checks/suites).

Por exemplo, você poderá executar um fluxo de trabalho quando um conjunto de verificações for `completed`.

```yaml
on:
  check_suite:
    types: [completed]
```

## `create`

| Carga de evento webhook                                     | Tipos de Atividade | `GITHUB_SHA`                          | `GITHUB_REF`         |
|-----------------------------------------------------------|------------------|-------------------------------------|--------------------|
| [`create`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#create) | Não aplicável      | Último commit no branch ou tag criado | Branch ou tag criado |

!!! note
    Um evento não será criado quando você criar mais de três marcas de uma só vez.

Executa o fluxo de trabalho quando alguém cria uma referência Git (branch ou tag) no repositório do fluxo de trabalho. Para obter informações sobre as APIs usadas para criar uma referência Git, confira [Git](https://docs.github.com/pt/graphql/reference/git#mutation-createref) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para referências Git](https://docs.github.com/pt/rest/git/refs#create-a-reference).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `create` ocorrer.

```yaml
on:
  create
```

## `delete`

| Carga de evento webhook                                     | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------------------------------------------|------------------|------------------------------|-------------|
| [`delete`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#delete) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Um evento não será criado quando você excluir mais de três marcas de uma só vez.

Executa o fluxo de trabalho quando alguém exclui uma referência Git (branch ou tag) no repositório do fluxo de trabalho. Para obter informações sobre as APIs usadas para excluir uma referência do Git, confira [Git](https://docs.github.com/pt/graphql/reference/git#mutation-deleteref) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para referências Git](https://docs.github.com/pt/rest/git/refs#delete-a-reference).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `delete` ocorrer.

```yaml
on:
  delete
```

## `deployment`

| Carga de evento webhook                                             | Tipos de Atividade | `GITHUB_SHA`            | `GITHUB_REF`                                                             |
|-------------------------------------------------------------------|------------------|-----------------------|------------------------------------------------------------------------|
| [`deployment`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment) | Não aplicável      | Commit a ser implantado | Branch ou tag a ser implantado (vazio, se criado com o SHA de um commit) |

Executa o fluxo de trabalho quando alguém cria uma implantação no repositório do fluxo de trabalho. As implantações criadas com um SHA de commit podem não ter uma referência do Git. Para obter informações sobre as APIs usadas para criar uma implantação, confira [Deployments](https://docs.github.com/pt/graphql/reference/deployments#mutation-createdeployment) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#deployments).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `deployment` ocorrer.

```yaml
on:
  deployment
```

## `deployment_status`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`deployment_status`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment_status) | Não aplicável | Commit a ser implantado | Branch ou tag a ser implantado (vazio se commit) |

!!! note
    Quando o estado de um status de implantação for definido como `inactive`, um fluxo de trabalho não será disparado.

Executa o fluxo de trabalho quando uma terceira parte fornece um status de implantação. As implantações criadas com um SHA de commit podem não ter uma referência do Git. Para obter informações sobre as APIs usadas para criar um status de implantação, confira [Deployments](https://docs.github.com/pt/graphql/reference/deployments#mutation-createdeploymentstatus) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para implantações](https://docs.github.com/pt/rest/deployments#create-a-deployment-status).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `deployment_status` ocorrer.

```yaml
on:
  deployment_status
```

## `discussion`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`discussion`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#discussion) | - `created`<br>- `edited`<br>- `deleted`<br>- `transferred`<br>- `pinned`<br>- `unpinned`<br>- `labeled`<br>- `unlabeled`<br>- `locked`<br>- `unlocked`<br>- `category_changed`<br> - `answered`<br> - `unanswered` | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#discussion). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Atualmente, os eventos de webhook do GitHub Discussions estão em prévia pública e estão sujeitos a alterações.

Executa o fluxo de trabalho quando uma discussão no repositório do fluxo de trabalho é criada ou modificada. Para as atividades relacionadas a comentários sobre uma discussão, use o evento [`discussion_comment`](#discussion_comment). Para obter mais informações sobre discussões, confira [Sobre discussões](https://docs.github.com/pt/discussions/collaborating-with-your-community-using-discussions/about-discussions). Para obter informações sobre a API do GraphQL, confira [Discussões](https://docs.github.com/pt/graphql/reference/discussions#object-discussion).

Por exemplo, você poderá executar um fluxo de trabalho quando uma discussão for `created`, `edited` ou `answered`.

```yaml
on:
  discussion:
    types: [created, edited, answered]
```

## `discussion_comment`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`discussion_comment`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#discussion_comment) | - `created`<br>- `edited`<br>- `deleted`<br> | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#discussion_comment). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Atualmente, os eventos de webhook do GitHub Discussions estão em prévia pública e estão sujeitos a alterações.

Executa o fluxo de trabalho quando um comentário em uma discussão no repositório do fluxo de trabalho é criado ou modificado. Para as atividades relacionadas a uma discussão em vez de comentários sobre uma discussão, use o evento [`discussion`](#discussion). Para obter mais informações sobre discussões, confira [Sobre discussões](https://docs.github.com/pt/discussions/collaborating-with-your-community-using-discussions/about-discussions). Para obter informações sobre a API do GraphQL, confira [Discussões](https://docs.github.com/pt/graphql/reference/discussions#object-discussion).

Por exemplo, você poderá executar um fluxo de trabalho quando um comentário de discussão for `created` ou `deleted`.

```yaml
on:
  discussion_comment:
    types: [created, deleted]
```

## `fork`

| Carga de evento webhook                                 | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-------------------------------------------------------|------------------|------------------------------|-------------|
| [`fork`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#fork) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando alguém bifurca um repositório. Para obter informações sobre a API REST, confira [Pontos de extremidade de API REST para forks](https://docs.github.com/pt/rest/repos/forks#create-a-fork).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `fork` ocorrer.

```yaml
on:
  fork
```

## `gollum`

| Carga de evento webhook                                     | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------------------------------------------|------------------|------------------------------|-------------|
| [`gollum`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#gollum) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando alguém cria ou atualiza uma página wiki. Para obter mais informações, confira [Sobre wikis](https://docs.github.com/pt/communities/documenting-your-project-with-wikis/about-wikis).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `gollum` ocorrer.

```yaml
on:
  gollum
```

## `image_version`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------|------------------|------------------------------|-------------|
| Não aplicável           | Não aplicável      | Último commit no branch padrão | Branch padrão |

Executa o fluxo de trabalho quando uma nova versão de uma imagem especificada fica disponível para uso. Esse evento normalmente é disparado após uma criação bem-sucedida da versão da imagem, permitindo que você automatize ações como implantação ou notificações em resposta a novas versões de imagem.

Este evento oferece suporte a padrões globais para nomes e versões de imagem. O exemplo a seguir dispara quando uma nova versão de imagem corresponde a qualquer uma das combinações de nome e versão especificadas. Por exemplo, `["MyNewImage", 1.0.0]`, `["MyNewImage", 2.53.0]`, `["MyOtherImage", 1.0.0]`e `["MyOtherImage", 2.0.0]`.

```yaml
on:
  image_version:
    names:
    - "MyNewImage"
    - "MyOtherImage"
    versions:
    - 1.*
    - 2.*
```

## `issue_comment`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`issue_comment`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#issue_comment) | - `created`<br>- `edited`<br>- `deleted`<br> | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#issue_comment). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando um problema ou comentário de pull request é criado, editado ou excluído. Para obter informações sobre as APIs de comentários de problemas, confira [Problemas](https://docs.github.com/pt/graphql/reference/issues#object-issuecomment) na documentação da API do GraphQL ou [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#issue_comment) na documentação da API REST.

Por exemplo, você poderá executar um fluxo de trabalho quando um comentário ou um problema de uma solicitação de pull for `created` ou `deleted`.

```yaml
on:
  issue_comment:
    types: [created, deleted]
```

### `issue_comment` apenas em problemas ou em solicitações de pull { #issuecomment-on-issues-only-or-pull-requests-only }

O evento `issue_comment` ocorre em comentários sobre problemas e solicitações de pull. Você pode usar a propriedade `github.event.issue.pull_request` em um condicional para realizar uma ação diferente, dependendo se o objeto de gatilho foi um problema ou uma solicitação de pull.

Por exemplo, esse fluxo de trabalho executará o trabalho `pr_commented` somente se o evento `issue_comment` for originado de uma solicitação de pull. Ele executará o trabalho `issue_commented` somente se o evento `issue_comment` tiver se originado de um problema.

```yaml
on: issue_comment

jobs:
  pr_commented:
    # This job only runs for pull request comments
    name: PR comment
    if: ${{ github.event.issue.pull_request }}
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo A comment on PR $NUMBER
        env:
          NUMBER: ${{ github.event.issue.number }}

  issue_commented:
    # This job only runs for issue comments
    name: Issue comment
    if: ${{ !github.event.issue.pull_request }}
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo A comment on issue $NUMBER
        env:
          NUMBER: ${{ github.event.issue.number }}
```

## `issues`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`issues`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#issues) | - `opened`<br>- `edited`<br>- `deleted`<br>- `transferred`<br>- `pinned`<br>- `unpinned`<br>- `closed`<br>- `reopened`<br>- `assigned`<br>- `unassigned`<br>- `labeled`<br>- `unlabeled`<br>- `locked`<br>- `unlocked`<br>- `milestoned`<br> - `demilestoned`<br> - `typed`<br> - `untyped`<br> - `field_added`<br> - `field_removed` | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#issues). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando um problema no repositório do fluxo de trabalho é criado ou modificado. Para as atividades relacionadas a comentários em um problema, use o evento [`issue_comment`](#issue_comment). Para obter mais informações sobre problemas, confira [Sobre problemas](https://docs.github.com/pt/issues/tracking-your-work-with-issues/learning-about-issues/about-issues). Para obter informações sobre as APIs de problemas, confira [Problemas](https://docs.github.com/pt/graphql/reference/issues#object-issue) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para issues](https://docs.github.com/pt/rest/issues).

Por exemplo, você poderá executar um fluxo de trabalho quando um problema for `opened`, `edited` ou `milestoned`.

```yaml
on:
  issues:
    types: [opened, edited, milestoned]
```

Você também pode executar um fluxo de trabalho quando um valor de campo de problema é definido, alterado ou desmarcado. O `field_added` tipo de atividade é acionado quando um valor de campo é inicialmente definido e quando um valor existente é atualizado. O tipo de atividade `field_removed` é disparado quando um valor de campo é apagado.

```yaml
on:
  issues:
    types: [field_added, field_removed]
```

## `label`

| Carga de evento webhook                                   | Tipos de Atividade                              | `GITHUB_SHA`                   | `GITHUB_REF`  |
|---------------------------------------------------------|-----------------------------------------------|------------------------------|-------------|
| [`label`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#label) | - `created`<br>- `edited`<br>- `deleted`<br>    | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#label). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando uma etiqueta no repositório do fluxo de trabalho é criada ou modificada. Para obter mais informações sobre rótulos, confira [Gerenciar etiquetas](https://docs.github.com/pt/issues/using-labels-and-milestones-to-track-work/managing-labels). Para obter informações sobre as APIs de rótulo, confira "[Problemas](https://docs.github.com/pt/graphql/reference/issues#object-label) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para rótulos](https://docs.github.com/pt/rest/issues/labels).

Caso deseje executar seu fluxo de trabalho quando um rótulo for adicionado ou removido de um problema, solicitação de pull ou discussão, use os tipos de atividade `labeled` ou `unlabeled` para os eventos [`issues`](#issues), [`pull_request`](#pull_request), [`pull_request_target`](#pull_request_target), ou [`discussion`](#discussion), no lugar.

Por exemplo, você poderá executar um fluxo de trabalho quando um rótulo for `created` ou `deleted`.

```yaml
on:
  label:
    types: [created, deleted]
```

## `merge_group`

| Carga de evento webhook                                               | Tipos de Atividade | `GITHUB_SHA`              | `GITHUB_REF`                     |
|---------------------------------------------------------------------|------------------|-------------------------|--------------------------------|
| [`merge_group`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#merge_group) | `checks_requested` | SHA do grupo de mesclagem | Referência do grupo de mesclagem |

!!! note
    *

Mais de um tipo de atividade aciona este evento. Embora haja suporte apenas para o `checks_requested` tipo de atividade, especificar o tipo de atividade manterá seu fluxo de trabalho específico se mais tipos de atividade forem adicionados no futuro. Para obter informações sobre cada tipo de atividade, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#merge_group). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

> * Se o seu repositório usa o GitHub Actions para realizar verificações necessárias  em solicitações pull em seu repositório, é necessário atualizar os fluxos de trabalho para incluir o evento `merge_group` como um gatilho adicional. Caso contrário, as verificações de status não serão disparadas quando você adicionar uma solicitação de pull a uma fila de mesclagem. A mesclagem falhará, pois o verificação de status obrigatória não será relatada. O evento `merge_group` é separado dos eventos `pull_request` e `push`.

Executa o fluxo de trabalho quando uma solicitação de pull é adicionada a uma fila de mesclagem, o que adiciona a solicitação de pull a um grupo de mesclagem. Para obter mais informações, confira [Como mesclar uma pull request com uma fila de mesclagem](https://docs.github.com/pt/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request-with-a-merge-queue).

Você pode usar o filtro `branches` ou `branches-ignore` para configurar seu fluxo de trabalho para que seja executado somente para grupos de mesclagem que têm como destino ramificações específicas. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](https://docs.github.com/pt/actions/using-workflows/workflow-syntax-for-github-actions#onmerge_groupbranchesbranches-ignore).

Por exemplo, o fluxo de trabalho a seguir é executado quando ocorre a atividade `checks_requested` para um grupo de mesclagem direcionado para `main`.

```yaml
on:
  pull_request:
    branches: [main]
  merge_group:
    types: [checks_requested]
    branches: [main]
```

## `milestone`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`milestone`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#milestone) | - `created`<br>- `closed`<br>- `opened`<br>- `edited`<br>- `deleted`<br> | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#milestone). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando um marco no repositório do fluxo de trabalho é criado ou modificado. Para obter mais informações sobre marcos, confira [Sobre marcos](https://docs.github.com/pt/issues/using-labels-and-milestones-to-track-work/about-milestones). Para obter informações sobre as APIs de marcos, confira [Problemas](https://docs.github.com/pt/graphql/reference/issues#object-milestone) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para marcos](https://docs.github.com/pt/rest/issues/milestones).

Caso deseje executar seu fluxo de trabalho quando um problema for adicionado ou removido de um marco, use os tipos de atividade `milestoned` ou `demilestoned` para o evento [`issues`](#issues) no lugar.

Por exemplo, você poderá executar um fluxo de trabalho quando um marco for `opened` ou `deleted`.

```yaml
on:
  milestone:
    types: [opened, deleted]
```

## `page_build`

| Carga de evento webhook                                             | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-------------------------------------------------------------------|------------------|------------------------------|-------------|
| [`page_build`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#page_build) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa seu fluxo de trabalho quando alguém faz um push em um branch que é a origem da publicação para o GitHub Pages, se o GitHub Pages estiver habilitado para o repositório. Para obter mais informações sobre GitHub Pages fontes de publicação, consulte [Configurando uma fonte de publicação para seu site GitHub Pages](https://docs.github.com/pt/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). Para obter informações sobre a API REST, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#pages).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `page_build` ocorrer.

```yaml
on:
  page_build
```

## `public`

| Carga de evento webhook                                     | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------------------------------------------|------------------|------------------------------|-------------|
| [`public`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#public) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando o repositório do fluxo de trabalho é alterado de privado para público. Para obter informações sobre a API REST, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#edit).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `public` ocorrer.

```yaml
on:
  public
```

## `pull_request`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`pull_request`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request) | - `assigned`<br>- `unassigned`<br>- `labeled`<br>- `unlabeled`<br>- `opened`<br>- `edited`<br>- `closed`<br>- `reopened`<br>- `synchronize`<br>- `converted_to_draft`<br>- `locked`<br>- `unlocked`<br>- `enqueued`<br>- `dequeued`<br>- `milestoned`<br>- `demilestoned`<br>- `ready_for_review`<br>- `review_requested`<br>- `review_request_removed`<br>- `auto_merge_enabled`<br>- `auto_merge_disabled` | Último commit de mesclagem no branch `GITHUB_REF` | Branch de mesclagem de PR `refs/pull/PULL_REQUEST_NUMBER/merge` |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request). Por padrão, um fluxo de trabalho só é executado quando o tipo de atividade de um evento `pull_request` é `opened`, `synchronize` ou `reopened`. Para disparar fluxos de trabalho em diferentes tipos de atividades, use a palavra-chave `types`. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Os fluxos de trabalho não serão executados na atividade `pull_request` se a solicitação de pull tiver um conflito de mesclagem. O conflito de merge tem de ser resolvido primeiro. Inversamente, os fluxos de trabalho com o evento `pull_request_target` serão executados mesmo que a solicitação de pull tenha um conflito de mesclagem. Antes de usar o gatilho `pull_request_target`, você deve estar ciente dos riscos de segurança. Para obter mais informações, confira [`pull_request_target`](#pull_request_target).
    * A carga do evento do webhook `pull_request` está vazia para pull requests mescladas e pull requests provenientes de repositórios bifurcados.
    * Quando um pull request é criado ou atualizado por um fluxo de trabalho usando `GITHUB_TOKEN`, os eventos `pull_request` com os tipos de atividade `opened`, `synchronize` ou `reopened` criam execuções de fluxo de trabalho que exigem aprovação. Um usuário com permissão de gravação no repositório pode aprovar essas execuções na página da pull request. Com exceção de `workflow_dispatch` e `repository_dispatch`, outros eventos acionados por `GITHUB_TOKEN` não criam execuções de fluxo de trabalho.
    * O valor de `GITHUB_REF` varia em uma solicitação de pull fechada, dependendo de se a solicitação de pull foi mesclada ou não. Se uma solicitação de pull foi fechada, mas não mesclada, ela será `refs/pull/PULL_REQUEST_NUMBER/merge`. Se uma solicitação de pull foi fechada como resultado de ter sido mesclada, ela será totalmente qualificada como `ref` da ramificação em que foi mesclada, por exemplo, `/refs/heads/main`.

Executa o fluxo de trabalho quando ocorre uma atividade em uma pull request no repositório do fluxo de trabalho. Por exemplo, se nenhum tipo de atividade for especificado, o fluxo de trabalho será executado quando uma pull request é aberta ou reaberta, ou quando o branch principal da pull request é atualizado. Para as atividades relacionadas a revisões de solicitação de pull, a comentários de revisão de uma solicitação de pull ou a comentários de uma solicitação pull, use os eventos [`pull_request_review`](#pull_request_review), [`pull_request_review_comment`](#pull_request_review_comment), ou [`issue_comment`](#issue_comment) no lugar. Para obter informações sobre as APIs de solicitação de pull, confira [Solicitações de pull](https://docs.github.com/pt/graphql/reference/pulls#object-pullrequest) na documentação da API do GraphQL ou [Endpoints da API REST para solicitações de pull](https://docs.github.com/pt/rest/pulls)."

Observe que o `GITHUB_SHA` desse evento é o último commit de mesclagem do branch de mesclagem da pull request. Caso deseje obter a ID de commit do último commit no branch principal da pull request, use `github.event.pull_request.head.sha`. Para obter mais informações sobre ramificações de mesclagem, consulte [Solicitações de pull](https://docs.github.com/pt/pull-requests/reference/pull-requests#pull-request-refs-and-merge-branches).

### Como o ramo de mesclagem afeta seu fluxo de trabalho { #how-the-merge-branch-affects-your-workflow }

Para solicitações de pull abertas e mescláveis, os fluxos de trabalho acionados pelo evento `pull_request` definem o `GITHUB_REF` para o branch de mesclagem. Como o `actions/checkout` usa o `GITHUB_REF` por padrão, ele faz o checkout do branch de mesclagem. Os testes de CI são executados no resultado mesclado, não apenas no branch principal:

* `GITHUB_REF` é definido como `refs/pull/PULL_REQUEST_NUMBER/merge`.
* `GITHUB_SHA` é o SHA do commit de mesclagem no branch de mesclagem

Para testar apenas os commits do branch principal sem simular uma mesclagem, faça o checkout do branch principal usando `github.event.pull_request.head.sha` em seu fluxo de trabalho.

Por exemplo, você pode executar um fluxo de trabalho quando uma pull request for aberta ou reaberta.

```yaml
on:
  pull_request:
    types: [opened, reopened]
```

Você pode usar o contexto do evento para controlar ainda mais quando os trabalhos no seu fluxo de trabalho serão executados. Por exemplo, esse fluxo de trabalho será executado quando uma revisão for solicitada em uma pull request, mas o trabalho `specific_review_requested` só será executado quando uma revisão por `octo-team` for solicitada.

```yaml
on:
  pull_request:
    types: [review_requested]
jobs:
  specific_review_requested:
    runs-on: ubuntu-latest
    if: ${{ github.event.requested_team.name == 'octo-team'}}
    steps:
      - run: echo 'A review from octo-team was requested'
```

### Executar o fluxo de trabalho de `pull_request` com base no branch de cabeçalho ou no branch base de uma pull request { #running-your-pullrequest-workflow-based-on-the-head-or-base-branch-of-a-pull-request }

Você pode usar o filtro `branches` ou `branches-ignore` para configurar seu fluxo de trabalho para que ele seja executado somente em solicitações de pull direcionadas a branches específicos. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore).

Por exemplo, este fluxo de trabalho será executado quando alguém abrir uma solicitação de pull direcionada a um branch cujo nome começa com `releases/`:

```yaml
on:
  pull_request:
    types:
      - opened
    branches:
      - 'releases/**'
```

!!! note
    Se você usar os filtros `branches` e `paths`, o fluxo de trabalho só será executado quando os dois filtros forem atendidos. Por exemplo, o fluxo de trabalho a seguir só será executado quando uma solicitação de pull que inclui uma alteração em um arquivo JavaScript (`.js`) for aberta em um branch cujo nome começa com `releases/`:

                ```yaml
    on:
      pull_request:
        types:
          - opened
        branches:
          - 'releases/**'
        paths:
          - '**.js'
                ```

Para executar um trabalho com base no nome do branch de cabeçalho da solicitação de pull (em vez do nome do branch base da solicitação de pull), use o contexto `github.head_ref` em um condicional. Por exemplo, este fluxo de trabalho será executado sempre que uma solicitação de pull for aberta, mas o trabalho `run_if` só será executado se o cabeçalho da solicitação de pull for um branch cujo nome começa com `releases/`:

```yaml
on:
  pull_request:
    types:
      - opened
jobs:
  run_if:
    if: startsWith(github.head_ref, 'releases/')
    runs-on: ubuntu-latest
    steps:
      - run: echo "The head of this PR starts with 'releases/'"
```

### Executar o fluxo de trabalho de `pull_request` com base em arquivos alterados em uma solicitação de pull { #running-your-pullrequest-workflow-based-on-files-changed-in-a-pull-request }

Também é possível configurar o fluxo de trabalho para ser executado quando uma pull request alterar arquivos específicos. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore).

Por exemplo, este fluxo de trabalho será executado quando uma solicitação de pull incluir uma alteração em um arquivo JavaScript (`.js`):

```yaml
on:
  pull_request:
    paths:
      - '**.js'
```

!!! note
    Se você usar os filtros `branches` e `paths`, o fluxo de trabalho só será executado quando os dois filtros forem atendidos. Por exemplo, o fluxo de trabalho a seguir só será executado quando uma solicitação de pull que inclui uma alteração em um arquivo JavaScript (`.js`) for aberta em um branch cujo nome começa com `releases/`:

                ```yaml
    on:
      pull_request:
        types:
          - opened
        branches:
          - 'releases/**'
        paths:
          - '**.js'
                ```

### Executar o fluxo de trabalho de `pull_request` quando ocorrer uma mesclagem de solicitação de pull { #running-your-pullrequest-workflow-when-a-pull-request-merges }

Quando uma pull request faz merge, a pull request é automaticamente fechada. Para executar um fluxo de trabalho quando uma solicitação de pull surgir, use o tipo de evento `pull_request``closed` juntamente com uma condicional que verifica o valor `merged` do evento. Por exemplo, o fluxo de trabalho a seguir será executado sempre que uma pull request for fechada. O trabalho `if_merged` só será executado se a pull request também tiver sido mesclada.

```yaml
on:
  pull_request:
    types:
      - closed

jobs:
  if_merged:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
    - run: |
        echo The PR was merged
```

#### Fluxos de trabalho em repositórios com fork { #workflows-in-forked-repositories }

Por padrão, os fluxos de trabalho não são executados em repositórios com fork. É preciso habilitar o GitHub Actions na guia **Actions** do repositório com fork.

Com exceção do `GITHUB_TOKEN`, os segredos não são transmitidos para o executor quando um fluxo de trabalho é disparado de um repositório com fork. O `GITHUB_TOKEN` tem permissões somente leitura em solicitações de pull de repositórios bifurcados. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

#### Eventos de pull request para repositórios bifurcados { #pull-request-events-for-forked-repositories }

Para solicitações de pull de um repositório bifurcado para o repositório base, GitHub envia o `pull_request`, `issue_comment`, , `pull_request_review_comment`e `pull_request_target``pull_request_review`eventos para o repositório base. Nenhum evento de solicitação de pull ocorre no repositório com fork.

Quando um colaborador pela primeira vez envia uma solicitação de pull para um repositório público, um mantenedor com acesso de gravação pode precisar aprovar a execução de fluxos de trabalho na solicitação de pull. Para saber mais, confira [Aprovando execuções de fluxo de trabalho de forks](../../how-tos/manage-workflow-runs/approve-runs-from-forks.md).

Para pull requests de um repositório com forks para um repositório privado, os fluxos de trabalho só são executados quando eles são habilitados, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

!!! note
    Os fluxos de trabalho disparados por Dependabot solicitações de pull são tratados como se fossem de um repositório bifurcado e também estão sujeitos a essas restrições.

## `pull_request_comment` (usar `issue_comment`) { #pullrequestcomment-use-issuecomment }

Para executar o fluxo de trabalho quando um comentário em uma solicitação de pull (não em um diff de uma solicitação de pull) é criado, editado ou excluído, use o evento [`issue_comment`](#issue_comment). Para as atividades relacionadas a avaliações de solicitação de pull ou a comentários de avaliações de uma solicitação de pull, use os eventos [`pull_request_review`](#pull_request_review) ou [`pull_request_review_comment`](#pull_request_review_comment).

## `pull_request_review`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`pull_request_review`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request_review) | - `submitted`<br>- `edited`<br>- `dismissed` | Último commit de mesclagem no branch `GITHUB_REF` | Branch de mesclagem de PR `refs/pull/PULL_REQUEST_NUMBER/merge` |

!!! note
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request_review). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

Executa o fluxo de trabalho quando uma revisão de pull request é enviada, editada ou ignorada. Uma revisão de pull request é um grupo de comentários de revisão de pull request, além de um comentário e estado de texto. Para as atividades relacionadas a comentários de revisão de uma solicitação de pull ou a comentários de uma solicitação de pull, use os eventos [`pull_request_review_comment`](#pull_request_review_comment) ou [`issue_comment`](#issue_comment) no lugar. Para obter informações sobre as APIs de avaliação de solicitação de pull, confira [Solicitações de pull](https://docs.github.com/pt/graphql/reference/pulls#object-pullrequest) na documentação da API do GraphQL ou [Endpoints da API REST para solicitações de pull](https://docs.github.com/pt/rest/pulls#reviews).

Por exemplo, você poderá executar um fluxo de trabalho quando uma revisão de solicitação de pull for `edited` ou `dismissed`.

```yaml
on:
  pull_request_review:
    types: [edited, dismissed]
```

### Executando um fluxo de trabalho quando uma pull request é aprovada { #running-a-workflow-when-a-pull-request-is-approved }

Para executar o fluxo de trabalho quando uma solicitação de pull tiver sido aprovada, dispare o fluxo de trabalho com o tipo `submitted` de evento `pull_request_review` e verifique o estado de revisão com a propriedade `github.event.review.state`. Por exemplo, este fluxo de trabalho será executado sempre que uma revisão de solicitação de pull for enviada, mas o trabalho `approved` só será executado se a revisão enviada for uma revisão de aprovação:

```yaml
on:
  pull_request_review:
    types: [submitted]

jobs:
  approved:
    if: github.event.review.state == 'approved'
    runs-on: ubuntu-latest
    steps:
      - run: echo "This PR was approved"
```

#### Fluxos de trabalho em repositórios com fork { #workflows-in-forked-repositories-1 }

Por padrão, os fluxos de trabalho não são executados em repositórios com fork. É preciso habilitar o GitHub Actions na guia **Actions** do repositório com fork.

Com exceção do `GITHUB_TOKEN`, os segredos não são transmitidos para o executor quando um fluxo de trabalho é disparado de um repositório com fork. O `GITHUB_TOKEN` tem permissões somente leitura em solicitações de pull de repositórios bifurcados. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

#### Eventos de pull request para repositórios bifurcados { #pull-request-events-for-forked-repositories-1 }

Para solicitações de pull de um repositório bifurcado para o repositório base, GitHub envia o `pull_request`, `issue_comment`, , `pull_request_review_comment`e `pull_request_target``pull_request_review`eventos para o repositório base. Nenhum evento de solicitação de pull ocorre no repositório com fork.

Quando um colaborador pela primeira vez envia uma solicitação de pull para um repositório público, um mantenedor com acesso de gravação pode precisar aprovar a execução de fluxos de trabalho na solicitação de pull. Para saber mais, confira [Aprovando execuções de fluxo de trabalho de forks](../../how-tos/manage-workflow-runs/approve-runs-from-forks.md).

Para pull requests de um repositório com forks para um repositório privado, os fluxos de trabalho só são executados quando eles são habilitados, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

!!! note
    Os fluxos de trabalho disparados por Dependabot solicitações de pull são tratados como se fossem de um repositório bifurcado e também estão sujeitos a essas restrições.

## `pull_request_review_comment`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`pull_request_review_comment`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request_review_comment) | - `created`<br>- `edited`<br>- `deleted` | Último commit de mesclagem no branch `GITHUB_REF` | Branch de mesclagem de PR `refs/pull/PULL_REQUEST_NUMBER/merge` |

!!! note
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request_review_comment). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

Executa o fluxo de trabalho quando um comentário de revisão de pull request é modificado. Um comentário de revisão de pull request é um comentário no diff de uma pull request. Para as atividades relacionadas a revisões de solicitação de pull ou a comentários de uma solicitação de pull, use os eventos [`pull_request_review`](#pull_request_review) ou [`issue_comment`](#issue_comment) no lugar. Para obter informações sobre as APIs dos comentários da análise de solicitação de pull, confira [Solicitações de pull](https://docs.github.com/pt/graphql/reference/pulls#object-pullrequestreviewcomment) na documentação da API do GraphQL ou [Endpoints da API REST para solicitações de pull](https://docs.github.com/pt/rest/pulls#comments).

Por exemplo, você poderá executar um fluxo de trabalho quando um comentário de revisão de uma solicitação de pull for `created` ou `deleted`.

```yaml
on:
  pull_request_review_comment:
    types: [created, deleted]
```

#### Fluxos de trabalho em repositórios com fork { #workflows-in-forked-repositories-2 }

Por padrão, os fluxos de trabalho não são executados em repositórios com fork. É preciso habilitar o GitHub Actions na guia **Actions** do repositório com fork.

Com exceção do `GITHUB_TOKEN`, os segredos não são transmitidos para o executor quando um fluxo de trabalho é disparado de um repositório com fork. O `GITHUB_TOKEN` tem permissões somente leitura em solicitações de pull de repositórios bifurcados. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

#### Eventos de pull request para repositórios bifurcados { #pull-request-events-for-forked-repositories-2 }

Para solicitações de pull de um repositório bifurcado para o repositório base, GitHub envia o `pull_request`, `issue_comment`, , `pull_request_review_comment`e `pull_request_target``pull_request_review`eventos para o repositório base. Nenhum evento de solicitação de pull ocorre no repositório com fork.

Quando um colaborador pela primeira vez envia uma solicitação de pull para um repositório público, um mantenedor com acesso de gravação pode precisar aprovar a execução de fluxos de trabalho na solicitação de pull. Para saber mais, confira [Aprovando execuções de fluxo de trabalho de forks](../../how-tos/manage-workflow-runs/approve-runs-from-forks.md).

Para pull requests de um repositório com forks para um repositório privado, os fluxos de trabalho só são executados quando eles são habilitados, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

!!! note
    Os fluxos de trabalho disparados por Dependabot solicitações de pull são tratados como se fossem de um repositório bifurcado e também estão sujeitos a essas restrições.

## `pull_request_target`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
|  |  |  | !!! note<br>Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#pull_request). Por padrão, um fluxo de trabalho só é executado quando o tipo de atividade de um evento `pull_request_target` é `opened`, `synchronize` ou `reopened`. Para disparar fluxos de trabalho em diferentes tipos de atividades, use a palavra-chave `types`. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).<br>Executa o fluxo de trabalho quando ocorre uma atividade em uma pull request no repositório do fluxo de trabalho. Por exemplo, se nenhum tipo de atividade for especificado, o fluxo de trabalho será executado quando uma pull request é aberta ou reaberta, ou quando o branch principal da pull request é atualizado.<br>Esse evento é executado no contexto da ramificação padrão do repositório base, em vez de ser no contexto do commit de mesclagem, como ocorre no evento `pull_request`. Isso impede a execução de código inseguro do cabeçalho da pull request que poderia alterar seu repositório ou roubar quaisquer segredos que você usa no fluxo de trabalho. Este evento permite que seu fluxo de trabalho faça coisas como etiquetar ou comentar nas pull requests a partir das bifurcações. Evite usar este evento se você precisar criar ou executar o código a partir da pull request.<br>Para garantir a segurança do repositório, branches com nomes que correspondem a determinados padrões (como aqueles que se parecem com SHAs) podem não disparar fluxos de trabalho com o evento `pull_request_target`.<br>!!! warning<br>A execução de código não confiável no gatilho `pull_request_target` pode levar a vulnerabilidades de segurança. Essas vulnerabilidades incluem o envenenamento de cache e a concessão de acesso não intencional a segredos ou privilégios de gravação. Para saber como usar esse gatilho com segurança, consulte [Uso seguro de pull_request_target](../security/securely-using-pull_request_target.md). Para obter mais detalhes sobre os riscos envolvidos, consulte [Referência de uso seguro](../security/secure-use.md#mitigating-the-risks-of-untrusted-code-checkout) e [Preventing pwn requests](https://securitylab.github.com/research/github-actions-preventing-pwn-requests) em GitHub Security Lab.<br>Por exemplo, você poderá executar um fluxo de trabalho quando uma solicitação de pull for `assigned`, `opened`, `synchronize` ou `reopened`. |
```yaml
on:
  pull_request_target:
    types: [assigned, opened, synchronize, reopened]
```

### Executar o fluxo de trabalho de `pull_request_target` com base no branch de cabeçalho ou no branch base de uma pull request { #running-your-pullrequesttarget-workflow-based-on-the-head-or-base-branch-of-a-pull-request }

Você pode usar o filtro `branches` ou `branches-ignore` para configurar seu fluxo de trabalho para que ele seja executado somente em solicitações de pull direcionadas a branches específicos. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore).

Por exemplo, este fluxo de trabalho será executado quando alguém abrir uma solicitação de pull direcionada a um branch cujo nome começa com `releases/`:

```yaml
on:
  pull_request_target:
    types:
      - opened
    branches:
      - 'releases/**'
```

!!! note
    Se você usar os filtros `branches` e `paths`, o fluxo de trabalho só será executado quando os dois filtros forem atendidos. Por exemplo, o fluxo de trabalho a seguir só será executado quando uma solicitação de pull que inclui uma alteração em um arquivo JavaScript (`.js`) for aberta em um branch cujo nome começa com `releases/`:

                ```yaml
    on:
      pull_request_target:
        types:
          - opened
        branches:
          - 'releases/**'
        paths:
          - '**.js'
                ```

Para executar um trabalho com base no nome do branch de cabeçalho da solicitação de pull (em vez do nome do branch base da solicitação de pull), use o contexto `github.head_ref` em um condicional. Por exemplo, este fluxo de trabalho será executado sempre que uma solicitação de pull for aberta, mas o trabalho `run_if` só será executado se o cabeçalho da solicitação de pull for um branch cujo nome começa com `releases/`:

```yaml
on:
  pull_request_target:
    types:
      - opened
jobs:
  run_if:
    if: startsWith(github.head_ref, 'releases/')
    runs-on: ubuntu-latest
    steps:
      - run: echo "The head of this PR starts with 'releases/'"
```

### Executar o fluxo de trabalho de `pull_request_target` com base em arquivos alterados em uma solicitação de pull { #running-your-pullrequesttarget-workflow-based-on-files-changed-in-a-pull-request }

Você pode usar o filtro `paths` ou `paths-ignore` para configurar o fluxo de trabalho para ser executado quando uma solicitação de pull alterar arquivos específicos. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore).

Por exemplo, este fluxo de trabalho será executado quando uma solicitação de pull incluir uma alteração em um arquivo JavaScript (`.js`):

```yaml
on:
  pull_request_target:
    paths:
      - '**.js'
```

!!! note
    Se você usar os filtros `branches` e `paths`, o fluxo de trabalho só será executado quando os dois filtros forem atendidos. Por exemplo, o fluxo de trabalho a seguir só será executado quando uma solicitação de pull que inclui uma alteração em um arquivo JavaScript (`.js`) for aberta em um branch cujo nome começa com `releases/`:

                ```yaml
    on:
      pull_request_target:
        types:
          - opened
        branches:
          - 'releases/**'
        paths:
          - '**.js'
                ```

### Executar o fluxo de trabalho de `pull_request_target` quando ocorrer uma mesclagem de solicitação de pull { #running-your-pullrequesttarget-workflow-when-a-pull-request-merges }

Quando uma pull request faz merge, a pull request é automaticamente fechada. Para executar um fluxo de trabalho quando uma solicitação de pull surgir, use o tipo de evento `pull_request_target``closed` juntamente com uma condicional que verifica o valor `merged` do evento. Por exemplo, o fluxo de trabalho a seguir será executado sempre que uma pull request for fechada. O trabalho `if_merged` só será executado se a pull request também tiver sido mesclada.

```yaml
on:
  pull_request_target:
    types:
      - closed

jobs:
  if_merged:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
    - run: |
        echo The PR was merged
```

## `push`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`push`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#push) | Não aplicável | Commit de extremidade para o ref via push. Quando você exclui uma ramificação, o SHA na execução do fluxo de trabalho (e os refs associados) é revertido para a ramificação padrão do repositório. | ref atualizado |

!!! note
    * O conteúdo do webhook disponível para GitHub Actions não inclui os atributos `added`, `removed` e `modified` no objeto `commit`. Você pode recuperar o objeto de commit completo usando a API. Para obter mais informações, confira [Confirmações](https://docs.github.com/pt/graphql/reference/commits#object-commit) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para commits](https://docs.github.com/pt/rest/commits#get-a-commit).
    * Os eventos não serão criados se mais de 5.000 ramificações forem enviadas por push ao mesmo tempo. Os eventos não serão criados para tags quando mais de três tags forem transmitidas ao mesmo tempo.

Executa o fluxo de trabalho quando você efetua push em um commit ou tag ou quando cria um repositório a partir de um modelo. Isso inclui fluxos de trabalho que não são mesclados no branch padrão. Para obter mais informações, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md#running-your-workflow-only-when-a-push-to-specific-branches-occurs).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `push` ocorrer.

```yaml
on:
  push
```

!!! note
    Quando um evento de webhook `push` aciona uma execução de fluxo de trabalho, o campo "enviado por" da interface do usuário de ações mostra a conta do pusher e não o autor ou o confirmador. No entanto, se as alterações forem enviadas para um repositório usando autenticação SSH com uma chave de implantação, o campo "enviado por" será o administrador do repositório que verificou a chave de implantação quando ela foi adicionada a um repositório.

### Executando o fluxo de trabalho apenas quando um push para branches específicos ocorre { #running-your-workflow-only-when-a-push-to-specific-branches-occurs }

Você pode usar o filtro `branches` ou `branches-ignore` para configurar seu fluxo de trabalho para ser executado somente quando branches específicos forem enviados por push. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpushbranchestagsbranches-ignoretags-ignore).

Por exemplo, este fluxo de trabalho será executado quando alguém efetuar push para `main` ou para um branch que começa com `releases/`.

```yaml
on:
  push:
    branches:
      - 'main'
      - 'releases/**'
```

!!! note
    Se você usar os filtros `branches` e `paths`, o fluxo de trabalho só será executado quando os dois filtros forem atendidos. Por exemplo, o fluxo de trabalho a seguir só será executado quando um push que inclui uma alteração em um arquivo JavaScript (`.js`) for feito em um branch cujo nome começa com `releases/`:

                ```yaml
    on:
      push:
        branches:
          - 'releases/**'
        paths:
          - '**.js'
                ```

### Executando o fluxo de trabalho somente quando ocorre um push de tags específicas { #running-your-workflow-only-when-a-push-of-specific-tags-occurs }

Você pode usar o filtro `tags` ou `tags-ignore` para configurar seu fluxo de trabalho para ser executado somente quando marcas específicas forem enviadas por push. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpushbranchestagsbranches-ignoretags-ignore).

Por exemplo, este fluxo de trabalho será executado quando alguém efetuar push de uma marca que começa com `v1.`.

```yaml
on:
  push:
    tags:
      - v1.**
```

### Executando seu fluxo de trabalho apenas quando um push afeta arquivos específicos { #running-your-workflow-only-when-a-push-affects-specific-files }

Você pode usar o filtro `paths` ou `paths-ignore` para configurar o fluxo de trabalho para ser executado quando ocorrer um push para arquivos específicos. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore).

Por exemplo, este fluxo de trabalho será executado quando alguém efetuar push de uma alteração para um arquivo JavaScript (`.js`):

```yaml
on:
  push:
    paths:
      - '**.js'
```

## `registry_package`

| Carga de evento webhook                                                | Tipos de Atividade            | `GITHUB_SHA`               | `GITHUB_REF`                      |
|----------------------------------------------------------------------|-----------------------------|--------------------------|---------------------------------|
| [`registry_package`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#package) | - `published`<br>- `updated`  | Commit do pacote publicado | Branch ou tag do pacote publicado |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#registry_package). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Ao realizar push de imagens de contêiner de várias arquiteturas, esse evento ocorre uma vez por manifesto, portanto, você pode observar o fluxo de trabalho sendo disparado várias vezes. Para atenuar isso e executar apenas o trabalho de fluxo de trabalho para o evento que contém as informações reais da marca de imagem, use um condicional:

                ```yaml
    jobs:
        job_name:
            if: $true
                ```

Executa o fluxo de trabalho quando ocorre atividade relacionada a GitHub Packages em seu repositório. Para obter mais informações, consulte [GitHub Packages Documentação](https://docs.github.com/pt/packages).

Por exemplo, você pode executar um fluxo de trabalho quando uma nova versão do pacote foi `published`.

```yaml
on:
  registry_package:
    types: [published]
```

## `release`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [`release`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#release) | - `published` <br>- `unpublished` <br>- `created` <br>- `edited` <br>- `deleted` <br>- `prereleased`<br> - `released` | Último commit na versão com tag | Referência de marca da versão `refs/tags/<tag_name>` |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Para obter informações sobre cada tipo de atividade, consulte [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#release). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Os fluxos de trabalho não são disparados para os tipos de atividade `created`, `edited`, ou `deleted` para versões de rascunho. Quando você cria sua versão pela interface de usuário do GitHub, sua versão pode ser salva automaticamente como um rascunho.
    * O tipo `prereleased` não disparará para pré-versões publicadas de versões de rascunho, mas o tipo `published` disparará. Caso deseje que um fluxo de trabalho seja executado quando as versões estáveis *e* de pré-lançamento forem publicadas, assine `published` em vez de `released` e `prereleased`.

Executa o fluxo de trabalho quando a atividade de da versão no repositório ocorre. Para obter informações sobre as APIs da lançamento, confira [Lançamentos](https://docs.github.com/pt/graphql/reference/releases#object-release) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para lançamentos e ativos de lançamento](https://docs.github.com/pt/rest/releases)" na documentação da API REST.

Por exemplo, você poderá executar um fluxo de trabalho quando uma versão for `published`.

```yaml
on:
  release:
    types: [published]
```

## `repository_dispatch`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [repository_dispatch](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#repository_dispatch) | Personalizado | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Você pode usar a GitHub API para disparar um evento de webhook chamado [`repository_dispatch`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#repository_dispatch) quando quiser disparar um fluxo de trabalho para atividades que ocorrem fora de GitHub. Para obter mais informações, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos/repos#create-a-repository-dispatch-event).

Ao fazer uma solicitação para criar um evento `repository_dispatch`, você precisa especificar um `event_type` para descrever o tipo de atividade. Por padrão, todos os tipos de atividade `repository_dispatch` disparam a execução de um fluxo de trabalho. Você pode usar a palavra-chave `types` para limitar o fluxo de trabalho a ser executado quando um valor `event_type` específico é enviado na carga do webhook `repository_dispatch`.

```yaml
on:
  repository_dispatch:
    types: [test_result]
```

!!! note
    O valor de `event_type` está limitado a 100 caracteres.

Todos os dados enviados por meio do parâmetro `client_payload` ficarão disponíveis no contexto `github.event` no seu fluxo de trabalho. Por exemplo, se você enviar esse texto de solicitação quando criar um evento de despacho de repositório:

```json
{
  "event_type": "test_result",
  "client_payload": {
    "passed": false,
    "message": "Error: timeout"
  }
}
```

então você poderá acessar a carga em um fluxo de trabalho assim:

```yaml
on:
  repository_dispatch:
    types: [test_result]

jobs:
  run_if_failure:
    if: ${{ !github.event.client_payload.passed }}
    runs-on: ubuntu-latest
    steps:
      - env:
          MESSAGE: ${{ github.event.client_payload.message }}
        run: echo $MESSAGE
```

!!! note
    * O número máximo de propriedades de nível superior em `client_payload` é 10.
    * O payload pode conter no máximo 65.535 caracteres.

## `schedule`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------|------------------|------------------------------|-------------|
| Não aplicável           | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    * O evento `schedule` pode ser atrasado durante períodos de cargas altas de execuções de fluxo de trabalho do GitHub Actions. Os tempos de carregamento altos incluem o início de cada hora. Se a carga for suficientemente alta o suficiente, alguns trabalhos enfileirados talvez sejam descartados. Para diminuir a probabilidade de atraso, agende o fluxo de trabalho para ser executado em uma parte diferente da hora.
    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Os fluxos de trabalho agendados só serão executados no branch padrão.
    * Em um repositório público, os fluxos de trabalho agendados são automaticamente desabilitados quando nenhuma atividade do repositório ocorreu em 60 dias. Para obter informações sobre como reabilitar fluxos de trabalho desabilitados, confira [Desabilitar e habilitar um fluxo de trabalho](../../how-tos/manage-workflow-runs/disable-and-enable-workflows.md#enabling-a-workflow).

O evento `schedule` permite disparar um fluxo de trabalho em um horário agendado.

**Exemplo:**

```yaml
 on:
   schedule:
     - cron: "15 4,5 * * *"
```

Use a [sintaxe cron POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07) para agendar fluxos de trabalho para serem executados em horários específicos.
Por padrão, fluxos de trabalho agendados são executados em UTC. Opcionalmente, você pode especificar um fuso horário usando uma cadeia de [caracteres de fuso horário IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) para agendamento. Fluxos de trabalho agendados são executados sobre o último commit no branch padrão. O intervalo mais curto que você pode executar fluxos de trabalho agendados é a cada 5 minutos.

!!! note
    Para agendamentos que definem `timezone` em um fuso horário que observa o horário de verão, durante as transições de adiantamento do horário de verão, fluxos de trabalho agendados durante as horas não contabilizadas avançam para o próximo horário válido. Por exemplo, um horário agendado para as 2h30 avança para as 3h00.

A sintaxe cron tem cinco campos separados por um espaço, e cada campo representa uma unidade de tempo.

```text
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)
│ │ │ │ │
* * * * *
```

Você pode usar estes operadores em qualquer um dos cinco campos:

| Operador | Descrição | Exemplo |
| --- | --- | --- |
| \* | Qualquer valor |  |
| `15 * * * *` é executado no minuto 15 de cada hora todos os dias. |  |  |
| , | Separador de valores em lista |  |
| `2,10 4,5 * * *` é executado nos minutos 2 e 10 da quarta e da quinta hora todos os dias. |  |  |
| - | Intervalo de valores |  |
| `30 4-6 * * *` é executado no minuto 30 da 4ª, 5ª e 6ª hora. |  |  |
| / | Valores de etapa |  |
| `20/15 * * * *` é executado a cada 15 minutos, começando do minuto 20 ao 59 (minutos 20, 35 e 50). |  | Este exemplo inicia o fluxo de trabalho para ser executado às 5h30, no fuso horário América/New_York, de segunda a sexta-feira. |
```yaml
on:
  schedule:
    - cron: '30 5 * * 1-5'
      timezone: "America/New_York"
```

Um fluxo de trabalho individual pode ser disparado por vários eventos `schedule`. Acesse o evento `schedule` que disparou o fluxo de trabalho por meio do contexto `github.event.schedule`. Este exemplo dispara o fluxo de trabalho para ser executado às 5:30 UTC toda segunda-feira a quinta-feira e às 17:30 UTC às terças e quintas-feiras, mas ignora a etapa `Not on Monday or Wednesday` na segunda-feira e na quarta-feira.

```yaml
on:
  schedule:
    - cron: '30 5 * * 1,3'
    - cron: '30 5,17 * * 2,4'

jobs:
  test_schedule:
    runs-on: ubuntu-latest
    steps:
      - name: Not on Monday or Wednesday
        if: github.event.schedule != '30 5 * * 1,3'
        run: echo "This step will be skipped on Monday and Wednesday"
      - name: Every time
        run: echo "This step will always run"
```

!!! note
    GitHub Actions não dá suporte à sintaxe não padrão `@yearly`, `@monthly`, `@weekly`, `@daily`, `@hourly` e `@reboot`.

Você pode usar o [crontab guru](https://crontab.guru/) para ajudar a gerar a sintaxe cron e confirmar a hora em que ela será executada. Para ajudar você a começar, há também uma lista de [exemplos do crontab guru](https://crontab.guru/examples.html).

### `actor` para fluxos de trabalho agendados { #actor-for-scheduled-workflows }

Determinados eventos de repositório alteram a `actor` associada ao fluxo de trabalho. Por exemplo, um usuário que altera o branch padrão do repositório, o que altera o branch no qual os fluxos de trabalho agendados são executados, torna-se `actor` para esses fluxos de trabalho agendados.

Para um fluxo de trabalho agendado desativado, se um usuário com permissões de `write` para o repositório fizer um commit que altera a agenda de `cron` no fluxo de trabalho, o fluxo de trabalho será reativado e esse usuário se tornará o `actor` associado a qualquer execução de fluxo de trabalho.

As notificações de fluxos de trabalho agendados são enviadas ao usuário que modificou a sintaxe cron no arquivo do fluxo de trabalho. Para obter mais informações, confira [Notificações para execuções de fluxo de trabalho](../../concepts/workflows-and-actions/notifications-for-workflow-runs.md).

!!! note
    Para uma empresa com Enterprise Managed Users, disparar um fluxo de trabalho agendado requer que o status da conta de `actor` usuário associada ao fluxo de trabalho esteja ativo no momento (ou seja, não está suspenso ou excluído).

    * Os fluxos de trabalho agendados não serão executados se o último `actor` associado ao fluxo de trabalho agendado tiver sido desprovisionado pelo Enterprise Managed User IdP (provedor de identidade). No entanto, se o último `actor`Enterprise Managed User não tiver sido desprovisionado pelo IdP e tiver sido removido apenas como membro de uma determinada organização na empresa, os fluxos de trabalho agendados ainda serão executados com esse usuário definido como .`actor`
    * Da mesma forma, para uma empresa sem Enterprise Managed Users, a remoção de um usuário de uma organização não impedirá que fluxos de trabalho agendados que tinham esse usuário como seu `actor` sejam executados.
    * Assim, o status *da conta de usuário*, tanto em cenários Enterprise Managed User quanto em cenários nãoEnterprise Managed User, é o que importa, *não* o *status de associação* do usuário na organização onde o fluxo de trabalho agendado está localizado.

## `status`

| Carga de evento webhook                                     | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------------------------------------------|------------------|------------------------------|-------------|
| [`status`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#status) | Não aplicável      | Último commit no branch padrão | Branch padrão |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando o status do commit de Git é alterado. Por exemplo, os commits podem ser marcados como `error`, `failure`, `pending` ou `success`. Caso deseje fornecer mais detalhes sobre a alteração de status, o ideal é usar o evento [`check_run`](#check_run). Para obter informações sobre as APIs de status do commit, confira [Confirmações](https://docs.github.com/pt/graphql/reference/commits#object-status) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para commits](https://docs.github.com/pt/rest/commits#commit-statuses).

Por exemplo, você poderá executar um fluxo de trabalho quando o evento `status` ocorrer.

```yaml
on:
  status
```

Caso deseje executar um trabalho no seu fluxo de trabalho com base no novo estado de commit, use o contexto `github.event.state`. Por exemplo, o fluxo de trabalho a seguir é disparado quando um status de commit é alterado, mas o trabalho `if_error_or_failure` só é executado se o novo estado de commit é `error` ou `failure`.

```yaml
on:
  status
jobs:
  if_error_or_failure:
    runs-on: ubuntu-latest
    if: >-
      github.event.state == 'error' ||
      github.event.state == 'failure'
    steps:
      - env:
          DESCRIPTION: ${{ github.event.description }}
        run: |
          echo The status is error or failed: $DESCRIPTION
```

## `watch`

| Carga de evento webhook                                   | Tipos de Atividade | `GITHUB_SHA`                   | `GITHUB_REF`  |
|---------------------------------------------------------|------------------|------------------------------|-------------|
| [`watch`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#watch) | - `started`        | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. Embora haja suporte apenas para o `started` tipo de atividade, especificar o tipo de atividade manterá seu fluxo de trabalho específico se mais tipos de atividade forem adicionados no futuro. Para obter informações sobre cada tipo de atividade, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#watch). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Executa o fluxo de trabalho quando o repositório do fluxo de trabalho é favoritado. Para obter informações sobre as APIs de solicitação de pull, confira [Activity](https://docs.github.com/pt/graphql/reference/activity#mutation-addstar) na documentação da API do GraphQL ou [Pontos de extremidade da API REST para estrela](https://docs.github.com/pt/rest/activity/starring)."

Por exemplo, você poderá executar um fluxo de trabalho quando alguém adiciona um repositório aos favoritos, que é o tipo de atividade `started` para um evento de inspeção.

```yaml
on:
  watch:
    types: [started]
```

## `workflow_call`

| Carga de evento webhook                | Tipos de Atividade | `GITHUB_SHA`                           | `GITHUB_REF`                           |
|--------------------------------------|------------------|--------------------------------------|--------------------------------------|
| Igual ao fluxo de trabalho de chamadas | Não aplicável      | Igual ao fluxo de trabalho de chamadas | Igual ao fluxo de trabalho de chamadas |

`workflow_call` é usado para indicar que um fluxo de trabalho pode ser chamado por outro fluxo de trabalho. Quando um fluxo de trabalho é disparado com o evento `workflow_call`, a carga do evento no fluxo de trabalho chamado é a mesma carga do evento do fluxo de trabalho de chamada. Para obter mais informações, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

O exemplo abaixo só executa o fluxo de trabalho quando é chamado a partir de outro fluxo de trabalho:

```yaml
on: workflow_call
```

## `workflow_dispatch`

| Carga de evento webhook | Tipos de Atividade | `GITHUB_SHA` | `GITHUB_REF` |
| --- | --- | --- | --- |
| [workflow_dispatch](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_dispatch) | Não aplicável | Último commit no branch `GITHUB_REF` ou na marcação | Branch ou marcação que recebeu expedição |

!!! note
    Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.

Para permitir que um fluxo de trabalho seja disparado manualmente, configure o evento `workflow_dispatch`. Na interface do usuário do GitHub, o botão "Executar fluxo de trabalho" será exibido se o arquivo do fluxo de trabalho existir na ramificação padrão. Depois que um fluxo de trabalho for executado pelo menos uma vez, você poderá dispará-lo em qualquer branch ou tag por meio da API GitHub ou GitHub CLI. Para obter mais informações, confira [Executar um fluxo de trabalho manualmente](../../how-tos/manage-workflow-runs/manually-run-a-workflow.md).

```yaml
on: workflow_dispatch
```

### Fornecendo entradas { #providing-inputs }

É possível configurar as propriedades de entrada definidas por personalização, os valores-padrão de entrada e as entradas obrigatórias para o evento diretamente no seu fluxo de trabalho. Ao disparar o evento, você pode fornecer a `ref` e qualquer `inputs`. Quando o fluxo de trabalho é executado, você pode acessar os valores de entrada no contexto `inputs`. Para obter mais informações, confira [Referência de contextos](contexts.md).

!!! note
    * O fluxo de trabalho também receberá as entradas no contexto de `github.event.inputs`. As informações no contexto `inputs` e no contexto `github.event.inputs` são idênticas, exceto que o contexto `inputs` preserva valores boolianos como boolianos em vez de convertê-los em cadeias de caracteres. O tipo `choice` é resolvido para uma cadeia de caracteres e é uma única opção selecionável.
    * O número máximo de propriedades de nível superior é `inputs` 25 .
    * O conteúdo máximo para `inputs` é de 65.535 caracteres.

Esse exemplo define entradas chamadas `logLevel`, `tags` e `environment`. Você passa os valores destas entradas para o fluxo de trabalho quando o executa. Em seguida, esse fluxo de trabalho imprime os valores no log usando as propriedades do contexto `inputs.logLevel`, `inputs.tags` e `inputs.environment`.

```yaml
on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning'
        type: choice
        options:
        - info
        - warning
        - debug
      tags:
        description: 'Test scenario tags'
        required: false
        type: boolean
      environment:
        description: 'Environment to run tests against'
        type: environment
        required: true

jobs:
  log-the-inputs:
    runs-on: ubuntu-latest
    steps:
      - run: |
          echo "Log level: $LEVEL"
          echo "Tags: $TAGS"
          echo "Environment: $ENVIRONMENT"
        env:
          LEVEL: ${{ inputs.logLevel }}
          TAGS: ${{ inputs.tags }}
          ENVIRONMENT: ${{ inputs.environment }}
```

Se você executar este fluxo de trabalho em um navegador, você deverá inserir valores para as entradas necessárias manualmente antes de o fluxo de trabalho ser executado.

![Captura de tela de uma lista de execuções de fluxo de trabalho. Um menu suspenso, rotulado "Executar fluxo de trabalho" e expandido para mostrar os campos de entrada, está contornado em laranja escuro.](https://docs.github.com/assets/images/help/actions/workflow-dispatch-inputs.png)

Você também pode passar entradas ao executar um fluxo de trabalho de um script ou usando GitHub CLI. Por exemplo:

```shell
gh workflow run run-tests.yml -f logLevel=warning -f tags=false -f environment=staging
```

Para obter mais informações, consulte as GitHub CLI informações em [Executar um fluxo de trabalho manualmente](../../how-tos/manage-workflow-runs/manually-run-a-workflow.md).

## `workflow_run`

| Carga de evento webhook                                                 | Tipos de Atividade                                  | `GITHUB_SHA`                   | `GITHUB_REF`  |
|-----------------------------------------------------------------------|---------------------------------------------------|------------------------------|-------------|
| [`workflow_run`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_run) | - `completed`<br>- `requested`<br>- `in_progress`   | Último commit no branch padrão | Branch padrão |

!!! note
    *
    Mais de um tipo de atividade aciona este evento. O `requested` tipo de atividade não ocorre quando um fluxo de trabalho é executado novamente. Para obter informações sobre cada tipo de atividade, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_run). Por padrão, todos os tipos de atividade disparam fluxos de trabalho que são executados nesse evento. Você pode limitar suas execuções de fluxo de trabalho a tipos de atividades específicos usando a palavra-chave `types`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onevent_nametypes).

    * Esse evento vai disparar apenas um fluxo de trabalho executado se o arquivo de fluxo de trabalho existe no branch padrão.
    * Não é possível usar `workflow_run` para encadear mais de três níveis de fluxos de trabalho. Por exemplo, se você tentar disparar cinco fluxos de trabalho (chamados de `B` para `F`) para serem executados sequencialmente após a execução de um fluxo de trabalho `A` inicial (ou seja: `A` → `B` → `C` → `D` → `E` →`F`), os fluxos de trabalho `E` e `F` não serão executados.

Este evento ocorre quando uma execução do fluxo de trabalho é solicitada ou concluída. Ele permite que você execute um fluxo de trabalho baseado na execução ou conclusão de outro fluxo de trabalho. O fluxo de trabalho iniciado pelo evento `workflow_run` pode acessar segredos e gravar tokens, mesmo que o fluxo de trabalho anterior não tenha essa permissão. Isso é útil em casos em que o fluxo de trabalho anterior não é intencionalmente privilegiado, mas você precisa tomar uma ação privilegiada em um fluxo de trabalho posterior.

!!! warning
    A execução de código não confiável no gatilho `workflow_run` pode levar a vulnerabilidades de segurança. Essas vulnerabilidades incluem o envenenamento de cache e a concessão de acesso não intencional a segredos ou privilégios de gravação. Para obter mais informações, consulte [Referência de uso seguro](../security/secure-use.md#mitigating-the-risks-of-untrusted-code-checkout) na documentação do GitHub Enterprise Cloud e [Preventing pwn requests](https://securitylab.github.com/research/github-actions-preventing-pwn-requests) no site do GitHub Security Lab.

Neste exemplo, um fluxo de trabalho está configurado para ser executado após o fluxo de trabalho "Executar Testes" separado ser concluído.

```yaml
on:
  workflow_run:
    workflows: [Run Tests]
    types:
      - completed
```

Se você especificar vários `workflows` para o evento `workflow_run`, apenas um dos fluxos de trabalho precisará ser executado. Por exemplo, um fluxo de trabalho com o seguinte gatilho será executado sempre que o fluxo de trabalho "Staging" ou "Lab" forem concluídos.

```yaml
on:
  workflow_run:
    workflows: [Staging, Lab]
    types:
      - completed
```

### Executando um fluxo de trabalho com base na conclusão de outro fluxo de trabalho { #running-a-workflow-based-on-the-conclusion-of-another-workflow }

A execução de um fluxo de trabalho é acionada independentemente da conclusão do fluxo de trabalho anterior. Caso deseje executar um trabalho ou uma etapa com base no resultado do fluxo de trabalho disparado, use uma condição com a propriedade `github.event.workflow_run.conclusion`. Por exemplo, este fluxo de trabalho será executado sempre que um fluxo de trabalho chamado "Build" for concluído, mas o trabalho `on-success` só será executado se o fluxo de trabalho "Build" for bem-sucedido, e o trabalho `on-failure` só será executado se o fluxo de trabalho "Build" falhar:

```yaml
on:
  workflow_run:
    workflows: [Build]
    types: [completed]

jobs:
  on-success:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - run: echo 'The triggering workflow passed'
  on-failure:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - run: echo 'The triggering workflow failed'
```

### Limitando seu fluxo de trabalho para ser executado com base em branches { #limiting-your-workflow-to-run-based-on-branches }

Você pode usar o filtro `branches` ou `branches-ignore` para especificar os branches em que o fluxo de trabalho de gatilho precisa ser executado para disparar o fluxo de trabalho. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#onworkflow_runbranchesbranches-ignore). Por exemplo, um fluxo de trabalho com o gatilho a seguir só será executado quando o fluxo de trabalho chamado `Build` for executado em um branch chamado `canary`.

```yaml
on:
  workflow_run:
    workflows: [Build]
    types: [requested]
    branches: [canary]
```

### Usando dados do fluxo de trabalho acionador { #using-data-from-the-triggering-workflow }

Você pode acessar a payload do evento [`workflow_run` que](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_run) corresponde ao fluxo de trabalho que disparou seu fluxo de trabalho. Por exemplo, se o fluxo de trabalho de disparo gerar artefatos, um fluxo de trabalho disparado com o evento `workflow_run` poderá acessar esses artefatos.

O seguinte fluxo de trabalho faz o upload de dados como um artefato. (Neste exemplo simplificado, os dados são o número da pull request.)

```yaml
name: Upload data

on:
  pull_request:

jobs:
  upload:
    runs-on: ubuntu-latest

    steps:
      - name: Save PR number
        env:
          PR_NUMBER: ${{ github.event.number }}
        run: |
          mkdir -p ./pr
          echo $PR_NUMBER > ./pr/pr_number
      - uses: actions/upload-artifact@v4
        with:
          name: pr_number
          path: pr/
```

Quando uma execução do fluxo de trabalho acima é concluída, ela aciona a execução de um fluxo de trabalho seguinte. O fluxo de trabalho a seguir usa o contexto `github.event.workflow_run` e a ação actions/download-artifact\@v5 para baixar o artefato que foi carregado pelo fluxo de trabalho acima e, em seguida, comenta sobre a solicitação de pull cujo número foi carregado como um artefato.

```yaml
name: Use the data

on:
  workflow_run:
    workflows: [Upload data]
    types:
      - completed

jobs:
  download:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      issues: write
    steps:
      - name: 'Download artifact'
        uses: actions/download-artifact@v5
        with:
          name: pr_number
          # do not extract in the workspace dir that may contain executable scripts
          path: ${{ runner.temp }}/artifacts
          run-id: ${{ github.event.workflow_run.id }}
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: 'Comment on PR'
        uses: actions/github-script@v8
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const fs = require('fs');
            const path = require('path');
            const temp = '${{ runner.temp }}/artifacts';
            const issue_number_raw = fs.readFileSync(path.join(temp, 'pr_number'), 'utf8').trim();
            const issue_number = Number(issue_number_raw);
            if (!Number.isInteger(issue_number)) {
              throw new Error(`Invalid PR number in pr_number artifact: "${issue_number_raw}"`);
            }
            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue_number,
              body: 'Thank you for the PR!'
            });
```
