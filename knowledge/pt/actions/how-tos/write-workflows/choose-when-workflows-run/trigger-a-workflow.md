---
title: Acionando um fluxo de trabalho
description: Como disparar GitHub Actions fluxos de trabalho automaticamente
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
captured: '2026-10-11'
section: GitHub Actions
---

# Acionando um fluxo de trabalho

_Como disparar GitHub Actions fluxos de trabalho automaticamente_

## Pré-requisitos

Para saber mais sobre fluxos de trabalho e o disparo de fluxos de trabalho, confira [Fluxos de trabalho](../../../concepts/workflows-and-actions/workflows.md).

## Acionando um fluxo de trabalho a partir de um fluxo de trabalho

Quando você usa o `GITHUB_TOKEN` do repositório para executar tarefas, os eventos acionados pelo `GITHUB_TOKEN` não criarão uma nova execução de fluxo de trabalho, com as seguintes exceções:

* ```
            Eventos `workflow_dispatch` e `repository_dispatch` sempre criam execuções do fluxo de trabalho.
        ```
* ```
            Eventos `pull_request` com os tipos de atividade `opened`, `synchronize` ou `reopened`: quando um fluxo de trabalho que usa `GITHUB_TOKEN` cria ou atualiza uma pull request, o evento `pull_request` resultante cria execuções do fluxo de trabalho em um estado **aprovação-obrigatória**. O pull request exibe um banner na caixa de merge, e um usuário com acesso de escrita ao repositório pode iniciar as execuções selecionando **Aprovar fluxos de trabalho para execução**. Outros `pull_request` tipos de atividade (como `labeled`, `edited`ou `closed`) não criam execuções de fluxo de trabalho. Isso impede que o fluxo de trabalho recursivo seja executado enquanto ainda permite que os fluxos de trabalho de CI sejam executados em solicitações de pull criadas pela automação. Para obter mais informações sobre como aprovar execuções de fluxo de trabalho, consulte [AUTOTITLE](../../manage-workflow-runs/approve-runs-from-forks.md).
  ```

Para todos os outros eventos, esse comportamento impede que você crie acidentalmente execuções de fluxo de trabalho recursivo. Por exemplo, se uma execução de fluxo de trabalho efetuar push do código usando o `GITHUB_TOKEN` do repositório, um novo fluxo de trabalho não será executado mesmo quando o repositório contiver um fluxo de trabalho configurado para ser executado quando os eventos do `push` ocorrerem. Para obter mais informações, consulte [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](../../../tutorials/authenticate-with-github_token.md).

Se você quiser disparar um fluxo de trabalho de dentro de uma execução de fluxo de trabalho, poderá usar um GitHub App token de acesso de instalação ou um personal access token em vez de `GITHUB_TOKEN` para disparar eventos que exigem um token. Usar uma dessas alternativas também permite que os fluxos de trabalho sejam executados `pull_request` automaticamente (sem o prompt de aprovação descrito acima) quando a solicitação de pull é criada ou atualizada pela automação.

Se você usar um GitHub App, precisará criar um GitHub App e armazenar o ID do aplicativo e a chave privada como segredos. Para saber mais, confira [Fazer solicitações de API autenticadas com um aplicativo GitHub em um fluxo de trabalho GitHub Actions](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow). Se você usar um personal access token, precisará criar um personal access token e armazená-lo como um segredo. Para obter mais informações sobre como criar um personal access token, consulte [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens). Para saber mais sobre como armazenar segredos, confira [Usar segredos em ações do GitHub](../choose-what-workflows-do/use-secrets.md).

Para minimizar os GitHub Actions custos de uso, verifique se você não cria execuções de fluxo de trabalho recursivas ou não intencionais.

Por exemplo, o fluxo de trabalho a seguir usa um personal access token (armazenado como um segredo chamado `MY_TOKEN`) para adicionar um rótulo a um problema por meio de GitHub CLI. Todos os fluxos de trabalho que forem executados quando uma etiqueta é adicionada, serão executados assim que esta etapa for executada.

```yaml
on:
  issues:
    types:
      - opened

jobs:
  label_issue:
    runs-on: ubuntu-latest
    steps:
      - env:
          GH_TOKEN: ${{ secrets.MY_TOKEN }}
          ISSUE_URL: ${{ github.event.issue.html_url }}
        run: |
          gh issue edit $ISSUE_URL --add-label "triage"
```

