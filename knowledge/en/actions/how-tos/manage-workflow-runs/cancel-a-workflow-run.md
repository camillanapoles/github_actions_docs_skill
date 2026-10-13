---
title: Canceling a workflow run
description: You can cancel a workflow run, including all jobs and steps, that is in progress.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/cancel-a-workflow-run.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Canceling a workflow run

_You can cancel a workflow run, including all jobs and steps, that is in progress._

## Canceling a workflow run { #canceling-a-workflow-run-1 }

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the `queued` or `in progress` run that you want to cancel.
1. In the upper-right corner of the workflow, click **Cancel workflow**.
![Screenshot showing the summary for a workflow that is currently running. The "Cancel workflow" button is highlighted with a dark orange outline.](https://docs.github.com/assets/images/help/repository/cancel-check-suite-updated.png)

## Next steps

To learn about the process GitHub uses to cancel a workflow run, as well as the ways you can free up related resources, see [Workflow cancellation reference](../../reference/workflows-and-actions/workflow-cancellation.md).
