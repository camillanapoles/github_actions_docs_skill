---
title: Migrando do CircleCI com GitHub Actions Importer
description: Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do CircleCI para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration
captured: '2026-10-11'
section: GitHub Actions
---

# Migrando do CircleCI com GitHub Actions Importer

_Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do CircleCI para GitHub Actions._

## Sobre a migração de CircleCI usando o Importador de GitHub Actions

As instruções a seguir orientarão você na configuração do seu ambiente para usar GitHub Actions Importer para migrar pipelines do CircleCI para GitHub Actions.

### Pré-requisitos

* Uma conta ou organização CircleCI com projetos e pipelines que você deseja converter em GitHub Actions fluxos de trabalho.
* Acesso para criar um token de API pessoal do CircleCI para sua conta ou sua organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
  > \[!NOTE]
  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações

Há algumas limitações ao migrar do CircleCI para GitHub Actions com GitHub Actions Importer:

* Não há suporte para o cache automático entre trabalhos de fluxos de trabalho diferentes.
* O comando `audit` só é suportado quando você usa uma conta de organização CircleCI. Os comandos `dry-run` e `migrate` podem ser usados com uma organização do CircleCI ou uma conta de usuário.

#### Tarefas manuais

Alguns constructos do CircleCI precisam ser migrados manualmente. Estão incluídos:

* Contextos
* Variáveis de ambiente de nível do projeto
* Propriedades de trabalho desconhecidas
* Orbs desconhecidos

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

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer trabalhar com o CircleCI e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   Seu token deve ter os escopos `repo` e `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um token de API pessoal do CircleCI. Para obter mais informações, confira [Como gerenciar tokens de API](https://circleci.com/docs/managing-api-tokens/#creating-a-personal-api-token) na documentação do CircleCI.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
   ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `CircleCI`, pressione <kbd>Espaço</kbd> para fazer a seleção e pressione <kbd>Enter</kbd>.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione <kbd>Enter</kbd>.
   * Para "URL base da instância do GitHub", insira pressione <kbd>Enter</kbd> para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token for CircleCI", insira o valor do token de API pessoal do CircleCI criado anteriormente e pressione <kbd>Enter</kbd>.
   * Em "URL base da instância do CircleCI", pressione <kbd>ENTER</kbd> para aceitar o valor padrão (`https://circleci.com`).
   * Em "Nome da organização do CircleCI", insira o nome da sua organização do CircleCI e pressione <kbd>ENTER</kbd>.

   Um exemplo do comando `configure` é mostrado abaixo:

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: CircleCI
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for CircleCI: ********************
   ✔ Base url of the CircleCI instance: https://circleci.com
   ✔ CircleCI organization name: mycircleciorganization
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

## Executar uma auditoria do CircleCI

Use o comando `audit` para obter uma exibição de alto nível de todos os projetos de uma organização do CircleCI.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos em uma organização do CircleCI.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria

Para executar uma auditoria de uma organização do CircleCI, execute o seguinte comando no terminal:

```shell
gh actions-importer audit circle-ci --output-dir tmp/audit
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

Você pode usar o comando `forecast` para prever o uso potencial de GitHub Actions calculando métricas de execuções de pipeline concluídas no CircleCI.

### Como executar o comando de previsão

Para executar uma previsão de uso potencial GitHub Actions , execute o comando a seguir em seu terminal. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast circle-ci --output-dir tmp/forecast_reports
```

### Como inspecionar o relatório de previsão

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.

  Essa métrica está correlacionada ao quanto você deve esperar gastar GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* ```
            As métricas de **tempo de espera** descrevem o tempo gasto por um trabalho aguardando um executor ficar disponível para executá-lo.
        ```
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Essa métrica pode ser usada para definir o número de executores que você deve configurar.

Além disso, essas métricas são definidas para cada fila de executores no CircleCI. Isso é especialmente útil se há uma combinação de executores hospedados ou auto-hospedados, ou computadores de especificação alta ou baixa, de modo que você possa ver métricas específicas para diferentes tipos de executores.

## Executar uma migração de simulação de um pipeline do CircleCI

Você pode usar o `dry-run` comando para converter um pipeline CircleCI em um fluxo de trabalho equivalente GitHub Actions . Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

Para executar uma execução seca de migração do projeto CircleCI para GitHub Actionsexecutar o comando a seguir em seu terminal, substituindo `my-circle-ci-project` pelo nome do projeto CircleCI.

```
gh actions-importer dry-run circle-ci --output-dir tmp/dry-run --circle-ci-project my-circle-ci-project
```

Você pode ver os logs da simulação e os arquivos de fluxo de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Executar uma migração de produção de um pipeline do CircleCI

Você pode usar o comando `migrate` para converter um pipeline CircleCI e abrir um pull request com o fluxo de trabalho equivalente GitHub Actions.

### Como executar o comando de migração

