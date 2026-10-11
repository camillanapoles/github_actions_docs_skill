---
title: Remover artefatos de fluxo de trabalho
description: Você pode recuperar o armazenamento usado GitHub Actions excluindo artefatos antes que eles expirem GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Remover artefatos de fluxo de trabalho { #removing-workflow-artifacts }

_Você pode recuperar o armazenamento usado GitHub Actions excluindo artefatos antes que eles expirem GitHub._

## Excluir um artefato { #deleting-an-artifact }

!!! warning
    Depois que você excluir um artefato, ele não poderá ser restaurado.

É necessário o acesso de gravação ao repositório é para executar essas etapas.

Por padrão, GitHub armazena logs de build e artefatos por 90 dias e esse período de retenção pode ser personalizado. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-repository).

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. Em **Artefatos**, clique (Remove artifact ARTIFACT-NAME) ao lado do artefato que você deseja remover.

   ![Captura de tela mostrando artefatos criados durante uma execução de fluxo de trabalho. Um ícone de lixeira, usado para remover um artefato, está contornado em laranja escuro.](/assets/images/help/repository/actions-delete-artifact-updated.png)

## Definir o período de retenção para um artefato { #setting-the-retention-period-for-an-artifact }

Os períodos de retenção para artefatos e registros podem ser configurados no repositório, organização e no nível corporativo. Para obter mais informações, consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#setting-the-check-workflow-run-status-artifact-and-log-retention-period-for-a-repository) e [Configurando o período de retenção para verificações, execuções de fluxo de trabalho, status de confirmação, artefatos e logs em sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization).

Você também pode definir um período de retenção personalizado para artefatos individuais usando a ação `actions/upload-artifact` em um fluxo de trabalho. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../tutorials/store-and-share-data.md#configuring-a-custom-artifact-retention-period).

## Localizar a data de expiração de um artefato { #finding-the-expiration-date-of-an-artifact }

Você pode usar a API para confirmar a data em que um artefato está agendado para ser excluído. Para obter mais informações, confira o valor de `expires_at` retornado pela API REST. Para saber mais, confira [Pontos de extremidade de API REST para artefatos do GitHub Actions](https://docs.github.com/pt/rest/actions/artifacts).

## Artefatos de execuções de fluxo de trabalho excluídas { #artifacts-from-deleted-workflow-runs }

Quando uma execução de fluxo de trabalho é excluída, todos os artefatos associados a ela também são excluídos do armazenamento. Você pode excluir uma execução de fluxo de trabalho usando a interface do usuário do GitHub Actions, a API REST ou a CLI do GitHub, confira: [Excluir a execução de um fluxo de trabalho](delete-a-workflow-run.md), [Excluir uma execução de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#delete-a-workflow-run) ou [gh run delete](https://cli.github.com/manual/gh_run_delete).
