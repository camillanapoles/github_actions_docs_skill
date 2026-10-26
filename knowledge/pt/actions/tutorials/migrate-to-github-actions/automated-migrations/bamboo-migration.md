---
title: Migrando do Bamboo para o GitHub Actions Importer
description: Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do Bamboo para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bamboo-migration
captured: '2026-10-26'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando do Bamboo para o GitHub Actions Importer

_Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do Bamboo para GitHub Actions._

## Sobre a migração do Bamboo usando o Importador do GitHub Actions

As instruções a seguir orientarão você sobre como configurar seu ambiente para usar GitHub Actions Importer e migrar os pipelines do Bamboo para GitHub Actions.

### Pré-requisitos

* Uma conta do Bamboo ou uma organização com projetos e pipelines que você deseja converter para fluxos de trabalho do GitHub Actions.
* Versão Bamboo 7.1.1 ou superior.
* Acesso para criar um Bamboo personal access token para sua conta ou organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações

Há algumas limitações ao migrar do Bamboo para GitHub Actions com GitHub Actions Importer:

* GitHub Actions Importer depende da especificação YAML gerada pelo Bamboo Server para executar migrações. Quando o Bamboo não dá suporte à exportação de algo para YAML, as informações ausentes não são migradas.
* Não há suporte para condições de gatilho. Quando o GitHub Actions Importer encontra um gatilho com uma condição, a condição é exibida como um comentário e o gatilho é transformado sem ele.
* Os Planos do Bamboo com configurações personalizadas para armazenar artefatos não são transformados. Em vez disso, os artefatos são armazenados e recuperados usando as ações [`upload-artifact`](https://github.com/actions/upload-artifact) e [`download-artifact`](https://github.com/actions/download-artifact).
* Planos desativados devem ser desabilitados manualmente na interface do GitHub. Para saber mais, confira [Desabilitar e habilitar um fluxo de trabalho](../../../how-tos/manage-workflow-runs/disable-and-enable-workflows.md).
* Trabalhos desabilitados são transformados com uma condição `if: false` que impede a sua execução. Remova isso para reativar a tarefa.
* As tarefas desabilitadas não são transformadas porque não estão incluídas no plano exportado ao usar a API do Bamboo.
* O Bamboo fornece opções para limpar workspaces de builds após a conclusão de um build. Eles não são transformados porque supõe-se que executores hospedados no GitHub ou executores auto-hospedados efêmeros lidarão automaticamente com isso.
* As opções de detecção de build pendente não são transformadas porque não há equivalente no GitHub Actions. A opção mais próxima é `timeout-minutes` em um trabalho, que pode ser usado para definir o número máximo de minutos para permitir que um trabalho seja executado. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idtimeout-minutes).
* A rotulagem por correspondência de padrões não é transformada porque não há equivalente em GitHub Actions.
* Todos os artefatos são transformados em um `actions/upload-artifact`, independentemente de serem `shared` ou não, para que possam ser baixados de qualquer trabalho no fluxo de trabalho.
* As permissões não são transformadas porque não há equivalente adequado em GitHub Actions.
* Se a versão do Bamboo estiver entre 7.1.1 e 8.1.1, as variáveis de projeto e plano não serão migradas.

#### Tarefas manuais

Certos constructos do Bamboo devem ser migrados manualmente. Eles incluem:

