---
title: Configurando OpenID Connect na Google Cloud Platform
description: Use OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com a Google Cloud Platform.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform
captured: '2026-10-13'
section: How tos / Secure your work / Security harden deployments
---

# Configurando OpenID Connect na Google Cloud Platform

_Use OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com a Google Cloud Platform._

## Visão geral

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho acessem recursos no GCP (Google Cloud Platform), sem a necessidade de armazenar as credenciais do GCP como segredos de GitHub longa duração.

Este guia fornece uma visão geral de como configurar o GCP para confiar no GitHubOIDC como uma identidade federada e inclui um exemplo de fluxo de trabalho para a ação [`google-github-actions/auth`](https://github.com/google-github-actions/auth) que usa tokens para autenticar no GCP e acessar recursos.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

Para repositórios criados após 15 de julho de 2026 e renomeações ou transferências de repositórios após essa data, use uma declaração OIDC padrão imutável `sub` que inclui os IDs do proprietário e do repositório (não disponível no GitHub Enterprise Server). Os repositórios existentes mantêm o formato anterior, a menos que aceitem. Para saber mais, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#immutable-subject-claims).

## Adicionando um provedor de identidade de carga do Google Cloud

Para configurar o provedor de identidade OIDC no GCP, você deverá definir a configuração a seguir. Para obter instruções sobre como fazer essas alterações, veja [a documentação do GCP](https://github.com/google-github-actions/auth).

1. Crie um novo conjunto de identidades.
2. Configure o mapeamento e adicione condições.
3. Conecte o novo grupo a uma conta de serviço.

Orientação adicional para a configuração do provedor de identidade:

* Para reforçar a segurança, certifique-se de ter revisado [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles). Para ver um exemplo, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#configuring-the-subject-in-your-cloud-provider).
* Para que a conta de serviço esteja disponível para configuração, ela precisa ser atribuída à função `roles/iam.workloadIdentityUser`. Para obter mais informações, confira [a documentação do GCP](https://cloud.google.com/iam/docs/workload-identity-federation?_ga=2.114275588.-285296507.1634918453#conditions).
* A URL do Emissor a ser usada: `https://token.actions.githubusercontent.com`

## Atualizando seu GitHub Actions fluxo de trabalho

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação [`google-github-actions/auth`](https://github.com/google-github-actions/auth) para trocar o token OIDC (JWT) por um token de acesso à nuvem.

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adicionando configurações de permissões

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> [!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

### Solicitando o token de acesso

A `google-github-actions/auth` ação recebe um JWT do provedor OIDC GitHub e solicita um token de acesso do GCP. Para obter mais informações, confira a [documentação](https://github.com/google-github-actions/auth) do GCP.

Este exemplo contém um trabalho chamado `Get_OIDC_ID_token` que usa ações para solicitar uma lista de serviços do GCP.

* `WORKLOAD-IDENTITY-PROVIDER`: substitua isso pelo caminho para o provedor de identidade no GCP. Por exemplo, `projects/example-project-id/locations/global/workloadIdentityPools/name-of-pool/providers/name-of-provider`
* `SERVICE-ACCOUNT`: substitua isso pelo nome da sua conta de serviço no GCP.

Essa ação troca um token OIDC GitHub por um token de acesso do Google Cloud usando a [Federação de Identidade de Carga de Trabalho](https://cloud.google.com/iam/docs/workload-identity-federation).

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
name: List services in GCP
on:
  pull_request:
    branches:
      - main

permissions:
  id-token: write

jobs:
  Get_OIDC_ID_token:
    runs-on: ubuntu-latest
    steps:
    - id: 'auth'
      name: 'Authenticate to GCP'
      uses: 'google-github-actions/auth@f1e2d3c4b5a6f7e8d9c0b1a2c3d4e5f6a7b8c9d0'
      with:
          create_credentials_file: 'true'
          workload_identity_provider: 'WORKLOAD-IDENTITY-PROVIDER'
          service_account: 'SERVICE-ACCOUNT'
    - id: 'gcloud'
      name: 'gcloud'
      run: |-
        gcloud auth login --brief --cred-file="${{ steps.auth.outputs.credentials_file_path }}"
        gcloud services list
```

```
## Leitura adicional

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
