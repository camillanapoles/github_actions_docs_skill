---
title: Configuring OpenID Connect in JFrog
description: Use OpenID Connect within your workflows to authenticate with JFrog.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-jfrog.md
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configuring OpenID Connect in JFrog

_Use OpenID Connect within your workflows to authenticate with JFrog._

## Overview

OpenID Connect (OIDC) allows your GitHub Actions workflows to authenticate with [JFrog](https://jfrog.com/) to download and publish artifacts without storing JFrog passwords, tokens, or API keys in GitHub.

This guide gives an overview of how to configure JFrog to trust GitHub's OIDC as a federated identity, and demonstrates how to use this configuration in a GitHub Actions workflow.

For an example GitHub Actions workflow, see [Sample GitHub Actions Integration](https://jfrog.com/help/r/jfrog-platform-administration-documentation/sample-github-actions-integration) in the JFrog documentation.

For an example GitHub Actions workflow using the JFrog CLI, see [`build-publish.yml`](https://github.com/jfrog/jfrog-github-oidc-example/blob/main/.github/workflows/build-publish.yml) in the `jfrog-github-oidc-example` repository.

## Prerequisites

* To learn the basic concepts of how GitHub uses OpenID Connect (OIDC), and its architecture and benefits, see [OpenID Connect](../../../concepts/security/openid-connect.md).

* Before proceeding, you must plan your security strategy to ensure that access tokens are only allocated in a predictable way. To control how your cloud provider issues access tokens, you **must** define at least one condition, so that untrusted repositories can’t request access tokens for your cloud resources. For more information, see [OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* OIDC tokens requested for Dependabot update jobs have an `event_name` claim of `dynamic`. If your trust policy is intended to authorize only GitHub Actions workflows and your cloud provider supports conditions on `event_name`, allow only the event names expected by your workflows. For more information, see [OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* If you're following this guide on GHE.com, understand that you must substitute certain values in the following documentation. See [OpenID Connect](../../../concepts/security/openid-connect.md#configuring-oidc-on-ghecom#configuring-oidc-on-ghecom).

* To be secure, you need to set a Claims JSON in JFrog when configuring identity mappings. For more information, see [Configure identity mappings](https://jfrog.com/help/r/jfrog-platform-administration-documentation/configure-identity-mappings) and [OpenID Connect reference](../../../reference/security/oidc.md#customizing-the-token-claims#customizing-the-token-claims).

  For example, you can set `iss` to `https://token.actions.githubusercontent.com`, and the `repository` to something like `octo-org/octo-repo`. JFrog identity mappings match each claim against an exact value, so to ensure only GitHub Actions workflows from the specified repository have access to your JFrog platform, also set `event_name` to the event that triggers your workflow, such as `push`. This prevents OIDC tokens requested for Dependabot update jobs, which have an `event_name` of `dynamic`, from matching the identity mapping. If your workflows are triggered by more than one event, create a separate identity mapping for each event name. The following is an example Claims JSON when configuring identity mappings.

                ```json copy
{
    "iss": "https://token.actions.githubusercontent.com",
    "repository": "octo-org/octo-repo",
    "event_name": "push"
}
                ```

## Adding the identity provider to JFrog

To use OIDC with JFrog, establish a trust relationship between GitHub Actions and the JFrog platform. For more information about this process, see [OpenID Connect Integration](https://docs.jfrog.com/administration/docs/openid-connect-integration) in the JFrog documentation.

1. Sign in to your JFrog Platform.
1. Configure trust between JFrog and your GitHub Actions workflows.
1. Configure identity mappings.

## Updating your GitHub Actions workflow

### Authenticating with JFrog using OIDC

In your GitHub Actions workflow file, ensure you are using the provider name and audience you configured in the JFrog Platform.

The following example uses the placeholders `YOUR_PROVIDER_NAME` and `YOUR_AUDIENCE`.

```yaml
```
# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.
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
    When OIDC authentication is used, the `setup-jfrog-cli` action automatically provides `oidc-user` and `oidc-token` as step outputs.
    These can be used for other integrations that require authentication with JFrog.
    To reference these outputs, ensure the step has an explicit `id` defined (for example `id: setup-jfrog-cli`).

```
### Using OIDC Credentials in other steps

```yaml
```
# This workflow uses actions that are not certified by GitHub. { #this-workflow-uses-actions-that-are-not-certified-by-github-1 }
# They are provided by a third-party and are governed by { #they-are-provided-by-a-third-party-and-are-governed-by-1 }
# separate terms of service, privacy policy, and support { #separate-terms-of-service-privacy-policy-and-support-1 }
# documentation. { #documentation-1 }
      - name: Sign in to Artifactory Docker registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.JF_URL }}
          username: ${{ steps.setup-jfrog-cli.outputs.oidc-user }}
          password: ${{ steps.setup-jfrog-cli.outputs.oidc-token }}
```

```
## Further reading

* [OpenID Connect Integration](https://docs.jfrog.com/administration/docs/openid-connect-integration) in the JFrog documentation
* [Identity Mappings](https://jfrog.com/help/r/jfrog-platform-administration-documentation/identity-mappings) in the JFrog documentation
* [OpenID Connect](../../../concepts/security/openid-connect.md)
