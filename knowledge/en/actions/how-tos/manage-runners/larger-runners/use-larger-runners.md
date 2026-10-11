---
title: Running jobs on larger runners
description: Identify available larger runners, then route jobs to the right runners by using runner groups and workflow labels.
lang: en
plan: feature
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/larger-runners/use-larger-runners.md
captured: '2026-10-11'
section: How tos / Manage runners / Larger runners
---

# Running jobs on larger runners

_Identify available larger runners, then route jobs to the right runners by using runner groups and workflow labels._

## Identifying available runners for a repository

If you have `repo: write` access to a repository, you can view a list of the runners available to the repository.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, under the "Management" section, click ** Runners**.
1. Review the list of available runners for the repository.
1. Optionally, to copy a runner's label to use it in a workflow, click  to the right of the runner, then click **Copy label**.

!!! note
    Enterprise and organization owners and users with the "Manage organization runners and runner groups" permission can create runners from this page. To create a new runner, click **New runner** at the top right of the list of runners to add runners to the repository.

    For more information, see [Managing larger runners](manage-larger-runners.md) and [Adding self-hosted runners](../self-hosted-runners/add-runners.md).

    For more information about custom organization roles, see [Permissions of custom organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles).

## Targeting larger runners in a workflow

After you identify the larger runners you want to use, you can target them in your workflow with runner groups, workflow labels, or both. Use runner groups to route jobs to a set of runners, workflow labels to target runners with a specific label, or both when a job must match both conditions.

If an administrator has disabled standard GitHub-hosted runners, you can only use runner groups.

### Targeting by runner group

Reference the runner group name in your workflow. Use this when you want to route a job to any available runner in a specific group.

**Linux**

In this example, runners have been added to a group called `build-runners`. The `runs-on` key sends the job to any available runner in the `build-runners` group:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: build-runners
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**Windows**

In this example, runners have been added to a group called `build-runners`. The `runs-on` key sends the job to any available runner in the `build-runners` group:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: build-runners
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**macOS**

In this example, the `runs-on` key sends the job to any available runner in the `macos-build-runners` group:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on:
      group: macos-build-runners
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

### Targeting by workflow label

Reference a workflow label in your workflow when you want to route a job to runners that share a specific label.

Larger runners are automatically assigned a workflow label that matches the runner name.

**Linux**

In this example, the `runs-on` key sends the job to any available runner that has been assigned the `ubuntu-24.04-16core` label:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**Windows**

In this example, the `runs-on` key sends the job to any available runner that has been assigned the `windows-2022-16core` label:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      labels: windows-2022-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**macOS**

For macOS larger runners, you can use either GitHub-defined workflow labels or the workflow label that is automatically assigned from the larger runner name you set when you create it. For a list of available macOS workflow labels, see [Larger runners reference](../../../reference/runners/larger-runners.md#available-macos-larger-runners-and-labels#available-macos-larger-runners-and-labels).

In this example, the `runs-on` key sends the job to any available runner that has been assigned the `macos-26-xlarge` label.

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on: macos-26-xlarge
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

### Using labels and groups to control where jobs are run

Use both labels and groups when a job must run only on runners in a specific group that also have a specific label. The runner must meet both requirements to be eligible to run the job.

**Linux**

When you combine groups and labels, the runner must meet both requirements to be eligible to run the job.

In this example, the `runs-on` key combines `group` and `labels` so that the job is routed to any available runner within the group that also has a matching label:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: ubuntu-runners
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**Windows**

When you combine groups and labels, the runner must meet both requirements to be eligible to run the job.

In this example, the `runs-on` key combines `group` and `labels` so that the job is routed to any available runner within the group that also has a matching label:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: ubuntu-runners
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

**macOS**

In this example, the `runs-on` key combines `group` and `labels` so that the job is routed to any available runner within the group that also has a matching label:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-swift-version:
    runs-on:
      group: macos-runners
      labels: macos-26-xlarge
    steps:
      - uses: actions/checkout@v6
      - name: Build
        run: swift build
      - name: Run tests
        run: swift test
```

## Further reading

For syntax details for the `runs-on` key, see [Workflow syntax for GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on#jobsjob_idruns-on).

For specifications, labels, limitations, and troubleshooting information, see [Larger runners reference](../../../reference/runners/larger-runners.md).
