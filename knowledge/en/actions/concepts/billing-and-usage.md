---
title: Billing and usage
description: There are usage limits for GitHub Actions workflows. Usage charges apply to repositories that go beyond the amount of free minutes and storage for a repository.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/billing-and-usage.md
captured: '2026-10-11'
section: Concepts
---

# Billing and usage

_There are usage limits for GitHub Actions workflows. Usage charges apply to repositories that go beyond the amount of free minutes and storage for a repository._

## About billing for GitHub Actions

GitHub Actions usage is free for standard GitHub-hosted runners in public repositories, and for self-hosted runners. See [Choosing the runner for a job](../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#standard-github-hosted-runners-for-public-repositories#standard-github-hosted-runners-for-public-repositories). For private repositories, each GitHub account receives a quota of free minutes and storage for use with GitHub-hosted runners, depending on the account's plan. Any usage beyond the included amounts is billed to your account. For more information, see [Github actions](https://docs.github.com/billing/concepts/product-billing/github-actions).

GitHub Actions usage is free for GitHub Enterprise Server instances that use self-hosted runners. For more information, see [Self-hosted runners](runners/self-hosted-runners.md).

## Availability

GitHub Actions is available on all GitHub products, but GitHub Actions is not available for private repositories owned by accounts using legacy per-repository plans. See [Githubs plans](https://docs.github.com/get-started/learning-about-github/githubs-plans).

## Usage limits and policy

There are several limits on GitHub Actions usage when using GitHub-hosted runners. See [Actions limits](../reference/limits.md).

In addition to the usage limits, you must ensure that you use GitHub Actions within the [GitHub Terms of Service](https://docs.github.com/free-pro-team@latest/site-policy/github-terms/github-terms-of-service). For more information on GitHub Actions-specific terms, see the [GitHub Additional Product Terms](https://docs.github.com/free-pro-team@latest/site-policy/github-terms/github-terms-for-additional-products-and-features#actions).

## GitHub Actions usage metrics

Organization owners and users with the "View organization Actions metrics" permission can view GitHub Actions usage metrics for their organization. These metrics can help you understand how and where your Actions minutes are being used. For more information, see [Viewing github actions metrics for your organization](https://docs.github.com/enterprise-cloud@latest/organizations/collaborating-with-groups-in-organizations/viewing-github-actions-metrics-for-your-organization).

When you view usage metrics, it is important to remember that GitHub Actions usage metrics do not apply minute multipliers to the metrics displayed. While they _can_ help you understand your bill, their primary purpose is to help you understand how and where Actions minutes are being used in your organization.

For more information about minute multipliers, see [Github actions](https://docs.github.com/billing/concepts/product-billing/github-actions#baseline-minute-costs#baseline-minute-costs).

## Billing for reusable workflows

If you reuse a workflow, billing is always associated with the caller workflow. Assignment of GitHub-hosted runners is always evaluated using only the caller's context. The caller cannot use GitHub-hosted runners from the called repository.

For more information see, [Reuse workflows](../how-tos/reuse-automations/reuse-workflows.md).

## Next steps

You can manage your GitHub Actions usage and retention policies for your repository, organization, or enterprise account. For more information, see:
* [Managing github actions settings for a repository](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
* [Configuring the retention period for github actions artifacts and logs in your organization](https://docs.github.com/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization)
* [Disabling or limiting github actions for your organization](https://docs.github.com/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization)
* [Enforcing policies for github actions in your enterprise](https://docs.github.com/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise)
