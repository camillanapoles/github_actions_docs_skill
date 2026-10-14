---
title: Self-hosted runners
description: You can host your own runners and customize the environment used to run jobs in your GitHub Actions workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/runners/self-hosted-runners.md
captured: '2026-10-11'
section: Concepts / Runners
---

# Self-hosted runners

_You can host your own runners and customize the environment used to run jobs in your GitHub Actions workflows._

A self-hosted runner is a system that you deploy and manage to execute jobs from GitHub Actions on GitHub.

Self-hosted runners:

* Give you more control of hardware, operating system, and software tools than GitHub-hosted runners provide. Be aware that you are responsible for updating the operating system and all other software.
* Allow you to use machines and services that your company already maintains and pays to use.
* Are free to use with GitHub Actions, but you are responsible for the cost of maintaining your runner machines.
* Let you create custom hardware configurations that meet your needs with processing power or memory to run larger jobs, install software available on your local network.
* Receive automatic updates for the self-hosted runner application only, though you may disable automatic updates of the runner.
* Don't need to have a clean instance for every job execution.
* Can be organized into groups to restrict access to specific workflows, organizations, and repositories. See [Managing access to self-hosted runners using groups](../../how-tos/manage-runners/self-hosted-runners/manage-access.md).
* Can be physical, virtual, in a container, on-premises, or in a cloud.

You can use self-hosted runners anywhere in the management hierarchy. Repository-level runners are dedicated to a single repository, while organization-level runners can process jobs for multiple repositories in an organization. Organization owners can choose which repositories are allowed to create repository-level self-hosted runners. See [Disabling or limiting github actions for your organization](https://docs.github.com/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners#limiting-the-use-of-self-hosted-runners). Finally, enterprise-level runners can be assigned to multiple organizations in an enterprise account.

## Next steps

To set up a self-hosted runner in your workspace, see [Adding self-hosted runners](../../how-tos/manage-runners/self-hosted-runners/add-runners.md).

To find information about the requirements and supported software and hardware for self-hosted runners, see [Self-hosted runners reference](../../reference/runners/self-hosted-runners.md).
