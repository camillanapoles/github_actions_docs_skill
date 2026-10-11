---
title: Get started with Actions Runner Controller
description: In this tutorial, you'll try out the basics of Actions Runner Controller.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/tutorials/use-actions-runner-controller/get-started.md
captured: '2026-10-11'
section: Tutorials / Use actions runner controller
---

# Get started with Actions Runner Controller

_In this tutorial, you'll try out the basics of Actions Runner Controller._

## Prerequisites

In order to use ARC, ensure you have the following.

* A Kubernetes cluster
  * For a managed cloud environment, you can use AKS. For more information, see [Azure Kubernetes Service](https://azure.microsoft.com/en-us/products/kubernetes-service) in the Azure documentation.
  * For a local setup, you can use minikube or kind. For more information, see [minikube start](https://minikube.sigs.k8s.io/docs/start/) in the minikube documentation and [kind](https://kind.sigs.k8s.io/) in the kind documentation.

* Helm 3
  * For more information, see [Installing Helm](https://helm.sh/docs/intro/install/) in the Helm documentation.
* While it is not required for ARC to be deployed, we recommend ensuring you have implemented a way to collect and retain logs from the controller, listeners, and ephemeral runners before deploying ARC in production workflows.

## Installing Actions Runner Controller

1. To install the operator and the custom resource definitions (CRDs) in your cluster, do the following.
    1. In your Helm chart, update the `NAMESPACE` value to the location you want your operator pods to be created. This namespace must allow access to the Kubernetes API server.
    1. Install the Helm chart.

    The following example installs the latest version of the chart. To install a specific version, you can pass the `--version` argument along with the version of the chart you wish to install. You can find the list of releases in the [GitHub Container Registry](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set-controller).

                ```bash copy
    NAMESPACE="arc-systems"
    helm install arc \
        --namespace "${NAMESPACE}" \
        --create-namespace \
        oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
    ```

    For additional Helm configuration options, see [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) in the ARC documentation.

1. To enable ARC to authenticate to GitHub, choose an authentication method for your runner scale set. If you are registering runners at the repository or organization level, we recommend authenticating with a GitHub App. Runner scale sets registered at the enterprise level require personal access token (classic) authentication. For more information, see [Authenticating ARC to the GitHub API](../../how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md).

## Configuring a runner scale set

1. To configure your runner scale set, run the following command in your terminal, using values from your ARC configuration.

    When you run the command, keep the following in mind.

    * Update the `INSTALLATION_NAME` value carefully. You will use the installation name as the value of `runs-on` in your workflows. For more information, see [Workflow syntax for GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on#jobsjob_idruns-on).
    * Update the `NAMESPACE` value to the location you want the runner pods to be created.
    * Set `GITHUB_CONFIG_URL` to the URL of your repository, organization, or enterprise. This is the entity that the runners will belong to.
    * This example uses a personal access token (classic) to keep the initial setup short. For repository or organization runner scale sets, use a GitHub App in production environments when possible.
    * Set `GITHUB_PAT` to a GitHub personal access token (classic) with the `repo` and `admin:org` scopes for repository and organization runners.

* Set `GITHUB_PAT` to a GitHub personal access token (classic) with the `repo` and `manage_runners:org` scopes for repository and organization runners, and the `manage_runners:enterprise` scope for enterprise runners.
    * This example command installs the latest version of the Helm chart. To install a specific version, you can pass the `--version` argument with the version of the chart you wish to install. You can find the list of releases in the [GitHub Container Registry](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set).

        > [!NOTE]
        > * As a security best practice, create your runner pods in a different namespace than the namespace containing your operator pods.
        > * As a security best practice, create Kubernetes secrets and pass the secret references. Passing your secrets in plain text via the CLI can pose a security risk. For more information, see [Deploying runner scale sets with Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).

                                ```bash copy
        INSTALLATION_NAME="arc-runner-set"
        NAMESPACE="arc-runners"
        GITHUB_CONFIG_URL="https://github.com/<your_enterprise/org/repo>"
        GITHUB_PAT="<PAT>"
        helm install "${INSTALLATION_NAME}" \
            --namespace "${NAMESPACE}" \
            --create-namespace \
            --set githubConfigUrl="${GITHUB_CONFIG_URL}" \
            --set githubConfigSecret.github_token="${GITHUB_PAT}" \
            oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
        ```

        For additional Helm configuration options, see [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) in the ARC documentation.

1. From your terminal, run the following command to check your installation.

                ```bash copy
    helm list -A
    ```

    You should see an output similar to the following.

                ```bash
    NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                                       APP VERSION
    arc             arc-systems     1               2023-04-12 11:45:59.152090536 +0000 UTC deployed        gha-runner-scale-set-controller-0.4.0       0.4.0
    arc-runner-set  arc-runners     1               2023-04-12 11:46:13.451041354 +0000 UTC deployed        gha-runner-scale-set-0.4.0                  0.4.0
    ```

1. To check the manager pod, run the following command in your terminal.

                ```bash copy
    kubectl get pods -n arc-systems
    ```

    If everything was installed successfully, the status of the pods shows as **Running**.

                ```bash
    NAME                                                   READY   STATUS    RESTARTS   AGE
    arc-gha-runner-scale-set-controller-594cdc976f-m7cjs   1/1     Running   0          64s
    arc-runner-set-754b578d-listener                       1/1     Running   0          12s
    ```

If your installation was not successful, see [Troubleshooting Actions Runner Controller errors](troubleshoot.md) for troubleshooting information.

## Using runner scale sets

Now you will create and run a simple test workflow that uses the runner scale set runners.

1. In a repository, create a workflow similar to the following example. The `runs-on` value should match the Helm installation name you used when you installed the autoscaling runner set.

    For more information on adding workflows to a repository, see [Quickstart for GitHub Actions](../../get-started/quickstart.md#creating-your-first-workflow#creating-your-first-workflow).

                ```yaml copy
    name: Actions Runner Controller Demo
    on:
      workflow_dispatch:

    jobs:
      Explore-GitHub-Actions:
        # You need to use the INSTALLATION_NAME from the previous step
        runs-on: arc-runner-set
        steps:
        - run: echo "🎉 This job uses runner scale set runners!"
    ```

1. Once you've added the workflow to your repository, manually trigger the workflow. For more information, see [Manually running a workflow](../../how-tos/manage-workflow-runs/manually-run-a-workflow.md).

1. To view the runner pods being created while the workflow is running, run the following command from your terminal.

                ```bash copy
    kubectl get pods -n arc-runners -w
    ```

    A successful output will look similar to the following.

                ```bash
    NAMESPACE     NAME                                                  READY   STATUS    RESTARTS      AGE
    arc-runners   arc-runner-set-rmrgw-runner-p9p5n                     1/1     Running   0             21s
    ```

## Next steps

Actions Runner Controller can help you efficiently manage your GitHub Actions runners. Ready to get started? Here are some helpful resources for taking your next steps with ARC:

* For detailed authentication information, see [Authenticating ARC to the GitHub API](../../how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md).
* For help using ARC runners in your workflows, see [Using Actions Runner Controller runners in a workflow](../../how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md).
* For deployment information, see [Deploying runner scale sets with Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).

## Legal notice

Portions have been adapted from https://github.com/actions/actions-runner-controller/ under the Apache-2.0 license:

```text
Copyright 2019 Moto Ishizawa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
