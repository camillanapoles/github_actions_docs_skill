---
title: Passing information between jobs
description: You can define outputs to pass information from one job to another.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs.md
captured: '2026-10-11'
section: How tos / Write workflows / Choose what workflows do
---

# Passing information between jobs

_You can define outputs to pass information from one job to another._

## Defining and using job outputs

1. Open the workflow file containing the job you want to get outputs from.
1. Use the `jobs.<job_id>.outputs` syntax to define the outputs for the job. For example, the following job defines the `output1` and `output2` outputs, which are mapped to the results of `step1` and `step2` respectively:

            ```yaml
   jobs:
     job1:
       runs-on: ubuntu-latest
       outputs:
         output1: ${{ steps.step1.outputs.test }}
         output2: ${{ steps.step2.outputs.test }}
       steps:
         - id: step1
           run: echo "test=hello" >> "$GITHUB_OUTPUT"
         - id: step2
           run: echo "test=world" >> "$GITHUB_OUTPUT"
            ```

1. In a separate job where you want to access those outputs, use the `jobs.<job_id>.needs` syntax to make it dependent on the original job. For example, the following job checks that `job1` is complete before running:

                ```yaml
    jobs:
      # Assume job1 is defined as above
      job2:
        runs-on: ubuntu-latest
        needs: job1
                ```

1. To access the outputs in the dependent job, use the `needs.<job_id>.outputs.<output_name>` syntax. For example, the following job accesses the `output1` and `output2` outputs defined in `job1`:

                ```yaml
    jobs:
      # Assume job1 is defined as above
      job2:
        runs-on: ubuntu-latest
        needs: job1
        steps:
          - env:
              OUTPUT1: ${{needs.job1.outputs.output1}}
              OUTPUT2: ${{needs.job1.outputs.output2}}
            run: echo "$OUTPUT1 $OUTPUT2"
                ```

## Next steps

To learn more about job outputs and the `needs` context, see the following sections of [Workflow syntax for GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs#jobsjob_idoutputs):
* [`jobs.<job_id>.outputs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs)
* [`jobs.<job_id>.needs`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds)

To learn more about passing job outputs from one workflow to another, see the following section of [Reuse workflows](../../reuse-automations/reuse-workflows.md):
* [Using outputs from a reusable workflow](../../reuse-automations/reuse-workflows.md#using-outputs-from-a-reusable-workflow)
