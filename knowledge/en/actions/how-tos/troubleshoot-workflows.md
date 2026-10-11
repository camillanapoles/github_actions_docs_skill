---
title: Troubleshooting workflows
description: You can use the tools in GitHub Actions to debug your workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/troubleshoot-workflows.md
captured: '2026-10-11'
section: How tos
---

# Troubleshooting workflows

_You can use the tools in GitHub Actions to debug your workflows._

> [!NOTE]
> GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Initial troubleshooting suggestions

There are several ways you can troubleshoot failed workflow runs.

>[!NOTE] If you are on a GitHub Copilot Free subscription, this will count towards your monthly chat message limit.

### Using GitHub Copilot

To open a chat with GitHub Copilot about a failed workflow run, you can either:

* Next to the failed check in the merge box, click ****, then click ** Explain error**.
* In the merge box, click on the failed check. At the top of the workflow run summary page, click ** Explain error**.

This opens a chat window with GitHub Copilot, where it will provide instructions to resolve the issue.

### Using workflow run logs

Each workflow run generates activity logs that you can view, search, and download. For more information, see [Using workflow run logs](monitor-workflows/use-workflow-run-logs.md).

### Enabling debug logging

If the workflow logs do not provide enough detail to diagnose why a workflow, job, or step is not working as expected, you can enable additional debug logging. For more information, see [Enabling debug logging](monitor-workflows/enable-debug-logging.md).

If your workflow uses specific tools or actions, enabling their debug or verbose logging options can help generate more detailed output for troubleshooting.
For example, you can use `npm install --verbose` for npm or `GIT_TRACE=1 GIT_CURL_VERBOSE=1 git ...` for git.

## Reviewing billing errors

