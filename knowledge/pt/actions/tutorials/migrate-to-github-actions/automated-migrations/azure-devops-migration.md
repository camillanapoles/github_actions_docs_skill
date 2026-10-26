---
title: Migrando de Azure DevOps com o Importador de GitHub Actions
description: Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de Azure DevOps para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration
captured: '2026-10-26'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando de Azure DevOps com o Importador de GitHub Actions

_Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de Azure DevOps para GitHub Actions._

## Sobre a migração do Azure DevOps usando o Importador do GitHub Actions

As instruções a seguir orientarão você na configuração do seu ambiente para usar GitHub Actions Importer para migrar pipelines do Azure DevOps para GitHub Actions.

### Pré-requisitos

* Uma conta do Azure DevOps ou organização com projetos e pipelines que você deseja converter em fluxos de trabalho do GitHub Actions.
* Acesso para criar um Azure DevOps personal access token para sua conta ou organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações

Há algumas limitações ao migrar de Azure DevOps para GitHub Actions comGitHub Actions Importer:

* GitHub Actions Importerrequer a versão 5.0 da API Azure DevOps, disponível nos Serviços Azure DevOps ou no Azure DevOps Server 2019. Versões mais antigas de Azure DevOps Server não são compatíveis.
* Tarefas que são adicionadas implicitamente a um pipeline de Azure DevOps, como verificar o código-fonte, podem ser adicionadas a uma auditoria do GitHub Actions Importer como um nome GUID. Para localizar o nome da tarefa amigável de um GUID, use a seguinte URL: `https://dev.azure.com/:organization/_apis/distributedtask/tasks/:guid`.

#### Tarefas manuais

Determinados constructos de Azure DevOps devem ser migrados manualmente de Azure DevOps para GitHub Actions configurações. Estão incluídos:

* Segredos de organização, repositório e ambiente
* Conexões de serviço, como OIDC Connect, GitHub Apps e personal access tokens
* Tarefas desconhecidas
* Agentes auto-hospedados
* Ambientes
* Aprovações pré-implantação

Para saber mais sobre migrações manuais, confira [Migrando de Azure Pipelines para GitHub Actions](../manual-migrations/migrate-from-azure-pipelines.md).

#### Tarefas sem suporte

GitHub Actions Importer não dá suporte à migração das seguintes tarefas:

