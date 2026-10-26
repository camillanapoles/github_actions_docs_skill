---
title: Como ver as métricas do GitHub Actions
description: Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/administer/view-metrics
captured: '2026-10-26'
section: How tos / Administer
---

# Como ver as métricas do GitHub Actions

_Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo._

## Exibindo GitHub Actions métricas para sua organização

!!! note
    Pode haver uma discrepância entre a contagem de trabalhos da guia **Fluxos de Trabalho** e a contagem da guia **Trabalhos** devido a diferenças em como os trabalhos únicos são identificados. Isso não afeta o total de minutos calculados.

1. No canto superior direito de GitHub, clique na foto de perfil e clique em **(organization) Your organizations**.
2. Clique no nome da sua organização.
3. No nome da organização, clique em **(graph) Insights**.

   ![Captura de tela da barra de navegação horizontal para uma organização. Uma guia, rotulada com um ícone de grafo e "Insights" tem um contorno laranja escuro.](https://docs.github.com/assets/images/help/organizations/org-nav-insights-tab.png)
4. No menu de navegação “Insights”, selecione **Métricas de Uso do Actions** ou **Métricas de Desempenho do Actions**.
5. Opcionalmente, para selecionar um período de tempo para exibir as métricas de uso, escolha uma opção no menu suspenso **Período** no canto superior direito da página. Para saber mais, confira [Como ver as métricas do GitHub Actions](view-metrics.md#understanding-github-actions-metrics-aggregation).
6. Selecione a guia que contém as métricas que deseja ver. Para saber mais, confira [Sobre as métricas do GitHub Actions](../../concepts/metrics.md).
7. Opcionalmente, para filtrar os dados exibidos em uma guia, crie um filtro.
   1. Clique no **(filter) botão Filtrar** .
   2. Clique **(plus) Adicionar um filtro**.
   3. Escolha uma métrica pela qual você gostaria de filtrar os resultados.
   4. Dependendo da métrica escolhida, preencha as informações nas colunas "Qualificador", "Operador" e "Valor".
   5. Opcionalmente, clique em **(plus) Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
8. Opcionalmente, para baixar as métricas de uso em um arquivo CSV, clique em (Download report).

## Exibindo GitHub Actions métricas para seu repositório

!!! note
    Pode haver uma discrepância entre a contagem de trabalhos da guia **Fluxos de Trabalho** e a contagem da guia **Trabalhos** devido a diferenças em como os trabalhos únicos são identificados. Isso não afeta o total de minutos calculados.

1. Em GitHub, acesse a página principal do repositório.
2. Abaixo do nome do repositório, clique na guia **(graph) Insights**.
3. No menu de navegação “Insights”, selecione **Métricas de Uso do Actions** ou **Métricas de Desempenho do Actions**.
4. Opcionalmente, para selecionar um período de tempo para exibir as métricas de uso, escolha uma opção no menu suspenso **Período** no canto superior direito da página. Para saber mais, confira [Como ver as métricas do GitHub Actions](view-metrics.md#understanding-github-actions-metrics-aggregation).
5. Selecione a guia que contém as métricas que deseja ver. Para saber mais, confira [Sobre as métricas do GitHub Actions](../../concepts/metrics.md).
6. Opcionalmente, para filtrar os dados exibidos em uma guia, crie um filtro.
   1. Clique no **(filter) botão Filtrar** .
   2. Clique **(plus) Adicionar um filtro**.
   3. Escolha uma métrica pela qual você gostaria de filtrar os resultados.
   4. Dependendo da métrica escolhida, preencha as informações nas colunas "Qualificador", "Operador" e "Valor".
   5. Opcionalmente, clique em **(plus) Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
7. Opcionalmente, para baixar as métricas de uso em um arquivo CSV, clique em (Download report).

## Noções básicas sobre GitHub Actions agregação de métricas

O recurso de seleção de período permite que você veja as métricas do GitHub Actions em períodos predefinidos, conforme detalhado na tabela a seguir. Essas métricas excluem execuções ignoradas e aquelas que usam zero minutos. Os dados são apresentados usando dias em Tempo Universal Coordenado (UTC).

| Período | Descrição |
| --- | --- |
| Semana atual (seg-dom) | Dados de segunda-feira até o dia atual em que a página é visualizada. |
| Mês atual | Dados do primeiro dia do mês até o dia atual em que a página é visualizada. |
| Mês passado | Dados do primeiro ao último dia do mês anterior. |
| Últimos 30 dias | Dados dos últimos 30 dias até quando a página é visualizada. |
| Últimos 90 dias | Dados dos últimos 90 dias até quando a página é visualizada. |
| Último ano | Dados agregados dos últimos 12 meses. |
| Personalizado | Dados de um intervalo de datas personalizado. O intervalo pode ser de até 100 dias, incluindo as datas de início e término, e voltar até um ano. |
