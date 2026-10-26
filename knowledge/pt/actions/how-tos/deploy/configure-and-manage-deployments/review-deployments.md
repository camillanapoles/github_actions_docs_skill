---
title: Revisar implantações
description: Você pode aprovar ou rejeitar trabalhos que estão aguardando revisão.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments
captured: '2026-10-26'
section: How tos / Deploy / Configure and manage deployments
---

# Revisar implantações

_Você pode aprovar ou rejeitar trabalhos que estão aguardando revisão._

## Aprovar ou rejeitar um trabalho

1. Acesse a execução do fluxo de trabalho que requer revisão. Para obter mais informações sobre como acessar uma execução de fluxo de trabalho, confira [Visualizar o histórico de execução do fluxo de trabalho](../../monitor-workflows/view-workflow-run-history.md).
2. Se a execução exigir revisão, você verá uma notificação para a solicitação de revisão. Na notificação, clique em **Examinar implantações**.
3. Selecione o(s) ambiente(s) de trabalho a serem aprovados ou rejeitados. Opcionalmente, deixe um comentário.
4. Aprovar ou rejeitar:
   * Para aprovar o trabalho, clique em **Aprovar e implantar**. Assim que um trabalho for aprovado (e quaisquer outras regras de proteção de implantação tiverem sido aprovadas), o trabalho prosseguirá. Nesta altura, o trabalho pode acessar quaisquer segredos armazenados no ambiente.
   * Para rejeitar o trabalho, clique em **Rejeitar**. Se um trabalho for rejeitado, o fluxo de trabalho falhará.

!!! note
    Se o ambiente de destino estiver configurado para impedir a autoaprovação de implementações, você não poderá aprovar uma implementação com base em uma execução de fluxo de trabalho iniciada por você. Para saber mais, confira [Gerenciar ambientes para implantação](manage-environments.md).

## Ignorando as regras de proteção de implantação

Se você configurou regras de proteção de implantação que controlam se o software pode ser implantado em um ambiente, você pode ignorá-las e forçar todos os trabalhos pendentes que fazem referência ao ambiente a prosseguir.

!!! note
    * Você não poderá ignorar as regras de proteção de implantação caso tenham sido configuradas para impedir que os administradores ignorem as regras de proteção configuradas. Para saber mais, confira [Gerenciar ambientes para implantação](manage-environments.md#creating-an-environment).
    * Você só poderá ignorar as regras de proteção de implantação durante a execução do fluxo de trabalho quando um trabalho que faz referência ao ambiente estiver em um estado "Pendente".

1. Navegue até a execução do fluxo de trabalho. Para obter mais informações sobre como acessar uma execução de fluxo de trabalho, confira [Visualizar o histórico de execução do fluxo de trabalho](../../monitor-workflows/view-workflow-run-history.md).
2. À direita das **Regras de proteção de implantação**, clique em **Iniciar todos os trabalhos pendentes**.

![Captura de tela da seção "Regras de proteção de implantação" com o botão "Iniciar todas as tarefas em espera" destacado em laranja.](https://docs.github.com/assets/images/actions-bypass-env-protection-rules.png)

1. Na janela pop-up, selecione os ambientes para os quais você deseja ignorar as regras de proteção de implantação.
2. Em **Deixar um comentário**, insira uma descrição para ignorar as regras de proteção de implantação.
3. Clique em **Eu entendo as consequências, iniciar a implantação**.
