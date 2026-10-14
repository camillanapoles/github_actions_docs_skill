---
title: Viewing your current jobs
description: Monitor how GitHub-hosted runners are processing jobs in your organization or enterprise, and identify any related constraints.
lang: en
plan: feature
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/github-hosted-runners/view-current-jobs.md
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners
---

# Viewing your current jobs

_Monitor how GitHub-hosted runners are processing jobs in your organization or enterprise, and identify any related constraints._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Viewing active jobs in your organization or enterprise

You can get a list of all jobs currently running on GitHub-hosted runners in your organization or enterprise.

1. Navigate to the main page of the organization or repository.
1. Click ** Settings**.
1. In the left sidebar, click **Actions**, then click **Runners**.

1. In the "Runners" table, click the entry for **GitHub-hosted runners**. This entry will only be present if you're using GitHub-hosted runners.
1. Review the "Active jobs" section, which contains a list of all jobs currently running on GitHub-hosted runners.

## Viewing queued jobs in your organization or enterprise

GitHub-hosted runners allow you to run jobs concurrently, and the maximum number of concurrent jobs will vary depending on your plan. If you reach the maximum number of concurrent jobs, any new jobs will start to enter a queue. To find out more about the number of concurrent jobs available to your plan, see [Billing and usage](../../../concepts/billing-and-usage.md).

The following procedure demonstrates how to check the maximum number of concurrent jobs you can run.

1. Navigate to the main page of the organization or repository.
1. Click ** Settings**.
1. In the left sidebar, click **Actions**, then click **Runners**.

1. In the "Runners" table, click the entry for **GitHub-hosted runners**. This entry will only be present if you're using GitHub-hosted runners.
1. Review the "All jobs usage" section, which lists the number of active jobs and the maximum number of jobs you can run.
