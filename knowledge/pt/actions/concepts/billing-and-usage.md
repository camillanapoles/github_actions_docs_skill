---
title: Cobrança e uso
description: Há limites de uso para GitHub Actions fluxos de trabalho. As taxas de uso são aplicadas a repositórios que excedem a quantidade de minutos gratuitos e armazenamento disponíveis gratuitamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/billing-and-usage
captured: '2026-10-11'
section: Concepts
---

# Cobrança e uso

_Há limites de uso para GitHub Actions fluxos de trabalho. As taxas de uso são aplicadas a repositórios que excedem a quantidade de minutos gratuitos e armazenamento disponíveis gratuitamente._

## Sobre faturamento de GitHub Actions

O uso do GitHub Actions é gratuito para executores padrão hospedados por GitHub em repositórios públicos, e executores auto-hospedados. Confira [Escolhendo o executor para um trabalho](../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#standard-github-hosted-runners-for-public-repositories). Para repositórios privados, cada conta GitHub recebe uma cota de minutos e de armazenamento gratuitos para uso com executores hospedados no GitHub, de acordo com o plano da conta. Qualquer uso além dos valores incluídos é cobrado em sua conta. Para obter mais informações, consulte [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions).

## Disponibilidade

GitHub Actions está disponível em todos os produtos GitHub, mas GitHub Actions não está disponível para repositórios privados pertencentes a contas que usam planos herdados por repositório. Consulte [Planos do GitHub](https://docs.github.com/pt/get-started/learning-about-github/githubs-plans).

## Limites de uso e política

Há vários limites para o uso de GitHub Actions ao usar executores hospedados em GitHub. Confira [Limites do Actions](../reference/limits.md).

Além dos limites de uso, você deve garantir que você use GitHub Actions dentro dos [Termos de Serviço GitHub](https://docs.github.com/pt/site-policy/github-terms/github-terms-of-service). Para obter mais informações sobre os termos específicos de GitHub Actions, consulte os [Termos Adicionais de Produto do GitHub](https://docs.github.com/pt/site-policy/github-terms/github-terms-for-additional-products-and-features#actions).

## GitHub Actions métricas de uso

Os proprietários e usuários da organização com a permissão "Exibir métricas de ações da organização" podem exibir GitHub Actions métricas de uso para sua organização. Essas métricas podem ajudar a entender como e onde seus Minutos de ações estão sendo usados. Para saber mais, confira [Como ver as métricas do GitHub Actions da sua organização](https://docs.github.com/pt/enterprise-cloud@latest/organizations/collaborating-with-groups-in-organizations/viewing-github-actions-metrics-for-your-organization).

Ao exibir métricas de uso, é importante lembrar que As métricas de uso GitHub Actions não aplicam multiplicadores de minutos às métricas exibidas. Embora *possam* ajudar você a entender sua fatura, seu objetivo principal é ajudar você a entender como e onde os minutos do Actions estão sendo usados em sua organização.

Para obter mais informações sobre os multiplicadores de minutos, confira [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions#baseline-minute-costs).

## Cobrança de fluxos de trabalho reutilizáveis

Se você reutilizar um fluxo de trabalho, a cobrança será sempre associada ao fluxo de trabalho de chamadas. A atribuição de executores hospedados em GitHub é sempre avaliada considerando apenas o contexto do chamador. O chamador não pode utilizar executores hospedados em GitHub do repositório chamado.

Para saber mais, confira [Reutilizar fluxos de trabalho](../how-tos/reuse-automations/reuse-workflows.md).

## Próximas etapas

Você pode gerenciar suas GitHub Actions políticas de uso e retenção para seu repositório, organização ou conta corporativa. Para saber mais, veja:

* [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
* [Configurando o período de retenção para verificações, execuções de fluxo de trabalho, status de confirmação, artefatos e logs em sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization)
* [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)
* [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise)
