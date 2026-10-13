---
title: Visualizar o tempo de execução do trabalho
description: Você pode visualizar o tempo de execução de um trabalho, incluindo os minutos faturáveis que um trabalho acumulou.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/view-job-execution-time
captured: '2026-10-13'
section: How tos / Monitor workflows
---

# Visualizar o tempo de execução do trabalho { #viewing-job-execution-time }

_Você pode visualizar o tempo de execução de um trabalho, incluindo os minutos faturáveis que um trabalho acumulou._

Os minutos de execução de um trabalho faturável são exibidos para trabalhos executados em repositórios privados que usam executores hospedados em GitHub e são arredondados para o próximo minuto. Não há minutos faturáveis ao usar GitHub Actions em repositórios públicos ou para trabalhos executados em executores auto-hospedados.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. No resumo do trabalho, você pode ver o tempo de execução do trabalho.
6. Para exibir detalhes sobre o tempo de execução faturável do trabalho, na barra lateral esquerda, em "Detalhes da execução", clique em **(stopwatch)Uso**.

!!! note

   > O tempo faturável exibido não inclui multiplicadores de minutos. Para ver o uso total GitHub Actions, incluindo multiplicadores de minutos, consulte [Como exibir o uso de licenças e produtos mensuráveis](https://docs.github.com/pt/billing/how-tos/products/view-productlicense-use).
