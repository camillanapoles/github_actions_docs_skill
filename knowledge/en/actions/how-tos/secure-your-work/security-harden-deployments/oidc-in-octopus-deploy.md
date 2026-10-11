---
title: Configuring OpenID Connect in Octopus Deploy
description: Use OpenID Connect within your workflows to authenticate with Octopus Deploy.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-octopus-deploy.md
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configuring OpenID Connect in Octopus Deploy

_Use OpenID Connect within your workflows to authenticate with Octopus Deploy._

## Overview

OpenID Connect (OIDC) allows your GitHub Actions workflows to authenticate with [Octopus Deploy](https://octopus.com/) to push packages, create releases or trigger deployments without storing Octopus Deploy passwords or API keys as long-lived GitHub secrets.

This guide provides an overview of how to configure Octopus Deploy to trust GitHub's OIDC as a federated identity, and includes a workflow example for the [`octopusdeploy/login`](https://github.com/OctopusDeploy/login) action that uses tokens to authenticate to your Octopus Deploy instance.

## Prerequisites

* To learn the basic concepts of how GitHub uses OpenID Connect (OIDC), and its architecture and benefits, see [OpenID Connect](../../../concepts/security/openid-connect.md).

* Before proceeding, you must plan your security strategy to ensure that access tokens are only allocated in a predictable way. To control how your cloud provider issues access tokens, you **must** define at least one condition, so that untrusted repositories can’t request access tokens for your cloud resources. For more information, see [OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* OIDC tokens requested for Dependabot update jobs have an `event_name` claim of `dynamic`. If your trust policy is intended to authorize only GitHub Actions workflows and your cloud provider supports conditions on `event_name`, allow only the event names expected by your workflows. For more information, see [OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* If you're following this guide on GHE.com, understand that you must substitute certain values in the following documentation. See [OpenID Connect](../../../concepts/security/openid-connect.md#configuring-oidc-on-ghecom#configuring-oidc-on-ghecom).

## Adding the identity provider to Octopus Deploy

To use OIDC with Octopus Deploy, first establish a trust relationship between GitHub Actions and your Octopus Deploy instance. For more information about this process, see [Using OpenID Connect with the Octopus API](https://octopus.com/docs/octopus-rest-api/openid-connect) in the Octopus Deploy documentation.

1. Sign in to your Octopus Deploy instance.
1. Create or open the Service Account that will be granted access via the token request.
1. Configure a new OIDC Identity, defining the relevant subject that the GitHub Actions workflow token request will be validated against.

## Updating your GitHub Actions workflow

To update your workflows for OIDC, you will need to make two changes to your YAML:
1. Add permissions settings for the token.
1. Use the [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) action to exchange the OIDC token (JWT) for a cloud access token.

!!! note
    When environments are used in workflows or in OIDC policies, we recommend adding protection rules to the environment for additional security. For example, you can configure deployment rules on an environment to restrict which branches and tags can deploy to the environment or access environment secrets. For more information, see [Managing environments for deployment](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adding permissions settings

The job or workflow run requires a `permissions` setting with [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) to allow GitHub's OIDC provider to create a JSON Web Token for every run.

> [!NOTE] Setting `id-token: write` in the workflow’s permissions does not give the workflow permission to modify or write to any resources. Instead, it only allows the workflow to request (fetch) and use (set) an OIDC token for an action or step. This token is then used to authenticate with external services using a short-lived access token.

For detailed information on required permissions, configuration examples, and advanced scenarios, see [OpenID Connect reference](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token#workflow-permissions-for-the-requesting-the-oidc-token).

### Requesting the access token

The [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) action receives a JWT from the GitHub OIDC provider, and then requests an access token from your Octopus Server instance. For more information, see the [`OctopusDeploy/login`](https://github.com/OctopusDeploy/login) documentation.

The following example exchanges an OIDC ID token with your Octopus Deploy instance to receive an access token, which can then be used to access your Octopus Deploy resources. Be sure to replace the `server` and `service_account_id` details appropriately for your scenario.

```yaml copy
# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.

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

## Further reading

* [Using OpenID Connect with reusable workflows](oidc-with-reusable-workflows.md)
* [Self-hosted runners reference](../../../reference/runners/self-hosted-runners.md)
