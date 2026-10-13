---
title: Managing access to self-hosted runners using groups
description: You can use policies to limit access to self-hosted runners that have been added to an organization or enterprise.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/self-hosted-runners/manage-access.md
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Managing access to self-hosted runners using groups

_You can use policies to limit access to self-hosted runners that have been added to an organization or enterprise._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Creating a self-hosted runner group for an organization

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

!!! note
    When creating a runner group, you must choose a policy that defines which repositories and workflows have access to the runner group. To change which repositories and workflows can access the runner group, organization owners and users with the “Manage organization runners and runner groups” permission can set a policy for the organization. For more information, see [Managing access to self-hosted runners using groups](manage-access.md#changing-which-repositories-can-access-a-runner-group#changing-which-repositories-can-access-a-runner-group).

All organizations have a single default runner group. Organization owners and users with the "Manage organization runners and runner groups" permission can create additional organization-level runner groups. For more information about custom organization roles, see [Permissions of custom organization roles](https://docs.github.com/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles).

If no group is specified during the registration process, runners are automatically added to the default group. You can later move the runner from the default group to a custom group.

For information about how to create a runner group with the REST API, see [Actions](https://docs.github.com/rest/actions#self-hosted-runner-groups#self-hosted-runner-groups).

1. On GitHub, navigate to the main page of the organization.
1. Under your organization name, click ** Settings**. If you cannot see the "Settings" tab, select the **** dropdown menu, then click **Settings**.

   ![Screenshot of the tabs in an organization's profile. The "Settings" tab is outlined in dark orange.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)
1. In the left sidebar, click ** Actions**, then click **Runner groups**.
1. In the "Runner groups" section, click **New runner group**.
1. Enter a name for your runner group.
1. Assign a policy for repository access.

    You can configure a runner group to be accessible to a specific list of repositories, or to all repositories in the organization. By default, only private repositories can access runners in a runner group, but you can override this. This setting can't be overridden if configuring an organization's runner group that was shared by an enterprise.

1. Assign a policy for workflow access.

   You can configure a runner group to be accessible to a specific list of workflows, or to all workflows. This setting can't be overridden if you are configuring an organization's runner group that was shared by an enterprise. If you specify what workflows can access the runner group, use the full path to the workflow, including the repository name and owner. Pin non-reusable workflows to a branch. Pin reusable workflows to a branch, tag, or full SHA. For example: `octo-org/octo-repo/.github/workflows/build.yml@refs/tags/v2, octo-org/octo-repo/.github/workflows/deploy.yml@d6dc6c96df4f32fa27b039f2084f576ed2c5c2a5, monalisa/octo-test/.github/workflows/test.yml@refs/heads/main`.

   It is best practice to fully qualify ambiguous refs. For example, instead of providing `main` as a ref, provide `refs/heads/main`.

   Only jobs directly defined within the selected workflows will have access to the runner group. Organization-owned runner groups cannot access workflows from a different organization in the enterprise; instead, you must create an enterprise-owned runner group.
1. Click **Create group** to create the group and apply the policy.

## Creating a self-hosted runner group for an enterprise

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

Enterprises can add their runners to groups for access management. Enterprises can create groups of runners that are accessible to specific organizations in the enterprise account or to specific workflows. Organization owners can then assign additional granular repository or workflow access policies to the enterprise runner groups. For information about how to create a runner group with the REST API, see the enterprise endpoints in the [GitHub Actions REST API](https://docs.github.com/rest/actions#self-hosted-runner-groups).

If no group is specified during the registration process, runners are automatically added to a default group. You can later move the runner from the default group to a custom group.

When creating a group, you must choose a policy that defines which organizations have access to the runner group.

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runner groups** tab.
1. Click **New runner group**.
1. Under "Group name", type a name for your runner group.
1. To choose a policy for organization access, select the **Organization access** dropdown menu and click a policy. You can configure a runner group to be accessible to a specific list of organizations, or all organizations in the enterprise. By default, only private repositories can access runners in a runner group, but you can override this.

1. Assign a policy for workflow access.

   You can configure a runner group to be accessible to a specific list of workflows, or to all workflows. This setting can't be overridden if you are configuring an organization's runner group that was shared by an enterprise. If you specify what workflows can access the runner group, use the full path to the workflow, including the repository name and owner. Pin non-reusable workflows to a branch. Pin reusable workflows to a branch, tag, or full SHA. For example: `octo-org/octo-repo/.github/workflows/build.yml@refs/tags/v2, octo-org/octo-repo/.github/workflows/deploy.yml@d6dc6c96df4f32fa27b039f2084f576ed2c5c2a5, monalisa/octo-test/.github/workflows/test.yml@refs/heads/main`.

   It is best practice to fully qualify ambiguous refs. For example, instead of providing `main` as a ref, provide `refs/heads/main`.

   Only jobs directly defined within the selected workflows will have access to the runner group.
1. Click **Save group** to create the group and apply the policy.

## Changing which organizations can access a runner group

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).

For runner groups in an enterprise, you can change what organizations in the enterprise can access a runner group.

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runner groups** tab.

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

1. Under "Organization access," use the dropdown menu to click **Selected organizations**.
   1. To the right of the dropdown menu, click .
   1. In the popup, use the checkboxes to select organizations that can use this runner group.
1. Click **Save group**.

## Changing which repositories can access a runner group

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).

For runner groups in an organization, you can change what repositories in the organization can access a runner group.

1. Navigate to the main page of the organization where your runner groups are located.
1. Click ** Settings**.
1. In the left sidebar, click ** Actions**, then click **Runner groups**.

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

1. In the list of groups, click the runner group you'd like to configure.
1. Under "Repository access," use the dropdown menu to click **Selected repositories**.
   1. To the right of the dropdown menu, click .
   1. In the popup, use the checkboxes to select repositories that can access this runner group.
1. Click **Save group**.

## Changing which workflows can access a runner group

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).

You can configure a runner group to run either selected workflows or all workflows. For example, you might use this setting to protect secrets that are stored on runners or to standardize deployment workflows by restricting a runner group to run only a specific reusable workflow. This setting cannot be overridden if you are configuring an organization's runner group that was shared by an enterprise.

* [Changing which workflows can access an organization runner group](#changing-which-workflows-can-access-an-organization-runner-group)
* [Changing which workflows can access an enterprise runner group](#changing-which-workflows-can-access-an-enterprise-runner-group)

### Changing which workflows can access an organization runner group

1. Navigate to the main page of the organization where your runner groups are located.
1. Click ** Settings**.
1. In the left sidebar, click ** Actions**, then click **Runner groups**.

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

1. In the list of groups, click the runner group you'd like to configure.
1. Under **Workflow access**, select the dropdown menu and click **Selected workflows**.
1. Click .
1. Enter a comma separated list of the workflows that can access the runner group. Use the full path, including the repository name and owner. Pin non-reusable workflows to a branch. Pin reusable workflows to a branch, tag, or full SHA. For example: `octo-org/octo-repo/.github/workflows/build.yml@v2, octo-org/octo-repo/.github/workflows/deploy.yml@d6dc6c96df4f32fa27b039f2084f576ed2c5c2a5, monalisa/octo-test/.github/workflows/test.yml@main`.

   Only jobs directly defined within the selected workflows will have access to the runner group.

   Organization-owned runner groups cannot access workflows from a different organization in the enterprise; instead, you must create an enterprise-owned runner group.

1. Click **Save**.

### Changing which workflows can access an enterprise runner group

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runner groups** tab.

Always include a security admonition above this procedure. This is either one of the following, depending on whether the context is self-hosted runners or larger runners.

!!! warning
    We recommend that you only use self-hosted runners with private repositories. This is because forks of your public repository can potentially run dangerous code on your self-hosted runner machine by creating a pull request that executes the code in a workflow.

    For more information, see [Secure use reference](../../../reference/security/secure-use.md).
    [!WARNING]
    If you are using a Fixed IP range, we recommend that you only use larger runners with private repositories. Forks of your repository can potentially run dangerous code on your larger runner by creating a pull request that executes the code in a workflow.

1. In the list of groups, click the runner group you'd like to configure.
1. Under **Workflow access**, select the dropdown menu and click **Selected workflows**.
1. Click .
1. Enter a comma separated list of the workflows that can access the runner group. Use the full path, including the repository name and owner. Pin non-reusable workflows to a branch. Pin reusable workflows to a branch, tag, or full SHA. For example: `octo-org/octo-repo/.github/workflows/build.yml@v2, octo-org/octo-repo/.github/workflows/deploy.yml@d6dc6c96df4f32fa27b039f2084f576ed2c5c2a5, monalisa/octo-test/.github/workflows/test.yml@main`.

   Only jobs directly defined within the selected workflows will have access to the runner group.

   Organization-owned runner groups cannot access workflows from a different organization in the enterprise; instead, you must create an enterprise-owned runner group.

1. Click **Save**.

## Changing the name of a runner group

You can edit the name of your runner groups at the enterprise and organization levels.

* [Changing the name of an organization runner group](#changing-the-name-of-an-organization-runner-group)
* [Changing the name of an enterprise runner group](#changing-the-name-of-an-enterprise-runner-group)

### Changing the name of an organization runner group

1. Navigate to the main page of the organization where your runner groups are located.
1. Click ** Settings**.
1. In the left sidebar, click ** Actions**, then click **Runner groups**.
1. In the list of groups, click the runner group you'd like to configure.
1. Enter the new runner group name in the text field under "Group name."
1. Click **Save**.

### Changing the name of an enterprise runner group

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runner groups** tab.
1. In the list of groups, click the runner group you'd like to configure.
1. Enter the new runner group name in the text field under "Group name."
1. Click **Save**.

## Automatically adding a self-hosted runner to a group

You can use the configuration script to automatically add a new runner to a group. For example, this command registers a new runner and uses the `--runnergroup` parameter to add it to a group named `rg-runnergroup`.

```shell
./config.sh --url $org_or_enterprise_url --token $token --runnergroup rg-runnergroup
```

The command will fail if the runner group doesn't exist:

```shell
Could not find any self-hosted runner group named "rg-runnergroup".
```

## Moving a self-hosted runner to a group

If you don't specify a runner group during the registration process, your new runners are automatically assigned to the default group, and can then be moved to another group.

* [Moving an organization runner to a group](#moving-an-organization-runner-to-a-group)
* [Moving an enterprise runner to a group](#moving-an-enterprise-runner-to-a-group)

### Moving an organization runner to a group

1. On GitHub, navigate to the main page of the organization.
1. Under your organization name, click ** Settings**. If you cannot see the "Settings" tab, select the **** dropdown menu, then click **Settings**.

   ![Screenshot of the tabs in an organization's profile. The "Settings" tab is outlined in dark orange.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)
1. In the left sidebar, click ** Actions**, then click **Runners**.
1. In the "Runners" list, click the runner that you want to configure.
1. Select the **Runner group** drop-down.
1. In "Move runner to group", choose a destination group for the runner.

### Moving an enterprise runner to a group

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runners** tab.
1. In the "Runners" list, click the runner that you want to configure.
1. Select the **Runner group** drop-down.
1. In "Move runner to group", choose a destination group for the runner.

## Removing a self-hosted runner group

In order to remove a runner group, you must first move or remove all of the runners from the group.

* [Removing a runner group from an organization](#removing-a-runner-group-from-an-organization)
* [Removing a runner group from an enterprise](#removing-a-runner-group-from-an-enterprise)

### Removing a runner group from an organization

1. Navigate to the main page of the organization where your runner groups are located.
1. Click ** Settings**.
1. In the left sidebar, click ** Actions**, then click **Runner groups**.
1. In the list of groups, to the right of the group you want to delete, click .
1. To remove the group, click **Remove group**.
1. Review the confirmation prompts, and click **Remove this runner group**.

### Removing a runner group from an enterprise

1. Navigate to your enterprise. For example, from the [Enterprises](https://github.com/settings/enterprises?ref_product=ghec&ref_type=engagement&ref_style=text) page on GitHub.com.

1. At the top of the page, click ** Policies**.
1. Under " Policies", click **Actions**.
1. Click the **Runner groups** tab.
1. In the list of groups, to the right of the group you want to delete, click .
1. To remove the group, click **Remove group**.
1. Review the confirmation prompts, and click **Remove this runner group**.

## Using unique names for runner groups

GitHub Actions requires that runner group names must be unique at the organization level. This means that an organization will no longer be able to create a runner group with the same name as one in the enterprise. In addition, users will see a warning banner on any runner groups that share the same name as a group in the enterprise, suggesting that the organization group should be renamed.

To avoid ambiguity, a workflow will fail if there are duplicate runner groups in the organization and enterprise. To address this, you can either rename one of your runner groups in the organization or enterprise, or you can update your workflow file to add a prefix to the runner group name:

* `org/` or `organization/`
* `ent/` or `enterprise/`

### Example: Using prefixes to differentiate runner groups

For example, if you have a runner group named `my-group` in the organization and another named `my-group` in the enterprise, you can update your workflow file to use `org/my-group` or `ent/my-group` to differentiate between the two.

Using `org/`:

```yaml
runs-on:
  group: org/my-group
  labels: [ self-hosted, label-1 ]
```

Using `ent/`:

```yaml
runs-on:
  group: ent/my-group
  labels: [ self-hosted, label-1 ]
```
