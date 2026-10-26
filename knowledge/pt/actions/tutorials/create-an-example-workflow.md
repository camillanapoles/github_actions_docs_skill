---
title: Criando um exemplo de fluxo de trabalho
description: Neste tutorial, você aprenderá a criar um fluxo de trabalho básico disparado por um evento push.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/create-an-example-workflow
captured: '2026-10-26'
section: Tutorials
---

# Criando um exemplo de fluxo de trabalho

_Neste tutorial, você aprenderá a criar um fluxo de trabalho básico disparado por um evento push._

## Introdução

Este guia mostra como criar um fluxo de trabalho básico que é disparado quando o código é enviado por push para o repositório.

Para começar a usar fluxos de trabalho pré-configurados, navegue pela lista de modelos no repositório [actions/starter-workflows](https://github.com/actions/starter-workflows). Para saber mais, confira [Usando modelos de fluxo de trabalho](../how-tos/write-workflows/use-workflow-templates.md).

> [!IMPORTANT] Para obter mais informações sobre as práticas recomendadas para proteger seus fluxos de trabalho e o uso seguro de GitHub Actions recursos, consulte [Referência de uso seguro](../reference/security/secure-use.md#writing-workflows).

## Criando um exemplo de fluxo de trabalho

GitHub Actions usa a sintaxe YAML para definir o fluxo de trabalho. Cada fluxo de trabalho é armazenado como um arquivo YAML separado no seu repositório de código, em um diretório chamado `.github/workflows`.

Você pode criar um exemplo de fluxo de trabalho no repositório que aciona automaticamente uma série de comandos sempre que o código for carregado. Neste fluxo de trabalho, GitHub Actions verifica o código enviado por push, instala a estrutura de teste [bats](https://www.npmjs.com/package/bats) e executa um comando básico para gerar a versão do bats: `bats -v`.

1. No repositório, crie o diretório `.github/workflows/` para armazenar os arquivos de fluxo de trabalho.

2. No diretório `.github/workflows/`, crie um arquivo chamado `learn-github-actions.yml` e adicione o código a seguir.

            ```yaml copy
   name: learn-github-actions
   run-name: ${{ github.actor }} is learning GitHub Actions
   on: [push]
   jobs:
     check-bats-version:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v6
         - uses: actions/setup-node@v7
           with:
             node-version: '24'
         - run: npm install -g bats
         - run: bats -v
   ```

3. Confirme essas alterações e envie-as para o seu repositório GitHub.

Seu novo GitHub Actions arquivo de fluxo de trabalho agora está instalado em seu repositório e será executado automaticamente sempre que alguém enviar uma alteração por push para o repositório. Para conferir os detalhes sobre o histórico de execução de um fluxo de trabalho, confira [Exibir a atividade de uma execução de fluxo de trabalho](#viewing-the-activity-for-a-workflow-run).

## Entender o arquivo de fluxo de trabalho

Para ajudar você a entender como a sintaxe de YAML é usada para criar um arquivo de fluxo de trabalho, esta seção explica cada linha do exemplo Introdução:

```yaml annotate copy
```
# Optional - The name of the workflow as it will appear in the "Actions" tab of the GitHub repository. If this field is omitted, the name of the workflow file will be used instead.
name: learn-github-actions

# Optional - The name for workflow runs generated from the workflow, which will appear in the list of workflow runs on your repository's "Actions" tab. This example uses an expression with the `github` context to display the username of the actor that triggered the workflow run. For more information, see [AUTOTITLE](https://docs.github.com/pt/actions/using-workflows/workflow-syntax-for-github-actions#run-name).
run-name: ${{ github.actor }} is learning GitHub Actions

# Specifies the trigger for this workflow. This example uses the `push` event, so a workflow run is triggered every time someone pushes a change to the repository or merges a pull request. This is triggered by a push to every branch; for examples of syntax that runs only on pushes to specific branches, paths, or tags, see [AUTOTITLE](https://docs.github.com/pt/actions/reference/workflow-syntax-for-github-actions#onpushpull_requestpull_request_targetpathspaths-ignore).
on: [push]

# Groups together all the jobs that run in the `learn-github-actions` workflow.
jobs:

# Defines a job named `check-bats-version`. The child keys will define properties of the job.
  check-bats-version:

# Configures the job to run on the latest version of an Ubuntu Linux runner. This means that the job will execute on a fresh virtual machine hosted by GitHub. For syntax examples using other runners, see [AUTOTITLE](https://docs.github.com/pt/actions/reference/workflow-syntax-for-github-actions#jobsjob_idruns-on)
    runs-on: ubuntu-latest

# Groups together all the steps that run in the `check-bats-version` job. Each item nested under this section is a separate action or shell script.
    steps:

# The `uses` keyword specifies that this step will run the `actions/checkout@v6` action. This is an action that checks out your repository onto the runner, allowing you to run scripts or other actions against your code (such as build and test tools). You should use the checkout action any time your workflow will use the repository's code.
      - uses: actions/checkout@v6

# This step uses the `actions/setup-node@v7` action to install the specified version of the Node.js. (This example uses version 24.) This puts both the `node` and `npm` commands in your `PATH`.
      - uses: actions/setup-node@v7
        with:
          node-version: '24'

# The `run` keyword tells the job to execute a command on the runner. In this case, you are using `npm` to install the `bats` software testing package.
      - run: npm install -g bats

# Finally, you'll run the `bats` command with a parameter that outputs the software version.
      - run: bats -v
```

```
### Visualizar o arquivo de fluxo de trabalho

Neste diagrama, você pode ver o arquivo de fluxo de trabalho que acabou de criar e como os GitHub Actions componentes são organizados em uma hierarquia. Cada etapa executa uma única ação ou script do shell. As etapas 1 e 2 executam ações, enquanto as etapas 3 e 4 executam scripts de shell. Para encontrar mais ações predefinidas para seus fluxos de trabalho, confira [Usando blocos de construção pré-gravados no seu fluxo de trabalho](../how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions.md).

![Diagrama mostrando o gatilho, o executante e a tarefa de um fluxo de trabalho. O trabalho é dividido em quatro etapas.](https://docs.github.com/assets/images/help/actions/overview-actions-event.png)

## Exibir a atividade para uma execução de fluxo de trabalho

Quando seu fluxo de trabalho é acionado, é criada uma *execução de fluxo de trabalho* que executa o fluxo de trabalho. Depois que uma execução de fluxo de trabalho for iniciada, você poderá visualizar um gráfico do progresso da execução e acompanhar a atividade de cada etapa em GitHub.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Na barra lateral esquerda ou no grafo de visualização, clique no trabalho que deseja ver.
6. Para ver os resultados de uma etapa, clique na etapa.
