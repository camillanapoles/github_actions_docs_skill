---
title: Desenvolver fluxos de trabalho agente no GitHub Actions
description: Use GitHub Agentic Workflows para transformar instruções do Markdown em automações alimentadas por agentes de codificação de terceiros.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/develop-agentic-workflows-in-github-actions
captured: '2026-10-13'
section: Tutorials
---

# Desenvolver fluxos de trabalho agente no GitHub Actions

_Use GitHub Agentic Workflows para transformar instruções do Markdown em automações alimentadas por agentes de codificação de terceiros._

!!! note
    GitHub Agentic Workflows estão sujeitos prévia pública a alterações.

## Introduction

GitHub Agentic Workflows permitir que você defina automações de repositório no Markdown e escolha o agente de codificação de IA que as executa. A `gh aw` extensão compila cada fluxo de trabalho agente em um GitHub Actions fluxo de trabalho.

Todo o ciclo de vida do fluxo de trabalho — criação, depuração e otimização — é ele próprio agente. Você descreve o que deseja em linguagem natural e um agente de codificação cria, refina e soluciona o fluxo de trabalho para você.

Este tutorial usa um agente de codificação para criar um revisor de solicitação de pull automatizado que verifica se as alterações são testadas adequadamente.

## Pré-requisitos

Antes de começar, verifique se você tem:

* Um repositório onde GitHub Actions está habilitado e você tem acesso de gravação
* GitHub CLI versão 2.0.0 ou posterior instalada e autenticada
* Acesso a um agente de codificação com suporte, como Claude Code, OpenAI Codexou CLI do Google Gemini, ou Copilot CLI, e sua credencial necessária

Para autenticar GitHub CLI, execute:

```shell
gh auth login --scopes repo,workflow
```

## Instalando a `gh aw` extensão

Instale a GitHub Agentic Workflows extensão para GitHub CLI:

```shell
gh extension install github/gh-aw
```

## Escolhendo um agente e configurando a autenticação

Escolha a CLI do agente que melhor se ajusta ao fluxo de trabalho.
Claude Code, OpenAI Codexou CLI do Google Gemini
Copilot CLI e todos podem ser executadosGitHub Agentic Workflows.

Este artigo explica uma configuração simples que adiciona a credencial do agente como um segredo do repositório. Se você usar Claude Code, OpenAI Codexou CLI do Google Gemini, armazene a chave de API do agente como um segredo do repositório.

| CLI do agente | Valor `engine` | Segredo do repositório |
| --- | --- | --- |
| Código Claude | `claude` |  |
| `ANTHROPIC_API_KEY`que contém uma chave de API Anthropic |  |  |
| OpenAI Codex | `codex` |  |
| `OPENAI_API_KEY` que contém uma chave de API OpenAI |  |  |
| CLI do Google Gemini | `gemini` |  |
| `GEMINI_API_KEY` que contém uma chave de API do Google AI Studio |  |  |
| Copilot CLI (predefinição) | `copilot` | Nenhum segredo necessário para repositórios da organização (veja abaixo). Para repositórios pessoais, `COPILOT_GITHUB_TOKEN` contendo um refinamento personal access token com **Copilot solicitações definidas** como **Leitura**. |

Outros mecanismos, como Pi (experimental), também têm suporte. Para obter a lista completa, consulte a [GitHub Agentic Workflows referência de autenticação](https://github.github.com/gh-aw/reference/auth/).

### Cobrança da organização para GitHub Copilot

Se você usar GitHub Copilot em um repositório de propriedade da organização, poderá usar GitHub Actions' interno em `GITHUB_TOKEN` vez de um personal access token. Adicione `copilot-requests: write` ao frontmatter `permissions` de fluxo de trabalho e nenhum segredo separado é necessário. Para obter as etapas de instalação, consulte [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows#using-the-built-in-github_token).

### Armazenando um segredo na interface do usuário do GitHub

Para adicionar um segredo para Claude Code, OpenAI Codexou CLI do Google Geminirepositórios pessoais ou GitHub Copilot pessoais:

1. Em GitHubseguida, navegue até o repositório.
2. No nome do repositório, clique em **(gear) Configurações**.
3. Na barra lateral, clique em **Segredos e variáveis e** clique em **Ações**.
4. Clique em **Novo segredo de repositório**.
5. No campo **Nome** , insira o nome do segredo da tabela acima.
6. No campo **Segredo** , insira o valor.
7. Clique em **Adicionar segredo**.

## Criar o fluxo de trabalho

Use um agente de codificação para criar o fluxo de trabalho a partir de uma descrição de linguagem natural.

1. Na raiz do repositório, inicialize o repositório para criação agente. Isso adiciona habilidades e instruções que ajudam o agente de codificação a criar e editar fluxos de trabalho:

            ```shell
   gh aw init
   ```

2. Inicie uma sessão de agente de codificação no contexto do repositório, por exemplo, usando Claude Code, OpenAI Codexou CLI do Google Gemini, Copilot CLIou modo de agente do VS Code.

3. Use a `agentic-workflows` habilidade e descreva o fluxo de trabalho desejado:

            ```copilot copy
   /agentic-workflows create a pr reviewer that ensure the changes are tested.
   ```

   O agente cria um arquivo Markdown de fluxo de trabalho, `.github/workflows/`compila o arquivo de fluxo de trabalho correspondente `.lock.yml`GitHub Actions e solicita que você examine e confirme ambos os arquivos.

4. Examine o fluxo de trabalho gerado e, em seguida, peça ao agente para confirmar e enviar os arquivos por push.

!!! tip
    Você pode usar a mesma abordagem agente para atualizar e melhorar o fluxo de trabalho após a execução. Peça ao agente para refinar os critérios de revisão, adicionar mais verificações ou depurar uma execução com falha, tudo em linguagem natural. Se você editar o frontmatter de fluxo de trabalho mais tarde, execute `gh aw compile` antes de confirmar suas alterações.

## Executando o fluxo de trabalho

O fluxo de trabalho gerado é disparado automaticamente em solicitações pull, portanto, ele é executado na próxima vez que você abrir ou atualizar uma solicitação de pull em seu repositório.

1. Abra uma solicitação pull no repositório.
2. Em GitHubseguida, navegue até o repositório e clique na guia **Ações** .
3. Na barra lateral esquerda, selecione o fluxo de trabalho que o agente criou.
4. Depois que a execução for concluída, o fluxo de trabalho deixará uma revisão de solicitação de pull observando se as alterações incluem testes suficientes.

## Próximas Etapas

* Para criar um fluxo de trabalho que produz um relatório de atividade de problema semanal, consulte [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).
* Para obter configuração avançada do mecanismo, saídas seguras e mais exemplos de fluxo de trabalho, consulte o site de [GitHub Agentic Workflows documentação](https://github.github.com/gh-aw/).
