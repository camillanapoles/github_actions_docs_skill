---
title: Como ver as métricas do GitHub Actions
description: Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/administer/view-metrics
captured: '2026-10-11'
section: GitHub Actions
---

# Como ver as métricas do GitHub Actions

_Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo._

## Exibindo GitHub Actions métricas para sua organização

> \[!NOTE]
> Pode haver uma discrepância entre a contagem de trabalhos da guia **Fluxos de Trabalho** e a contagem da guia **Trabalhos** devido a diferenças em como os trabalhos únicos são identificados. Isso não afeta o total de minutos calculados.

1. No canto superior direito de GitHub, clique na foto de perfil e clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-organization" aria-label="organization" role="img"><path d="M1.75 16A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0h8.5C11.216 0 12 .784 12 1.75v12.5c0 .085-.006.168-.018.25h2.268a.25.25 0 0 0 .25-.25V8.285a.25.25 0 0 0-.111-.208l-1.055-.703a.749.749 0 1 1 .832-1.248l1.055.703c.487.325.779.871.779 1.456v5.965A1.75 1.75 0 0 1 14.25 16h-3.5a.766.766 0 0 1-.197-.026c-.099.017-.2.026-.303.026h-3a.75.75 0 0 1-.75-.75V14h-1v1.25a.75.75 0 0 1-.75.75Zm-.25-1.75c0 .138.112.25.25.25H4v-1.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 .75.75v1.25h2.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM3.75 6h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 3.75A.75.75 0 0 1 3.75 3h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 3.75Zm4 3A.75.75 0 0 1 7.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 7 6.75ZM7.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 9.75A.75.75 0 0 1 3.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 9.75ZM7.75 9h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path></svg> Your organizations**.
2. Clique no nome da sua organização.
3. No nome da organização, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-graph" aria-label="graph" role="img"><path d="M1.5 1.75V13.5h13.75a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm14.28 2.53-5.25 5.25a.75.75 0 0 1-1.06 0L7 7.06 4.28 9.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.25-3.25a.75.75 0 0 1 1.06 0L10 7.94l4.72-4.72a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg> Insights**.

   ![Captura de tela da barra de navegação horizontal para uma organização. Uma guia, rotulada com um ícone de grafo e "Insights" tem um contorno laranja escuro.](/assets/images/help/organizations/org-nav-insights-tab.png)
4. No menu de navegação “Insights”, selecione **Métricas de Uso do Actions** ou **Métricas de Desempenho do Actions**.
5. Opcionalmente, para selecionar um período de tempo para exibir as métricas de uso, escolha uma opção no menu suspenso **Período** no canto superior direito da página. Para saber mais, confira [Como ver as métricas do GitHub Actions](view-metrics.md#understanding-github-actions-metrics-aggregation).
6. Selecione a guia que contém as métricas que deseja ver. Para saber mais, confira [Sobre as métricas do GitHub Actions](../../concepts/metrics.md).
7. Opcionalmente, para filtrar os dados exibidos em uma guia, crie um filtro.
   1. Clique no **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-filter" aria-label="filter" role="img"><path d="M.75 3h14.5a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1 0-1.5ZM3 7.75A.75.75 0 0 1 3.75 7h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 3 7.75Zm3 4a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg> botão Filtrar** .
   2. Clique **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro**.
   3. Escolha uma métrica pela qual você gostaria de filtrar os resultados.
   4. Dependendo da métrica escolhida, preencha as informações nas colunas "Qualificador", "Operador" e "Valor".
   5. Opcionalmente, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
8. Opcionalmente, para baixar as métricas de uso em um arquivo CSV, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-download" aria-label="Download report" role="img"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"></path><path d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.969a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.78a.749.749 0 1 1 1.06-1.06l1.97 1.969Z"></path></svg>.

## Exibindo GitHub Actions métricas para seu repositório

> \[!NOTE]
> Pode haver uma discrepância entre a contagem de trabalhos da guia **Fluxos de Trabalho** e a contagem da guia **Trabalhos** devido a diferenças em como os trabalhos únicos são identificados. Isso não afeta o total de minutos calculados.

1. Em GitHub, acesse a página principal do repositório.
2. Abaixo do nome do repositório, clique na guia **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-graph" aria-label="graph" role="img"><path d="M1.5 1.75V13.5h13.75a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm14.28 2.53-5.25 5.25a.75.75 0 0 1-1.06 0L7 7.06 4.28 9.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.25-3.25a.75.75 0 0 1 1.06 0L10 7.94l4.72-4.72a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg> Insights**.
3. No menu de navegação “Insights”, selecione **Métricas de Uso do Actions** ou **Métricas de Desempenho do Actions**.
4. Opcionalmente, para selecionar um período de tempo para exibir as métricas de uso, escolha uma opção no menu suspenso **Período** no canto superior direito da página. Para saber mais, confira [Como ver as métricas do GitHub Actions](view-metrics.md#understanding-github-actions-metrics-aggregation).
5. Selecione a guia que contém as métricas que deseja ver. Para saber mais, confira [Sobre as métricas do GitHub Actions](../../concepts/metrics.md).
6. Opcionalmente, para filtrar os dados exibidos em uma guia, crie um filtro.
   1. Clique no **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-filter" aria-label="filter" role="img"><path d="M.75 3h14.5a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1 0-1.5ZM3 7.75A.75.75 0 0 1 3.75 7h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 3 7.75Zm3 4a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg> botão Filtrar** .
   2. Clique **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro**.
   3. Escolha uma métrica pela qual você gostaria de filtrar os resultados.
   4. Dependendo da métrica escolhida, preencha as informações nas colunas "Qualificador", "Operador" e "Valor".
   5. Opcionalmente, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
7. Opcionalmente, para baixar as métricas de uso em um arquivo CSV, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-download" aria-label="Download report" role="img"><path d="M2.75 14A1.75 1.75 0 0 1 1 12.25v-2.5a.75.75 0 0 1 1.5 0v2.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25v-2.5a.75.75 0 0 1 1.5 0v2.5A1.75 1.75 0 0 1 13.25 14Z"></path><path d="M7.25 7.689V2a.75.75 0 0 1 1.5 0v5.689l1.97-1.969a.749.749 0 1 1 1.06 1.06l-3.25 3.25a.749.749 0 0 1-1.06 0L4.22 6.78a.749.749 0 1 1 1.06-1.06l1.97 1.969Z"></path></svg>.

## Noções básicas sobre GitHub Actions agregação de métricas

O recurso de seleção de período permite que você veja as métricas do GitHub Actions em períodos predefinidos, conforme detalhado na tabela a seguir. Essas métricas excluem execuções ignoradas e aquelas que usam zero minutos. Os dados são apresentados usando dias em Tempo Universal Coordenado (UTC).

<div class="ghd-tool rowheaders">

| Período                | Descrição                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Semana atual (seg-dom) | Dados de segunda-feira até o dia atual em que a página é visualizada.                                                                            |
| Mês atual              | Dados do primeiro dia do mês até o dia atual em que a página é visualizada.                                                                      |
| Mês passado            | Dados do primeiro ao último dia do mês anterior.                                                                                                 |
| Últimos 30 dias        | Dados dos últimos 30 dias até quando a página é visualizada.                                                                                     |
| Últimos 90 dias        | Dados dos últimos 90 dias até quando a página é visualizada.                                                                                     |
| Último ano             | Dados agregados dos últimos 12 meses.                                                                                                            |
| Personalizado          | Dados de um intervalo de datas personalizado. O intervalo pode ser de até 100 dias, incluindo as datas de início e término, e voltar até um ano. |

</div>
