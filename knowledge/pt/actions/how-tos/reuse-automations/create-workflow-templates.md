---
title: Criar modelos de fluxo de trabalho para sua organização
description: Saiba como você pode criar modelos de fluxo de trabalho para ajudar as pessoas de sua equipe a adicionar novos fluxos de trabalho com mais facilidade.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/reuse-automations/create-workflow-templates
captured: '2026-10-11'
section: How tos / Reuse automations
---

# Criar modelos de fluxo de trabalho para sua organização

_Saiba como você pode criar modelos de fluxo de trabalho para ajudar as pessoas de sua equipe a adicionar novos fluxos de trabalho com mais facilidade._

## Criando modelos de fluxo de trabalho

Esse procedimento demonstra como criar um modelo de fluxo de trabalho e um arquivo de metadados. O arquivo de metadados descreve como os modelos de fluxo de trabalho serão apresentados aos usuários quando eles criarem um novo fluxo de trabalho.

1. Se ainda não existir, crie um novo nomeado `.github` em sua organização.

2. Crie um diretório com o nome `workflow-templates`.

3. Crie o arquivo de fluxo de trabalho no diretório `workflow-templates`.

   Caso precise referir-se ao branch padrão de um repositório, use o placeholder `$default-branch`. Quando um fluxo de trabalho é criado, o placeholder será automaticamente substituído pelo nome do branch padrão do repositório.

   Por exemplo, este arquivo chamado `octo-organization-ci.yml` demonstra um fluxo de trabalho básico.

            ```yaml copy
   name: Octo Organization CI

   on:
     push:
       branches: [ $default-branch ]
     pull_request:
       branches: [ $default-branch ]

   jobs:
     build:
       runs-on: ubuntu-latest

       steps:
         - uses: actions/checkout@v6

         - name: Run a one-line script
           run: echo Hello from Octo Organization
   ```

4. Crie um arquivo de metadados no diretório `workflow-templates`. O arquivo de metadados precisa ter o mesmo nome do arquivo de fluxo de trabalho, mas, em vez da extensão `.yml`, é preciso acrescentar `.properties.json` a ele. Por exemplo, este arquivo chamado `octo-organization-ci.properties.json` contém os metadados para o arquivo de fluxo de trabalho chamado `octo-organization-ci.yml`:

            ```json copy
   {
       "name": "Octo Organization Workflow",
       "description": "Octo Organization CI workflow template.",
       "iconName": "example-icon",
       "categories": [
           "Go"
       ],
       "filePatterns": [
           "package.json$",
           "^Dockerfile",
           ".*\\.md$"
       ]
   }
   ```

   * `name`

   - **Obrigatório.** Nome do fluxo de trabalho. É exibido na lista de fluxos de trabalho disponíveis.

   * `description`

   - **Obrigatório.** Descrição do fluxo de trabalho. É exibido na lista de fluxos de trabalho disponíveis.

   * `iconName`

   - **Opcional**. Especifica um ícone para o fluxo de trabalho exibido na lista correspondente.
     `iconName` pode ser um dos seguintes tipos:
     * Um arquivo SVG armazenado no diretório de `workflow-templates`. Para fazer referência a um arquivo, o valor deve ser o nome do arquivo sem a extensão dele. Por exemplo, um arquivo SVG chamado `example-icon.svg` é referenciado como `example-icon`.
     * Um ícone do conjunto de [Octicons](https://primer.style/octicons/) do GitHub. Para fazer referência a um octicon, o valor dele deve ser `octicon <icon name>`. Por exemplo, `octicon smiley`.

   * `categories`

   - **Opcional**. Define as categorias em que o fluxo de trabalho é mostrado. Você pode usar nomes de categoria das seguintes listas:
     * Nomes de categorias gerais do repositório [starter-workflows](https://github.com/actions/starter-workflows/blob/main/README.md#categories).

     * Linguagens Linguist da lista de repositório em [linguist](https://github.com/github-linguist/linguist/blob/main/lib/linguist/languages.yml).

     * Pilhas de tecnologia com suporte da lista no repositório [starter-workflows](https://github.com/github-starter-workflows/repo-analysis-partner/blob/main/tech_stacks.yml).

   * `filePatterns`

   - **Opcional**. Permite que o modelo seja usado caso o repositório do usuário tenha um arquivo no diretório raiz que corresponda a uma expressão regular definida.

5. Para adicionar outro modelo de fluxo de trabalho, adicione seus arquivos ao mesmo diretório `workflow-templates`.

## Próximas etapas

* Para obter informações de referência sobre modelos de fluxo de trabalho, consulte [Reutilizando configurações de fluxo de trabalho](../../reference/workflows-and-actions/reusing-workflow-configurations.md#workflow-templates).
