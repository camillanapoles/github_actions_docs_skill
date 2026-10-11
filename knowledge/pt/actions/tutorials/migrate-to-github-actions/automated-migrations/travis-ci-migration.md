---
title: Migrando do Travis CI com GitHub Actions Importer
description: Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de CI travis para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/travis-ci-migration
captured: '2026-10-11'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando do Travis CI com GitHub Actions Importer

_Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de CI travis para GitHub Actions._

## Sobre a migração do Travis CI para o GitHub Actions usando o importador

As instruções a seguir orientarão você na configuração do ambiente a ser usado GitHub Actions Importer para migrar pipelines de CI do Travis para GitHub Actions.

### Pré-requisitos

* Uma conta de CI do Travis ou uma organização com pipelines e trabalhos que você deseja converter em GitHub Actions fluxos de trabalho.
* Acesso para criar um token de acesso à API do Travis CI para sua conta ou sua organização.
* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações

Há algumas limitações ao migrar de pipelines de CI travis para GitHub Actions com GitHub Actions Importer.

#### Tarefas manuais

Alguns constructos do Travis CI precisam ser migrados manualmente. Estão incluídos:

* Segredos
* Propriedades de trabalho desconhecidas

Para saber mais sobre migrações manuais, confira [Migrando de Travis CI para GitHub Actions](../manual-migrations/migrate-from-travis-ci.md).

#### Linguagens do projeto do Travis CI

GitHub Actions Importer transforma as linguagens de projeto do Travis CI adicionando um conjunto de ferramentas de build pré-configuradas e um script de build padrão ao fluxo de trabalho transformado. Se nenhum idioma for declarado explicitamente, GitHub Actions Importer pressupõe que uma linguagem de projeto seja Ruby.