Por outro lado, o fluxo de trabalho a seguir usa `GITHUB_TOKEN` para adicionar um rótulo a um problema. Ele não acionará nenhum fluxo de trabalho executado quando uma etiqueta é adicionada.

```yaml
on:
  issues:
    types:
      - opened

jobs:
  label_issue:
    runs-on: ubuntu-latest
    steps:
      - env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ISSUE_URL: ${{ github.event.issue.html_url }}
        run: |
          gh issue edit $ISSUE_URL --add-label "triage"
```

## Usando eventos para acionar fluxos de trabalho

Use a chave `on` para especificar os eventos que disparam o fluxo de trabalho. Para obter mais informações sobre os eventos que podem ser usados, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md).

### Usando um evento único

Por exemplo, um fluxo de trabalho com o seguinte valor `on` será executado quando um push for feito em qualquer branch no repositório do fluxo de trabalho:

```yaml
on: push
```

### Usando eventos múltiplos

É possível especificar um único evento ou vários eventos. Por exemplo, um fluxo de trabalho com o valor `on` a seguir será executado quando um push for feito em qualquer branch no repositório ou quando alguém criar um fork do repositório:

```yaml
on: [push, fork]
```

Se você especificar vários eventos, apenas um desses eventos deverá ocorrer para acionar seu fluxo de trabalho. Se vários eventos de acionamento para o seu fluxo de trabalho ocorrerem ao mesmo tempo, várias execuções de fluxo de trabalho serão acionadas.

### Usando tipos de atividade e filtros com vários eventos

É possível usar tipos de atividade e filtros para controlar ainda mais quando o fluxo de trabalho será executado. Para obter mais informações, confira [Como usar tipos de atividade de evento](#using-event-activity-types) e [Como usar filtros](#using-filters). Se você especificar tipos de atividade ou filtros para um evento e seu fluxo de trabalho for acionado em vários eventos, você deverá configurar cada evento separadamente. Você deve acrescentar dois-pontos (`:`) a todos os eventos, incluindo eventos sem configuração.

Por exemplo, um fluxo de trabalho com o seguinte valor `on` será executado quando:

* Uma etiqueta foi criada
* Um push for feito para o branch `main` no repositório
* Um push é feito para um branch habilitado para GitHub Pages

```yaml
on:
  label:
    types:
      - created
  push:
    branches:
      - main
  page_build:
```

## Usando tipos de atividade do evento

Alguns eventos têm tipos de atividade que oferecem mais controle sobre quando o fluxo de trabalho deve ser executado. Use `on.<event_name>.types` para definir o tipo de atividade de evento que vai disparar uma execução de fluxo de trabalho.

Por exemplo, o evento `issue_comment` tem os tipos de atividades `created`, `edited` e `deleted`. Se o seu fluxo de trabalho for acionado pelo evento `label`, ele será executado sempre que uma etiqueta for criada, editada ou excluída. Se você especificar o tipo de atividade `created` para o evento `label`, o fluxo de trabalho será executado quando um rótulo for criado, mas não quando um rótulo for editado ou excluído.

```yaml
on:
  label:
    types:
      - created
```

Se você especificar vários tipos de atividades, apenas um desses tipos de atividade deverá ocorrer para acionar o fluxo de trabalho. Se vários tipos de atividade do evento de acionamento ocorrer em seu fluxo de trabalho ao mesmo tempo, várias execuções de fluxo de trabalho serão acionadas. Por exemplo, o fluxo de trabalho a seguir é acionado quando um problema é aberto ou rotulado. Se um problema com duas etiquetas for aberta, serão iniciadas três execuções de fluxos de trabalho: uma para o problema aberto e duas para os dois problemas etiquetados.

```yaml
on:
  issues:
    types:
      - opened
      - labeled
```

Para obter mais informações sobre cada evento e os respectivos tipos de atividade, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md).

## Usando filtros

Alguns eventos têm filtros que dão mais controle sobre quando seu fluxo de trabalho deve ser executado.

