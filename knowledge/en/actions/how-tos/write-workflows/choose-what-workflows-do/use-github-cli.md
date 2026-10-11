---
title: Using GitHub CLI in workflows
description: You can script with GitHub CLI in GitHub Actions workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md
captured: '2026-10-11'
section: How tos / Write workflows / Choose what workflows do
---

# Using GitHub CLI in workflows

_You can script with GitHub CLI in GitHub Actions workflows._

!!! note
    To learn more about GitHub CLI, see [About github cli](https://docs.github.com/github-cli/github-cli/about-github-cli).

GitHub CLI is preinstalled on all GitHub-hosted runners. For each step that uses GitHub CLI, you must set an environment variable called `GH_TOKEN` to a token with the required scopes.

You can execute any GitHub CLI command. For example, this workflow uses the `gh issue comment` subcommand to add a comment when an issue is opened.

```yaml copy
name: Comment when opened
on:
  issues:
    types:
      - opened
jobs:
  comment:
    runs-on: ubuntu-latest
    steps:
      - run: gh issue comment $ISSUE --body "Thank you for opening this issue!"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE: ${{ github.event.issue.html_url }}
```

You can also execute API calls through GitHub CLI. For example, this workflow first uses the `gh api` subcommand to query the GraphQL API and parse the result. Then it stores the result in an environment variable that it can access in a later step. In the second step, it uses the `gh issue create` subcommand to create an issue containing the information from the first step.

```yaml copy
name: Report remaining open issues
on:
  schedule:
    # Daily at 8:20 UTC
    - cron: '20 8 * * *'
jobs:
  track_pr:
    runs-on: ubuntu-latest
    steps:
      - run: |
          numOpenIssues="$(gh api graphql -F owner=$OWNER -F name=$REPO -f query='
            query($name: String!, $owner: String!) {
              repository(owner: $owner, name: $name) {
                issues(states:OPEN){
                  totalCount
                }
              }
            }
          ' --jq '.data.repository.issues.totalCount')"

          echo 'NUM_OPEN_ISSUES='$numOpenIssues >> $GITHUB_ENV
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OWNER: ${{ github.repository_owner }}
          REPO: ${{ github.event.repository.name }}
      - run: |
          gh issue create --title "Issue report" --body "$NUM_OPEN_ISSUES issues remaining" --repo $GITHUB_REPOSITORY
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
