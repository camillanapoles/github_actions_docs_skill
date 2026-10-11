---
title: Removing workflow artifacts
description: You can reclaim used GitHub Actions storage by deleting artifacts before they expire on GitHub.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/remove-workflow-artifacts.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Removing workflow artifacts

_You can reclaim used GitHub Actions storage by deleting artifacts before they expire on GitHub._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Deleting an artifact

!!! warning
    Once you delete an artifact, it cannot be restored.

Write access to the repository is required to perform these steps.

By default, GitHub stores build logs and artifacts for 90 days, and this retention period can be customized. For more information, see [Managing github actions settings for a repository](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-repository#configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-repository).

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.
1. Under **Artifacts**, click  next to the artifact you want to remove.

    ![Screenshot showing artifacts created during a workflow run. A trash can icon, used to remove an artifact, is outlined in dark orange.](/assets/images/help/repository/actions-delete-artifact-updated.png)

## Setting the retention period for an artifact

Retention periods for artifacts and logs can be configured at the repository, organization, and enterprise level. For more information, see [Managing github actions settings for a repository](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#setting-the-check-workflow-run-status-artifact-and-log-retention-period-for-a-repository#setting-the-check-workflow-run-status-artifact-and-log-retention-period-for-a-repository) and [Configuring the retention period for github actions artifacts and logs in your organization](https://docs.github.com/organizations/managing-organization-settings/configuring-the-retention-period-for-github-actions-artifacts-and-logs-in-your-organization).

You can also define a custom retention period for individual artifacts using the `actions/upload-artifact` action in a workflow. For more information, see [Store and share data with workflow artifacts](../../tutorials/store-and-share-data.md#configuring-a-custom-artifact-retention-period#configuring-a-custom-artifact-retention-period).

## Finding the expiration date of an artifact

You can use the API to confirm the date that an artifact is scheduled to be deleted. For more information, see the `expires_at` value returned by the REST API. For more information, see [Artifacts](https://docs.github.com/rest/actions/artifacts).

## Artifacts from deleted workflow runs

When a workflow run is deleted all artifacts associated with the run are also deleted from storage. You can delete a workflow run using the GitHub Actions UI, the REST API, or using the GitHub CLI, see: [Deleting a workflow run](delete-a-workflow-run.md), [Delete a workflow run](https://docs.github.com/rest/actions/workflow-runs#delete-a-workflow-run), or [gh run delete](https://cli.github.com/manual/gh_run_delete).
