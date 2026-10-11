---
title: Configurar regras de proteção de implantação personalizadas
description: Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules
captured: '2026-10-11'
section: How tos / Deploy / Configure and manage deployments
---

# Configurar regras de proteção de implantação personalizadas

_Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros._

!!! note
    Regras de proteção de implementação personalizada estão em prévia pública e estão sujeitas a alterações.

## Sobre regras de proteção de implantação personalizada

As regras de proteção de implantação personalizada são alimentadas por GitHub Apps. Depois que uma regra de proteção de implantação é configurada e instalada em um repositório, ela pode ser habilitada para qualquer ambiente no repositório.

Depois de habilitar uma regra de proteção de implantação personalizada em um ambiente, sempre que uma etapa de fluxo de trabalho for direcionada a esse ambiente, a regra de proteção de implantação será executada automaticamente. Para saber mais sobre como direcionar um ambiente para implantações, confira [Gerenciar ambientes para implantação](manage-environments.md).

Quando uma regra de proteção de implantação personalizada é acionada, ela aguarda até 30 dias por uma resposta de evento de webhook antes que ela atinja o tempo limite e o fluxo de trabalho falhe.

Para saber mais sobre como criar suas regras de proteção de implantação personalizadas, confira [Criar regras de proteção de implantação personalizadas](create-custom-protection-rules.md).

!!! note
    Qualquer quantidade de regras de proteção de implantação baseadas no GitHub Apps pode ser instalada em um repositório. No entanto, no máximo seis regras de proteção de implantação podem ser habilitadas em qualquer ambiente ao mesmo tempo.

## Usar regras de proteção de implantação personalizadas existentes

Você pode optar por criar suas próprias regras de proteção de implantação personalizadas ou pode usar qualquer regra de proteção de implantação personalizada existente.

A seguir está uma lista de implementações de parceiros oficiais para regras de proteção de implantação.

* Datadog: você pode impor regras de proteção em seus GitHub Actions fluxos de trabalho de implantação usando monitores Datadog. Para obter mais informações, consulte [Controlando suas implantações de GitHub Actions com monitores do Datadog](https://docs.datadoghq.com/continuous_integration/guides/github_gating/) na documentação da Datadog.
* Honeycomb: você pode definir limites para rejeitar ou aprovar implantações com base nos dados que você está enviando para o Honeycomb. Para obter mais informações, consulte [o aplicativo Honeycomb](https://github.com/apps/honeycomb-io) no GitHub Marketplace.
* Nova Relic: para obter mais informações, consulte [o aplicativo New Relic](https://github.com/apps/new-relic-gate) no GitHub Marketplace.
* NCM NodeSource: para obter mais informações, consulte [o aplicativo NCM NodeSource](https://github.com/apps/ncm-nodesource) no GitHub Marketplace.
* ServiceNow: para obter mais informações, consulte [integração do GitHub com o DevOps Change Velocity](https://www.servicenow.com/docs/bundle/utah-devops/page/product/enterprise-dev-ops/concept/github-integration-dev-ops.html) na documentação do ServiceNow.

## Pré-requisitos

Para que uma regra de proteção de implantação personalizada esteja disponível para todos os ambientes em um repositório, primeiro você deve instalar a regra de proteção de implantação personalizada no repositório. Para saber mais, confira [Instalando seu próprio aplicativo GitHub](https://docs.github.com/pt/apps/using-github-apps/installing-your-own-github-app).

Após a instalação de uma regra de proteção de implantação personalizada em um repositório, ela deve ser habilitada para cada ambiente em que você deseja que a regra seja aplicada.

## Habilitar regras de proteção de implantação personalizadas para o ambiente

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Selecione o ambiente que deseja configurar.
5. Em "Regras de proteção de implantação", marcar a caixa ao lado de cada regra de proteção de implantação personalizada que você deseja habilitar para o ambiente.
6. Clique em **Salvar regras de proteção**.

Depois que uma regra de proteção de implantação personalizada for habilitada para um ambiente, ela será executada automaticamente sempre que um fluxo de trabalho atingir um trabalho que faça referência ao ambiente. Você pode ver os resultados de uma aprovação ou rejeição para sua implantação examinando os detalhes da implantação. Para saber mais, confira [Revisar implantações](review-deployments.md).
