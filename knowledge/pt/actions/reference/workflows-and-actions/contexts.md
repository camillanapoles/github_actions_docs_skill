---
title: Referência de contextos
description: Encontre informações sobre contextos disponíveis em GitHub Actions fluxos de trabalho, incluindo propriedades disponíveis, métodos de acesso e exemplos de uso.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/contexts
captured: '2026-10-19'
section: Reference / Workflows and actions
---

# Referência de contextos

_Encontre informações sobre contextos disponíveis em GitHub Actions fluxos de trabalho, incluindo propriedades disponíveis, métodos de acesso e exemplos de uso._

## Contextos disponíveis

| Nome do contexto | Tipo | Descrição |
| --- | --- | --- |
| `github` | `object` | Informações sobre a execução do fluxo de trabalho. Para obter mais informações, confira [Contexto `github`](#github-context). |
| `env` | `object` | Contém variáveis definidas em um fluxo de trabalho, um trabalho ou uma etapa. Para obter mais informações, confira [Contexto `env`](#env-context). |
| `vars` | `object` | Contém variáveis definidas nos níveis de repositório, organização ou ambiente. Para obter mais informações, confira [Contexto `vars`](#vars-context). |
| `job` | `object` | Informações sobre o trabalho atualmente em execução. Para obter mais informações, confira [Contexto `job`](#job-context). |
| `jobs` | `object` | Somente para fluxos de trabalho reutilizáveis, contém saídas de trabalhos do fluxo de trabalho reutilizável. Para obter mais informações, confira [Contexto `jobs`](#jobs-context). |
| `steps` | `object` | Informações sobre as etapas que foram executadas no trabalho atual. Para obter mais informações, confira [Contexto `steps`](#steps-context). |
| `runner` | `object` | Informações sobre o executor do trabalho atual. Para obter mais informações, confira [Contexto `runner`](#runner-context). |
| `secrets` | `object` | Contém os nomes e valores de segredos que estão disponíveis para uma execução de fluxo de trabalho. Para obter mais informações, confira [Contexto `secrets`](#secrets-context). |
| `strategy` | `object` | Informações sobre a estratégia de execução da matriz para o trabalho atual. Para obter mais informações, confira [Contexto `strategy`](#strategy-context). |
| `matrix` | `object` | Contém as propriedades da matriz definidas no fluxo de trabalho que se aplicam ao trabalho atual. Para obter mais informações, confira [Contexto `matrix`](#matrix-context). |
| `needs` | `object` | Contém as saídas de todos os trabalhos que são definidos como uma dependência do trabalho atual. Para obter mais informações, confira [Contexto `needs`](#needs-context). |
| `inputs` | `object` | Contém as entradas de um fluxo de trabalho reutilizável ou disparado manualmente. Para obter mais informações, confira [Contexto `inputs`](#inputs-context). |

Como parte de uma expressão, você pode acessar informações de contexto usando uma das duas sintaxes.

* Sintaxe de índice: `github['sha']`
* Sintaxe de desreferência de propriedade: `github.sha`

Para usar a sintaxe de desreferência de propriedade, o nome da propriedade deve começar com uma letra `_` ou e conter apenas caracteres alfanuméricos, `-` ou `_`.

Se você tentar desreferenciar uma propriedade inexistente, ela será avaliada como uma cadeia de caracteres vazia.

### Determinar quando usar contextos

GitHub Actions inclui uma coleção de variáveis chamadas *contextos* e uma coleção semelhante de variáveis chamadas *variáveis padrão*. Estas variáveis são destinadas a serem usadas em diferentes pontos do fluxo de trabalho:

* **Variáveis de ambiente padrão:** essas variáveis de ambiente existem apenas no executor que está executando seu trabalho. Para saber mais, confira [Referência de variáveis](variables.md).
* **Contextos:** você pode usar a maioria dos contextos em qualquer ponto do fluxo de trabalho, inclusive quando as *variáveis padrão* não estão disponíveis. Por exemplo, você pode usar contextos com expressões para executar o processamento inicial antes que o trabalho seja encaminhado para um executor para execução. Isso permite que você use um contexto com a palavra-chave `if` condicional para determinar se uma etapa deve ser executada. Depois que o trabalho estiver em execução, você também poderá recuperar variáveis de contexto do executor que está executando o trabalho, como `runner.os`. Para ver detalhes do local em que você pode usar vários contextos em um fluxo de trabalho, confira [Disponibilidade de contexto](#context-availability).

O seguinte exemplo demonstra como esses diferentes tipos de variáveis podem ser usados juntos em um trabalho:

```yaml copy
name: CI
on: push
jobs:
  prod-check:
    if: ${{ github.ref == 'refs/heads/main' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production server on branch $GITHUB_REF"
```

Neste exemplo, a instrução `if` verifica o contexto [`github.ref`](contexts.md#github-context) para determinar o nome do branch atual. Se o nome for `refs/heads/main`, as etapas seguintes serão executadas. A `if` verificação é processada por GitHub Actions, e o trabalho só é enviado para o executor se o resultado for `true`. Depois que o trabalho é enviado para o executor, a etapa é executada e refere-se à variável [`$GITHUB_REF`](variables.md) do executor.

### Disponibilidade do contexto

Contextos diferentes estão disponíveis durante a execução de um fluxo de trabalho. Por exemplo, o contexto `secrets` só pode ser usado em alguns lugares de um trabalho.

Além disso, algumas funções só podem ser utilizadas em determinados lugares. Por exemplo, a função `hashFiles` não está disponível em todos os lugares.

A tabela a seguir lista as restrições nas quais cada contexto e função especial podem ser utilizados em um fluxo de trabalho. Os contextos listados estão disponíveis apenas para a chave de fluxo de trabalho fornecida e não podem ser usados em nenhum outro lugar. A menos que esteja listado abaixo, uma função pode ser usada em qualquer lugar.

| Chave de fluxo de trabalho | Contexto | Funções especiais |
| --- | --- | --- |
| `run-name` | `github, inputs, vars` | Nenhum |
| `concurrency` | `github, inputs, vars` | Nenhum |
| `env` | `github, secrets, inputs, vars` | Nenhum |
| `jobs.<job_id>.concurrency` | `github, needs, strategy, matrix, inputs, vars` | Nenhum |
| `jobs.<job_id>.container` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.container.credentials` | `github, needs, strategy, matrix, env, vars, secrets, inputs` | Nenhum |
| `jobs.<job_id>.container.env.<env_id>` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, inputs` | Nenhum |
| `jobs.<job_id>.container.image` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.continue-on-error` | `github, needs, strategy, vars, matrix, inputs` | Nenhum |
| `jobs.<job_id>.defaults.run` | `github, needs, strategy, matrix, env, vars, inputs` | Nenhum |
| `jobs.<job_id>.env` | `github, needs, strategy, matrix, vars, secrets, inputs` | Nenhum |
| `jobs.<job_id>.environment` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.environment.url` | `github, needs, strategy, matrix, job, runner, env, vars, steps, inputs` | Nenhum |
| `jobs.<job_id>.if` | `github, needs, vars, inputs` | `always, cancelled, success, failure` |
| `jobs.<job_id>.name` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.outputs.<output_id>` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | Nenhum |
| `jobs.<job_id>.runs-on` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.secrets.<secrets_id>` | `github, needs, strategy, matrix, secrets, inputs, vars` | Nenhum |
| `jobs.<job_id>.services` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.services.<service_id>.credentials` | `github, needs, strategy, matrix, env, vars, secrets, inputs` | Nenhum |
| `jobs.<job_id>.services.<service_id>.env.<env_id>` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, inputs` | Nenhum |
| `jobs.<job_id>.steps.continue-on-error` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.env` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.if` | `github, needs, strategy, matrix, job, runner, env, vars, steps, inputs` | `always, cancelled, success, failure, hashFiles` |
| `jobs.<job_id>.steps.name` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.run` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.timeout-minutes` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.with` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.steps.working-directory` | `github, needs, strategy, matrix, job, runner, env, vars, secrets, steps, inputs` | `hashFiles` |
| `jobs.<job_id>.strategy` | `github, needs, vars, inputs` | Nenhum |
| `jobs.<job_id>.timeout-minutes` | `github, needs, strategy, matrix, vars, inputs` | Nenhum |
| `jobs.<job_id>.with.<with_id>` | `github, needs, strategy, matrix, inputs, vars` | Nenhum |
| `on.workflow_call.inputs.<inputs_id>.default` | `github, inputs, vars` | Nenhum |
| `on.workflow_call.outputs.<output_id>.value` | `github, jobs, vars, inputs` | Nenhum |

### Exemplo: imprimir informações de contexto no registro

Você pode imprimir o conteúdo de contextos no registro para depuração. A função [`toJSON`](expressions.md#tojson) é necessária para imprimir objetos JSON no log.

!!! warning
    Ao usar todo o contexto `github`, lembre-se de que ele inclui informações confidenciais, como `github.token`. GitHub oculta segredos quando eles são impressos no console, mas você deve ter cuidado ao exportar ou imprimir o contexto.

```yaml copy
name: Context testing
on: push

jobs:
  dump_contexts_to_log:
    runs-on: ubuntu-latest
    steps:
      - name: Dump GitHub context
        env:
          GITHUB_CONTEXT: ${{ toJson(github) }}
        run: echo "$GITHUB_CONTEXT"
      - name: Dump job context
        env:
          JOB_CONTEXT: ${{ toJson(job) }}
        run: echo "$JOB_CONTEXT"
      - name: Dump steps context
        env:
          STEPS_CONTEXT: ${{ toJson(steps) }}
        run: echo "$STEPS_CONTEXT"
      - name: Dump runner context
        env:
          RUNNER_CONTEXT: ${{ toJson(runner) }}
        run: echo "$RUNNER_CONTEXT"
      - name: Dump strategy context
        env:
          STRATEGY_CONTEXT: ${{ toJson(strategy) }}
        run: echo "$STRATEGY_CONTEXT"
      - name: Dump matrix context
        env:
          MATRIX_CONTEXT: ${{ toJson(matrix) }}
        run: echo "$MATRIX_CONTEXT"
```

## Contexto `github`

O contexto `github` contém informações sobre a execução do fluxo de trabalho e sobre o evento que a disparou. Você pode ler a maior parte dos dados de contexto `github` em variáveis de ambiente. Para saber mais sobre variáveis de ambiente, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

!!! warning
    Ao usar todo o contexto `github`, lembre-se de que ele inclui informações confidenciais, como `github.token`. GitHub oculta segredos quando eles são impressos no console, mas você deve ter cuidado ao exportar ou imprimir o contexto.
    [!WARNING]
    Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `github` | `object` | Contexto de nível mais alto disponível em qualquer trabalho ou etapa de um fluxo de trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `github.action` | `string` | O nome da ação atualmente em execução ou a [`id`](workflow-syntax.md#jobsjob_idstepsid) de uma etapa. |
| GitHub remove caracteres especiais e usa o nome `__run` quando a etapa atual executa um script sem um `id`. Se você usar a mesma ação mais de uma vez no mesmo trabalho, o nome incluirá um sufixo com o número da sequência com o sublinhado antes dele. Por exemplo, o primeiro script que você executar terá o nome `__run`, e o segundo script será chamado `__run_2`. Da mesma forma, a segunda invocação de `actions/checkout` será `actionscheckout2`. |  |  |
| `github.action_path` | `string` | O caminho onde uma ação está localizada. Esta propriedade só é compatível com ações compostas. Você pode usar esse caminho para acessar arquivos localizados no mesmo repositório da ação, por exemplo, alterando diretórios para o caminho (usando a variável de ambiente correspondente): `cd "$GITHUB_ACTION_PATH"`. Para obter mais informações sobre variáveis de ambiente, consulte [Referência de uso seguro](../security/secure-use.md#use-an-intermediate-environment-variable). |
| `github.action_ref` | `string` | Para uma etapa executando uma ação, este é o ref da ação que está sendo executada. Por exemplo, `v2`.<br><br>Não use na palavra-chave `run`. Para que esse contexto funcione com ações compostas, referencie-o no contexto `env` da ação composta. |
| `github.action_repository` | `string` | Para uma etapa que executa uma ação, este é o nome do proprietário e do repositório da ação. Por exemplo, `actions/checkout`.<br><br>Não use na palavra-chave `run`. Para que esse contexto funcione com ações compostas, referencie-o no contexto `env` da ação composta. |
| `github.action_status` | `string` | Para uma ação composta, o resultado atual da ação composta. |
| `github.actor` | `string` | O nome de usuário de quem acionou a execução do fluxo de trabalho inicial. Se a execução do fluxo de trabalho for executada novamente, esse valor poderá ser diferente de `github.triggering_actor`. Qualquer nova execução de fluxo de trabalho usará os privilégios de `github.actor`, mesmo que o ator que inicie a nova execução (`github.triggering_actor`) tenha privilégios diferentes. |
| `github.actor_id` | `string` | A ID da conta da pessoa ou do aplicativo que disparou a execução inicial do fluxo de trabalho. Por exemplo, `1234567`. Observe que isso é diferente do nome de usuário do ator. |
| `github.api_url` | `string` | O URL da API REST GitHub. |
| `github.artifacts` | `string` | Caminho no runner para o arquivo que identifica os artefatos do workflow da etapa atual. Escreva uma declaração por linha para identificar arquivos ou referências de resumo OCI como artefatos de fluxo de trabalho. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#declaring-workflow-artifacts). |
| `github.artifacts_list` | `string` | Caminho no runner para um arquivo somente para leitura que contém, em JSON, os metadados agregados dos artefatos do fluxo de trabalho do trabalho atual. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#reading-workflow-artifacts). |
| `github.base_ref` | `string` | A `base_ref` ou o branch de destino da solicitação de pull em uma execução de fluxo de trabalho. Essa propriedade só fica disponível quando o evento que dispara a execução de fluxo de trabalho é `pull_request` ou `pull_request_target`. |
| `github.env` | `string` | Caminho no executor para o arquivo que define variáveis de ambiente dos comandos do fluxo de trabalho. Este arquivo é único para a etapa atual e é um arquivo diferente para cada etapa de um trabalho. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#setting-an-environment-variable). |
| `github.event` | `object` | Carga de evento de webhook completa. Você pode acessar as propriedades individuais do evento usando este contexto. Este objeto é idêntico à carga do webhook do evento que acionou a execução do fluxo de trabalho e é diferente para cada evento. Os webhooks para cada evento GitHub Actions são vinculados em [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md#workflow_call). Por exemplo, para uma execução de fluxo de trabalho disparada pelo [`push` evento](events-that-trigger-workflows.md#push), esse objeto contém o conteúdo do [payload do webhook por push](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#push). |
| `github.event_name` | `string` | Nome do evento que acionou a execução do fluxo de trabalho. |
| `github.event_path` | `string` | O caminho para o arquivo no executor que contém a carga completa do webhook do evento. |
| `github.graphql_url` | `string` | A URL da API do GitHub GraphQL. |
| `github.head_ref` | `string` | A `head_ref` ou o branch de origem da solicitação de pull em uma execução de fluxo de trabalho. Essa propriedade só fica disponível quando o evento que dispara a execução de fluxo de trabalho é `pull_request` ou `pull_request_target`. |
| `github.job` | `string` | A [`job_id`](workflow-syntax.md#jobsjob_id) do trabalho atual. <br> Observação: essa propriedade de contexto é definida pelo executor de Ações e só está disponível na execução `steps` de um trabalho. Caso contrário, o valor dessa propriedade será `null`. |
| `github.path` | `string` | O caminho no executor para o arquivo que define as variáveis do sistema `PATH` por meio dos comandos do fluxo de trabalho. Este arquivo é único para a etapa atual e é um arquivo diferente para cada etapa de um trabalho. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#adding-a-system-path). |
| `github.ref` | `string` | A referência completa do branch ou tag que acionou o fluxo de trabalho. Para fluxos de trabalho disparados por `push`, esse é o branch ou a ref da tag que foi enviada. Para fluxos de trabalho disparados por `pull_request` que não foram mesclados, este é o branch de mesclagem do pull request. Se a solicitação de pull foi mesclada, essa é a ramificação na qual ela foi mesclada. Para fluxos de trabalho disparados por `release`, essa é a tag de versão criada. Para outros gatilhos, esse é o branch ou a ref de tag que disparou a execução do fluxo de trabalho. Essa variável só é definida quando há um branch ou uma tag disponível para o tipo de evento. A ref fornecida tem o formato completo, o que significa que, para branches, o formato é `refs/heads/<branch_name>`. Para eventos de solicitação de pull, exceto `pull_request_target` que não foram mesclados, é `refs/pull/<pr_number>/merge`. Eventos `pull_request_target` têm o `ref` do ramo base. Para as etiquetas, é `refs/tags/<tag_name>`. Por exemplo, `refs/heads/feature-branch-1`. Para obter mais informações sobre branches de mesclagem de solicitação de pull, consulte [Solicitações de pull](https://docs.github.com/pt/pull-requests/reference/pull-requests#pull-request-refs-and-merge-branches). |
| `github.ref_name` | `string` | O nome de ref curto do branch ou tag que acionou a execução do fluxo de trabalho. Esse valor corresponde ao nome do branch ou tag mostrado em GitHub. Por exemplo, `feature-branch-1`.<br><br>Para solicitações de pull que não foram mescladas, o formato é `<pr_number>/merge`. |
| `github.ref_protected` | `boolean` | `true` se proteções de ramificação ou [conjuntos de regras](https://docs.github.com/pt/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository) estiverem configurados para a referência que disparou a execução do fluxo de trabalho. |
| `github.ref_type` | `string` | O tipo de ref que acionou a execução do fluxo de trabalho. Os valores válidos são `branch` ou `tag`. |
| `github.repository` | `string` | Nome do repositório e o proprietário. Por exemplo, `octocat/Hello-World`. |
| `github.repository_id` | `string` | A ID do repositório. Por exemplo, `123456789`. Observe que isso é diferente do nome do repositório. |
| `github.repository_owner` | `string` | O nome de usuário do proprietário do repositório. Por exemplo, `octocat`. |
| `github.repository_owner_id` | `string` | A ID da conta do proprietário do repositório. Por exemplo, `1234567`. Observe que isso é diferente do nome do proprietário. |
| `github.repositoryUrl` | `string` | A URL do repositório Git. Por exemplo, `git://github.com/octocat/hello-world.git`. |
| `github.retention_days` | `string` | O número de dias em que os logs e os artefatos da execução de fluxo de trabalho são mantidos. |
| `github.run_id` | `string` | Um número exclusivo para cada fluxo de trabalho executado em um repositório. Este número não muda se você executar novamente o fluxo de trabalho. |
| `github.run_number` | `string` | Um número exclusivo para cada execução de um fluxo de trabalho específico em um repositório. Esse número começa em 1 para a primeira execução do fluxo de trabalho e é incrementado a cada nova operação. Este número não muda se você executar novamente o fluxo de trabalho. |
| `github.run_attempt` | `string` | Um número exclusivo para cada tentativa de execução de um fluxo de trabalho específico em um repositório. Este número começa em 1 para a primeira tentativa de execução do fluxo de trabalho e aumenta a cada nova execução. |
| `github.secret_source` | `string` | A origem de um segredo usado em um fluxo de trabalho. Os valores possíveis são`None`, , `Actions`ou `Codespaces``Dependabot`. |
| `github.server_url` | `string` | A URL do servidor do GitHub. Por exemplo: `https://github.com`. |
| `github.sha` | `string` | O commit SHA que acionou o fluxo de trabalho. O valor do commit deste SHA depende do evento que acionou o fluxo de trabalho. Para saber mais, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md). Por exemplo, `ffac537e6cbbf934b08745a378932722df287a53`. |
| `github.token` | `string` | Um token para autenticação em nome do aplicativo do GitHub instalado no seu repositório. Isso é funcionalmente equivalente ao segredo `GITHUB_TOKEN`. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).  <br> Observação: essa propriedade de contexto é definida pelo executor de Ações e só está disponível na execução `steps` de um trabalho. Caso contrário, o valor dessa propriedade será `null`. |
| `github.triggering_actor` | `string` | O nome de usuário de quem iniciou a execução do fluxo de trabalho. Se a execução do fluxo de trabalho for executada novamente, esse valor poderá ser diferente de `github.actor`. Qualquer nova execução de fluxo de trabalho usará os privilégios de `github.actor`, mesmo que o ator que inicie a nova execução (`github.triggering_actor`) tenha privilégios diferentes. |
| `github.workflow` | `string` | Nome do fluxo de trabalho. Se o arquivo de fluxo de trabalho não especificar um `name`, o valor dessa propriedade será o caminho completo do arquivo de fluxo de trabalho no repositório. |
| `github.workflow_ref` | `string` | O caminho de referência para o fluxo de trabalho. Por exemplo, `octocat/hello-world/.github/workflows/my-workflow.yml@refs/heads/my_branch`. |
| `github.workflow_sha` | `string` | O SHA de commit para o arquivo de fluxo de trabalho. |
| `github.workspace` | `string` | O diretório de trabalho padrão no executor para as etapas, e a localização padrão do repositório quando a ação [`checkout`](https://github.com/actions/checkout) é usada. |

### Exemplo de conteúdo do contexto `github`

O contexto a seguir foi obtido de uma execução de fluxo de trabalho disparada pelo evento `push`. O objeto `event` deste exemplo foi truncado porque é idêntico ao conteúdo do payload do webhook [`push`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#push).

!!! note
    Esse contexto é apenas um exemplo. O conteúdo de um contexto depende do fluxo de trabalho que você está executando. Os contextos, objetos e propriedades variarão significativamente em diferentes condições de execução do fluxo de trabalho.

```json
{
  "token": "***",
  "job": "dump_contexts_to_log",
  "ref": "refs/heads/my_branch",
  "sha": "c27d339ee6075c1f744c5d4b200f7901aad2c369",
  "repository": "octocat/hello-world",
  "repository_owner": "octocat",
  "repositoryUrl": "git://github.com/octocat/hello-world.git",
  "run_id": "1536140711",
  "run_number": "314",
  "retention_days": "90",
  "run_attempt": "1",
  "actor": "octocat",
  "workflow": "Context testing",
  "head_ref": "",
  "base_ref": "",
  "event_name": "push",
  "event": {
    ...
  },
  "server_url": "https://github.com",
  "api_url": "https://api.github.com",
  "graphql_url": "https://api.github.com/graphql",
  "ref_name": "my_branch",
  "ref_protected": false,
  "ref_type": "branch",
  "secret_source": "Actions",
  "workspace": "/home/runner/work/hello-world/hello-world",
  "action": "github_step",
  "event_path": "/home/runner/work/_temp/_github_workflow/event.json",
  "action_repository": "",
  "action_ref": "",
  "path": "/home/runner/work/_temp/_runner_file_commands/add_path_b037e7b5-1c88-48e2-bf78-eaaab5e02602",
  "env": "/home/runner/work/_temp/_runner_file_commands/set_env_b037e7b5-1c88-48e2-bf78-eaaab5e02602"
}
```

### Exemplo de uso do contexto `github`

Este exemplo de fluxo de trabalho usa o contexto `github.event_name` para executar um trabalho somente se a execução de fluxo de trabalho foi disparada pelo evento `pull_request`.

```yaml copy
name: Run CI
on: [push, pull_request]

jobs:
  normal_ci:
    runs-on: ubuntu-latest
    steps:
      - name: Run normal CI
        run: echo "Running normal CI"

  pull_request_ci:
    runs-on: ubuntu-latest
    if: ${{ github.event_name == 'pull_request' }}
    steps:
      - name: Run PR CI
        run: echo "Running PR only CI"
```

## Contexto `env`

O contexto `env` contém variáveis que foram definidas em um fluxo de trabalho, um trabalho ou uma etapa. Ele não contém variáveis herdadas pelo processo do executor. Para saber mais sobre como definir variáveis em seu fluxo de trabalho, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#env).

Você pode recuperar os valores das variáveis armazenadas no contexto `env` e usá-los no arquivo do fluxo de trabalho. O contexto `env` pode ser usado em qualquer chave em uma etapa do fluxo de trabalho, exceto nas chaves `id` e `uses`. Para saber mais sobre a sintaxe da etapa, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idsteps).

Se você deseja utilizar o valor de uma variável dentro de um executor, use o método normal do sistema operacional do executor para ler as variáveis de ambiente.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `env` | `object` | Esse contexto altera cada etapa em um trabalho. Você pode acessar esse contexto em qualquer etapa de um trabalho. Este objeto contém as propriedades listadas abaixo. |
| `env.<env_name>` | `string` | O valor de uma variável de ambiente específica. |

### Exemplo de conteúdo do contexto `env`

O conteúdo do contexto `env` é um mapeamento de nomes de variáveis para os respectivos valores. O conteúdo do contexto pode mudar dependendo de onde é usado na execução do fluxo de trabalho. Neste exemplo, o `env` contexto contém duas variáveis.

```json
{
  "first_name": "Mona",
  "super_duper_var": "totally_awesome"
}
```

### Exemplo de uso do contexto `env`

Este exemplo de fluxo de trabalho mostra variáveis sendo definidas no contexto `env` nos níveis de fluxo de trabalho, trabalho e etapa. Em seguida, a sintaxe `${{ env.VARIABLE-NAME }}` é usada para recuperar valores de variáveis em etapas individuais no fluxo de trabalho.

Quando mais de uma variável de ambiente é definida com o mesmo nome, GitHub usa a variável mais específica. Por exemplo, uma variável de ambiente definida em uma etapa substituirá as variáveis de ambiente do trabalho e do fluxo de trabalho que tenham o mesmo nome enquanto a etapa é executada. Uma variável de ambiente definida para um trabalho substituirá uma variável de fluxo de trabalho com o mesmo nome enquanto o trabalho é executado.

```yaml copy
name: Hi Mascot
on: push
env:
  mascot: Mona
  super_duper_var: totally_awesome

jobs:
  windows_job:
    runs-on: windows-latest
    steps:
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Mona
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Octocat
        env:
          mascot: Octocat
  linux_job:
    runs-on: ubuntu-latest
    env:
      mascot: Tux
    steps:
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Tux
```

## Contexto `vars`

O contexto `vars` contém variáveis de configuração personalizadas definidas nos níveis da organização, do repositório e do ambiente. Para saber mais sobre como definir variáveis de configuração para uso em vários fluxos de trabalho, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-configuration-variables-for-multiple-workflows).

### Exemplo de conteúdo do contexto `vars`

O conteúdo do contexto `vars` é um mapeamento de nomes de variáveis de configuração para os respectivos valores.

```json
{
  "mascot": "Mona"
}
```

### Exemplo de uso do contexto `vars`

Este exemplo de fluxo de trabalho mostra como as variáveis de configuração definidas nos níveis de repositório, ambiente ou organização estão automaticamente disponíveis usando o contexto `vars`.

!!! note
    As variáveis de configuração no ambiente ficam automaticamente disponíveis depois que o ambiente é declarado pelo executor.

Se uma variável de configuração não tiver sido definida, o valor retornado de um contexto referenciando a variável será uma cadeia de caracteres vazia.

O exemplo a seguir mostra o uso de variáveis de configuração com o contexto `vars` em um fluxo de trabalho. Cada uma das variáveis de configuração a seguir foram definidas no nível do repositório, da organização ou do ambiente.

```yaml copy
on:
  workflow_dispatch:
env:
  # Setting an environment variable with the value of a configuration variable
  env_var: ${{ vars.ENV_CONTEXT_VAR }}

jobs:
  display-variables:
    name: ${{ vars.JOB_NAME }}
    # You can use configuration variables with the `vars` context for dynamic jobs
    if: ${{ vars.USE_VARIABLES == 'true' }}
    runs-on: ${{ vars.RUNNER }}
    environment: ${{ vars.ENVIRONMENT_STAGE }}
    steps:
    - name: Use variables
      run: |
        echo "repository variable : $REPOSITORY_VAR"
        echo "organization variable : $ORGANIZATION_VAR"
        echo "overridden variable : $OVERRIDE_VAR"
        echo "variable from shell environment : $env_var"
      env:
        REPOSITORY_VAR: ${{ vars.REPOSITORY_VAR }}
        ORGANIZATION_VAR: ${{ vars.ORGANIZATION_VAR }}
        OVERRIDE_VAR: ${{ vars.OVERRIDE_VAR }}

    - name: ${{ vars.HELLO_WORLD_STEP }}
      if: ${{ vars.HELLO_WORLD_ENABLED == 'true' }}
      uses: actions/hello-world-javascript-action@main
      with:
        who-to-greet: ${{ vars.GREET_NAME }}
```

## Contexto `job`

O contexto `job` contém informações sobre o trabalho atualmente em execução.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `job` | `object` | O contexto muda para cada trabalho durante a execução de um fluxo de trabalho. Você pode acessar esse contexto em qualquer etapa de um trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `job.check_run_id` | `number` | A ID de verificação de execução do trabalho atual. |
| `job.container` | `object` | Informações sobre o contêiner do trabalho. Para saber mais sobre contêineres, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idcontainer). |
| `job.container.id` | `string` | O ID do contêiner. |
| `job.container.network` | `string` | O identificador da rede do contêiner. O executor cria a rede usada por todos os contêineres em um trabalho. |
| `job.services` | `object` | Contêineres de serviços criados para um trabalho. Para saber mais sobre contêineres de serviço, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idservices). |
| `job.services.<service_id>.id` | `string` | O ID do contêiner de serviço. |
| `job.services.<service_id>.network` | `string` | O ID da rede de contêiner de serviço. O executor cria a rede usada por todos os contêineres em um trabalho. |
| `job.services.<service_id>.ports` | `object` | As portas expostas do contêiner de serviço. |
| `job.status` | `string` | O estado atual do trabalho. Os valores possíveis são `success`, `failure`, ou `cancelled`. |
| `job.workflow_ref` | `string` | O ref completo do arquivo de fluxo de trabalho que define o trabalho atual. Por exemplo, `octo-org/octo-repo/.github/workflows/deploy.yml@refs/heads/main`. Para trabalhos definidos diretamente em um arquivo de fluxo de trabalho, isso é o mesmo que `github.workflow_ref`. Para trabalhos definidos em um [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md), isso se refere ao arquivo de fluxo de trabalho reutilizável. (não disponível em GitHub Enterprise Server) |
| `job.workflow_sha` | `string` | O SHA da versão do arquivo de fluxo de trabalho que define o trabalho atual. (não disponível em GitHub Enterprise Server) |
| `job.workflow_repository` | `string` | O `owner/repo` do repositório que contém o arquivo de fluxo de trabalho que define a tarefa atual. Por exemplo, `octo-org/octo-repo`. (não disponível em GitHub Enterprise Server) |
| `job.workflow_file_path` | `string` | O caminho do arquivo de fluxo de trabalho que define o trabalho atual, em relação à raiz do repositório. Por exemplo, `.github/workflows/deploy.yml`. (não disponível em GitHub Enterprise Server) |

### Exemplo de conteúdo do contexto `job`

Este exemplo de contexto `job` usa um contêiner de serviço do PostgreSQL com as portas mapeadas. Se não houver contêineres ou contêineres de serviço usados em um trabalho, o contexto `job` conterá apenas `status`. As propriedades de identidade `check_run_id` e de fluxo de trabalho (`workflow_ref`, `workflow_sha`, `workflow_repository`, `workflow_file_path`) não estão disponíveis em GitHub Enterprise Server.

```json
{
  "status": "success",
  "check_run_id": 51725241954,
  "workflow_ref": "octo-org/octo-repo/.github/workflows/deploy.yml@refs/heads/main",
  "workflow_sha": "abc123def456789abc123def456789abc123def4",
  "workflow_repository": "octo-org/octo-repo",
  "workflow_file_path": ".github/workflows/deploy.yml",
  "container": {
    "network": "github_network_53269bd575974817b43f4733536b200c"
  },
  "services": {
    "postgres": {
      "id": "60972d9aa486605e66b0dad4abb638dc3d9116f566579e418166eedb8abb9105",
      "ports": {
        "5432": "49153"
      },
      "network": "github_network_53269bd575974817b43f4733536b200c"
    }
  }
}
```

### Exemplo de uso do contexto `job`

Este exemplo de fluxo de trabalho configura um contêiner de serviço do PostgreSQL e mapeia automaticamente a porta 5432 do recipiente de serviço com uma porta disponível escolhida aleatoriamente no host. O contexto `job` é usado para acessar o número da porta atribuída no host.

```yaml copy
name: PostgreSQL Service Example
on: push
jobs:
  postgres-job:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres
        env:
          POSTGRES_PASSWORD: postgres
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
        ports:
          # Maps TCP port 5432 in the service container to a randomly chosen available port on the host.
          - 5432

    steps:
      - run: pg_isready -h localhost -p ${{ job.services.postgres.ports[5432] }}
      - run: echo "Run tests against Postgres"
```

### Exemplo de uso da identidade de fluxo de trabalho no contexto de `job`

!!! note
    As `job.workflow_*` propriedades de contexto não estão disponíveis em GitHub Enterprise Server.

Este exemplo de fluxo de trabalho reutilizável usa `job.workflow_repository` e `job.workflow_sha` para verificar seu próprio código-fonte, em vez do repositório do chamador. Isso é útil quando um fluxo de trabalho reutilizável precisa acessar arquivos co-localizados com a definição de fluxo de trabalho.

```yaml copy
```
# In a reusable workflow (e.g., octo-org/shared-workflows/.github/workflows/deploy.yml)
name: Reusable deploy workflow
on:
  workflow_call:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          repository: ${{ job.workflow_repository }}
          ref: ${{ job.workflow_sha }}

      - run: echo "Deploying from ${{ job.workflow_ref }}"
      - run: echo "Workflow file path is ${{ job.workflow_file_path }}"
```

```
## Contexto `jobs`

O contexto `jobs` só está disponível em fluxos de trabalho reutilizáveis e só pode ser usado para definir as saídas de um fluxo de trabalho reutilizável. Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#using-outputs-from-a-reusable-workflow).

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `jobs` | `object` | Isso só está disponível em fluxos de trabalho reutilizáveis e só pode ser usado para definir as saídas de um fluxo de trabalho reutilizável. Este objeto contém todas as propriedades listadas abaixo. |
| `jobs.<job_id>.result` | `string` | O resultado de um trabalho no fluxo de trabalho reutilizável. Os valores possíveis são `success`, `failure`, `cancelled` ou `skipped`. |
| `jobs.<job_id>.outputs` | `object` | O conjunto de saídas de um trabalho em um fluxo de trabalho reutilizável. |
| `jobs.<job_id>.outputs.<output_name>` | `string` | O valor de uma saída específica para um trabalho em um fluxo de trabalho reutilizável. |

### Exemplo de conteúdo do contexto `jobs`

O contexto deste exemplo `jobs` contém o resultado e as saídas de um trabalho derivado de uma execução de fluxo de trabalho reutilizável.

```json
{
  "example_job": {
    "result": "success",
    "outputs": {
      "output1": "hello",
      "output2": "world"
    }
  }
}
```

### Exemplo de uso do contexto `jobs`

Este exemplo de fluxo de trabalho reutilizável usa o contexto `jobs` para definir saídas para o fluxo de trabalho reutilizável. Observe como as saídas fluem das etapas para o trabalho e, em seguida, para o gatilho `workflow_call`. Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#using-outputs-from-a-reusable-workflow).

```yaml copy
name: Reusable workflow

on:
  workflow_call:
    # Map the workflow outputs to job outputs
    outputs:
      firstword:
        description: "The first output string"
        value: ${{ jobs.example_job.outputs.output1 }}
      secondword:
        description: "The second output string"
        value: ${{ jobs.example_job.outputs.output2 }}

jobs:
  example_job:
    name: Generate output
    runs-on: ubuntu-latest
    # Map the job outputs to step outputs
    outputs:
      output1: ${{ steps.step1.outputs.firstword }}
      output2: ${{ steps.step2.outputs.secondword }}
    steps:
      - id: step1
        run: echo "firstword=hello" >> $GITHUB_OUTPUT
      - id: step2
        run: echo "secondword=world" >> $GITHUB_OUTPUT
```

## Contexto `steps`

O contexto `steps` contém informações sobre as etapas do trabalho atual que têm uma [`id`](workflow-syntax.md#jobsjob_idstepsid) especificada e que já foram executadas.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `steps` | `object` | Esse contexto altera cada etapa em um trabalho. Você pode acessar esse contexto em qualquer etapa de um trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `steps.<step_id>.outputs` | `object` | Conjunto de saídas definidas para esta etapa. Para saber mais, confira [Referência de sintaxe de metadados](metadata-syntax.md#outputs-for-docker-container-and-javascript-actions). |
| `steps.<step_id>.conclusion` | `string` | O resultado de uma etapa concluída após a aplicação de [`continue-on-error`](workflow-syntax.md#jobsjob_idstepscontinue-on-error). Os valores possíveis são `success`, `failure`, `cancelled` ou `skipped`. Quando uma etapa `continue-on-error` falha, o `outcome` é `failure`, mas a `conclusion` final é `success`. |
| `steps.<step_id>.outcome` | `string` | O resultado de uma etapa concluída antes da aplicação de [`continue-on-error`](workflow-syntax.md#jobsjob_idstepscontinue-on-error). Os valores possíveis são `success`, `failure`, `cancelled` ou `skipped`. Quando uma etapa `continue-on-error` falha, o `outcome` é `failure`, mas a `conclusion` final é `success`. |
| `steps.<step_id>.outputs.<output_name>` | `string` | Valor de uma saída específica. |

### Exemplo de conteúdo do contexto `steps`

Este exemplo de contexto `steps` mostra duas etapas anteriores que tinham uma [`id`](workflow-syntax.md#jobsjob_idstepsid) especificada. A primeira etapa tinha a `id` chamada `checkout`, e a segunda, `generate_number`. A etapa `generate_number` tinha uma saída chamada `random_number`.

```json
{
  "checkout": {
    "outputs": {},
    "outcome": "success",
    "conclusion": "success"
  },
  "generate_number": {
    "outputs": {
      "random_number": "1"
    },
    "outcome": "success",
    "conclusion": "success"
  }
}
```

### Exemplo de uso do contexto `steps`

Este exemplo de fluxo de trabalho gera um número aleatório como saída em uma etapa, e uma etapa posterior usa o contexto `steps` para ler o valor dessa saída.

```yaml copy
name: Generate random failure
on: push
jobs:
  randomly-failing-job:
    runs-on: ubuntu-latest
    steps:
      - name: Generate 0 or 1
        id: generate_number
        run: echo "random_number=$(($RANDOM % 2))" >> $GITHUB_OUTPUT
      - name: Pass or fail
        run: |
          if [[ ${{ steps.generate_number.outputs.random_number }} == 0 ]]; then exit 0; else exit 1; fi
```

## Contexto `runner`

O contexto `runner` contém informações sobre o runner que está executando o trabalho atual.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `runner` | `object` | O contexto muda para cada trabalho durante a execução de um fluxo de trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `runner.name` | `string` | O nome do executor que executa a tarefa. Esse nome pode não ser exclusivo em uma execução de fluxo de trabalho, pois os executores nos níveis de repositório e organização podem usar o mesmo nome. |
| `runner.os` | `string` | O sistema operacional do executor que está executando o trabalho. Os valores possíveis são `Linux`, `Windows`, ou `macOS`. |
| `runner.arch` | `string` | A arquitetura do executor que está executando o trabalho. Os valores possíveis são `X86`, `X64`, `ARM` ou `ARM64`. |
| `runner.temp` | `string` | O caminho para um diretório temporário no executor. Este diretório é esvaziado no início e no final de cada trabalho. Observe que os arquivos não serão removidos se a conta de usuário do executor não tiver permissão para excluí-los. |
| `runner.tool_cache` | `string` | O caminho para o diretório contendo ferramentas pré-instaladas de executores GitHub hospedados. Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images). |
| `runner.debug` | `string` | Isso será definido somente se o [log de depuração](../../how-tos/monitor-workflows/enable-debug-logging.md) estiver habilitado e sempre tiver o valor de `1`. Pode ser útil como um indicador para habilitar a depuração adicional ou o log detalhado em suas etapas de trabalho. |
| `runner.environment` | `string` | O ambiente do executor que realiza a tarefa. Os valores possíveis são: `github-hosted` para executores hospedados no GitHub fornecidos pelo GitHub e `self-hosted` para executores auto-hospedados configurados pelo proprietário do repositório. |

### Exemplo de conteúdo do contexto `runner`

O contexto de exemplo a seguir é de um executor hospedado no Linux GitHub.

```json
{
  "os": "Linux",
  "arch": "X64",
  "name": "GitHub Actions 2",
  "tool_cache": "/opt/hostedtoolcache",
  "temp": "/home/runner/work/_temp"
}
```

### Exemplo de uso do contexto `runner`

Este exemplo de fluxo de trabalho usa o contexto `runner` para definir o caminho para o diretório temporário onde serão gravados registros, e se o fluxo de trabalho falhar, ele fará o upload desses registros como artefato.

```yaml copy
name: Build
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Build with logs
        run: |
          mkdir ${{ runner.temp }}/build_logs
          echo "Logs from building" > ${{ runner.temp }}/build_logs/build.logs
          exit 1
      - name: Upload logs on fail
        if: ${{ failure() }}
        uses: actions/upload-artifact@v4
        with:
          name: Build failure logs
          path: ${{ runner.temp }}/build_logs
```

## Contexto `secrets`

O contexto `secrets` contém os nomes e valores de segredos que estão disponíveis para a execução de um fluxo de trabalho. O contexto `secrets` não está disponível para ações compostas por motivos de segurança. Para passar um segredo para uma ação composta, é necessário fazê-lo explicitamente como um parâmetro. Para saber mais sobre segredos, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

`GITHUB_TOKEN` é um segredo que é criado automaticamente para cada execução de fluxo de trabalho e é sempre incluído no contexto `secrets`. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

!!! warning
    Se um segredo foi usado em um trabalho de fluxo de trabalho, o GitHub edita automaticamente os segredos impressos no log. Você deve evitar imprimir segredos no log intencionalmente.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `secrets` | `object` | Esse contexto é o mesmo para cada trabalho em uma execução do fluxo de trabalho. Você pode acessar esse contexto em qualquer etapa de um trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `secrets.GITHUB_TOKEN` | `string` | Token criado automaticamente para cada execução do fluxo de trabalho. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md). |
| `secrets.<secret_name>` | `string` | O valor de um segredo específico. |

### Exemplo de conteúdo do contexto `secrets`

O exemplo de conteúdo do contexto `secrets` mostra o `GITHUB_TOKEN` automático, assim como outros dois segredos disponíveis para a execução de fluxo de trabalho.

```json
{
  "github_token": "***",
  "NPM_TOKEN": "***",
  "SUPERSECRET": "***"
}
```

### Exemplo de uso do contexto `secrets`

Este exemplo de fluxo de trabalho usa a [CLI do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md), que requer o `GITHUB_TOKEN` como o valor para o parâmetro de entrada `GH_TOKEN`:

```yaml copy
name: Open new issue
on: workflow_dispatch

jobs:
  open-issue:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - run: |
          gh issue --repo ${{ github.repository }} \
            create --title "Issue title" --body "Issue body"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Contexto `strategy`

Para fluxos de trabalho com uma matriz, o contexto `strategy` contém informações sobre a estratégia de execução da matriz para o trabalho atual.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `strategy` | `object` | O contexto muda para cada trabalho durante a execução de um fluxo de trabalho. Você pode acessar este contexto a partir de qualquer trabalho ou etapa em um fluxo de trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `strategy.fail-fast` | `boolean` | Quando isso é avaliado como `true`, todos os trabalhos em andamento são cancelados em caso de falha em qualquer trabalho em uma matriz. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idstrategyfail-fast). |
| `strategy.job-index` | `number` | O índice do trabalho atual na matriz. |
| **Observação:** esse número é um número baseado em zero. O índice da primeira tarefa na matriz é `0`. |  |  |
| `strategy.job-total` | `number` | O número total de trabalhos na matriz. |
| **Observação:** esse número **não é** um número baseado em zero. Por exemplo, para uma matriz com quatro trabalhos, o valor de `job-total` é `4`. |  |  |
| `strategy.max-parallel` | `number` | O número máximo de trabalhos que podem ser executados simultaneamente quando uma estratégia de trabalho `matrix` é usada. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idstrategymax-parallel). |

### Exemplo de conteúdo do contexto `strategy`

O exemplo de conteúdo a seguir do contexto `strategy` é de uma matriz com quatro tarefas e foi obtido da tarefa final. Observe a diferença entre o número `job-index` baseado em zero e `job-total`, que não é baseado em zero.

```json
{
  "fail-fast": true,
  "job-index": 3,
  "job-total": 4,
  "max-parallel": 4
}
```

### Exemplo de uso do contexto `strategy`

Este exemplo de fluxo de trabalho usa a propriedade `strategy.job-index` para definir um nome exclusivo para um arquivo de log para cada trabalho em uma matriz.

```yaml copy
name: Test strategy
on: push

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-group: [1, 2]
        node: [14, 16]
    steps:
      - run: echo "Mock test logs" > test-job-${{ strategy.job-index }}.txt
      - name: Upload logs
        uses: actions/upload-artifact@v4
        with:
          name: Build log for job ${{ strategy.job-index }}
          path: test-job-${{ strategy.job-index }}.txt
```

## Contexto `matrix`

Para fluxos de trabalho com uma matriz, o contexto `matrix` contém as propriedades definidas no arquivo de fluxo de trabalho que se aplicam ao trabalho atual. Por exemplo, se você configurar uma matriz com as chaves `os` e `node`, o objeto de contexto `matrix` incluirá as propriedades `os` e `node` com os valores que estão sendo usados para o trabalho atual.

Não há propriedades padrão no contexto `matrix`, apenas aquelas que são definidas no arquivo de fluxo de trabalho.

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `matrix` | `object` | Esse contexto só está disponível para trabalhos em uma matriz e em alterações para cada trabalho na execução de um fluxo de trabalho. Você pode acessar este contexto a partir de qualquer trabalho ou etapa em um fluxo de trabalho. Este objeto contém as propriedades listadas abaixo. |
| `matrix.<property_name>` | `string` | O valor da propriedade de uma matriz. |

!!! note
    Os nomes das variáveis não fazem distinção entre maiúsculas e minúsculas. Por exemplo, `OS` e `os` será tratado como a mesma variável.

### Exemplo de conteúdo do contexto `matrix`

O exemplo a seguir do contexto `matrix` é de um trabalho em uma matriz que tem as propriedades de matriz `os` e `node` definidas no fluxo de trabalho. O trabalho executa a combinação matricial de um sistema operacional `ubuntu-latest` com a versão `16` do Node.js.

```json
{
  "os": "ubuntu-latest",
  "node": 16
}
```

### Exemplo de uso do contexto `matrix`

Este exemplo de fluxo de trabalho cria uma matriz com as chaves `os` e `node`. Ele usa a propriedade `matrix.os` para definir o tipo de executor de cada trabalho e a propriedade `matrix.node` para definir a versão do Node.js de cada trabalho.

```yaml copy
name: Test matrix
on: push

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        node: [14, 16]
    steps:
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.node }}
      - name: Output node version
        run: node --version
```

## Contexto `needs`

O contexto `needs` contém as saídas de todos os trabalhos definidos como uma dependência direta do trabalho atual. Observe que isso não inclui trabalhos implicitamente dependentes (por exemplo, trabalhos dependentes de outro dependente). Para saber mais sobre como definir dependências de trabalho, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idneeds).

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `needs` | `object` | Esse contexto só é preenchido para execuções de fluxo de trabalho com funções dependentes e as alterações para cada trabalho em uma execução de fluxo de trabalho. Você pode acessar este contexto a partir de qualquer trabalho ou etapa em um fluxo de trabalho. Este objeto contém todas as propriedades listadas abaixo. |
| `needs.<job_id>` | `object` | Um único trabalho do qual o trabalho atual depende. |
| `needs.<job_id>.outputs` | `object` | O conjunto de saídas de um trabalho do qual o trabalho atual depende. |
| `needs.<job_id>.outputs.<output name>` | `string` | O valor de um resultado específico para um trabalho do qual o trabalho atual depende. |
| `needs.<job_id>.result` | `string` | O resultado de um trabalho do qual depende o trabalho atual. Os valores possíveis são `success`, `failure`, `cancelled` ou `skipped`. |

### Exemplo de conteúdo do contexto `needs`

O exemplo de conteúdo a seguir do contexto `needs` mostra informações de dois trabalhos dos quais o trabalho atual depende.

```json
{
  "build": {
    "result": "success",
    "outputs": {
      "build_id": "123456"
    }
  },
  "deploy": {
    "result": "failure",
    "outputs": {}
  }
}
```

### Exemplo de uso do contexto `needs`

Este exemplo de fluxo de trabalho tem três trabalhos: um trabalho `build` que faz um build, um trabalho `deploy` que exige o trabalho `build` e um trabalho `debug` que exige os trabalhos `build` e `deploy` e que será executado somente se houver uma falha no fluxo de trabalho. O trabalho `deploy` também usa o contexto `needs` para acessar uma saída do trabalho `build`.

```yaml copy
name: Build and deploy
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      build_id: ${{ steps.build_step.outputs.build_id }}
    steps:
      - name: Build
        id: build_step
        run: echo "build_id=$RANDOM" >> $GITHUB_OUTPUT
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying build ${{ needs.build.outputs.build_id }}"
  debug:
    needs: [build, deploy]
    runs-on: ubuntu-latest
    if: ${{ failure() }}
    steps:
      - run: echo "Failed to build and deploy"
```

## Contexto `inputs`

O contexto `inputs` contém propriedades de entrada passadas para uma ação, para um fluxo de trabalho reutilizável ou para um fluxo de trabalho disparado manualmente. Para fluxos de trabalho reutilizáveis, os nomes e os tipos de entrada são definidos na [configuração de evento `workflow_call`](events-that-trigger-workflows.md) de um fluxo de trabalho reutilizável, e os valores de entrada são transmitidos de [`jobs.<job_id>.with`](workflow-syntax.md#jobsjob_idwith) em um fluxo de trabalho externo que chama o fluxo de trabalho reutilizável. Para fluxos de trabalho disparados manualmente, as entradas são definidas na configuração de evento[`workflow_dispatch`](events-that-trigger-workflows.md#workflow_dispatch) de um fluxo de trabalho.

As propriedades no contexto `inputs` são definidas no arquivo de fluxo de trabalho. Eles estão disponíveis apenas em um [fluxo de trabalho reutilizável](../../how-tos/reuse-automations/reuse-workflows.md) ou em um fluxo de trabalho acionado pelo [`workflow_dispatch` evento](events-that-trigger-workflows.md#workflow_dispatch)

| Nome da propriedade | Tipo | Descrição |
| --- | --- | --- |
| `inputs` | `object` | Esse contexto só está disponível em um [fluxo de trabalho reutilizável](../../how-tos/reuse-automations/reuse-workflows.md) ou em um fluxo de trabalho acionado pelo [`workflow_dispatch` evento](events-that-trigger-workflows.md#workflow_dispatch). Você pode acessar este contexto a partir de qualquer trabalho ou etapa em um fluxo de trabalho. Este objeto contém as propriedades listadas abaixo. |
| `inputs.<name>` |  |  |
| `string` ou `number` ou `boolean` ou `choice` | Cada valor de entrada é passado de um fluxo de trabalho externo. |  |

### Exemplo de conteúdo do contexto `inputs`

O conteúdo de exemplo a seguir do contexto `inputs` é de um fluxo de trabalho que definiu as entradas `build_id`, `deploy_target` e `perform_deploy`.

```json
{
  "build_id": 123456768,
  "deploy_target": "deployment_sys_1a",
  "perform_deploy": true
}
```

### Exemplo de uso do contexto `inputs` em um fluxo de trabalho reutilizável

Este exemplo de fluxo de trabalho reutilizável usa o contexto `inputs` para obter os valores dos inputs `build_id`, `deploy_target` e `perform_deploy` que foram passados para o fluxo de trabalho reutilizável a partir do fluxo de trabalho chamador.

```yaml copy
name: Reusable deploy workflow
on:
  workflow_call:
    inputs:
      build_id:
        required: true
        type: number
      deploy_target:
        required: true
        type: string
      perform_deploy:
        required: true
        type: boolean

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ inputs.perform_deploy }}
    steps:
      - name: Deploy build to target
        run: echo "Deploying build:${{ inputs.build_id }} to target:${{ inputs.deploy_target }}"
```

### Exemplo de uso do contexto `inputs` em um fluxo de trabalho acionado manualmente

Este exemplo de fluxo de trabalho disparado por um evento de `workflow_dispatch` usa o contexto `inputs` para obter os valores de entrada de `build_id`, `deploy_target` e `perform_deploy` que foram passadas para o fluxo de trabalho.

```yaml copy
on:
  workflow_dispatch:
    inputs:
      build_id:
        required: true
        type: string
      deploy_target:
        required: true
        type: string
      perform_deploy:
        required: true
        type: boolean

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ inputs.perform_deploy }}
    steps:
      - name: Deploy build to target
        run: echo "Deploying build:${{ inputs.build_id }} to target:${{ inputs.deploy_target }}"
```

## Leitura adicional

* [Contextos](../../concepts/workflows-and-actions/contexts.md)
