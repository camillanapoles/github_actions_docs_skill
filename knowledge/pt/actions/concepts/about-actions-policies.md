---
title: Sobre as políticas do Actions
description: Governe como GitHub Actions os fluxos de trabalho são executados em seu repositório, organização ou empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/about-actions-policies
captured: '2026-10-13'
section: Concepts
---

# Sobre as políticas do Actions { #about-actions-policies }

_Governe como GitHub Actions os fluxos de trabalho são executados em seu repositório, organização ou empresa._

## Sobre as políticas do Actions { #about-actions-policies-1 }

As políticas de ações permitem que você governe como GitHub Actions os fluxos de trabalho são executados. Você pode configurá-las na seção **Políticas** de suas GitHub Actions configurações (separadas das configurações **gerais** ).

As políticas de ações estão disponíveis nos níveis corporativo, organizacional e repositório. Atualmente, eles contêm um tipo de política: proteções de execução de fluxo de trabalho.
GitHub planeja adicionar mais políticas ao longo do tempo.

## Sobre proteções de execução de fluxo de trabalho { #about-workflow-execution-protections }

Com as proteções de execução de fluxo de trabalho, você pode definir uma lista de permissões que controla quem pode disparar GitHub Actions fluxos de trabalho e quais eventos têm permissão para executá-los. Essas proteções podem interromper vários padrões de ataque do mundo real:

* **Execução de pipeline comprometida por pull requests.** Restrinja ou proíba `pull_request_target`, inclusive em repositórios públicos em que ele é explorado com mais frequência.
* **Abuso de acionamento manual.** Limite `workflow_dispatch` para que identidades não confiáveis não possam iniciar fluxos de trabalho.
* **Execução por agente não confiável.** Bloqueie completamente identidades de baixa confiança para que não acionem fluxos de trabalho.
* **Exploração de configuração incorreta.** Aplique uma política central que substitua qualquer arquivo de fluxo de trabalho configurado incorretamente.

Quando aplicada, as execuções de fluxo de trabalho não permitidas falharão com erro. Por exemplo:

```text
Event 'workflow_dispatch' is not allowed to trigger Actions workflows. Workflow file: '.github/workflows/0-welcome.yml'.
```

<!-- expires 2026-11-02 -->

> [!NOTE] GitHub adicionou uma política padrão que bloqueará o `pull_request_target` evento em repositórios públicos. Essa política será imposta em 2 de novembro de 2026. Consulte [Uso seguro de pull_request_target](../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target).

<!-- end expires 2026-11-02 -->

### Regras disponíveis { #available-rules }

* **Regras de atores** controlam quem pode disparar fluxos de trabalho, incluindo usuários individuais, funções de repositório, GitHub Apps, Copilot e Dependabot. Por padrão, cada usuário com acesso de gravação a um repositório pode disparar fluxos de trabalho. As regras para atores permitem separar quem contribui com código de quem executa sua integração contínua (CI), para que você possa conceder a um colaborador permissão de escrita sem conceder a ele a permissão de executar fluxos de trabalho.
* **As regras de** evento controlam quais eventos são permitidos, como`push`, , `pull_request`e `pull_request_target``workflow_dispatch`.

GitHub planeja adicionar mais regras ao longo do tempo.

## Próximas Etapas { #next-steps }

Para configurar proteções de execução de fluxo de trabalho, consulte [Controle da execução de GitHub Actions fluxos de trabalho](../how-tos/administer/control-workflow-execution.md).

Para gerenciar políticas programaticamente, consulte [Pontos de extremidade da API REST para políticas de GitHub Actions](https://docs.github.com/pt/rest/actions/policies).
