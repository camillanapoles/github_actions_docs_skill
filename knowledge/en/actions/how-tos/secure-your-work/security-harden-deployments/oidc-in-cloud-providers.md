---
title: Configuring OpenID Connect in cloud providers
description: Use OpenID Connect within your workflows to authenticate with cloud providers.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers.md
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configuring OpenID Connect in cloud providers

_Use OpenID Connect within your workflows to authenticate with cloud providers._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Overview

OpenID Connect (OIDC) allows your GitHub Actions workflows to access resources in your cloud provider, without having to store any credentials as long-lived GitHub secrets.

To use OIDC, you will first need to configure your cloud provider to trust GitHub's OIDC as a federated identity, and must then update your workflows to authenticate using tokens.

## Prerequisites

* To learn the basic concepts of how GitHub uses OpenID Connect (OIDC), and its architecture and benefits, see [OpenID Connect](../../../concepts/security/openid-connect.md).

* Before proceeding, you must plan your security strategy to ensure that access tokens are only allocated in a predictable way. To control how your cloud provider issues access tokens, you **must** define at least one condition, so that untrusted repositories can’t request access tokens for your cloud resources. For more information, see [OpenID Connect](../../../concepts/security/openid-connect.md#establishing-oidc-trust-with-your-cloud-provider#establishing-oidc-trust-with-your-cloud-provider)

[OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).
* OIDC tokens requested for Dependabot update jobs have an `event_name` claim of `dynamic`. If your trust policy is intended to authorize only GitHub Actions workflows and your cloud provider supports conditions on `event_name`, allow only the event names expected by your workflows. For more information, see [OpenID Connect](../../../concepts/security/openid-connect.md#establishing-oidc-trust-with-your-cloud-provider#establishing-oidc-trust-with-your-cloud-provider)

[OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* If you're following this guide on GHE.com, understand that you must substitute certain values in the following documentation. See [OpenID Connect](../../../concepts/security/openid-connect.md#configuring-oidc-on-ghecom#configuring-oidc-on-ghecom).

## Updating your GitHub Actions workflow

To update your workflows for OIDC, you will need to make two changes to your YAML:
1. Add permissions settings for the token.
1. Use the official action from your cloud provider to exchange the OIDC token (JWT) for a cloud access token.

If your cloud provider doesn't yet offer an official action, you can update your workflows to perform these steps manually.

> [!NOTE]
> When environments are used in workflows or in OIDC policies, we recommend adding protection rules to the environment for additional security. For example, you can configure deployment rules on an environment to restrict which branches and tags can deploy to the environment or access environment secrets. For more information, see [Managing environments for deployment](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adding permissions settings

The job or workflow run requires a `permissions` setting with [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) to allow GitHub's OIDC provider to create a JSON Web Token for every run.

> [!NOTE] Setting `id-token: write` in the workflow’s permissions does not give the workflow permission to modify or write to any resources. Instead, it only allows the workflow to request (fetch) and use (set) an OIDC token for an action or step. This token is then used to authenticate with external services using a short-lived access token.

For detailed information on required permissions, configuration examples, and advanced scenarios, see [OpenID Connect reference](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token#workflow-permissions-for-the-requesting-the-oidc-token).

### Using official actions

If your cloud provider has created an official action for using OIDC with GitHub Actions, it will allow you to easily exchange the OIDC token for an access token. You can then update your workflows to use this token when accessing cloud resources.

For example, Alibaba Cloud created [`aliyun/configure-aliyun-credentials-action`](https://github.com/aliyun/configure-aliyun-credentials-action) to integrate with using OIDC with GitHub.

## Using custom actions

If your cloud provider doesn't have an official action, or if you prefer to create custom scripts, you can manually request the JSON Web Token (JWT) from GitHub's OIDC provider.

If you're not using an official action, then GitHub recommends that you use the Actions core toolkit. Alternatively, you can use the following environment variables to retrieve the token: `ACTIONS_ID_TOKEN_REQUEST_TOKEN`, `ACTIONS_ID_TOKEN_REQUEST_URL`.

To update your workflows using this approach, you will need to make three changes to your YAML:

1. Add permissions settings for the token.
1. Add code that requests the OIDC token from GitHub's OIDC provider.
1. Add code that exchanges the OIDC token with your cloud provider for an access token.

### Requesting the JWT using the Actions core toolkit

The following example demonstrates how to use `actions/github-script` with the `core` toolkit to request the JWT from GitHub's OIDC provider. For more information, see [Creating a JavaScript action](../../../tutorials/create-actions/create-a-javascript-action.md#adding-actions-toolkit-packages#adding-actions-toolkit-packages).

```yaml
jobs:
  job:
    environment: Production
    runs-on: ubuntu-latest
    steps:
    - name: Install OIDC Client from Core Package
      run: npm install @actions/core@1.6.0 @actions/http-client
    - name: Get Id Token
      uses: actions/github-script@v8
      id: idtoken
      with:
        script: |
          let id_token = await core.getIDToken()
          core.setOutput('id_token', id_token)
```

### Requesting the JWT using environment variables

The following example demonstrates how to use environment variables to request a JSON Web Token.

For your deployment job, you will need to define the token settings, using `actions/github-script` with the `core` toolkit. For more information, see [Creating a JavaScript action](../../../tutorials/create-actions/create-a-javascript-action.md#adding-actions-toolkit-packages#adding-actions-toolkit-packages).

For example:

```yaml
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/github-script@v8
      id: script
      timeout-minutes: 10
      with:
        debug: true
        script: |
          const token = process.env['ACTIONS_ID_TOKEN_REQUEST_TOKEN']
          const runtimeUrl = process.env['ACTIONS_ID_TOKEN_REQUEST_URL']
          core.setOutput('TOKEN', token.trim())
          core.setOutput('IDTOKENURL', runtimeUrl.trim())
```

You can then use `curl` to retrieve a JWT from the GitHub OIDC provider. For example:

```yaml
    - run: |
        IDTOKEN=$(curl -H "Authorization: Bearer ${{steps.script.outputs.TOKEN}}" ${{steps.script.outputs.IDTOKENURL}}  -H "Accept: application/json; api-version=2.0" -H "Content-Type: application/json" -d "{}" | jq -r '.value')
        echo $IDTOKEN
        jwtd() {
            if [[ -x $(command -v jq) ]]; then
                jq -R 'split(".") | .[0],.[1] | @base64d | fromjson' <<< "${1}"
                echo "Signature: $(echo "${1}" | awk -F'.' '{print $3}')"
            fi
        }
        jwtd $IDTOKEN
        echo "idToken=${IDTOKEN}" >> $GITHUB_OUTPUT
      id: tokenid
```

### Getting the access token from the cloud provider

You will need to present the OIDC JSON web token to your cloud provider in order to obtain an access token.

For each deployment, your workflows must use cloud login actions (or custom scripts) that fetch the OIDC token and present it to your cloud provider. The cloud provider then validates the claims in the token; if successful, it provides a cloud access token that is available only to that job run. The provided access token can then be used by subsequent actions in the job to connect to the cloud and deploy to its resources.

The steps for exchanging the OIDC token for an access token will vary for each cloud provider.

### Accessing resources in your cloud provider

Once you've obtained the access token, you can use specific cloud actions or scripts to authenticate to the cloud provider and deploy to its resources. These steps could differ for each cloud provider.

For example, Alibaba Cloud maintains their own instructions for OIDC authentication. For more information, see [Overview of OIDC-based SSO](https://www.alibabacloud.com/help/en/ram/user-guide/overview-of-oidc-based-sso) in the Alibaba Cloud documentation.

In addition, the default expiration time of this access token could vary between each cloud and can be configurable at the cloud provider's side.

## Further reading

* [Using OpenID Connect with reusable workflows](oidc-with-reusable-workflows.md)
* [Self-hosted runners reference](../../../reference/runners/self-hosted-runners.md)