* Portões pré-implantação
* Portões pós-implantação
* Aprovações pós-implantação
* Alguns gatilhos de recurso

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

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer trabalhar com Azure DevOps e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Criar um Azure DevOps personal access token. Para obter mais informações, consulte [Usar personal access tokens](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops\&tabs=Windows#create-a-pat) na documentação do Azure DevOps. O token precisa ter os seguintes escopos:

   * Pool de agentes: `Read`
   * Construir: `Read`
   * Código: `Read`
   * Versão: `Read`
   * Conexões de serviço: `Read`
   * Grupos de tarefas: `Read`
   * Grupo de variáveis: `Read`

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
   ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `Azure DevOps`, pressione `Space` para selecioná-lo e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token para Azure DevOps", insira o valor do Azure DevOps personal access token que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância Azure DevOps", pressione `Enter` para aceitar o valor padrão (`https://dev.azure.com`).
   * Para "Azure DevOps nome da organização", insira o nome da sua organização Azure DevOps e pressione `Enter`.
   * Para "Azure DevOps nome do projeto", insira o nome do projeto Azure DevOps e pressione `Enter`.

   Um exemplo do comando `configure` é mostrado abaixo:

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: Azure DevOps
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for Azure DevOps: ***************
   ✔ Base url of the Azure DevOps instance: https://dev.azure.com
   ✔ Azure DevOps organization name: :organization
   ✔ Azure DevOps project name: :project
   Environment variables successfully updated.
   ```

4. No terminal, execute o comando CLI GitHub Actions Importer`update` para se conectar ao GitHub PackagesContainer registry e garantir que a imagem do contêiner esteja atualizada para a versão mais recente:

            ```shell
   gh actions-importer update
   ```

   A saída do comando será semelhante ao seguinte:

            ```shell
   Updating ghcr.io/actions-importer/cli:latest...
   ghcr.io/actions-importer/cli:latest up-to-date
   ```

## Executar uma auditoria de Azure DevOps

Você pode usar o comando `audit` para obter uma exibição de alto nível de todos os projetos em uma organização Azure DevOps.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos em uma organização Azure DevOps.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria

Para executar uma auditoria de uma organização Azure DevOps, execute o seguinte comando em seu terminal:

```shell
gh actions-importer audit azure-devops --output-dir tmp/audit
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

## Previsão de uso potencial GitHub Actions

Você pode usar o comando para prever o `forecast` uso potencial GitHub Actions calculando métricas de execuções de pipeline concluídas em Azure DevOps.

### Como executar o comando de previsão

Para executar uma previsão de uso potencial GitHub Actions , execute o comando a seguir em seu terminal. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast azure-devops --output-dir tmp/forecast_reports
```

### Como inspecionar o relatório de previsão

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.

  Essa métrica está correlacionada ao quanto você deve esperar gastar no GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* ```
            As métricas de **tempo de espera** descrevem o tempo gasto por um trabalho aguardando um executor ficar disponível para executá-lo.
        ```
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Esta métrica pode ser usada para definir o número de executores que você deve configurar.

Além disso, essas métricas são definidas para cada fila de corredores em Azure DevOps. Isso é especialmente útil quando há uma combinação de executores hospedados ou auto-hospedados ou quando há computadores de especificação alta ou baixa, a fim de ver métricas específicas para diferentes tipos de executores.

  ```
## Realizar uma simulação de migração

Você pode usar o `dry-run` comando para converter um pipeline de Azure DevOps em um fluxo de trabalho equivalenteGitHub Actions. Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

### Como executar o comando de 'dry-run' para um pipeline de build

Para executar uma simulação de migração do pipeline de build do Azure DevOps para o GitHub Actions, execute o comando a seguir no terminal, substituindo `pipeline_id` pela ID do pipeline que você está convertendo.

```shell
gh actions-importer dry-run azure-devops pipeline --pipeline-id :pipeline_id --output-dir tmp/dry-run
```

É possível ver os logs da simulação e os arquivos de fluxos de trabalho convertidos no diretório de saída especificado.

### Como executar o comando de simulação para um pipeline de lançamento

Para executar uma execução seca de migração para o pipeline GitHub Actionsde lançamento do Azure DevOps, execute o seguinte comando em seu terminal, substituindo `pipeline_id` pela ID do pipeline que você está convertendo.

```shell
gh actions-importer dry-run azure-devops release --pipeline-id :pipeline_id --output-dir tmp/dry-run
```

É possível ver os logs da simulação e os arquivos de fluxos de trabalho convertidos no diretório de saída especificado.

## Executar uma migração de produção

Você pode usar o comando `migrate` para converter um pipeline do Azure DevOps e abrir uma pull request com o fluxo de trabalho GitHub Actions equivalente.

### Como executar o comando de migração para um pipeline de build

Para migrar um pipeline de build do Azure DevOps para GitHub Actions, execute o seguinte comando no seu terminal, substituindo o valor de `target-url` pela URL do seu repositório do GitHub, e `pipeline_id` pelo ID do pipeline que você está convertendo.

```shell
gh actions-importer migrate azure-devops pipeline --pipeline-id :pipeline_id --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate
```

A saída do comando inclui a URL da solicitação de pull que adiciona o fluxo de trabalho convertido ao repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```shell
$ gh actions-importer migrate azure-devops pipeline --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --azure-devops-project my-azure-devops-project
[2022-08-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
[2022-08-20 22:08:20] Pull request: 'https://github.com/octo-org/octo-repo/pull/1'
```

### Como executar o comando de migração para um pipeline de release

Para migrar um pipeline de release do Azure DevOps para GitHub Actions, execute o seguinte comando no terminal, substituindo o valor de `target-url` pela URL do seu repositório GitHub e `pipeline_id` pelo ID do pipeline que você está convertendo.

```shell
gh actions-importer migrate azure-devops release --pipeline-id :pipeline_id --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate
```

A saída do comando inclui a URL da solicitação de pull que adiciona o fluxo de trabalho convertido ao repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```shell
$ gh actions-importer migrate azure-devops release --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --azure-devops-project my-azure-devops-project
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

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe suportada ao usar GitHub Actions Importer para migrar do Azure DevOps.

### Variáveis de ambiente da configuração

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importerusa as seguintes variáveis de ambiente para se conectar à instância de Azure DevOps:

* `GITHUB_ACCESS_TOKEN`: o personal access token (classic) usado para criar pull requests com um fluxo de trabalho convertido (requer o escopo do `workflow`).
* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).
* `AZURE_DEVOPS_ACCESS_TOKEN`: o personal access token usado para autenticar com sua instância de Azure DevOps. Esse token exige os seguintes escopos:
  * Construir: `Read`
  * Pools de agentes: `Read`
  * Código: `Read`
  * Versão: `Read`
  * Conexões de serviço: `Read`
  * Grupos de tarefas: `Read`
  * Grupo de variáveis: `Read`
* `AZURE_DEVOPS_PROJECT`: O nome ou GUID do projeto a ser usado ao migrar um pipeline. Caso você deseje executar uma auditoria em todos os projetos, isso é opcional.
* `AZURE_DEVOPS_ORGANIZATION`: o nome da organização de sua instância de Azure DevOps.
* `AZURE_DEVOPS_INSTANCE_URL`: a URL para a instância de Azure DevOps, como `https://dev.azure.com`.

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Argumentos opcionais

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `forecast`, `dry-run` ou `migrate`.

Por padrão, o GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--source-file-path` informa ao GitHub Actions Importer que use o caminho do arquivo de origem especificado.

Por exemplo:

```shell
gh actions-importer dry-run azure-devops pipeline --output-dir ./output/ --source-file-path ./path/to/azure_devops/pipeline.yml
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, o GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

O argumento `--config-file-path` também pode ser usado para especificar para qual repositório um fluxo de trabalho reutilizável convertido ou uma ação composta deve ser migrada.

##### Exemplo de auditoria

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma auditoria.

```shell
gh actions-importer audit azure-devops pipeline --output-dir ./output/ --config-file-path ./path/to/azure_devops/config.yml
```

Para auditar uma instância Azure DevOps usando um arquivo de configuração, o arquivo de configuração deve estar no seguinte formato e cada `repository_slug` deve ser exclusivo:

```yaml
source_files:
  - repository_slug: azdo-project/1
    path: file.yml
  - repository_slug: azdo-project/2
    paths: path.yml
```

Você pode gerar o `repository_slug` para um pipeline combinando o nome da organização Azure DevOps, o nome do projeto e a ID do pipeline. Por exemplo, `my-organization-name/my-project-name/42`.

##### Exemplo de simulação a seco

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma execução seca.

O pipeline é selecionado pela correspondência do `repository_slug` no arquivo de configuração com o valor das opções `--azure-devops-organization` e `--azure-devops-project`. Em seguida, `path` é usado para efetuar pull do arquivo de origem especificado.

```shell
gh actions-importer dry-run azure-devops pipeline --output-dir ./output/ --config-file-path ./path/to/azure_devops/config.yml
```

##### Especificar o repositório de fluxos de trabalho reutilizáveis convertidos e ações compostas

GitHub Actions Importer usa o arquivo YAML fornecido para o `--config-file-path` argumento para determinar o repositório para o qual os fluxos de trabalho reutilizáveis convertidos e as ações compostas são migrados.

Para começar, você deve executar uma auditoria sem o argumento `--config-file-path`:

```shell
gh actions-importer audit azure-devops --output-dir ./output/
```

A saída desse comando conterá um arquivo nomeado `config.yml` que contém uma lista de todos os fluxos de trabalho reutilizáveis e ações compostas que foram convertidas por GitHub Actions Importer. Por exemplo, o arquivo `config.yml` pode ter o seguinte conteúdo:

```yaml
reusable_workflows:
  - name: my-reusable-workflow.yml
    target_url: https://github.com/octo-org/octo-repo
    ref: main

composite_actions:
  - name: my-composite-action.yml
    target_url: https://github.com/octo-org/octo-repo
    ref: main
```

Você pode usar esse arquivo para especificar a qual repositório e ref um fluxo de trabalho reutilizável ou uma ação composta deve ser adicionado. Em seguida, você pode usar o `--config-file-path` argumento para fornecer o `config.yml` arquivo para GitHub Actions Importer. Por exemplo, você pode usar esse arquivo ao executar um comando `migrate` para abrir uma solicitação de pull para cada repositório exclusivo definido no arquivo de configuração:

```shell
gh actions-importer migrate azure-devops pipeline --config-file-path config.yml --target-url https://github.com/my-org/my-repo
```

### Sintaxe suportada para pipelines do Azure DevOps

A tabela a seguir mostra o tipo de propriedades que GitHub Actions Importer atualmente é capaz de converter.

| Azure Pipelines | GitHub Actions | Status |
| :-- | :-- | :-- |
| condição | <ul><li>`jobs.<job_id>.if`</li><li>`jobs.<job_id>.steps[*].if`</li></ul> | Com suporte |
| contêiner | <ul><li>`jobs.<job_id>.container`</li><li>`jobs.<job_id>.name`</li></ul> | Com suporte |
| integração contínua | <ul><li>`on.<push>.<branches>`</li><li>`on.<push>.<tags>`</li><li>`on.<push>.paths`</li></ul> | Com suporte |
| cargo | <ul><li>`jobs.<job_id>`</li></ul> | Com suporte |
| solicitação de pull | <ul><li>`on.<pull_request>.<branches>`</li><li>`on.<pull_request>.paths`</li></ul> | Com suporte |
| fase | <ul><li>`jobs`</li></ul> | Com suporte |
| etapas | <ul><li>`jobs.<job_id>.steps`</li></ul> | Com suporte |
| estratégia | <ul><li>`jobs.<job_id>.strategy.fail-fast`</li><li>`jobs.<job_id>.strategy.max-parallel`</li><li>`jobs.<job_id>.strategy.matrix`</li></ul> | Com suporte |
| timeoutInMinutes | <ul><li>`jobs.<job_id>.timeout-minutes`</li></ul> | Com suporte |
| variáveis | <ul><li>`env`</li><li>`jobs.<job_id>.env`</li><li>`jobs.<job_id>.steps.env`</li></ul> | Com suporte |
| implantação manual | <ul><li>`jobs.<job_id>.environment`</li></ul> | Suporte parcial |
| pool | <ul><li>`runners`</li><li>`self hosted runners`</li></ul> | Suporte parcial |
| serviços | <ul><li>`jobs.<job_id>.services`</li></ul> | Suporte parcial |
| estratégia | <ul><li>`jobs.<job_id>.strategy`</li></ul> | Suporte parcial |
| disparadores | <ul><li>`on`</li></ul> | Suporte parcial |
| solicitação de pull | <ul><li>`on.<pull_request>.<tags>`</li></ul> | Sem suporte |
| schedules | <ul><li>`on.schedule`</li><li>`on.workflow_run`</li></ul> | Sem suporte |
| disparadores | <ul><li>`on.<event_name>.types`</li></ul> | Sem suporte |

Para obter mais informações sobre tarefas de Azure DevOps com suporte, consulte o [`github/gh-actions-importer` repositório](https://github.com/github/gh-actions-importer/blob/main/docs/azure_devops/index.md).

### Mapeamento de variáveis de ambiente

GitHub Actions Importerusa o mapeamento na tabela abaixo para converter variáveis de ambiente padrão Azure DevOps para o equivalente mais próximo em GitHub Actions.

| Azure Pipelines                             | GitHub Actions                                      |
|:------------------------------------------|:--------------------------------------------------|
| `$(Agent.BuildDirectory)`                   | `${{ runner.workspace }}`                           |
| `$(Agent.HomeDirectory)`                    | `${{ env.HOME }}`                                   |
| `$(Agent.JobName)`                          | `${{ github.job }}`                                 |
| `$(Agent.OS)`                               | `${{ runner.os }}`                                  |
| `$(Agent.ReleaseDirectory)`                 | `${{ github.workspace}}`                            |
| `$(Agent.RootDirectory)`                    | `${{ github.workspace }}`                           |
| `$(Agent.ToolsDirectory)`                   | `${{ runner.tool_cache }}`                          |
| `$(Agent.WorkFolder)`                       | `${{ github.workspace }}`                           |
| `$(Build.ArtifactStagingDirectory)`         | `${{ runner.temp }}`                                |
| `$(Build.BinariesDirectory)`                | `${{ github.workspace }}`                           |
| `$(Build.BuildId)`                          | `${{ github.run_id }}`                              |
| `$(Build.BuildNumber)`                      | `${{ github.run_number }}`                          |
| `$(Build.DefinitionId)`                     | `${{ github.workflow }}`                            |
| `$(Build.DefinitionName)`                   | `${{ github.workflow }}`                            |
| `$(Build.PullRequest.TargetBranch)`         | `${{ github.base_ref }}`                            |
| `$(Build.PullRequest.TargetBranch.Name)`    | `${{ github.base_ref }}`                            |
| `$(Build.QueuedBy)`                         | `${{ github.actor }}`                               |
| `$(Build.Reason)`                           | `${{ github.event_name }}`                          |
| `$(Build.Repository.LocalPath)`             | `${{ github.workspace }}`                           |
| `$(Build.Repository.Name)`                  | `${{ github.repository }}`                          |
| `$(Build.Repository.Provider)`              | `GitHub`                                            |
| `$(Build.Repository.Uri)`                   | `${{ github.server.url }}/${{ github.repository }}` |
| `$(Build.RequestedFor)`                     | `${{ github.actor }}`                               |
| `$(Build.SourceBranch)`                     | `${{ github.ref }}`                                 |
| `$(Build.SourceBranchName)`                 | `${{ github.ref }}`                                 |
| `$(Build.SourceVersion)`                    | `${{ github.sha }}`                                 |
| `$(Build.SourcesDirectory)`                 | `${{ github.workspace }}`                           |
| `$(Build.StagingDirectory)`                 | `${{ runner.temp }}`                                |
| `$(Pipeline.Workspace)`                     | `${{ runner.workspace }}`                           |
| `$(Release.DefinitionEnvironmentId)`        | `${{ github.job }}`                                 |
| `$(Release.DefinitionId)`                   | `${{ github.workflow }}`                            |
| `$(Release.DefinitionName)`                 | `${{ github.workflow }}`                            |
| `$(Release.Deployment.RequestedFor)`        | `${{ github.actor }}`                               |
| `$(Release.DeploymentID)`                   | `${{ github.run_id }}`                              |
| `$(Release.EnvironmentId)`                  | `${{ github.job }}`                                 |
| `$(Release.EnvironmentName)`                | `${{ github.job }}`                                 |
| `$(Release.Reason)`                         | `${{ github.event_name }}`                          |
| `$(Release.RequestedFor)`                   | `${{ github.actor }}`                               |
| `$(System.ArtifactsDirectory)`              | `${{ github.workspace }}`                           |
| `$(System.DefaultWorkingDirectory)`         | `${{ github.workspace }}`                           |
| `$(System.HostType)`                        | `build`                                             |
| `$(System.JobId)`                           | `${{ github.job }}`                                 |
| `$(System.JobName)`                         | `${{ github.job }}`                                 |
| `$(System.PullRequest.PullRequestId)`       | `${{ github.event.number }}`                        |
| `$(System.PullRequest.PullRequestNumber)`   | `${{ github.event.number }}`                        |
| `$(System.PullRequest.SourceBranch)`        | `${{ github.ref }}`                                 |
| `$(System.PullRequest.SourceRepositoryUri)` | `${{ github.server.url }}/${{ github.repository }}` |
| `$(System.PullRequest.TargetBranch)`        | `${{ github.event.base.ref }}`                      |
| `$(System.PullRequest.TargetBranchName)`    | `${{ github.event.base.ref }}`                      |
| `$(System.StageAttempt)`                    | `${{ github.run_number }}`                          |
| `$(System.TeamFoundationCollectionUri)`     | `${{ github.server.url }}/${{ github.repository }}` |
| `$(System.WorkFolder)`                      | `${{ github.workspace }}`                           |

### Modelos

Você pode transformar modelos de Azure DevOps com GitHub Actions Importer.

#### Limitações

GitHub Actions Importeré capaz de transformar modelos Azure DevOps com algumas limitações.

* Os modelos do Azure DevOps usados sob as chaves `stages`, `deployments` e `jobs` são convertidos em fluxos de trabalho reutilizáveis em GitHub Actions. Para saber mais, confira [Reutilizar fluxos de trabalho](../../../how-tos/reuse-automations/reuse-workflows.md).
* Modelos do Azure DevOps usados na chave `steps` são convertidos em ações compostas. Para saber mais, confira [Criar uma ação composta](../../create-actions/create-a-composite-action.md).
* Se você tiver atualmente modelos de trabalho que fazem referência a outros modelos de trabalho, GitHub Actions Importer converterá os modelos em fluxos de trabalho reutilizáveis. Como os fluxos de trabalho reutilizáveis não podem referenciar outros fluxos de trabalho reutilizáveis, essa sintaxe é inválida em GitHub Actions. Você precisa corrigir manualmente os fluxos de trabalho aninhados reutilizáveis.
* Se um modelo fizer referência a uma organização ou GitHub repositório Azure DevOps externo, você deverá usar a opção `--credentials-file` para fornecer credenciais para acessar esse modelo. Para saber mais, confira [Argumentos e configurações complementares](../../../reference/github-actions-importer/supplemental-arguments-and-settings.md#using-a-credentials-file-for-authentication).
* Você pode gerar o YAML dinamicamente usando expressões `each` com as seguintes advertências:
  * Não há suporte para blocos `each` aninhados, e eles fazem com que o bloco pai `each` não tenha suporte.
  * `each` e as condições `if` contidas são avaliadas durante a transformação, pois GitHub Actions não oferece suporte a esse estilo de inserção.
  * Não há suporte para blocos `elseif`. Se essa funcionalidade for necessária, você precisará corrigi-las manualmente.
  * Há suporte para blocos `if` aninhados, mas não há suporte para blocos `if/elseif/else` aninhados em uma condição `if`.
  * não há suporte para blocos de `if` que usam variáveis de Azure DevOps predefinidas.

#### Modelos com suporte

GitHub Actions Importer dá suporte aos modelos listados na tabela abaixo.

| Azure Pipelines | GitHub Actions | Status |
| :-- | :-- | --: |
| Estendendo a partir de um modelo | `Reusable workflow` | Com suporte |
| Modelos de trabalho | `Reusable workflow` | Com suporte |
| Modelos de etapas | `Reusable workflow` | Com suporte |
| Modelos de etapa | `Composite action` | Com suporte |
| Grupos de tarefas no editor clássico | Varia | Com suporte |
| Modelos em uma organização, projeto ou repositório de Azure DevOps diferente | Varia | Com suporte |
| Modelos em um repositório GitHub | Varia | Com suporte |
| Modelos de variável | `env` | Com suporte |
| Inserção condicional | Condições `if` no trabalho/nas etapas | Suporte parcial |
| Inserção iterativa | Não aplicável | Suporte parcial |
| Modelos com parâmetros | Varia | Suporte parcial |

#### Nomes de caminho de arquivo de modelo

GitHub Actions Importer pode extrair modelos com caminhos de arquivo relativos ou dinâmicos com variável, parâmetro e expressões iterativas no nome do arquivo. No entanto, é preciso haver um conjunto de valores padrão.

##### Exemplo de nome de caminho de arquivo variável

```yaml
```
# File: azure-pipelines.yml
variables:
- template: 'templates/vars.yml'

steps:
- template: "./templates/$"
```

```
```
# File: templates/vars.yml
variables:
  one: 'simple_step.yml'
```

```
##### Exemplo de nome do caminho de arquivo de parâmetro

```
parameters:
- name: template
  type: string
  default: simple_step.yml

steps:
- template: "./templates/${{ parameters.template }}"
```

##### Exemplo de nome do caminho de arquivo iterativo

```
parameters:
- name: steps
  type: object
  default:
  - build_step
  - release_step
steps:
- ${{ each step in parameters.steps }}:
    - template: "$-variables.yml"
```

#### Parâmetros de modelo

GitHub Actions Importer dá suporte aos parâmetros listados na tabela abaixo.

| Azure Pipelines                            | GitHub Actions   | Status          |
| :----------------------------------------- | :--------------- | :-------------- |
| cadeia                                     | `inputs.string`  | Com suporte     |
| número                                     | `inputs.number`  | Com suporte     |
| booleano                                   | `inputs.boolean` | Com suporte     |
| objeto                                     |                  |                 |
| `inputs.string` com a expressão `fromJSON` | Suporte parcial  |                 |
| etapa                                      | `step`           | Suporte parcial |
| stepList                                   | `step`           | Suporte parcial |
| cargo                                      | `job`            | Suporte parcial |
| lista de trabalhos                         | `job`            | Suporte parcial |
| implantação                                | `job`            | Suporte parcial |
| deploymentList                             | `job`            | Suporte parcial |
| fase                                       | `job`            | Suporte parcial |
| listaDeEtapas                              | `job`            | Suporte parcial |

!!! note
    Um modelo usado na chave `step` com esse tipo de parâmetro só será serializado como uma ação composta se as etapas forem usadas no início ou no final das etapas do modelo. Um modelo usado nas chaves `stage`, `deployment` e `job` com esse tipo de parâmetro não é transformado em um fluxo de trabalho reutilizável e é serializado como um fluxo de trabalho independente.

## Aviso legal

Partes foram adaptadas do <https://github.com/github/gh-actions-importer/> de acordo com a licença MIT:

```
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
