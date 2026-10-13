---
title: Migrando do Jenkins com o Importador de GitHub Actions
description: Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Jenkins para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/jenkins-migration
captured: '2026-10-11'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando do Jenkins com o Importador de GitHub Actions { #migrating-from-jenkins-with-github-actions-importer }

_Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Jenkins para GitHub Actions._

## Sobre a migração a partir do Jenkins com o Importador de GitHub Actions { #about-migrating-from-jenkins-with-github-actions-importer }

As instruções a seguir orientarão você na configuração do ambiente a ser usado GitHub Actions Importer para migrar pipelines do Jenkins para GitHub Actions.

### Pré-requisitos { #prerequisites }

* Uma conta ou organização jenkins com pipelines e trabalhos que você deseja converter em GitHub Actions fluxos de trabalho.
* Acesso para criar um token de API pessoal do Jenkins para sua conta ou sua organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações { #limitations }

Há algumas limitações ao migrar do Jenkins para GitHub Actions com GitHub Actions Importer. Por exemplo, você precisa migrar os seguintes constructos manualmente:

* Ferramentas de build obrigatórias
* Pipelines roteirizadas
* Segredos
* Executores auto-hospedados
* Plug-ins desconhecidos

Para saber mais sobre migrações manuais, confira [Migrando do Jenkins para o GitHub Actions](../manual-migrations/migrate-from-jenkins.md).

## Instalando a extensão da GitHub Actions Importer CLI { #installing-the-github-actions-importer-cli-extension }

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

## Como configurar credenciais { #configuring-credentials }

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer trabalhar com Jenkins e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um token de API do Jenkins. Para obter mais informações, confira [Como autenticar clientes com script](https://www.jenkins.io/doc/book/system-administration/authenticating-scripted-clients/) na documentação do Jenkins.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
            ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `Jenkins`, pressione `Espaço` para fazer a seleção e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token for Jenkins", insira o valor do token de API pessoal do Jenkins criado anteriormente e pressione `Enter`.
   * Em "Nome de usuário do Jenkins", insira seu nome de usuário do Jenkins e pressione `ENTER`.
   * Em "URL base da instância do Jenkins", insira a URL da instância do Jenkins e pressione `ENTER`.

   Um exemplo do comando `configure` é mostrado abaixo:

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: Jenkins
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for Jenkins: ***************
   ✔ Username of Jenkins user: admin
   ✔ Base url of the Jenkins instance: https://localhost
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

## Executar uma auditoria do Jenkins { #perform-an-audit-of-jenkins }

Use o comando `audit` para obter uma exibição de alto nível de todos os pipelines de um servidor do Jenkins.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos em um servidor do Jenkins.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria { #running-the-audit-command }

Para executar uma auditoria de um servidor do Jenkins, execute o seguinte comando no terminal:

```shell
gh actions-importer audit jenkins --output-dir tmp/audit
```

### Como inspecionar os resultados da auditoria { #inspecting-the-audit-results }

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

#### Etapas de compilação { #build-steps }

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

#### Tarefas manuais { #manual-tasks }

A seção "Tarefas manuais" contém uma visão geral das tarefas que GitHub Actions Importer não podem ser concluídas automaticamente e que você deve concluir manualmente.

Veja abaixo alguns termos importantes que podem aparecer na seção "Tarefas manuais":

* Um **segredo** é um segredo no nível do repositório ou da organização que é usado nos pipelines convertidos. Esses segredos devem ser criados manualmente no GitHub Actions para que esses pipelines funcionem corretamente. Para saber mais, confira [Usar segredos em ações do GitHub](../../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).
* Um **executor auto-hospedado refere-se** a um rótulo de um executor que é referenciado em um pipeline convertido que não é um GitHubexecutor hospedado. Será necessário definir manualmente esses executores para que os pipelines funcionem de maneira correta.

#### Arquivos { #files }

A seção final do relatório de auditoria fornece um manifesto de todos os arquivos que foram gravados em disco durante a auditoria.

Cada arquivo de pipeline tem diversos arquivos incluídos na auditoria, incluindo:

* O pipeline original como ele foi definido em GitHub.
* Todas as respostas de rede usadas para converter o pipeline.
* O arquivo de fluxo de trabalho convertido.
* Rastros de pilha que podem ser usados para solucionar problemas em uma falha na conversão de um pipeline.

Além disso, o arquivo `workflow_usage.csv` contém uma lista separada por vírgula de todas as ações, todos os segredos e todos os executores usados pelos pipelines convertidos com sucesso. Isso pode ser útil para determinar quais fluxos de trabalho usam quais ações, segredos ou executores e para executar revisões de segurança.

## Prever o uso potencial do executor de compilação { #forecast-potential-build-runner-usage }

Você pode usar o comando para prever o `forecast` uso potencial GitHub Actions calculando métricas de execuções de pipeline concluídas no servidor Jenkins.

### Pré-requisitos para executar o comando de previsão { #prerequisites-for-running-the-forecast-command }

Para executar o comando `forecast` em uma instância do Jenkins, você precisa instalar o [ plug-in `paginated-builds`](https://plugins.jenkins.io/paginated-builds) no servidor do Jenkins. Esse plug-in permite recuperar com eficiência dados históricos de build para trabalhos GitHub Actions Importer que têm um grande número de builds. Como o Jenkins não fornece um método para recuperar dados de build paginados, o uso desse plug-in impede tempos limite do servidor do Jenkins que possam ocorrer durante a busca de um grande volume de dados históricos. O plugin `paginated-builds` é de código aberto e expõe um endpoint da API REST para buscar dados de compilação em páginas, em vez de tudo de uma vez.

Para instalar o plug-in `paginated-builds`:

1. Na sua instância do Jenkins, navegue até `https://<your-jenkins-instance>/pluginManager/available`.
2. Procure o plug-in `paginated-builds`.
3. Marque a caixa à esquerda e selecione **Instalar sem reiniciar**.

### Como executar o comando de previsão { #running-the-forecast-command }

Para executar uma previsão de potencial GitHub Actions, execute o comando a seguir em seu terminal. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast jenkins --output-dir tmp/forecast
```

### Como inspecionar o relatório de previsão { #inspecting-the-forecast-report }

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.
  * Essa métrica está correlacionada ao quanto você deve esperar gastar GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* ```
            As métricas de **tempo de espera** descrevem o tempo gasto por um trabalho aguardando um executor ficar disponível para executá-lo.
        ```
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Essa métrica pode ser usada para definir o número de executores que você deve configurar.

Além disso, essas métricas são definidas para cada fila de executores no Jenkins. Isso é especialmente útil se há uma combinação de executores hospedados ou auto-hospedados, ou computadores de especificação alta ou baixa, de modo que você possa ver métricas específicas para diferentes tipos de executores.

        ```
## Executar uma migração de simulação de um pipeline do Jenkins { #perform-a-dry-run-migration-of-a-jenkins-pipeline }

Você pode usar o `dry-run` comando para converter um pipeline jenkins em seu fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de simulação { #running-the-dry-run-command }

Você pode usar o `dry-run` comando para converter um pipeline jenkins em um fluxo de trabalho equivalente GitHub Actions . Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

Para executar uma execução seca de migração dos pipelines do Jenkins para GitHub Actionsexecutar o comando a seguir no terminal, substituindo `my-jenkins-project` pela URL do trabalho do Jenkins.

```
gh actions-importer dry-run jenkins --source-url my-jenkins-project --output-dir tmp/dry-run
```

### Como inspecionar os fluxos de trabalho convertidos { #inspecting-the-converted-workflows }

Você pode ver os logs da simulação e os arquivos de fluxo de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Executar uma migração de produção de um pipeline do Jenkins { #perform-a-production-migration-of-a-jenkins-pipeline }

Você pode usar o `migrate` comando para converter um pipeline do Jenkins e abrir uma solicitação de pull com o fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de migração { #running-the-migrate-command }

Para migrar um pipeline do Jenkins, GitHub Actionsexecute o seguinte comando em seu terminal, substituindo o `target-url` valor pela URL do repositório GitHub e `my-jenkins-project` pela URL do trabalho do Jenkins.

```
gh actions-importer migrate jenkins --target-url https://github.com/:owner/:repo --output-dir tmp/migrate --source-url my-jenkins-project
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```
$ gh actions-importer migrate jenkins --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --source-url http://localhost:8080/job/monas_dev_work/job/monas_freestyle
[2022-08-20 22:08:20] Logs: 'tmp/migrate/log/actions-importer-20220916-014033.log'
[2022-08-20 22:08:20] Pull request: 'https://github.com/octo-org/octo-repo/pull/1'
```

### Como inspecionar a solicitação de pull { #inspecting-the-pull-request }

A saída de uma execução bem-sucedida do comando `migrate` contém um link para a nova solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório.

Alguns elementos importantes da solicitação de pull incluem:

* Na descrição da solicitação de pull, uma seção chamada **Etapas manuais**, que lista as etapas que você precisa concluir manualmente para concluir a migração dos pipelines para o GitHub Actions. Por exemplo, esta seção pode solicitar a criação dos segredos usados nos fluxos de trabalho.
* O arquivo de fluxos de trabalho convertido. Selecione a guia **Files changed** na pull request para ver o arquivo de fluxo de trabalho que será adicionado ao repositório do GitHub.

Quando terminar de inspecionar a pull request, você poderá mesclá-la para adicionar o fluxo de trabalho ao repositório do GitHub.

## Referência { #reference }

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do Jenkins.

### Usando variáveis de ambiente { #using-environment-variables }

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as seguintes variáveis de ambiente para se conectar à instância do Jenkins:

* `GITHUB_ACCESS_TOKEN`: personal access token (classic) usado para criar pull requests com um fluxo de trabalho convertido (requer os escopos `repo` e `workflow`).

* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).

* `JENKINS_ACCESS_TOKEN`: o token de API do Jenkins usado para exibir recursos do Jenkins.

!!! note

  > Esse token exige acesso a todos os trabalhos que você deseja migrar ou auditar. Nos casos em que uma pasta ou um trabalho não herda as listas de controle de acesso dos pais, você precisa conceder permissões explícitas ou privilégios de administrador completos.

* `JENKINS_USERNAME`: o nome de usuário da conta de usuário que criou o token de API do Jenkins.

* `JENKINS_INSTANCE_URL`: a URL da instância do Jenkins.

* `JENKINSFILE_ACCESS_TOKEN` (Opcional) O token de API usado para recuperar o conteúdo de um `Jenkinsfile` armazenado no repositório de build. Isso exige o escopo `repo`. Se isso não for fornecido, o `GITHUB_ACCESS_TOKEN` será usado no lugar dele.

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Como usar argumentos opcionais { #using-optional-arguments }

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `forecast`, `dry-run` ou `migration`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--source-file-path` indica a GitHub Actions Importer usar o caminho do arquivo de origem especificado. Use essa opção para pipelines de Jenkinsfile e de vários branches.

Caso você deseje fornecer vários arquivos de origem ao executar o subcomando `forecast`, use padrões correspondentes no valor do caminho do arquivo. Por exemplo, `gh forecast --source-file-path ./tmp/previous_forecast/jobs/*.json` fornece todos os GitHub Actions Importer arquivos de origem que correspondam ao caminho do `./tmp/previous_forecast/jobs/*.json` arquivo.

##### Exemplo de pipeline do Jenkinsfile { #jenkinsfile-pipeline-example }

Neste exemplo, GitHub Actions Importer usa o Jenkinsfile especificado como o arquivo de origem para executar uma execução seca.

```
gh actions-importer dry-run jenkins --output-dir path/to/output/ --source-file-path path/to/Jenkinsfile --source-url :url_to_jenkins_job
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

Quando você usa a opção `--config-file-path` com os `dry-run` subcomandos ou `migrate` subcomandos, GitHub Actions Importer corresponde à lesma do repositório ao trabalho representado pela opção `--source-url` para selecionar o pipeline. Ele usa o `config-file-path` para efetuar pull do arquivo de origem especificado.

##### Exemplo de auditoria { #audit-example }

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```
gh actions-importer audit jenkins --output-dir path/to/output/ --config-file-path path/to/jenkins/config.yml
```

Para auditar uma instância do Jenkins usando um arquivo de configuração, o arquivo de configuração precisa estar no seguinte formato e cada valor `repository_slug` precisa ser exclusivo:

```
source_files:
  - repository_slug: pipeline-name
    path: path/to/Jenkinsfile
  - repository_slug: multi-branch-pipeline-name
    branches:
      - branch: main
        path: path/to/Jenkinsfile
      - branch: node
        path: path/to/Jenkinsfile
```

### Sintaxe com suporte para pipelines do Jenkins { #supported-syntax-for-jenkins-pipelines }

As tabelas a seguir mostram que o tipo de propriedades GitHub Actions Importer é capaz de converter no momento. Para obter mais detalhes sobre como a sintaxe de pipeline do Jenkins se alinha GitHub Actions, consulte [Migrando do Jenkins para o GitHub Actions](../manual-migrations/migrate-from-jenkins.md).

Para obter informações sobre os plug-ins do Jenkins com suporte, confira o [ repositório `github/gh-actions-importer`](https://github.com/github/gh-actions-importer/blob/main/docs/jenkins/index.md).

#### Sintaxe suportada para pipelines Freestyle { #supported-syntax-for-freestyle-pipelines }

| Jenkins           | GitHub Actions            | Status          |
| :---------------- | :------------------------ | :-------------- |
| modelo do Docker  | `jobs.<job_id>.container` | Com suporte     |
| build             | `jobs`                    | Suporte parcial |
| compilar ambiente | `env`                     | Suporte parcial |
| gatilhos de build | `on`                      | Suporte parcial |
| geral             | `runners`                 | Suporte parcial |

#### Sintaxe suportada para pipelines Jenkinsfile { #supported-syntax-for-jenkinsfile-pipelines }

| Jenkins      | GitHub Actions                  | Status          |
| :----------- | :------------------------------ | :-------------- |
| docker       | `jobs.<job_id>.container`       | Com suporte     |
| fase         | `jobs.<job_id>`                 | Com suporte     |
| agente       | `runners`                       | Suporte parcial |
| ambiente     | `env`                           | Suporte parcial |
| fases        | `jobs`                          | Suporte parcial |
| etapas       | `jobs.<job_id>.steps`           | Suporte parcial |
| disparadores | `on`                            | Suporte parcial |
| quando       | `jobs.<job_id>.if`              | Suporte parcial |
| entradas     | `inputs`                        | Sem suporte     |
| matriz       | `jobs.<job_id>.strategy.matrix` | Sem suporte     |
| opções       | `jobs.<job_id>.strategy`        | Sem suporte     |
| parâmetros   | `inputs`                        | Sem suporte     |

### Sintaxe das variáveis de ambiente { #environment-variables-syntax }

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente jenkins padrão para o equivalente mais próximo em GitHub Actions.

| Jenkins           | GitHub Actions                                                                        |
| :---------------- | :------------------------------------------------------------------------------------ |
| `${BUILD_ID}`     | `${{ github.run_id }}`                                                                |
| `${BUILD_NUMBER}` | `${{ github.run_id }}`                                                                |
| `${BUILD_TAG}`    | `${{ github.workflow }}-${{ github.run_id }}`                                         |
| `${BUILD_URL}`    | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |
| `${JENKINS_URL}`  | `${{ github.server_url }}`                                                            |
| `${JOB_NAME}`     | `${{ github.workflow }}`                                                              |
| `${WORKSPACE}`    | `${{ github.workspace }}`                                                             |

## Aviso legal { #legal-notice }

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
