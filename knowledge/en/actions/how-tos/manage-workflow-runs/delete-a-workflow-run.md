---
title: Deleting a workflow run
description: You can delete a workflow run that has been completed, or is more than two weeks old.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/delete-a-workflow-run.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Deleting a workflow run

_You can delete a workflow run that has been completed, or is more than two weeks old._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

Write access to the repository is required to perform these steps.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. To delete a workflow run, select , then click **Delete workflow run**.

   ![Screenshot of a list of workflow runs. To the right of a run, an icon of three horizontal dots is highlighted with an orange outline.](https://docs.github.com/assets/images/help/settings/workflow-delete-run.png)

1. Review the confirmation prompt and click **Yes, permanently delete this workflow run**.
