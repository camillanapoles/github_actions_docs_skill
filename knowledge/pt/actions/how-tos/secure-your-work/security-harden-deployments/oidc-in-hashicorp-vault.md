---
title: Configurando o OpenID Connect no HashiCorp Vault
description: Use o OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com o HashiCorp Vault.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-hashicorp-vault
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no HashiCorp Vault { #configuring-openid-connect-in-hashicorp-vault }

_Use o OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com o HashiCorp Vault._

## Visão geral { #overview }

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho se autentiquem com um HashiCorp Vault para recuperar segredos.

Este guia fornece uma visão geral de como configurar o HashiCorp Vault para confiar no GitHubOIDC como uma identidade federada e demonstra como usar essa configuração na [ação hashicorp/vault-action](https://github.com/hashicorp/vault-action) para recuperar segredos do HashiCorp Vault.

## Pré-requisitos { #prerequisites }

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

## Adicionando o provedor de identidade ao HashiCorp Vault { #adding-the-identity-provider-to-hashicorp-vault }

Para usar o OIDC com o HashiCorp Vault, você precisará adicionar uma configuração de confiança para o provedor OIDC GitHub . Para obter mais informações, confira a [documentação](https://www.vaultproject.io/docs/auth/jwt) do HashiCorp Vault.

Para configurar o servidor do Cofre para aceitar JWT (Tokens Web JSON) para autenticação:

1. Habilite o método `auth` do JWT e use `write` para aplicar a configuração ao Cofre.
   Para `oidc_discovery_url` e `bound_issuer` parâmetros, use `https://token.actions.githubusercontent.com`. Esses parâmetros permitem que o servidor do Cofre verifique os JWT (Tokens Web JSON) recebidos durante o processo de autenticação.

            ```shell copy
   vault auth enable jwt
   ```

            ```shell copy
   vault write auth/jwt/config \
     bound_issuer="https://token.actions.githubusercontent.com" \
     oidc_discovery_url="https://token.actions.githubusercontent.com"
   ```

2. Configure uma política que só concede acesso aos caminhos específicos que seus fluxos de trabalho usarão para recuperar segredos. Para obter políticas mais avançadas, confira a [documentação de Políticas](https://www.vaultproject.io/docs/concepts/policies) do HashiCorp Vault.

            ```shell copy
   vault policy write myproject-production - <<EOF
   # Read-only permission on 'secret/data/production/*' path

   path "secret/data/production/*" {
     capabilities = [ "read" ]
   }
   EOF
   ```

3. Configure funções para agrupar políticas diferentes. Se a autenticação for bem-sucedida, essas políticas serão anexadas ao token de acesso resultante do Cofre.

            ```shell copy
   vault write auth/jwt/role/myproject-production -<<EOF
   {
     "role_type": "jwt",
     "user_claim": "actor",
     "bound_claims": {
       "repository": "user-or-org-name/repo-name"
     },
     "policies": ["myproject-production"],
     "ttl": "10m"
   }
   EOF
   ```

* `ttl` define a validade do token de acesso resultante.
* Verifique se o parâmetro `bound_claims` está definido para seus requisitos de segurança e tenha pelo menos uma condição. Opcionalmente, você também pode definir o parâmetro `bound_subject`, bem como o parâmetro `bound_audiences`.
* Para verificar as declarações arbitrárias no conteúdo JWT recebido, o parâmetro `bound_claims` contém um conjunto de declarações e seus valores necessários. No exemplo acima, a função aceitará quaisquer solicitações de autenticação de entrada do repositório `repo-name` pertencente à conta `user-or-org-name`.
* Para ver todas as declarações disponíveis compatibilizadas pelo provedor OIDC de GitHub, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-token-claims).

Para obter mais informações, confira a [documentação](https://www.vaultproject.io/docs/auth/jwt) do HashiCorp Vault.

## Atualizando seu GitHub Actions fluxo de trabalho { #updating-your-github-actions-workflow }

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação [`hashicorp/vault-action`](https://github.com/hashicorp/vault-action) para trocar o token OIDC (JWT) por um token de acesso à nuvem.

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

Para adicionar a integração do OIDC a seus fluxos de trabalho que lhes permitem acessar os segredos no Vault, você deverá adicionar as seguintes alterações de código:

* Conceda permissão para buscar o token do provedor OIDC GitHub :
  * O fluxo de trabalho precisa de configurações `permissions:` com o valor de `id-token` definido como `write`. Isso permite obter o token do OIDC de cada trabalho do fluxo de trabalho.
* Solicite o JWT do provedor OIDC e apresente-o GitHub ao HashiCorp Vault para receber um token de acesso:
  * Você pode usar a ação [`hashicorp/vault-action`](https://github.com/hashicorp/vault-action) para buscar o JWT e receber o token de acesso do Cofre ou pode usar o [kit de ferramentas do Actions](https://github.com/actions/toolkit/) para buscar os tokens para seu trabalho.

Este exemplo demonstra como usar o OIDC com a ação oficial para solicitar um segredo ao HashiCorp Vault.

### Adicionando configurações de permissões { #adding-permissions-settings }

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> [!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

!!! note
    Quando a chave `permissions` é usada, todas as permissões não especificadas são definidas como *sem acesso*, com exceção do escopo de metadados, que sempre obtém acesso de *leitura*. Como resultado, talvez seja necessário adicionar outras permissões, como `contents: read`. Para obter mais informações, confira "[Autenticação automática de token](../../../tutorials/authenticate-with-github_token.md)".

### Solicitando o token de acesso { #requesting-the-access-token }

A ação `hashicorp/vault-action` recebe um JWT do provedor OIDC GitHub e, em seguida, solicita um token de acesso à sua instância do HashiCorp Vault para recuperar segredos. Para obter mais informações, confira a [documentação](https://github.com/hashicorp/vault-action) do HashiCorp Vault GitHub Action.

Este exemplo demonstra como criar um trabalho que solicita um segredo para o HashiCorp Vault.

* `VAULT-URL`: substitua isso pela URL do seu HashiCorp Vault.
* `VAULT-NAMESPACE`: substitua isso pelo Namespace que você definiu no HashiCorp Vault. Por exemplo: `admin`.
* `ROLE-NAME`: substitua isso pela função que você definiu na relação de confiança do HashiCorp Vault.
* `SECRET-PATH`: substitua isso pelo caminho para o segredo que está sendo recuperado do HashiCorp Vault. Por exemplo: `secret/data/production/ci npmToken`.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
jobs:
  retrieve-secret:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Retrieve secret from Vault
        uses: hashicorp/vault-action@9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b
        with:
          method: jwt
          url: VAULT-URL
          namespace: VAULT-NAMESPACE # HCP Vault and Vault Enterprise only
          role: ROLE-NAME
          secrets: SECRET-PATH

      - name: Use secret from Vault
        run: |
          # This step has access to the secret retrieved above; see hashicorp/vault-action for more details.
```

!!! note
    * Se o servidor do Cofre não estiver acessível na rede pública, considere usar um executor auto-hospedado com outros [métodos de autenticação](https://www.vaultproject.io/docs/auth) do Cofre disponíveis. Para saber mais, confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md).
    *

`VAULT-NAMESPACE` deve ser definido para uma implantação do Vault Enterprise (incluindo o HCP Vault). Para mais informações, confira [Namespace do Cofre](https://www.vaultproject.io/docs/enterprise/namespaces).

### Revogando o token de acesso { #revoking-the-access-token }

Por padrão, o servidor do Cofre revogará automaticamente os tokens de acesso quando a TTL expirar, para que você não precise revogar manualmente os tokens de acesso. No entanto, se você quiser revogar tokens de acesso imediatamente após a conclusão ou falha do trabalho, será possível fazer isso manualmente usando a [API do Cofre](https://www.vaultproject.io/api/auth/token#revoke-a-token-self).

1. Defina a opção `exportToken` como `true` (padrão: `false`). Isso exporta o token de acesso do Cofre emitido como uma variável de ambiente: `VAULT_TOKEN`.
2. Adicione uma etapa para chamar a API do Cofre de [Revogação de um Token (Auto)](https://www.vaultproject.io/api/auth/token#revoke-a-token-self) para revogar o token de acesso.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
jobs:
  retrieve-secret:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Retrieve secret from Vault
        uses: hashicorp/vault-action@9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b
        with:
          exportToken: true
          method: jwt
          url: VAULT-URL
          role: ROLE-NAME
          secrets: SECRET-PATH

      - name: Use secret from Vault
        run: |
          # This step has access to the secret retrieved above; see hashicorp/vault-action for more details.

      - name: Revoke token
        # This step always runs at the end regardless of the previous steps result
        if: always()
        run: |
          curl -X POST -sv -H "X-Vault-Token: ${{ env.VAULT_TOKEN }}" \
            VAULT-URL/v1/auth/token/revoke-self
```

## Leitura adicional { #further-reading }

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
