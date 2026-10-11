---
title: Customizing GitHub-hosted runners
description: You can install additional software on GitHub-hosted runners as a part of your workflow.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/github-hosted-runners/customize-runners.md
captured: '2026-10-11'
section: How tos / Manage runners / Github hosted runners
---

# Customizing GitHub-hosted runners

_You can install additional software on GitHub-hosted runners as a part of your workflow._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

If you require additional software packages on GitHub-hosted runners, you can create a job that installs the packages as part of your workflow.

To see which packages are already installed by default, see [GitHub-hosted runners](../../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images#preinstalled-software-for-github-owned-images).

This guide demonstrates how to create a job that installs additional software on a GitHub-hosted runner.

## Installing software on Ubuntu runners

The following example demonstrates how to install an `apt` package as part of a job.

```yaml
name: Build on Ubuntu
on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Install jq tool
        run: |
          sudo apt-get update
          sudo apt-get install jq
```

> [!NOTE]
> Always run `sudo apt-get update` before installing a package. In case the `apt` index is stale, this command fetches and re-indexes any available packages, which helps prevent package installation failures.

## Installing software on macOS runners

The following example demonstrates how to install Brew packages and casks as part of a job.

```yaml
name: Build on macOS
on: push

jobs:
  build:
    runs-on: macos-latest
    steps:
      - name: Check out repository code
        uses: actions/checkout@v6
      - name: Install GitHub CLI
        run: |
          brew update
          brew install gh
      - name: Install Microsoft Edge
        run: |
          brew update
          brew install --cask microsoft-edge
```

## Installing software on Windows runners

The following example demonstrates how to use [Chocolatey](https://community.chocolatey.org/packages) to install the GitHub CLI as part of a job.

```yaml
name: Build on Windows
on: push
jobs:
  build:
    runs-on: windows-latest
    steps:
      - run: choco install gh
      - run: gh version
```
