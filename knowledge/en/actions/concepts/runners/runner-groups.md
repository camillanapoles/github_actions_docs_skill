---
title: Runner groups
description: Use runner groups to control access to runners and organize runners across your organization or enterprise.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/runners/runner-groups.md
captured: '2026-10-11'
section: Concepts / Runners
---

# Runner groups

_Use runner groups to control access to runners and organize runners across your organization or enterprise._

## About runner groups

To control access to runners at the organizationand/or enterprise levels, enterprise and organization owners can use runner groups.

level, organizations using the GitHub Team plan can use runner groups. Runner groups are used to collect sets of runners and create a security boundary around them.

When you grant access to a runner group, you can see the runner group listed in the organization's runner settings. Optionally, you can assign additional granular repositoryand workflow access policies to the runner group.

When new runners are created, they are automatically assigned to the default group unless otherwise specified. Runners can only be in one group at a time. You can move runners from one runner group to another.

Runner groups help you enforce consistent access policies for runners across your infrastructure.

With runner groups, you can:

* Organize larger runners and self-hosted runners
* Restrict which organizations and repositories can use specific runners
* Route jobs to a specific runner group in your workflow file
* Set concurrency limits to control costs and capacity

You can also disable standard GitHub-hosted runners, to require Linux, Windows, and macOS jobs to run through runner groups instead of standard runner labels. For organization-level settings, see [Disabling or limiting github actions for your organization](https://docs.github.com/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization). If you're an enterprise owner, see [Enforcing policies for github actions in your enterprise](https://docs.github.com/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise).

## Next steps

To learn how to use runner groups to control access to larger runners, see [Controlling access to larger runners](../../how-tos/manage-runners/larger-runners/control-access.md).

For information on how to route jobs to runners in a specific group, see [Choosing the runner for a job](../../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#choosing-runners-in-a-group#choosing-runners-in-a-group).
