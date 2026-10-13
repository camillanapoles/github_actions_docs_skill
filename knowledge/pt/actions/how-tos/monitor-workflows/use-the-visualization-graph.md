---
title: Usar o gráfico de visualização
description: Cada execução de fluxo de trabalho gera um gráfico em tempo real que ilustra o progresso da execução. Você pode usar este gráfico para monitorar e depurar fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/use-the-visualization-graph
captured: '2026-10-13'
section: How tos / Monitor workflows
---

# Usar o gráfico de visualização

_Cada execução de fluxo de trabalho gera um gráfico em tempo real que ilustra o progresso da execução. Você pode usar este gráfico para monitorar e depurar fluxos de trabalho._

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. O gráfico exibe cada trabalho no fluxo de trabalho. Um ícone à esquerda do nome do trabalho indica o status do trabalho. As linhas entre as trabalhos indicam dependências.

   ![Captura de tela do gráfico de execução de um fluxo de trabalho.](https://docs.github.com/assets/images/help/actions/workflow-graph.png)

6. Para ver o registro de tarefas, clique sobre o trabalho.
