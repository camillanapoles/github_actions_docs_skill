---
title: Referência de variáveis
description: Encontre informações para variáveis com suporte, convenções de nomenclatura, limites e contextos em GitHub Actions fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/variables
captured: '2026-10-11'
section: Reference / Workflows and actions
---

# Referência de variáveis

_Encontre informações para variáveis com suporte, convenções de nomenclatura, limites e contextos em GitHub Actions fluxos de trabalho._

Este artigo lista as variáveis com suporte que você pode usar em GitHub Actions fluxos de trabalho, incluindo variáveis de ambiente, variáveis de configuração e variáveis padrão fornecidas por GitHub. Use essa referência para pesquisar nomes de variáveis, convenções de nomenclatura, limites e contextos com suporte ao configurar seus fluxos de trabalho.

Para obter mais informações sobre variáveis, confira [Variáveis](../../concepts/workflows-and-actions/variables.md).

## Variáveis de ambiente padrão

As variáveis de ambiente padrão que GitHub definem estão disponíveis para cada etapa em um fluxo de trabalho.

Como as variáveis de ambiente padrão são definidas por GitHub e não em um fluxo de trabalho, elas não são acessíveis por meio do contexto `env`. No entanto, a maioria das variáveis padrão tem uma propriedade de contexto correspondente e nomeada de modo semelhante. Por exemplo, o valor da variável `GITHUB_REF` pode ser lido durante o processamento do fluxo de trabalho usando a propriedade de contexto `${{ github.ref }}`.

