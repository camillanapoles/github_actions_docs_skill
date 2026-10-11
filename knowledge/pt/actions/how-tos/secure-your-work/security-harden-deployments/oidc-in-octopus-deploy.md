---
title: Configurando o OpenID Connect no Octopus Deploy
description: Use OpenID Connect em seus fluxos de trabalho para autenticar com o Octopus Deploy.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-octopus-deploy
captured: '2026-10-11'
section: GitHub Actions
---

# Configurando o OpenID Connect no Octopus Deploy

_Use OpenID Connect em seus fluxos de trabalho para autenticar com o Octopus Deploy._

## Visão geral

OpenID Connect (OIDC) permite que seus fluxos de trabalho GitHub Actions se autentiquem com o [Octopus Deploy](https://octopus.com/) para enviar pacotes, criar versões ou acionar implantações sem armazenar senhas ou chaves de API do Octopus Deploy como segredos de GitHub de longa duração.

Este guia fornece uma visão geral de como configurar o Octopus Deploy para confiar no OIDC do GitHub como uma identidade federada e inclui um exemplo de fluxo de trabalho para a ação [`octopusdeploy/login`](https://github.com/OctopusDeploy/login) que utiliza tokens para autenticar em sua instância do Octopus Deploy.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

## Adicionando o provedor de identidade ao Octopus Deploy

Para usar o OIDC com o Octopus Deploy, primeiro estabeleça uma relação de confiança entre GitHub Actions e sua instância do Octopus Deploy. Para obter mais informações sobre esse processo, consulte [Como usar o OpenID Connect com a API do Octopus](https://octopus.com/docs/octopus-rest-api/openid-connect) na documentação do Octopus Deploy.

1. Faça login na sua instância de Octopus Deploy.
2. Crie ou abra a Conta de Serviço que receberá acesso por meio da solicitação de token.
3. Configure uma nova identidade OIDC, definindo o sujeito relevante com o qual a solicitação de token do fluxo de trabalho GitHub Actions será validada.

## Atualizar o seu fluxo de trabalho de GitHub Actions

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) para trocar o token OIDC (JWT) por um token de acesso à nuvem.

> \[!NOTE]
> Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adicionando configurações de permissões

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> \[!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

### Solicitando o token de acesso

A ação [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) recebe um JWT do provedor OIDC GitHub e, em seguida, solicita um token de acesso da sua instância do Octopus Server. Para obter mais informações, consulte a documentação do [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) .

O exemplo a seguir troca um token de identificação OIDC com sua instância do Octopus Deploy para receber um token de acesso, que pode ser usado para acessar os recursos do Octopus Deploy. Certifique-se de substituir `server` e `service_account_id` pelos detalhes adequados ao seu cenário.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

jobs:
  create_release_in_octopus:
    runs-on: ubuntu-latest
    name: Create a release in Octopus
    permissions:
      # You might need to add other permissions here like `contents: read` depending on what else your job needs to do
      id-token: write # This is required to obtain an ID token from GitHub Actions for the job
    steps:
      - name: Login to Octopus
        uses: OctopusDeploy/login@34b6dcc1e86fa373c14e6a28c5507d221e4de629 #v1.0.2
        with:
          server: https://my.octopus.app
          service_account_id: 5be4ac10-2679-4041-a8b0-7b05b445e19e

      - name: Create a release in Octopus
        uses: OctopusDeploy/create-release-action@fe13cc69c1c037cb7bb085981b152f5e35257e1f #v3.2.2
        with:
          space: Default
          project: My Octopus Project
```

## Leitura adicional

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