Para migrar um pipeline do CircleCI para GitHub Actions, execute o seguinte comando em seu terminal, substituindo o valor de `target-url` pela URL do seu repositório GitHub e `my-circle-ci-project` pelo nome do seu projeto CircleCI.

```
gh actions-importer migrate circle-ci --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --circle-ci-project my-circle-ci-project
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```
$ gh actions-importer migrate circle-ci --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --circle-ci-project my-circle-ci-project
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

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do CircleCI.

### Usando variáveis de ambiente

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as seguintes variáveis de ambiente para se conectar à instância do CircleCI:

* `GITHUB_ACCESS_TOKEN`: personal access token (classic) usado para criar pull requests com um fluxo de trabalho convertido (requer os escopos `repo` e `workflow`).
* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).
* `CIRCLE_CI_ACCESS_TOKEN`: o token de API pessoal do CircleCI usado para se autenticar com a sua instância do CircleCI.
* `CIRCLE_CI_INSTANCE_URL`: a URL da instância do CircleCI (por exemplo, `https://circleci.com`). Se a variável for deixada sem definição, `https://circleci.com` será usado como o valor padrão.
* `CIRCLE_CI_ORGANIZATION`: o nome da organização da instância do CircleCI.
* `CIRCLE_CI_PROVIDER`: o local em que o arquivo de origem do pipeline é armazenado (como `github`). Atualmente, há suporte apenas para GitHub.
* `CIRCLE_CI_SOURCE_GITHUB_ACCESS_TOKEN` (Opcional): o personal access token (classic) usado para autenticar com sua instância de origem GitHub (requer escopo `repo`). Se ele não for fornecido, o valor de `GITHUB_ACCESS_TOKEN` será usado.
* `CIRCLE_CI_SOURCE_GITHUB_INSTANCE_URL` (Opcional): a URL para a instância de origem GitHub . Se ele não for fornecido, o valor de `GITHUB_INSTANCE_URL` será usado.

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Argumentos opcionais

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `forecast`, `dry-run` ou `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--source-file-path` indica a GitHub Actions Importer usar o caminho do arquivo de origem especificado.

Por exemplo:

```
gh actions-importer dry-run circle-ci --output-dir ./output/ --source-file-path ./path/to/.circleci/config.yml
```

Caso você deseje fornecer vários arquivos de origem ao executar o subcomando `forecast`, use padrões correspondentes no valor do caminho do arquivo. Por exemplo, `gh forecast --source-file-path ./tmp/previous_forecast/jobs/*.json` fornece todos os GitHub Actions Importer arquivos de origem que correspondam ao caminho do `./tmp/previous_forecast/jobs/*.json` arquivo.

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

O argumento `--config-file-path` também pode ser usado para especificar para qual repositório uma ação composta convertida deve ser migrada.

##### Exemplo de auditoria

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```
gh actions-importer audit circle-ci --output-dir ./output/ --config-file-path ./path/to/circle-ci/config.yml
```

Para auditar uma instância do CircleCI usando um arquivo de configuração, o arquivo de configuração precisa estar no seguinte formato e cada `repository_slug` precisa ser exclusivo:

```
source_files:
  - repository_slug: circle-org-name/circle-project-name
    path: path/to/.circleci/config.yml
  - repository_slug: circle-org-name/some-other-circle-project-name
    path: path/to/.circleci/config.yml
```

##### Exemplo de simulação a seco

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma execução seca.

O pipeline é selecionado pela correspondência do `repository_slug` no arquivo de configuração com o valor das opções `--circle-ci-organization` e `--circle-ci-project`. Em seguida, o `path` é usado para efetuar pull do arquivo de origem especificado.

```
gh actions-importer dry-run circle-ci --circle-ci-project circle-org-name/circle-project-name --output-dir ./output/ --config-file-path ./path/to/circle-ci/config.yml
```

##### Especificar o repositório de ações compostas convertidas

GitHub Actions Importer usa o arquivo YAML fornecido para o `--config-file-path` argumento para determinar o repositório para o qual as ações compostas convertidas são migradas.

Para começar, você deve executar uma auditoria sem o argumento `--config-file-path`:

```
gh actions-importer audit circle-ci --output-dir ./output/
```

A saída desse comando conterá um arquivo nomeado `config.yml` que contém uma lista de todas as ações compostas que foram convertidas por GitHub Actions Importer. Por exemplo, o arquivo `config.yml` pode ter o seguinte conteúdo:

```
composite_actions:
  - name: my-composite-action.yml
    target_url: https://github.com/octo-org/octo-repo
    ref: main
```

Você pode usar esse arquivo para especificar a qual repositório e ref um fluxo de trabalho reutilizável ou uma ação composta deve ser adicionado. Em seguida, você pode usar o `--config-file-path` argumento para fornecer o `config.yml` arquivo para GitHub Actions Importer. Por exemplo, você pode usar esse arquivo ao executar um comando `migrate` para abrir uma solicitação de pull para cada repositório exclusivo definido no arquivo de configuração:

