---
title: Ambientes de implantação
description: Você pode criar e implementar em ambientes diferentes.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/deployment-environments
captured: '2026-10-13'
section: Concepts / Workflows and actions
---

# Ambientes de implantação { #deployment-environments }

_Você pode criar e implementar em ambientes diferentes._

Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../../how-tos/deploy/configure-and-manage-deployments/manage-environments.md).

Cada trabalho em um fluxo de trabalho pode fazer referência a um único ambiente. Todas as regras de proteção configuradas para o ambiente têm de ser aprovadas antes que um trabalho de referência ao ambiente seja enviado a um executor. O trabalho só pode acessar os segredos do ambiente depois que for enviado para um executor.

Quando um fluxo de trabalho faz referência a um ambiente, o ambiente aparecerá nas implantações do repositório. Para saber mais sobre como ver as implantações atuais e anteriores, confira [Exibir o histórico de implantações](../../how-tos/deploy/configure-and-manage-deployments/view-deployment-history.md).
