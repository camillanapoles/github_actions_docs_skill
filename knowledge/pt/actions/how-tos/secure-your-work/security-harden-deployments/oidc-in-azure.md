---
title: Configurando o OpenID Connect no Azure
description: Use o OpenID Connect em seus fluxos de trabalho para autenticar com Azure.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure
captured: '2026-10-19'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no Azure

_Use o OpenID Connect em seus fluxos de trabalho para autenticar com Azure._

## Visão geral

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho acessem recursos no Azure, sem a necessidade de armazenar as credenciais do Azure como segredos de GitHub longa duração.

Este guia fornece uma visão geral de como configurar o Azure para confiar no GitHubOIDC como uma identidade federada e inclui um exemplo de fluxo de trabalho para a ação [`azure/login`](https://github.com/Azure/login) que usa tokens para autenticar no Azure e acessar recursos.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

Para repositórios criados após 15 de julho de 2026 e renomeações ou transferências de repositórios após essa data, use uma declaração padrão imutável do OIDC `sub` que inclui IDs do proprietário e do repositório (não disponível no GitHub Enterprise Server). Os repositórios existentes mantêm o formato anterior, a menos que aceitem. Para saber mais, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#immutable-subject-claims).

## Adicionando as credenciais federadas a Azure

O provedor OIDC do GitHub funciona com a federação de identidade de carga de trabalho do Azure. Para ter uma visão geral, confira a documentação da Microsoft em [Federação de identidade de carga de trabalho](https://docs.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation).

Para configurar o provedor de identidade OIDC no Azure, você precisará executar a configuração a seguir. Para obter instruções sobre como fazer essas alterações, consulte [a documentação Azure](https://docs.microsoft.com/en-us/azure/developer/github/connect-from-azure).

No procedimento a seguir, você criará um aplicativo para a ID do Microsoft Entra (anteriormente conhecida como Azure AD).

1. Crie um aplicativo Entra ID e uma entidade de serviço.
2. Adicione credenciais federadas para o aplicativo do Entra ID.
3. Crie GitHub segredos para armazenar configurações do Azure.

Orientação adicional para a configuração do provedor de identidade:

* Para reforçar a segurança, certifique-se de ter revisado [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles). Para ver um exemplo, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#configuring-the-subject-in-your-cloud-provider).
* Para a configuração `audience`, `api://AzureADTokenExchange` é o valor recomendado, mas você também pode especificar outros valores aqui.

## Atualizando seu GitHub Actions fluxo de trabalho

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação [`azure/login`](https://github.com/Azure/login) para trocar o token OIDC (JWT) por um token de acesso à nuvem.

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adicionando configurações de permissões

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> [!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

### Solicitando o token de acesso

A [`azure/login`](https://github.com/Azure/login) ação recebe um JWT do provedor OIDC GitHub e solicita um token de acesso do Azure. Para obter mais informações, consulte a documentação [`azure/login`](https://github.com/Azure/login).

O exemplo a seguir troca um token de ID OIDC com Azure para receber um token de acesso, que pode ser usado para acessar recursos de nuvem.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
name: Run Azure Login with OIDC
on: [push]

permissions:
  id-token: write
  contents: read
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: 'Az CLI login'
        uses: azure/login@8c334a195cbb38e46038007b304988d888bf676a
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: 'Run az commands'
        run: |
          az account show
          az group list
```

```
## Leitura adicional

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