Não é possível substituir o valor das variáveis de ambiente padrão chamadas `GITHUB_*` e `RUNNER_*`. Atualmente, você pode substituir o valor da variável `CI`. No entanto, não é garantido que isso sempre será possível. Para obter mais informações sobre como definir variáveis de ambiente, consulte [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-environment-variables-for-a-single-workflow) e [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#setting-an-environment-variable).

É altamente recomendável que as ações usem variáveis para acessar o sistema de arquivos em vez de usar caminhos de arquivos codificados.
GitHub define variáveis para ações a serem usadas em todos os ambientes de executor.

| Variável | Descrição |
| --- | --- |
| `CI` | Sempre defina como `true`. Você pode usar essa variável para diferenciar quando os testes estão sendo executados localmente ou por GitHub Actions. |
| `GITHUB_ACTION` | O nome da ação atualmente em execução, ou o [`id`](workflow-syntax.md#jobsjob_idstepsid) de uma etapa. Por exemplo, para uma ação, `__repo-owner_name-of-action-repo`. |
| GitHub remove caracteres especiais e usa o nome `__run` quando a etapa atual executa um script sem um `id`. Se você usar o mesmo script ou ação mais de uma vez no mesmo trabalho, o nome incluirá um sufixo que consiste do número de sequência precedido por um sublinhado. Por exemplo, o primeiro script que você executar terá o nome `__run`, e o segundo script será chamado `__run_2`. Da mesma forma, a segunda invocação de `actions/checkout` será `actionscheckout2`. |  |
| `GITHUB_ACTION_PATH` | O caminho onde uma ação está localizada. Esta propriedade só é compatível com ações compostas. Você pode usar este caminho para mudar os diretórios onde a ação está localizada e acessar outros arquivos localizados no mesmo repositório da ação. Por exemplo, `/home/runner/work/_actions/repo-owner/name-of-action-repo/v1`. |
| `GITHUB_ACTION_REPOSITORY` | Para uma etapa que executa uma ação, este é o nome do proprietário e do repositório da ação. Por exemplo, `actions/checkout`. |
| `GITHUB_ACTIONS` | Sempre definido como `true` quando GitHub Actions estiver executando o fluxo de trabalho. Você pode usar essa variável para diferenciar quando os testes estão sendo executados localmente ou por GitHub Actions. |
| `GITHUB_ACTOR` | Nome da pessoa ou aplicativo que iniciou o fluxo de trabalho. Por exemplo, `octocat`. |
| `GITHUB_ACTOR_ID` | A ID da conta da pessoa ou do aplicativo que disparou a execução inicial do fluxo de trabalho. Por exemplo, `1234567`. Observe que isso é diferente do nome de usuário do ator. |
| `GITHUB_API_URL` | Retorna a URL da API. Por exemplo: `https://api.github.com`. |
| `GITHUB_ARTIFACTS` | O caminho no runner para o arquivo que declara artefatos de fluxo de trabalho na etapa atual. Escreva uma declaração por linha para identificar arquivos ou referências de resumo OCI como artefatos de fluxo de trabalho. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#declaring-workflow-artifacts). |
| `GITHUB_ARTIFACTS_LIST` | O caminho no runner para um arquivo somente para leitura que contém metadados agregados dos artefatos do fluxo de trabalho da tarefa atual na forma de um objeto JSON. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#reading-workflow-artifacts). |
| `GITHUB_BASE_REF` | O nome do ref da base ou o branch de destino do pull request na execução de um fluxo de trabalho. Isso só é definido quando o evento que dispara uma execução de fluxo de trabalho é `pull_request` ou `pull_request_target`. Por exemplo, `main`. |
| `GITHUB_ENV` | O caminho no executor para o arquivo que define as variáveis por meio de comandos do fluxo de trabalho. O caminho deste arquivo é único para a etapa atual e muda em cada etapa de um trabalho. Por exemplo, `/home/runner/work/_temp/_runner_file_commands/set_env_87406d6e-4979-4d42-98e1-3dab1f48b13a`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#setting-an-environment-variable). |
| `GITHUB_EVENT_NAME` | Nome do evento que acionou a execução do fluxo de trabalho. Por exemplo, `workflow_dispatch`. |
| `GITHUB_EVENT_PATH` | O caminho para o arquivo no executor que contém a carga completa do webhook do evento. Por exemplo, `/github/workflow/event.json`. |
| `GITHUB_GRAPHQL_URL` | Retorna a URL da API GraphQL. Por exemplo: `https://api.github.com/graphql`. |
| `GITHUB_HEAD_REF` | A ref principal ou o branch da fonte do pull request na execução de um fluxo de trabalho. Essa propriedade só é definida quando o evento que dispara uma execução de fluxo de trabalho é `pull_request` ou `pull_request_target`. Por exemplo, `feature-branch-1`. |
| `GITHUB_JOB` | A [job_id](workflow-syntax.md#jobsjob_id) do trabalho atual. Por exemplo, `greeting_job`. |
| `GITHUB_OUTPUT` | O caminho no executor para o arquivo que define as saídas da etapa atual a partir de comandos do fluxo de trabalho. O caminho deste arquivo é único para a etapa atual e muda em cada etapa de um trabalho. Por exemplo, `/home/runner/work/_temp/_runner_file_commands/set_output_a50ef383-b063-46d9-9157-57953fc9f3f0`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#setting-an-output-parameter). |
| `GITHUB_PATH` | O caminho no executor para o arquivo que define as variáveis `PATH` do ambiente por meio dos comandos do fluxo de trabalho. O caminho deste arquivo é único para a etapa atual e muda em cada etapa de um trabalho. Por exemplo, `/home/runner/work/_temp/_runner_file_commands/add_path_899b9445-ad4a-400c-aa89-249f18632cf5`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#adding-a-system-path). |
| `GITHUB_REF` | A referência completa do branch ou tag que acionou o fluxo de trabalho. Para fluxos de trabalho disparados por `push`, esse é o branch ou a ref da tag que foi enviada. Para fluxos de trabalho disparados por `pull_request` que não foram mesclados, este é o branch de mesclagem do pull request. Se a solicitação de pull foi mesclada, essa é a ramificação na qual ela foi mesclada. Para fluxos de trabalho disparados por `release`, essa é a tag de versão criada. Para outros gatilhos, esse é o branch ou a ref de tag que disparou a execução do fluxo de trabalho. Essa variável só é definida quando há um branch ou uma tag disponível para o tipo de evento. A ref fornecida tem o formato completo, o que significa que, para branches, o formato é `refs/heads/<branch_name>`. Para eventos de solicitação de pull, exceto `pull_request_target` que não foram mesclados, é `refs/pull/<pr_number>/merge`. Eventos `pull_request_target` têm o `ref` do ramo base. Para as etiquetas, é `refs/tags/<tag_name>`. Por exemplo, `refs/heads/feature-branch-1`. Para obter mais informações sobre branches de mesclagem de solicitação de pull, consulte [Solicitações de pull](https://docs.github.com/pt/pull-requests/reference/pull-requests#pull-request-refs-and-merge-branches). |
| `GITHUB_REF_NAME` | O nome de ref curto do branch ou tag que acionou a execução do fluxo de trabalho. Esse valor corresponde ao nome do branch ou tag mostrado em GitHub. Por exemplo, `feature-branch-1`.  Para solicitações de pull que não foram mescladas, o formato é `<pr_number>/merge`. |
| `GITHUB_REF_PROTECTED` | `true` se proteções de ramificação ou [conjuntos de regras](https://docs.github.com/pt/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository) estiverem configurados para a referência que disparou a execução do fluxo de trabalho. |
| `GITHUB_REF_TYPE` | O tipo de ref que acionou a execução do fluxo de trabalho. Os valores válidos são `branch` ou `tag`. |
| `GITHUB_REPOSITORY` | Nome do repositório e o proprietário. Por exemplo, `octocat/Hello-World`. |
| `GITHUB_REPOSITORY_ID` | A ID do repositório. Por exemplo, `123456789`. Observe que isso é diferente do nome do repositório. |
| `GITHUB_REPOSITORY_OWNER` | O nome do proprietário do repositório. Por exemplo, `octocat`. |
| `GITHUB_REPOSITORY_OWNER_ID` | A ID da conta do proprietário do repositório. Por exemplo, `1234567`. Observe que isso é diferente do nome do proprietário. |
| `GITHUB_RETENTION_DAYS` | O número de dias em que os logs e os artefatos da execução de fluxo de trabalho são mantidos. Por exemplo, `90`. |
| `GITHUB_RUN_ATTEMPT` | Um número exclusivo para cada tentativa de execução de um fluxo de trabalho específico em um repositório. Este número começa em 1 para a primeira tentativa de execução do fluxo de trabalho e aumenta a cada nova execução. Por exemplo, `3`. |
| `GITHUB_RUN_ID` |  |
| Um número exclusivo para cada fluxo de trabalho executado em um repositório. Este número não muda se você executar novamente o fluxo de trabalho. Por exemplo, `1658821493`. |  |
| `GITHUB_RUN_NUMBER` |  |
| Um número exclusivo para cada execução de um fluxo de trabalho específico em um repositório. Esse número começa em 1 para a primeira execução do fluxo de trabalho e é incrementado a cada nova operação. Este número não muda se você executar novamente o fluxo de trabalho. Por exemplo, `3`. |  |
| `GITHUB_SERVER_URL` | A URL do servidor GitHub. Por exemplo: `https://github.com`. |
| `GITHUB_SHA` | O commit SHA que acionou o fluxo de trabalho. O valor do commit deste SHA depende do evento que acionou o fluxo de trabalho. Para saber mais, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md). Por exemplo, `ffac537e6cbbf934b08745a378932722df287a53`. |
| `GITHUB_STEP_SUMMARY` | O caminho no executor para o arquivo que contém os resumos de trabalho dos comandos de fluxo de trabalho. O caminho deste arquivo é único para a etapa atual e muda em cada etapa de um trabalho. Por exemplo, `/home/runner/_layout/_work/_temp/_runner_file_commands/step_summary_1cb22d7f-5663-41a8-9ffc-13472605c76c`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#adding-a-job-summary). |
| `GITHUB_TRIGGERING_ACTOR` | O nome de usuário de quem iniciou a execução do fluxo de trabalho. Se a execução do fluxo de trabalho for executada novamente, esse valor poderá ser diferente de `github.actor`. Qualquer nova execução de fluxo de trabalho usará os privilégios de `github.actor`, mesmo que o ator que inicie a nova execução (`github.triggering_actor`) tenha privilégios diferentes. |
| `GITHUB_WORKFLOW` | Nome do fluxo de trabalho. Por exemplo, `My test workflow`. Se o arquivo de fluxo de trabalho não especificar um `name`, o valor dessa variável será o caminho completo do arquivo de fluxo de trabalho no repositório. |
| `GITHUB_WORKFLOW_REF` | O caminho de referência para o fluxo de trabalho. Por exemplo, `octocat/hello-world/.github/workflows/my-workflow.yml@refs/heads/my_branch`. |
| `GITHUB_WORKFLOW_SHA` | O SHA de commit para o arquivo de fluxo de trabalho. |
| `GITHUB_WORKSPACE` | O diretório de trabalho padrão no executador para as etapas, assim como o local padrão do seu repositório ao utilizar a ação [`checkout`](https://github.com/actions/checkout). Por exemplo, `/home/runner/work/my-repo-name/my-repo-name`. |
| `RUNNER_ARCH` | A arquitetura do executor que está executando o trabalho. Os valores possíveis são `X86`, `X64`, `ARM` ou `ARM64`. |
| `RUNNER_DEBUG` | Isso será definido somente se o [log de depuração](../../how-tos/monitor-workflows/enable-debug-logging.md) estiver habilitado e sempre tiver o valor de `1`. Pode ser útil como um indicador para habilitar a depuração adicional ou o log detalhado em suas etapas de trabalho. |
| `RUNNER_ENVIRONMENT` | O ambiente do executor que realiza a tarefa. Os valores possíveis são: `github-hosted` para executores hospedados no GitHub fornecidos pelo GitHub e `self-hosted` para executores auto-hospedados configurados pelo proprietário do repositório. |
| `RUNNER_NAME` |  |
| O nome do executor que executa a tarefa. Esse nome pode não ser exclusivo em uma execução de fluxo de trabalho, pois os executores nos níveis de repositório e organização podem usar o mesmo nome. Por exemplo `Hosted Agent` |  |
| `RUNNER_OS` |  |
| O sistema operacional do executor que está executando o trabalho. Os valores possíveis são `Linux`, `Windows`, ou `macOS`. Por exemplo `Windows` |  |
| `RUNNER_TEMP` |  |
| O caminho para um diretório temporário no executor. Este diretório é esvaziado no início e no final de cada trabalho. Observe que os arquivos não serão removidos se a conta de usuário do executor não tiver permissão para excluí-los. Por exemplo `D:\a_temp` |  |
| `RUNNER_TOOL_CACHE` |  |
| O caminho para o diretório contendo ferramentas pré-instaladas de executores GitHub hospedados. Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images). Por exemplo `C:\hostedtoolcache\windows` |  |

!!! note
    Caso precise usar a URL de execução de um fluxo de trabalho dentro de um trabalho, combine estas variáveis: `$GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID`

## Convenções de nomenclatura para variáveis de configuração

As seguintes regras se aplicam aos nomes de variáveis de configuração:

* Só pode conter caracteres alfanuméricos (`[a-z]`, `[A-Z]`, `[0-9]`) ou sublinhados (`_`). Espaços não são permitidos.
* Não precisa começar com o prefixo `GITHUB_`.
* Não precisa começar com um número.
* Não diferenciam maiúsculas de minúsculas quando referenciados. GitHub armazena nomes secretos como maiúsculas, independentemente de como eles são inseridos.
* Deve ser exclusivo para o repositório, a organização ou a empresa em que são criados.

## Convenções de nomenclatura para variáveis de ambiente

Ao definir uma variável de ambiente, você não pode usar nenhum dos nomes das variáveis de ambiente padrão. Para obter uma lista completa de variáveis de ambiente padrão, confira [Referência de variáveis](variables.md#default-environment-variables) abaixo. Se você tentar substituir o valor de uma dessas variáveis padrão, a atribuição será ignorada.

!!! note
    Você pode listar todo o conjunto de variáveis de ambiente disponíveis para uma etapa de fluxo de trabalho usando `run: env` em uma etapa e analisando a saída da etapa.

## Precedência da variável de configuração

Se houver uma variável com mesmo nome em vários níveis, a variável do nível mais baixo terá precedência. Por exemplo, se uma variável no nível da organização tiver o mesmo nome que uma no nível do repositório, a segunda terá precedência. Da mesma forma, se uma organização, um repositório e um ambiente tiverem uma variável com mesmo nome, àquela no nível do ambiente terá precedência.

!!! note
    As variáveis de nível de ambiente só estão disponíveis no runner depois que a tarefa começa a ser executada. Isso significa que as variáveis de nível de ambiente não substituirão variáveis nos contextos `env` e `vars`.

Para fluxos de trabalho reutilizáveis, são usadas as variáveis do repositório do fluxo de trabalho do chamador. As variáveis do repositório que contém o fluxo de trabalho chamado não são disponibilizadas para o fluxo de trabalho do chamador.

## Limites para variáveis de configuração

As variáveis individuais são limitadas a 48 KB.

Você pode armazenar até 1.000 variáveis por organização, 500 variáveis por repositório e 100 variáveis por ambiente. O limite total de tamanho combinado para variáveis de organização e repositório é de 256 KB por execução de fluxo de trabalho.

Um fluxo de trabalho criado em um repositório pode acessar o seguinte número de variáveis:

* Até 500 variáveis de repositório, se o tamanho total dessas variáveis for menor que 256 KB. Se o tamanho total das variáveis de repositório exceder 256 KB, somente as que estiverem abaixo do limite estarão disponíveis (conforme classificado em ordem alfabética pelo nome da variável).
* Até 1.000 variáveis de organização, se o tamanho total combinado das variáveis de repositório e organização for menor que 256 KB. Se o tamanho total combinado das variáveis de organização e repositório exceder 256 KB, somente as variáveis da organização que estiverem abaixo desse limite estarão disponíveis (após a contabilização de variáveis de repositório e classificadas em ordem alfabética pelo nome da variável).
* Até 100 variáveis de nível de ambiente.

!!! note
    As variáveis de nível de ambiente não contam para o limite de tamanho total de 256 KB. Se você exceder o limite de tamanho combinado para variáveis de repositório e de organização e ainda precisar de variáveis adicionais, poderá usar um ambiente e definir mais variáveis no ambiente.

## Contextos com suporte

Normalmente, você usará o contexto `env` ou `github` para acessar valores de variáveis em partes do fluxo de trabalho processadas antes que os trabalhos sejam enviados aos executores.

> [!WARNING] Não imprima o contexto `github` em logs. Ele contém informações confidenciais.

| Contexto | Caso de uso | Exemplo |
| --- | --- | --- |
| `env` | Variáveis personalizadas de referência definidas no fluxo de trabalho. | `${{ env.MY_VARIABLE }}` |
| `github` | Informações de referência sobre a execução do fluxo de trabalho e o evento que acionou a execução. | `${{ github.repository }}` |
