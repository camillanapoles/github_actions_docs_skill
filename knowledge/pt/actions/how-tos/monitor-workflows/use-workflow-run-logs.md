---
title: Usando registros de execução de fluxo de trabalho
description: Você pode visualizar, pesquisar e fazer download dos logs para cada trabalho em uma execução de fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/use-workflow-run-logs
captured: '2026-10-11'
section: GitHub Actions
---

# Usando registros de execução de fluxo de trabalho

_Você pode visualizar, pesquisar e fazer download dos logs para cada trabalho em uma execução de fluxo de trabalho._

Na página de execução de fluxo de trabalho, você pode verificar se a execução está em andamento ou foi concluída. Você deve estar conectado a uma GitHub conta para exibir informações de execução de fluxo de trabalho, inclusive para repositórios públicos. Para saber mais, confira [Permissões de acesso no GitHub](https://docs.github.com/pt/get-started/learning-about-github/access-permissions-on-github).

Se a execução estiver concluída, será possível ver se o resultado teve êxito, se houve falha, se foi cancelado ou se ficou neutro. Em caso de falha, você poderá exibir e pesquisar os logs de criação para diagnosticar a falha e executar o fluxo de trabalho novamente. Você também pode visualizar os minutos da execução do trabalho faturável ou fazer o download dos registros e criar artefatos.

GitHub Actions use a API de Verificações para gerar status, resultados e logs para um fluxo de trabalho.
GitHub cria um novo conjunto de verificações para cada execução de fluxo de trabalho. O conjunto de verificações contêm uma execução de verificação para cada trabalho no fluxo de trabalho, e cada trabalho inclui etapas.
GitHub Actions são executados como uma etapa em um fluxo de trabalho. Para saber mais sobre a API de Verificações, confira [Pontos de extremidade da API REST para verificações](https://docs.github.com/pt/rest/checks).

> \[!NOTE]
> Faça commit apenas de arquivos de fluxo de trabalho válidos em seu repositório. Se `.github/workflows` contiver um arquivo de fluxo de trabalho inválido, GitHub Actions gerará uma execução de fluxo de trabalho com falha para cada nova confirmação.

## Exibir logs para diagnosticar falhas

Se houver falha na execução do fluxo de trabalho, você poderá ver qual etapa causou a falha e revisar os logs de criação da etapa com falha para resolver os problemas. Também é possível ver a duração da execução de cada etapa. Além disso, você pode copiar um permalink para determinada linha no arquivo de log a fim de compartilhar com a sua equipe. É necessário o acesso de leitura ao repositório é para executar essas etapas.

Além das etapas configuradas no arquivo de fluxo de trabalho, GitHub adiciona duas etapas adicionais a cada trabalho para configurar e concluir a execução do trabalho. Estas etapas estão registradas na execução do fluxo de trabalho com os nomes "Configurar trabalho" e "Concluir trabalho".

Para trabalhos executados em executores hospedados no GitHub, "Configurar trabalho" registra os detalhes da imagem do executor e inclui um link para a lista de ferramentas pré-instaladas que estavam presentes na máquina do executor.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. Todas as etapas com falha são automaticamente expandidas para exibir os resultados.
7. Para obter um link para uma linha específica nos logs, clique no número da linha da etapa. Em seguida, você pode copiar o link da barra de endereço do seu navegador da web.

   ![Captura de tela dos logs de um trabalho. Os logs de uma etapa com falha são expandidos, e um número de linha está realçado com um contorno laranja.](/assets/images/help/repository/copy-link-button-updated-2.png)

## Pesquisar registros

É possível pesquisar os logs de criação em determinadas etapas. Quando você pesquisa os logs, somente as etapas expandidas são incluídas nos resultados. É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. No canto superior direito da saída do log, na caixa de pesquisa **Pesquisar logs**, digite uma consulta de pesquisa.

## Baixar registros

Você pode fazer o download dos arquivos de registro da execução do seu fluxo de trabalho. Você também pode fazer o download dos artefatos de um fluxo de trabalho. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../tutorials/store-and-share-data.md). É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Trabalhos** ou no grafo de visualização, clique no trabalho que deseja ver.
6. No canto superior direito do log, selecione o menu suspenso <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="Show options" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> e, em seguida, clique em **Baixar arquivo de log**.

   ![Captura de tela do log de uma tarefa. No cabeçalho, um ícone de engrenagem está destacado em laranja escuro.](/assets/images/help/actions/download-logs-drop-down.png)

> \[!NOTE]
> Quando você baixa o arquivo morto de log de um fluxo de trabalho que foi parcialmente executado novamente, o arquivo morto só inclui os trabalhos que foram executados de novo. Para obter um conjunto completo de logs de trabalhos que foram executados a partir de um fluxo de trabalho, você deve fazer o download dos arquivos de logs para as tentativas anteriores que executaram os outros trabalhos.

## Excluir registros

Você pode excluir os arquivos de log das execuções do seu fluxo de trabalho por meio da interface web GitHub ou programaticamente. É necessário o acesso de gravação ao repositório é para executar essas etapas.

### Excluindo logs por meio da interface da Web GitHub

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. No canto superior direito, selecione o menu suspenso <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="Show workflow options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> e, em seguida, clique em **Excluir todos os logs**.

   ![Captura de tela da página de um fluxo de trabalho executado. No canto superior direito, há um botão, rotulado com um ícone de kebab, com um contorno laranja escuro.](/assets/images/help/actions/workflow-run-kebab-horizontal-icon.png)

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

## Exibindo logs com GitHub CLI

> \[!NOTE]
> Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

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
