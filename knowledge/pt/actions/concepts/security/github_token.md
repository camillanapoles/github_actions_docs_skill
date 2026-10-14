---
title: GITHUB_TOKEN
description: Saiba o que GITHUB_TOKEN é, como funciona e por que ele é importante para a automação segura em GitHub Actions fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/github_token
captured: '2026-10-11'
section: Concepts / Security
---

# GITHUB_TOKEN

_Saiba o que GITHUB_TOKEN é, como funciona e por que ele é importante para a automação segura em GitHub Actions fluxos de trabalho._

## Sobre o `GITHUB_TOKEN` { #about-the-githubtoken }

No início de cada tarefa do fluxo de trabalho, GitHub cria automaticamente um segredo exclusivo `GITHUB_TOKEN` a ser usado no fluxo de trabalho. Use o `GITHUB_TOKEN` para se autenticar em um fluxo de trabalho.

Quando você habilita GitHub Actions, GitHub instala um GitHub App no repositório. O segredo `GITHUB_TOKEN` é um GitHub App token de acesso de instalação. Você pode usar o token de acesso de instalação para autenticar em nome do GitHub App instalado em seu repositório. As permissões do token são restritas ao repositório do fluxo de trabalho. Para obter mais informações, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#permissions).

Antes de cada trabalho começar, GitHub busca um token de acesso de instalação para o trabalho. O `GITHUB_TOKEN` expira quando o trabalho é concluído ou após seu tempo de vida máximo efetivo.

O tempo de vida útil máximo efetivo do token depende do tipo de runner:

* **GitHub-execuções hospedadas** O tempo de execução do trabalho máximo é de 6 horas, logo, o `GITHUB_TOKEN` pode durar, no máximo, 6 horas.
* **Executores auto-hospedados** O tempo máximo de execução do trabalho é de 5 dias. No entanto, como o `GITHUB_TOKEN` é um token de acesso de instalação, ele só pode ser renovado por no máximo 24 horas. Se o trabalho durar mais de 24 horas, use um personal access token ou outro método de autenticação em vez disso.

O token também está disponível no contexto `github.token`. Para obter mais informações, consulte [Referência de contextos](../../reference/workflows-and-actions/contexts.md#github-context).

## Quando `GITHUB_TOKEN` dispara execuções do fluxo de trabalho { #when-githubtoken-triggers-workflow-runs }

Quando você usa o `GITHUB_TOKEN` do repositório para executar tarefas, os eventos acionados pelo `GITHUB_TOKEN` não criarão uma nova execução de fluxo de trabalho, com as seguintes exceções:

* ```
            Eventos `workflow_dispatch` e `repository_dispatch` sempre criam execuções do fluxo de trabalho.
        ```
* ```
            Eventos `pull_request` com os tipos de atividade `opened`, `synchronize` ou `reopened`: quando um fluxo de trabalho que usa `GITHUB_TOKEN` cria ou atualiza uma pull request, o evento `pull_request` resultante cria execuções do fluxo de trabalho em um estado **aprovação-obrigatória**. O pull request exibe um banner na caixa de merge, e um usuário com acesso de escrita ao repositório pode iniciar as execuções selecionando **Aprovar fluxos de trabalho para execução**. Outros `pull_request` tipos de atividade (como `labeled`, `edited`ou `closed`) não criam execuções de fluxo de trabalho. Isso impede que o fluxo de trabalho recursivo seja executado enquanto ainda permite que os fluxos de trabalho de CI sejam executados em solicitações de pull criadas pela automação. Para obter mais informações sobre como aprovar execuções de fluxo de trabalho, consulte [Approve runs from forks](../../how-tos/manage-workflow-runs/approve-runs-from-forks.md).
        ```

Para todos os outros eventos, esse comportamento impede que você crie acidentalmente execuções de fluxo de trabalho recursivo. Por exemplo, se uma execução de fluxo de trabalho efetuar push do código usando o `GITHUB_TOKEN` do repositório, um novo fluxo de trabalho não será executado mesmo quando o repositório contiver um fluxo de trabalho configurado para ser executado quando os eventos do `push` ocorrerem.

!!! note
    Se você precisar de execuções do fluxo de trabalho a partir de pull requests criadas pelo fluxo de trabalho a serem executadas sem exigir aprovação, use um GitHub App token de acesso de instalação ou um personal access token em vez de `GITHUB_TOKEN` durante a criação ou a atualização da pull request.

Commits enviados por push por um fluxo de trabalho de GitHub Actions que usa o `GITHUB_TOKEN` não disparam um build de GitHub Pages.

## Próximas etapas { #next-steps }

* [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md)
* [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#permissions)
