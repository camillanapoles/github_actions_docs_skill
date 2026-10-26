---
title: Configurando o OpenID Connect no Docker
description: Use o OpenID Connect em seus fluxos de trabalho para autenticar com o Docker sem armazenar credenciais de longa duração.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-docker
captured: '2026-10-26'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no Docker

_Use o OpenID Connect em seus fluxos de trabalho para autenticar com o Docker sem armazenar credenciais de longa duração._

## Overview

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho se autentiquem com o [Docker](https://www.docker.com/) para acessar Docker Hub e Docker Build Cloud sem armazenar senhas, personal access tokens segredos ou tokens de acesso da organização (OATs) do Docker em GitHub.

Em vez de gerenciar credenciais de longa duração, você configura uma relação de confiança entre sua GitHub organização e sua organização do Docker. Quando um fluxo de trabalho é executado, GitHub emite um token OIDC de curta duração que o Docker valida em relação aos conjuntos de regras configurados e então emite um token de acesso com escopo para o fluxo de trabalho.

Este guia fornece uma visão geral de como configurar o Docker para confiar no OIDC do GitHub como uma identidade federada e demonstra como usar essa configuração em um fluxo de trabalho GitHub Actions.

Para obter mais informações, consulte [as conexões OIDC](https://docs.docker.com/enterprise/security/oidc-connections/) na documentação do Docker.

## Prerequisites

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Sua organização do Docker deve usar o Docker Business, o Docker Team ou o Docker Hardened Images, ou estar inscrita no Programa de Software Livre Patrocinado pelo Docker.

* Você deve ser proprietário ou editor em sua organização Docker.

* Você deve planejar quais repositórios, branches e fluxos de trabalho precisam de acesso ao Docker e configurar conjuntos de regras adequadamente.

## Adicionando o provedor de identidade ao Docker

Para usar o OIDC com o Docker, estabeleça uma relação de confiança entre GitHub Actions e o Docker criando uma conexão OIDC. Para obter mais informações sobre esse processo, consulte [Criar e gerenciar conexões OIDC](https://docs.docker.com/security/authentication/oidc-connections/create-manage/) na documentação do Docker.

1. Entre no [Docker Home](https://app.docker.com/) e navegue até sua organização.
2. Vá para **Identidade e autenticação**\*\*\*\* > .
3. Selecione **Criar conexão OIDC**.
4. Configure pelo menos um conjunto de regras para definir quais GitHub repositórios, branches ou fluxos de trabalho podem se autenticar. Cada conjunto de regras especifica:
   * **Regras**: Condições correspondentes às declarações de token OIDC (repositório, branch, caminho de fluxo de trabalho). Padrões curinga como `repo:my-org/*` são compatíveis.
   * **Recursos**: repositórios do Docker Hub ou projetos do Docker Build Cloud que o fluxo de trabalho pode acessar.
   * **Escopos**: níveis de permissão (`read`, `write`).
5. Salve a conexão e copie a **ID da conexão** para uso no fluxo de trabalho.

## Atualizando seu GitHub Actions fluxo de trabalho

Depois de criar uma conexão OIDC no Docker, atualize o fluxo de trabalho para autenticar usando a ação [`docker/login-action`](https://github.com/docker/login-action) .

O exemplo a seguir usa o espaço reservado `YOUR-CONNECTION-ID` para a ID de conexão copiada do Docker e `YOUR-DOCKER-ORG` para o nome da organização do Docker.

```yaml
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
permissions:
  id-token: write
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v6

      - name: Sign in to Docker Hub with OIDC
        uses: docker/login-action@abd2ef45e78c5afb21d64d4ca52ee8550d9572c7 # v4.5.1
        with:
          username: YOUR-DOCKER-ORG
        env:
          DOCKERHUB_OIDC_CONNECTIONID: YOUR-CONNECTION-ID

      - name: Build and push
        uses: docker/build-push-action@10e90e3645eae34f1e60eeb005ba3a3d33f178e8 # v6
        with:
          push: true
          tags: YOUR-DOCKER-ORG/my-image:latest
```

```
### Principais configurações do fluxo de trabalho

* **`permissions.id-token: write`** é necessário para que GitHub possa emitir um token OIDC para o fluxo de trabalho.
* O `docker/login-action` gerencia a troca de tokens OIDC e o logon do Docker em uma única etapa quando `DOCKERHUB_OIDC_CONNECTIONID` é definido e `password` é omitido.
* O `username` campo deve ser o nome da organização do Docker.

### Correspondência da declaração de sujeito

O Docker avalia a `sub` claim do GitHub token OIDC em relação aos conjuntos de regras configurados. O formato padrão da declaração de sujeito é:

```text
repo:<owner>/<repo>:ref:refs/heads/<branch>
```

!!! note
    Repositórios criados após 15 de julho de 2026 e renomeações ou transferências de repositório após essa data usam uma declaração OIDC `sub` padrão imutável que inclui IDs de proprietário e repositório. Os repositórios existentes mantêm o formato anterior, a menos que aceitem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#immutable-subject-claims).

Gatilhos de fluxo de trabalho diferentes produzem claims de assunto diferentes. Por exemplo:

| Trigger             | Formato de declaração de assunto             |
|-------------------|--------------------------------------------|
| Push da branch      | `repo:my-org/my-repo:ref:refs/heads/main`    |
| Solicitação de pull | `repo:my-org/my-repo:pull_request`           |
| Etiqueta            | `repo:my-org/my-repo:ref:refs/tags/v1.0`     |
| Ambiente            | `repo:my-org/my-repo:environment:production` |

Você pode usar padrões curinga em seus conjuntos de regras para corresponder a vários repositórios ou branches. Para declarações de assunto legadas, `repo:my-org/*` corresponde a todos os repositórios na organização. Para claims de assunto imutáveis, use `repo:my-org@OWNER-ID/*`; se a organização contiver repositórios usando ambos os formatos, configure ambos os padrões.

Para obter mais informações, consulte [Conjuntos de regras e declarações de sujeito](https://docs.docker.com/security/authentication/oidc-connections/rulesets-claims/) na documentação do Docker.
