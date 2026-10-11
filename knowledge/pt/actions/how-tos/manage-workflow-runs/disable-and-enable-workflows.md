---
title: Desabilitar e habilitar um fluxo de trabalho
description: Você pode desabilitar e habilitar novamente um fluxo de trabalho usando a interface do usuário de GitHub, a API REST, ou GitHub CLI.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows
captured: '2026-10-11'
section: GitHub Actions
---

# Desabilitar e habilitar um fluxo de trabalho

_Você pode desabilitar e habilitar novamente um fluxo de trabalho usando a interface do usuário de GitHub, a API REST, ou GitHub CLI._

Desabilitar um fluxo de trabalho permite que você impeça que um fluxo de trabalho seja acionado sem ter de excluir o arquivo do repositório. Você pode facilmente reabilitar o fluxo de trabalho novamente em GitHub.

Desabilitar temporariamente um fluxo de trabalho pode ser útil em vários cenários. Estes são alguns exemplos em que desabilitar um fluxo de trabalho pode ser útil:

* Um erro de fluxo de trabalho que produz muitas solicitações ou solicitações erradas, afetando negativamente os serviços externos.
* Um fluxo de trabalho que não é crítico e está consumindo muitos minutos na sua conta.
* Um fluxo de trabalho que envia solicitações para um serviço que não está ativo.
* Fluxos de trabalho que não são necessários em um repositório bifurcado (por exemplo, fluxos de trabalho agendados).

> \[!WARNING]
> Para evitar execuções desnecessárias do fluxo de trabalho, os fluxos de trabalho programados podem ser desabilitados automaticamente. Quando um repositório público é bifurcado, os fluxos de trabalho programados são desabilitados por padrão. Em um repositório público, os fluxos de trabalho agendados são automaticamente desabilitados quando nenhuma atividade do repositório ocorreu em 60 dias.

Também é possível desabilitar e habilitar um fluxo de trabalho usando a API REST. Para saber mais, confira [Endpoints da API REST para fluxos de trabalho](https://docs.github.com/pt/rest/actions/workflows).

## Desabilitar um fluxo de trabalho

<div class="ghd-tool webui">

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja desabilitar.
4. Clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="Show workflow options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> para exibir um menu suspenso e clique em **Desabilitar fluxo de trabalho**.

   ![Captura de tela de um fluxo de trabalho. O botão "Mostrar opções de fluxo de trabalho", exibido com um ícone de kebab, e o item de menu "Desativar fluxo de trabalho" estão contornados em laranja.](/assets/images/help/repository/actions-disable-workflow-2022.png)

</div>

<div class="ghd-tool cli">

> \[!NOTE]
> Para saber mais sobre GitHub CLI, confira [Sobre GitHub CLI](https://docs.github.com/pt/github-cli/github-cli/about-github-cli).

Para desabilitar um fluxo de trabalho, use o subcomando `workflow disable`. Substitua `workflow` pelo nome, pela ID ou pelo nome do arquivo de fluxo de trabalho que deseja desabilitar. Por exemplo, `"Link Checker"`, `1234567` ou `"link-check-test.yml"`. Se você não especificar um fluxo de trabalho, GitHub CLI irá retornar um menu interativo para você escolher um fluxo de trabalho.

```shell
gh workflow disable WORKFLOW
```

</div>

## Habilitar um fluxo de trabalho

<div class="ghd-tool webui">

Você pode habilitar novamente um fluxo de trabalho que foi desabilitado anteriormente.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja habilitar.

   ![Captura de tela da página "Ações". Na barra lateral esquerda, o nome do fluxo de trabalho está realçado com um contorno em laranja escuro.](/assets/images/help/repository/actions-select-disabled-workflow-2022.png)

4. Clique em **Habilitar fluxo de trabalho**.

</div>

<div class="ghd-tool cli">

Para habilitar um fluxo de trabalho, use o subcomando `workflow enable`. Substitua `workflow` pelo nome, pela ID ou pelo nome do arquivo de fluxo de trabalho que deseja habilitar. Por exemplo, `"Link Checker"`, `1234567` ou `"link-check-test.yml"`. Se você não especificar um fluxo de trabalho, GitHub CLI irá retornar um menu interativo para você escolher um fluxo de trabalho.

```shell
gh workflow enable WORKFLOW
```

</div>
