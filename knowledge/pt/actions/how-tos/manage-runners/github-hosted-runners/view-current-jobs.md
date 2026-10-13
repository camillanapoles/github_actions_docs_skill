---
title: Visualizando suas tarefas atuais
description: Monitore como GitHubos executores hospedados estão processando trabalhos em sua organização ou empresa e identifique quaisquer restrições relacionadas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/view-current-jobs
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners
---

# Visualizando suas tarefas atuais { #viewing-your-current-jobs }

_Monitore como GitHubos executores hospedados estão processando trabalhos em sua organização ou empresa e identifique quaisquer restrições relacionadas._

## Visualização de trabalhos ativos na sua organização ou empresa { #viewing-active-jobs-in-your-organization-or-enterprise }

Você pode obter uma lista de todos os trabalhos atualmente em execução em GitHubexecutores hospedados em sua organização ou empresa.

1. Acesse a página principal da organização ou repositório.

2. Clique em **(gear) Settings**.

3. Na barra lateral esquerda, clique em **Actions** e em **Executores**.

4. Na tabela "Executores", clique na entrada de **Executores hospedados pelo GitHub**. Esta entrada só estará presente se você estiver usando executores hospedados em GitHub.

5. Examine a seção "Trabalhos ativos", que contém uma lista de todos os trabalhos atualmente em execução em GitHubexecutores hospedados.

## Visualizando tarefas em fila na sua organização ou empresa { #viewing-queued-jobs-in-your-organization-or-enterprise }

GitHubOs executores hospedados permitem que você execute trabalhos simultaneamente e o número máximo de trabalhos simultâneos variará dependendo do seu plano. Se você atingir o número máximo de trabalhos simultâneos, tdos os novos trabalhos começarão a entrar na fila. Para saber mais sobre o número de trabalhos simultâneos disponíveis para seu plano, confira [Cobrança e uso](../../../concepts/billing-and-usage.md).

O procedimento seguinte demonstra como verificar o número máximo de trabalhos simultâneos que pode ser executado.

1. Acesse a página principal da organização ou repositório.

2. Clique em **(gear) Settings**.

3. Na barra lateral esquerda, clique em **Actions** e em **Executores**.

4. Na tabela "Executores", clique na entrada de **Executores hospedados pelo GitHub**. Esta entrada só estará presente se você estiver usando executores hospedados em GitHub.

5. Revise a seção "Uso de todos os trabalhos", que lista o número de trabalhos ativos e o número máximo de trabalhos que você pode executar.
