---
title: Use GITHUB_TOKEN for authentication in workflows
description: Learn how to use the `GITHUB_TOKEN` to authenticate on behalf of GitHub Actions.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/tutorials/authenticate-with-github_token.md
captured: '2026-10-11'
section: Tutorials
---

# Use GITHUB_TOKEN for authentication in workflows

_Learn how to use the `GITHUB_TOKEN` to authenticate on behalf of GitHub Actions._

This tutorial leads you through how to use the `GITHUB_TOKEN` for authentication in GitHub Actions workflows, including examples for passing the token to actions, making API requests, and configuring permissions for secure automation.

For reference information, see [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions#permissions).

## Using the `GITHUB_TOKEN` in a workflow

You can use the `GITHUB_TOKEN` by using the standard syntax for referencing secrets: `${{ secrets.GITHUB_TOKEN }}`. Examples of using the `GITHUB_TOKEN` include passing the token as an input to an action, or using it to make an authenticated GitHub API request.

> [!IMPORTANT]
> An action can access the `GITHUB_TOKEN` through the `github.token` context even if the workflow does not explicitly pass the `GITHUB_TOKEN` to the action. As a good security practice, you should always make sure that actions only have the minimum access they require by limiting the permissions granted to the `GITHUB_TOKEN`. For more information, see [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions#permissions).

### Example 1: passing the `GITHUB_TOKEN` as an input

This example workflow uses the [GitHub CLI](../how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md), which requires the `GITHUB_TOKEN` as the value for the `GH_TOKEN` input parameter:

```yaml copy
name: Open new issue
on: workflow_dispatch

jobs:
  open-issue:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
    steps:
      - run: |
          gh issue --repo ${{ github.repository }} \
            create --title "Issue title" --body "Issue body"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Example 2: calling the REST API

You can use the `GITHUB_TOKEN` to make authenticated API calls. This example workflow creates an issue using the GitHub REST API:

```yaml
name: Create issue on commit

on: [ push ]

jobs:
  create_issue:
    runs-on: ubuntu-latest
    permissions:
      issues: write
    steps:
      - name: Create issue using REST API
        run: |
          curl --request POST \
          --url https://api.github.com

http(s)://HOSTNAME/api/v3/repos/${{ github.repository }}/issues \
          --header 'authorization: Bearer ${{ secrets.GITHUB_TOKEN }}' \
          --header 'content-type: application/json' \
          --data '{
            "title": "Automated issue for commit: ${{ github.sha }}",
            "body": "This issue was automatically created by the GitHub Action workflow **${{ github.workflow }}**. \n\n The commit hash was: _${{ github.sha }}_."
            }' \
          --fail
```

## Modifying the permissions for the `GITHUB_TOKEN`

Use the `permissions` key in your workflow file to modify permissions for the `GITHUB_TOKEN` for an entire workflow or for individual jobs. This allows you to configure the minimum required permissions for a workflow or job. As a good security practice, you should grant the `GITHUB_TOKEN` the least required access.

 To see the list of permissions available for use and their parameterized names, see [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions#permissions).

The two workflow examples earlier in this article show the `permissions` key being used at the job level.

## Granting additional permissions

If you need a token that requires permissions that aren't available in the `GITHUB_TOKEN`, create a GitHub App and generate an installation access token within your workflow. For more information, see [Making authenticated api requests with a github app in a github actions workflow](https://docs.github.com/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow). Alternatively, you can create a personal access token, store it as a secret in your repository, and use the token in your workflow with the `${{ secrets.SECRET_NAME }}` syntax. For more information, see [Managing your personal access tokens](https://docs.github.com/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) and [Using secrets in GitHub Actions](../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## Next steps

* [GITHUB_TOKEN](../concepts/security/github_token.md)
* [Workflow syntax for GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#permissions#permissions)
