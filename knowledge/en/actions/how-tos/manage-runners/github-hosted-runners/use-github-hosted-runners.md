---
title: Using GitHub-hosted runners
description: You can assign a job to run on a virtual machine hosted by GitHub.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners.md
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners
---

# Using GitHub-hosted runners

_You can assign a job to run on a virtual machine hosted by GitHub._

## Using a GitHub-hosted runner

To use a GitHub-hosted runner, create a job and use `runs-on` to specify the type of runner that will process the job, such as `ubuntu-latest`, `windows-latest`, or `macos-latest`. For the full list of runner types, see [GitHub-hosted runners reference](../../../reference/runners/github-hosted-runners.md#supported-runners-and-hardware-resources#supported-runners-and-hardware-resources). If you have `repo: write` access to a repository, you can view a list of the runners available to use in workflows in the repository. For more information, see [Viewing available runners for a repository](#viewing-available-runners-for-a-repository).

When the job begins, GitHub automatically provisions a new VM for that job. All steps in the job execute on the VM, allowing the steps in that job to share information using the runner's filesystem. You can run workflows directly on the VM or in a Docker container. When the job has finished, the VM is automatically decommissioned.

The following diagram demonstrates how two jobs in a workflow are executed on two different GitHub-hosted runners.

![Diagram of a workflow that consists of two jobs. One job runs on Ubuntu and the other runs on Windows.](https://docs.github.com/assets/images/help/actions/overview-github-hosted-runner.png)

The following example workflow has two jobs, named `Run-npm-on-Ubuntu` and `Run-PSScriptAnalyzer-on-Windows`. When this workflow is triggered, GitHub provisions a new virtual machine for each job.

* The job named `Run-npm-on-Ubuntu` is executed on a Linux VM, because the job's `runs-on:` specifies `ubuntu-latest`.
* The job named `Run-PSScriptAnalyzer-on-Windows` is executed on a Windows VM, because the job's `runs-on:` specifies `windows-latest`.

```yaml copy
name: Run commands on different operating systems
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  Run-npm-on-Ubuntu:
    name: Run npm on Ubuntu
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm help

  Run-PSScriptAnalyzer-on-Windows:
    name: Run PSScriptAnalyzer on Windows
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v6
      - name: Install PSScriptAnalyzer module
        shell: pwsh
        run: |
          Set-PSRepository PSGallery -InstallationPolicy Trusted
          Install-Module PSScriptAnalyzer -ErrorAction Stop
      - name: Get list of rules
        shell: pwsh
        run: |
          Get-ScriptAnalyzerRule
```

While the job runs, the logs and output can be viewed in the GitHub UI:

![Screenshot of a workflow run. The steps for the "Run PSScriptAnalyzer on Windows" job are displayed.](https://docs.github.com/assets/images/help/repository/actions-runner-output.png)

The GitHub Actions runner application is open source. You can contribute and file issues in the [runner](https://github.com/actions/runner) repository.

## Viewing available runners for a repository

If you have `repo: write` access to a repository, you can view a list of the runners available to the repository.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, under the "Management" section, click ** Runners**.
1. Review the list of available GitHub-hosted runners for the repository.
1. Optionally, to copy a runner's label to use it in a workflow, click  to the right of the runner, then click **Copy label**.

!!! note
    Enterprise and organization owners and users with the "Manage organization runners and runner groups" permission can create runners from this page. To create a new runner, click **New runner** at the top right of the list of runners to add runners to the repository.

    For more information, see [Managing larger runners](../larger-runners/manage-larger-runners.md) and [Adding self-hosted runners](../self-hosted-runners/add-runners.md).

    For more information about custom organization roles, see [Permissions of custom organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles).
