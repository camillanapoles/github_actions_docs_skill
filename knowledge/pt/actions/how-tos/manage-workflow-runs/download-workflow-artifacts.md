---
title: Baixar artefatos do fluxo de trabalho
description: Você pode fazer o download de artefatos arquivados antes que expirem automaticamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/download-workflow-artifacts
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Baixar artefatos do fluxo de trabalho { #downloading-workflow-artifacts }

_Você pode fazer o download de artefatos arquivados antes que expirem automaticamente._

Por padrão, o GitHub armazena registros e artefatos de compilação por 90 dias, e você pode personalizar este período de retenção dependendo do tipo de repositório. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-repository).

É necessário o acesso de leitura ao repositório é para executar essas etapas.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Na seção "Artefatos", clique no artefato que deseja baixar.

   ![Captura de tela da seção "Artefatos" de uma execução de fluxo de trabalho. O nome de um artefato gerado pela execução, "artefato", está destacado em laranja.](/assets/images/help/repository/artifact-drop-down-updated.png)

!!! note
    Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

GitHub CLI irá fazer o download de cada artefato em diretórios separados baseados no nome do artefato. Se apenas um único artefato for especificado, ele será extraído para o diretório atual.

Para baixar todos os artefatos gerados por uma execução de fluxo de trabalho, use o subcomando `run download`. Substitua `run-id` pela ID da execução da qual deseja baixar artefatos. Se você não especificar um `run-id`, o GitHub CLI retornará um menu interativo para você escolher uma execução recente.

```shell
gh run download RUN_ID
```

Para baixar um artefato específico de uma execução, use o subcomando `run download`. Substitua `run-id` pela ID da execução da qual deseja baixar artefatos. Substitua `artifact-name` pelo nome do artefato que deseja baixar.

```shell
gh run download RUN_ID -n ARTIFACT_NAME
```

Você pode especificar mais de um artefato.

```shell
gh run download RUN_ID> -n ARTIFACT_NAME-1 -n ARTIFACT_NAME-2
```

Para baixar artefatos específicos em todas as execuções em um repositório, use o subcomando `run download`.

```shell
gh run download -n ARTIFACT_NAME-1 ARTIFACT_NAME-2
```
