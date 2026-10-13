---
title: Usando um gateway de API com o OIDC
description: Você pode usar tokens OpenID Connect (OIDC) para autenticar seu fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners / Connect to a private network
---

# Usando um gateway de API com o OIDC { #using-an-api-gateway-with-oidc }

_Você pode usar tokens OpenID Connect (OIDC) para autenticar seu fluxo de trabalho._

## Usando um gateway de API com o OIDC { #using-an-api-gateway-with-oidc-1 }

Com o GitHub Actions, você pode usar tokens OIDC (OpenID Connect) para autenticar seu fluxo de trabalho fora do GitHub Actions. Por exemplo, você pode executar um gateway de API na borda da rede privada que autentica solicitações de entrada com o token OIDC e, em seguida, faz solicitações de API em nome do fluxo de trabalho em sua rede privada.

O seguinte diagrama fornece uma visão geral da arquitetura desta solução:

![Diagrama de uma arquitetura de gateway do OIDC, começando com um executor do GitHub Actions e terminando com um serviço privado de rede privada.](https://docs.github.com/assets/images/help/actions/actions-oidc-gateway.png)

É importante que você verifique não apenas se o token OIDC veio GitHub Actions, mas que ele veio especificamente de seus fluxos de trabalho esperados, para que outros GitHub Actions usuários não possam acessar serviços em sua rede privada. Você pode usar declarações OIDC para criar essas condições. Para saber mais, confira [Referência do OpenID Connect](../../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

As principais desvantagens dessa abordagem são que você deve implementar o gateway de API para fazer solicitações em seu nome e executar o gateway na borda da rede.

As seguintes vantagens são aplicáveis.

* Você não precisa configurar nenhum firewall ou modificar o roteamento de sua rede privada.
* O gateway de API não tem estado e é dimensionado horizontalmente para lidar com alta disponibilidade e alta taxa de transferência.

Para obter mais informações, consulte [uma implementação de referência de um API Gateway](https://github.com/github/actions-oidc-gateway-example) no repositório github/actions-oidc-gateway. Essa implementação requer personalização para seu caso de uso e não está pronta para execução as-is. Para saber mais, confira [OpenID Connect](../../../../concepts/security/openid-connect.md).
