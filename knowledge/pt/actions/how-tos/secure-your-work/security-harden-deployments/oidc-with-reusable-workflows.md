---
title: Usando o OpenID Connect com fluxos de trabalho reutilizáveis
description: Você pode usar fluxos de trabalho reutilizáveis com o OIDC para padronizar e melhorar as suas etapas de implantação.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows
captured: '2026-10-26'
section: How tos / Secure your work / Security harden deployments
---

# Usando o OpenID Connect com fluxos de trabalho reutilizáveis

_Você pode usar fluxos de trabalho reutilizáveis com o OIDC para padronizar e melhorar as suas etapas de implantação._

## Sobre fluxos de trabalho reutilizáveis

Em vez de copiar e colar trabalhos de implantação de um fluxo de trabalho para outro, é possível criar um fluxo de trabalho reutilizável que executa as etapas de implantação. Um fluxo de trabalho reutilizável poderá ser usado por outro fluxo de trabalho se atender a um dos requisitos de acesso descritos em [Reutilizando configurações de fluxo de trabalho](../../../reference/workflows-and-actions/reusing-workflow-configurations.md#access-to-reusable-workflows).

Você deve ter familiaridade com os conceitos descritos em [Reutilizar fluxos de trabalho](../../reuse-automations/reuse-workflows.md) e [Referência do OpenID Connect](../../../reference/security/oidc.md#customizing-the-token-claims).

## Definindo as condições de confiança

Quando combinado com o OpenID Connect (OIDC), os fluxos de trabalho reutilizáveis permitem que você aplique implantações consistentes no seu repositório, organização ou empresa. Você pode fazer isso definindo condições de confiança nas funções da nuvem com base em fluxos de trabalho reutilizáveis. As opções disponíveis variam dependendo do provedor de nuvem:

* **Usando`job_workflow_ref`:**
  * Para criar condições de relação de confiança com base em fluxos de trabalho reutilizáveis, o provedor de nuvem precisa dar suporte a declarações personalizadas de `job_workflow_ref`. Isso permite que seu provedor de nuvem identifique de qual repositório o trabalho veio originalmente.
  * Para nuvens que dão suporte apenas às declarações padrão (audiência \[`aud`] e assunto \[`sub`]), você pode usar a API para personalizar a declaração `sub` para incluir `job_workflow_ref`. Para saber mais, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#customizing-the-token-claims). O suporte para declarações personalizadas está disponível atualmente para o Google Cloud Platform e o HashiCorp Vault.

* **Personalizar as declarações de token:**
  * Você pode configurar condições de confiança mais granulares personalizando as declarações de assunto (`sub`)  que são incluídas no JWT. Para saber mais, confira [OpenID Connect](../../../concepts/security/openid-connect.md).

## Como o token funciona com fluxos de trabalho reutilizáveis

Durante uma execução de um fluxo de trabalho, o provedor OIDC de GitHub apresenta um token OIDC ao provedor de nuvem, que contém informações sobre o job. Se esse trabalho fizer parte de um fluxo de trabalho reutilizável, o token incluirá as declarações padrão que contêm informações sobre o fluxo de trabalho chamador e incluirá uma declaração personalizada chamada `job_workflow_ref` que contém informações sobre o fluxo de trabalho chamado.

Por exemplo, o token OIDC a seguir é para um trabalho que fazia parte de um fluxo de trabalho previamente definido. O `workflow`, a `ref` e outros atributos descrevem o fluxo de trabalho chamador, enquanto a `job_workflow_ref` se refere ao fluxo de trabalho chamado:

```yaml copy
{
  "typ": "JWT",
  "alg": "RS256",
  "x5t": "example-thumbprint",
  "kid": "example-key-id"
}
{
  "jti": "example-id",
  "sub": "repo:octo-org/octo-repo:environment:prod",
  "aud": "https://github.com/octo-org",
  "ref": "refs/heads/main",
  "sha": "example-sha",
  "repository": "octo-org/octo-repo",
  "repository_owner": "octo-org",
  "actor_id": "12",
  "repository_id": "74",
  "repository_owner_id": "65",
  "run_id": "example-run-id",
  "run_number": "10",
  "run_attempt": "2",
  "actor": "octocat",
  "workflow": "example-workflow",
  "head_ref": "",
  "base_ref": "",
  "event_name": "workflow_dispatch",
  "ref_type": "branch",
  "job_workflow_ref": "octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main",
  "iss": "https://token.actions.githubusercontent.com",
  "nbf": 1632492967,
  "exp": 1632493867,
  "iat": 1632493567
}
```

Se o seu fluxo de trabalho reutilizável executa etapas de implantação, ele, de modo geral, irá precisar de acesso a um função de nuvem específica, e você deverá permitir que qualquer repositório da sua organização chame esse fluxo de trabalho reutilizável. Para permitir isso, você criará uma condição de confiança que permite qualquer repositório e fluxo de trabalho de chamadas, e, em seguida, irá filtrar a organização e o fluxo de trabalho chamado. Veja a próxima seção para obter alguns exemplos.

## Exemplos

**Filtragem para fluxos de trabalho reutilizáveis em um repositório específico**

É possível configurar uma declaração personalizada que filtra qualquer fluxo de trabalho reutilizável em um repositório específico. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado de um trabalho definido em um fluxo de trabalho reutilizável no repositório `octo-org/octo-automation` e em qualquer repositório pertencente à organização `octo-org`.

* **Assunto**:
  * Sintaxe: `repo:ORG_NAME/*`
  * Exemplo: `repo:octo-org/*`

* **Declaração personalizada**:
  * Sintaxe: `job_workflow_ref:ORG_NAME/REPO_NAME`
  * Exemplo: `job_workflow_ref:octo-org/octo-automation@*`

**Filtragem de um fluxo de trabalho específico reutilizável em uma referência específica**

Você pode configurar uma declaração personalizada que filtra para um fluxo de trabalho reutilizável específico. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado de um trabalho definido no fluxo de trabalho reutilizável `octo-org/octo-automation/.github/workflows/deployment.yml` e em qualquer repositório pertencente à organização `octo-org`.

* **Assunto**:
  * Sintaxe: `repo:ORG_NAME/*`
  * Exemplo: `repo:octo-org/*`

* **Declaração personalizada**:
  * Sintaxe: `job_workflow_ref:ORG_NAME/REPO_NAME/.github/workflows/WORKFLOW_FILE@ref`
  * Exemplo: `job_workflow_ref:octo-org/octo-automation/.github/workflows/deployment.yml@ 10040c56a8c0253d69db7c1f26a0d227275512e2`
