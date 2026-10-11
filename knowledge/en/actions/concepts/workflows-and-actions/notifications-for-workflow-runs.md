---
title: Notifications for workflow runs
description: You can subscribe to notifications about workflow runs that you trigger.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/workflows-and-actions/notifications-for-workflow-runs.md
captured: '2026-10-11'
section: Concepts / Workflows and actions
---

# Notifications for workflow runs

_You can subscribe to notifications about workflow runs that you trigger._

If you enable email or web notifications for GitHub Actions, you'll receive a notification when any workflow runs that you've triggered have completed. The notification will include the workflow run's status (including successful, failed, neutral, and canceled runs). You can also choose to receive a notification only when a workflow run has failed. For more information about enabling or disabling notifications, see [About notifications](https://docs.github.com/subscriptions-and-notifications/concepts/about-notifications).

Notifications for scheduled workflows are sent to the user who initially created the workflow.
 * If a different user updates the cron syntax, in the `schedule` event in the workflow file, subsequent notifications will be sent to that user instead.
 * If a scheduled workflow is disabled and then re-enabled, notifications will be sent to the user who re-enabled the workflow rather than the user who last modified the cron syntax.

You can also see the status of workflow runs on a repository's Actions tab. For more information, see [Manage workflow runs](../../how-tos/manage-workflow-runs.md).