```
gh actions-importer migrate circle-ci --circle-ci-project my-project-name --output-dir output/ --config-file-path config.yml --target-url https://github.com/my-org/my-repo
```

#### `--include-from`

Use o argumento `--include-from` com o subcomando `audit`.

O argumento `--include-from` especifica um arquivo que contém uma lista delimitada por linhas de repositórios a serem incluídos na auditoria de uma organização do CircleCI. Todos os repositórios que não estão incluídos no arquivo são excluídos da auditoria.

Por exemplo:

```
gh actions-importer audit circle-ci --output-dir ./output/ --include-from repositories.txt
```

O arquivo fornecido para esse parâmetro precisa ser uma lista de repositórios delimitada por linhas, por exemplo:

```
repository_one
repository_two
repository_three
```

### Sintaxe com suporte para pipelines do CircleCI

A tabela a seguir mostra o tipo de propriedades que GitHub Actions Importer atualmente é capaz de converter.

| Pipelines do CircleCI | GitHub Actions                                                                        | Status              |
| :-------------------- | :------------------------------------------------------------------------------------ | :------------------ |
| gatilhos cron         | <ul><li>`on.schedule`</li></ul>                                                       | Com suporte         |
| ambiente              | <ul><li>`env`</li><li>`jobs.<job_id>.env`</li><li>`jobs.<job_id>.steps.env`</li></ul> | Com suporte         |
| executors             | <ul><li>`runs-on`</li></ul>                                                           | Com suporte         |
| trabalhos             | <ul><li>`jobs`</li></ul>                                                              | Com suporte         |
| cargo                 | <ul><li>`jobs.<job_id>`</li><li>`jobs.<job_id>.name`</li></ul>                        | Com suporte         |
| matriz                | <ul><li>`jobs.<job_id>.strategy`</li><li>`jobs.<job_id>.strategy.matrix`</li></ul>    | Com suporte         |
| parâmetros            | <ul><li>`env`</li><li>`workflow-dispatch.inputs`</li></ul>                            | Com suporte         |
| etapas                | <ul><li>`jobs.<job_id>.steps`</li></ul>                                               | Com suporte         |
| quando, a menos que   | <ul><li>`jobs.<job_id>.if`</li></ul>                                                  | Com suporte         |
| disparadores          | <ul><li>`on`</li></ul>                                                                | Com suporte         |
| executors             | <ul><li>`container`</li><li>`services`</li></ul>                                      | Com suporte parcial |
| esferas               | <ul><li>`actions`</li></ul>                                                           | Com suporte parcial |
| executors             | <ul><li>`self hosted runners`</li></ul>                                               | Sem suporte         |
| configuração          | Não aplicável                                                                         | Sem suporte         |
| versão                | Não aplicável                                                                         | Sem suporte         |

Para obter mais informações sobre os conceitos do CircleCI e os mapeamentos de orbs suportados, confira o [`github/gh-actions-importer` repositório](https://github.com/github/gh-actions-importer/blob/main/docs/circle_ci/index.md).

### Mapeamento de variáveis de ambiente

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente CircleCI padrão para o equivalente mais próximo em GitHub Actions.

| CircleCI                           | GitHub Actions                              |
| :--------------------------------- | :------------------------------------------ |
| `CI`                               | `$CI`                                       |
| `CIRCLE_BRANCH`                    | `${{ github.ref }}`                         |
| `CIRCLE_JOB`                       | `${{ github.job }}`                         |
| `CIRCLE_PR_NUMBER`                 | `${{ github.event.number }}`                |
| `CIRCLE_PR_REPONAME`               | `${{ github.repository }}`                  |
| `CIRCLE_PROJECT_REPONAME`          | `${{ github.repository }}`                  |
| `CIRCLE_SHA1`                      | `${{ github.sha }}`                         |
| `CIRCLE_TAG`                       | `${{ github.ref }}`                         |
| `CIRCLE_USERNAME`                  | `${{ github.actor }}`                       |
| `CIRCLE_WORKFLOW_ID`               | `${{ github.run_number }}`                  |
| `CIRCLE_WORKING_DIRECTORY`         | `${{ github.workspace }}`                   |
| `<< pipeline.id >>`                | `${{ github.workflow }}`                    |
| `<< pipeline.number >>`            | `${{ github.run_number }}`                  |
| `<< pipeline.project.git_url >>`   | `$GITHUB_SERVER_URL/$GITHUB_REPOSITORY`     |
| `<< pipeline.project.type >>`      | `github`                                    |
| `<< pipeline.git.tag >>`           | `${{ github.ref }}`                         |
| `<< pipeline.git.branch >>`        | `${{ github.ref }}`                         |
| `<< pipeline.git.revision >>`      | `${{ github.event.pull_request.head.sha }}` |
| `<< pipeline.git.base_revision >>` | `${{ github.event.pull_request.base.sha }}` |

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
