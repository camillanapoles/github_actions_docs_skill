---
title: Visualizar o histórico de execução do fluxo de trabalho
description: Você pode visualizar registros para cada execução de um fluxo de trabalho. Os registros incluem a situação de cada trabalho e a etapa de um fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/view-workflow-run-history
captured: '2026-10-13'
section: How tos / Monitor workflows
---

# Visualizar o histórico de execução do fluxo de trabalho

_Você pode visualizar registros para cada execução de um fluxo de trabalho. Os registros incluem a situação de cada trabalho e a etapa de um fluxo de trabalho._

É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

!!! note
    Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

## Visualizando execuções de fluxo de trabalho recentes

Para listar as execuções de fluxo de trabalho recentes, use o subcomando `run list`.

```shell
gh run list
```

Para especificar o número máximo de execuções a serem retornadas, use o sinalizador `-L` ou `--limit`. O padrão é `10`.

```shell
gh run list --limit 5
```

Para retornar apenas as execuções de fluxo de trabalho especificadas, use o sinalizador `-w` ou `--workflow`. Substitua `workflow` pelo nome, pela ID ou pelo nome de arquivo do fluxo de trabalho. Por exemplo, `"Link Checker"`, `1234567` ou `"link-check-test.yml"`.

```shell
gh run list --workflow WORKFLOW
```

## Visualização de detalhes de uma execução específica do fluxo de trabalho

Para ver os detalhes de uma execução de fluxo de trabalho específica, use o subcomando `run view`. Substitua `run-id` pela ID da execução que deseja ver. Se você não especificar um `run-id`, o GitHub CLI retornará um menu interativo para você escolher uma execução recente.

```shell
gh run view RUN_ID
```

Para incluir as etapas de trabalho na saída, use o sinalizador `-v` ou `--verbose`.

```shell
gh run view RUN_ID --verbose
```

Para ver os detalhes de um trabalho específico na execução, use o sinalizador `-j` ou `--job`. Substitua `job-id` pela ID do trabalho que deseja ver.

```shell
gh run view --job JOB_ID
```

Para ver o log completo de um trabalho, use o sinalizador `--log`.

```shell
gh run view --job JOB_ID --log
```

Use o sinalizador `--exit-status` para sair com um status diferente de zero se a execução falhar. Por exemplo:

```shell
gh run view 0451 --exit-status && echo "run pending or passed"
```
