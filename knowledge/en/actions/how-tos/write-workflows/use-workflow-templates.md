---
title: Using workflow templates
description: GitHub provides workflow templates for a variety of languages and tooling.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/write-workflows/use-workflow-templates.md
captured: '2026-10-11'
section: How tos / Write workflows
---

# Using workflow templates

_GitHub provides workflow templates for a variety of languages and tooling._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Choosing and using a workflow template

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. If you already have a workflow in your repository, click **New workflow**.
1. The "Choose a workflow" page shows a selection of recommended workflow templates. Find the workflow template that you want to use, then click **Configure**. To help you find the workflow template that you want, you can search for keywords or filter by category.
1. If the workflow template contains comments detailing additional setup steps, follow these steps.

   There are guides to accompany many of the workflow templates for building and testing projects. For more information, see [Build and test code](../../tutorials/build-and-test-code.md).

1. Some workflow templates use secrets. For example, `${{ secrets.npm_token }}`. If the workflow template uses a secret, store the value described in the secret name as a secret in your repository. For more information, see [Using secrets in GitHub Actions](choose-what-workflows-do/use-secrets.md).
1. Optionally, make additional changes. For example, you might want to change the value of `on` when the workflow runs.
1. Click **Start commit**.
1. Write a commit message and decide whether to commit directly to the default branch or to open a pull request.

## Further reading

* [Continuous integration](../../get-started/continuous-integration.md)
* [Manage workflow runs](../manage-workflow-runs.md)
* [Monitor workflows](../monitor-workflows.md)
* [Github actions](https://docs.github.com/billing/concepts/product-billing/github-actions)
