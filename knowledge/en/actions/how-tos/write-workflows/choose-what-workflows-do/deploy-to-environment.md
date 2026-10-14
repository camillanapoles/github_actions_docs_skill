---
title: Deploying to a specific environment
description: Specify a deployment environment in your workflow.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/write-workflows/choose-what-workflows-do/deploy-to-environment.md
captured: '2026-10-11'
section: How tos / Write workflows / Choose what workflows do
---

# Deploying to a specific environment

_Specify a deployment environment in your workflow._

## Prerequisites

You need to create an environment before you can use it in a workflow. See [Managing environments for deployment](../../deploy/configure-and-manage-deployments/manage-environments.md#creating-an-environment#creating-an-environment).

## Using an environment in a workflow

1. Open the workflow file you want to edit.
1. Use the following syntax to add a [`jobs.<job_id>.environment`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idenvironment) key to your workflow:

                ```yaml copy
    jobs:
      JOB-ID:
        environment: ENVIRONMENT-NAME
                ```

    The chosen job will now be subject to any rules configured for the specified environment.
1. Optionally, specify a deployment URL for the environment using the following syntax:

                ```yaml copy
    jobs:
      JOB-ID:
        environment:
            name: ENVIRONMENT-NAME
            url: URL
                ```

    The specified URL will appear:
    * On the deployments page for the repository
    * In the visualization graph for the workflow run
    * (If a pull request triggers the workflow) As a "View deployment" button in the pull request timeline

1. Optionally, prevent a deployment object from being created by adding the `deployment` property. When set to `false`, the job still has access to environment secrets and variables, but no GitHub deployment is created:

                ```yaml copy
    jobs:
      JOB-ID:
        environment:
            name: ENVIRONMENT-NAME
            deployment: false
                ```

    This is useful for CI or testing jobs that need environment secrets but aren't actually deploying anything. For more information, see [Deploying with GitHub Actions](../../deploy/configure-and-manage-deployments/control-deployments.md#using-environments-without-deployments#using-environments-without-deployments).
