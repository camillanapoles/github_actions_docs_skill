---
title: Visualizar o tempo de execução do trabalho
description: Você pode visualizar o tempo de execução de um trabalho, incluindo os minutos faturáveis que um trabalho acumulou.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/view-job-execution-time
captured: '2026-10-11'
section: GitHub Actions
---

# Visualizar o tempo de execução do trabalho

_Você pode visualizar o tempo de execução de um trabalho, incluindo os minutos faturáveis que um trabalho acumulou._

Os minutos de execução de um trabalho faturável são exibidos para trabalhos executados em repositórios privados que usam executores hospedados em GitHub e são arredondados para o próximo minuto. Não há minutos faturáveis ao usar GitHub Actions em repositórios públicos ou para trabalhos executados em executores auto-hospedados.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. No resumo do trabalho, você pode ver o tempo de execução do trabalho.
6. Para exibir detalhes sobre o tempo de execução faturável do trabalho, na barra lateral esquerda, em "Detalhes da execução", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-stopwatch" aria-label="stopwatch" role="img"><path d="M5.75.75A.75.75 0 0 1 6.5 0h3a.75.75 0 0 1 0 1.5h-.75v1l-.001.041a6.724 6.724 0 0 1 3.464 1.435l.007-.006.75-.75a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734l-.75.75-.006.007a6.75 6.75 0 1 1-10.548 0L2.72 5.03l-.75-.75a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018l.75.75.007.006A6.72 6.72 0 0 1 7.25 2.541V1.5H6.5a.75.75 0 0 1-.75-.75ZM8 14.5a5.25 5.25 0 1 0-.001-10.501A5.25 5.25 0 0 0 8 14.5Zm.389-6.7 1.33-1.33a.75.75 0 1 1 1.061 1.06L9.45 8.861A1.503 1.503 0 0 1 8 10.75a1.499 1.499 0 1 1 .389-2.95Z"></path></svg>Uso**.

   > \[!NOTE]
   > O tempo faturável exibido não inclui multiplicadores de minutos. Para ver o uso total GitHub Actions, incluindo multiplicadores de minutos, consulte [Como exibir o uso de licenças e produtos mensuráveis](https://docs.github.com/pt/billing/how-tos/products/view-productlicense-use).
