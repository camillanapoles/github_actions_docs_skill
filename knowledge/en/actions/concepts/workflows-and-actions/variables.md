---
title: Variables
description: Learn about variables in GitHub Actions workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/workflows-and-actions/variables.md
captured: '2026-10-11'
section: Concepts / Workflows and actions
---

# Variables

_Learn about variables in GitHub Actions workflows._

## About

Variables provide a way to store and reuse non-sensitive configuration information. You can store any configuration data such as compiler flags, usernames, or server names as variables. Variables are interpolated on the runner machine that runs your workflow. Commands that run in actions or workflow steps can create, read, and modify variables.

You can set your own custom variables or use the default environment variables that GitHub sets automatically.

You can set a custom variable in two ways.

* To define an environment variable for use in a single workflow, you can use the `env` key in the workflow file. For more information, see [Defining environment variables for a single workflow](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-environment-variables-for-a-single-workflow).
* To define a configuration variable across multiple workflows, you can define it at the organization, repository, or environment level. When creating a variable in an organization, you can use a policy to limit access by repository. For example, you can grant access to all repositories, or limit access to only private repositories or a specified list of repositories. For more information, see [Defining configuration variables for multiple workflows](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-configuration-variables-for-multiple-workflows).

!!! warning
    By default, variables render unmasked in your build outputs. If you need greater security for sensitive information, such as passwords, use secrets instead. For more information, see [Secrets](../security/secrets.md).

For reference documentation, see [Variables reference](../../reference/workflows-and-actions/variables.md).
