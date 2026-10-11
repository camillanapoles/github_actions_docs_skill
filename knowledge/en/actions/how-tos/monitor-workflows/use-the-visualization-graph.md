---
title: Using the visualization graph
description: Every workflow run generates a real-time graph that illustrates the run progress. You can use this graph to monitor and debug workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/monitor-workflows/use-the-visualization-graph.md
captured: '2026-10-11'
section: How tos / Monitor workflows
---

# Using the visualization graph

_Every workflow run generates a real-time graph that illustrates the run progress. You can use this graph to monitor and debug workflows._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, click the workflow you want to see.

   ![Screenshot of the left sidebar of the "Actions" tab. A workflow, "CodeQL," is outlined in dark orange.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
1. From the list of workflow runs, click the name of the run to see the workflow run summary.

1. The graph displays each job in the workflow. An icon to the left of the job name indicates the status of the job. Lines between jobs indicate dependencies.

   ![Screenshot of the visualization graph of a workflow run.](/assets/images/help/actions/workflow-graph.png)
1. To view a job's log, click the job.
