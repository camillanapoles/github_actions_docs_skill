---
title: Adicionar um selo de status de fluxo de trabalho
description: Você pode exibir um selo de status no seu repositório para indicar o status dos seus fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/monitor-workflows/add-a-status-badge
captured: '2026-10-11'
section: GitHub Actions
---

# Adicionar um selo de status de fluxo de trabalho

_Você pode exibir um selo de status no seu repositório para indicar o status dos seus fluxos de trabalho._

> \[!NOTE]
> As notificações de fluxo de trabalho em um repositório privado não podem ser acessadas ​​externamente, portanto, você não poderá inseri-los ou vinculá-los por meio de um site externo.

Um selo de status mostra se um fluxo de trabalho está falhando ou passando. Um local comum para adicionar uma notificação de status é no arquivo `README.md` do repositório, mas você pode adicioná-lo a qualquer página da Web desejada. Por padrão, os selos exibem o status do seu branch-padrão. Se não houver execuções de fluxo de trabalho em seu branch padrão, ele exibirá o status da execução mais recente em todos os branches. Você pode exibir o status de uma execução de fluxo de trabalho para um branch ou um evento específico usando os parâmetros de consulta `branch` e `event` na URL.

![Captura de tela de um selo de status de fluxo de trabalho. Da direita para a esquerda, são mostrados: o logotipo do GitHub, o nome do fluxo de trabalho ("GitHub Actions Demo") e o status ("passing").](/assets/images/help/repository/actions-workflow-status-badge.png)

Para adicionar uma notificação de status de fluxo de trabalho ao arquivo `README.md`, primeiro localize a URL da notificação de status que você gostaria de exibir. Em seguida, você pode usar o Markdown para exibir a notificação como uma imagem em seu arquivo `README.md`. Para saber mais sobre a marcação de imagem no Markdown, confira [Sintaxe básica de escrita e formatação](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images).

## Usando a IU

Você pode criar um emblema de status do fluxo de trabalho diretamente na interface usando o nome do arquivo de fluxo de trabalho, o parâmetro de branch e o parâmetro de evento.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. No lado direito da página, ao lado do campo "Filter workflow runs", clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="Show workflow options" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg> para exibir um menu suspenso e clique em **Create status badge**.
5. Opcionalmente, selecione um branch se quiser exibir a notificação de status de um branch diferente do branch padrão.
6. Como alternativa, selecione o evento que acionará o fluxo de trabalho.
7. Clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-copy" aria-label="copy" role="img"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg> Copy status badge Markdown**.
8. Copie o Markdown para o arquivo `README.md`.

## Usar o nome do arquivo do fluxo de trabalho

Você pode criar a URL para uma notificação de status de fluxo de trabalho usando o nome do arquivo de fluxo de trabalho:

```text
https://github.com/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg
```

Para exibir a notificação de status do fluxo de trabalho em seu arquivo `README.md`, use a marcação do Markdown para inserir imagens. Para saber mais sobre a marcação de imagem no Markdown, confira [Sintaxe básica de escrita e formatação](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#images).

Por exemplo, adicione o Markdown a seguir ao arquivo `README.md` para adicionar uma notificação de status para um fluxo de trabalho com o caminho do arquivo `.github/workflows/main.yml`. O `OWNER` do repositório é a organização `github`, e o nome do `REPOSITORY` é `docs`.

```markdown
![example workflow](https://github.com/github/docs/actions/workflows/main.yml/badge.svg)
```

## Como usar o parâmetro `branch`

Para exibir o status de uma execução de fluxo de trabalho para um branch específico, adicione `?branch=BRANCH-NAME` ao final da URL da notificação de status.

Por exemplo, adicione o seguinte Markdown ao seu arquivo `README.md` para exibir um emblema de status para uma ramificação com o nome `feature-1`.

```markdown
![example branch parameter](https://github.com/github/docs/actions/workflows/main.yml/badge.svg?branch=feature-1)
```

## Como usar o parâmetro `event`

Para exibir o status das execuções de fluxo de trabalho disparadas pelo evento `push`, adicione `?event=push` ao final da URL da notificação de status.

Por exemplo, adicione o seguinte Markdown ao seu arquivo `README.md` para exibir uma notificação com o status das execuções de fluxo de trabalho acionadas pelo evento `push`, que mostrará o status do build para o estado atual desse branch.

```markdown
![example event parameter](https://github.com/github/docs/actions/workflows/main.yml/badge.svg?event=push)
```
