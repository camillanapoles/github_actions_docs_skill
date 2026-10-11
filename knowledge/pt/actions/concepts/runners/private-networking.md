---
title: Rede privada com executores hospedados pelo GitHub
description: Você pode conectar executores hospedados no GitHub a recursos em uma rede privada, incluindo registros de pacotes, gerentes secretos e outros serviços locais.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/private-networking
captured: '2026-10-11'
section: GitHub Actions
---

# Rede privada com executores hospedados pelo GitHub

_Você pode conectar executores hospedados no GitHub a recursos em uma rede privada, incluindo registros de pacotes, gerentes secretos e outros serviços locais._

## Sobre a rede dos executores hospedados em GitHub

Por padrão, os executores hospedados no GitHub têm acesso à Internet pública. No entanto, talvez você também queira que esses executores acessem recursos em sua rede privada, como um registro de pacote, um gerenciador de segredos ou outros serviços locais.

Executores hospedados no GitHub são compartilhados entre todos os clientes do GitHub. No entanto, com a rede privada, você pode configurar executores hospedados para serem usados exclusivamente para se conectar à sua rede privada e seus recursos enquanto eles estão executando seus fluxos de trabalho.

Há algumas abordagens diferentes que você pode adotar para configurar esse acesso, cada uma com vantagens e desvantagens diferentes.

## Usar um Gateway de API com OIDC

Com o GitHub Actions, você pode usar tokens OIDC (OpenID Connect) para autenticar seu fluxo de trabalho fora do GitHub Actions. Para obter mais informações, consulte [Usando um gateway de API com o OIDC](../../how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md).

## Usar o WireGuard para criar uma sobreposição de rede

Se você não quiser manter uma infraestrutura separada para um Gateway de API, poderá criar uma rede de sobreposição entre o executor e um serviço em sua rede privada, executando o WireGuard em ambos os locais. Para obter mais informações, consulte [Usar o WireGuard para criar uma sobreposição de rede](../../how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard.md).

## Usando uma Rede Virtual Azure (VNET)

Você pode usar executores hospedados no GitHub em uma VNET do Azure. Isso permite usar a infraestrutura gerenciada pela GitHub para CI/CD e, ao mesmo tempo, fornece controle total sobre as políticas de rede dos seus executores. Para obter mais informações sobre VNETs do Azure, consulte [O que é uma Rede Virtual do Azure?](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview), na documentação do Azure.

Os proprietários da organização que usam o plano GitHub Team podem configurar a rede privada do Azure para executores hospedados em GitHub no nível da organização. Para saber mais, confira [Sobre a rede privada do Azure para executores hospedados por GitHub em sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/about-azure-private-networking-for-github-hosted-runners-in-your-organization).
