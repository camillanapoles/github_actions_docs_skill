---
title: Suporte para o Controlador do Executor de Ações
description: O que você precisa saber antes de entrar em contato Suporte do GitHub para obter ajuda com o Actions Runner Controller.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/support-for-arc
captured: '2026-10-19'
section: Concepts / Runners
---

# Suporte para o Controlador do Executor de Ações

_O que você precisa saber antes de entrar em contato Suporte do GitHub para obter ajuda com o Actions Runner Controller._

## Visão geral

O projeto ARC (Controlador executor de ações) [ foi adotado pelo GitHub](https://github.com/actions/actions-runner-controller/discussions/2072) para ser lançado como um novo produto GitHub. Como resultado, atualmente há duas versões do ARC: o ARC legado mantido pela comunidade e o Autoscaling Runner Sets da GitHub. Os conjuntos de runners com escalonamento automático do GitHub funcionam com Kubernetes e OpenShift.

O GitHub dá suporte apenas à versão mais recente de Autoscaling Runner Sets do ARC. O suporte para o ARC herdado é fornecido pela comunidade apenas no repositório do [Actions Runner Controller](https://github.com/actions/actions-runner-controller).

## Escopo de suporte para o Actions Runner Controller

Para garantir uma adoção tranquila de Actions Runner Controller, recomendamos que as organizações contem com profissionais com conhecimento especializado em orquestração de contêineres. Muitos aspectos da instalação do ARC, incluindo orquestração, rede, aplicação de políticas e integração com provedores de clusters gerenciados, estão fora do escopo de Suporte do GitHub e exigem conhecimento aprofundado das suas ferramentas de clusterização (ou seja, Kubernetes ou OpenShift). Se sua solicitação de suporte estiver fora do escopo do que nossa equipe pode ajudá-lo, talvez possamos recomendar as próximas etapas para ajudar a resolver seu problema ou fornecer outras diretrizes. Sua solicitação de suporte estará fora do Suporte do GitHubescopo se a solicitação for principalmente sobre:

* A versão herdada do ARC mantida pela comunidade
* Instalando, configurando ou mantendo dependências
* Personalização de especificações de modelo
* Orquestração de contêineres, como configuração de Kubernetes/OpenShift, redes, criação de imagens em ARC (DinD), etc.
* Aplicando políticas de cluster
* Provedores gerenciados de orquestração de containers ou configurações específicas do provedor
* [Runner Container Hooks](https://github.com/actions/runner-container-hooks) em conjunto com o modo `kubernetes` do ARC
* Ferramentas de instalação além do Helm
* Provisionadores de armazenamento e PVCs (PersistentVolumeClaims)
* Práticas recomendadas, como configuração de servidores de métricas, cache de imagens etc.

Embora o ARC possa ser implantado com êxito com diferentes ferramentas e configurações, sua solicitação de suporte possivelmente estará fora do Suporte do GitHubescopo se o ARC tiver sido implantado com:

* Ferramentas de instalação além do Helm
* Personalização de especificações de conta de serviço e/ou modelo

Para mais informações sobre como entrar em contato com Suporte do GitHub, consulte [Entrando em contato com o suporte do GitHub](https://docs.github.com/pt/support/contacting-github-support).

!!! note
    * O ARC só tem suporte nas versões 3.9 e superiores do GitHub Enterprise Server.

## Trabalhando com Suporte do GitHub no Actions Runner Controller

Suporte do GitHub pode fazer perguntas sobre a implantação do Controlador do Executor de Ações e solicitar que você colete e anexe [logs do controlador, logs de ouvinte](../../tutorials/use-actions-runner-controller/troubleshoot.md#checking-the-logs-of-the-controller-and-runner-set-listener), logs de executor e gráficos do Helm (`values.yaml`) ao tíquete de suporte.
