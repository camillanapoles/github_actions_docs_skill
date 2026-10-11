---
title: Sharing actions and workflows with your organization
description: You can share an action or reusable workflow with your organization without publishing the action or workflow publicly.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/reuse-automations/share-with-your-organization.md
captured: '2026-10-11'
section: How tos / Reuse automations
---

# Sharing actions and workflows with your organization

_You can share an action or reusable workflow with your organization without publishing the action or workflow publicly._

> [!WARNING]
> * If you make a private repository accessible to GitHub Actions workflows in other repositories, outside collaborators on the other repositories can indirectly access the private repository, even though they do not have direct access to these repositories. The outside collaborators can view logs for workflow runs when actions or workflows from the private repository are used.
> * To allow runners to download these actions, GitHub passes a scoped installation token to the runner. This token has read access to the repository, and automatically expires after one hour.

## Sharing actions and workflows with your organization

1. Store the action or reusable workflow in a private repository. For more information, see [About repositories](https://docs.github.com/repositories/creating-and-managing-repositories/about-repositories#about-repository-visibility#about-repository-visibility).
1. On GitHub, navigate to the main page of the private repository.
1. Under your repository name, click ** Settings**.
This reusable is only to be used in other repo/org/enterprise setting reusables.
1. In the left sidebar, click ** Actions**, then click **General**.
1. To grant access to other private repositories in the organization, in the **Access** section at the bottom of the page, select **Accessible from repositories in the 'ORGANIZATION-NAME' organization**.
1. Click **Save** to apply the settings.

## Next steps

To learn how to reuse your shared workflows, see [Reuse workflows](reuse-workflows.md).