Para obter uma lista dos idiomas de projeto com suporte, consulte [os idiomas de projeto com suporte](#supported-project-languages)GitHub Actions Importer.

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

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer ao trabalhar com Travis CI e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um token de acesso à API do Travis CI. Para obter mais informações, confira [Obter seu token de API do Travis CI](https://docs.travis-ci.com/user/migrate/travis-migrate-to-apps-gem-guide/#4-get-your-travis-ci-api-token) na documentação do Travis CI.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
   ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `Travis CI`, pressione `Espaço` para fazer a seleção e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token para Travis CI", insira o valor do token de acesso da API de CI travis que você criou anteriormente e pressione `Enter`.
   * Em "URL base da instância do Travis CI", insira a URL da instância do Travis CI e pressione `ENTER`.
   * Em "Nome da organização do Travis CI", insira o nome da sua organização do Travis CI e pressione `ENTER`.

   Um exemplo da saída do comando `configure` é mostrado abaixo.

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: Travis CI
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for Travis CI: ***************
   ✔ Base url of the Travis CI instance: https://travis-ci.com
   ✔ Travis CI organization name: actions-importer-labs
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

## Executar uma auditoria do Travis CI

Use o comando `audit` para obter uma exibição de alto nível de todos os pipelines de um servidor do Travis CI.

O comando `audit` executa as seguintes etapas:

1. Busca todos os projetos definidos em um servidor do Travis CI.
2. Converte cada pipeline em seu fluxo de trabalho equivalente GitHub Actions .
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria

Para executar uma auditoria de um servidor do Travis CI, execute o seguinte comando no terminal:

```shell
gh actions-importer audit travis-ci --output-dir tmp/audit
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

#### Tarefas manuais { #tarefas-manuais-1 }

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

Você pode usar o comando para prever o `forecast` uso potencial GitHub Actions com base em métricas de computação de execuções de pipeline concluídas em seu servidor de CI Travis.

### Como executar o comando de previsão

Para executar uma previsão de uso potencial GitHub Actions , execute o comando a seguir em seu terminal. Por padrão, GitHub Actions Importer inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast travis-ci --output-dir tmp/forecast
```

### Como inspecionar o relatório de previsão

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.
  * Essa métrica está correlacionada ao quanto você deve esperar gastar GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* ```
            As métricas de **tempo de espera** descrevem o tempo gasto por um trabalho aguardando um executor ficar disponível para executá-lo.
        ```
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento. Esta métrica pode ser usada para definir o número de executores que você deve configurar.

Além disso, essas métricas são definidas para cada fila de runners no Travis CI. Isso é especialmente útil quando há uma combinação de executores hospedados ou auto-hospedados ou quando há computadores de especificação alta ou baixa, a fim de ver métricas específicas para diferentes tipos de executores.

## Executar uma simulação de migração de um pipeline do Travis CI

Você pode usar o `dry-run` comando para converter um pipeline de CI do Travis em um fluxo de trabalho equivalente GitHub Actions . Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

Para executar uma execução seca da migração dos pipelines de CI do Travis para GitHub Actions, execute o seguinte comando em seu terminal, substituindo `my-travis-ci-repository` pelo nome do repositório travis ci.

```
gh actions-importer dry-run travis-ci --travis-ci-repository my-travis-ci-repository --output-dir tmp/dry-run
```

É possível ver os logs da simulação e os arquivos de fluxos de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Executar uma migração de produção de um pipeline do Travis CI

Você pode usar o `migrate` comando para converter um pipeline de CI do Travis e abrir uma solicitação pull com o fluxo de trabalho equivalente GitHub Actions .

### Como executar o comando de migração

Para migrar um pipeline de CI do Travis, GitHub Actionsexecute o seguinte comando em seu terminal, substituindo o `target-url` valor pela URL do repositório GitHub e `my-travis-ci-repository` pelo nome do repositório travis ci.

```
gh actions-importer migrate travis-ci --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --travis-ci-repository my-travis-ci-repository
```

A saída do comando inclui a URL para a solicitação de pull que adiciona o fluxo de trabalho convertido ao repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```
$ gh actions-importer migrate travis-ci --target-url https://github.com/octo-org/octo-repo --output-dir tmp/migrate --travis-ci-repository my-travis-ci-repository
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

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do Travis CI.

### Usando variáveis de ambiente

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as seguintes variáveis de ambiente para se conectar à instância de CI do Travis:

* `GITHUB_ACCESS_TOKEN`: o personal access token (classic) usado para criar solicitações de pull com um fluxo de trabalho convertido (requer o `workflow` escopo).
* `GITHUB_INSTANCE_URL`: a URL para a instância de destino GitHub (por exemplo, `https://github.com`).
* `TRAVIS_CI_ACCESS_TOKEN`: o token de acesso à API do Travis CI usado para exibir os recursos do Travis CI.
* `TRAVIS_CI_ORGANIZATION`: O nome da organização da sua instância do Travis CI.
* `TRAVIS_CI_INSTANCE_URL`: a URL da instância do Travis CI.
* `TRAVIS_CI_SOURCE_GITHUB_ACCESS_TOKEN`: (Opcional) O personal access token usado para autenticar com sua instância de GitHub de origem. Se isso não for fornecido, `GITHUB_ACCESS_TOKEN` será usado no lugar dele.
* `TRAVIS_CI_SOURCE_GITHUB_INSTANCE_URL`: (Opcional) A URL para a instância de GitHub de origem, como <https://github.com>. Se isso não for fornecido, `GITHUB_INSTANCE_URL` será usado no lugar dele.

Essas variáveis de ambiente podem ser especificadas em um `.env.local` arquivo que é carregado pelo GitHub Actions Importer quando ele é executado.

### Como usar argumentos opcionais

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `forecast`, `dry-run` ou `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--source-file-path` indica a GitHub Actions Importer usar o caminho do arquivo de origem especificado.

Por exemplo:

```
gh actions-importer dry-run travis-ci --output-dir ./path/to/output/ --travis-ci-repository my-travis-ci-repository --source-file-path ./path/to/.travis.yml
```

#### `--allow-inactive-repositories`

Você pode usar esse argumento para especificar se GitHub Actions Importer deve incluir repositórios inativos em uma auditoria. Se essa opção não for definida, os repositórios inativos não serão incluídos nas auditorias.

```
gh actions-importer dry-run travis-ci --output-dir ./path/to/output/ --travis-ci-repository my-travis-ci-repository --allow-inactive-repositories
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline do controle do código-fonte. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

##### Exemplo de auditoria

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```
gh actions-importer audit travis-ci --output-dir ./path/to/output/ --config-file-path ./path/to/travis-ci/config.yml
```

Para auditar uma instância do Travis CI usando um arquivo de configuração, o arquivo precisa estar no seguinte formato e cada valor `repository_slug` precisa ser exclusivo:

```
source_files:
  - repository_slug: travis-org-name/travis-repo-name
    path: path/to/.travis.yml
  - repository_slug: travis-org-name/some-other-travis-repo-name
    path: path/to/.travis.yml
```

##### Exemplo de simulação a seco

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado como o arquivo de origem para executar uma execução seca.

O pipeline é selecionado pela correspondência do `repository_slug` no arquivo de configuração com o valor da opção `--travis-ci-repository`. Em seguida, `path` é usado para efetuar pull do arquivo de origem especificado.

```
gh actions-importer dry-run travis-ci --travis-ci-repository travis-org-name/travis-repo-name --output-dir ./output/ --config-file-path ./path/to/travis-ci/config.yml
```

### Linguagens de projeto com suporte

GitHub Actions Importer dá suporte à migração de projetos de CI travis nos idiomas a seguir.

<ul style="-webkit-column-count: 3; -moz-column-count: 3; column-count: 3;">
<li><code>android</code></li>
<li><code>bash</code></li>
<li><code>c</code></li>
<li><code>clojure</code></li>
<li><code>c++</code></li>
<li><code>crystal</code></li>
<li><code>c#</code></li>
<li><code>d</code></li>
<li><code>dart</code></li>
<li><code>elixir</code></li>
<li><code>erlang</code></li>
<li><code>generic</code></li>
<li><code>go</code></li>
<li><code>groovy</code></li>
<li><code>haskell</code></li>
<li><code>haxe</code></li>
<li><code>java</code></li>
<li><code>julia</code></li>
<li><code>matlab</code></li>
<li><code>minimal</code></li>
<li><code>nix</code></li>
<li><code>node_js</code></li>
<li><code>objective-c</code></li>
<li><code>perl</code></li>
<li><code>perl6</code></li>
<li><code>php</code></li>
<li><code>python</code></li>
<li><code>r</code></li>
<li><code>ruby</code></li>
<li><code>rust</code></li>
<li><code>scala</code></li>
<li><code>sh</code></li>
<li><code>shell</code></li>
<li><code>smalltalk</code></li>
<li><code>swift</code></li>
</ul>

### Sintaxe com suporte para pipelines do Travis CI

A tabela a seguir mostra os tipos de propriedades que GitHub Actions Importer pode converter atualmente. Para obter mais detalhes sobre como a sintaxe do pipeline do Travis CI se alinha GitHub Actions, consulte [Migrando de Travis CI para GitHub Actions](../manual-migrations/migrate-from-travis-ci.md).

| Travis CI                                              | GitHub Actions                                                                                                           |          Status |
| :----------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- | --------------: |
| ramificações                                           | <ul><li>`on.<push>.<branches>`</li>                                                                                      |     Com suporte |
| build_pull_requests (construir solicitações de pull) | <ul><li>`on.<pull_request>`</li>                                                                                         |     Com suporte |
| env                                                    | <ul><li>`env`</li> <li>`jobs.<job_id>.env`</li><li>`jobs.<job_id>.steps.env`</li>                                        |     Com suporte |
| if                                                     | <ul><li>`jobs.<job_id>.if`</li></ul>                                                                                     |     Com suporte |
| cargo                                                  | <ul><li>`jobs.<job_id>`</li><li>`jobs.<job_id>.name`</li></ul>                                                           |     Com suporte |
| matriz                                                 | <ul><li>`jobs.<job_id>.strategy`</li><li>`jobs.<job_id>.strategy.fail-fast`</li><li>`jobs.<job_id>.strategy.matrix`</li> |     Com suporte |
| os \&dist                                              | <ul><li>`runners`</li></ul>                                                                                              |     Com suporte |
| scripts                                                | <ul><li>`jobs.<job_id>.steps`</li></ul>                                                                                  |     Com suporte |
| fases                                                  | <ul><li>`jobs`</li></ul>                                                                                                 |     Com suporte |
| env                                                    | <ul><li>`on`</li>                                                                                                        | Suporte parcial |
| ramificações                                           | <ul><li>`on.<push>.<tags>`</li><li>`on.<push>.paths`</li>                                                                |     Sem suporte |
| build_pull_requests (construir solicitações de pull) | <ul><li>`on.<pull_request>.<branches>`</li><li>`on.<pull_request>.<tags>`</li><li>`on.<pull_request>.paths`</li>         |     Sem suporte |
| gatilhos cron                                          | <ul><li>`on.schedule`</li><li>`on.workflow_run`</li></ul>                                                                |     Sem suporte |
| env                                                    | <ul><li>`jobs.<job_id>.timeout-minutes`</li><li>`on.<event_name>.types`</li>                                             |     Sem suporte |
| cargo                                                  | <ul><li>`jobs.<job_id>.container`</li>                                                                                   |     Sem suporte |
| os \&dist                                              | <ul><li>`self hosted runners`</li></ul>                                                                                  |     Sem suporte |

Para obter informações sobre os recursos do Travis CI compatíveis, consulte o repositório [`github/gh-actions-importer`](https://github.com/github/gh-actions-importer/blob/main/docs/travis_ci/index.md).

### Sintaxe de variáveis de ambiente

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente de CI travis padrão para o equivalente mais próximo em GitHub Actions.

| Travis CI                 | GitHub Actions        |
| :------------------------ | :-------------------- |
| `$CONTINUOUS_INTEGRATION` | `$CI`                 |
| `$USER`                   | `${{ github.actor }}` |
| `$HOME`                   |                       `${{ github.workspace }}` |
|
| `$TRAVIS_BRANCH`             | `${{ github.ref }}`                                                                   |
| `$TRAVIS_BUILD_DIR`           | `${{ github.workspace }}`                                                             |
| `$TRAVIS_BUILD_ID`            | `${{ github.run_number }}`                                                            |
| `$TRAVIS_BUILD_NUMBER`        | `${{ github.run_id }}`                                                                |
| `$TRAVIS_COMMIT`              | `${{ github.sha }}`                                                                   |
| `$TRAVIS_EVENT_TYPE`          | `${{ github.event_name }}`                                                            |
| `$TRAVIS_PULL_REQUEST_BRANCH` | `${{ github.base_ref }}`                                                              |
| `$TRAVIS_PULL_REQUEST`        | `${{ github.event.number }}`                                                          |
| `$TRAVIS_PULL_REQUEST_SHA`    | `${{ github.head.sha }}`                                                              |
| `$TRAVIS_PULL_REQUEST_SLUG`   | `${{ github.repository }}`                                                            |
| `$TRAVIS_TAG`                 | `${{ github.ref }}`                                                                   |
| `$TRAVIS_OS_NAME`             | `${{ runner.os }}`                                                                    |
| `$TRAVIS_JOB_ID`              | `${{ github.job }}`                                                                   |
| `$TRAVIS_REPO_SLUG`           | `${{ github.repository_owner/github.repository }}`                                    |
| `$TRAVIS_BUILD_WEB_URL`       | `${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}` |

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
