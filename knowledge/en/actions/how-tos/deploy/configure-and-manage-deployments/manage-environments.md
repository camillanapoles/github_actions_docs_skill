---
title: Managing environments for deployment
description: You can create environments and secure those environments with deployment protection rules. A job that references an environment must follow any protection rules for the environment before running or accessing the environment's secrets.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments.md
captured: '2026-10-11'
section: How tos / Deploy / Configure and manage deployments
---

# Managing environments for deployment

_You can create environments and secure those environments with deployment protection rules. A job that references an environment must follow any protection rules for the environment before running or accessing the environment's secrets._

## Prerequisites

!!! note
    Users with GitHub Free plans can only configure environments for public repositories. If you convert a repository from public to private, any configured protection rules or environment secrets will be ignored, and you will not be able to configure any environments. If you convert your repository back to public, you will have access to any previously configured protection rules and environment secrets.

    Organizations with GitHub Team and users with GitHub Pro can configure environments for private repositories. For more information, see [Githubs plans](https://docs.github.com/get-started/learning-about-github/githubs-plans).

* For general information about environments, see [Deploying with GitHub Actions](control-deployments.md#using-environments#using-environments).
* For information about available rules, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md).

## Creating an environment

To configure an environment in a personal account repository, you must be the repository owner. To configure an environment in an organization repository, you must have `admin` access.

!!! note
    * Creation of an environment in a private repository is available to organizations with GitHub Team and users with GitHub Pro.
    * Some features for environments have no or limited availability for private repositories. If you are unable to access a feature described in the instructions below, please see the documentation linked in the related step for availability information.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Settings**. If you cannot see the "Settings" tab, select the **** dropdown menu, then click **Settings**.

   ![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/images/help/repository/repo-actions-settings.png)
1. In the left sidebar, click **Environments**.
1. Click **New environment**.
1. Enter a name for the environment, then click **Configure environment**. Environment names are not case sensitive. An environment name may not exceed 255 characters and must be unique within the repository.
1. Optionally, specify people or teams that must approve workflow jobs that use this environment. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#required-reviewers#required-reviewers).
   1. Select **Required reviewers**.
   1. Enter up to 6 people or teams. Only one of the required reviewers needs to approve the job for it to proceed.
   1. Optionally, to prevent users from approving workflows runs that they triggered, select **Prevent self-review**.
   1. Click **Save protection rules**.
1. Optionally, specify the amount of time to wait before allowing workflow jobs that use this environment to proceed. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#wait-timer#wait-timer).
   1. Select **Wait timer**.
   1. Enter the number of minutes to wait.
   1. Click **Save protection rules**.
1. Optionally, disallow bypassing configured protection rules. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#allow-administrators-to-bypass-configured-protection-rules#allow-administrators-to-bypass-configured-protection-rules).
   1. Deselect **Allow administrators to bypass configured protection rules**.
   1. Click **Save protection rules**.
1. Optionally, enable any custom deployment protection rules that have been created with GitHub Apps. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#custom-deployment-protection-rules#custom-deployment-protection-rules).
   1. Select the custom protection rule you want to enable.
   1. Click **Save protection rules**.
1. Optionally, specify what branches and tags can deploy to this environment. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#deployment-branches-and-tags#deployment-branches-and-tags).
   1. Select the desired option in the **Deployment branches** dropdown.
   1. If you chose **Selected branches and tags**, to add a new rule, click **Add deployment branch or tag rule**
   1. In the "Ref type" dropdown menu, depending on what rule you want to apply, click ** Branch** or ** Tag**.
   1. Enter the name pattern for the branch or tag that you want to allow.

!!! note
    Name patterns must be configured for branches or tags individually.

   1. Click **Add rule**.
1. Optionally, add environment secrets. These secrets are only available to workflow jobs that use the environment. Additionally, workflow jobs that use this environment can only access these secrets after any configured rules (for example, required reviewers) pass. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#environment-secrets#environment-secrets).
   1. Under **Environment secrets**, click **Add Secret**.
   1. Enter the secret name.
   1. Enter the secret value.
   1. Click **Add secret**.
1. Optionally, add environment variables. These variables are only available to workflow jobs that use the environment, and are only accessible using the [`vars`](../../../reference/workflows-and-actions/contexts.md#vars-context) context. For more information, see [Deployments and environments](../../../reference/workflows-and-actions/deployments-and-environments.md#environment-variables#environment-variables).
   1. Under **Environment variables**, click **Add Variable**.
   1. Enter the variable name.
   1. Enter the variable value.
   1. Click **Add variable**.

You can also create and configure environments through the REST API. For more information, see [Environments](https://docs.github.com/rest/deployments/environments), [Secrets](https://docs.github.com/rest/actions/secrets), [Variables](https://docs.github.com/rest/actions/variables), and [Branch policies](https://docs.github.com/rest/deployments/branch-policies).

Running a workflow that references an environment that does not exist will create an environment with the referenced name. If the environment is created from running implicit page builds (for example, from a branch or folder source), the source branch will be added as a protection rule to the environment. Otherwise, the newly created environment will not have any protection rules or secrets configured. Anyone that can edit workflows in the repository can create environments via a workflow file, but only repository admins can configure the environment.

## Deleting an environment

To configure an environment in a personal account repository, you must be the repository owner. To configure an environment in an organization repository, you must have `admin` access.

Deleting an environment will delete all secrets and protection rules associated with the environment. Any jobs currently waiting because of protection rules from the deleted environment will automatically fail.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Settings**. If you cannot see the "Settings" tab, select the **** dropdown menu, then click **Settings**.

   ![Screenshot of a repository header showing the tabs. The "Settings" tab is highlighted by a dark orange outline.](https://docs.github.com/assets/images/help/repository/repo-actions-settings.png)
1. In the left sidebar, click **Environments**.
1. Next to the environment that you want to delete, click .
1. Click **I understand, delete this environment**.

You can also delete environments through the REST API. For more information, see [Repos](https://docs.github.com/rest/repos#environments#environments).

## How environments relate to deployments

When a workflow job that references an environment runs, it creates a deployment object with the `environment` property set to the name of your environment. As the workflow progresses, it also creates deployment status objects with the `environment` property set to the name of your environment, the `environment_url` property set to the URL for environment (if specified in the workflow), and the `state` property set to the status of the job.

You can access these objects through the REST API or GraphQL API. You can also subscribe to these webhook events. For more information, see [Repos](https://docs.github.com/rest/repos#deployments#deployments), [Deployments](https://docs.github.com/graphql/reference/deployments#object-deployment#object-deployment) (GraphQL API), or [Webhook events and payloads](https://docs.github.com/webhooks/webhook-events-and-payloads#deployment#deployment).

## Next steps

GitHub Actions provides several features for managing your deployments. For more information, see [Deploying with GitHub Actions](control-deployments.md).
