---
title: Migrando do GitLab com o Importador de GitHub Actions
description: Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do GitLab para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/gitlab-migration
captured: '2026-10-26'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando do GitLab com o Importador de GitHub Actions

_Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do GitLab para GitHub Actions._

## Sobre a migração do GitLab usando o Importador do GitHub Actions

As instruções abaixo orientarão você na configuração do seu ambiente para usar GitHub Actions Importer para migrar pipelines do GitLab para GitHub Actions.

### Pré-requisitos

* Uma conta ou organização do GitLab com pipelines e trabalhos que você deseja converter em fluxos de trabalho do GitHub Actions.
* Acesso para criar um GitLab personal access token para sua conta ou organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações

Há algumas limitações para migrar processos automaticamente dos pipelines do GitLab para GitHub Actions com GitHub Actions Importer.

* Não há suporte para o cache automático entre trabalhos de fluxos de trabalho diferentes.
* Só há suporte para o comando `audit` quando uma conta de organização é usada. No entanto, os comandos `dry-run` e `migrate` podem ser usados com uma conta de usuário ou de organização.

#### Tarefas manuais

Certos constructos do GitLab devem ser migrados manualmente. Estão incluídos:

* Valores mascarados de variáveis de projeto ou grupo
* Relatórios de artefatos

Para saber mais sobre migrações manuais, confira [Migrando de CI/CD do GitLab para GitHub Actions](../manual-migrations/migrate-from-gitlab-cicd.md).

## Instalando a extensão da GitHub Actions Importer CLI

1. Instale a extensão da CLI do GitHub Actions Importer:

            ```bash copy
   gh extension install github/gh-actions-importer
   ```

2. Verifique se a extensão foi instalada:

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

