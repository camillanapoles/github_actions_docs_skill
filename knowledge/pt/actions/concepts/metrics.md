---
title: Sobre as métricas do GitHub Actions
description: Saiba mais sobre as GitHub Actions métricas disponíveis para suas organizações e repositórios.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/metrics
captured: '2026-10-13'
section: Concepts
---

# Sobre as métricas do GitHub Actions { #about-github-actions-metrics }

_Saiba mais sobre as GitHub Actions métricas disponíveis para suas organizações e repositórios._

## Sobre as métricas do GitHub Actions { #about-github-actions-metrics-1 }

As métricas do GitHub Actions trazem insights sobre o desempenho dos seus fluxos de trabalho e trabalhos na organização e no repositório. Há dois tipos de métricas para ajudar você a analisar diferentes aspectos dos seus fluxos de trabalho:

* **Métricas de uso do GitHub Actions**: as métricas de uso ajudam a acompanhar os minutos consumidos pelos seus fluxos de trabalho e trabalhos. Você pode usar esses dados para entender como funciona o custo de execução do Actions e garantir que esteja dentro dos limites do seu plano. Isso é especialmente útil para identificar fluxos de trabalho ou repositórios de alto uso.
* **Métricas de desempenho do GitHub Actions**: as métricas de desempenho têm como foco a eficiência e a confiabilidade dos seus trabalhos e fluxos de trabalho. Com as métricas de desempenho, você pode monitorar indicadores importantes, como tempos de execução de trabalho, tempos de fila e taxas de falha para identificar gargalos, trabalhos de execução lenta ou fluxos de trabalho com falha frequente.

## Habilitando o acesso às GitHub Actions métricas { #enabling-access-to-github-actions-metrics }

Os proprietários da organização podem criar papéis personalizados na organização para permitir que as pessoas visualizem as GitHub Actionsmétricas de uso da organização. Para fornecer acesso aos usuários, escolha a função “Exibir métricas do Actions da organização” ao criar uma função de organização personalizada. Para saber mais, confira [Permissões de funções de organização personalizadas](https://docs.github.com/pt/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles).

## Sobre métricas de uso de GitHub Actions { #about-github-actions-usage-metrics }

As métricas de uso de GitHub Actions permitem que você analise como sua organização está usando os minutos do Actions. Você pode exibir informações de uso relacionadas a:

* **Fluxos de trabalho**. Exiba dados de uso para cada fluxo de trabalho em sua organização e use essas informações para identificar oportunidades de otimização, como refatoração de um fluxo de trabalho ou uso de um executor avançado.
* **Trabalhos.** Veja quais trabalhos consomem mais recursos e onde estão sendo executados.
* **Repositórios**. Obtenha um instantâneo de alto nível de cada repositório em sua organização e seu volume de uso de minutos do Actions.
* **SO do runtime**. Entenda como os executores de cada sistema operacional estão usando os minutos do Actions e em quais tipos de sistemas operacionais seus fluxos de trabalho estão sendo executados com mais frequência.
* **Tipo de executor**. Compare como seus executores auto-hospedados e os executores hospedados no GitHub usam os minutos do Actions e o volume de execuções do fluxo de trabalho para cada tipo de executor.

## Sobre GitHub Actions as métricas de desempenho { #about-github-actions-performance-metrics }

As métricas de desempenho do GitHub Actions permitem que você analise a eficiência e a confiabilidade dos seus fluxos de trabalho. Você pode ver informações de desempenho, como tempos médios de execução, tempos médios de fila e taxas de falha, relacionadas a:

* **Fluxos de trabalho**. Veja dados de desempenho para cada fluxo de trabalho da sua organização, incluindo tempo médio de execução e falhas de trabalho. Use essas informações para identificar fluxos de trabalho ineficientes e a estabilidade da execução.
* **Trabalhos.** Veja dados de desempenho de cada trabalho individual, incluindo tempo médio de execução, tempo médio de fila e falhas de trabalho. Use essas informações para identificar trabalhos ineficientes.
* **Repositórios**. Obtenha um snapshot de alto nível de cada repositório da sua organização e as métricas de desempenho médio.
* **SO do runtime**. Entenda como está o desempenho dos executores de cada sistema operacional.
* **Tipo de executor**. Compare o desempenho de executores auto-hospedados e dos executores hospedados no GitHub para tomar decisões sobre os tipos de executores.

## Próximas etapas { #next-steps }

Para saber como encontrar métricas para sua organização ou repositório, confira [Como ver as métricas do GitHub Actions](../how-tos/administer/view-metrics.md).
