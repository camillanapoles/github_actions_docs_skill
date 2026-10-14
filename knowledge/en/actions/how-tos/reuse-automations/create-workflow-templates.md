---
title: Creating workflow templates for your organization
description: Learn how you can create workflow templates to help people in your team add new workflows more easily.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/reuse-automations/create-workflow-templates.md
captured: '2026-10-11'
section: How tos / Reuse automations
---

# Creating workflow templates for your organization

_Learn how you can create workflow templates to help people in your team add new workflows more easily._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

## Creating workflow templates

This procedure demonstrates how to create a workflow template and metadata file. The metadata file describes how the workflow templates will be presented to users when they are creating a new workflow.

1. If it doesn't already exist, create a new public repository named `.github` in your organization.
1. Create a directory named `workflow-templates`.
1. Create your new workflow file inside the `workflow-templates` directory.

   If you need to refer to a repository's default branch, you can use the `$default-branch` placeholder. When a workflow is created the placeholder will be automatically replaced with the name of the repository's default branch.

!!! note

   > The following values in the `runs-on` key are also treated as placeholders:
   >
   > * `ubuntu-latest` is replaced with `[ self-hosted ]`
   > * `windows-latest` is replaced with `[ self-hosted, windows ]`
   > * `macos-latest` is replaced with `[ self-hosted, macOS ]`

   For example, this file named `octo-organization-ci.yml` demonstrates a basic workflow.

            ```yaml copy
   name: Octo Organization CI

   on:
     push:
       branches: [ $default-branch ]
     pull_request:
       branches: [ $default-branch ]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v6

         - name: Run a one-line script
           run: echo Hello from Octo Organization
            ```

1. Create a metadata file inside the `workflow-templates` directory. The metadata file must have the same name as the workflow file, but instead of the `.yml` extension, it must be appended with `.properties.json`. For example, this file named `octo-organization-ci.properties.json` contains the metadata for a workflow file named `octo-organization-ci.yml`:

            ```json copy
{
    "name": "Octo Organization Workflow",
    "description": "Octo Organization CI workflow template.",
    "iconName": "example-icon",
    "categories": [
        "Go"
    ],
    "filePatterns": [
        "package.json$",
        "^Dockerfile",
        ".*\.md$"
    ]
}
            ```

   * `name` - **Required.** The name of the workflow. This is displayed in the list of available workflows.
* `description` - **Required.** The description of the workflow. This is displayed in the list of available workflows.
* `iconName` - **Optional.** Specifies an icon for the workflow that is displayed in the list of workflows. `iconName` can be one of the following types:
  * An SVG file that is stored in the `workflow-templates` directory. To reference a file, the value must be the file name without the file extension. For example, an SVG file named `example-icon.svg` is referenced as `example-icon`.
  * An icon from GitHub's set of [Octicons](https://primer.style/octicons/). To reference an octicon, the value must be `octicon <icon name>`. For example, `octicon smiley`.
* `categories` - **Optional.** Defines the categories that the workflow is shown under. You can use category names from the following lists:
  * General category names from the [starter-workflows](https://github.com/actions/starter-workflows/blob/main/README.md#categories) repository.
  * Linguist languages from the list in the [linguist](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml) repository.
  * Supported tech stacks from the list in the [starter-workflows](https://github.com/github-starter-workflows/repo-analysis-partner/blob/main/tech_stacks.yml) repository.

* `filePatterns` - **Optional.** Allows the workflow to be used if the user's repository has a file in its root directory that matches a defined regular expression.

1. To add another workflow template, add your files to the same `workflow-templates` directory.

## Next steps

* For reference information about workflow templates, see [Reusing workflow configurations](../../reference/workflows-and-actions/reusing-workflow-configurations.md#workflow-templates#workflow-templates).
