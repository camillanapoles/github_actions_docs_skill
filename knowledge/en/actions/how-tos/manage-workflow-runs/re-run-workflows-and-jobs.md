---
title: Re-running workflows and jobs
description: You can re-run a workflow run, all failed jobs in a workflow run, or specific jobs in a workflow run up to 30 days after its initial run.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Re-running workflows and jobs

_You can re-run a workflow run, all failed jobs in a workflow run, or specific jobs in a workflow run up to 30 days after its initial run._

Re-runs use the privileges of the actor who initially triggered the workflow, not the privileges of the actor who initiated the re-run. The workflow will also use the same `GITHUB_SHA` (commit SHA) and `GITHUB_REF` (git ref) of the original event that triggered the workflow run.

A workflow run can be re-run a maximum of 50 times. This limit includes both full re-runs and re-runs of a subset of jobs.

## Re-running all the jobs in a workflow

**Usando a interface do GitHub**

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.
1. In the upper-right corner of the workflow, re-run jobs.

   * If any jobs failed, select the ** Re-run jobs** dropdown menu and click **Re-run all jobs**.
   * If no jobs failed, click **Re-run all jobs**.

1. Optionally, to enable runner diagnostic logging and step debug logging for the re-run, select **Enable debug logging**. For more information, see [Enabling debug logging](../monitor-workflows/enable-debug-logging.md).
1. Click **Re-run jobs**.

**Usando a CLI do GitHub**

1. To re-run a failed workflow run, use the `run rerun` subcommand, replacing `RUN_ID` with the ID of the failed run that you want to re-run. If you don't specify a `run-id`, GitHub CLI returns an interactive menu for you to choose a recent failed run.

                ```shell copy
    gh run rerun RUN_ID
    ```

    To enable runner diagnostic logging and step debug logging for the re-run, use the `--debug` flag.

                ```shell copy
    gh run rerun RUN_ID --debug
    ```

1. To view the progress of the workflow run, use the `run watch` subcommand and select the run from the interactive list.

                ```shell copy
    gh run watch
    ```

## Re-running failed jobs in a workflow

**Usando a interface do GitHub**

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.
1. In the upper-right corner of the workflow, select the ** Re-run jobs** dropdown menu, and click **Re-run failed jobs**.
1. Optionally, to enable runner diagnostic logging and step debug logging for the re-run, select **Enable debug logging**. For more information, see [Enabling debug logging](../monitor-workflows/enable-debug-logging.md).
1. Click **Re-run jobs**.

**Usando a CLI do GitHub**

To re-run failed jobs in a workflow run, use the `run rerun` subcommand with the `--failed` flag. Replace `RUN_ID` with the ID of the run for which you want to re-run failed jobs. If you don't specify a `run-id`, GitHub CLI returns an interactive menu for you to choose a recent failed run.

```shell
gh run rerun RUN_ID --failed
```

To enable runner diagnostic logging and step debug logging for the re-run, use the `--debug` flag.

```shell
gh run rerun RUN_ID --failed --debug
```

## Re-running a specific job in a workflow

**Usando a interface do GitHub**

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.
1. Under the "Jobs" section of the left sidebar, next to the job that you want to re-run, click .

1. Optionally, to enable runner diagnostic logging and step debug logging for the re-run, select **Enable debug logging**. For more information, see [Enabling debug logging](../monitor-workflows/enable-debug-logging.md).
1. Click **Re-run jobs**.

**Usando a CLI do GitHub**

To re-run a specific job in a workflow run, use the `run rerun` subcommand with the `--job` flag. Replace `JOB_ID` with the ID of the job that you want to re-run.

```shell
gh run rerun --job JOB_ID
```

To enable runner diagnostic logging and step debug logging for the re-run, use the `--debug` flag.

```shell
gh run rerun --job JOB_ID --debug
```

## Reviewing previous workflow runs

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.
1. To the right of the run name, select the **Latest** dropdown menu and click a previous run attempt.
