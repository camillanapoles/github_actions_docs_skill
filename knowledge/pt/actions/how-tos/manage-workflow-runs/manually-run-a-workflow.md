---
title: Executar um fluxo de trabalho manualmente
description: Quando um fluxo de trabalho é configurado para ser executado no workflow_dispatch evento, você pode executar o fluxo de trabalho usando a guia GitHubGitHub CLIAções, ou a API REST.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/manually-run-a-workflow
captured: '2026-10-19'
section: How tos / Manage workflow runs
---

# Executar um fluxo de trabalho manualmente

_Quando um fluxo de trabalho é configurado para ser executado no workflow_dispatch evento, você pode executar o fluxo de trabalho usando a guia GitHubGitHub CLIAções, ou a API REST._

## Configurar um fluxo de trabalho para ser executado manualmente

Para executar um fluxo de trabalho manualmente, o fluxo de trabalho precisa ser configurado para ser executado no evento `workflow_dispatch`.

Para disparar o evento `workflow_dispatch`, seu fluxo de trabalho precisa estar no branch padrão. Para saber mais sobre a configuração do evento `workflow_dispatch`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch).

É necessário o acesso de gravação ao repositório é para executar essas etapas.

## Executando um fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no nome do fluxo de trabalho que deseja executar.

   ![Captura de tela da página "Ações". Na barra lateral esquerda, o nome do fluxo de trabalho está realçado com um contorno em laranja escuro.](https://docs.github.com/assets/images/help/repository/actions-select-workflow-2022.png)

4. Clique no botão **Executar fluxo de trabalho**, que fica acima da lista de execuções de fluxo de trabalho.

!!! note

   > Para você ver o botão **Run workflow**, o arquivo de fluxo de trabalho precisa usar o gatilho de evento `workflow_dispatch`. Somente os arquivos de fluxo de trabalho que usam o gatilho do evento `workflow_dispatch` têm a opção de executar o fluxo de trabalho manualmente usando o botão **Executar fluxo de trabalho**. Para saber mais sobre a configuração do evento `workflow_dispatch`, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch).

   ![Captura de tela da página de fluxo de trabalho. Acima da lista de execuções de fluxo de trabalho, o botão rotulado como "Executar fluxo de trabalho" está delineado em laranja escuro.](https://docs.github.com/assets/images/help/actions/actions-workflow-dispatch.png)

5. Selecione o menu suspenso **Branch** e clique em um branch para executar o fluxo de trabalho.

6. Se o fluxo de trabalho exigir entradas, preencha os campos.

7. Clique em **Executar fluxo de trabalho**.

!!! note
    Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

Para executar um fluxo de trabalho, use o subcomando `workflow run`. Substitua o parâmetro `workflow` pelo nome, pela ID ou pelo nome do arquivo de fluxo de trabalho que deseja executar. Por exemplo, `"Link Checker"`, `1234567` ou `"link-check-test.yml"`. Se você não especificar um fluxo de trabalho, GitHub CLI retornará um menu interativo para escolher um fluxo de trabalho.

```shell
gh workflow run WORKFLOW
```

Se o fluxo de trabalho aceitar entradas, GitHub CLI solicitará que você as insira. Como alternativa, você pode usar `-f` ou `-F` para adicionar uma entrada no formato `key=value`. Use `-F` para fazer a leitura de um arquivo.

```shell
gh workflow run greet.yml -f name=mona -f greeting=hello -F data=@myfile.txt
```

Você também pode passar as entradas como JSON usando a entrada padrão.

```shell
echo '{"name":"mona", "greeting":"hello"}' | gh workflow run greet.yml --json
```

Para executar um fluxo de trabalho em um branch que não seja o branch padrão do repositório, use o sinalizador `--ref`.

```shell
gh workflow run WORKFLOW --ref BRANCH
```

Para ver o progresso da execução do fluxo de trabalho, use o subcomando `run watch` e selecione a execução na lista interativa.

```shell
gh run watch
```

## Executar um fluxo de trabalho usando a API REST

Ao usar a API REST, você configura os parâmetros do corpo da solicitação `inputs` e `ref`. Se as entradas forem omitidas, serão usados os valores-padrão definidos no arquivo de fluxo de trabalho.

!!! note
    Você pode definir até 25 `inputs`para um `workflow_dispatch` evento.

Para saber mais sobre o uso da API REST, confira [Endpoints da API REST para fluxos de trabalho](https://docs.github.com/pt/rest/actions/workflows#create-a-workflow-dispatch-event).
