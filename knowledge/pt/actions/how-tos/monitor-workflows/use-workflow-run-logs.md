---
title: Usando registros de execução de fluxo de trabalho
description: Você pode visualizar, pesquisar e fazer download dos logs para cada trabalho em uma execução de fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/use-workflow-run-logs
captured: '2026-10-26'
section: How tos / Monitor workflows
---

# Usando registros de execução de fluxo de trabalho

_Você pode visualizar, pesquisar e fazer download dos logs para cada trabalho em uma execução de fluxo de trabalho._

Na página de execução de fluxo de trabalho, você pode verificar se a execução está em andamento ou foi concluída. Você deve estar conectado a uma GitHub conta para exibir informações de execução de fluxo de trabalho, inclusive para repositórios públicos. Para saber mais, confira [Permissões de acesso no GitHub](https://docs.github.com/pt/get-started/learning-about-github/access-permissions-on-github).

Se a execução estiver concluída, será possível ver se o resultado teve êxito, se houve falha, se foi cancelado ou se ficou neutro. Em caso de falha, você poderá exibir e pesquisar os logs de criação para diagnosticar a falha e executar o fluxo de trabalho novamente. Você também pode visualizar os minutos da execução do trabalho faturável ou fazer o download dos registros e criar artefatos.

GitHub Actions use a API de Verificações para gerar status, resultados e logs para um fluxo de trabalho.
GitHub cria um novo conjunto de verificações para cada execução de fluxo de trabalho. O conjunto de verificações contêm uma execução de verificação para cada trabalho no fluxo de trabalho, e cada trabalho inclui etapas.
GitHub Actions são executados como uma etapa em um fluxo de trabalho. Para saber mais sobre a API de Verificações, confira [Pontos de extremidade da API REST para verificações](https://docs.github.com/pt/rest/checks).

!!! note
    Faça commit apenas de arquivos de fluxo de trabalho válidos em seu repositório. Se `.github/workflows` contiver um arquivo de fluxo de trabalho inválido, GitHub Actions gerará uma execução de fluxo de trabalho com falha para cada nova confirmação.

## Exibir logs para diagnosticar falhas

Se houver falha na execução do fluxo de trabalho, você poderá ver qual etapa causou a falha e revisar os logs de criação da etapa com falha para resolver os problemas. Também é possível ver a duração da execução de cada etapa. Além disso, você pode copiar um permalink para determinada linha no arquivo de log a fim de compartilhar com a sua equipe. É necessário o acesso de leitura ao repositório é para executar essas etapas.

Além das etapas configuradas no arquivo de fluxo de trabalho, GitHub adiciona duas etapas adicionais a cada trabalho para configurar e concluir a execução do trabalho. Estas etapas estão registradas na execução do fluxo de trabalho com os nomes "Configurar trabalho" e "Concluir trabalho".

Para trabalhos executados em executores hospedados no GitHub, "Configurar trabalho" registra os detalhes da imagem do executor e inclui um link para a lista de ferramentas pré-instaladas que estavam presentes na máquina do executor.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. Todas as etapas com falha são automaticamente expandidas para exibir os resultados.
7. Para obter um link para uma linha específica nos logs, clique no número da linha da etapa. Em seguida, você pode copiar o link da barra de endereço do seu navegador da web.

   ![Captura de tela dos logs de um trabalho. Os logs de uma etapa com falha são expandidos, e um número de linha está realçado com um contorno laranja.](https://docs.github.com/assets/images/help/repository/copy-link-button-updated-2.png)

## Pesquisar registros

É possível pesquisar os logs de criação em determinadas etapas. Quando você pesquisa os logs, somente as etapas expandidas são incluídas nos resultados. É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. No canto superior direito da saída do log, na caixa de pesquisa **Pesquisar logs**, digite uma consulta de pesquisa.

## Baixar registros

Você pode fazer o download dos arquivos de registro da execução do seu fluxo de trabalho. Você também pode fazer o download dos artefatos de um fluxo de trabalho. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../tutorials/store-and-share-data.md). É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. No canto superior direito do log, selecione o menu suspenso (Show options) e, em seguida, clique em **Baixar arquivo de log**.

   ![Captura de tela do log de uma tarefa. No cabeçalho, um ícone de engrenagem está destacado em laranja escuro.](https://docs.github.com/assets/images/help/actions/download-logs-drop-down.png)

!!! note
    Quando você baixa o arquivo morto de log de um fluxo de trabalho que foi parcialmente executado novamente, o arquivo morto só inclui os trabalhos que foram executados de novo. Para obter um conjunto completo de logs de trabalhos que foram executados a partir de um fluxo de trabalho, você deve fazer o download dos arquivos de logs para as tentativas anteriores que executaram os outros trabalhos.

## Excluir registros

Você pode excluir os arquivos de log das execuções do seu fluxo de trabalho por meio da interface web GitHub ou programaticamente. É necessário o acesso de gravação ao repositório é para executar essas etapas.

### Excluindo logs por meio da interface da Web GitHub

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. No canto superior direito, selecione o menu suspenso (Show workflow options) e, em seguida, clique em **Excluir todos os logs**.

   ![Captura de tela da página de um fluxo de trabalho executado. No canto superior direito, há um botão, rotulado com um ícone de kebab, com um contorno laranja escuro.](https://docs.github.com/assets/images/help/actions/workflow-run-kebab-horizontal-icon.png)

6. Leia o aviso de confirmação.

Após a exclusão dos logs, o botão **Excluir todos os logs** é removido para indicar que nenhum arquivo de log permanece na execução de fluxo de trabalho.

### Excluir logs programaticamente

Você pode usar o script a seguir para excluir automaticamente todos os logs de um fluxo de trabalho. Essa pode ser uma maneira útil de limpar logs para várias execuções de fluxo de trabalho.

Para executar o script de exemplo abaixo:

1. Copie o exemplo de código e salve-o em um arquivo chamado `delete-logs.sh`.
2. Conceda a ele a permissão de execução com `chmod +x delete-logs.sh`.
3. Execute o comando a seguir, em que `REPOSITORY_NAME` é o nome do repositório e `WORKFLOW_NAME` é o nome do arquivo do fluxo de trabalho.

            ```shell copy
   ./delete-logs.sh REPOSITORY_NAME WORKFLOW_NAME
   ```

   Por exemplo, para excluir todos os logs no repositório `monalisa/octocat` do fluxo de trabalho `.github/workflows/ci.yaml`, você executaria `./delete-logs.sh monalisa/octocat ci.yaml`.

#### Script de exemplo

```bash copy
#!/usr/bin/env bash

```
# Delete all logs for a given workflow
# Usage: delete-logs.sh <repository> <workflow-name>

set -oe pipefail

REPOSITORY=$1
WORKFLOW_NAME=$2

# Validate arguments
if [[ -z "$REPOSITORY" ]]; then
  echo "Repository is required"
  exit 1
fi

if [[ -z "$WORKFLOW_NAME" ]]; then
  echo "Workflow name is required"
  exit 1
fi

echo "Getting all completed runs for workflow $WORKFLOW_NAME in $REPOSITORY"

RUNS=$(
  gh api \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "/repos/$REPOSITORY/actions/workflows/$WORKFLOW_NAME/runs" \
    --paginate \
    --jq '.workflow_runs[] | select(.conclusion != "") | .id'
)

echo "Found $(echo "$RUNS" | wc -l) completed runs for workflow $WORKFLOW_NAME"

# Delete logs for each run
for RUN in $RUNS; do
  echo "Deleting logs for run $RUN"
  gh api \
    --silent \
    --method DELETE \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "/repos/$REPOSITORY/actions/runs/$RUN/logs" || echo "Failed to delete logs for run $RUN"

  # Sleep for 100ms to avoid rate limiting
  sleep 0.1
done
```

```
## Exibindo logs com GitHub CLI

!!! note
    Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

Para ver o log de um trabalho específico, use o subcomando `run view`. Substitua `run-id` pela ID da execução para a qual deseja ver os logs.
GitHub CLI retorna um menu interativo para você escolher um trabalho na execução. Se você não especificar `run-id`, GitHub CLI exibirá um menu interativo para que você escolha uma execução recente e, em seguida, exibirá outro menu interativo para que você escolha uma tarefa dessa execução.

```shell
gh run view RUN_ID --log
```

Use também o sinalizador `--job` para especificar uma ID de trabalho. Substitua `job-id` pela ID do trabalho para o qual você deseja ver os logs.

```shell
gh run view --job JOB_ID --log
```

Você pode usar `grep` para buscar no log. Por exemplo, este comando retornará todas as entradas do log que contêm a palavra `error`.

```shell
gh run view --job JOB_ID --log | grep error
```

Para filtrar os logs de qualquer etapa com falha, use `--log-failed` em vez de `--log`.

```shell
gh run view --job JOB_ID --log-failed
```
