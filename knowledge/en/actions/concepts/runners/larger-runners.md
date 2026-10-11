---
title: Larger runners
description: Organize and govern your workflows with GitHub-hosted larger runners using runner groups, concurrency policies, and granular access controls.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/runners/larger-runners.md
captured: '2026-10-11'
section: Concepts / Runners
---

# Larger runners

_Organize and govern your workflows with GitHub-hosted larger runners using runner groups, concurrency policies, and granular access controls._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

To learn about larger runners, see [the GitHub Enterprise Cloud documentation](https://docs.github.com/enterprise-cloud@latest/actions/concepts/runners/larger-runners).

## About larger runners

Larger runners are managed virtual machines with more resources than [standard GitHub-hosted runners](../../reference/runners/github-hosted-runners.md#supported-runners-and-hardware-resources). They offer the following advanced features:

* More RAM, CPU, and disk space
* Static IP addresses
* Azure private networking
* The ability to group runners
* Autoscaling to support concurrent workflows
* GPU-powered runners

These larger runners are hosted by GitHub and have the runner application and other tools preinstalled.

## What you can do with larger runners

All larger runners support the following capabilities:

* **Runner groups**: Organize runners and control which repositories can use them
* **Autoscaling**: Scale runners up or down based on workload demand
* **Concurrency controls**: Limit how many jobs can run at the same time

The following capabilities are available only on Linux and Windows runners:

* **Static IP addresses**: Assign static IP addresses from a specific range to runners, allowing you to configure firewall allowlists.
* **Custom images**: Use custom runner images to pre-install dependencies and reduce setup time.
* **Azure private networking**: Connect your runners to Azure private networks.

## About larger runners for code scanning default setup

Consider configuring larger runners for code scanning default setup if:

* Your scans with standard GitHub-hosted runners are taking too long.
* Your scans with standard GitHub-hosted runners are returning memory or disk errors.
* You want to customize aspects of your code scanning runner, such as the runner size, runner image, and job concurrency, without using self-hosted runners.

For more information on configuring larger runners for code scanning default setup, see [Configure larger runners](https://docs.github.com/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/configure-larger-runners).

## Billing

> [!NOTE]
> Larger runners are not eligible for the use of included minutes on private repositories. For both private and public repositories, when larger runners are in use, they will always be billed at the per-minute rate.

Compared to standard GitHub-hosted runners, larger runners are billed differently. Larger runners are only billed at the per-minute rate for the amount of time workflows are executed on them. There is no cost associated with creating a larger runner that is not being used by a workflow. For more information, see [Actions runner pricing](https://docs.github.com/billing/reference/actions-runner-pricing).

## Next steps

To start using larger runners, see [Managing larger runners](../../how-tos/manage-runners/larger-runners/manage-larger-runners.md).

To find reference information about using larger runners, see [Larger runners reference](../../reference/runners/larger-runners.md).
