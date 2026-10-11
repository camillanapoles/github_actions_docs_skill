---
title: Manually running a workflow
description: When a workflow is configured to run on the `workflow_dispatch` event, you can run the workflow using the Actions tab on GitHub, GitHub CLI, or the REST API.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/manually-run-a-workflow.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Manually running a workflow

_When a workflow is configured to run on the `workflow_dispatch` event, you can run the workflow using the Actions tab on GitHub, GitHub CLI, or the REST API._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Configuring a workflow to run manually

To run a workflow manually, the workflow must be configured to run on the `workflow_dispatch` event.

To trigger the `workflow_dispatch` event, your workflow must be in the default branch. For more information about configuring the `workflow_dispatch` event, see [Events that trigger workflows](../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch#workflow_dispatch).

Write access to the repository is required to perform these steps.

## Running a workflow

**Usando a interface do GitHub**

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the name of the workflow you want to run.

   ![Screenshot of the "Actions" page. In the left sidebar, a workflow name is highlighted with an outline in dark orange.](/assets/images/help/repository/actions-select-workflow-2022.png)

1. Above the list of workflow runs, click the **Run workflow** button.

   > [!NOTE]
   > To see the **Run workflow** button, your workflow file must use the `workflow_dispatch` event trigger. Only workflow files that use the `workflow_dispatch` event trigger will have the option to run the workflow manually using the **Run workflow** button. For more information about configuring the `workflow_dispatch` event, see [Events that trigger workflows](../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch#workflow_dispatch).

   ![Screenshot of a workflow page. Above the list of workflow runs, a button, labeled "Run workflow", is outlined in dark orange.](/assets/images/help/actions/actions-workflow-dispatch.png)
1. Select the **Branch** dropdown menu and click a branch to run the workflow on.
1. If the workflow requires input, fill in the fields.
1. Click **Run workflow**.

**Usando a CLI do GitHub**

> [!NOTE]
> To learn more about GitHub CLI, see [About github cli](https://docs.github.com/github-cli/github-cli/about-github-cli).

To run a workflow, use the `workflow run` subcommand. Replace the `workflow` parameter with either the name, ID, or file name of the workflow you want to run. For example, `"Link Checker"`, `1234567`, or `"link-check-test.yml"`. If you don't specify a workflow, GitHub CLI returns an interactive menu for you to choose a workflow.

```shell
gh workflow run WORKFLOW
```

If your workflow accepts inputs, GitHub CLI will prompt you to enter them. Alternatively, you can use `-f` or `-F` to add an input in `key=value` format. Use `-F` to read from a file.

```shell
gh workflow run greet.yml -f name=mona -f greeting=hello -F data=@myfile.txt
```

You can also pass inputs as JSON by using standard input.

```shell
echo '{"name":"mona", "greeting":"hello"}' | gh workflow run greet.yml --json
```

To run a workflow on a branch other than the repository's default branch, use the `--ref` flag.

```shell
gh workflow run WORKFLOW --ref BRANCH
```

To view the progress of the workflow run, use the `run watch` subcommand and select the run from the interactive list.

```shell
gh run watch
```

## Running a workflow using the REST API

When using the REST API, you configure the `inputs` and `ref` as request body parameters. If the inputs are omitted, the default values defined in the workflow file are used.

> [!NOTE]
> You can define up to 25

10 `inputs` for a `workflow_dispatch` event.

For more information about using the REST API, see [Workflows](https://docs.github.com/rest/actions/workflows#create-a-workflow-dispatch-event#create-a-workflow-dispatch-event).
