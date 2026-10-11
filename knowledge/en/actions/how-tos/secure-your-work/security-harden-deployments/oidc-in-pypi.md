---
title: Configuring OpenID Connect in PyPI
description: Use OpenID Connect within your workflows to authenticate with PyPI.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-pypi.md
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configuring OpenID Connect in PyPI

_Use OpenID Connect within your workflows to authenticate with PyPI._

## Overview

OpenID Connect (OIDC) allows your GitHub Actions workflows to authenticate with [PyPI](https://pypi.org) to publish Python packages.

This guide gives an overview of how to configure PyPI to trust GitHub's OIDC as a federated identity, and demonstrates how to use this configuration in the [`pypa/gh-action-pypi-publish`](https://github.com/marketplace/actions/pypi-publish) action to publish packages to PyPI (or other Python package repositories) without any manual API token management.

## Prerequisites

* To learn the basic concepts of how GitHub uses OpenID Connect (OIDC), and its architecture and benefits, see [OpenID Connect](../../../concepts/security/openid-connect.md).

* Before proceeding, you must plan your security strategy to ensure that access tokens are only allocated in a predictable way. To control how your cloud provider issues access tokens, you **must** define at least one condition, so that untrusted repositories can’t request access tokens for your cloud resources. For more information, see [OpenID Connect](../../../concepts/security/openid-connect.md#establishing-oidc-trust-with-your-cloud-provider#establishing-oidc-trust-with-your-cloud-provider)

[OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).
* OIDC tokens requested for Dependabot update jobs have an `event_name` claim of `dynamic`. If your trust policy is intended to authorize only GitHub Actions workflows and your cloud provider supports conditions on `event_name`, allow only the event names expected by your workflows. For more information, see [OpenID Connect](../../../concepts/security/openid-connect.md#establishing-oidc-trust-with-your-cloud-provider#establishing-oidc-trust-with-your-cloud-provider)

[OpenID Connect reference](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* If you're following this guide on GHE.com, understand that you must substitute certain values in the following documentation. See [OpenID Connect](../../../concepts/security/openid-connect.md#configuring-oidc-on-ghecom#configuring-oidc-on-ghecom).

## Adding the identity provider to PyPI

To use OIDC with PyPI, add a trust configuration that links each project on PyPI to each repository and workflow combination that's allowed to publish for it.

1. Sign in to PyPI and navigate to the trusted publishing settings for the project you'd like to configure. For a project named `myproject`, this will be at `https://pypi.org/manage/project/myproject/settings/publishing/`.

1. Configure a trust relationship between the PyPI project and a GitHub repository (and workflow within the repository). For example, if your GitHub repository is at `myorg/myproject` and your release workflow is defined in `release.yml` with an environment of `release`, you should use the following settings for your trusted publisher on PyPI.

   > [!NOTE]
   > Enter these values carefully. Giving the incorrect user, repository, or workflow the ability to publish to your PyPI project is equivalent to sharing an API token.

   * Owner: `myorg`
   * Repository name: `myproject`
   * Workflow name: `release.yml`
   * (Optionally) a GitHub Actions environment name: `release`

## Updating your GitHub Actions workflow

Once your trusted publisher is registered on PyPI, you can update your release workflow to use trusted publishing.

> [!NOTE]
> When environments are used in workflows or in OIDC policies, we recommend adding protection rules to the environment for additional security. For example, you can configure deployment rules on an environment to restrict which branches and tags can deploy to the environment or access environment secrets. For more information, see [Managing environments for deployment](../../deploy/configure-and-manage-deployments/manage-environments.md).

The [`pypa/gh-action-pypi-publish`](https://github.com/marketplace/actions/pypi-publish) action has built-in support for trusted publishing, which can be enabled by giving its containing job the `id-token: write` permission and omitting `username` and `password`.

The following example uses the `pypa/gh-action-pypi-publish` action to exchange an OIDC token for a PyPI API token, which is then used to upload a package's release distributions to PyPI.

```yaml copy
# This workflow uses actions that are not certified by GitHub.
# They are provided by a third-party and are governed by
# separate terms of service, privacy policy, and support
# documentation.
jobs:
  release-build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: build release distributions
        run: |
          # NOTE: put your own distribution build steps here.
          python -m pip install build
          python -m build

      - name: upload windows dists
        uses: actions/upload-artifact@v4

v3
        with:
          name: release-dists
          path: dist/

  pypi-publish:
    runs-on: ubuntu-latest
    needs:
      - release-build
    permissions:
      id-token: write

    steps:
      - name: Retrieve release distributions
        uses: actions/download-artifact@v5

v3
        with:
          name: release-dists
          path: dist/

      - name: Publish release distributions to PyPI
        uses: pypa/gh-action-pypi-publish@3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f
```
