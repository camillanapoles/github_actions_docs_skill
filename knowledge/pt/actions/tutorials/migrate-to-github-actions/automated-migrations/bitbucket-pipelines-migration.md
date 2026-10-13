---
title: Migrando do Bitbucket Pipelines com o importador de GitHub Actions
description: Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Bitbucket para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bitbucket-pipelines-migration
captured: '2026-10-13'
section: Tutorials / Migrate to github actions / Automated migrations
---

# Migrando do Bitbucket Pipelines com o importador de GitHub Actions { #migrating-from-bitbucket-pipelines-with-github-actions-importer }

_Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Bitbucket para GitHub Actions._

## Sobre a migração do Bitbucket Pipelines com GitHub Actions Importer { #about-migrating-from-bitbucket-pipelines-with-github-actions-importer }

As instruções a seguir orientarão você na configuração do seu ambiente para usar GitHub Actions Importer para migrar pipelines do Bitbucket para GitHub Actions.

### Pré-requisitos { #prerequisites }

* Um ambiente em que seja possível executar contêineres baseados no Linux e instalar as ferramentas necessárias.
  * O Docker está [instalado](https://docs.docker.com/get-docker/) e em execução.

  * A [CLI do GitHub](https://cli.github.com) está instalada.
!!! note

  > A CLI e o contêiner do GitHub Actions Importer não precisam ser instalados no mesmo servidor que a plataforma de CI.

### Limitações { #limitations }

Há algumas limitações ao migrar do Bitbucket Pipelines para GitHub Actions com GitHub Actions Importer.

* Não há suporte para imagens em um AWS ECR privado.
* Não há suporte para a opção do Bitbucket Pipelines `size`.
  Se precisar de recursos adicionais de executor no GitHub Actions, considere usar executor avançados. Para obter mais informações, consulte [Usando executores maiores](../../../how-tos/manage-runners/larger-runners.md).
* As métricas que detalham o tempo de fila dos trabalhos não são compatíveis com o comando `forecast`.
* Os [after-scripts](https://support.atlassian.com/bitbucket-cloud/docs/step-options/#After-script) do Bitbucket são compatíveis usando-se GitHub Actions`always()` em combinação com a verificação de `steps.<step_id>.conclusion` da etapa anterior. Para saber mais, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#steps-context).

  Veja a seguir um exemplo de uso do `always()` com o `steps.<step_id>.conclusion`.

        ```yaml
    - name: After Script 1
      run: |-
        echo "I'm after the script ran!"
        echo "We should be grouped!"
      id: after-script-1
      if: "${{ always() }}"
    - name: After Script 2
      run: |-
        echo "this is really the end"
        echo "goodbye, for now!"
      id: after-script-2
      if: "${{ steps.after-script-1.conclusion == 'success' && always() }}"
        ```

### Tarefas manuais { #manual-tasks }

Certos constructos do Bitbucket Pipelines devem ser migrados manualmente. Estão incluídos:

* Repositório seguro, espaço de trabalho e variáveis de implementação
* Chaves SSH

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

O `configure` comando da CLI é usado para definir as credenciais e as opções necessárias para GitHub Actions Importer ao trabalhar com o Bitbucket Pipelines e GitHub.

1. Criar um GitHubpersonal access token (classic). Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   O token precisa ter o escopo `workflow`.

   Depois de criar o token, copie-o e salve-o em um local seguro para uso posterior.

2. Crie um token de acesso ao espaço de trabalho para o Bitbucket Pipelines. Para obter mais informações, consulte [Permissões do token de acesso ao espaço de trabalho](https://support.atlassian.com/bitbucket-cloud/docs/workspace-access-token-permissions/) na documentação do Bitbucket. Seu token deve ter o escopo `read` para pipelines, projetos e repositórios.

3. No seu terminal, execute o comando CLI GitHub Actions Importer`configure`:

            ```shell
   gh actions-importer configure
            ```

   O comando `configure` solicitará que você insira as seguintes informações:

   * Em "Quais provedores de CI você está configurando?", use as teclas de direção para selecionar `Bitbucket`, pressione `Espaço` para fazer a seleção e pressione `Enter`.
   * Para "Personal access token para GitHub", insira o valor do personal access token (classic) que você criou anteriormente e pressione `Enter`.
   * Para "URL base da instância do GitHub", insira pressione `Enter` para aceitar o valor padrão (`https://github.com`).
   * Para "Personal access token for Bitbucket", insira o Token de Acesso do Workspace que você criou anteriormente e pressione `Enter`.
   * Em "URL base da instância do Bitbucket", digite o URL da sua instância do Bitbucket e pressione `Enter`.

   Um exemplo do comando `configure` é mostrado abaixo:

            ```shell
   $ gh actions-importer configure
   ✔ Which CI providers are you configuring?: Bitbucket
   Enter the following values (leave empty to omit):
   ✔ Personal access token for GitHub: ***************
   ✔ Base url of the GitHub instance: https://github.com
   ✔ Personal access token for Bitbucket: ********************
   ✔ Base url of the Bitbucket instance: https://bitbucket.example.com
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

## Realizar uma auditoria da instância do Bitbucket { #perform-an-audit-of-the-bitbucket-instance }

Você pode usar o comando audit para obter uma visão de alto nível dos pipelines em uma instância do Bitbucket.

O comando audit executa as seguintes etapas.

1. Obtém todos os pipelines de um espaço de trabalho.
2. Converte o pipeline em seu equivalente fluxo de trabalho do GitHub Actions.
3. Gera um relatório que resume o quão completa e complexa de uma migração é possível com GitHub Actions Importer.

### Como executar o comando de auditoria { #running-the-audit-command }

Para realizar uma auditoria, execute o seguinte comando em seu terminal, substituindo `:workspace` pelo nome do espaço de trabalho do Bitbucket a ser auditado.

```bash
gh actions-importer audit bitbucket --workspace :workspace --output-dir tmp/audit
```

Opcionalmente, uma opção `--project-key` pode ser fornecida ao comando audit para limitar os resultados apenas aos pipelines associados a um projeto.

No exemplo de comando abaixo, `:project_key` deve ser substituído pela chave do projeto que deve ser auditado. As chaves do projeto podem ser encontradas no Bitbucket na página de projetos do espaço de trabalho.

```bash
gh actions-importer audit bitbucket --workspace :workspace --project-key :project_key --output-dir tmp/audit
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

#### Tarefas manuais { #manual-tasks-1 }

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

## Previsão de uso { #forecasting-usage }

Você pode usar o comando `forecast` para prever o uso potencial de GitHub Actions ao calcular métricas a partir de execuções de pipeline concluídas na sua instância do Bitbucket.

### Como executar o comando de previsão { #running-the-forecast-command }

Para realizar uma projeção do uso potencial do GitHub Actions, execute o seguinte comando no seu terminal, substituindo `:workspace` pelo nome do workspace do Bitbucket para projetar. Por padrão, GitHub Actions Importador inclui os sete dias anteriores no relatório de previsão.

```shell
gh actions-importer forecast bitbucket --workspace :workspace --output-dir tmp/forecast_reports
```

### Previsão de um projeto { #forecasting-a-project }

Para limitar a previsão a um projeto, você pode usar a opção `--project-key`. Substitua o valor do `:project_key` pela chave do projeto a ser previsto.

```shell
gh actions-importer forecast bitbucket --workspace :workspace --project-key :project_key --output-dir tmp/forecast_reports
```

### Como inspecionar o relatório de previsão { #inspecting-the-forecast-report }

O arquivo `forecast_report.md` no diretório de saída especificado contém os resultados da previsão.

Veja abaixo alguns termos importantes que podem aparecer no relatório de previsão:

* A **contagem de trabalhos** é o número total de trabalhos concluídos.
* A **contagem de pipelines** é o número de pipelines exclusivos usados.
* O **tempo de execução** descreve a quantidade de tempo que um executor gastou na execução de uma tarefa. Essa métrica pode ser usada para ajudar a planejar o custo dos GitHubexecutores hospedados.
  * Essa métrica está correlacionada ao quanto você deve esperar gastar no GitHub Actions. Isso pode variar de acordo com o hardware usado para esses minutos. Você pode usar a [GitHub Actions calculadora de preços](https://github.com/pricing/calculator) para estimar os custos.
* As métricas de **trabalhos simultâneos** descrevem a quantidade de trabalhos em execução a qualquer momento.

## Realização de uma migração simulada { #performing-a-dry-run-migration }

Você pode usar o comando de dry-run para converter um pipeline do Bitbucket em fluxo(s) de trabalho equivalente(s) doGitHub Actions. Uma simulação cria os arquivos de saída em um diretório especificado, mas não abre uma solicitação de pull para migrar o pipeline.

### Como executar o comando de simulação { #running-the-dry-run-command }

Para fazer uma simulação da migração de um pipeline no Bitbucket para GitHub Actions, execute o seguinte comando no terminal, substituindo `:workspace` pelo nome do espaço de trabalho e `:repo` pelo nome do repositório no Bitbucket.

```bash
gh actions-importer dry-run bitbucket --workspace :workspace --repository :repo --output-dir tmp/dry-run
```

### Como inspecionar os fluxos de trabalho convertidos { #inspecting-the-converted-workflows }

Você pode ver os logs da simulação e os arquivos de fluxo de trabalho convertidos no diretório de saída especificado.

Se houver algo que GitHub Actions Importer não foi capaz de converter automaticamente, como etapas de build desconhecidas ou um pipeline parcialmente bem-sucedido, talvez você queira criar transformadores personalizados para personalizar ainda mais o processo de conversão. Para saber mais, confira [Estendendo o Importador do GitHub Actions com transformadores personalizados](../../../reference/github-actions-importer/custom-transformers.md).

## Realização de uma migração de produção { #performing-a-production-migration }

Você pode usar o comando migrate para converter um pipeline do Bitbucket e abrir uma pull request com os fluxos de trabalho equivalentes do GitHub Actions.

### Como executar o comando de migração { #running-the-migrate-command }

Para migrar um pipeline do Bitbucket para GitHub Actions, execute o seguinte comando no terminal, substituindo os valores a seguir.

* Substitua o valor de `target-url` pela URL do seu repositório GitHub.
* Substitua `:repo` pelo nome do repositório no Bitbucket.
* Substitua `:workspace` pelo nome do espaço de trabalho.

```bash
gh actions-importer migrate bitbucket --workspace :workspace --repository :repo --target-url https://github.com/:owner/:repo --output-dir tmp/dry-run
```

A saída do comando inclui a URL da solicitação de pull que adiciona o fluxo de trabalho convertido ao repositório. Um exemplo de uma saída bem-sucedida é semelhante ao seguinte:

```bash
gh actions-importer migrate bitbucket --workspace actions-importer --repository custom-trigger --target-url https://github.com/valet-dev-testing/demo-private --output-dir tmp/bitbucket
[2023-07-18 09:56:06] Logs: 'tmp/bitbucket/log/valet-20230718-165606.log'
[2023-07-18 09:56:24] Pull request: 'https://github.com/valet-dev-testing/demo-private/pull/55'
```

### Como inspecionar a solicitação de pull { #inspecting-the-pull-request }

A saída de uma execução bem-sucedida do comando `migrate` contém um link para a nova solicitação de pull que adiciona o fluxo de trabalho convertido ao seu repositório.

Alguns elementos importantes da solicitação de pull incluem:

* Na descrição da solicitação de pull, uma seção chamada **Etapas manuais**, que lista as etapas que você precisa concluir manualmente para concluir a migração dos pipelines para o GitHub Actions. Por exemplo, esta seção pode solicitar a criação dos segredos usados nos fluxos de trabalho.
* O arquivo de fluxos de trabalho convertido. Selecione a guia **Files changed** na pull request para ver o arquivo de fluxo de trabalho que será adicionado ao repositório do GitHub.

Quando terminar de inspecionar a pull request, você poderá mesclá-la para adicionar o fluxo de trabalho ao repositório do GitHub.

## Referência { #reference }

Esta seção contém informações de referência sobre variáveis de ambiente, argumentos opcionais e sintaxe com suporte ao usar GitHub Actions Importer para migrar do Bitbucket Pipelines.

### Usando variáveis de ambiente { #using-environment-variables }

O GitHub Actions Importer usa variáveis de ambiente para a configuração de autenticação. Essas variáveis são definidas durante o processo de configuração com o comando `configure`. Para obter mais informações, confira a seção [Como configurar as credenciais](#configuring-credentials).

GitHub Actions Importer usa as variáveis de ambiente a seguir para se conectar à instância do Bitbucket.

* `GITHUB_ACCESS_TOKEN`: o personal access token (classic) usado para criar solicitações de pull com um fluxo de trabalho transformado (requer os escopos de `repo` e `workflow`).
* `GITHUB_INSTANCE_URL`: a url para a instância de GitHub de destino. (por exemplo, `https://github.com`)
* `BITBUCKET_ACCESS_TOKEN`: o token de acesso ao workspace com escopos de leitura para pipeline, projeto e repositório.

Essas variáveis de ambiente podem ser especificadas em um arquivo `.env.local` que será carregado por GitHub Actions Importer em tempo de execução. O arquivo de distribuição contém um arquivo `.env.local.template` que pode ser usado para criar esses arquivos.

### Argumentos opcionais { #optional-arguments }

Há argumentos opcionais que você pode usar com os subcomandos do GitHub Actions Importer para personalizar sua migração.

#### `--source-file-path`

Use o argumento `--source-file-path` com os subcomandos `dry-run` ou `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline da instância do Bitbucket. O argumento `--source-file-path` informa ao GitHub Actions Importer que use o caminho do arquivo de origem especificado.

Por exemplo:

```bash
gh actions-importer dry-run bitbucket --workspace :workspace --repository :repo --output-dir tmp/dry-run --source-file-path path/to/my/pipeline/file.yml
```

#### `--config-file-path`

Use o argumento `--config-file-path` com os subcomandos `audit`, `dry-run` e `migrate`.

Por padrão, GitHub Actions Importer busca o conteúdo do pipeline da instância do Bitbucket. O argumento `--config-file-path` instrui GitHub Actions Importer a usar os arquivos de origem especificados.

### Exemplo de auditoria { #audit-example }

Neste exemplo, GitHub Actions Importer usa o arquivo de configuração YAML especificado para executar uma auditoria.

```bash
gh actions-importer audit bitbucket --workspace :workspace --output-dir tmp/audit --config-file-path "path/to/my/bitbucket/config.yml"
```

Para auditar uma instância do Bitbucket usando um arquivo de configuração, este deve estar no seguinte formato, e cada `repository_slug` deve ser exclusivo:

```yaml
source_files:
  - repository_slug: repo_name
    path: path/to/one/source/file.yml
  - repository_slug: another_repo_name
    path: path/to/another/source/file.yml
```

## Sintaxe compatível com o Bitbucket Pipelines { #supported-syntax-for-bitbucket-pipelines }

A tabela a seguir mostra o tipo de propriedades que GitHub Actions Importer atualmente é capaz de converter.

| Bitbucket                 | GitHub Actions                                  |      Status |
|:------------------------|:----------------------------------------------|----------:|
| `after-script`            | `jobs.<job_id>.steps[*]`                        | Com suporte |
| `artifacts`               | `actions/upload-artifact` & `download-artifact` | Com suporte |
| `caches`                  | `actions/cache`                                 | Com suporte |
| `clone`                   | `actions/checkout`                              | Com suporte |
| `condition`               | `job.<job_id>.steps[*].run`                     | Com suporte |
| `deployment`              | `jobs.<job_id>.environment`                     | Com suporte |
| `image`                   | `jobs.<job_id>.container`                       | Com suporte |
| `max-time`                | `jobs.<job_id>.steps[*].timeout-minutes`        | Com suporte |
| `options.docker`          | Nenhum                                          | Com suporte |
| `options.max-time`        | `jobs.<job_id>.steps[*].timeout-minutes`        | Com suporte |
| `parallel`                | `jobs.<job_id>`                                 | Com suporte |
| `pipelines.branches`      | `on.push`                                       | Com suporte |
| `pipelines.custom`        | `on.workflow_dispatch`                          | Com suporte |
| `pipelines.default`       | `on.push`                                       | Com suporte |
| `pipelines.pull-requests` | `on.pull_requests`                              | Com suporte |
| `pipelines.tags`          | `on.tags`                                       | Com suporte |
| `runs-on`                 | `jobs.<job_id>.runs-on`                         | Com suporte |
| `script`                  | `job.<job_id>.steps[*].run`                     | Com suporte |
| `services`                | `jobs.<job_id>.service`                         | Com suporte |
| `stage`                   | `jobs.<job_id>`                                 | Com suporte |
| `step`                    | `jobs.<job_id>.steps[*]`                        | Com suporte |
| `trigger`                 | `on.workflow_dispatch`                          | Com suporte |
| `fail-fast`               | Nenhum                                          | Sem suporte |
| `oidc`                    | Nenhum                                          | Sem suporte |
| `options.size`            | Nenhum                                          | Sem suporte |
| `size`                    | Nenhum                                          | Sem suporte |

### Mapeamento de variáveis de ambiente { #environment-variable-mapping }

GitHub Actions Importer usa o mapeamento na tabela abaixo para converter variáveis de ambiente do Bitbucket padrão para o equivalente mais próximo em GitHub Actions.

| Bitbucket                               | GitHub Actions                                              |
|:--------------------------------------|:----------------------------------------------------------|
| `CI`                                    | `true`                                                      |
| `BITBUCKET_BUILD_NUMBER`                | `${{ github.run_number }}`                                  |
| `BITBUCKET_CLONE_DIR`                   | `${{ github.workspace }}`                                   |
| `BITBUCKET_COMMIT`                      | `${{ github.sha }}`                                         |
| `BITBUCKET_WORKSPACE`                   | `${{ github.repository_owner }}`                            |
| `BITBUCKET_REPO_SLUG`                   | `${{ github.repository }}`                                  |
| `BITBUCKET_REPO_UUID`                   | `${{ github.repository_id }}`                               |
| `BITBUCKET_REPO_FULL_NAME`              | `${{ github.repository_owner }}`/`${{ github.repository }}` |
| `BITBUCKET_BRANCH`                      | `${{ github.ref }}`                                         |
| `BITBUCKET_TAG`                         | `${{ github.ref }}`                                         |
| `BITBUCKET_PR_ID`                       | `${{ github.event.pull_request.number }}`                   |
| `BITBUCKET_PR_DESTINATION_BRANCH`       | `${{ github.event.pull_request.base.ref }}`                 |
| `BITBUCKET_GIT_HTTP_ORIGIN`             | `${{ github.event.repository.clone_url }}`                  |
| `BITBUCKET_GIT_SSH_ORIGIN`              | `${{ github.event.repository.ssh_url }}`                    |
| `BITBUCKET_EXIT_CODE`                   | `${{ job.status }}`                                         |
| `BITBUCKET_STEP_UUID`                   | `${{ job.github_job }}`                                     |
| `BITBUCKET_PIPELINE_UUID`               | `${{ github.workflow }}`                                    |
| `BITBUCKET_PROJECT_KEY`                 | `${{ github.repository_owner }}`                            |
| `BITBUCKET_PROJECT_UUID`                | `${{ github.repository_owner }}`                            |
| `BITBUCKET_STEP_TRIGGERER_UUID`         | `${{ github.actor_id }}`                                    |
| `BITBUCKET_SSH_KEY_FILE`                | `${{ github.workspace }}/.ssh/id_rsa`                       |
| `BITBUCKET_STEP_OIDC_TOKEN`             | Sem mapeamento                                              |
| `BITBUCKET_DEPLOYMENT_ENVIRONMENT`      | Sem mapeamento                                              |
| `BITBUCKET_DEPLOYMENT_ENVIRONMENT_UUID` | Sem mapeamento                                              |
| `BITBUCKET_BOOKMARK`                    | Sem mapeamento                                              |
| `BITBUCKET_PARALLEL_STEP`               | Sem mapeamento                                              |
| `BITBUCKET_PARALLEL_STEP_COUNT`         | Sem mapeamento                                              |

### Variáveis do sistema { #system-variables }

As variáveis do sistema usadas em tarefas são transformadas na variável de shell de bash equivalente e são consideradas disponíveis. Por exemplo, `${system.<variable.name>}` será transformado em `$variable_name`. Recomendamos que você verifique isso para garantir a operação adequada do fluxo de trabalho.

## Aviso legal { #legal-notice }

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
