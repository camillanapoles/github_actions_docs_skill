---
title: Conjuntos de dimensionamento de executor
description: Saiba mais sobre o que é um runner scale set e como ele pode interagir com o Actions Runner Controller.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/runner-scale-sets
captured: '2026-10-13'
section: Concepts / Runners
---

# Conjuntos de dimensionamento de executor { #runner-scale-sets }

_Saiba mais sobre o que é um runner scale set e como ele pode interagir com o Actions Runner Controller._

## Sobre os conjuntos de dimensionamento de executores { #about-runner-scale-sets }

Um conjunto de escala de runners é um grupo de runners homogêneos aos quais podem ser atribuídos trabalhos de GitHub Actions. O número de runners ativos pertencentes a um conjunto de dimensionamento de runners pode ser controlado por soluções de dimensionamento automático de runners, como Actions Runner Controller (ARC).

Use grupos de executores para gerenciar conjuntos de dimensionamento de executores. De modo semelhante aos executores auto-hospedados, você pode adicionar conjuntos de dimensionamento de executores a grupos de executores existentes. No entanto, os conjuntos de dimensionamento de executores podem pertencer a apenas um grupo de executores por vez. Um runner scale set pode ter mais de um rótulo, e os fluxos de trabalho podem direcioná-lo por seu nome ou por seus rótulos em `runs-on`. O suporte para vários rótulos foi adicionado no Actions Runner Controller 0.14.0.

Para atribuir trabalhos a um conjunto de dimensionamento de executores, você precisa configurar o fluxo de trabalho para referenciar o nome do conjunto de dimensionamento de executores. Para saber mais, confira [Usar executores do Controlador do Executor de Ações em um fluxo de trabalho](../../how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md).

## Aviso legal { #legal-notice }

Partes foram adaptadas do <https://github.com/actions/actions-runner-controller/> de acordo com a licença Apache-2.0:

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

## Próximas etapas { #next-steps }

* Para obter mais informações sobre o conceito Actions Runner Controller como conceito, consulte [Controlador de Ações Runner](actions-runner-controller.md).
* Para saber mais sobre grupos de runners, consulte [Gerenciar o acesso a executores auto-hospedados usando grupos](../../how-tos/manage-runners/self-hosted-runners/manage-access.md).
