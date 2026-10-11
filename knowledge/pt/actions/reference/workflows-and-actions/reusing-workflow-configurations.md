---
title: Reutilizando configurações de fluxo de trabalho
description: Encontre informações sobre como evitar a duplicação ao criar um fluxo de trabalho reutilizando fluxos de trabalho existentes e usando âncoras e aliases YAML.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/reusing-workflow-configurations
captured: '2026-10-11'
section: Reference / Workflows and actions
---

# Reutilizando configurações de fluxo de trabalho

_Encontre informações sobre como evitar a duplicação ao criar um fluxo de trabalho reutilizando fluxos de trabalho existentes e usando âncoras e aliases YAML._

## Fluxos de trabalho reutilizáveis

Este artigo fornece informações de referência para fluxos de trabalho reutilizáveis e modelos de fluxo de trabalho, incluindo regras de acesso, limitações, palavras-chave com suporte e comportamento do executor.

Você pode centralizar a lógica determinística e repetível em fluxos de trabalho reutilizáveis e usar agentic workflows para tarefas que exigem julgamento contextual sobre o conteúdo do repositório, como análise, resumos e recomendações. Para saber mais, confira [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

### Acesso a fluxos de trabalho reutilizáveis

Um fluxo de trabalho reutilizável pode ser usado por outro fluxo de trabalho se qualquer uma das seguintes opções for verdadeira:

* Ambos os fluxos de trabalho estão no mesmo repositório.
* O fluxo de trabalho chamado é armazenado em um repositórioe sua  empresarialpermite que você use fluxos de trabalho reutilizáveis públicos.
* O fluxo de trabalho chamado é armazenado em um repositório privado e as configurações desse repositório permitem que ele seja acessado. Para obter mais informações, consulte [Compartilhamento de ações e fluxos de trabalho com sua organização](../../how-tos/reuse-automations/share-with-your-organization.md) e [Compartilhamento de ações e fluxos de trabalho de seu repositório privado](../../how-tos/reuse-automations/share-across-private-repositories.md).

A tabela a seguir mostra a acessibilidade de fluxos de trabalho reutilizáveis a um fluxo de trabalho do chamador, dependendo da visibilidade do repositório do host.

| Repositório do chamador | Repositórios de fluxos de trabalho acessíveis |
|-----------------------|---------------------------------------------|
| `private`               |                                               |
| `private`               |                                               |
| e`public`               |                                               |
| `public`                | `public`                                      |

As **permissões de ações** na página de configurações de ações do repositório do chamador devem ser configuradas para permitir o uso de ações e fluxos de trabalho reutilizáveis; consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-select-actions-and-reusable-workflows-to-run).

Para privados, é necessário configurar explicitamente a política de **Acesso** na página de configurações de Ações do repositório do fluxo de trabalho chamado, permitindo o acesso por repositórios que contenham fluxos de trabalho de origem — consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-access-to-components-in-a-private-repository).

!!! note
    Para aprimorar a segurança, o GitHub Actions não dá suporte a redirecionamentos de ações nem a fluxos de trabalho reutilizáveis. Isso significa que quando o proprietário, o nome do repositório de uma ação ou o nome da ação é alterado, todos os fluxos de trabalho que usarem essa ação com o nome anterior falharão.

### Limitações de fluxos de trabalho reutilizáveis