## Como configurar credenciais

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer trabalhar com o GitLab e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um personal access token do GitLab. Para obter mais informações, consulte [Personal access tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#create-a-personal-access-token) a documentação do GitLab.

   O token precisa ter o escopo `read_api`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
   ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `GitLab`, pressione `Espaço` para fazer a seleção e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Token privado para GitLab", insira o valor do GitLab personal access token que você criou anteriormente e pressione `Enter`.
   * Em "URL base da instância do GitLab", digite a URL da instância do GitLab e pressione `Enter`.

   Um exemplo da saída do comando `configure` é mostrado abaixo.

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: GitLab
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Private token for GitLab: ***************
   ✔ Base url of the GitLab instance: http://localhost
   Environment variables successfully updated.
   ```

4. No terminal, execute o comando CLI GitHub Actions Importer`update` para se conectar a GitHub PackagesContainer registry e garantir que a imagem do contêiner esteja atualizada para a versão mais recente:

            ```shell
   gh actions-importer update
   ```

   A saída do comando será semelhante ao seguinte:

            ```shell
   Updating ghcr.io/actions-importer/cli:latest...
   ghcr.io/actions-importer/cli:latest up-to-date
   ```

## Executar uma auditoria do GitLab

É possível usar o comando `audit` para obter uma exibição resumida de todos os pipelines em um servidor do GitLab.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos em um servidor do GitLab.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Pré-requisitos para o comando audit

Para usar o `audit` comando, você deve ter uma personal access token conta de organização do GitLab configurada.

### Como executar o comando de auditoria

Para realizar uma auditoria de um servidor do GitLab, execute o seguinte comando no terminal, substituindo `my-gitlab-namespace` pelo namespace ou grupo que será auditado:

```shell
gh actions-importer audit gitlab --output-dir tmp/audit --namespace my-gitlab-namespace
```

### Como inspecionar os resultados da auditoria

Os arquivos do diretório de saída especificado contêm os resultados da auditoria. Confira o arquivo `audit_summary.md` para ver um resumo dos resultados da auditoria.

O resumo da auditoria contém as seções a seguir.

#### Pipelines

A seção "Pipelines" contém estatísticas gerais sobre a taxa de conversão realizada por GitHub Actions Importer.

Veja abaixo alguns termos importantes que podem aparecer na seção "Pipelines":

* **Pipelines bem-sucedidos** tiveram 100% dos componentes do pipeline e itens individuais convertidos automaticamente para seus equivalentes GitHub Actions.
* **Pipelines parcialmente bem-sucedidos** tiveram todos os constructos de pipeline convertidos, no entanto, havia alguns itens individuais que não foram convertidos automaticamente em seu GitHub Actions equivalente.
* **Pipelines sem suporte** são tipos de definição que não têm suporte GitHub Actions Importer.
* Pipelines **com falha** apresentaram um erro fatal durante a conversão. Isso pode ocorrer por uma das seguintes razões:
  * O pipeline foi originalmente configurado incorretamente e era inválido.
  * GitHub Actions Importer encontrou um erro interno ao convertê-lo.
  * Houve uma resposta de rede malsucedida que tornou o pipeline inacessível, o que geralmente ocorre devido a credenciais inválidas.

#### Etapas de compilação

A seção "Etapas de compilação" contém uma visão geral das etapas de compilação individuais usadas em todos os pipelines e de quantas delas foram convertidas automaticamente por GitHub Actions Importer.

A seguir estão alguns termos-chave que podem aparecer na seção "Build steps":

* Uma etapa de compilação **conhecida** foi convertida automaticamente em uma ação equivalente.
* Uma etapa de compilação **desconhecida** não foi convertida automaticamente em uma ação equivalente.
* Uma etapa de compilação **sem suporte** é aquela que:
  * Fundamentalmente não suportado por GitHub Actions.
  * Configurado de uma maneira incompatível com GitHub Actions.
* Uma **ação** é uma lista das ações que foram usadas nos fluxos de trabalho convertidos. Isso pode ser importante para:
  * Se você usar GitHub Enterprise Server, reunindo a lista de ações para sincronizar com sua instância.
  * Definir uma lista de permissões em nível organizacional para as ações utilizadas. Essa lista de ações é abrangente e inclui as ações que as equipes de segurança ou conformidade podem precisar analisar.

#### Tarefas manuais

A seção "Tarefas manuais" contém uma visão geral das tarefas que GitHub Actions Importer não podem ser concluídas automaticamente e que você deve concluir manualmente.

Veja abaixo alguns termos importantes que podem aparecer na seção "Tarefas manuais":

* Um **segredo** é um segredo no nível do repositório ou da organização que é usado nos pipelines convertidos. Esses segredos devem ser criados manualmente no GitHub Actions para que esses pipelines funcionem corretamente. Para saber mais, confira [Usar segredos em ações do GitHub](../../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).
* Um **executor auto-hospedado refere-se** a um rótulo de um executor que é referenciado em um pipeline convertido que não é um GitHubexecutor hospedado. Será necessário definir manualmente esses executores para que os pipelines funcionem de maneira correta.

#### Arquivos

A seção final do relatório de auditoria fornece um manifesto de todos os arquivos que foram gravados em disco durante a auditoria.

Cada arquivo de pipeline tem diversos arquivos incluídos na auditoria, incluindo:

* O pipeline original como ele foi definido em GitHub.
* Todas as respostas de rede usadas para converter o pipeline.
* O arquivo de fluxo de trabalho convertido.
* Rastros de pilha que podem ser usados para solucionar problemas em uma falha na conversão de um pipeline.

Além disso, o arquivo `workflow_usage.csv` contém uma lista separada por vírgula de todas as ações, todos os segredos e todos os executores usados pelos pipelines convertidos com sucesso. Isso pode ser útil para determinar quais fluxos de trabalho usam quais ações, segredos ou executores e para executar revisões de segurança.

## Prever o uso potencial do executor de compilação

Você pode usar o comando `forecast` para prever o uso potencial GitHub Actions calculando métricas a partir de execuções concluídas de pipeline no seu servidor GitLab.

### Como executar o comando de previsão

Para executar uma previsão de uso potencial GitHub Actions , execute o seguinte comando em seu terminal, substituindo `my-gitlab-namespace` pelo namespace ou grupo que você está prevendo. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast gitlab --output-dir tmp/forecast --namespace my-gitlab-namespace
```

### Previsão de um namespace inteiro

Para prever um namespace inteiro e todos os subgrupos dele, especifique cada umm desses subgrupos no argumento `--namespace` ou na variável de ambiente `NAMESPACE`.

Por exemplo:

```shell
gh actions-importer forecast gitlab --namespace my-gitlab-namespace my-gitlab-namespace/subgroup-one my-gitlab-namespace/subgroup-two ...
```

### Como inspecionar o relatório de previsão

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.
  * Essa métrica está correlacionada ao quanto você deve esperar gastar no GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* ```
            As métricas de **tempo de espera** descrevem o tempo gasto por um trabalho aguardando um executor ficar disponível para executá-lo.
        ```
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Esta métrica pode ser usada para definir o número de executores que você deve configurar.

Além disso, essas métricas são definidas para cada fila de executores no GitLab. Isso é especialmente útil quando há uma combinação de executores hospedados ou auto-hospedados ou quando há computadores de especificação alta ou baixa, a fim de ver métricas específicas para diferentes tipos de executores.

  ```
## Executar uma migração de simulação de um pipeline do GitLab

Você pode usar o `dry-run` comando para converter um pipeline do GitLab em seu fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de simulação

Você pode usar o `dry-run` comando para converter um pipeline do GitLab em um fluxo de trabalho equivalente GitHub Actions . Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

Para executar uma simulação de migração dos pipelines do GitLab para o GitHub Actions, execute o comando a seguir no terminal, substituindo `my-gitlab-project` pelo campo de dados dinâmico do projeto do GitLab e pelo `my-gitlab-namespace` ou grupo (caminho completo do grupo para subgrupos, por exemplo, `my-org/my-team`) para o qual você está executando a simulação.

```shell
gh actions-importer dry-run gitlab --output-dir tmp/dry-run --namespace my-gitlab-namespace --project my-gitlab-project
```

### Como inspecionar os fluxos de trabalho convertidos

Você pode ver os logs da simulação e os arquivos de fluxo de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Executar uma migração de produção de um pipeline do GitLab

Você pode usar o `migrate` comando para converter um pipeline do GitLab e abrir uma solicitação de pull com o fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de migração

Para migrar um pipeline do GitLab para GitHub Actions, execute o seguinte comando no seu terminal, substituindo os seguintes valores:

* `target-url`valor com a URL do repositório do GitHub
* `my-gitlab-project` pelo seu campo de dados dinâmico projeto do GitLab
* `my-gitlab-namespace` com o namespace ou grupo que você está migrando (caminho completo para subgrupos, por exemplo `my-org/my-team`)

```shell
gh actions-importer migrate gitlab --target-url https://github.com/:owner/:repo --output-dir tmp/migrate --namespace my-gitlab-namespace --project my-gitlab-project
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```shell
$ gh actions-importer migrate gitlab --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --namespace octo-org --project monas-project
[2022-08-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
[2022-08-20 22:08:20] Pull request: 'https://github.com/octo-org/octo-repo/pull/1'
```

### Como inspecionar a solicitação de pull

A saída de uma execução bem-sucedida do comando `migrate` contém um link para a nova solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório.

Alguns elementos importantes da solicitação de pull incluem:

* Na descrição da solicitação de pull, uma seção chamada **Etapas manuais**, que lista as etapas que você precisa concluir manualmente para concluir a migração dos pipelines para o GitHub Actions. Por exemplo, esta seção pode solicitar a criação dos segredos usados nos fluxos de trabalho.
* O arquivo de fluxos de trabalho convertido. Selecione a guia **Files changed** na pull request para ver o arquivo de fluxo de trabalho que será adicionado ao repositório do GitHub.

Quando terminar de inspecionar a pull request, você poderá mesclá-la para adicionar o fluxo de trabalho ao repositório do GitHub.

## Referência

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do GitLab.

### Usando variáveis de ambiente

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as seguintes variáveis de ambiente para se conectar à instância do GitLab:

* `GITHUB_ACCESS_TOKEN`: o personal access token (classic) usado para criar pull requests com um fluxo de trabalho convertido (requer o escopo do `workflow`).
* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).
* `GITLAB_ACCESS_TOKEN`: GitLab personal access token utilizado para visualizar recursos do GitLab.
* `GITLAB_INSTANCE_URL`: a URL da instância do GitLab.
* `NAMESPACE`: os namespaces ou grupos que contêm os pipelines do GitLab.

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Como usar argumentos opcionais

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `forecast`, `dry-run` ou `migrate`.

