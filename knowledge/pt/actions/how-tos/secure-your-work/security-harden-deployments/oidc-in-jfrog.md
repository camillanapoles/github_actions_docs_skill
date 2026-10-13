---
title: Configurando o OpenID Connect no JFrog
description: Use o OpenID Connect em seus fluxos de trabalho para se autenticar no JFrog.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-jfrog
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no JFrog { #configuring-openid-connect-in-jfrog }

_Use o OpenID Connect em seus fluxos de trabalho para se autenticar no JFrog._

## Visão geral { #overview }

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho se autentiquem com [jFrog](https://jfrog.com/) para baixar e publicar artefatos sem armazenar senhas JFrog, tokens ou chaves de API em GitHub.

Este guia fornece uma visão geral de como configurar o JFrog para confiar no GitHubOIDC como uma identidade federada e demonstra como usar essa configuração em um GitHub Actions fluxo de trabalho.

Para ver um fluxo de trabalho de exemplo GitHub Actions, consulte [Integração de exemplo GitHub Actions](https://jfrog.com/help/r/jfrog-platform-administration-documentation/sample-github-actions-integration) na documentação da JFrog.

Para obter um exemplo GitHub Actions de fluxo de trabalho usando a CLI JFrog, consulte [`build-publish.yml`](https://github.com/jfrog/jfrog-github-oidc-example/blob/main/.github/workflows/build-publish.yml) no `jfrog-github-oidc-example` repositório.

## Pré-requisitos { #prerequisites }

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Para ser seguro, você precisa definir um JSON de declarações no JFrog ao configurar mapeamentos de identidade. Para saber mais, confira [AUTOTITLE](https://jfrog.com/help/r/jfrog-platform-administration-documentation/configure-identity-mappings) e [Referência do OpenID Connect](../../../reference/security/oidc.md#customizing-the-token-claims).

  Por exemplo, você pode definir `iss` como `https://token.actions.githubusercontent.com` e definir o(a) `repository` como algo como `octo-org/octo-repo`. Os mapeamentos de identidade do JFrog comparam cada declaração com um valor exato; portanto, para garantir que apenas os fluxos de trabalho GitHub Actions do repositório especificado tenham acesso à sua plataforma JFrog, também defina `event_name` como o evento que aciona seu fluxo de trabalho, como `push`. Isso impede que os tokens OIDC solicitados para trabalhos de atualização Dependabot, que têm um `event_name` de `dynamic`, coincidam com o mapeamento de identidade. Se os fluxos de trabalho forem disparados por mais de um evento, crie um mapeamento de identidade separado para cada nome de evento. A seguir, um exemplo de JSON de declarações ao configurar mapeamentos de identidade.

        ```json copy
  {
      "iss": "https://token.actions.githubusercontent.com",
      "repository": "octo-org/octo-repo",
      "event_name": "push"
  }
  ```

## Adicionando o provedor de identidade ao JFrog { #adding-the-identity-provider-to-jfrog }

Para usar o OIDC com o JFrog, estabeleça uma relação de confiança entre GitHub Actions e a plataforma JFrog. Para obter mais informações sobre esse processo, consulte [Integração do OpenID Connect](https://docs.jfrog.com/administration/docs/openid-connect-integration) na documentação do JFrog.

1. Inicie sessão na plataforma JFrog.
2. Configure a confiança entre o JFrog e seus GitHub Actions fluxos de trabalho.
3. Configurar mapeamentos de identidade.

## Atualizando seu GitHub Actions fluxo de trabalho { #updating-your-github-actions-workflow }

### Autenticação com JFrog usando OIDC { #authenticating-with-jfrog-using-oidc }

GitHub Actions No arquivo de fluxo de trabalho, verifique se você está usando o nome do provedor e o público que você configurou na Plataforma JFrog.

O exemplo a seguir usa os espaços reservados `YOUR_PROVIDER_NAME` e `YOUR_AUDIENCE`.

```yaml
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
      - name: Set up JFrog CLI with OIDC
        id: setup-jfrog-cli
        uses: jfrog/setup-jfrog-cli@29fa5190a4123350e81e2a2e8d803b2a27fed15e
        with:
          JF_URL: ${{ env.JF_URL }}
          oidc-provider-name: 'YOUR_PROVIDER_NAME'
          oidc-audience: 'YOUR_AUDIENCE' # This is optional

      - name: Upload artifact
        run: jf rt upload "dist/*.zip" my-repo/

```

!!! tip
    Quando a autenticação OIDC é usada, a ação `setup-jfrog-cli` fornece automaticamente `oidc-user` e `oidc-token` como saídas da etapa.
    Essas opções podem ser usadas para outras integrações que exigem autenticação com o JFrog.
    Para referenciar essas saídas, certifique-se de que a etapa tenha `id` explícito definido (por exemplo, `id: setup-jfrog-cli`).

### Usando credenciais do OIDC em outras etapas { #using-oidc-credentials-in-other-steps }

```yaml
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
      - name: Sign in to Artifactory Docker registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.JF_URL }}
          username: ${{ steps.setup-jfrog-cli.outputs.oidc-user }}
          password: ${{ steps.setup-jfrog-cli.outputs.oidc-token }}
```

## Leitura adicional { #further-reading }

* [Integração do OpenID Connect](https://docs.jfrog.com/administration/docs/openid-connect-integration) na documentação do JFrog
* [Mapeamentos de identidade](https://jfrog.com/help/r/jfrog-platform-administration-documentation/identity-mappings) na documentação do JFrog
* [OpenID Connect](../../../concepts/security/openid-connect.md)
