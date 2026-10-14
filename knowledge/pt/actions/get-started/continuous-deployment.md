---
title: Implantação contínua
description: Você pode criar fluxos de trabalho personalizados de CD (implantação contínua) diretamente no seu repositório GitHub com GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/get-started/continuous-deployment
captured: '2026-10-11'
section: Get started
---

# Implantação contínua { #continuous-deployment }

_Você pode criar fluxos de trabalho personalizados de CD (implantação contínua) diretamente no seu repositório GitHub com GitHub Actions._

## Sobre a implantação contínua { #about-continuous-deployment }

A CD (*implantação contínua*) é a prática de usar a automação para publicar e implantar atualizações de software. Como parte do processo típico do CD, o código é automaticamente criado e testado antes da implantação.

O desdobramento contínuo é frequentemente integrado à integração contínua. Para saber mais sobre a integração contínua, confira [Integração contínua](continuous-integration.md).

## Sobre a implantação contínua usando GitHub Actions { #about-continuous-deployment-using-github-actions }

Você pode configurar um GitHub Actions fluxo de trabalho para implantar seu produto de software. Para verificar se o produto funciona como esperado, seu fluxo de trabalho pode criar o código no repositório e executar seus testes antes da implantação.

Você pode configurar seu fluxo de trabalho do CD para ser executado quando ocorrer um evento (por exemplo, quando o novo código é enviado para o branch padrão do seu repositório), em um cronograma definido, manualmente ou quando ocorre um evento externo usando o webhook de envio do repositório. Para saber mais sobre quando o fluxo de trabalho pode ser executado, confira [Eventos que disparam fluxos de trabalho](../reference/workflows-and-actions/events-that-trigger-workflows.md).

GitHub Actions fornece recursos que oferecem mais controle sobre implantações. Por exemplo, você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais branches podem acionar um fluxo de trabalho, ou limitar o acesso a segredos. Você pode usar concorrência para limitar o pipeline do CD até uma implantação em andamento. Para saber mais sobre esses recursos, confira [Implantando com GitHub Actions](../how-tos/deploy/configure-and-manage-deployments/control-deployments.md) e [Gerenciar ambientes para implantação](../how-tos/deploy/configure-and-manage-deployments/manage-environments.md).

!!! tip
    Você pode usar agentic workflows para a preparação da implantação, como notas de versão, análise de alterações e resumos de distribuição, mantendo as implantações de produção em fluxos de trabalho determinísticos GitHub Actions . Para saber mais, confira [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

## Modelos de fluxo de trabalho e ações de terceiros { #workflow-templates-and-third-party-actions }

GitHuboferece modelos de fluxo de trabalho de implantação para vários serviços populares, como Azure Aplicativo Web. Para saber como começar a usar um modelo de fluxo de trabalho, confira [Usando modelos de fluxo de trabalho](../how-tos/write-workflows/use-workflow-templates.md) ou [navegue pela lista completa de modelos de fluxo de trabalho de implantação](https://github.com/actions/starter-workflows/tree/main/deployments). Confira também nossos guias mais detalhados de fluxos de trabalho de implantação específicos, como [Implantando Node.js em Azure App Service](../how-tos/deploy/deploy-to-third-party-platforms/nodejs-to-azure-app-service.md).

Muitos provedores de serviços também oferecem ações no GitHub Marketplace para implantar em seus serviços. Para obter a lista completa, consulte [GitHub Marketplace](https://github.com/marketplace?category=deployment\&type=actions).

## Próximas etapas { #next-steps }

Se seus GitHub Actions fluxos de trabalho precisarem acessar recursos de um provedor de nuvem que dê suporte ao OpenID Connect (OIDC), você poderá configurar seus fluxos de trabalho para autenticar diretamente no provedor de nuvem. Isso permitirá que você pare de armazenar essas credenciais como segredos de longa duração e proporcione outros benefícios de segurança. Para saber mais, confira [OpenID Connect](../concepts/security/openid-connect.md).