Por exemplo, o evento `push` tem um filtro `branches` que faz com que seu fluxo de trabalho seja executado somente quando ocorrer um push para um branch que corresponde ao filtro `branches`, em vez de quando ocorrer qualquer push.

```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
```

### Usando filtros para focar em branches específicos para eventos de pull request

Ao usar os eventos `pull_request` e `pull_request_target`, você pode configurar um fluxo de trabalho para ser executado somente para solicitações de pull direcionadas a branches específicos.

Use o filtro `branches` quando quiser incluir padrões de nomes de branches ou quando quiser incluir e excluir padrões de nomes de branches. Use o filtro `branches-ignore` quando quiser excluir apenas padrões de nomes de branches. Não é possível usar os filtros `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho.

Se você definir `branches`/`branches-ignore` e [`paths`/`paths-ignore`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore), o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `branches` e `branches-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, faça escape de cada um desses caracteres especiais com ``. Para saber mais sobre padrões glob, confira o [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet).

#### Exemplo: Incluindo ramificações

Os padrões definidos em `branches` são avaliados em relação ao nome da referência do Git. Por exemplo, o seguinte fluxo de trabalho será executado sempre que houver um evento `pull_request` para uma solicitação de pull direcionada a:

* Uma ramificação chamada `main` (`refs/heads/main`)
* Uma ramificação chamada `mona/octocat` (`refs/heads/mona/octocat`)
* Um branch cujo nome começa com `releases/`, como `releases/10` (`refs/heads/releases/10`)

```yaml
on:
  pull_request:
    # Sequence of patterns matched against refs/heads
    branches:
      - main
      - 'mona/octocat'
      - 'releases/**'
```

Se um fluxo de trabalho for ignorado devido à filtragem de ramificação, à [filtragem de caminho](../../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore) ou a uma [mensagem de confirmação](../../manage-workflow-runs/skip-workflow-runs.md), as verificações associadas a esse fluxo de trabalho permanecerão no estado "Pendente". Uma solicitação de pull que exige que essas verificações sejam bem-sucedidas não poderá ser mesclada.

#### Exemplo: Excluir branches

Quando um padrão corresponder ao padrão `branches-ignore`, o fluxo de trabalho não será executado. Os padrões definidos em `branches-ignore` são avaliados em relação ao nome da referência do Git. Por exemplo, o seguinte fluxo de trabalho será executado sempre que houver um evento `pull_request`, a menos que a solicitação de pull seja direcionada a:

* Um branch chamado `mona/octocat` (`refs/heads/mona/octocat`)
* Um branch cujo nome corresponde a `releases/**-alpha`, como `releases/beta/3-alpha` (`refs/heads/releases/beta/3-alpha`) <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  pull_request:
    # Sequence of patterns matched against refs/heads
    branches-ignore:
      - 'mona/octocat'
      - 'releases/**-alpha'
