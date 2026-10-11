---
title: Viewing workflow run history
description: You can view logs for each run of a workflow. Logs include the status for each job and step in a workflow.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/monitor-workflows/view-workflow-run-history.md
captured: '2026-10-11'
section: How tos / Monitor workflows
---

# Viewing workflow run history

_You can view logs for each run of a workflow. Logs include the status for each job and step in a workflow._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

Read access to the repository is required to perform these steps.

**Usando a interface do GitHub**

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.

**Usando a CLI do GitHub**

> [!NOTE]
> To learn more about GitHub CLI, see [About github cli](https://docs.github.com/github-cli/github-cli/about-github-cli).

## Viewing recent workflow runs

To list the recent workflow runs, use the `run list` subcommand.

```shell
gh run list
```

To specify the maximum number of runs to return, you can use the `-L` or `--limit` flag . The default is `10`.

```shell
gh run list --limit 5
```

To only return runs for the specified workflow, you can use the `-w` or `--workflow` flag. Replace `workflow` with either the workflow name, workflow ID, or workflow file name. For example, `"Link Checker"`, `1234567`, or `"link-check-test.yml"`.

```shell
gh run list --workflow WORKFLOW
```

## Viewing details for a specific workflow run

To display details for a specific workflow run, use the `run view` subcommand. Replace `run-id` with the ID of the run that you want to view. If you don't specify a `run-id`, GitHub CLI returns an interactive menu for you to choose a recent run.

```shell
gh run view RUN_ID
```

To include job steps in the output, use the `-v` or `--verbose` flag.

```shell
gh run view RUN_ID --verbose
```

To view details for a specific job in the run, use the `-j` or `--job` flag. Replace `job-id` with the ID of the job that you want to view.

```shell
gh run view --job JOB_ID
```

To view the full log for a job, use the `--log` flag.

```shell
gh run view --job JOB_ID --log
```

Use the `--exit-status` flag to exit with a non-zero status if the run failed. For example:

```shell
gh run view 0451 --exit-status && echo "run pending or passed"
```