Actions usage includes runner minutes and storage for [workflow artifacts](../tutorials/store-and-share-data.md). For more information, see [Github actions](https://docs.github.com/billing/concepts/product-billing/github-actions).

### Setting a budget

Setting an Actions budget may help immediately unblock workflows failing due to billing or storage errors. It will allow further minutes and storage usage to be billed up to the set budget amount. To learn more, see [Set up budgets](https://docs.github.com/billing/how-tos/set-up-budgets).

## Reviewing GitHub Actions activity with metrics

To analyze the efficiency and reliability of your workflows using metrics, see [Viewing GitHub Actions metrics](administer/view-metrics.md).

## Troubleshooting workflow triggers

First, make sure that your workflow wasn't disabled manually, see [Disabling and enabling a workflow](manage-workflow-runs/disable-and-enable-workflows.md). A disabled workflow does not respond to its triggers.

You can review your workflow's `on:` field to understand what is expected to trigger the workflow. For more information, see [Triggering a workflow](write-workflows/choose-when-workflows-run/trigger-a-workflow.md).

For a full list of available events, see [Events that trigger workflows](../reference/workflows-and-actions/events-that-trigger-workflows.md).

### Triggering event conditions

Some triggering events only run from the default branch (i.e. `issues`, `schedule`). Workflow file versions that exist outside of the default branch will not trigger on these events.

Workflows will not run on `pull_request` activity if the pull request has a merge conflict.

Workflows that would otherwise be triggered on `push` or `pull_request` activity will be skipped if the commit message contains a skip annotation. For more information, see [Skipping workflow runs](manage-workflow-runs/skip-workflow-runs.md).

### Scheduled workflows running at unexpected times

Scheduled events can be delayed during periods of high loads of GitHub Actions workflow runs.

High load times include the start of every hour. If the load is sufficiently high enough, some queued jobs may be dropped. To decrease the chance of delay, schedule your workflow to run at a different time of the hour. For more information, see [Events that trigger workflows](../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule#schedule).

### Scheduled workflow stopped running

A scheduled (`cron`) workflow can stop running even though it is still enabled and manual or `workflow_dispatch` runs still work.

This can happen when the workflow's associated `actor` account is suspended, deleted, or deprovisioned. To restart it, a user with `write` access to the repository can commit a change to the `cron` schedule. See [Events that trigger workflows](../reference/workflows-and-actions/events-that-trigger-workflows.md#actor-for-scheduled-workflows#actor-for-scheduled-workflows).

### Filtering and diff limits

Specific events allow for filtering by branch, tag, and/or paths you can customize. Workflow run creation will be skipped if the filter conditions apply to filter out the workflow.

You can use special characters with filters. For more information, see [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet#filter-pattern-cheat-sheet).

For path filtering, evaluating diffs is limited to the first 3,000

300 files. If there are files changed that are not matched in the first 3,000

300 files returned by the filter, the workflow will not be run. For more information, see [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#git-diff-comparisons#git-diff-comparisons).

## Troubleshoot workflow execution

Workflow execution involves any issues seen after the workflow was triggered and a workflow run has been created.

### Debugging job conditions

If a job was skipped unexpectedly, or ran when you expected it to be skipped, you can view the expression evaluation to understand why:

1. Click on the job in the workflow run.
1. Download the log archive from the job's menu.
1. Open the `JOB-NAME/system.txt` file.
1. Look for the `Evaluating`, `Expanded`, and `Result` lines.

The `Expanded` line shows the actual runtime values that were substituted into your `if` condition, making it clear why the expression evaluated to `true` or `false`.

For more information, see [Viewing job condition expression logs](monitor-workflows/view-job-condition-logs.md).

### Canceling Workflows

If standard cancellation through the [UI](../reference/workflows-and-actions/workflow-cancellation.md) or [API](https://docs.github.com/rest/actions/workflow-runs#cancel-a-workflow-run) does not process as expected, there may be a conditional statement configured for your running workflow job(s) that causes it to not cancel.

In these cases, you can leverage the API to force cancel the run. For more information, see [Workflow runs](https://docs.github.com/rest/actions/workflow-runs#force-cancel-a-workflow-run#force-cancel-a-workflow-run).

A common cause can be using the `always()` [status check function](../reference/workflows-and-actions/expressions.md#status-check-functions) which returns `true`, even on cancellation. An alternative is to use the inverse of the `cancelled()` function, `${{ !cancelled() }}`.

For more information, see [Using conditions to control job execution](write-workflows/choose-when-workflows-run/control-jobs-with-conditions.md) and [Canceling a workflow run](manage-workflow-runs/cancel-a-workflow-run.md).

## Troubleshooting runners

### Defining runner labels

GitHub-hosted runners leverage [preset labels](../reference/runners/github-hosted-runners.md#standard-github-hosted-runners-for-public-repositories) maintained through the [`actions/runner-images`](https://github.com/actions/runner-images?tab=readme-ov-file#available-images) repository.

We recommend using unique label names for larger and self-hosted runners. If a label matches to any of the existing preset labels, there can be runner assignment issues where there is no guarantee on which matching runner option the job will run on.

### Self-hosted runners

If you use self-hosted runners, you can view their activity and diagnose common issues.

For more information, see [Monitoring and troubleshooting self-hosted runners](manage-runners/self-hosted-runners/monitor-and-troubleshoot.md).

### Runner IP addresses flagged by security scanners

GitHub-hosted runners use dynamically assigned IP addresses from shared infrastructure. These IP addresses are published via the Meta API (for example, the `actions` and `actions_macos` keys). For more information, see [Meta](https://docs.github.com/rest/meta/meta#get-github-meta-information#get-github-meta-information).

Third-party threat intelligence services, IP reputation scanners, or firewall vendors may flag these IP addresses as "malicious" or "suspicious." Because the underlying infrastructure is shared, activity from other users of the same infrastructure can influence the reputation scores assigned to these addresses.

GitHub does not control third-party IP reputation lists and cannot comment on their accuracy or update frequency. To verify whether an IP address belongs to GitHub-hosted runners, check the IP ranges returned by the Meta API.

If you have a security concern about a Microsoft-owned IP address, report it to the [Microsoft Security Response Center (MSRC)](https://msrc.microsoft.com/report/).

## Networking troubleshooting suggestions

Our support is limited for network issues that involve:

* Your networks
* External networks
* Third-party systems
* General internet connectivity

To view GitHub's realtime platform status, check [GitHub Status](https://githubstatus.com/).

For other network-related issues, review your organization's network settings and verify the status of any third-party services you're accessing. If problems persist, consider reaching out to your network administrators for further assistance.

If you're unsure about the issue, contact GitHub Support. For details on how to contact support, see [Contacting github support](https://docs.github.com/support/contacting-github-support).

### DNS

Issues may occur from Domain Name System (DNS) configuration, resolution, or resolver problems. We recommend you review available logs, vendor documentation, or consult with your administrators for additional assistance.

### Firewalls

Activities may become blocked by firewalls. If this occurs, you may want to review available logs, vendor documentation, or consult with your administrators for additional assistance.

### Proxies

Activities could fail when using a proxy for communications. It's good practice to review available logs, vendor documentation, or consult with your administrators for additional assistance.

Refer to [Using proxy servers with a runner](manage-runners/use-proxy-servers.md) for information about configuring the runner application to utilize a proxy.

### Subnets

It is possible to encounter issues with subnets in use or overlaps with an existing network, such as within virtual cloud provider or Docker networks. In such cases, we recommend you review your network topology and subnets in use.

### Certificates

Issues may occur from self-signed or custom certificate chains and certificate stores. You can check that a certificate in use has not expired and is currently trusted. Certificates may be inspected with `curl` or similar tools. You can also review available logs, vendor documentation, or consult with your administrators for additional assistance.

### IP lists

IP allow or deny lists may disrupt expected communications. If there is a problem, you should review available logs, vendor documentation, or consult with your administrators for additional assistance.

If your GitHub account is configured with an IP allowlist, workflows will fail if a runner uses an IP address that isn’t included in the allowlist. To resolve this, verify that the runner's IP addresses are added to your organization's or enterprise's allowlist. For more details, see [Managing allowed ip addresses for your organization](https://docs.github.com/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization) and/or [Restricting network traffic to your enterprise with an ip allow list](https://docs.github.com/admin/configuring-settings/hardening-security-for-your-enterprise/restricting-network-traffic-to-your-enterprise-with-an-ip-allow-list).

For information on GitHub's IP addresses, such as those used by GitHub-hosted runners, see [About githubs ip addresses](https://docs.github.com/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses).

Static IP addresses are available for use with GitHub-hosted larger runners. See [Managing larger runners](manage-runners/larger-runners/manage-larger-runners.md) for more information.

### Operating systems and software applications

In addition to firewalls or proxies, customizations performed to GitHub-hosted runners, such as installing additional software packages, may result in communication disruptions. For information about available customization options, see [Customizing GitHub-hosted runners](manage-runners/github-hosted-runners/customize-runners.md).

* For self-hosted runners, learn more about necessary endpoints in [Self-hosted runners reference](../reference/runners/self-hosted-runners.md).

* For help configuring WireGuard, see [Using WireGuard to create a network overlay](manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard.md).

* For details about configuring OpenID Connect (OIDC), see [Using an API gateway with OIDC](manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md).
### Azure private networking for GitHub-hosted runners

Issues may arise from the use of GitHub-hosted runners within your configured Azure Virtual Networks (VNETs) settings.

For troubleshooting advice, see [Troubleshooting azure private network configurations for github hosted runners in your organization](https://docs.github.com/organizations/managing-organization-settings/troubleshooting-azure-private-network-configurations-for-github-hosted-runners-in-your-organization) or [Troubleshooting azure private network configurations for github hosted runners in your enterprise](https://docs.github.com/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/troubleshooting-azure-private-network-configurations-for-github-hosted-runners-in-your-enterprise)

[Troubleshooting azure private network configurations for github hosted runners in your enterprise](https://docs.github.com/enterprise-cloud@latest/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/troubleshooting-azure-private-network-configurations-for-github-hosted-runners-in-your-enterprise) in the GitHub Enterprise Cloud docs.
