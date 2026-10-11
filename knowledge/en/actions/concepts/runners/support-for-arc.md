---
title: Support for Actions Runner Controller
description: What to know before you [contact GitHub Support](/support/contacting-github-support) for assistance with Actions Runner Controller.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/concepts/runners/support-for-arc.md
captured: '2026-10-11'
section: Concepts / Runners
---

# Support for Actions Runner Controller

_What to know before you [contact GitHub Support](/support/contacting-github-support) for assistance with Actions Runner Controller._

## Overview

The Actions Runner Controller (ARC) project [was adopted by GitHub](https://github.com/actions/actions-runner-controller/discussions/2072) to release as a new GitHub product. As a result, there are currently two ARC releases: the legacy community-maintained ARC and GitHub's Autoscaling Runner Sets. GitHub's Autoscaling Runner Sets work with both Kubernetes and OpenShift.

GitHub only supports the latest Autoscaling Runner Sets version of ARC. Support for the legacy ARC is provided by the community in the [Actions Runner Controller](https://github.com/actions/actions-runner-controller) repository only.

## Scope of support for Actions Runner Controller

To ensure a smooth adoption of Actions Runner Controller, we recommend that organizations have staff with expert-level knowledge of container orchestration. Many aspects of ARC installation, including orchestration, networking, policy application, and integration with managed cluster providers, fall outside GitHub Support's scope and require in-depth knowledge of your clustering tools (i.e. Kubernetes or OpenShift). If your support request is outside of the scope of what our team can help you with, we may be able to recommend next steps to help resolve your issue or provide other guidance. Your support request is out of GitHub Support's scope if the request is primarily about:

* The legacy community-maintained version of ARC
* Installing, configuring, or maintaining dependencies
* Template spec customization
* Container orchestration, such as Kubernetes/OpenShift setup, networking, building images in ARC (DinD), etc.
* Applying cluster policies
* Managed container orchestration providers or provider-specific configurations
* [Runner Container Hooks](https://github.com/actions/runner-container-hooks) in conjunction with ARC's `kubernetes` mode
* Installation tooling other than Helm
* Storage provisioners and PersistentVolumeClaims (PVCs)
* Best practices, such as configuring metrics servers, image caching, etc.

While ARC may be deployed successfully with different tooling and configurations, your support request is possibly out of GitHub Support's scope if ARC has been deployed with:

* Installation tooling other than Helm
* Service account and/or template spec customization

For more information about contacting GitHub Support, see [Contacting github support](https://docs.github.com/support/contacting-github-support).

> [!NOTE]
> * ARC is only supported on GitHub Enterprise Server versions 3.9 and greater.

## Working with GitHub Support for Actions Runner Controller

GitHub Support may ask questions about your Actions Runner Controller deployment and request that you collect and attach [controller logs, listener logs](../../tutorials/use-actions-runner-controller/troubleshoot.md#checking-the-logs-of-the-controller-and-runner-set-listener), runner logs, and Helm charts (`values.yaml`) to the support ticket.