* Você pode conectar até dez níveis de fluxos de trabalho. Para obter mais informações, confira [Aninhar fluxos de trabalho reutilizáveis](../../how-tos/reuse-automations/reuse-workflows.md#nesting-reusable-workflows).

* Você pode chamar até 50 fluxos de trabalho reutilizáveis exclusivos por meio de um só arquivo de fluxo de trabalho. Esse limite inclui árvores de fluxos de trabalho aninhados reutilizáveis que podem ser chamados começando do arquivo de fluxo de trabalho do chamador de nível superior.

  Por exemplo, *top-level-caller-workflow\.yml* → *called-workflow-1.yml* → *called-workflow-2.yml* conta como 2 fluxos de trabalho reutilizáveis.

* As variáveis de ambiente definidas em um contexto `env` definido no nível do fluxo de trabalho do chamador não são propagadas para o fluxo de trabalho chamado. Para saber mais, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md) e [Referência de contextos](contexts.md#env-context).

* Da mesma forma, as variáveis de ambiente definidas no contexto de `env`, definidas no fluxo de trabalho chamado, não são acessíveis no contexto do fluxo de trabalho do chamador `env`. Em vez disso, você deve usar saídas do fluxo de trabalho reutilizável. Para obter mais informações, consulte [Usando saídas de um fluxo de trabalho reutilizável](../../how-tos/reuse-automations/reuse-workflows.md#using-outputs-from-a-reusable-workflow).

* Para reutilizar variáveis em vários fluxos de trabalho, defina-as nos níveis da organização, do repositório ou do ambiente e faça referência a elas usando o contexto `vars`. Para saber mais, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md) e [Referência de contextos](contexts.md#vars-context).

* Fluxos de trabalho reutilizáveis são chamados diretamente dentro de um trabalho, e não de dentro de uma etapa de trabalho. Portanto, você não pode usar `GITHUB_ENV` para passar valores para as etapas de trabalho no fluxo de trabalho do chamador.

### Palavras-chave compatíveis com tarefas que utilizam um fluxo de trabalho reutilizável

Ao chamar um fluxo de trabalho reutilizável, você só poderá usar as palavras-chave a seguir no trabalho que contém a chamada:

* [`jobs.<job_id>.name`](workflow-syntax.md#jobsjob_idname)
* [`jobs.<job_id>.uses`](workflow-syntax.md#jobsjob_iduses)
* [`jobs.<job_id>.with`](workflow-syntax.md#jobsjob_idwith)
* [`jobs.<job_id>.with.<input_id>`](workflow-syntax.md#jobsjob_idwithinput_id)
* [`jobs.<job_id>.secrets`](workflow-syntax.md#jobsjob_idsecrets)
* [`jobs.<job_id>.secrets.<secret_id>`](workflow-syntax.md#jobsjob_idsecretssecret_id)
* [`jobs.<job_id>.secrets.inherit`](workflow-syntax.md#jobsjob_idsecretsinherit)
* [`jobs.<job_id>.strategy`](workflow-syntax.md#jobsjob_idstrategy)
* [`jobs.<job_id>.needs`](workflow-syntax.md#jobsjob_idneeds)
* [`jobs.<job_id>.if`](workflow-syntax.md#jobsjob_idif)
* [`jobs.<job_id>.concurrency`](workflow-syntax.md#jobsjob_idconcurrency)
* [`jobs.<job_id>.permissions`](workflow-syntax.md#jobsjob_idpermissions)
* [`jobs.<job_id>.cache-mode`](workflow-syntax.md#jobsjob_idcache-mode)

!!! note

  >
  > * Se `jobs.<job_id>.permissions` não for especificado no trabalho de chamada, o fluxo de trabalho chamado terá as permissões padrão para o `GITHUB_TOKEN`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#permissions).
  > * As permissões `GITHUB_TOKEN` transmitidas do fluxo de trabalho do chamador só podem ser rebaixadas (não elevadas) pelo fluxo de trabalho chamado.
  > * Se você usar `jobs.<job_id>.concurrency.cancel-in-progress: true`, não use o mesmo valor para `jobs.<job_id>.concurrency.group` nos fluxos de trabalho chamado e chamador, pois isso fará com que o fluxo de trabalho que já está em execução seja cancelado. Um fluxo de trabalho chamado utiliza o nome do fluxo de trabalho de origem em ${{ github.workflow }}, então, usar esse contexto como o valor de `jobs.<job_id>.concurrency.group` tanto no fluxo de trabalho de origem quanto no fluxo de trabalho chamado fará com que o fluxo de trabalho de origem seja cancelado quando o fluxo de trabalho chamado for executado.

### Como os fluxos de trabalho reutilizáveis usam executores

#### Executores hospedados em GitHub

A atribuição de executores hospedados em GitHub é sempre avaliada considerando apenas o contexto do chamador. A cobrança de executores hospedados em GitHub está sempre vinculada ao chamador. O fluxo de trabalho do chamador não pode utilizar executores hospedados em GitHub do repositório chamado. Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md).

#### Executores auto-hospedados

Fluxos de trabalho chamados que pertencem ao mesmo usuário, organização que o fluxo de trabalho do chamador podem acessar executores auto-hospedados a partir do contexto do chamador. Isso significa que um fluxo de trabalho chamado pode acessar executores auto-hospedados que estão:

* No repositório do chamador
* Na organização do repositório do chamador, desde que o executor tenha sido disponibilizado para esse repositório.

### Acesso e permissões para fluxos de trabalho aninhados

Um fluxo de trabalho que contém fluxos de trabalho aninhados reutilizáveis falhará se qualquer um dos fluxos de trabalho aninhados estiver inacessível ao fluxo de trabalho inicial do chamador. Para obter mais informações, confira "[Como acessar a fluxos de trabalho reutilizáveis](#access-to-reusable-workflows)".

As permissões `GITHUB_TOKEN` só podem ser as mesmas ou mais restritivas nos fluxos de trabalho aninhados. Por exemplo, na cadeia de fluxo de trabalho A > B > C, se o fluxo de trabalho A tiver permissão do token `package: read`, B e C não poderão ter a permissão `package: write`. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

Para obter informações sobre como usar a API para determinar quais arquivos de fluxo de trabalho estavam envolvidos em uma execução de fluxo de trabalho específica, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#monitoring-which-workflows-are-being-used).

### Comportamento de fluxos de trabalho reutilizáveis ao executar trabalhos novamente

Fluxos de trabalho reutilizáveis de repositórios públicos podem ser referenciados usando um SHA, uma tag de lançamento ou um nome de branch. Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#calling-a-reusable-workflow).

Quando você executa novamente um fluxo de trabalho que usa um fluxo de trabalho reutilizável e a referência não é um SHA, há alguns comportamentos a serem observados:

* A reexecução de todos os trabalhos em um fluxo de trabalho usará o fluxo de trabalho reutilizável da referência especificada. Para obter mais informações sobre como executar novamente todos os trabalhos em um fluxo de trabalho, confira [Reexecutando fluxos de trabalho e tarefas](../../how-tos/manage-workflow-runs/re-run-workflows-and-jobs.md#re-running-all-the-jobs-in-a-workflow).
* Executar novamente trabalhos com falha ou um trabalho específico em um fluxo de trabalho usará o fluxo de trabalho reutilizável do mesmo SHA do commit da primeira tentativa. Para obter mais informações sobre como executar novamente trabalhos com falha em um fluxo de trabalho, confira [Reexecutando fluxos de trabalho e tarefas](../../how-tos/manage-workflow-runs/re-run-workflows-and-jobs.md#re-running-failed-jobs-in-a-workflow). Para obter mais informações sobre como executar um trabalho específico em um fluxo de trabalho, confira [Reexecutando fluxos de trabalho e tarefas](../../how-tos/manage-workflow-runs/re-run-workflows-and-jobs.md#re-running-a-specific-job-in-a-workflow).

### Contexto `github`

Quando um fluxo de trabalho reutilizável é disparado por um fluxo de trabalho do chamador, o contexto `github` é sempre associado ao fluxo de trabalho do chamador. O fluxo de trabalho chamado recebe automaticamente o acesso a `github.token` e a `secrets.GITHUB_TOKEN`. Para saber mais sobre o contexto `github`, confira [Referência de contextos](contexts.md#github-context).

## Modelos de fluxo de trabalho

Informações de referência a serem usadas ao criar modelos de fluxo de trabalho para sua organização.

### Disponibilidade do modelo de fluxo de trabalho

Você pode usar modelos em repositórios que correspondem ou têm visibilidade mais restrita do que o repositório modelo.

* Modelos de fluxo de trabalho em um repositório público do `.github` estão disponíveis para todos os tipos de repositório.
* Modelos de fluxo de trabalho em um repositório interno do `.github` só estão disponíveis para repositórios internos e privados.
* Modelos de fluxo de trabalho em um repositório privado do `.github` só estão disponíveis para repositórios privados.

### Concedendo acesso a repositórios privados/internos

Se você estiver usando um repositório privado ou interno do `.github`, precisará conceder acesso de leitura aos usuários ou às equipes que deverão poder usar os modelos.

### O espaço reservado `$default-branch`

Se você precisar referir-se ao branch padrão de um repositório, pode usar o marcador de posição `$default-branch` em seu modelo de fluxo de trabalho. Quando um fluxo de trabalho é criado, o placeholder será automaticamente substituído pelo nome do branch padrão do repositório.

### Exemplo de arquivo de modelo de fluxo de trabalho

Este arquivo chamado `octo-organization-ci.yml` demonstra um fluxo de trabalho básico.

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

### Requisitos de arquivo de metadados

O arquivo de metadados precisa ter o mesmo nome do arquivo de fluxo de trabalho, mas, em vez da extensão `.yml`, é preciso acrescentar `.properties.json` a ele. Por exemplo, este arquivo chamado `octo-organization-ci.properties.json` contém os metadados para o arquivo de fluxo de trabalho chamado `octo-organization-ci.yml`:

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

## Âncoras e aliases YAML

Você pode usar âncoras e aliases YAML para reduzir a repetição nos fluxos de trabalho. Uma âncora (marcada com `&`) identifica uma parte do conteúdo que você deseja reutilizar, enquanto um alias (marcado com `*`) repete esse conteúdo em outro local.

Para obter informações detalhadas sobre âncoras e aliases, consulte [Aliases e âncoras do Node na especificação YAML](https://yaml.org/spec/1.2.2/#3222-anchors-and-aliases).

Veja um exemplo que usa âncoras e aliases YAML com variáveis de ambiente:

```yaml
jobs:
  job1:
    env: &env_vars # Define the anchor on first use
      NODE_ENV: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    steps:
      - run: echo "Using production settings"

  job2:
    env: *env_vars # Reuse the environment variables
    steps:
      - run: echo "Same environment variables here"
```

Isso é equivalente a escrever o seguinte YAML, sem âncoras e aliases:

```yaml
jobs:
  job1:
    env:
      NODE_ENV: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    steps:
      - run: echo "Using production settings"

  job2:
    env:
      NODE_ENV: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    steps:
      - run: echo "Same environment variables here"
```

Você também pode usar âncoras para configurações mais complexas, como a reutilização de uma configuração de trabalho inteira:

```yaml
jobs:
  test: &base_job # Define the anchor on first use
    runs-on: ubuntu-latest
    timeout-minutes: 30
    env:
      NODE_VERSION: '18'
    steps:
      - uses: actions/checkout@v6
      - name: Set up Node.js
        uses: actions/setup-node@v7
        with:
          node-version: ${{ env.NODE_VERSION }}
      - run: npm test

  alt-test: *base_job # Reuse the entire job configuration
```