* Variáveis mascaradas
* Configurações de expiração do artefato

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

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer trabalhar com Bamboo e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um personal access token do Bamboo. Para obter mais informações, consulte [Personal Access Tokens](https://confluence.atlassian.com/bamboo/personal-access-tokens-976779873.html) a documentação do Bamboo.

   Seu token deve ter as seguintes permissões, dependendo de quais recursos serão transformados.

| Tipo de recurso | Visualizar | Exibir configuração | Editar |
| :-- | :-: | :-: | :-: |
| Plano de build | (Required) | (Required) | (Required) |
| Projeto de implantação | (Required) | (Required) | (Not required) |
| Ambiente de implantação | (Required) | (Not required) | (Not required) |

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
   ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `Bamboo`, pressione `Espaço` para fazer a seleção e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token para Bamboo", insira o valor do Bamboo personal access token que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do Bamboo", insira a URL da instância do Bamboo Server ou do Bamboo Data Center e pressione `Enter`.

   Um exemplo do comando `configure` é mostrado abaixo:

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: Bamboo
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for Bamboo: ********************
   ✔ Base url of the Bamboo instance: https://bamboo.example.com
   Environment variables successfully updated.
   ```

4. No terminal, execute o comando CLI GitHub Actions Importer`update` para se conectar a GitHub PackagesContainer registry e garantir que a imagem do contêiner esteja atualizada para a versão mais recente:

            ```shell
   gh actions-importer update
   ```

   A saída do comando será parecida com a mostrada abaixo:

            ```shell
   Updating ghcr.io/actions-importer/cli:latest...
   ghcr.io/actions-importer/cli:latest up-to-date
   ```

## Executar uma auditoria do Bamboo

Você pode usar o comando `audit` para obter uma exibição de alto nível de todos os projetos em uma organização Bamboo.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos na organização Bamboo.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria

Para executar uma auditoria de uma instância do Bamboo, execute o seguinte comando no terminal:

```shell
gh actions-importer audit bamboo --output-dir tmp/audit
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

## Previsão de uso

Você pode usar o comando `forecast` para prever o uso potencial do GitHub Actions calculando as métricas direto de execuções de pipeline concluídas na instância do Bamboo.

### Como executar o comando de previsão

Para executar uma previsão de uso potencial GitHub Actions , execute o comando a seguir em seu terminal. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast bamboo --output-dir tmp/forecast_reports
```

### Previsão de um projeto

Para limitar a previsão aos ambientes de planos e implantações associados a um projeto, você pode usar a opção `--project`, em que o valor é definido como uma chave do projeto de build.

Por exemplo:

```shell
gh actions-importer forecast bamboo --project PAN --output-dir tmp/forecast_reports
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
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Essa métrica pode ser usada para

  ```
## Executar uma migração de simulação de um pipeline do Bamboo

Você pode usar o `dry-run` comando para converter um pipeline do Bamboo em um fluxo de trabalho equivalente GitHub Actions . Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

### Executar uma migração simulada para um plano de build

Para executar uma simulação da migração do plano de build do Bamboo para o GitHub Actions, execute o seguinte comando no terminal, substituindo `:my_plan_slug` pelo projeto do plano e pela chave de plano no formato `<projectKey>-<planKey>` (por exemplo: `PAN-SCRIP`).

```shell
gh actions-importer dry-run bamboo build --plan-slug :my_plan_slug --output-dir tmp/dry-run
```

### Executar uma migração simulada para um projeto de implantação

Para executar uma simulação da migração do seu projeto de implantação do Bamboo para GitHub Actions, execute o seguinte comando no terminal, substituindo `:my_deployment_project_id` pela ID do projeto de implantação que você está convertendo.

```shell
gh actions-importer dry-run bamboo deployment --deployment-project-id :my_deployment_project_id --output-dir tmp/dry-run
```

Você pode ver os logs da simulação e os arquivos de fluxo de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Executar uma migração de produção de um pipeline do Bamboo

Você pode usar o `migrate` comando para converter um pipeline do Bamboo e abrir uma solicitação de pull com o fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de migração para um plano de build

Para migrar um plano de build do Bamboo para GitHub Actions, execute o seguinte comando no terminal, substituindo o valor de `target-url` pela URL do seu repositório GitHub e o valor de `:my_plan_slug` pelo projeto e pela chave do plano no formato `<projectKey>-<planKey>`.

```shell
gh actions-importer migrate bamboo build --plan-slug :my_plan_slug --target-url :target_url --output-dir tmp/migrate
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```shell
$ gh actions-importer migrate bamboo build --plan-slug :PROJECTKEY-PLANKEY --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate
[2022-08-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
[2022-08-20 22:08:20] Pull request: 'https://github.com/octo-org/octo-repo/pull/1'
```

### Executar o comando de migração para um projeto de implantação

Para migrar um projeto de implantação do Bamboo para GitHub Actions, execute o seguinte comando no terminal, substituindo o valor de `target-url` pela URL do seu repositório GitHub e `:my_deployment_project_id` pelo ID do projeto de implantação que você está convertendo.

```shell
gh actions-importer migrate bamboo deployment --deployment-project-id :my_deployment_project_id --target-url :target_url --output-dir tmp/migrate
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```shell
$ gh actions-importer migrate bamboo deployment --deployment-project-id 123 --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate
[2023-04-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20230420-014033.log'
[2023-04-20 22:08:20] Pull request: 'https://github.com/octo-org/octo-repo/pull/1'
```

### Como inspecionar a solicitação de pull

A saída de uma execução bem-sucedida do comando `migrate` contém um link para a nova solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório.

Alguns elementos importantes da solicitação de pull incluem:

* Na descrição da solicitação de pull, uma seção chamada **Etapas manuais**, que lista as etapas que você precisa concluir manualmente para concluir a migração dos pipelines para o GitHub Actions. Por exemplo, esta seção pode solicitar a criação dos segredos usados nos fluxos de trabalho.
* O arquivo de fluxos de trabalho convertido. Selecione a guia **Files changed** na pull request para ver o arquivo de fluxo de trabalho que será adicionado ao repositório do GitHub.

Quando terminar de inspecionar a pull request, você poderá mesclá-la para adicionar o fluxo de trabalho ao repositório do GitHub.

## Referência

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do Bamboo.

### Usando variáveis de ambiente

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as seguintes variáveis de ambiente para se conectar à instância do Bamboo:

* `GITHUB_ACCESS_TOKEN`: o personal access token (classic) usado para criar pull requests com um fluxo de trabalho convertido (requer os escopos de `repo` e `workflow`).
* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).
* `BAMBOO_ACCESS_TOKEN`: o personal access token do Bamboo usado para autenticar com a instância do Bamboo.
* `BAMBOO_INSTANCE_URL`: a URL da instância do Bamboo (por exemplo, `https://bamboo.example.com`).

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Argumentos opcionais

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `dry-run` ou `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline da instância do Bamboo. O argumento `--source-file-path` informa ao GitHub Actions Importer que use o caminho do arquivo de origem especificado.

Por exemplo:

```shell
gh actions-importer dry-run bamboo build --plan-slug IN-COM -o tmp/bamboo --source-file-path ./path/to/my/bamboo/file.yml
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline da instância do Bamboo. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

##### Exemplo de auditoria

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```bash
gh actions-importer audit bamboo -o tmp/bamboo --config-file-path "./path/to/my/bamboo/config.yml"
```

Para auditar uma instância do Bamboo usando um arquivo de configuração, o arquivo de configuração precisa estar no seguinte formato e cada `repository_slug` precisa ser exclusivo:

```yaml
source_files:
  - repository_slug: IN/COM
    path: path/to/one/source/file.yml
  - repository_slug: IN/JOB
    path: path/to/another/source/file.yml
```

##### Exemplo de simulação a seco

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma execução seca.

O campo de dados dinâmico do repositório é criado usando a opção `--plan-slug` . O caminho do arquivo de origem é localizado e extraído do arquivo especificado.

```bash
gh actions-importer dry-run bamboo build --plan-slug IN-COM -o tmp/bamboo --config-file-path "./path/to/my/bamboo/config.yml"
```

### Sintaxe com suporte para pipelines do Bamboo

A tabela a seguir mostra o tipo de propriedades que GitHub Actions Importer atualmente é capaz de converter.

| Bamboo                              | GitHub Actions                                  |              Status |
|:----------------------------------|:----------------------------------------------|------------------:|
| `environments`                      | `jobs`                                          |         Com suporte |
| `environments.<environment_id>`     | `jobs.<job_id>`                                 |         Com suporte |
| `<job_id>.artifacts`                | `jobs.<job_id>.steps.actions/upload-artifact`   |         Com suporte |
| `<job_id>.artifact-subscriptions`   | `jobs.<job_id>.steps.actions/download-artifact` |         Com suporte |
| `<job_id>.docker`                   | `jobs.<job_id>.container`                       |         Com suporte |
| `<job_id>.final-tasks`              | `jobs.<job_id>.steps.if`                        |         Com suporte |
| `<job_id>.requirements`             | `jobs.<job_id>.runs-on`                         |         Com suporte |
| `<job_id>.tasks`                    | `jobs.<job_id>.steps`                           |         Com suporte |
| `<job_id>.variables`                | `jobs.<job_id>.env`                             |         Com suporte |
| `stages`                            | `jobs.<job_id>.needs`                           |         Com suporte |
| `stages.<stage_id>.final`           | `jobs.<job_id>.if`                              |         Com suporte |
| `stages.<stage_id>.jobs`            | `jobs`                                          |         Com suporte |
| `stages.<stage_id>.jobs.<job_id>`   | `jobs.<job_id>`                                 |         Com suporte |
| `stages.<stage_id>.manual`          | `jobs.<job_id>.environment`                     |         Com suporte |
| `triggers`                          | `on`                                            |         Com suporte |
| `dependencies`                      | `jobs.<job_id>.steps.<gh cli step>`             | Com suporte parcial |
| `branches`                          | Não aplicável                                   |         Sem suporte |
| `deployment.deployment-permissions` | Não aplicável                                   |         Sem suporte |
| `environment-permissions`           | Não aplicável                                   |         Sem suporte |
| `notifications`                     | Não aplicável                                   |         Sem suporte |
| `plan-permissions`                  | Não aplicável                                   |         Sem suporte |
| `release-naming`                    | Não aplicável                                   |         Sem suporte |
| `repositories`                      | Não aplicável                                   |         Sem suporte |

Para obter mais informações sobre o conceito do Bamboo e os mapeamentos de plug-in com suporte, confira o repositório [`github/gh-actions-importer`](https://github.com/github/gh-actions-importer/blob/main/docs/bamboo/index.md).

### Mapeamento de variáveis de ambiente

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente padrão do Bamboo para os equivalentes mais próximos em GitHub Actions.

| Bamboo | GitHub Actions |
| :-- | :-- |
| `bamboo.agentId` | `${{ github.runner_name }}` |
| `bamboo.agentWorkingDirectory` | `${{ github.workspace }}` |
| `bamboo.buildKey` | `${{ github.workflow }}-${{ github.job }}` |
| `bamboo.buildNumber` | `${{ github.run_id }}` |
| `bamboo.buildPlanName` | `${{ github.repository }}-${{ github.workflow }}-${{ github.job }` |
| `bamboo.buildResultKey` | `${{ github.workflow }}-${{ github.job }}-${{ github.run_id }}` |
| `bamboo.buildResultsUrl` | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |
| `bamboo.build.working.directory` | `${{ github.workspace }}` |
| `bamboo.deploy.project` | `${{ github.repository }}` |
| `bamboo.ManualBuildTriggerReason.userName` | `${{ github.actor }}` |
| `bamboo.planKey` | `${{ github.workflow }}` |
| `bamboo.planName` | `${{ github.repository }}-${{ github.workflow }}` |
| `bamboo.planRepository.branchDisplayName` | `${{ github.ref }}` |
| `bamboo.planRepository.<position>.branch` | `${{ github.ref }}` |
| `bamboo.planRepository.<position>.branchName` | `${{ github.ref }}` |
| `bamboo.planRepository.<position>.name` | `${{ github.repository }}` |
| `bamboo.planRepository.<position>.repositoryUrl` | `${{ github.server }}/${{ github.repository }}` |
| `bamboo.planRepository.<position>.revision` | `${{ github.sha }}` |
| `bamboo.planRepository.<position>.username` | `${{ github.actor}}` |
| `bamboo.repository.branch.name` | `${{ github.ref }}` |
| `bamboo.repository.git.branch` | `${{ github.ref }}` |
| `bamboo.repository.git.repositoryUrl` | `${{ github.server }}/${{ github.repository }}` |
| `bamboo.repository.pr.key` | `${{ github.event.pull_request.number }}` |
| `bamboo.repository.pr.sourceBranch` | `${{ github.event.pull_request.head.ref }}` |
| `bamboo.repository.pr.targetBranch` | `${{ github.event.pull_request.base.ref }}` |
| `bamboo.resultsUrl` | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |
| `bamboo.shortJobKey` | `${{ github.job }}` |
| `bamboo.shortJobName` | `${{ github.job }}` |
| `bamboo.shortPlanKey` | `${{ github.workflow }}` |
| `bamboo.shortPlanName` | `${{ github.workflow }}` |

!!! note
    Variáveis desconhecidas são transformadas `${{ env.<variableName> }}` e devem ser substituídas ou adicionadas `env` para a operação adequada. Por exemplo, `${bamboo.jira.baseUrl}` se tornará `${{ env.jira_baseUrl }}`.

### Variáveis do sistema

As variáveis do sistema usadas em tarefas são transformadas na variável de shell de bash equivalente e são consideradas disponíveis. Por exemplo, `${system.<variable.name>}` será transformado em `$variable_name`. Recomendamos que você verifique isso para garantir a operação adequada do fluxo de trabalho.

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