```

#### Exemplo: Incluindo e excluindo branches

Não é possível usar `branches` e `branches-ignore` para filtrar o mesmo evento em um só fluxo de trabalho. Caso deseje incluir e excluir padrões de branch para um só evento, use o filtro `branches` com o caractere `!` para indicar os branches que devem ser excluídos.

Se você definir um branch com o caractere `!`, também precisará definir, pelo menos, um branch sem o caractere `!`. Caso deseje apenas excluir os branches, use `branches-ignore`.

A ordem na qual você define os padrões é importante.

* Um padrão de correspondência negativa (precedido por `!`) após uma correspondência positiva excluirá a referência do Git.
* Um padrão positivo correspondente após uma correspondência negativa incluirá a Git ref novamente.

O fluxo de trabalho a seguir será executado em eventos `pull_request` para solicitações de pull direcionadas a `releases/10` ou `releases/beta/mona`, mas não para solicitações de pull direcionadas a `releases/10-alpha` ou `releases/beta/3-alpha`, porque o padrão `!releases/**-alpha` negativo segue o padrão positivo. <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  pull_request:
    branches:
      - 'releases/**'
      - '!releases/**-alpha'
```

### Usando filtros para destinar eventos de push a branches ou tags específicas

Ao usar o evento `push`, você pode configurar um fluxo de trabalho para ser executado em marcas ou em branches específicos.

Use o filtro `branches` quando quiser incluir padrões de nomes de branches ou quando quiser incluir e excluir padrões de nomes de branches. Use o filtro `branches-ignore` quando quiser excluir apenas padrões de nomes de branches. Não é possível usar os filtros `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho.

Use o filtro `tags` quando quiser incluir padrões de nomes de marcas ou quando quiser incluir e excluir padrões de nomes de marcas. Use o filtro `tags-ignore` quando quiser excluir apenas padrões de nomes de marcas. Não é possível usar os filtros `tags` e `tags-ignore` para o mesmo evento em um fluxo de trabalho.

Se você definir apenas `tags`/`tags-ignore` or apenas `branches`/`branches-ignore`, o fluxo de trabalho não será executado para eventos que afetam o Git ref indefinido. Se você não definir `tags`/`tags-ignore` nem `branches`/`branches-ignore`, o fluxo de trabalho será executado para eventos que afetam seus branches ou rótulos. Se você definir `branches`/`branches-ignore` e [`paths`/`paths-ignore`](../../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore), o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `branches`, `branches-ignore`, `tags` e `tags-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de marca ou de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, *faça escape* de cada um desses caracteres especiais com ``. Para obter mais informações sobre padrões glob, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet).

#### Exemplo: Incluindo ramificações e etiquetas

Os padrões definidos em `branches` e `tags` são avaliados em relação ao nome de referência do Git. Por exemplo, o seguinte fluxo de trabalho será executado sempre que houver um evento `push` para:

* Um branch chamado `main` (`refs/heads/main`)
* Um branch chamado `mona/octocat` (`refs/heads/mona/octocat`)
* Um branch cujo nome começa com `releases/`, como `releases/10` (`refs/heads/releases/10`)
* Uma marca chamada `v2` (`refs/tags/v2`)
* Uma marca cujo nome começa com `v1.`, como `v1.9.1` (`refs/tags/v1.9.1`)

```yaml
on:
  push:
    # Sequence of patterns matched against refs/heads
    branches:
      - main
      - 'mona/octocat'
      - 'releases/**'
    # Sequence of patterns matched against refs/tags
    tags:
      - v2
      - v1.*
```

#### Exemplo: Excluindo branches e tags

Quando um padrão corresponder ao padrão `branches-ignore` ou `tags-ignore`, o fluxo de trabalho não será executado. Os padrões definidos em `branches` e `tags` são avaliados em relação ao nome de referência do Git. Por exemplo, o seguinte fluxo de trabalho será executado sempre que houver um evento `push`, a menos que o evento `push` seja para:

* Um branch chamado `mona/octocat` (`refs/heads/mona/octocat`)
* Um branch cujo nome corresponde a `releases/**-alpha`, como `releases/beta/3-alpha` (`refs/heads/releases/beta/3-alpha`) <!-- markdownlint-disable-line outdated-release-phase-terminology -->
* Uma marca chamada `v2` (`refs/tags/v2`)
* Uma marca cujo nome começa com `v1.`, como `v1.9` (`refs/tags/v1.9`)

```yaml
on:
  push:
    # Sequence of patterns matched against refs/heads
    branches-ignore:
      - 'mona/octocat'
      - 'releases/**-alpha'
    # Sequence of patterns matched against refs/tags
    tags-ignore:
      - v2
      - v1.*
```

#### Exemplo: Incluindo e excluindo branches e tags

Não é possível usar `branches` e `branches-ignore` para filtrar o mesmo evento em um fluxo de trabalho individual. Da mesma forma, não é possível usar `tags` e `tags-ignore` para filtrar o mesmo evento em um fluxo de trabalho individual. Caso deseje incluir e excluir padrões de branch para um evento individual, use o filtro `branches` ou `tags` com o caractere `!` para indicar as marcas ou os branches que devem ser excluídos.

Se você definir um branch com o caractere `!`, também precisará definir, pelo menos, um branch sem o caractere `!`. Caso deseje apenas excluir os branches, use `branches-ignore`. Da mesma forma, se você definir uma marca com o caractere `!`, também precisará definir, pelo menos, uma marca sem o caractere `!`. Caso deseje apenas excluir as marcas, use `tags-ignore`.

A ordem na qual você define os padrões é importante.

* Um padrão de correspondência negativa (precedido por `!`) após uma correspondência positiva excluirá a referência do Git.
* Um padrão positivo correspondente após uma correspondência negativa incluirá a Git ref novamente.

O fluxo de trabalho a seguir será executado em pushes para `releases/10` ou `releases/beta/mona`, mas não em `releases/10-alpha` ou `releases/beta/3-alpha` porque o padrão `!releases/**-alpha` negativo vem após o padrão positivo. <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  push:
    branches:
      - 'releases/**'
      - '!releases/**-alpha'
```

### Usando filtros para especificar caminhos específicos para eventos de pull request ou de push

Ao usar os eventos `push` e `pull_request`, você pode configurar um fluxo de trabalho para ser executado com base nos caminhos de arquivo alterados. Os filtros de caminho não são avaliados em envios de tags.

Use o filtro `paths` quando quiser incluir padrões de caminho de arquivo ou quando quiser incluir e excluir padrões de caminho de arquivo. Use o filtro `paths-ignore` quando quiser apenas excluir padrões de caminho de arquivo. Não é possível usar os filtros `paths` e `paths-ignore` para o mesmo evento em um fluxo de trabalho. Caso deseje incluir e excluir padrões de caminho para um evento individual, use o filtro `paths` prefixado o caractere `!` para indicar os caminhos que devem ser excluídos.

> \[!NOTE]
> A ordem de definição dos padrões `paths` é importante:
>
> * Um padrão negativo correspondente (prefixado com `!`) após uma correspondência positiva excluirá o caminho.
> * Um padrão positivo correspondente após uma correspondência negativa incluirá o caminho novamente.

Se você definir `branches`/`branches-ignore` e `paths`/`paths-ignore`, o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `paths` e `paths-ignore` aceitam padrões glob que usam os caracteres curinga `*` e `**` para fazer a correspondência com mais de um nome de caminho. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet).

#### Exemplo: Incluindo caminhos

Se, pelo menos, um caminho corresponder a um padrão no filtro `paths`, o fluxo de trabalho será executado. Por exemplo, o fluxo de trabalho a seguir será executado sempre que você efetuar push de um arquivo JavaScript (`.js`).

```yaml
on:
  push:
    paths:
      - '**.js'
```

Se um fluxo de trabalho for ignorado devido à filtragem de caminho, [à filtragem de ramificação](../../../reference/workflows-and-actions/workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore) ou a uma [mensagem de confirmação](../../manage-workflow-runs/skip-workflow-runs.md), as verificações associadas a esse fluxo de trabalho permanecerão no estado "Pendente". Uma solicitação de pull que exige que essas verificações sejam bem-sucedidas não poderá ser mesclada.

#### Exemplo: Excluindo caminhos

Quando todos os nomes de caminho corresponderem aos padrões de `paths-ignore`, o fluxo de trabalho não será executado. Se qualquer nome de caminho não corresponder aos padrões de `paths-ignore`, mesmo que alguns nomes de caminho correspondam aos padrões, o fluxo de trabalho será executado.

Um fluxo de trabalho com o filtro de caminho a seguir só será executado em eventos `push` que incluem, pelo menos, um arquivo fora do diretório `docs` na raiz do repositório.

```yaml
on:
  push:
    paths-ignore:
      - 'docs/**'
```

#### Exemplo: Incluindo e excluindo caminhos

Não é possível usar `paths` e `paths-ignore` para filtrar o mesmo evento em um só fluxo de trabalho. Caso deseje incluir e excluir padrões de caminho para um evento individual, use o filtro `paths` prefixado o caractere `!` para indicar os caminhos que devem ser excluídos.

Se você definir um caminho com o caractere `!`, também precisará definir, pelo menos, um caminho sem o caractere `!`. Caso você deseje apenas excluir os caminhos, use `paths-ignore`.

A ordem de definição dos padrões `paths` é importante:

* Um padrão de correspondência negativa (precedido por `!`) após uma correspondência positiva excluirá o caminho do Git.
* Um padrão positivo correspondente após uma correspondência negativa incluirá o caminho novamente.

Este exemplo é executado sempre que o evento `push` inclui um arquivo no diretório `sub-project` ou nos respectivos subdiretórios, a menos que o arquivo esteja no diretório `sub-project/docs`. Por exemplo, um push que alterar `sub-project/index.js` ou `sub-project/src/index.js` vai disparar uma execução de fluxo de trabalho, mas um push que só altera `sub-project/docs/readme.md` não.

```yaml
on:
  push:
    paths:
      - 'sub-project/**'
      - '!sub-project/docs/**'
```

#### Comparações de Git diff

O filtro determina se um fluxo de trabalho deve ser executado avaliando os arquivos alterados e executando-os na lista `paths-ignore` ou `paths`. Se não houver arquivos alterados, o fluxo de trabalho não será executado.

GitHub gera a lista de arquivos alterados usando diferenças de dois pontos para pushes e diferenças de três pontos para pull requests:

* **Pull requests:** as comparações de três pontos são uma comparação entre a versão mais recente da ramificação do tópico e a confirmação em que a ramificação do tópico foi sincronizado pela última vez com a ramificação base.
* **Pushes ramificações existentes:** uma comparação de dois pontos compara os SHAs principal e base diretamente um com o outro.
* **Pushes para novas ramificações:** uma comparação de dois pontos com o pai do ancestral da confirmação mais profunda enviada por push.

Em algumas situações, GitHub Actions aplica limites que alteram a forma como os fluxos de trabalho filtrados são executados:

* Se um push contiver mais de 1.000 confirmações, o fluxo de trabalho **sempre** será executado.
* Se a geração da diferença atingir o tempo limite, o fluxo de trabalho **sempre** será executado.
* Se o diff gerado contiver mais de 3,000 arquivos e os arquivos aos quais o filtro do fluxo de trabalho se aplica não estiverem entre os primeiros 3,000 retornados pelo filtro, o fluxo de trabalho **não** será executado.

Se você observar esses comportamentos, talvez seja necessário tornar seus filtros mais específicos ou mudar a forma como você trabalha com pushes e pull requests para gerar diffs mais simples.

Para saber mais, confira [Branches](https://docs.github.com/pt/pull-requests/reference/branches).

### Usando filtros para direcionar branches específicos para eventos de execução de fluxo de trabalho

Ao usar o evento `workflow_run`, você pode especificar em quais ramificações o fluxo de trabalho acionador deve ser executado para acionar seu fluxo de trabalho.

Os filtros `branches` e `branches-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, *faça escape* de cada um desses caracteres especiais com ``. Para saber mais sobre padrões glob, confira o [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet).

Por exemplo, um fluxo de trabalho com o seguinte gatilho só será executado quando o fluxo de trabalho chamado `Build` for executado em um branch cujo nome começa com `releases/`:

```yaml
on:
  workflow_run:
    workflows: ["Build"]
    types: [requested]
    branches:
      - 'releases/**'
```

Um fluxo de trabalho com o seguinte gatilho só será executado quando o fluxo de trabalho chamado `Build` for executado em um branch que não seja chamado `canary`:

```yaml
on:
  workflow_run:
    workflows: ["Build"]
    types: [requested]
    branches-ignore:
      - "canary"
```

Não é possível usar os filtros `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho. Caso deseje incluir e excluir padrões de branch para um só evento, use o filtro `branches` com o caractere `!` para indicar os branches que devem ser excluídos.

A ordem na qual você define os padrões é importante.

* Um padrão negativo correspondente (prefixado com `!`), após uma correspondência positiva, excluirá a ramificação.
* Um padrão positivo correspondente após uma correspondência negativa incluirá o branch novamente.

Por exemplo, um fluxo de trabalho com o gatilho a seguir será executado quando o fluxo de trabalho chamado `Build` for executado em uma ramificação chamada `releases/10` ou `releases/beta/mona`, mas não `releases/10-alpha`, `releases/beta/3-alpha` ou `main`. <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  workflow_run:
    workflows: ["Build"]
    types: [requested]
    branches:
      - 'releases/**'
      - '!releases/**-alpha'
```

## Definindo entradas para fluxos de trabalho acionados manualmente

Ao usar o evento `workflow_dispatch`, opcionalmente, você pode especificar as entradas que são transmitidas para o fluxo de trabalho.

Esse gatilho só recebe eventos quando o arquivo de fluxo de trabalho está na ramificação padrão.
O fluxo de trabalho disparado recebe os dados de entrada no contexto `inputs`. Para obter mais informações, confira [Contextos](../../../reference/workflows-and-actions/contexts.md#inputs-context).

> \[!NOTE]
>
> * O fluxo de trabalho também receberá as entradas no contexto de `github.event.inputs`. As informações no contexto `inputs` e no contexto `github.event.inputs` são idênticas, exceto que o contexto `inputs` preserva valores boolianos como boolianos em vez de convertê-los em cadeias de caracteres. O tipo `choice` é resolvido para uma cadeia de caracteres e é uma única opção selecionável.
> * O número máximo de propriedades de nível superior é `inputs` 25 .
> * O conteúdo máximo para `inputs` é de 65.535 caracteres.

```yaml
on:
  workflow_dispatch:
    inputs:
      logLevel:
        description: 'Log level'
        required: true
        default: 'warning'
        type: choice
        options:
          - info
          - warning
          - debug
      print_tags:
        description: 'True to print to STDOUT'
        required: true
        type: boolean
      tags:
        description: 'Test scenario tags'
        required: true
        type: string
      environment:
        description: 'Environment to run tests against'
        type: environment
        required: true

jobs:
  print-tag:
    runs-on: ubuntu-latest
    if: ${{ inputs.print_tags }}
    steps:
      - name: Print the input tag to STDOUT
        run: echo  The tags are ${{ inputs.tags }}
```

## Definindo entradas, saídas e segredos para fluxos de trabalho reutilizáveis

É possível definir entradas e segredos que um fluxo de trabalho reutilizável deve receber de um fluxo de trabalho chamado. Também é possível especificar saídas que um fluxo de trabalho reutilizável disponibilizará para um fluxo de trabalho chamado. Para saber mais, confira [Reutilizar fluxos de trabalho](../../reuse-automations/reuse-workflows.md).

## Usando informações do evento

As informações sobre o evento que disparou uma execução de fluxo de trabalho estão disponíveis no contexto `github.event`. As propriedades no contexto `github.event` dependem do tipo de evento que disparou o fluxo de trabalho. Por exemplo, um fluxo de trabalho acionado quando um problema está etiquetado teria informações sobre o problema e a etiqueta.

### Visualizando todas as propriedades de um evento

Consulte a documentação sobre eventos de webhook para propriedades comuns e exemplos de cargas. Para saber mais, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads).

Imprima também o contexto `github.event` inteiro para ver quais propriedades estão disponíveis para o evento que disparou seu fluxo de trabalho:

```yaml
jobs:
  print_context:
    runs-on: ubuntu-latest
    steps:
      - env:
          EVENT_CONTEXT: ${{ toJSON(github.event) }}
        run: |
          echo $EVENT_CONTEXT
```

### Acessando e usando as propriedades do evento

Use o contexto `github.event` no fluxo de trabalho. Por exemplo, o fluxo de trabalho a seguir é executado quando uma solicitação de pull que altera `package*.json`, `.github/CODEOWNERS` ou `.github/workflows/**` é aberta. Se o autor do pull request (`github.event.pull_request.user.login`) não for `octobot` nem `dependabot[bot]`, o fluxo de trabalho usará o GitHub CLI para rotular e comentar no pull request (`github.event.pull_request.number`).

```yaml
on:
  pull_request:
    types:
      - opened
    paths:
      - '.github/workflows/**'
      - '.github/CODEOWNERS'
      - 'package*.json'

jobs:
  triage:
    if: >-
      github.event.pull_request.user.login != 'octobot' &&
      github.event.pull_request.user.login != 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: "Comment about changes we can't accept"
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR: ${{ github.event.pull_request.html_url }}
        run: |
          gh pr edit $PR --add-label 'invalid'
          gh pr comment $PR --body 'It looks like you edited `package*.json`, `.github/CODEOWNERS`, or `.github/workflows/**`. We do not allow contributions to these files. Please review our [contributing guidelines](https://github.com/octo-org/octo-repo/blob/main/CONTRIBUTING.md) for what contributions are accepted.'
```

Para obter mais informações sobre contextos, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md). Para obter mais informações sobre payloads de eventos, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads).

## Controlando ainda mais como seu fluxo de trabalho será executado

Se você quiser um controle mais granular do que o fornecido por eventos, tipos de atividade do evento ou filtros de evento, use condicionais e ambientes para controlar se trabalhos ou etapas individuais serão executados no fluxo de trabalho.

### Usando condicionais

Você pode usar condicionais para controlar ainda mais se os trabalhos ou etapas no seu fluxo de trabalho serão executados.

#### Exemplo de uso de um valor na carga do evento

Por exemplo, caso você deseje que o fluxo de trabalho seja executado quando um rótulo específico for adicionado a um problema, dispare o tipo de atividade do evento `issues labeled` e use um condicional para verificar qual rótulo disparou o fluxo de trabalho. O fluxo de trabalho a seguir será executado quando qualquer rótulo for adicionado a um problema no repositório do fluxo de trabalho, mas o trabalho `run_if_label_matches` só será executado se o rótulo for chamado `bug`.

```yaml
on:
  issues:
    types:
      - labeled

jobs:
  run_if_label_matches:
    if: github.event.label.name == 'bug'
    runs-on: ubuntu-latest
    steps:
      - run: echo 'The label was bug'
```

#### Exemplo de uso do tipo de evento

Por exemplo, se você deseja executar diferentes tarefas ou etapas, dependendo de qual evento acionou o fluxo de trabalho, você poderá usar uma condicional para verificar se um tipo de evento específico existe no contexto do evento. O fluxo de trabalho seguinte será executado sempre que um problema ou pull request for fechado. Se o fluxo de trabalho tiver sido executado porque um problema foi fechado, o contexto `github.event` conterá um valor para `issue`, mas não para `pull_request`. Portanto, a etapa `if_issue` será executada, mas a etapa `if_pr` não. Por outro lado, se o fluxo de trabalho for executado porque uma solicitação de pull foi fechada, a etapa `if_pr` será executada, mas a etapa `if_issue` não será executada.

```yaml
on:
  issues:
    types:
      - closed
  pull_request:
    types:
      - closed

jobs:
  state_event_type:
    runs-on: ubuntu-latest
    steps:
    - name: if_issue
      if: github.event.issue
      run: |
        echo An issue was closed
    - name: if_pr
      if: github.event.pull_request
      run: |
        echo A pull request was closed
```

Para obter mais informações sobre as informações que estão disponíveis no contexto do evento, confira [Como usar as informações do evento](#using-event-information). Para obter mais informações sobre como usar condicionais, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md).

### Usando ambientes para acionar trabalhos de fluxo de trabalho manualmente

Se você quiser acionar manualmente uma tarefa específica em um fluxo de trabalho, você pode usar um ambiente que exige a aprovação de uma equipe ou usuário específico. Primeiro, configure um ambiente com os revisores necessários. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md). Em seguida, referencie o nome do ambiente em um trabalho no fluxo de trabalho usando a chave `environment:`. Qualquer trabalho que faz referência ao ambiente não será executado até que pelo menos um revisor aprove o trabalho.

Por exemplo, o seguinte fluxo de trabalho será executado sempre que houver um push para o principal. O trabalho `build` sempre será executado. O trabalho `publish` só será executado depois que o trabalho `build` for concluído com sucesso (devido a `needs: [build]`) e depois de todas as regras (incluindo os revisores obrigatórios) para o ambiente chamado `production` forem aprovadas (devido a `environment: production`).

```yaml
on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: build
        run: |
          echo 'building'

  publish:
    needs: [build]
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: publish
        run: |
          echo 'publishing'
```

> \[!NOTE]
> Ambientes, segredos de ambiente e regras de proteção para implantações estão disponíveis em repositórios públicos para todos os planos atuais GitHub . Eles não estão disponíveis em planos antigos, como Bronze, Prata ou Ouro. Para acesso a ambientes, segredos de ambiente e ramificações de implantação em repositórios privados ou internos, você deve usar GitHub Pro, GitHub Team, ou GitHub Enterprise.
> Se você estiver em um GitHub Free, GitHub Proou GitHub Team plano, outras regras de proteção de implantação, como um temporizador de espera ou revisores necessários, só estarão disponíveis para repositórios públicos.

## Eventos disponíveis

Para obter uma lista completa de eventos disponíveis, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md).