Por padrão, o GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--source-file-path` informa ao GitHub Actions Importer que use o caminho do arquivo de origem especificado.

Por exemplo:

```shell
gh actions-importer dry-run gitlab --output-dir output/ --namespace my-gitlab-namespace --project my-gitlab-project --source-file-path path/to/.gitlab-ci.yml
```

Para fornecer diversos arquivos de origem ao executar o subcomando `forecast`, use padrões correspondentes no valor do caminho do arquivo. O exemplo a seguir fornece a GitHub Actions Importer quaisquer arquivos de origem que correspondam ao caminho de arquivo `./tmp/previous_forecast/jobs/*.json`.

```shell
gh actions-importer forecast gitlab --output-dir output/ --namespace my-gitlab-namespace --project my-gitlab-project --source-file-path ./tmp/previous_forecast/jobs/*.json
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, o GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

O argumento `--config-file-path` também pode ser usado para especificar para qual repositório um fluxo de trabalho reutilizável convertido deve ser migrado.

##### Exemplo de auditoria

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```shell
gh actions-importer audit gitlab --output-dir path/to/output/ --namespace my-gitlab-namespace --config-file-path path/to/gitlab/config.yml
```

Para auditar uma instância do GitLab usando um arquivo de configuração, o arquivo deve estar no seguinte formato e cada valor `repository_slug` deve ser exclusivo:

```yaml
source_files:
  - repository_slug: namespace/project-name
    path: path/to/.gitlab-ci.yml
  - repository_slug: namespace/some-other-project-name
    path: path/to/.gitlab-ci.yml
```

##### Exemplo de simulação a seco

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma execução seca.

O pipeline é selecionado pela correspondência de `repository_slug` no arquivo de configuração com o valor das opções `--namespace` e `--project`. Em seguida, `path` é usado para efetuar pull do arquivo de origem especificado.

```shell
gh actions-importer dry-run gitlab --namespace my-gitlab-namespace --project my-gitlab-project-name --output-dir ./output/ --config-file-path ./path/to/gitlab/config.yml
```

##### Especificar o repositório de fluxos de trabalho reutilizáveis convertidos

GitHub Actions Importer usa o arquivo YAML fornecido para o `--config-file-path` argumento para determinar o repositório para o qual os fluxos de trabalho reutilizáveis convertidos são migrados.

Para começar, você deve executar uma auditoria sem o argumento `--config-file-path`:

```shell
gh actions-importer audit gitlab --output-dir ./output/
```

A saída desse comando conterá um arquivo nomeado `config.yml` que contém uma lista de todas as ações compostas que foram convertidas por GitHub Actions Importer. Por exemplo, o arquivo `config.yml` pode ter o seguinte conteúdo:

```yaml
reusable_workflows:
  - name: my-reusable-workflow.yml
    target_url: https://github.com/octo-org/octo-repo
    ref: main
```

Você pode usar esse arquivo para especificar a qual repositório e ref um fluxo de trabalho reutilizável ou uma ação composta deve ser adicionado. Em seguida, você pode usar o `--config-file-path` argumento para fornecer o `config.yml` arquivo para GitHub Actions Importer. Por exemplo, você pode usar esse arquivo ao executar um comando `migrate` para abrir uma solicitação de pull para cada repositório exclusivo definido no arquivo de configuração:

```shell
gh actions-importer migrate gitlab --project my-project-name --output-dir output/ --config-file-path config.yml --target-url https://github.com/my-org/my-repo
```

### Sintaxe suportada para pipelines do GitLab

A tabela a seguir mostra os tipos de propriedades que GitHub Actions Importer pode converter atualmente. Para obter mais detalhes sobre como a sintaxe de pipeline do GitLab se alinha a GitHub Actions, consulte [Migrando de CI/CD do GitLab para GitHub Actions](../manual-migrations/migrate-from-gitlab-cicd.md).

| GitLab Pipelines | GitHub Actions | Status |
| :-- | :-- | :-- |
| `after_script` | `jobs.<job_id>.steps` | Com suporte |
| `auto_cancel_pending_pipelines` | `concurrency` | Com suporte |
| `before_script` | `jobs.<job_id>.steps` | Com suporte |
| `build_timeout` ou `timeout` | `jobs.<job_id>.timeout-minutes` | Com suporte |
| `default` | Não aplicável | Com suporte |
| `image` | `jobs.<job_id>.container` | Com suporte |
| `job` | `jobs.<job_id>` | Com suporte |
| `needs` | `jobs.<job_id>.needs` | Com suporte |
| `only_allow_merge_if_pipeline_succeeds` | `on.pull_request` | Com suporte |
| `resource_group` | `jobs.<job_id>.concurrency` | Com suporte |
| `schedule` | `on.schedule` | Com suporte |
| `script` | `jobs.<job_id>.steps` | Com suporte |
| `stages` | `jobs` | Com suporte |
| `tags` | `jobs.<job_id>.runs-on` | Com suporte |
| `variables` |  |  |
| `env`, `jobs.<job_id>.env` | Com suporte |  |
| Executar pipelines para novos confirmações | `on.push` | Com suporte |
| Executar pipelines manualmente | `on.workflow_dispatch` | Com suporte |
| `environment` | `jobs.<job_id>.environment` | Suporte parcial |
| `include` | Os arquivos referenciados em uma instrução `include` são mesclados em um único grafo de trabalho antes de serem transformados. | Suporte parcial |
| `only` ou `except` | `jobs.<job_id>.if` | Suporte parcial |
| `parallel` | `jobs.<job_id>.strategy` | Suporte parcial |
| `rules` | `jobs.<job_id>.if` | Suporte parcial |
| `services` | `jobs.<job_id>.services` | Suporte parcial |
| `workflow` | `if` | Suporte parcial |

Para saber mais sobre os constructos do GitLab com suporte, confira o [repositório `github/gh-actions-importer`](https://github.com/github/gh-actions-importer/blob/main/docs/gitlab/index.md).

### Sintaxe de variáveis de ambiente

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente padrão do GitLab para o equivalente mais próximo em GitHub Actions.

| GitLab | GitHub Actions |
| :-- | :-- |
| `CI_API_V4_URL` | `${{ github.api_url }}` |
| `CI_BUILDS_DIR` | `${{ github.workspace }}` |
| `CI_COMMIT_BRANCH` | `${{ github.ref }}` |
| `CI_COMMIT_REF_NAME` | `${{ github.ref }}` |
| `CI_COMMIT_REF_SLUG` | `${{ github.ref }}` |
| `CI_COMMIT_SHA` | `${{ github.sha }}` |
| `CI_COMMIT_SHORT_SHA` | `${{ github.sha }}` |
| `CI_COMMIT_TAG` | `${{ github.ref }}` |
| `CI_JOB_ID` | `${{ github.job }}` |
| `CI_JOB_MANUAL` | `${{ github.event_name == 'workflow_dispatch' }}` |
| `CI_JOB_NAME` | `${{ github.job }}` |
| `CI_JOB_STATUS` | `${{ job.status }}` |
| `CI_JOB_URL` | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |
| `CI_JOB_TOKEN` | `${{ github.token }}` |
| `CI_NODE_INDEX` | `${{ strategy.job-index }}` |
| `CI_NODE_TOTAL` | `${{ strategy.job-total }}` |
| `CI_PIPELINE_ID` | `${{ github.repository}}/${{ github.workflow }}` |
| `CI_PIPELINE_IID` | `${{ github.workflow }}` |
| `CI_PIPELINE_SOURCE` | `${{ github.event_name }}` |
| `CI_PIPELINE_TRIGGERED` | `${{ github.actions }}` |
| `CI_PIPELINE_URL` | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |
| `CI_PROJECT_DIR` | `${{ github.workspace }}` |
| `CI_PROJECT_ID` | `${{ github.repository }}` |
| `CI_PROJECT_NAME` | `${{ github.event.repository.name }}` |
| `CI_PROJECT_NAMESPACE` | `${{ github.repository_owner }}` |
| `CI_PROJECT_PATH_SLUG` | `${{ github.repository }}` |
| `CI_PROJECT_PATH` | `${{ github.repository }}` |
| `CI_PROJECT_ROOT_NAMESPACE` | `${{ github.repository_owner }}` |
| `CI_PROJECT_TITLE` | `${{ github.event.repository.full_name }}` |
| `CI_PROJECT_URL` | `${{ github.server_url }}/${{ github.repository }}` |
| `CI_REPOSITORY_URL` | `${{ github.event.repository.clone_url }}` |
| `CI_RUNNER_EXECUTABLE_ARCH` | `${{ runner.os }}` |
| `CI_SERVER_HOST` | `${{ github.server_url }}` |
| `CI_SERVER_URL` | `${{ github.server_url }}` |
| `CI_SERVER` | `${{ github.actions }}` |
| `GITLAB_CI` | `${{ github.actions }}` |
| `GITLAB_USER_EMAIL` | `${{ github.actor }}` |
| `GITLAB_USER_ID` | `${{ github.actor }}` |
| `GITLAB_USER_LOGIN` | `${{ github.actor }}` |
| `GITLAB_USER_NAME` | `${{ github.actor }}` |
| `TRIGGER_PAYLOAD` | `${{ github.event_path }}` |
| `CI_MERGE_REQUEST_ASSIGNEES` | `${{ github.event.pull_request.assignees }}` |
| `CI_MERGE_REQUEST_ID` | `${{ github.event.pull_request.number }}` |
| `CI_MERGE_REQUEST_IID` | `${{ github.event.pull_request.number }}` |
| `CI_MERGE_REQUEST_LABELS` | `${{ github.event.pull_request.labels }}` |
| `CI_MERGE_REQUEST_MILESTONE` | `${{ github.event.pull_request.milestone }}` |
| `CI_MERGE_REQUEST_PROJECT_ID` | `${{ github.repository }}` |
| `CI_MERGE_REQUEST_PROJECT_PATH` | `${{ github.repository }}` |
| `CI_MERGE_REQUEST_PROJECT_URL` | `${{ github.server_url }}/${{ github.repository }}` |
| `CI_MERGE_REQUEST_REF_PATH` | `${{ github.ref }}` |
| `CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` | `${{ github.event.pull_request.head.ref }}` |
| `CI_MERGE_REQUEST_SOURCE_BRANCH_SHA` | `${{ github.event.pull_request.head.sha}}` |
| `CI_MERGE_REQUEST_SOURCE_PROJECT_ID` | `${{ github.event.pull_request.head.repo.full_name }}` |
| `CI_MERGE_REQUEST_SOURCE_PROJECT_PATH` | `${{ github.event.pull_request.head.repo.full_name }}` |
| `CI_MERGE_REQUEST_SOURCE_PROJECT_URL` | `${{ github.event.pull_request.head.repo.url }}` |
| `CI_MERGE_REQUEST_TARGET_BRANCH_NAME` | `${{ github.event.pull_request.base.ref }}` |
| `CI_MERGE_REQUEST_TARGET_BRANCH_SHA` | `${{ github.event.pull_request.base.sha }}` |
| `CI_MERGE_REQUEST_TITLE` | `${{ github.event.pull_request.title }}` |
| `CI_EXTERNAL_PULL_REQUEST_IID` | `${{ github.event.pull_request.number }}` |
| `CI_EXTERNAL_PULL_REQUEST_SOURCE_REPOSITORY` | `${{ github.event.pull_request.head.repo.full_name }}` |
| `CI_EXTERNAL_PULL_REQUEST_TARGET_REPOSITORY` | `${{ github.event.pull_request.base.repo.full_name }}` |
| `CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_NAME` | `${{ github.event.pull_request.head.ref }}` |
| `CI_EXTERNAL_PULL_REQUEST_SOURCE_BRANCH_SHA` | `${{ github.event.pull_request.head.sha }}` |
| `CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_NAME` | `${{ github.event.pull_request.base.ref }}` |
| `CI_EXTERNAL_PULL_REQUEST_TARGET_BRANCH_SHA` | `${{ github.event.pull_request.base.sha }}` |

## Aviso legal

Partes foram adaptadas do <https://github.com/github/gh-actions-importer/> de acordo com a licença MIT:

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
