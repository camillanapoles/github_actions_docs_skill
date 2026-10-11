---
title: Sintaxe de fluxo de trabalho para o GitHub Actions
description: Um fluxo de trabalho é um processo automatizado configurável constituído de um ou mais trabalhos. Você deve criar um arquivo YAML para definir a configuração do seu fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/workflow-syntax
captured: '2026-10-11'
section: Reference / Workflows and actions
---

# Sintaxe de fluxo de trabalho para o GitHub Actions

_Um fluxo de trabalho é um processo automatizado configurável constituído de um ou mais trabalhos. Você deve criar um arquivo YAML para definir a configuração do seu fluxo de trabalho._

## Sobre sintaxe YAML para fluxos de trabalho

Os arquivos de fluxo de trabalho usam a sintaxe YAML e precisam ter uma extensão de arquivo `.yml` ou `.yaml`. Se você não estiver familiarizado com o YAML e quiser saber mais, confira [Aprenda a usar o YAML em Y minutos](https://learnxinyminutes.com/docs/yaml/).

Você precisa armazenar os arquivos de fluxo de trabalho no diretório `.github/workflows` do repositório.

!!! tip
    Ao contrário dos fluxos de trabalho tradicionais GitHub Actions, que exigem que você codifique cada decisão como etapas de tarefa no YAML, GitHub Agentic Workflows usam front matter em YAML para acionadores e configuração, mas permitem que você descreva o que deseja em Markdown com linguagem natural — para que não precise prever e codificar todos os cenários com antecedência. Para saber mais, confira [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

## `name`

Nome do fluxo de trabalho. O GitHub exibe os nomes dos fluxos de trabalho na guia "Ações" do repositório. Se você omitir `name`, o GitHub exibirá o caminho do arquivo de fluxo de trabalho em relação à raiz do repositório.

## `run-name`

O nome das execuções de fluxo de trabalho geradas pelo fluxo de trabalho.
GitHub exibe o nome da execução do fluxo de trabalho na lista de execuções de fluxo de trabalho na guia "Ações" do repositório. Se `run-name` for omitido ou for apenas espaço em branco, o nome da execução será definido como informações específicas do evento para a execução do fluxo de trabalho. Por exemplo, para um fluxo de trabalho disparado por um evento `push` ou `pull_request`, ele é definido como a mensagem do commit ou o título da pull request.

Esse valor pode incluir expressões e referenciar os contextos [`github`](contexts.md#github-context) e [`inputs`](contexts.md#inputs-context).

### Exemplo de `run-name`

```yaml
run-name: Deploy to ${{ inputs.deploy_target }} by @${{ github.actor }}
```

## `on`

Para disparar automaticamente um fluxo de trabalho, use `on` para definir os eventos que podem fazer com que o fluxo de trabalho seja executado. Para obter uma lista de eventos disponíveis, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md).

Você pode definir um ou vários eventos que possam disparar um fluxo de trabalho ou definir um cronograma. Também é possível restringir a execução de um fluxo de trabalho para que ocorra apenas para arquivos, tags ou alterações em branches específicos. Essas opções são descritas nas seções a seguir.

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

### Usando tipos de atividade

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

Para obter mais informações sobre cada evento e os respectivos tipos de atividade, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md).

### Usando filtros

Alguns eventos têm filtros que dão mais controle sobre quando seu fluxo de trabalho deve ser executado.

Por exemplo, o evento `push` tem um filtro `branches` que faz com que seu fluxo de trabalho seja executado somente quando ocorrer um push para um branch que corresponde ao filtro `branches`, em vez de quando ocorrer qualquer push.

```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
```

### Usando tipos de atividade e filtros com vários eventos

Se você especificar tipos de atividade ou filtros para um evento e seu fluxo de trabalho for acionado em vários eventos, você deverá configurar cada evento separadamente. Você deve acrescentar dois-pontos (`:`) a todos os eventos, incluindo eventos sem configuração.

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

## `on.<event_name>.types`

Use `on.<event_name>.types` para definir o tipo de atividade que vai disparar uma execução de fluxo de trabalho. A maioria dos eventos GitHub são acionados por mais de um tipo de atividade. Por exemplo, o `label` é disparado quando um rótulo é `created`, `edited` ou `deleted`. A palavra-chave `types` permite restringir a atividade que faz com que o fluxo de trabalho seja executado. Quando apenas um tipo de atividade dispara um evento de webhook, a palavra-chave `types` é desnecessária.

Você pode usar uma matriz de eventos `types`. Para obter mais informações sobre cada evento e seus tipos de atividade, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md).

```yaml
on:
  label:
    types: [created, edited]
```

## `on.<pull_request|pull_request_target>.<branches|branches-ignore>`

Ao usar os eventos `pull_request` e `pull_request_target`, você pode configurar um fluxo de trabalho para ser executado somente para solicitações de pull direcionadas a branches específicos.

Use o filtro `branches` quando quiser incluir padrões de nomes de branches ou quando quiser incluir e excluir padrões de nomes de branches. Use o filtro `branches-ignore` quando quiser excluir apenas padrões de nomes de branches. Não é possível usar os filtros `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho.

Se você definir `branches`/`branches-ignore` e [`paths`/`paths-ignore`](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore), o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `branches` e `branches-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, faça escape de cada um desses caracteres especiais com ``. Para saber mais sobre padrões glob, confira o [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#filter-pattern-cheat-sheet).

### Exemplo: Incluindo branches

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

Se um fluxo de trabalho for ignorado devido à filtragem de ramificação, à [filtragem de caminho](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore) ou a uma [mensagem de confirmação](../../how-tos/manage-workflow-runs/skip-workflow-runs.md), as verificações associadas a esse fluxo de trabalho permanecerão no estado "Pendente". Uma solicitação de pull que exige que essas verificações sejam bem-sucedidas não poderá ser mesclada.

### Exemplo: Excluir branches

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

### Exemplo: Incluindo e excluindo branches

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

## `on.merge_group.<branches|branches-ignore>`

Ao usar o evento `merge_group`, você pode configurar um fluxo de trabalho para ser executado apenas para grupos de mesclagem que tenham como destino ramificações específicas.

Use o filtro `branches` quando quiser incluir padrões de nome de ramificação ou quando quiser tanto incluir quanto excluir padrões de nome de ramificação. Use `branches-ignore` quando quiser excluir apenas padrões de nomes de branch. Você não pode usar ambos `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho.

Os filtros `branches` e `branches-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, faça escape de cada um desses caracteres especiais com ``. Para obter mais informações sobre padrões glob, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](https://docs.github.com/pt/actions/using-workflows/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet).

### Exemplo: Incluindo branches

Os padrões definidos em `branches` são avaliados em relação ao nome do branch de destino. Por exemplo, o fluxo de trabalho a seguir será executado sempre que houver um evento `merge_group` para um grupo de merge que tem como destino:

* Uma ramificação chamada `main`
* Uma ramificação cujo nome começa com `releases/`

```yaml
on:
  merge_group:
    types: [checks_requested]
    branches:
      - main
      - 'releases/**'
```

### Exemplo: Excluir branches

Quando um padrão corresponder ao padrão `branches-ignore`, o fluxo de trabalho não será executado. Os padrões definidos em `branches-ignore` são avaliados em relação ao nome do branch de destino. Por exemplo, o seguinte fluxo de trabalho será executado sempre que ocorrer um evento `merge_group`, a menos que os alvos do grupo de mesclagem:

* Uma ramificação chamada `canary`
* Um ramo cujo nome corresponde a `releases/**-alpha`, como `releases/beta/3-alpha` <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  merge_group:
    types: [checks_requested]
    branches-ignore:
      - canary
      - 'releases/**-alpha'
```

### Exemplo: Incluindo e excluindo branches

Não é possível usar `branches` e `branches-ignore` para filtrar o mesmo evento em um só fluxo de trabalho. Caso deseje incluir e excluir padrões de branch para um só evento, use o filtro `branches` com o caractere `!` para indicar os branches que devem ser excluídos.

Se você definir um branch com o caractere `!`, também precisará definir, pelo menos, um branch sem o caractere `!`. Se você quiser apenas excluir as ramificações, use `branches-ignore`.

A ordem na qual você define os padrões é importante.

* Um padrão negativo correspondente (prefixado com `!`), após uma correspondência positiva, excluirá a ramificação.
* Um padrão positivo correspondente após uma correspondência negativa incluirá o branch novamente.

O fluxo de trabalho a seguir será executado em eventos `merge_group` para grupos de merge que têm como destino `releases/10` ou `releases/beta/mona`, mas não para grupos de merge que têm como destino `releases/10-alpha` ou `releases/beta/3-alpha`, porque o padrão negativo `!releases/**-alpha` vem depois do padrão positivo. <!-- markdownlint-disable-line outdated-release-phase-terminology -->

```yaml
on:
  merge_group:
    types: [checks_requested]
    branches:
      - 'releases/**'
      - '!releases/**-alpha'
```

## `on.push.<branches|tags|branches-ignore|tags-ignore>`

Ao usar o evento `push`, você pode configurar um fluxo de trabalho para ser executado em marcas ou em branches específicos.

Use o filtro `branches` quando quiser incluir padrões de nomes de branches ou quando quiser incluir e excluir padrões de nomes de branches. Use o filtro `branches-ignore` quando quiser excluir apenas padrões de nomes de branches. Não é possível usar os filtros `branches` e `branches-ignore` para o mesmo evento em um fluxo de trabalho.

Use o filtro `tags` quando quiser incluir padrões de nomes de marcas ou quando quiser incluir e excluir padrões de nomes de marcas. Use o filtro `tags-ignore` quando quiser excluir apenas padrões de nomes de marcas. Não é possível usar os filtros `tags` e `tags-ignore` para o mesmo evento em um fluxo de trabalho.

Se você definir apenas `tags`/`tags-ignore` or apenas `branches`/`branches-ignore`, o fluxo de trabalho não será executado para eventos que afetam o Git ref indefinido. Se você não definir `tags`/`tags-ignore` nem `branches`/`branches-ignore`, o fluxo de trabalho será executado para eventos que afetam seus branches ou rótulos. Se você definir `branches`/`branches-ignore` e [`paths`/`paths-ignore`](workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore), o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `branches`, `branches-ignore`, `tags` e `tags-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de marca ou de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, *faça escape* de cada um desses caracteres especiais com ``. Para obter mais informações sobre padrões glob, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#filter-pattern-cheat-sheet).

### Exemplo: Incluindo branches e tags

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

### Exemplo: Excluindo branches e tags

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

### Exemplo: Incluindo e excluindo branches e tags

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

## `on.<push|pull_request|pull_request_target>.<paths|paths-ignore>`

Ao usar os eventos `push` e `pull_request`, você pode configurar um fluxo de trabalho para ser executado com base nos caminhos de arquivo alterados. Os filtros de caminho não são avaliados em envios de tags.

Use o filtro `paths` quando quiser incluir padrões de caminho de arquivo ou quando quiser incluir e excluir padrões de caminho de arquivo. Use o filtro `paths-ignore` quando quiser apenas excluir padrões de caminho de arquivo. Não é possível usar os filtros `paths` e `paths-ignore` para o mesmo evento em um fluxo de trabalho. Caso deseje incluir e excluir padrões de caminho para um evento individual, use o filtro `paths` prefixado o caractere `!` para indicar os caminhos que devem ser excluídos.

!!! note
    A ordem de definição dos padrões `paths` é importante:

    * Um padrão negativo correspondente (prefixado com `!`) após uma correspondência positiva excluirá o caminho.
    * Um padrão positivo correspondente após uma correspondência negativa incluirá o caminho novamente.

Se você definir `branches`/`branches-ignore` e `paths`/`paths-ignore`, o fluxo de trabalho só será executado quando ambos os filtros forem atendidos.

As palavras-chave `paths` e `paths-ignore` aceitam padrões glob que usam os caracteres curinga `*` e `**` para fazer a correspondência com mais de um nome de caminho. Para obter mais informações, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#filter-pattern-cheat-sheet).

### Exemplo: Incluindo caminhos

Se, pelo menos, um caminho corresponder a um padrão no filtro `paths`, o fluxo de trabalho será executado. Por exemplo, o fluxo de trabalho a seguir será executado sempre que você efetuar push de um arquivo JavaScript (`.js`).

```yaml
on:
  push:
    paths:
      - '**.js'
```

Se um fluxo de trabalho for ignorado devido à filtragem de caminho, [à filtragem de ramificação](workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore) ou a uma [mensagem de confirmação](../../how-tos/manage-workflow-runs/skip-workflow-runs.md), as verificações associadas a esse fluxo de trabalho permanecerão no estado "Pendente". Uma solicitação de pull que exige que essas verificações sejam bem-sucedidas não poderá ser mesclada.

### Exemplo: Excluindo caminhos

Quando todos os nomes de caminho corresponderem aos padrões de `paths-ignore`, o fluxo de trabalho não será executado. Se qualquer nome de caminho não corresponder aos padrões de `paths-ignore`, mesmo que alguns nomes de caminho correspondam aos padrões, o fluxo de trabalho será executado.

Um fluxo de trabalho com o filtro de caminho a seguir só será executado em eventos `push` que incluem, pelo menos, um arquivo fora do diretório `docs` na raiz do repositório.

```yaml
on:
  push:
    paths-ignore:
      - 'docs/**'
```

### Exemplo: Incluindo e excluindo caminhos

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

### Comparações Git diff

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

## `on.schedule`

Use `on.schedule` para definir um agendamento de tempo para seus fluxos de trabalho.

Use a [sintaxe cron POSIX](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07) para agendar fluxos de trabalho para serem executados em horários específicos.
Por padrão, fluxos de trabalho agendados são executados em UTC. Opcionalmente, você pode especificar um fuso horário usando uma cadeia de [caracteres de fuso horário IANA](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) para agendamento. Fluxos de trabalho agendados são executados sobre o último commit no branch padrão. O intervalo mais curto que você pode executar fluxos de trabalho agendados é a cada 5 minutos.

!!! note
    Para agendamentos que definem `timezone` em um fuso horário que observa o horário de verão, durante as transições de adiantamento do horário de verão, fluxos de trabalho agendados durante as horas não contabilizadas avançam para o próximo horário válido. Por exemplo, um horário agendado para as 2h30 avança para as 3h00.

A sintaxe cron tem cinco campos separados por um espaço, e cada campo representa uma unidade de tempo.

```text
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12 or JAN-DEC)
│ │ │ │ ┌───────────── day of the week (0 - 6 or SUN-SAT)
│ │ │ │ │
* * * * *
```

Você pode usar estes operadores em qualquer um dos cinco campos:

| Operador | Descrição | Exemplo |
| --- | --- | --- |
| \* | Qualquer valor |  |
| `15 * * * *` é executado no minuto 15 de cada hora todos os dias. |  |  |
| , | Separador de valores em lista |  |
| `2,10 4,5 * * *` é executado nos minutos 2 e 10 da quarta e da quinta hora todos os dias. |  |  |
| - | Intervalo de valores |  |
| `30 4-6 * * *` é executado no minuto 30 da 4ª, 5ª e 6ª hora. |  |  |
| / | Valores de etapa |  |
| `20/15 * * * *` é executado a cada 15 minutos, começando do minuto 20 ao 59 (minutos 20, 35 e 50). |  | Este exemplo inicia o fluxo de trabalho para ser executado às 5h30, no fuso horário América/New_York, de segunda a sexta-feira. |
```yaml
on:
  schedule:
    - cron: '30 5 * * 1-5'
      timezone: "America/New_York"
```

Um fluxo de trabalho individual pode ser disparado por vários eventos `schedule`. Acesse o evento `schedule` que disparou o fluxo de trabalho por meio do contexto `github.event.schedule`. Este exemplo dispara o fluxo de trabalho para ser executado às 5:30 UTC toda segunda-feira a quinta-feira e às 17:30 UTC às terças e quintas-feiras, mas ignora a etapa `Not on Monday or Wednesday` na segunda-feira e na quarta-feira.

```yaml
on:
  schedule:
    - cron: '30 5 * * 1,3'
    - cron: '30 5,17 * * 2,4'

jobs:
  test_schedule:
    runs-on: ubuntu-latest
    steps:
      - name: Not on Monday or Wednesday
        if: github.event.schedule != '30 5 * * 1,3'
        run: echo "This step will be skipped on Monday and Wednesday"
      - name: Every time
        run: echo "This step will always run"
```

Para saber mais sobre eventos `schedule`, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md#schedule).

## `on.workflow_call`

Use `on.workflow_call` para definir as entradas e as saídas de um fluxo de trabalho reutilizável. Você também pode mapear os segredos disponíveis para o fluxo de trabalho chamado. Para obter mais informações sobre os fluxos de trabalho reutilizáveis, consulte [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

## `on.workflow_call.inputs`

Ao usar a palavra-chave `workflow_call`, você poderá, opcionalmente, especificar as entradas que são transmitidas para o fluxo de trabalho chamado do fluxo de trabalho de chamada. Para obter mais informações sobre a palavra-chave `workflow_call`, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md#workflow_call).

Além dos parâmetros de entrada padrão disponíveis, `on.workflow_call.inputs` exige um parâmetro `type`. Para obter mais informações, consulte [`on.workflow_call.inputs.<input_id>.type`](#onworkflow_callinputsinput_idtype).

Se um parâmetro `default` não estiver definido, o valor padrão da entrada será `false` para um booliano, `0` para um número e `""` para uma cadeia de caracteres.

No fluxo de trabalho chamado, você pode usar o contexto `inputs` para se referir a uma entrada. Para saber mais, confira [Referência de contextos](contexts.md#inputs-context).

Se um fluxo de trabalho de chamada passar uma entrada que não é especificada no fluxo de trabalho de chamada, isso irá gerar um erro.

### Exemplo de `on.workflow_call.inputs`

```yaml
on:
  workflow_call:
    inputs:
      username:
        description: 'A username passed from the caller workflow'
        default: 'john-doe'
        required: false
        type: string

jobs:
  print-username:
    runs-on: ubuntu-latest

    steps:
      - name: Print the input name to STDOUT
        run: echo The username is ${{ inputs.username }}
```

Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

## `on.workflow_call.inputs.<input_id>.type`

Obrigatório se a entrada for definida para a palavra-chave `on.workflow_call`. O valor deste parâmetro é uma string que especifica o tipo de dados da entrada. Precisa ser `boolean`, `number` ou `string`.

## `on.workflow_call.outputs`

Um mapa de saídas para um fluxo de trabalho chamado. As saídas de fluxo de trabalho chamadas estão disponíveis para todas as tarefas a jusante no fluxo de trabalho de chamadas. Cada saída tem um identificador, uma `description,` opcional e um `value.`. O `value` precisa ser definido como o valor de uma saída de um trabalho no fluxo de trabalho chamado.

No exemplo abaixo, duas saídas são definidas para esse fluxo de trabalho reutilizável: `workflow_output1` e `workflow_output2`. Elas são mapeadas para as saídas chamadas `job_output1` e `job_output2`, ambas de um trabalho chamado `my_job`.

### Exemplo de `on.workflow_call.outputs`

```yaml
on:
  workflow_call:
    # Map the workflow outputs to job outputs
    outputs:
      workflow_output1:
        description: "The first job output"
        value: ${{ jobs.my_job.outputs.job_output1 }}
      workflow_output2:
        description: "The second job output"
        value: ${{ jobs.my_job.outputs.job_output2 }}
```

Para obter informações sobre como referenciar uma saída de trabalho, consulte [`jobs.<job_id>.outputs`](#jobsjob_idoutputs). Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

## `on.workflow_call.secrets`

Um mapa dos segredos que pode ser usado no fluxo de trabalho de chamada.

No fluxo de trabalho chamado, você pode usar o contexto `secrets` para se referir a um segredo.

!!! note
    Nota: se você estiver passando o segredo para um fluxo de trabalho aninhado reutilizável, deverá usar [`jobs.<job_id>.secrets`](#jobsjob_idsecrets) novamente para passar o segredo. Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#passing-secrets-to-nested-workflows).

Se um fluxo de trabalho de chamada passar um segredo que não é especificado no fluxo de trabalho chamado, isso irá gerar um erro.

### Exemplo de `on.workflow_call.secrets`

```yaml
on:
  workflow_call:
    secrets:
      access-token:
        description: 'A token passed from the caller workflow'
        required: false

jobs:

  pass-secret-to-action:
    runs-on: ubuntu-latest
    steps:
    # passing the secret to an action
      - name: Pass the received secret to an action
        uses: ./.github/actions/my-action
        with:
          token: ${{ secrets.access-token }}

  # passing the secret to a nested reusable workflow
  pass-secret-to-workflow:
    uses: ./.github/workflows/my-workflow
    secrets:
       token: ${{ secrets.access-token }}
```

## `on.workflow_call.secrets.<secret_id>`

Um identificador de string para associar ao segredo.

## `on.workflow_call.secrets.<secret_id>.required`

Um booleano que especifica se o segredo deve ser fornecido.

## `on.workflow_run.<branches|branches-ignore>`

Ao usar o evento `workflow_run`, você pode especificar em quais ramificações o fluxo de trabalho acionador deve ser executado para acionar seu fluxo de trabalho.

Os filtros `branches` e `branches-ignore` aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `?`, `!` e outros para corresponder a mais de um nome de branch. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, *faça escape* de cada um desses caracteres especiais com ``. Para saber mais sobre padrões glob, confira o [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#filter-pattern-cheat-sheet).

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

## `on.workflow_run.workflows`

Ao usar o `workflow_run` evento, você pode especificar quais fluxos de trabalho podem disparar seu fluxo de trabalho.

Os `workflows` filtros aceitam padrões glob que usam caracteres como `*`, `**`, `+`, `!`, `?` e outros para corresponder a mais de um nome do workflow. Se um nome contiver um desses caracteres e você quiser ter uma correspondência literal, *faça escape* de cada um desses caracteres especiais com ``. Para obter mais informações sobre padrões glob, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](https://docs.github.com/pt/actions/writing-workflows/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet).

Por exemplo, um fluxo de trabalho com o seguinte gatilho só será executado quando o fluxo de trabalho nomeado `Build` for executado:

```yaml
on:
  workflow_run:
    workflows: ["Build"]
    types: [requested]
```

Um fluxo de trabalho com o gatilho a seguir só será executado quando um fluxo de trabalho cujo nome começa com `Build` for concluído:

```yaml
on:
  workflow_run:
    workflows: ["Build*"]
    types: [completed]
```

Um fluxo de trabalho com o seguinte gatilho só será executado quando o fluxo de trabalho nomeado `Build C++` for concluído:

```yaml
on:
  workflow_run:
    workflows: ["Build C\\+\\+"]
    types: [completed]
```

## `on.workflow_dispatch`

Ao usar o evento `workflow_dispatch`, opcionalmente, você pode especificar as entradas que são transmitidas para o fluxo de trabalho.

Esse gatilho só recebe eventos quando o arquivo de fluxo de trabalho está na ramificação padrão.

## `on.workflow_dispatch.inputs`

O fluxo de trabalho disparado recebe os dados de entrada no contexto `inputs`. Para obter mais informações, confira [Contextos](contexts.md#inputs-context).

!!! note
    * O fluxo de trabalho também receberá as entradas no contexto de `github.event.inputs`. As informações no contexto `inputs` e no contexto `github.event.inputs` são idênticas, exceto que o contexto `inputs` preserva valores boolianos como boolianos em vez de convertê-los em cadeias de caracteres. O tipo `choice` é resolvido para uma cadeia de caracteres e é uma única opção selecionável.
    * O número máximo de propriedades de nível superior é `inputs` 25 .
    * O conteúdo máximo para `inputs` é de 65.535 caracteres.

### Exemplo de `on.workflow_dispatch.inputs`

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

## `on.workflow_dispatch.inputs.<input_id>.required`

Um booliano que especifica se a entrada precisa ser fornecida.

## `on.workflow_dispatch.inputs.<input_id>.type`

O valor deste parâmetro é uma string que especifica o tipo de dados da entrada. Precisa ser `boolean`, `choice`, `number`, `environment` ou `string`.

## `permissions`

Use `permissions` para modificar as permissões padrão concedidas ao `GITHUB_TOKEN`, adicionando ou removendo o acesso conforme necessário, de modo que você só permita o acesso mínimo necessário. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).

Use `permissions` como uma chave de nível superior a ser aplicada a todos os trabalhos no fluxo de trabalho ou em trabalhos específicos. Quando você adiciona a chave `permissions` a um trabalho específico, todas as ações e os comandos de execução nesse trabalho que usam o `GITHUB_TOKEN` obtêm os direitos de acesso especificados. Para obter mais informações, consulte [`jobs.<job_id>.permissions`](workflow-syntax.md#jobsjob_idpermissions).

Os proprietários de uma organização podem restringir o acesso de escrita para o `GITHUB_TOKEN` no nível do repositório. Para obter mais informações, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#setting-the-permissions-of-the-github_token-for-your-organization).

Quando um fluxo de trabalho é disparado pelo evento [`pull_request_target`](events-that-trigger-workflows.md#pull_request_target), recebe permissão `GITHUB_TOKEN` de repositório de leitura/gravação, mesmo quando é disparado de uma bifurcação pública. Para saber mais, confira [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md#pull_request_target).

Para cada uma das permissões disponíveis mostradas na tabela abaixo, você pode atribuir um dos níveis de acesso: `read` (se aplicável), `write` ou `none`.
`write` inclui `read`. Se você especificar o acesso para qualquer uma dessas permissões, todas aquelas que não forem especificadas serão definidas como `none`.

Permissões disponíveis e detalhes do que cada uma permite que uma ação faça:

| Permissão | Permite uma ação que usa `GITHUB_TOKEN` para |
| --- | --- |
| `actions` | Trabalhar com GitHub Actions. Por exemplo, `actions: write` permite que uma ação cancele uma execução de fluxo de trabalho. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-actions). |
| `artifact-metadata` | Trabalhe com metadados de artefatos. Por exemplo, `artifact-metadata: write` permite que uma ação crie registros de armazenamento em nome de um artefato de build. Para obter mais informações, confira [Pontos de extremidade de API REST para metadados de artefato](https://docs.github.com/pt/rest/orgs/artifact-metadata). |
| `attestations` | Trabalhar com atestados de artefatos. Por exemplo, `attestations: write` permite que uma ação gere um atestado de artefato para uma criação. Para obter mais informações, confira [Usar atestados de artefatos para estabelecer a procedência de compilações](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md) |
| `checks` | Trabalhar com verificação de execuções e verificação de conjuntos. Por exemplo, `checks: write` permite que uma ação crie uma verificação de execução. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-checks). |
| `code-quality` | Trabalhe com qualidade de código. Por exemplo, `code-quality: write` permite que uma ação carregue relatórios de cobertura de código. Para obter mais informações, confira [Qualidade do Código do GitHub](https://docs.github.com/pt/code-security/concepts/code-quality/code-quality). |
| `contents` | Trabalhar com o conteúdo do repositório. Por exemplo, `contents: read` permite que uma ação liste os commits e `contents: write` permite que a ação crie uma versão. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-contents). |
| `deployments` | Trabalhar com implantações. Por exemplo, `deployments: write` permite que uma ação crie uma implantação. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-deployments). |
| `discussions` | Trabalhar com discussões do GitHub. Por exemplo, `discussions: write` permite que uma ação feche ou exclua uma discussão. Para obter mais informações, confira [Usar a API do GraphQL para discussões](https://docs.github.com/pt/graphql/guides/using-the-graphql-api-for-discussions). |
| `id-token` | Recuperar um token OpenID Connect (OIDC). Isso exige usar `id-token: write`. Para obter mais informações, confira [OpenID Connect](../../concepts/security/openid-connect.md#updating-your-workflows-for-oidc) |
| `issues` | Trabalhar com problemas. Por exemplo, `issues: write` permite que uma ação adicione um comentário a um problema. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-issues). |
| `packages` | Trabalhar com GitHub Packages. Por exemplo, `packages: write` permite que uma ação carregue e publique pacotes no GitHub Packages. Para obter mais informações, confira [Sobre permissões para o GitHub Packages](https://docs.github.com/pt/packages/learn-github-packages/about-permissions-for-github-packages#about-scopes-and-permissions-for-package-registries). |
| `pages` | Trabalhar com páginas do GitHub. Por exemplo, `pages: write` permite que uma ação solicite um build de GitHub Pages. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-pages). |
| `pull-requests` | Trabalhar com solicitações de pull. Por exemplo, `pull-requests: write` permite que uma ação adicione um rótulo a uma PR. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-pull-requests). |
| `security-events` | Trabalhar com alertas de verificação de código do GitHub. Por exemplo, `security-events: read` permite que uma ação liste os alertas da digitalização de código para o repositório e `security-events: write` permite que uma ação atualize o status de um alerta de digitalização de código. Para obter mais informações, consulte [as permissões do Repositório para "Alertas de verificação de código"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-code-scanning-alerts). <br><br> |
| Para alertas do Dependabot, use a permissão `vulnerability-alerts`. Os alertas de verificação secreta não podem ser lidos com essa permissão e exigem um aplicativo GitHub ou um personal access token. Para obter mais informações, consulte [Permissões de Repositório para "Alertas de verificação de segredos"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-secret-scanning-alerts) em "Permissões necessárias para aplicativos GitHub". |  |
| `statuses` | Trabalhar com status de commits. Por exemplo, `statuses:read` permite que uma ação liste os status de commit de uma determinada referência. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-commit-statuses). |
| `vulnerability-alerts` | Leia os alertas do Dependabot. Por exemplo, `vulnerability-alerts: read` permite que uma ação liste os alertas do Dependabot para o repositório. Somente `read` e `none` há suporte; `write` não é válido. Quando `write-all` ou `read-all` é usado, `vulnerability-alerts` é incluído automaticamente como `read`. Para obter mais informações, consulte [as permissões do Repositório para "Alertas do Dependabot"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-dependabot-alerts). |

### Definindo o acesso para os escopos do `GITHUB_TOKEN`

Você pode definir o acesso que o `GITHUB_TOKEN` permitirá especificando `read`, `write` ou `none` como o valor das permissões disponíveis na chave `permissions`.

```yaml
permissions:
  actions: read|write|none
  artifact-metadata: read|write|none
  attestations: read|write|none
  checks: read|write|none
  code-quality: read|write|none
  contents: read|write|none
  deployments: read|write|none
  id-token: write|none
  issues: read|write|none
  discussions: read|write|none
  packages: read|write|none
  pages: read|write|none
  pull-requests: read|write|none

  security-events: read|write|none
  statuses: read|write|none
  vulnerability-alerts: read|none
```

Se você especificar o acesso para uma dessas permissões, todas aquelas que não forem especificadas serão definidas como `none`.

Você pode usar a sintaxe a seguir para definir o acesso de `read-all` ou `write-all` para todas as permissões disponíveis:

```yaml
permissions: read-all
```

```yaml
permissions: write-all
```

Você pode usar a seguinte sintaxe para desabilitar as permissões para todas as permissões disponíveis:

```yaml
permissions: {}
```

#### Alterar as permissões em um repositório bifurcado

Você pode usar a tecla `permissions` para adicionar e remover permissões de leitura de repositórios derivados (forks), mas normalmente não pode conceder acesso de gravação. A exceção a esse comportamento ocorre quando um usuário administrador seleciona a opção **Enviar tokens de gravação para fluxos de trabalho a partir de pull requests** nas GitHub Actions configurações. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

### Como as permissões são calculadas para um trabalho de fluxo de trabalho

Inicialmente, as permissões para o `GITHUB_TOKEN` são definidas como a configuração padrão para a empresa, a organização ou o repositório. Se o padrão for definido como permissões restritas em qualquer um desses níveis, isso irá aplicar-se aos repositórios relevantes. Por exemplo, Se você escolher o padrão restrito no nível da organização, todos os repositórios nessa organização usarão as permissões restritas como padrão. As permissões serão, então, ajustadas com base em qualquer configuração dentro do arquivo de fluxo de trabalho, primeiro no nível de fluxo de trabalho e, em seguida, no nível de trabalho. Por fim, se o fluxo de trabalho foi disparado por um evento de solicitação pull que não seja `pull_request_target` de um repositório com fork e a configuração **Enviar tokens de gravação para fluxos de trabalho por meio de solicitações pull** não está selecionada, as permissões são ajustadas para alterar as permissões de gravação para somente leitura.

### Definir as permissões do `GITHUB_TOKEN` para todos os trabalhos em um fluxo de trabalho

Você pode especificar `permissions` no nível superior de um fluxo de trabalho para que a configuração se aplique a todos os trabalhos no fluxo de trabalho.

#### Exemplo: definir as permissões do `GITHUB_TOKEN` para um fluxo de trabalho inteiro

Este exemplo mostra as permissões que estão sendo definidas para o `GITHUB_TOKEN` que se aplicará a todos os trabalhos no fluxo de trabalho. É concedido acesso de leitura a todas as permissões.

```yaml
name: "My workflow"

on: [ push ]

permissions: read-all

jobs:
  ...
```

### Como usar a chave `permissions` para repositórios bifurcados

Além disso, você pode usar a chave `permissions` para adicionar e remover permissões de `read` para repositórios com fork, mas normalmente não pode permitir acesso de `write`. A exceção a esse comportamento é quando um usuário administrador selecionou a opção **Enviar tokens de gravação para fluxos de trabalho de solicitações pull** nas configurações do GitHub Actions. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

### Permissões para execuções de fluxo de trabalho disparadas por Dependabot

As execuções de fluxo de trabalho disparadas por solicitações de pull Dependabot são executadas como se fossem de um repositório bifurcado e, portanto, usam `GITHUB_TOKEN` somente leitura. Estas execuções de fluxo de trabalho não podem acessar nenhum segredo. Para obter mais informações sobre as estratégias para manter esses fluxos de trabalho seguros, confira [Referência de uso seguro](../security/secure-use.md).

## `env`

Um `map` das variáveis que estão disponíveis para as etapas de todos os trabalhos do fluxo de trabalho. Também é possível definir variáveis que estão disponíveis apenas para as etapas de um trabalho ou para uma só etapa. Para obter mais informações, consulte [`jobs.<job_id>.env`](#jobsjob_idenv) e [`jobs.<job_id>.steps[*].env`](#jobsjob_idstepsenv).

As variáveis no mapa `env` não podem ser definidas em termos de outras variáveis no mapa.

Quando mais de uma variável de ambiente é definida com o mesmo nome, GitHub usa a variável mais específica. Por exemplo, uma variável de ambiente definida em uma etapa substituirá as variáveis de ambiente do trabalho e do fluxo de trabalho que tenham o mesmo nome enquanto a etapa é executada. Uma variável de ambiente definida para um trabalho substituirá uma variável de fluxo de trabalho com o mesmo nome enquanto o trabalho é executado.

### Exemplo de `env`

```yaml
env:
  SERVER: production
```

## `defaults`

Use `defaults` para criar um `map` com as configurações padrão que se aplicarão a todas as tarefas do fluxo de trabalho. Você também pode definir configurações padrão que estão disponíveis apenas para uma tarefa. Para obter mais informações, confira [`jobs.<job_id>.defaults`](workflow-syntax.md#jobsjob_iddefaults).

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `defaults.run`

Você pode usar `defaults.run` para fornecer as opções `shell` e `working-directory` padrão para todas as etapas do [`run`](workflow-syntax.md#jobsjob_idstepsrun) em um fluxo de trabalho. Você também pode definir configurações padrão para `run` as quais só estão disponíveis para um trabalho. Para obter mais informações, confira [`jobs.<job_id>.defaults.run`](workflow-syntax.md#jobsjob_iddefaultsrun). Você não pode usar contextos ou expressões nesta palavra-chave.

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

### Exemplo: Defina o shell padrão e o diretório de trabalho

```yaml
defaults:
  run:
    shell: bash
    working-directory: ./scripts
```

## `defaults.run.shell`

Use `shell` para definir o `shell` para uma etapa. Essa palavra-chave pode fazer referência a vários contextos. Para obter mais informações, confira [Contextos](contexts.md#context-availability).

| Plataforma compatível | Parâmetro `shell` | Descrição | Comando executado internamente |
| --- | --- | --- | --- |
| Linux / macOS | não especificado | O shell padrão em plataformas não Windows. Isso executa um comando diferente para quando `bash` é especificado explicitamente. Se `bash` não for encontrado no caminho, isso será tratado como `sh`. | `bash -e {0}` |
| Tudo | `bash` | O shell padrão em plataformas não Windows com um fallback para `sh`. Ao especificar um shell bash no Windows, é utilizado o shell bash incluído no Git para Windows. | `bash --noprofile --norc -eo pipefail {0}` |
| Tudo | `pwsh` | Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `pwsh -command ". '{0}'"` |
| Tudo | `python` | Executa o comando python. | `python {0}` |
| Linux / macOS | `sh` | O comportamento de fallback para plataformas não Windows se nenhum shell for fornecido e o `bash` não for encontrado no caminho. | `sh -e {0}` |
| Windows | `cmd` | O GitHub acrescenta a extensão `.cmd` ao nome do script e a substitui por `{0}`. | `%ComSpec% /D /E:ON /V:OFF /S /C "CALL "{0}""`. |
| Windows | `pwsh` | Essa é a shell padrão usada no Windows. Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. Se o executor auto-hospedado do Windows não tiver o *PowerShell Core* instalado, o *PowerShell Desktop* será usado. | `pwsh -command ". '{0}'"`. |
| Windows | `powershell` | O PowerShell Desktop. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `powershell -command ". '{0}'"`. |

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `defaults.run.working-directory`

Use `working-directory` para definir o diretório de trabalho do `shell` de uma etapa. Essa palavra-chave pode fazer referência a vários contextos. Para obter mais informações, confira [Contextos](contexts.md#context-availability).

!!! tip
    Verifique se o `working-directory` existe no executor antes de executar seu shell nele.
    Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `concurrency`

Use `concurrency` para garantir que apenas um trabalho ou um fluxo de trabalho que usa o mesmo grupo de simultaneidade seja executado por vez. Um grupo de concorrência pode ser qualquer string ou expressão. A expressão só pode usar os contextos [`github`](contexts.md#github-context), [`inputs`](contexts.md#inputs-context) e [`vars`](contexts.md#vars-context). Para obter mais informações sobre expressões, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

Você também pode especificar `concurrency` no nível do trabalho. Para obter mais informações, confira [`jobs.<job_id>.concurrency`](workflow-syntax.md#jobsjob_idconcurrency).

Isso significa que pode haver no máximo um trabalho ou fluxo de trabalho em execução em um grupo de concorrência a qualquer momento. Quando um trabalho ou um fluxo de trabalho simultâneo é colocado na fila, se outro trabalho ou fluxo de trabalho que usa o mesmo grupo de simultaneidade no repositório estiver em andamento, o trabalho ou o fluxo de trabalho na fila ficará `pending`. Por padrão, qualquer trabalho ou fluxo de trabalho existente `pending` no mesmo grupo de simultaneidade será cancelado e o novo trabalho ou fluxo de trabalho em fila tomará seu lugar.

Para também cancelar qualquer trabalho ou fluxo de trabalho em execução no mesmo grupo de concorrência, especifique `cancel-in-progress: true`. Para cancelar condicionalmente trabalhos ou fluxos de trabalho em execução no mesmo grupo de simultaneidade, é possível especificar `cancel-in-progress` como uma expressão com qualquer um dos contextos de expressão permitidos.

Para permitir que mais de uma tarefa ou execução de fluxo de trabalho aguardem no mesmo grupo de simultaneidade, use a propriedade opcional `queue`. A `queue` propriedade aceita os seguintes valores:

* `single` (padrão): no máximo uma execução de tarefa ou de fluxo de trabalho pode ser `pending` no grupo de simultaneidade. Quando uma nova execução de trabalho ou fluxo de trabalho é enfileirada, qualquer execução existente de trabalho ou fluxo de trabalho `pending` no mesmo grupo é cancelada e substituída.
* `max`: até 100 trabalhos ou execuções de fluxo de trabalho podem ser incluídos no grupo de simultaneidade. Quando a fila estiver cheia, quaisquer trabalhos adicionais ou execuções de fluxo de trabalho serão cancelados.

A combinação de `queue: max` e `cancel-in-progress: true` não é permitida e resultará em um erro de validação de fluxo de trabalho.

!!! note
    * O nome do grupo de simultaneidade não diferencia maiúsculas de minúsculas. Por exemplo, `prod` e `Prod` serão tratados como o mesmo grupo de simultaneidade.
    * Trabalhos ou execuções de fluxo de trabalho no mesmo grupo de simultaneidade são processados na ordem de primeiro a entrar em primeiro lugar (FIFO), de acordo com o momento em que cada um começou a esperar no grupo de simultaneidade, não o tempo em que cada fluxo de trabalho foi expedido. Como o horário de início efetivo de um trabalho ou execução pode variar, a ordenação não é garantida.

### Exemplos: Usar a simultaneidade e o comportamento padrão

O comportamento GitHub Actions padrão é permitir que vários trabalhos ou execuções de fluxo de trabalho sejam executados simultaneamente. A palavra-chave `concurrency` permite controlar a simultaneidade de execuções de fluxo de trabalho.

Por exemplo, você pode usar a palavra-chave `concurrency` imediatamente após a definição das condições de disparo para limitar a simultaneidade de execuções de fluxo de trabalho inteiro para uma ramificação específica:

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Você também pode limitar a simultaneidade de trabalhos em um fluxo de trabalho usando a palavra-chave `concurrency` no nível do trabalho:

```yaml
on:
  push:
    branches:
      - main

jobs:
  job-1:
    runs-on: ubuntu-latest
    concurrency:
      group: example-group
      cancel-in-progress: true
```

### Exemplo: grupos de concorrência

Os grupos de simultaneidade fornecem uma maneira de gerenciar e limitar a execução de fluxos de trabalho ou tarefas que compartilham a mesma chave de simultaneidade.

A chave `concurrency` é usada para agrupar fluxos de trabalho ou trabalhos em um grupo de simultaneidade. Quando você define uma `concurrency` chave, GitHub Actions garante que apenas um fluxo de trabalho ou trabalho com essa chave seja executado a qualquer momento. Se uma nova execução de fluxo de trabalho ou trabalho começar com a mesma `concurrency` chave, GitHub Actions cancelará qualquer fluxo de trabalho ou trabalho já em execução com essa chave. A chave `concurrency` pode ser uma cadeia de caracteres codificada ou pode ser uma expressão dinâmica que inclui variáveis de contexto.

É possível definir condições de concorrência no seu workflow para que o workflow ou tarefa faça parte de um grupo de concorrência.

Isso significa que, quando um fluxo de trabalho for executado ou iniciado, o GitHub cancelará todas as execuções de fluxo de trabalho ou trabalhos que já estejam em andamento no mesmo grupo de simultaneidade. Isso é útil em cenários em que você deseja impedir execuções paralelas para um determinado conjunto de fluxos de trabalho ou trabalhos, como os usados para implantações em um ambiente de preparo, a fim de evitar ações que possam causar conflitos ou consumir mais recursos do que o necessário.

Neste exemplo, `job-1` faz parte de um grupo de simultaneidade chamado `staging_environment`. Isso significa que, se uma nova execução de `job-1` for acionada, todas as execuções do mesmo trabalho no grupo de simultaneidade `staging_environment` que já estiverem em andamento serão canceladas.

```yaml
jobs:
  job-1:
    runs-on: ubuntu-latest
    concurrency:
      group: staging_environment
      cancel-in-progress: true
```

Como alternativa, usar uma expressão dinâmica, como `concurrency: ci-${{ github.ref }}` em seu fluxo de trabalho, significa que o fluxo de trabalho ou trabalho faria parte de um grupo de concorrência chamado `ci-`, seguido pela referência da ramificação ou tag que acionou o fluxo de trabalho. Neste exemplo, se uma nova confirmação for enviada para a ramificação principal enquanto uma execução anterior ainda estiver em andamento, a execução anterior será cancelada e a nova será iniciada:

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

### Exemplo: Enfileirando várias tarefas pendentes

Por padrão, apenas uma execução de tarefa ou de fluxo de trabalho pode estar `pending` em um grupo de simultaneidade por vez. Para permitir várias execuções na fila em vez de serem canceladas, defina `queue: max`. Com `queue: max`, até 100 trabalhos ou execuções de fluxo de trabalho podem aguardar no grupo de simultaneidade; depois que a fila estiver cheia, quaisquer execuções adicionais são canceladas.

Por exemplo, o fluxo de trabalho a seguir enfileira implantações no ambiente `production`, processando-as uma de cada vez em ordem com base no momento em que cada execução começou a aguardar no grupo de concorrência.

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: production-deploy
  queue: max
```

Observe que `queue: max` não pode ser combinado com `cancel-in-progress: true`, porque as duas opções descrevem comportamentos conflitantes para lidar com execuções em andamento.

### Exemplo: Usar a concorrência para cancelar qualquer trabalho em andamento ou em execução

Para usar a simultaneidade para cancelar qualquer trabalho em andamento GitHub Actions ou execução, você pode usar a tecla `concurrency` com a opção `cancel-in-progress` definida como `true`:

```yaml
concurrency:
  group: ${{ github.ref }}
  cancel-in-progress: true
```

Observe que, neste exemplo, sem definir um grupo de simultaneidade específico, GitHub Actions cancelará a execução de qualquer trabalho ou fluxo de trabalho em andamento.

### Exemplo: Usando um valor para segunda opção

Se você construir o nome do grupo com uma propriedade que só é definida para eventos específicos, você pode usar um valor de segunda opção. Por exemplo, `github.head_ref` só é definido em eventos `pull_request`. Se o fluxo de trabalho responder a outros eventos além de eventos `pull_request`, você precisará fornecer um fallback para evitar um erro de sintaxe. O grupo de simultaneidade a seguir cancela os trabalhos em andamento ou é executado somente em eventos `pull_request`. Se `github.head_ref` for indefinido, o grupo de simultaneidade fará fallback para a ID de execução, que tem a garantia de ser exclusiva e definida para a execução.

```yaml
concurrency:
  group: ${{ github.head_ref || github.run_id }}
  cancel-in-progress: true
```

### Exemplo: Cancele somente tarefas em andamento ou execuções no fluxo de trabalho atual

Se você tiver vários fluxos de trabalho no mesmo repositório, os nomes dos grupos de execução concorrente devem ser únicos em todos os fluxos de trabalho para evitar o cancelamento de tarefas ou execuções em andamento de outros fluxos de trabalho. Caso contrário, qualquer trabalho em andamento ou pendente será cancelado, independentemente do fluxo de trabalho.

Para cancelar apenas as execuções em andamento do mesmo fluxo de trabalho, use a propriedade `github.workflow` para criar o grupo de simultaneidade:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Exemplo: cancelar apenas trabalhos em andamento em ramificações específicas

Se você quiser cancelar trabalhos em andamento em determinadas ramificações, mas não em outras, poderá usar expressões condicionais com `cancel-in-progress`. Por exemplo, é possível fazer isso se quiser cancelar trabalhos em andamento em branches de desenvolvimento, mas não em branches de lançamento.

Para cancelar apenas execuções em andamento do mesmo fluxo de trabalho quando não estiverem em execução em um branch de lançamento, é possível definir `cancel-in-progress` para uma expressão semelhante à seguinte:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ !contains(github.ref, 'release/')}}
```

Neste exemplo, vários envios por push para um branch `release/1.2.3` não cancelariam execuções em andamento. Envios por push para outro branch, como `main`, cancelariam execuções em andamento.

## `cache-mode`

Use `cache-mode` para controlar o nível de acesso ao cache GitHub Actions que as tarefas no fluxo de trabalho têm. A configuração `cache-mode` no nível superior aplica-se a cada trabalho no fluxo de trabalho, a menos que um trabalho o substitua por [`jobs.<job_id>.cache-mode`](#jobsjob_idcache-mode).

O acesso é controlado por tokens de cache com escopo definido, portanto um job não pode restaurar nem salvar caches fora do modo que lhe foi concedido.
`cache-mode` aceita os valores a seguir.

| Value        | Restaurar caches | Salvar caches |
|------------|----------------|-------------|
| `read`       | Sim              | No            |
| `write`      | Sim              | Sim           |
| `write-only` | No               | Sim           |
| `none`       | No               | No            |

Se você omitir `cache-mode`, um `read` ou `write` padrão será usado com base no tipo de gatilho. Para valores padrão efetivos dependentes do acionador, consulte [Referência do cache de dependência](dependency-caching.md#defaults).

!!! warning
    Declarar explicitamente `cache-mode: write` ou `cache-mode: write-only` em gatilhos não confiáveis pode contornar a restrição segura padrão de cache somente de leitura e reintroduzir o risco de envenenamento por cache. Para obter diretrizes e mitigações, consulte [Referência do cache de dependência](dependency-caching.md#bypassing-the-default-untrusted-trigger-cache-restriction).

Quando uma operação de cache não é permitida pelo modo efetivo, a etapa de cache registra uma mensagem informativa e continua. A tarefa e o fluxo de trabalho não falham. Uma restauração ignorada é tratada como uma falha de cache; um salvamento ignorado simplesmente não é realizado. Para saber mais, confira [Referência do cache de dependência](dependency-caching.md#controlling-cache-access-with-cache-mode).

### Exemplo de `cache-mode`

```yaml
cache-mode: read

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/cache@v4
        with:
          path: ~/.npm
          key: npm-${{ hashFiles('**/package-lock.json') }}
```

## `jobs`

Uma execução de fluxo de trabalho é composta por um ou mais `jobs`, que são executados em paralelo por padrão. Para executar trabalhos sequencialmente, você pode definir dependências em outros trabalhos usando a palavra-chave `jobs.<job_id>.needs`.

Cada trabalho é executado em um ambiente do executor especificado por `runs-on`.

Você pode executar quantos trabalhos desejar, desde que esteja dentro dos limites de uso do fluxo de trabalho. Para obter mais informações, consulte [Cobrança e uso](../../concepts/billing-and-usage.md) sobre runners hospedados em GitHub e [Limites do Actions](../limits.md) para limites de uso de runners auto-hospedados.

Se você precisar encontrar o identificador exclusivo de um trabalho em execução em uma execução de fluxo de trabalho, poderá usar a GitHub API. Para saber mais, confira [Endpoints da API REST para Ações do GitHub](https://docs.github.com/pt/rest/actions#workflow-jobs).

## `jobs.<job_id>`

Use `jobs.<job_id>` para fornecer ao seu trabalho um identificador exclusivo. A chave `job_id` é uma cadeia de caracteres, e o valor dela é um mapa dos dados de configuração do trabalho. Você precisa substituir `<job_id>` por uma cadeia de caracteres exclusiva para o objeto `jobs`. A `<job_id>` precisa começar com uma letra ou `_` e conter apenas caracteres alfanuméricos, `-` ou `_`.

### Exemplo: Criando trabalhos

Neste exemplo, dois trabalhos foram criados, e os valores de `job_id` são `my_first_job` e `my_second_job`.

```yaml
jobs:
  my_first_job:
    name: My first job
  my_second_job:
    name: My second job
```

## `jobs.<job_id>.name`

Use `jobs.<job_id>.name` para definir um nome para o trabalho, que é exibido na interface do usuário do GitHub.

## `jobs.<job_id>.permissions`

Para um trabalho específico, você pode usar `jobs.<job_id>.permissions` para modificar as permissões padrão concedidas ao `GITHUB_TOKEN`, adicionando ou removendo o acesso conforme necessário, para que você permita apenas o acesso mínimo necessário. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).

Ao especificar a permissão em uma definição de trabalho, você pode configurar um conjunto diferente de permissões para o `GITHUB_TOKEN` em cada trabalho, se necessário. Como alternativa, você pode especificar as permissões para todas as tarefas do fluxo de trabalho. Para obter informações sobre como definir permissões no nível do fluxo de trabalho, confira [`permissions`](workflow-syntax.md#permissions).

Para cada uma das permissões disponíveis mostradas na tabela abaixo, você pode atribuir um dos níveis de acesso: `read` (se aplicável), `write` ou `none`.
`write` inclui `read`. Se você especificar o acesso para qualquer uma dessas permissões, todas aquelas que não forem especificadas serão definidas como `none`.

Permissões disponíveis e detalhes do que cada uma permite que uma ação faça:

| Permissão | Permite uma ação que usa `GITHUB_TOKEN` para |
| --- | --- |
| `actions` | Trabalhar com GitHub Actions. Por exemplo, `actions: write` permite que uma ação cancele uma execução de fluxo de trabalho. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-actions). |
| `artifact-metadata` | Trabalhe com metadados de artefatos. Por exemplo, `artifact-metadata: write` permite que uma ação crie registros de armazenamento em nome de um artefato de build. Para obter mais informações, confira [Pontos de extremidade de API REST para metadados de artefato](https://docs.github.com/pt/rest/orgs/artifact-metadata). |
| `attestations` | Trabalhar com atestados de artefatos. Por exemplo, `attestations: write` permite que uma ação gere um atestado de artefato para uma criação. Para obter mais informações, confira [Usar atestados de artefatos para estabelecer a procedência de compilações](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md) |
| `checks` | Trabalhar com verificação de execuções e verificação de conjuntos. Por exemplo, `checks: write` permite que uma ação crie uma verificação de execução. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-checks). |
| `code-quality` | Trabalhe com qualidade de código. Por exemplo, `code-quality: write` permite que uma ação carregue relatórios de cobertura de código. Para obter mais informações, confira [Qualidade do Código do GitHub](https://docs.github.com/pt/code-security/concepts/code-quality/code-quality). |
| `contents` | Trabalhar com o conteúdo do repositório. Por exemplo, `contents: read` permite que uma ação liste os commits e `contents: write` permite que a ação crie uma versão. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-contents). |
| `deployments` | Trabalhar com implantações. Por exemplo, `deployments: write` permite que uma ação crie uma implantação. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-deployments). |
| `discussions` | Trabalhar com discussões do GitHub. Por exemplo, `discussions: write` permite que uma ação feche ou exclua uma discussão. Para obter mais informações, confira [Usar a API do GraphQL para discussões](https://docs.github.com/pt/graphql/guides/using-the-graphql-api-for-discussions). |
| `id-token` | Recuperar um token OpenID Connect (OIDC). Isso exige usar `id-token: write`. Para obter mais informações, confira [OpenID Connect](../../concepts/security/openid-connect.md#updating-your-workflows-for-oidc) |
| `issues` | Trabalhar com problemas. Por exemplo, `issues: write` permite que uma ação adicione um comentário a um problema. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-issues). |
| `packages` | Trabalhar com GitHub Packages. Por exemplo, `packages: write` permite que uma ação carregue e publique pacotes no GitHub Packages. Para obter mais informações, confira [Sobre permissões para o GitHub Packages](https://docs.github.com/pt/packages/learn-github-packages/about-permissions-for-github-packages#about-scopes-and-permissions-for-package-registries). |
| `pages` | Trabalhar com páginas do GitHub. Por exemplo, `pages: write` permite que uma ação solicite um build de GitHub Pages. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-pages). |
| `pull-requests` | Trabalhar com solicitações de pull. Por exemplo, `pull-requests: write` permite que uma ação adicione um rótulo a uma PR. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-pull-requests). |
| `security-events` | Trabalhar com alertas de verificação de código do GitHub. Por exemplo, `security-events: read` permite que uma ação liste os alertas da digitalização de código para o repositório e `security-events: write` permite que uma ação atualize o status de um alerta de digitalização de código. Para obter mais informações, consulte [as permissões do Repositório para "Alertas de verificação de código"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-code-scanning-alerts). <br><br> |
| Para alertas do Dependabot, use a permissão `vulnerability-alerts`. Os alertas de verificação secreta não podem ser lidos com essa permissão e exigem um aplicativo GitHub ou um personal access token. Para obter mais informações, consulte [Permissões de Repositório para "Alertas de verificação de segredos"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-secret-scanning-alerts) em "Permissões necessárias para aplicativos GitHub". |  |
| `statuses` | Trabalhar com status de commits. Por exemplo, `statuses:read` permite que uma ação liste os status de commit de uma determinada referência. Para obter mais informações, confira [Permissões necessárias para aplicativos GitHub](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-commit-statuses). |
| `vulnerability-alerts` | Leia os alertas do Dependabot. Por exemplo, `vulnerability-alerts: read` permite que uma ação liste os alertas do Dependabot para o repositório. Somente `read` e `none` há suporte; `write` não é válido. Quando `write-all` ou `read-all` é usado, `vulnerability-alerts` é incluído automaticamente como `read`. Para obter mais informações, consulte [as permissões do Repositório para "Alertas do Dependabot"](https://docs.github.com/pt/rest/authentication/permissions-required-for-github-apps#repository-permissions-for-dependabot-alerts). |

### Definindo o acesso para os escopos do `GITHUB_TOKEN`

Você pode definir o acesso que o `GITHUB_TOKEN` permitirá especificando `read`, `write` ou `none` como o valor das permissões disponíveis na chave `permissions`.

```yaml
permissions:
  actions: read|write|none
  artifact-metadata: read|write|none
  attestations: read|write|none
  checks: read|write|none
  code-quality: read|write|none
  contents: read|write|none
  deployments: read|write|none
  id-token: write|none
  issues: read|write|none
  discussions: read|write|none
  packages: read|write|none
  pages: read|write|none
  pull-requests: read|write|none

  security-events: read|write|none
  statuses: read|write|none
  vulnerability-alerts: read|none
```

Se você especificar o acesso para uma dessas permissões, todas aquelas que não forem especificadas serão definidas como `none`.

Você pode usar a sintaxe a seguir para definir o acesso de `read-all` ou `write-all` para todas as permissões disponíveis:

```yaml
permissions: read-all
```

```yaml
permissions: write-all
```

Você pode usar a seguinte sintaxe para desabilitar as permissões para todas as permissões disponíveis:

```yaml
permissions: {}
```

#### Alterar as permissões em um repositório bifurcado

Você pode usar a tecla `permissions` para adicionar e remover permissões de leitura de repositórios derivados (forks), mas normalmente não pode conceder acesso de gravação. A exceção a esse comportamento ocorre quando um usuário administrador seleciona a opção **Enviar tokens de gravação para fluxos de trabalho a partir de pull requests** nas GitHub Actions configurações. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#enabling-workflows-for-forks-of-private-repositories).

#### Exemplo: definir as permissões do `GITHUB_TOKEN` para um trabalho em um fluxo de trabalho

Este exemplo mostra as permissões que estão sendo definidas para o `GITHUB_TOKEN` que se aplicará somente ao trabalho chamado `stale`. O acesso de gravação é permitido para as permissões `issues` e `pull-requests`. Nenhuma outra permissão terá acesso.

```yaml
jobs:
  stale:
    runs-on: ubuntu-latest

    permissions:
      issues: write
      pull-requests: write

    steps:
      - uses: actions/stale@v10
```

## `jobs.<job_id>.needs`

Use `jobs.<job_id>.needs` para identificar todos os trabalhos que precisam ser concluídos com êxito antes que este trabalho seja executado. Esse código pode ser uma string ou array de strings. Se houver falha em um trabalho ou ele for ignorado, todos os trabalhos que dependem dele serão ignorados, a menos que os trabalhos usem uma expressão condicional que faça o trabalho continuar. Se uma execução contiver uma série de trabalhos que precisem uns dos outros, uma falha ou omissão se aplicará a todos os trabalhos na cadeia de dependência do ponto de falha ou omissão em diante. Se quiser que um trabalho seja executado mesmo que um trabalho do qual ele dependa não seja bem-sucedido, use a expressão condicional `always()` em `jobs.<job_id>.if`.

### Exemplo: Exigir que as tarefas dependentes sejam concluídas com êxito

```yaml
jobs:
  job1:
  job2:
    needs: job1
  job3:
    needs: [job1, job2]
```

Neste exemplo, `job1` precisa ser concluído com êxito antes que `job2` seja iniciado, e `job3` aguarda a conclusão de `job1` e de `job2`.

Os trabalhos neste exemplo são executados sequencialmente:

1. `job1`
2. `job2`
3. `job3`

### Exemplo: Sem exigir a conclusão bem-sucedida de tarefas dependentes

```yaml
jobs:
  job1:
  job2:
    needs: job1
  job3:
    if: ${{ always() }}
    needs: [job1, job2]
```

Neste exemplo, `job3` usa a expressão condicional `always()` para que ela sempre seja executada após a conclusão de `job1` e de `job2`, independentemente de elas terem sido bem-sucedidas. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md#status-check-functions).

## `jobs.<job_id>.if`

Use o condicional `jobs.<job_id>.if` para impedir que um trabalho seja executado, a não ser que uma condição seja atendida. Você pode usar qualquer contexto e expressão compatível para criar uma condicional. Para obter mais informações sobre quais contextos têm suporte nessa chave, confira [Referência de contextos](contexts.md#context-availability).

!!! note
    A condição `jobs.<job_id>.if` é avaliada antes de [`jobs.<job_id>.strategy.matrix`](workflow-syntax.md#jobsjob_idstrategymatrix) ser aplicado.

Ao usar expressões em um condicional `if`, opcionalmente, você poderá omitir a sintaxe de expressão `${{ }}`, pois o GitHub Actions avalia automaticamente o condicional `if` como uma expressão. No entanto, essa exceção não se aplica a todos os lugares.

Você sempre deverá usar a sintaxe de expressão `${{ }}` ou escapar com `''`, `""` ou `()` quando a expressão começar com `!`, já que `!` é a notação reservada no formato YAML. Por exemplo:

```yaml
if: ${{ ! startsWith(github.ref, 'refs/tags/') }}
```

Para obter mais informações, consulte [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

### Exemplo: Somente executar o trabalho para um repositório específico

Este exemplo usa `if` para controlar quando o trabalho `production-deploy` pode ser executado. Ele só será executado se o repositório for chamado `octo-repo-prod` e estiver na organização `octo-org`. Caso contrário, o trabalho será marcado como *ignorado*.

```yaml copy
name: example-workflow
on: [push]
jobs:
  production-deploy:
    if: github.repository == 'octo-org/octo-repo-prod'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
```

## `jobs.<job_id>.runs-on`

Use `jobs.<job_id>.runs-on` para definir o tipo de computador no qual o trabalho será executado.

* A máquina de destino pode ser um [GitHubrunner](#choosing-github-hosted-runners) hospedado, [executor avançado](#choosing-runners-in-a-group), ou um [runner auto-hospedado](#choosing-self-hosted-runners).

* Você pode selecionar os executores com base nos rótulos atribuídos a eles, em sua participação em um grupo ou em uma combinação desses critérios.

* Você pode fornecer `runs-on` como:
  * Uma única string
  * Uma única variável que contém uma cadeia de caracteres
  * Uma matriz de cadeias de caracteres, variáveis que contêm cadeias de caracteres ou uma combinação de ambas
  * um par de `key: value` usando as chaves `group` ou `labels`

* Se você especificar uma matriz de cadeias de caracteres ou variáveis, o fluxo de trabalho será executado em qualquer executor que corresponda a todos os valores `runs-on` especificados. Por exemplo, aqui o trabalho só será executado em um executor auto-hospedado que tenha os rótulos `linux`, `x64` e `gpu`:

        ```yaml
  runs-on: [self-hosted, linux, x64, gpu]
  ```

  Para obter mais informações, confira [Como escolher executores auto-hospedados](#choosing-self-hosted-runners).

* Você pode misturar cadeias de caracteres e variáveis em uma matriz. Por exemplo:

        ```yaml
  on:
    workflow_dispatch:
      inputs:
        chosen-os:
          required: true
          type: choice
          options:
          - Ubuntu
          - macOS

  jobs:
    test:
      runs-on: [self-hosted, "${{ inputs.chosen-os }}"]
      steps:
      - run: echo Hello world!
  ```

* Se você quiser executar seu fluxo de trabalho em vários computadores, use [`jobs.<job_id>.strategy`](workflow-syntax.md#jobsjob_idstrategy).

!!! note
    Aspas não são necessárias em torno de cadeias de caracteres simples como`self-hosted`, mas são necessárias para expressões como`"${{ inputs.chosen-os }}"` .

### Escolher executores hospedados em GitHub

Se você usar um runner hospedado em GitHub, cada tarefa será executada em uma nova instância de uma imagem do runner especificada por `runs-on`.

O valor de runs-on, quando você estiver usando um runner hospedado pelo GitHub, é um rótulo de um fluxo de trabalho ou o nome de um grupo de executores. Os rótulos dos executores padrão hospedados em GitHub são exibidos nas tabelas a seguir.

Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md).

### Executores padrão hospedados GitHubpara repositórios públicos

Para repositórios públicos, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados com as especificações associadas.
Com exceção dos executores de CPU única, cada executor hospedado por GitHub é uma nova máquina virtual (VM) hospedada por GitHub. Processos de CPU única são hospedados em um contêiner em uma VM compartilhada—consulte [Referência de executores hospedados pelo GitHub](../runners/github-hosted-runners.md#single-cpu-runners). O uso dos executores hospedados padrão GitHubé gratuito e ilimitado em repositórios públicos.

| **Máquina virtual/contêiner** | **Processador (CPU)** | **Memória (RAM)** | **Armazenamento (SSD)** | **Arquitetura** | **Rótulo do fluxo de trabalho** |
| --- | --- | --- | --- | --- | --- |
| Linux | 1 | 5 GB | 14 GB | x64 | `[ubuntu-slim](https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md)`<br>Linux<br>4<br>16 GB<br>14 GB<br>x64 |
```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-VS2026-Readme.md">windows-2025-vs2026</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td>arm64</td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-VS2026-Arm64-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

### Executores hospedados padrão GitHubpara  privados

Para  privados, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados em máquinas virtuais com as especificações associadas. Esses executores usam a alocação de minutos gratuitos da sua GitHub conta e, posteriormente, são cobrados a taxas por minuto de uso. Confira [Precificação do executor de ações](https://docs.github.com/pt/billing/reference/actions-runner-pricing).

| **Máquina virtual** | **Processador (CPU)** | **Memória (RAM)** | **Armazenamento (SSD)** | **Arquitetura** | **Rótulo do fluxo de trabalho** |
| --- | --- | --- | --- | --- | --- |
| Linux | 1 | 5 GB | 14 GB | x64 | `[ubuntu-slim](https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md)`<br>Linux<br>2<br>8 GB<br>14 GB<br>x64 |
```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-VS2026-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

Além dos executores padrão hospedados em GitHub, GitHub oferece aos clientes dos planos GitHub Team e GitHub Enterprise Cloud uma variedade de máquinas virtuais gerenciadas com recursos avançados, como, por exemplo, mais núcleos e espaço em disco, máquinas com GPU e máquinas com arquitetura ARM. Para saber mais, confira [Executores avançados](../../concepts/runners/larger-runners.md).

!!! note
    As imagens do executor `-latest` são as imagens estáveis mais recentes fornecidas pelo GitHub, e podem não ser a versão mais recente do sistema operacional disponível junto ao fornecedor do sistema operacional.

    [!WARNING]
    As imagens beta e preteridas são fornecidas “no estado em que se encontram”, “com todas as falhas” e “conforme disponível” e são excluídas do contrato de nível de serviço e da garantia. As imagens beta podem não estar cobertas pelo suporte ao cliente.

#### Exemplo: Especificar um sistema operacional

```yaml
runs-on: ubuntu-latest
```

Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md).

### Escolhendo executores auto-hospedados

Para especificar um executor auto-hospedado para uma tarefa, configure `runs-on` no arquivo do fluxo de trabalho utilizando rótulos do executor auto-hospedado.

Os executores auto-hospedados podem ter o rótulo `self-hosted`. Ao configurar um corredor auto-hospedado, por padrão, incluiremos o rótulo `self-hosted`. Você pode passar o sinalizador `--no-default-labels` para impedir que o rótulo auto-hospedado seja aplicado. Rótulos podem ser usados para criar opções de segmentação para os executores, como sistema operacional ou arquitetura. Recomendamos fornecer uma matriz de rótulos que comece com `self-hosted` (isso deve ser listado primeiro) e depois inclua rótulos adicionais, conforme necessário. Quando você especifica um array de rótulos, os trabalhos serão enfileirados em executores que possuem todos os rótulos que você especificou.

> [!NOTE] Actions Runner Controller não dá suporte ao `self-hosted` rótulo.

#### Exemplo: Usando etiquetas para seleção do executor

```yaml
runs-on: [self-hosted, linux]
```

Para saber mais, confira [Executores auto-hospedados](../../concepts/runners/self-hosted-runners.md) e [Usar os executores auto-hospedados em um fluxo de trabalho](../../how-tos/manage-runners/self-hosted-runners/use-in-a-workflow.md).

### Escolher executores em um grupo

Você pode usar `runs-on` para direcionar grupos de executores para que o trabalho seja executado em qualquer executor que seja membro desse grupo. Para um controle mais granular, você também pode combinar grupos de executores com rótulos.

Os grupos de executores só podem ter [executor avançados](../../concepts/runners/larger-runners.md) ou [executores auto-hospedados](../../how-tos/manage-runners/self-hosted-runners.md) como membros.

#### Exemplo: usar grupos para controlar onde os trabalhos são executados

Neste exemplo, foram adicionados executores a um grupo chamado `build-runners`. A chave `runs-on` envia o trabalho para qualquer executor disponível no grupo `build-runners`:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: build-runners
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

#### Exemplo: combinar grupos e rótulos

Quando você combina grupos e rótulos, o executor deve atender aos dois requisitos para ser qualificado para executar o trabalho.

Neste exemplo, a `runs-on` chave combina `group` e `labels` , portanto, o trabalho é roteado para qualquer executor disponível dentro do grupo que também tenha um rótulo correspondente:

```yaml
name: learn-github-actions
on: [push]
jobs:
  check-bats-version:
    runs-on:
      group: ubuntu-runners
      labels: ubuntu-24.04-16core
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v7
        with:
          node-version: '14'
      - run: npm install -g bats
      - run: bats -v
```

## `jobs.<job_id>.snapshot`

Você pode usar `jobs.<job_id>.snapshot` para gerar uma imagem personalizada.

Adicione a palavra-chave "instantâneo" ao trabalho, utilizando a sintaxe de string ou a sintaxe de mapeamento, conforme mostrado em [Geração de uma Imagem Personalizada](../../how-tos/manage-runners/larger-runners/use-custom-images.md#generating-a-custom-image).

Cada tarefa que inclui a palavra-chave "captura" gera uma imagem separada. Para gerar apenas uma imagem ou versão de imagem, inclua todas as etapas de fluxo de trabalho em um único trabalho. Cada execução bem-sucedida de um trabalho que inclui a palavra-chave "snapshot" cria uma nova versão dessa imagem.

Para saber mais, confira [Usando imagens personalizadas](../../how-tos/manage-runners/larger-runners/use-custom-images.md).

## `jobs.<job_id>.environment`

Use `jobs.<job_id>.environment` para definir o ambiente que o trabalho referencia.

Você pode fornecer o ambiente como apenas o ambiente `name` ou como um objeto de ambiente com o `name` e a `url`. A URL é mapeada para `environment_url` na a API de implantações. Para obter mais informações sobre a API de implantações, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#deployments).

!!! note
    Todas as regras de proteção para implantação têm de ser aprovadas para que um trabalho que faça referência ao ambiente seja enviado a um executor. Para saber mais, confira [Gerenciar ambientes para implantação](../../how-tos/deploy/configure-and-manage-deployments/manage-environments.md).

### Exemplo: Usando um único nome de ambiente

```yaml
environment: staging_environment
```

### Exemplo: Usando o nome de ambiente e URL

```yaml
environment:
  name: production_environment
  url: https://github.com
```

O valor de `url` pode ser uma expressão. Contextos de expressão permitidos: [`github`](contexts.md#github-context), [`inputs`](contexts.md#inputs-context), [`vars`](contexts.md#vars-context), [`needs`](contexts.md#needs-context), [`strategy`](contexts.md#strategy-context), [`matrix`](contexts.md#matrix-context), [`job`](contexts.md#job-context), [`runner`](contexts.md#runner-context), [`env`](contexts.md#env-context) e [`steps`](contexts.md#steps-context). Para obter mais informações sobre expressões, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

### Exemplo: Usando a saída como URL

```yaml
environment:
  name: production_environment
  url: ${{ steps.step_id.outputs.url_output }}
```

O valor de `name` pode ser uma expressão. Contextos de expressão permitidos: [`github`](contexts.md#github-context), [`inputs`](contexts.md#inputs-context), [`vars`](contexts.md#vars-context), [`needs`](contexts.md#needs-context), [`strategy`](contexts.md#strategy-context) e [`matrix`](contexts.md#matrix-context). Para obter mais informações sobre expressões, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

### Exemplo: usando uma expressão como nome de ambiente

```yaml
environment:
  name: ${{ github.ref_name }}
```

### Exemplo: usar um ambiente sem criar uma implantação

Defina `deployment` para `false` usar os segredos e variáveis de um ambiente sem criar um objeto de implantação.

```yaml
environment:
  name: testing
  deployment: false
```

A configuração `deployment: false` não é compatível com regras de proteção de implantação personalizadas.
Para saber mais, confira [Implantando com GitHub Actions](../../how-tos/deploy/configure-and-manage-deployments/control-deployments.md#using-environments-without-deployments).

## `jobs.<job_id>.concurrency`

Você pode usar `jobs.<job_id>.concurrency` para garantir que apenas um trabalho ou fluxo de trabalho que usa o mesmo grupo de simultaneidade seja executado por vez. Um grupo de concorrência pode ser qualquer string ou expressão. Contextos de expressão permitidos: [`github`](contexts.md#github-context), [`inputs`](contexts.md#inputs-context), [`vars`](contexts.md#vars-context), [`needs`](contexts.md#needs-context), [`strategy`](contexts.md#strategy-context) e [`matrix`](contexts.md#matrix-context). Para obter mais informações sobre expressões, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

Especifique também `concurrency` no nível do fluxo de trabalho. Para obter mais informações, confira [`concurrency`](workflow-syntax.md#concurrency).

Isso significa que pode haver no máximo um trabalho ou fluxo de trabalho em execução em um grupo de concorrência a qualquer momento. Quando um trabalho ou um fluxo de trabalho simultâneo é colocado na fila, se outro trabalho ou fluxo de trabalho que usa o mesmo grupo de simultaneidade no repositório estiver em andamento, o trabalho ou o fluxo de trabalho na fila ficará `pending`. Por padrão, qualquer trabalho ou fluxo de trabalho existente `pending` no mesmo grupo de simultaneidade será cancelado e o novo trabalho ou fluxo de trabalho em fila tomará seu lugar.

Para também cancelar qualquer trabalho ou fluxo de trabalho em execução no mesmo grupo de concorrência, especifique `cancel-in-progress: true`. Para cancelar condicionalmente trabalhos ou fluxos de trabalho em execução no mesmo grupo de simultaneidade, é possível especificar `cancel-in-progress` como uma expressão com qualquer um dos contextos de expressão permitidos.

Para permitir que mais de uma tarefa ou execução de fluxo de trabalho aguardem no mesmo grupo de simultaneidade, use a propriedade opcional `queue`. A `queue` propriedade aceita os seguintes valores:

* `single` (padrão): no máximo uma execução de tarefa ou de fluxo de trabalho pode ser `pending` no grupo de simultaneidade. Quando uma nova execução de trabalho ou fluxo de trabalho é enfileirada, qualquer execução existente de trabalho ou fluxo de trabalho `pending` no mesmo grupo é cancelada e substituída.
* `max`: até 100 trabalhos ou execuções de fluxo de trabalho podem ser incluídos no grupo de simultaneidade. Quando a fila estiver cheia, quaisquer trabalhos adicionais ou execuções de fluxo de trabalho serão cancelados.

A combinação de `queue: max` e `cancel-in-progress: true` não é permitida e resultará em um erro de validação de fluxo de trabalho.

!!! note
    * O nome do grupo de simultaneidade não diferencia maiúsculas de minúsculas. Por exemplo, `prod` e `Prod` serão tratados como o mesmo grupo de simultaneidade.
    * Trabalhos ou execuções de fluxo de trabalho no mesmo grupo de simultaneidade são processados na ordem de primeiro a entrar em primeiro lugar (FIFO), de acordo com o momento em que cada um começou a esperar no grupo de simultaneidade, não o tempo em que cada fluxo de trabalho foi expedido. Como o horário de início efetivo de um trabalho ou execução pode variar, a ordenação não é garantida.

### Exemplos: Usar a simultaneidade e o comportamento padrão

O comportamento GitHub Actions padrão é permitir que vários trabalhos ou execuções de fluxo de trabalho sejam executados simultaneamente. A palavra-chave `concurrency` permite controlar a simultaneidade de execuções de fluxo de trabalho.

Por exemplo, você pode usar a palavra-chave `concurrency` imediatamente após a definição das condições de disparo para limitar a simultaneidade de execuções de fluxo de trabalho inteiro para uma ramificação específica:

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

Você também pode limitar a simultaneidade de trabalhos em um fluxo de trabalho usando a palavra-chave `concurrency` no nível do trabalho:

```yaml
on:
  push:
    branches:
      - main

jobs:
  job-1:
    runs-on: ubuntu-latest
    concurrency:
      group: example-group
      cancel-in-progress: true
```

### Exemplo: grupos de concorrência

Os grupos de simultaneidade fornecem uma maneira de gerenciar e limitar a execução de fluxos de trabalho ou tarefas que compartilham a mesma chave de simultaneidade.

A chave `concurrency` é usada para agrupar fluxos de trabalho ou trabalhos em um grupo de simultaneidade. Quando você define uma `concurrency` chave, GitHub Actions garante que apenas um fluxo de trabalho ou trabalho com essa chave seja executado a qualquer momento. Se uma nova execução de fluxo de trabalho ou trabalho começar com a mesma `concurrency` chave, GitHub Actions cancelará qualquer fluxo de trabalho ou trabalho já em execução com essa chave. A chave `concurrency` pode ser uma cadeia de caracteres codificada ou pode ser uma expressão dinâmica que inclui variáveis de contexto.

É possível definir condições de concorrência no seu workflow para que o workflow ou tarefa faça parte de um grupo de concorrência.

Isso significa que, quando um fluxo de trabalho for executado ou iniciado, o GitHub cancelará todas as execuções de fluxo de trabalho ou trabalhos que já estejam em andamento no mesmo grupo de simultaneidade. Isso é útil em cenários em que você deseja impedir execuções paralelas para um determinado conjunto de fluxos de trabalho ou trabalhos, como os usados para implantações em um ambiente de preparo, a fim de evitar ações que possam causar conflitos ou consumir mais recursos do que o necessário.

Neste exemplo, `job-1` faz parte de um grupo de simultaneidade chamado `staging_environment`. Isso significa que, se uma nova execução de `job-1` for acionada, todas as execuções do mesmo trabalho no grupo de simultaneidade `staging_environment` que já estiverem em andamento serão canceladas.

```yaml
jobs:
  job-1:
    runs-on: ubuntu-latest
    concurrency:
      group: staging_environment
      cancel-in-progress: true
```

Como alternativa, usar uma expressão dinâmica, como `concurrency: ci-${{ github.ref }}` em seu fluxo de trabalho, significa que o fluxo de trabalho ou trabalho faria parte de um grupo de concorrência chamado `ci-`, seguido pela referência da ramificação ou tag que acionou o fluxo de trabalho. Neste exemplo, se uma nova confirmação for enviada para a ramificação principal enquanto uma execução anterior ainda estiver em andamento, a execução anterior será cancelada e a nova será iniciada:

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

### Exemplo: Enfileirando várias tarefas pendentes

Por padrão, apenas uma execução de tarefa ou de fluxo de trabalho pode estar `pending` em um grupo de simultaneidade por vez. Para permitir várias execuções na fila em vez de serem canceladas, defina `queue: max`. Com `queue: max`, até 100 trabalhos ou execuções de fluxo de trabalho podem aguardar no grupo de simultaneidade; depois que a fila estiver cheia, quaisquer execuções adicionais são canceladas.

Por exemplo, o fluxo de trabalho a seguir enfileira implantações no ambiente `production`, processando-as uma de cada vez em ordem com base no momento em que cada execução começou a aguardar no grupo de concorrência.

```yaml
on:
  push:
    branches:
      - main

concurrency:
  group: production-deploy
  queue: max
```

Observe que `queue: max` não pode ser combinado com `cancel-in-progress: true`, porque as duas opções descrevem comportamentos conflitantes para lidar com execuções em andamento.

### Exemplo: Usar a concorrência para cancelar qualquer trabalho em andamento ou em execução

Para usar a simultaneidade para cancelar qualquer trabalho em andamento GitHub Actions ou execução, você pode usar a tecla `concurrency` com a opção `cancel-in-progress` definida como `true`:

```yaml
concurrency:
  group: ${{ github.ref }}
  cancel-in-progress: true
```

Observe que, neste exemplo, sem definir um grupo de simultaneidade específico, GitHub Actions cancelará a execução de qualquer trabalho ou fluxo de trabalho em andamento.

### Exemplo: Usando um valor para segunda opção

Se você construir o nome do grupo com uma propriedade que só é definida para eventos específicos, você pode usar um valor de segunda opção. Por exemplo, `github.head_ref` só é definido em eventos `pull_request`. Se o fluxo de trabalho responder a outros eventos além de eventos `pull_request`, você precisará fornecer um fallback para evitar um erro de sintaxe. O grupo de simultaneidade a seguir cancela os trabalhos em andamento ou é executado somente em eventos `pull_request`. Se `github.head_ref` for indefinido, o grupo de simultaneidade fará fallback para a ID de execução, que tem a garantia de ser exclusiva e definida para a execução.

```yaml
concurrency:
  group: ${{ github.head_ref || github.run_id }}
  cancel-in-progress: true
```

### Exemplo: Cancele somente tarefas em andamento ou execuções no fluxo de trabalho atual

Se você tiver vários fluxos de trabalho no mesmo repositório, os nomes dos grupos de execução concorrente devem ser únicos em todos os fluxos de trabalho para evitar o cancelamento de tarefas ou execuções em andamento de outros fluxos de trabalho. Caso contrário, qualquer trabalho em andamento ou pendente será cancelado, independentemente do fluxo de trabalho.

Para cancelar apenas as execuções em andamento do mesmo fluxo de trabalho, use a propriedade `github.workflow` para criar o grupo de simultaneidade:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

### Exemplo: cancelar apenas trabalhos em andamento em ramificações específicas

Se você quiser cancelar trabalhos em andamento em determinadas ramificações, mas não em outras, poderá usar expressões condicionais com `cancel-in-progress`. Por exemplo, é possível fazer isso se quiser cancelar trabalhos em andamento em branches de desenvolvimento, mas não em branches de lançamento.

Para cancelar apenas execuções em andamento do mesmo fluxo de trabalho quando não estiverem em execução em um branch de lançamento, é possível definir `cancel-in-progress` para uma expressão semelhante à seguinte:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ !contains(github.ref, 'release/')}}
```

Neste exemplo, vários envios por push para um branch `release/1.2.3` não cancelariam execuções em andamento. Envios por push para outro branch, como `main`, cancelariam execuções em andamento.

## `jobs.<job_id>.cache-mode`

Use `jobs.<job_id>.cache-mode` para definir o nível de acesso ao GitHub Actions cache para um único trabalho. Um valor definido aqui substitui qualquer nível [`cache-mode`](#cache-mode) de fluxo de trabalho somente para este trabalho.

Os valores aceitos são`read`, , `write``write-only`e `none`, com os mesmos significados que a chave de nível superior. Se nem o job nem o fluxo de trabalho definirem `cache-mode`, aplica-se um padrão baseado em gatilho. Para obter mais informações sobre cada valor, consulte [`cache-mode`](#cache-mode) e [Referência do cache de dependência](dependency-caching.md#defaults).

!!! warning
    Declarar explicitamente `cache-mode: write` ou `cache-mode: write-only` em gatilhos não confiáveis pode contornar a restrição segura padrão de cache somente de leitura e reintroduzir o risco de envenenamento por cache. Para obter diretrizes e mitigações, consulte [Referência do cache de dependência](dependency-caching.md#bypassing-the-default-untrusted-trigger-cache-restriction).

Você também pode definir `cache-mode` em um trabalho que chama um fluxo de trabalho reutilizável para limitar o acesso de cache concedido ao fluxo de trabalho chamado. Para saber mais, confira [Reutilizando configurações de fluxo de trabalho](reusing-workflow-configurations.md#supported-keywords-for-jobs-that-call-a-reusable-workflow) e [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#controlling-cache-access-in-reusable-workflows).

### Exemplo de `jobs.<job_id>.cache-mode`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    cache-mode: write
  test:
    runs-on: ubuntu-latest
    cache-mode: read
```

## `jobs.<job_id>.outputs`

Você pode usar `jobs.<job_id>.outputs` para criar um `map` das saídas de uma tarefa. As saídas de trabalho estão disponíveis para todos os trabalhos downstream que dependem deste trabalho. Para obter mais informações sobre como definir dependências de trabalho, confira [`jobs.<job_id>.needs`](workflow-syntax.md#jobsjob_idneeds).

As saídas podem ter no máximo 1 MB por trabalho. O total de todas as saídas em uma execução de fluxo de trabalho pode ter no máximo 50 MB. O tamanho é aproximado com base na codificação UTF-16.

As saídas de trabalho que contêm expressões são avaliadas no executor ao final de cada trabalho. As saídas que contêm segredos são ocultadas no runner e não são enviadas para GitHub Actions.

Se uma saída for ignorada porque pode conter um segredo, você verá a seguinte mensagem de aviso: "Ignorar saída `{output.Key}` pois ela pode conter segredo". Para obter mais informações sobre como lidar com segredos, consulte o [Exemplo: Mascarar e passar um segredo entre trabalhos ou fluxos de trabalho](workflow-commands.md#example-masking-and-passing-a-secret-between-jobs-or-workflows).

Para usar saídas de trabalho em um trabalho dependente, você pode usar o contexto `needs`. Para saber mais, confira [Referência de contextos](contexts.md#needs-context).

### Exemplo: Definindo saídas para um trabalho

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    # Map a step output to a job output
    outputs:
      output1: ${{ steps.step1.outputs.test }}
      output2: ${{ steps.step2.outputs.test }}
    steps:
      - id: step1
        run: echo "test=hello" >> "$GITHUB_OUTPUT"
      - id: step2
        run: echo "test=world" >> "$GITHUB_OUTPUT"
  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - env:
          OUTPUT1: ${{needs.job1.outputs.output1}}
          OUTPUT2: ${{needs.job1.outputs.output2}}
        run: echo "$OUTPUT1 $OUTPUT2"
```

### Uso de saídas de trabalho em um trabalho de matriz

As matrizes podem ser usadas para gerar várias saídas de nomes diferentes. Ao usar uma matriz, as saídas dos trabalhos serão combinadas a partir de todos os trabalhos na matriz.

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      output_1: ${{ steps.gen_output.outputs.output_1 }}
      output_2: ${{ steps.gen_output.outputs.output_2 }}
      output_3: ${{ steps.gen_output.outputs.output_3 }}
    strategy:
      matrix:
        version: [1, 2, 3]
    steps:
      - name: Generate output
        id: gen_output
        run: |
          version="${{ matrix.version }}"
          echo "output_${version}=${version}" >> "$GITHUB_OUTPUT"
  job2:
    runs-on: ubuntu-latest
    needs: [job1]
    steps:
      # Will show
      # {
      #   "output_1": "1",
      #   "output_2": "2",
      #   "output_3": "3"
      # }
      - run: echo '${{ toJSON(needs.job1.outputs) }}'
```

!!! warning
    O Actions não garante a ordem em que os trabalhos da matriz serão executados. Verifique se o nome de saída é exclusivo; caso contrário, o último trabalho de matriz executado substituirá o valor de saída.

## `jobs.<job_id>.env`

Um `map` das variáveis que estão disponíveis para todas as etapas do trabalho. Também é possível definir variáveis para todo o fluxo de trabalho ou uma etapa individual. Para obter mais informações, consulte [`env`](#env) e [`jobs.<job_id>.steps[*].env`](#jobsjob_idstepsenv).

Quando mais de uma variável de ambiente é definida com o mesmo nome, GitHub usa a variável mais específica. Por exemplo, uma variável de ambiente definida em uma etapa substituirá as variáveis de ambiente do trabalho e do fluxo de trabalho que tenham o mesmo nome enquanto a etapa é executada. Uma variável de ambiente definida para um trabalho substituirá uma variável de fluxo de trabalho com o mesmo nome enquanto o trabalho é executado.

### Exemplo de `jobs.<job_id>.env`

```yaml
jobs:
  job1:
    env:
      FIRST_NAME: Mona
```

## `jobs.<job_id>.defaults`

Use `jobs.<job_id>.defaults` para criar um `map` das configurações padrão que será aplicado a todas as etapas do trabalho. Você também pode definir as configurações-padrão para todo o fluxo de trabalho. Para obter mais informações, confira [`defaults`](workflow-syntax.md#defaults).

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `jobs.<job_id>.defaults.run`

Use `jobs.<job_id>.defaults.run` para fornecer o `shell` e o `working-directory` padrão para todas as etapas `run` do trabalho.

Você pode fornecer as opções `shell` e `working-directory` padrão para todas as etapas [`run`](workflow-syntax.md#jobsjob_idstepsrun) de um trabalho. Também pode definir as configurações padrão para `run` em todo o fluxo de trabalho. Para obter mais informações, consulte [`defaults.run`](workflow-syntax.md#defaultsrun).

Esses podem ser substituídos nos níveis `jobs.<job_id>.defaults.run` e `jobs.<job_id>.steps[*].run`.

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `jobs.<job_id>.defaults.run.shell`

Use `shell` para definir o `shell` para uma etapa. Essa palavra-chave pode fazer referência a vários contextos. Para obter mais informações, confira [Contextos](contexts.md#context-availability).

| Plataforma compatível | Parâmetro `shell` | Descrição | Comando executado internamente |
| --- | --- | --- | --- |
| Linux / macOS | não especificado | O shell padrão em plataformas não Windows. Isso executa um comando diferente para quando `bash` é especificado explicitamente. Se `bash` não for encontrado no caminho, isso será tratado como `sh`. | `bash -e {0}` |
| Tudo | `bash` | O shell padrão em plataformas não Windows com um fallback para `sh`. Ao especificar um shell bash no Windows, é utilizado o shell bash incluído no Git para Windows. | `bash --noprofile --norc -eo pipefail {0}` |
| Tudo | `pwsh` | Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `pwsh -command ". '{0}'"` |
| Tudo | `python` | Executa o comando python. | `python {0}` |
| Linux / macOS | `sh` | O comportamento de fallback para plataformas não Windows se nenhum shell for fornecido e o `bash` não for encontrado no caminho. | `sh -e {0}` |
| Windows | `cmd` | O GitHub acrescenta a extensão `.cmd` ao nome do script e a substitui por `{0}`. | `%ComSpec% /D /E:ON /V:OFF /S /C "CALL "{0}""`. |
| Windows | `pwsh` | Essa é a shell padrão usada no Windows. Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. Se o executor auto-hospedado do Windows não tiver o *PowerShell Core* instalado, o *PowerShell Desktop* será usado. | `pwsh -command ". '{0}'"`. |
| Windows | `powershell` | O PowerShell Desktop. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `powershell -command ". '{0}'"`. |

Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

## `jobs.<job_id>.defaults.run.working-directory`

Use `working-directory` para definir o diretório de trabalho do `shell` de uma etapa. Essa palavra-chave pode fazer referência a vários contextos. Para obter mais informações, confira [Contextos](contexts.md#context-availability).

!!! tip
    Verifique se o `working-directory` existe no executor antes de executar seu shell nele.
    Quando mais de uma configuração padrão é definida com o mesmo nome, GitHub usa a configuração padrão mais específica. Por exemplo, uma configuração padrão definida em uma tarefa irá substituir uma configuração padrão que tem o mesmo nome definido em um fluxo de trabalho.

### Exemplo: definição das opções da etapa `run` padrão para um trabalho

```yaml
jobs:
  job1:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash
        working-directory: ./scripts
```

## `jobs.<job_id>.steps`

Um trabalho contém uma sequência de tarefas chamada `steps`. As etapas podem executar comandos, executar trabalhos de configuração ou executar ações no seu repositório, em repositórios públicos, ou ações publicadas em registros do Docker. Nem todas as etapas executam ações, mas todas as ações são executadas como etapas. Cada etapa é executada em seu próprio processo no ambiente do executor, tendo acesso ao espaço de trabalho e ao sistema de arquivos. Como as etapas são executadas em seus próprios processos, as alterações nas variáveis de ambiente não são preservadas entre as etapas.
GitHub fornece etapas internas para configurar e concluir um trabalho.

GitHub exibe apenas as primeiras 1.000 verificações, no entanto, você pode executar um número ilimitado de etapas, desde que esteja dentro dos limites de uso do fluxo de trabalho. Para obter mais informações, consulte [Cobrança e uso](../../concepts/billing-and-usage.md) sobre executores hospedados em GitHub e [Limites do Actions](../limits.md) para limites de uso de executores auto-hospedados.

### Exemplo de `jobs.<job_id>.steps`

```yaml
name: Greeting from Mona

on: push

jobs:
  my-job:
    name: My Job
    runs-on: ubuntu-latest
    steps:
      - name: Print a greeting
        env:
          MY_VAR: Hi there! My name is
          FIRST_NAME: Mona
          MIDDLE_NAME: The
          LAST_NAME: Octocat
        run: |
          echo $MY_VAR $FIRST_NAME $MIDDLE_NAME $LAST_NAME.
```

## `jobs.<job_id>.steps[*].id`

Identificador exclusivo da etapa. Use a `id` para referenciar a etapa em contextos. Para saber mais, confira [Referência de contextos](contexts.md).

## `jobs.<job_id>.steps[*].if`

Use o condicional `if` para impedir que uma etapa seja executada, a não ser que uma condição seja atendida. Você pode usar qualquer contexto e expressão compatível para criar uma condicional. Para obter mais informações sobre quais contextos têm suporte nessa chave, confira [Referência de contextos](contexts.md#context-availability).

Ao usar expressões em um condicional `if`, opcionalmente, você poderá omitir a sintaxe de expressão `${{ }}`, pois o GitHub Actions avalia automaticamente o condicional `if` como uma expressão. No entanto, essa exceção não se aplica a todos os lugares.

Você sempre deverá usar a sintaxe de expressão `${{ }}` ou escapar com `''`, `""` ou `()` quando a expressão começar com `!`, já que `!` é a notação reservada no formato YAML. Por exemplo:

```yaml
if: ${{ ! startsWith(github.ref, 'refs/tags/') }}
```

Para obter mais informações, consulte [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

### Exemplo: Usando contextos

Essa etapa só é executada quando o tipo de evento é uma `pull_request` e a ação do evento é `unassigned`.

```yaml
steps:
  - name: My first step
    if: ${{ github.event_name == 'pull_request' && github.event.action == 'unassigned' }}
    run: echo This event is a pull request that had an assignee removed.
```

### Exemplo: Usando funções de verificação de status

A `my backup step` só é executada quando a etapa anterior de um trabalho falha. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md#status-check-functions).

```yaml
steps:
  - name: My first step
    uses: octo-org/action-name@main
  - name: My backup step
    if: ${{ failure() }}
    uses: actions/heroku@1.0.0
```

### Exemplo: Usando segredos

Não é possível referenciar segredos diretamente em condicionais `if:`. Em vez disso, considere definir segredos como variáveis de ambiente no nível de trabalho e, em seguida, fazer referência às variáveis de ambiente para executar etapas condicionalmente no trabalho.

Se um segredo não tiver sido definido, o valor retornado de uma expressão referenciando o segredo (como `${{ secrets.SuperSecret }}` no exemplo) será uma cadeia de caracteres vazia.

```yaml
name: Run a step if a secret has been set
on: push
jobs:
  my-jobname:
    runs-on: ubuntu-latest
    env:
      super_secret: ${{ secrets.SuperSecret }}
    steps:
      - if: ${{ env.super_secret != '' }}
        run: echo 'This step will only run if the secret has a value set.'
      - if: ${{ env.super_secret == '' }}
        run: echo 'This step will only run if the secret does not have a value set.'
```

Para saber mais, confira [Referência de contextos](contexts.md#context-availability) e [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

## `jobs.<job_id>.steps[*].name`

Um nome para sua etapa ser exibida em GitHub.

## `jobs.<job_id>.steps[*].uses`

Seleciona uma ação para executar como parte de uma etapa no trabalho. A ação é uma unidade reutilizável de código. Você pode usar uma ação definida no mesmo repositório do fluxo de trabalho, um repositório público ou em uma [imagem publicada de um contêiner do Docker](https://hub.docker.com/).

É altamente recomendável incluir a versão da ação que você está usando especificando uma referência de Git, SHA ou uma marca do Docker. Se você não especificar uma versão, ela poderá interromper seus fluxos de trabalho ou causar um comportamento inesperado quando o proprietário da ação publicar uma atualização.

* Usar o commit SHA de uma versão de ação lançada é a maneira mais garantida de obter estabilidade e segurança.
* Se a ação publicar marcas de versão principal, você deverá esperar receber correções críticas e patches de segurança enquanto ainda mantém a compatibilidade. Observe que esse comportamento fica a critério do autor da ação.
* Usar o branch-padrão de uma ação pode ser conveniente, mas se alguém lançar uma nova versão principal com uma mudança significativa, seu fluxo de trabalho poderá ter problemas.

Algumas ações exigem entradas que precisam ser definidas com a palavra-chave [`with`](#jobsjob_idstepswith). Revise o arquivo README da ação para determinar as entradas obrigatórias.

As ações podem ser ações JavaScript, ações compostas ou ações de contêiner do Docker. Se a ação em uso for um contêiner do Docker, você deverá executar o trabalho em um ambiente do Linux. Para obter mais detalhes, consulte [`runs-on`](#jobsjob_idruns-on).

### Exemplo: Usando ações de versão

```yaml
steps:
  # Reference a specific commit
  - uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3
  # Reference the major version of a release
  - uses: actions/checkout@v6
  # Reference a specific version
  - uses: actions/checkout@v6.2.0
  # Reference a branch
  - uses: actions/checkout@main
```

### Exemplo: Usando uma ação pública

`{owner}/{repo}@{ref}`

Você pode especificar um branch, ref ou SHA em um repositório público GitHub.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        # Uses the default branch of a public repository
        uses: actions/heroku@main
      - name: My second step
        # Uses a specific version tag of a public repository
        uses: actions/aws@v2.0.1
```

### Exemplo: Usando uma ação pública em um subdiretório

`{owner}/{repo}/{path}@{ref}`

Um subdiretório em um repositório público GitHub em uma ramificação, ref ou SHA específico.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: actions/aws/ec2@main
```

### Exemplo: usar uma ação no mesmo repositório que o fluxo de trabalho no commit em execução (recomendado)

`$/path/to/action`

O prefixo `$/` é a referência ao próprio repositório. Ele faz referência a uma ação armazenada no mesmo repositório que o fluxo de trabalho ou a ação em execução no momento e é resolvido para esse repositório no commit em execução (o mesmo SHA do fluxo de trabalho ou da ação em execução). Você não precisa fazer check-out do repositório primeiro, portanto, é a maneira recomendada de referenciar uma ação em seu próprio repositório.

A `$/` sintaxe não está disponível em GitHub Enterprise Server.

Uma `$/` referência não deve incluir um `@{ref}` sufixo. A ref é sempre o commit que o fluxo de trabalho ou a ação em execução está usando, portanto uma referência como `$/actions/my-action@v1` é inválida.

`$/` sempre é resolvido com base no repositório do arquivo em que aparece, não no repositório que o chamou. Por exemplo, se um fluxo de trabalho reutilizável em um repositório for acionado por um fluxo de trabalho em outro repositório, uma referência `$/` no fluxo de trabalho chamado remete ao repositório desse fluxo de trabalho, e não ao repositório do fluxo de trabalho que o chama. Isso torna `$/` confiável para a composição de ações, ao passo que um caminho relativo `./` seria resolvido com base no que estiver extraído no workspace de quem chama a ação. Para usar `$/` nas etapas de uma ação composta, consulte [Referência de sintaxe de metadados](metadata-syntax.md#runsstepsuses).

A tabela a seguir compara as maneiras de referenciar uma ação.

| Sintaxe | É resolvido desta forma | Recomendado para |
| --- | --- | --- |
| `$/path/to/action` | O mesmo repositório do workflow ou da action em execução, no commit em execução | Ações no mesmo repositório |
| `{owner}/{repo}@{ref}` | O repositório especificado na ref especificada | Ações em outro repositório |
| `./path/to/action` | Um caminho no workspace do runner, relativo ao diretório de trabalho padrão (`${{ github.workspace }}`) | Somente casos extremos |

```yaml
on: [push]

jobs:
  my_first_job:
    runs-on: ubuntu-latest
    steps:
      # References an action in the same repository at the running commit
      - uses: $/.github/actions/hello-world-action
```

### Exemplo: Usando uma ação no mesmo repositório que o fluxo de trabalho

`./path/to/dir`

Caminho para o diretório que contém a ação no repositório do seu fluxo de trabalho. Você deve fazer o checkout do seu repositório antes de usar a action, e o caminho `./` é resolvido em relação ao workspace do runner, em vez de ao repositório do workflow em execução. Para a maioria dos casos, use a `$/` sintaxe mostrada acima.

Exemplo de estrutura de arquivo de repositório:

```shell
|-- hello-world (repository)
|   |__ .github
|       └── workflows
|           └── my-first-workflow.yml
|       └── actions
|           |__ hello-world-action
|               └── action.yml
```

O caminho é relativo (`./`) ao diretório de trabalho padrão (`github.workspace`, `$GITHUB_WORKSPACE`). Se a ação fizer check-out do repositório para um local diferente do fluxo de trabalho, o caminho relativo usado para ações locais deverá ser atualizado.

Exemplo de arquivo de fluxo de trabalho:

```yaml
jobs:
  my_first_job:
    runs-on: ubuntu-latest
    steps:
      # This step checks out a copy of your repository.
      - name: My first step - check out repository
        uses: actions/checkout@v6
      # This step references the directory that contains the action.
      - name: Use local hello-world-action
        uses: ./.github/actions/hello-world-action
```

### Exemplo: Usando uma ação do Docker Hub

`docker://{image}:{tag}`

Uma imagem do Docker publicada no [Docker Hub](https://hub.docker.com/).

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: docker://alpine:3.8
```

### Exemplo: usando o GitHub PackagesContainer registry

`docker://{host}/{image}:{tag}`

Uma imagem pública do Docker na GitHub PackagesContainer registry.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: docker://ghcr.io/OWNER/IMAGE_NAME
```

### Exemplo: Usando uma ação do registro público do Docker

`docker://{host}/{image}:{tag}`

Imagem Docker em um registro público. Este exemplo usa o Registro de Contêiner do Google em `gcr.io`.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: docker://gcr.io/cloud-builders/gradle
```

### Exemplo: Usando uma ação dentro de um repositório privado diferente do fluxo de trabalho

Se a ação estiver em um repositório interno ou em um repositório privado configurado para permitir o acesso do repositório do seu fluxo de trabalho, você poderá referenciar a ação diretamente. Para obter mais informações, consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository) e [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-access-to-components-in-a-private-repository).

Se a ação não estiver em um repositório configurado para permitir acesso, você precisará verificar o repositório e referenciar a ação localmente. Gere um personal access token e adicione o token como um segredo. O exemplo a seguir mostra esse método para referenciar uma ação. Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) e [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

Substitua `PERSONAL_ACCESS_TOKEN` no exemplo pelo nome do segredo.

```yaml
jobs:
  my_first_job:
    steps:
      - name: Check out repository
        uses: actions/checkout@v6
        with:
          repository: octocat/my-private-repo
          ref: v1.0
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          path: ./.github/actions/my-private-repo
      - name: Run my action
        uses: ./.github/actions/my-private-repo/my-action
```

Como alternativa, use um GitHub App em vez de um personal access token para garantir que seu fluxo de trabalho continue sendo executado mesmo se o personal access token proprietário sair. Para saber mais, confira [Fazer solicitações de API autenticadas com um aplicativo GitHub em um fluxo de trabalho GitHub Actions](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow).

## `jobs.<job_id>.steps[*].run`

Executa programas de linha de comando que não excedem 21.000 caracteres usando o shell do sistema operacional. Se você não informar um `name`, o nome da etapa usará como padrão o texto indicado no comando `run`.

Por padrão, os comandos run usam shells que nao são de login. Você pode escolher um shell diferente e personalizar o shell usado para executar comandos. Para obter mais informações, consulte [`jobs.<job_id>.steps[*].shell`](#jobsjob_idstepsshell).

Cada palavra-chave `run` representa um novo processo e um shell no ambiente do executor. Ao fornecer comandos de várias linhas, cada linha será executada no mesmo shell. Por exemplo:

* Um comando de linha única:

        ```yaml
  - name: Install Dependencies
    run: npm install
  ```

* Um comando de várias linhas:

        ```yaml
  - name: Clean install dependencies and build
    run: |
      npm ci
      npm run build
  ```

## `jobs.<job_id>.steps[*].working-directory`

Com a palavra-chave `working-directory`, é possível especificar o diretório de trabalho do qual o comando será executado.

```yaml
- name: Clean temp directory
  run: rm -rf *
  working-directory: ./temp
```

Como alternativa, você pode especificar um diretório de trabalho padrão para todas as etapas `run` em um trabalho ou para todas as etapas `run` em todo o fluxo de trabalho. Para obter mais informações, consulte [`defaults.run.working-directory`](workflow-syntax.md#defaultsrunworking-directory) e [`jobs.<job_id>.defaults.run.working-directory`](workflow-syntax.md#jobsjob_iddefaultsrunworking-directory).

Você também pode usar uma etapa `run` para executar um script. Para saber mais, confira [Adicionar scripts ao seu fluxo de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/add-scripts.md).

## `jobs.<job_id>.steps[*].shell`

Substitua as configurações padrão do shell no sistema operacional do executor e o padrão do trabalho usando a palavra-chave `shell`. É possível usar palavras-chave `shell` internas ou definir um conjunto personalizado de opções de shell. O comando do shell que é executado internamente executa um arquivo temporário que contém os comandos especificados na palavra-chave `run`.

| Plataforma compatível | Parâmetro `shell` | Descrição | Comando executado internamente |
| --- | --- | --- | --- |
| Linux / macOS | não especificado | O shell padrão em plataformas não Windows. Isso executa um comando diferente para quando `bash` é especificado explicitamente. Se `bash` não for encontrado no caminho, isso será tratado como `sh`. | `bash -e {0}` |
| Tudo | `bash` | O shell padrão em plataformas não Windows com um fallback para `sh`. Ao especificar um shell bash no Windows, é utilizado o shell bash incluído no Git para Windows. | `bash --noprofile --norc -eo pipefail {0}` |
| Tudo | `pwsh` | Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `pwsh -command ". '{0}'"` |
| Tudo | `python` | Executa o comando python. | `python {0}` |
| Linux / macOS | `sh` | O comportamento de fallback para plataformas não Windows se nenhum shell for fornecido e o `bash` não for encontrado no caminho. | `sh -e {0}` |
| Windows | `cmd` | O GitHub acrescenta a extensão `.cmd` ao nome do script e a substitui por `{0}`. | `%ComSpec% /D /E:ON /V:OFF /S /C "CALL "{0}""`. |
| Windows | `pwsh` | Essa é a shell padrão usada no Windows. Powershell Core. O GitHub acrescenta a extensão `.ps1` ao nome do script. Se o executor auto-hospedado do Windows não tiver o *PowerShell Core* instalado, o *PowerShell Desktop* será usado. | `pwsh -command ". '{0}'"`. |
| Windows | `powershell` | O PowerShell Desktop. O GitHub acrescenta a extensão `.ps1` ao nome do script. | `powershell -command ". '{0}'"`. |

Como alternativa, você pode especificar um shell padrão para todas as etapas `run` em um trabalho ou para todas as etapas `run` em todo o fluxo de trabalho. Para obter mais informações, consulte [`defaults.run.shell`](workflow-syntax.md#defaultsrunshell) e [`jobs.<job_id>.defaults.run.shell`](workflow-syntax.md#jobsjob_iddefaultsrunshell).

### Exemplo: executar um comando usando o Bash

```yaml
steps:
  - name: Display the path
    shell: bash
    run: echo $PATH
```

### Exemplo: executar um comando usando o Windows `cmd`

```yaml
steps:
  - name: Display the path
    shell: cmd
    run: echo %PATH%
```

### Exemplo: executar um comando usando o PowerShell Core

```yaml
steps:
  - name: Display the path
    shell: pwsh
    run: echo ${env:PATH}
```

### Exemplo: usar o PowerShell Desktop para executar um comando

```yaml
steps:
  - name: Display the path
    shell: powershell
    run: echo ${env:PATH}
```

### Exemplo: executar um script do Python embutido

```yaml
steps:
  - name: Display the path
    shell: python
    run: |
      import os
      print(os.environ['PATH'])
```

### Shell personalizado

Você pode definir o valor `shell` como uma cadeia de caracteres de modelo usando `command [options] {0} [more_options]`.
GitHub interpreta a primeira palavra delimitada pelo espaço em branco da cadeia de caracteres como o comando e insere o nome do arquivo para o script temporário em `{0}`.

Por exemplo:

```yaml
steps:
  - name: Display the environment variables and their values
    shell: perl {0}
    run: |
      print %ENV
```

O comando usado, `perl` neste exemplo, precisa ser instalado no executor.

Para obter informações sobre o software incluído nos executores hospedados no GitHub, consulte [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

### Preferências de ação de erro e códigos de saída

Para palavras-chave de shell integradas, fornecemos os seguintes padrões que são executados por executores hospedados em GitHub. Você deve seguir estas diretrizes quando executar scripts shell.

* `bash`
  /
  `sh`:
  * Por padrão, o comportamento fail fast é imposto usando `set -e` para `sh` e `bash`. Quando `shell: bash` é especificado, `-o pipefail` também é aplicado para impor a saída antecipada de pipelines que geram um status de saída diferente de zero.
  * Você pode ter controle total sobre os parâmetros do shell fornecendo uma string de modelo para as opções do shell. Por exemplo, `bash {0}`.
  * ```
              Shells do tipo `sh` saem com o código de saída do último comando executado em um script, que também é o comportamento padrão das ações. O executor relatará o status da etapa como falha/êxito com base nesse código de saída.
                ```

* `powershell`/`pwsh`
  * Comportamento fail-fast quando possível. Para `pwsh` e o shell interno `powershell`, prefixaremos `$ErrorActionPreference = 'stop'` ao conteúdo do script.
  * Prefixamos `if ((Test-Path -LiteralPath variable:\LASTEXITCODE)) { exit $LASTEXITCODE }` aos scripts do PowerShell para que os status de ação reflitam o último código de saída do script.
  * Os usuários sempre podem recusar o uso do shell interno e fornecer uma opção de shell personalizada como: `pwsh -File {0}` ou `powershell -Command "& '{0}'"`, dependendo da necessidade.

* `cmd`
  * Parece não haver uma forma de optar totalmente por um comportamento fail-fast que não seja gravar seu script para verificar cada código de erro e reagir de acordo. Como não podemos fornecer esse comportamento por padrão, você precisa gravá-lo em seu script.
  * `cmd.exe` sairá com o nível de erro do último programa que executou e retornará o código de erro para o executor. Esse comportamento é internamente consistente com o comportamento anterior de `sh` e `pwsh` padrão e é o `cmd.exe` padrão. Portanto, esse comportamento permanece intacto.

## `jobs.<job_id>.steps[*].with`

Um `map` dos parâmetros de entrada definidos pela ação. Cada parâmetro de entrada é um par chave/valor. Parâmetros de entrada são definidos como variáveis de ambiente. A variável é precedida por `INPUT_` e convertida em letras maiúsculas.

Os parâmetros de entrada definidos para um contêiner do Docker devem usar `args`. Para obter mais informações, consulte [`jobs.<job_id>.steps[*].with.args`](#jobsjob_idstepswithargs).

### Exemplo de `jobs.<job_id>.steps[*].with`

Define os três parâmetros de entrada (`first_name`, `middle_name` e `last_name`) definidos pela ação `hello_world`. Essas variáveis de entrada estarão acessíveis para a ação `hello-world` como variáveis de ambiente `INPUT_FIRST_NAME`, `INPUT_MIDDLE_NAME` e `INPUT_LAST_NAME`.

```
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: actions/hello_world@main
        with:
          first_name: Mona
          middle_name: The
          last_name: Octocat
```

## `jobs.<job_id>.steps[*].with.args`

Uma `string` que define as entradas para um contêiner do Docker.               O GitHub passa o `args` para o `ENTRYPOINT` do contêiner quando o contêiner é iniciado. Não há suporte para uma `array of strings` nesse parâmetro. Um único argumento que inclui espaços deve ser cercado por aspas duplas `""`.

### Exemplo de `jobs.<job_id>.steps[*].with.args`

```
steps:
  - name: Explain why this job ran
    uses: octo-org/action-name@main
    with:
      entrypoint: /bin/echo
      args: The ${{ github.event_name }} event triggered this step.
```

Os `args` são usados no lugar da instrução `CMD` em um `Dockerfile`. Se você usar `CMD` no `Dockerfile`, use as diretrizes ordenadas por preferência:

1. Documente os argumentos necessários no README da ação e omita-os da instrução `CMD`.
2. Use padrões que permitam o uso da ação sem a especificação de `args`.
3. Se a ação expõe um sinalizador `--help` ou algo do tipo, use isso como o padrão para que a ação seja documentada automaticamente.

## `jobs.<job_id>.steps[*].with.entrypoint`

Substitui o `ENTRYPOINT` do Docker no `Dockerfile` ou define-o se um ainda não foi especificado. Ao contrário da instrução `ENTRYPOINT` do Docker que tem um shell e um formulário executável, a palavra-chave `entrypoint` só aceita uma cadeia de caracteres individual que define o executável para execução.

### Exemplo de `jobs.<job_id>.steps[*].with.entrypoint`

```
steps:
  - name: Run a custom command
    uses: octo-org/action-name@main
    with:
      entrypoint: /a/different/executable
```

A palavra-chave `entrypoint` destina-se a ser usada com as ações de contêiner do Docker, mas você também pode usá-la com as ações JavaScript que não definem nenhuma entrada.

## `jobs.<job_id>.steps[*].env`

Define variáveis para etapas a serem usadas no ambiente do executor. Também é possível definir variáveis para todo o fluxo de trabalho ou para um trabalho. Para obter mais informações, consulte [`env`](#env) e [`jobs.<job_id>.env`](#jobsjob_idenv).

Quando mais de uma variável de ambiente é definida com o mesmo nome, GitHub usa a variável mais específica. Por exemplo, uma variável de ambiente definida em uma etapa substituirá as variáveis de ambiente do trabalho e do fluxo de trabalho que tenham o mesmo nome enquanto a etapa é executada. Uma variável de ambiente definida para um trabalho substituirá uma variável de fluxo de trabalho com o mesmo nome enquanto o trabalho é executado.

Ações públicas podem especificar variáveis esperadas no arquivo LEIAME. Se você estiver definindo um valor secreto ou confidencial, como uma senha ou um token, deverá definir segredos usando o contexto `secrets`. Para saber mais, confira [Referência de contextos](contexts.md).

### Exemplo de `jobs.<job_id>.steps[*].env`

```
steps:
  - name: My first action
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      FIRST_NAME: Mona
      LAST_NAME: Octocat
```

## `jobs.<job_id>.steps[*].continue-on-error`

Impede a falha de um trabalho se uma etapa não funcionar. Defina isso como `true` para permitir que um trabalho seja aprovado quando houver uma falha nessa etapa.

## `jobs.<job_id>.steps[*].timeout-minutes`

Número máximo de minutos para executar a etapa antes de interromper o processo. Máximo: 360 para executores hospedados em GitHub e auto-hospedados.

Valores fracionados não são compatíveis.
`timeout-minutes` deve ser um número inteiro positivo.

## `jobs.<job_id>.steps[*].background`

Executa uma etapa de forma assíncrona para que o trabalho continue para a próxima etapa sem esperar que ela seja concluída. Use `background: true` para processos de execução longa, como bancos de dados, servidores ou tarefas de monitoramento, que precisam ser executados junto com outras etapas. Você sincroniza com as etapas em segundo plano mais tarde usando [`wait`](#jobsjob_idstepswait) ou [`wait-all`](#jobsjob_idstepswait-all) interrompendo-as com [`cancel`](#jobsjob_idstepscancel).

Você pode usar `background` em etapas que usam `run` ou `uses`. Para fazer referência a uma etapa em segundo plano de [`wait`](#jobsjob_idstepswait) ou [`cancel`](#jobsjob_idstepscancel), dê-lhe um [`id`](#jobsjob_idstepsid). No máximo, 10 etapas em segundo plano podem ser executadas simultaneamente em uma única tarefa; etapas adicionais em segundo plano ficam enfileiradas até haver uma vaga livre.

As saídas e as alterações de ambiente de uma etapa em segundo plano somente ficam disponíveis após a execução de uma etapa `wait` ou `wait-all` que inclua essa etapa. Se uma etapa em segundo plano falhar, o trabalho falhará na próxima `wait` ou `wait-all` que a inclui (a menos que [`continue-on-error`](#jobsjob_idstepscontinue-on-error) esteja definida nessa etapa). Uma `wait-all` implícita é executada antes de qualquer limpeza pós-tarefa.

Use `background` quando precisar de um controle refinado: iniciar um processo de execução longa (como um servidor ou banco de dados) que permaneça ativo enquanto as etapas posteriores são executadas, fazendo referência a uma etapa específica com [`wait`](#jobsjob_idstepswait) ou [`cancel`](#jobsjob_idstepscancel)ou intercalando o trabalho em segundo plano com outras etapas. Se, em vez disso, você tiver um grupo independente de etapas que devam ser concluídas antes que o trabalho continue, [`parallel`](#jobsjob_idstepsparallel) é uma forma abreviada mais conveniente.

!!! note
    Você não pode usar `background` em etapas dentro de uma ação composta. Uma ação composta pode ser executada como uma etapa em segundo plano, mas não pode declarar etapas em segundo plano internamente.

### Exemplo: executando uma etapa em segundo plano

```
steps:
  - name: Start server
    id: server
    run: npm start
    background: true

  - name: Run tests against the server
    run: npm test

  - name: Wait for the server step to finish
    wait: server
```

## `jobs.<job_id>.steps[*].wait`

Pausa o trabalho até que uma ou mais etapas em segundo plano sejam concluídas. Uma `wait` etapa não executa nenhum trabalho em si, ela só é bloqueada até que as etapas em segundo plano referenciadas sejam concluídas. Forneça uma única etapa `id` como uma cadeia de caracteres ou várias etapas `id`como uma matriz.

Após a conclusão de uma etapa `wait`, as saídas das etapas em segundo plano referenciadas tornam-se disponíveis para as etapas subsequentes. Se uma etapa em segundo plano referenciada falhar, a `wait` etapa também falhará.

!!! note
    Uma `wait` etapa sempre é executada e não oferece suporte à condicional [`if`](#jobsjob_idstepsif).

### Exemplo: aguardando etapas específicas em segundo plano

```
steps:
  - name: Build frontend
    id: build-frontend
    run: npm run build:frontend
    background: true

  - name: Build backend
    id: build-backend
    run: npm run build:backend
    background: true

  - name: Run linter while builds run
    run: npm run lint

  - name: Wait for both builds to finish
    wait: [build-frontend, build-backend]

  - name: Run tests
    run: npm test
```

## `jobs.<job_id>.steps[*].wait-all`

Pausa o trabalho até que todas as etapas em segundo plano ativas sejam concluídas. Isso é útil quando várias etapas em segundo plano estão em execução e você deseja que todas elas sejam concluídas antes de continuar. Assim como `wait`, a etapa `wait-all` falhará se qualquer uma das etapas em segundo plano das quais ela depende falhar, a menos que você defina [`continue-on-error`](#jobsjob_idstepscontinue-on-error) como `true`.

A `wait-all` palavra-chave não usa argumentos.

!!! note
    Uma `wait-all` etapa sempre é executada e não oferece suporte à condicional [`if`](#jobsjob_idstepsif).

### Exemplo: aguardando todas as etapas em segundo plano

```
steps:
  - name: Start database
    id: db
    run: docker run -d postgres:15
    background: true

  - name: Start cache
    id: cache
    run: docker run -d redis:7
    background: true

  - name: Run integration tests
    run: npm run test:integration

  - name: Wait for all services to stop
    wait-all:
```

## `jobs.<job_id>.steps[*].cancel`

Encerra de forma controlada uma etapa em segundo plano em execução. O executor envia ao processo da etapa um sinal de terminação (`SIGTERM`) para que ele possa limpar e o interrompe à força (`SIGKILL`) se ele não sair em um curto período de carência. A palavra-chave `cancel` tem como alvo uma única etapa de segundo plano pelo seu `id`.

!!! note
    Uma `cancel` etapa sempre é executada e não oferece suporte à condicional [`if`](#jobsjob_idstepsif).

### Exemplo: Cancelando uma etapa em segundo plano

```
steps:
  - name: Start long-running monitor
    id: monitor
    run: ./scripts/monitor.sh
    background: true

  - name: Run the main task
    run: npm test

  - name: Stop the monitor
    cancel: monitor
```

## `jobs.<job_id>.steps[*].parallel`

Executa um grupo de etapas simultaneamente e aguarda que todas elas sejam concluídas antes de continuar. A palavra-chave `parallel` é uma forma abreviada: cada etapa do grupo é executada em segundo plano, com um `wait` implícito no final do grupo. Use-o quando você tiver um grupo independente de etapas que possa ser executado ao mesmo tempo e não precisar referenciá-las individualmente.

Use `parallel` quando houver um grupo independente de etapas em que todas devem ser concluídas antes que a tarefa prossiga, como criar vários componentes de uma só vez. Use [`background`](#jobsjob_idstepsbackground) quando precisar de um controle mais fino: iniciar um processo de execução longa (como um servidor ou banco de dados) que permaneça ativo enquanto as etapas posteriores são executadas, fazendo referência a uma etapa específica com [`wait`](#jobsjob_idstepswait) ou [`cancel`](#jobsjob_idstepscancel)ou intercalando o trabalho em segundo plano com outras etapas. Em suma, `parallel` é mais limitado, mas mais conveniente para o caso de "executar este grupo de uma só vez", enquanto `background` é a primitiva de uso geral.

Cada etapa do grupo está sujeita ao mesmo limite de simultaneidade de 10 etapas aplicado às outras etapas em segundo plano.

!!! note
    Você não pode usar `parallel` dentro de uma ação composta.

### Exemplo: executando etapas em paralelo

```
steps:
  - uses: actions/checkout@v6

  - parallel:
      - name: Build frontend
        run: npm run build:frontend

      - name: Build backend
        run: npm run build:backend

      - name: Build docs
        run: npm run build:docs

  - name: Run tests after all builds complete
    run: npm test
```

O grupo acima é equivalente a declarar cada etapa com `background: true`, seguida por uma etapa `wait`.

## `jobs.<job_id>.timeout-minutes`

O número máximo de minutos para permitir que o trabalho seja executado antes que GitHub o cancele automaticamente. Padrão: 360

Se o tempo-limite exceder o tempo limite de execução do trabalho para o executor, o trabalho será cancelado quando o tempo limite de execução for atingido. Para obter mais informações sobre os limites de tempo de execução de trabalho, consulte [Cobrança e uso](../../concepts/billing-and-usage.md#usage-limits-and-policy) para executores hospedados em GitHub e, para limites de uso de executores auto-hospedados, consulte [Limites do Actions](../limits.md).

!!! note
    O `GITHUB_TOKEN` expira quando um trabalho é concluído ou após, no máximo, 24 horas. Para executores auto-hospedados, o token pode ser o fator limitante se o tempo limite do trabalho for maior que 24 horas. Para obter mais informações sobre `GITHUB_TOKEN`, consulte [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).

## `jobs.<job_id>.strategy`

Com o `jobs.<job_id>.strategy` você usa uma estratégia de matriz para seus trabalhos.
Uma estratégia de matriz permite que você use variáveis em uma única definição de trabalho para criar automaticamente várias execuções de trabalho baseadas nas combinações das variáveis. Por exemplo, você pode usar uma estratégia de matriz para testar seu código em várias versões de um idioma ou em vários sistemas operacionais. Para obter mais informações, consulte [Executando variações de tarefas em um workflow](../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md).

## `jobs.<job_id>.strategy.matrix`

Use `jobs.<job_id>.strategy.matrix` para definir uma matriz de diferentes configurações de trabalho. Para saber mais, confira [Executando variações de tarefas em um workflow](../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md).

Uma matriz pode gerar 256 tarefas no máximo por execução do fluxo de trabalho. Esse limite se aplica a executores hospedados em GitHub e auto-hospedados.

As variáveis que você define se tornam propriedades no contexto `matrix`, e você pode referenciar a propriedade em outras áreas do arquivo de fluxo de trabalho. Neste exemplo, você pode usar `matrix.version` e `matrix.os` para acessar o valor atual de `version` e `os` que o trabalho está usando. Para saber mais, confira [Referência de contextos](contexts.md).

!!! note
    Os nomes das variáveis não fazem distinção entre maiúsculas e minúsculas. Por exemplo, `OS` e `os` será tratado como a mesma variável.

Por padrão, GitHub maximizará o número de trabalhos executados em paralelo, dependendo da disponibilidade do executor. A ordem das variáveis na matriz determina a ordem na qual os trabalhos são criados. A primeira variável definida será o primeiro trabalho criado na execução do fluxo de trabalho.

### Como usar uma matriz unidimensional

O fluxo de trabalho a seguir define a variável `version` com os valores `[10, 12, 14]`. O fluxo de trabalho executará três trabalhos, um para cada valor na variável. Cada trabalho acessará o valor `version` por meio do contexto `matrix.version` e passará o valor como `node-version` à ação `actions/setup-node`.

```
jobs:
  example_matrix:
    strategy:
      matrix:
        version: [10, 12, 14]
    steps:
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.version }}
```

### Como usar uma matriz multidimensional

Especifique diversas variáveis para criar uma matriz multidimensional. Um trabalho será executado para cada combinação possível das variáveis.

Por exemplo, o fluxo de trabalho a seguir especifica duas variáveis:

* Dois sistemas operacionais especificados na variável `os`
* Três versões do Node.js especificadas na variável `version`

O fluxo de trabalho executará seis trabalhos, um para cada combinação entre as variáveis `os` e `version`. Cada trabalho definirá o valor `runs-on` como o valor atual `os` e passará o valor atual `version` para a ação `actions/setup-node`.

```
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-24.04]
        version: [10, 12, 14]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.version }}
```

Uma configuração variável em uma matriz pode ser um `array` de `object`s. Por exemplo, a matriz a seguir produz quatro trabalhos com contextos correspondentes.

```
matrix:
  os:
    - ubuntu-latest
    - macos-latest
  node:
    - version: 14
    - version: 20
      env: NODE_OPTIONS=--openssl-legacy-provider
```

Cada trabalho na matriz terá uma combinação própria de valores `os` e `node`, como mostrado abaixo.

```
- matrix.os: ubuntu-latest
  matrix.node.version: 14
- matrix.os: ubuntu-latest
  matrix.node.version: 20
  matrix.node.env: NODE_OPTIONS=--openssl-legacy-provider
- matrix.os: macos-latest
  matrix.node.version: 14
- matrix.os: macos-latest
  matrix.node.version: 20
  matrix.node.env: NODE_OPTIONS=--openssl-legacy-provider
```

## `jobs.<job_id>.strategy.matrix.include`

Para cada objeto na lista `include`, os pares key:value no objeto serão adicionados a cada uma das combinações de matriz se nenhum dos pares key:value substituir qualquer um dos valores de matriz originais. Se o objeto não puder ser adicionado a nenhuma das combinações de matriz, uma nova combinação de matriz será criada. Observe que os valores de matriz originais não serão substituídos, mas os valores de matriz adicionados podem ser substituídos.

### Exemplo: expandindo configurações

Por exemplo, o fluxo de trabalho a seguir executará quatro trabalhos, um para cada combinação de `os` e `node`. Quando o trabalho para o valor `os` de `windows-latest` e valor `node` as execuções `16`, uma variável adicional chamada `npm` com o valor de `6` será incluída no trabalho.

```
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [windows-latest, ubuntu-latest]
        node: [14, 16]
        include:
          - os: windows-latest
            node: 16
            npm: 6
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v7
        with:
          node-version: ${{ matrix.node }}
      - if: ${{ matrix.npm }}
        run: npm install -g npm@${{ matrix.npm }}
      - run: npm --version
```

### Exemplo: adicionando configurações

Por exemplo, essa matriz executará dez trabalhos, um para cada combinação de `os` e `version` na matriz, além de um trabalho para o valor `os` de `windows-latest` e o valor `version` de `17`.

```
jobs:
  example_matrix:
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
        version: [12, 14, 16]
        include:
          - os: windows-latest
            version: 17
```

Se você não especificar nenhuma variável de matriz, todas as configurações abaixo de `include` serão executadas. Por exemplo, o fluxo de trabalho a seguir executaria dois trabalhos, um para cada entrada `include`. Isso permite que você aproveite a estratégia de matriz sem ter uma matriz totalmente populada.

```
jobs:
  includes_only:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - site: "production"
            datacenter: "site-a"
          - site: "staging"
            datacenter: "site-b"
```

## `jobs.<job_id>.strategy.matrix.exclude`

Uma configuração excluída só precisa ser uma correspondência parcial para que ela seja excluída.

Todas as combinações de `include` são processadas após `exclude`. Isso permite que você use `include` para adicionar combinações anteriores que já foram excluídas.

## `jobs.<job_id>.strategy.fail-fast`

Você pode controlar como as falhas de trabalho são tratadas com `jobs.<job_id>.strategy.fail-fast` e `jobs.<job_id>.continue-on-error`.

`jobs.<job_id>.strategy.fail-fast` aplica-se a toda a matriz. Se `jobs.<job_id>.strategy.fail-fast` estiver definido como `true` ou sua expressão for avaliada como `true`, o GitHub cancelará todos os trabalhos em andamento e enfileirados na matriz se algum trabalho na matriz falhar. Essa propriedade tem como padrão `true`.

`jobs.<job_id>.continue-on-error` aplica-se a um único trabalho. Se `jobs.<job_id>.continue-on-error` for `true`, outros trabalhos na matriz continuarão em execução mesmo que o trabalho com `jobs.<job_id>.continue-on-error: true` falhe.

Você não pode usar `jobs.<job_id>.strategy.fail-fast` e `jobs.<job_id>.continue-on-error` juntos. Por exemplo, o fluxo de trabalho a seguir iniciará quatro trabalhos. Para cada trabalho, `continue-on-error` é determinado pelo valor de `matrix.experimental`. Se algum dos trabalhos com `continue-on-error: false` falhar, todos os trabalhos em andamento ou enfileirados serão cancelados. Se o trabalho com `continue-on-error: true` falhar, os outros trabalhos não serão afetados.

```
jobs:
  test:
    runs-on: ubuntu-latest
    continue-on-error: ${{ matrix.experimental }}
    strategy:
      fail-fast: true
      matrix:
        version: [6, 7, 8]
        experimental: [false]
        include:
          - version: 9
            experimental: true
```

## `jobs.<job_id>.strategy.max-parallel`

Por padrão, GitHub maximizará o número de trabalhos executados em paralelo, dependendo da disponibilidade do executor.

## `jobs.<job_id>.continue-on-error`

`jobs.<job_id>.continue-on-error` aplica-se a um único trabalho. Se `jobs.<job_id>.continue-on-error` for `true`, outros trabalhos na matriz continuarão em execução mesmo que o trabalho com `jobs.<job_id>.continue-on-error: true` falhe.

Impede que ocorra falha na execução de um fluxo de trabalho quando ocorrer uma falha em um trabalho. Defina isso como `true` para permitir que uma execução de fluxo de trabalho seja aprovada quando houver uma falha nesse trabalho.

### Exemplo: Evitando uma falha específica na matriz de trabalho por falha na execução de um fluxo de trabalho

Você pode permitir que as tarefas específicas em uma matriz de tarefas falhem sem que ocorra falha na execução do fluxo de trabalho. Por exemplo, caso deseje permitir apenas um trabalho experimental com o `node` definido como `15` para falhar sem falhar a execução de fluxo de trabalho.

```
runs-on: ${{ matrix.os }}
continue-on-error: ${{ matrix.experimental }}
strategy:
  fail-fast: false
  matrix:
    node: [13, 14]
    os: [macos-latest, ubuntu-latest]
    experimental: [false]
    include:
      - node: 15
        os: ubuntu-latest
        experimental: true
```

## `jobs.<job_id>.container`

!!! note
    Se os fluxos de trabalho usarem ações de contêiner do Docker, contêineres de trabalho ou contêineres de serviço, você precisará usar um executor do Linux:

    * Se você estiver usando executores hospedados em GitHub, você deverá usar um executor do Ubuntu.
    * Se você estiver usando executores auto-hospedados, você deve usar uma máquina Linux, pois seu executor e o Docker precisam ser instalados.

Use `jobs.<job_id>.container` para criar um contêiner e executar as etapas de um trabalho que ainda não especificam um contêiner. Se você tiver etapas que usam ações de script e de contêiner, as ações de contêiner serão executadas como contêineres irmãos na mesma rede e com as mesmas montagens de volume.

Se você não definir um `container`, todas as etapas serão executadas diretamente no host especificado por `runs-on`, a menos que uma etapa se refira a uma ação configurada para ser executada em um contêiner.

!!! note
    O shell padrão para etapas `run` dentro de um contêiner é `sh` em vez de `bash`. Isso pode ser substituído por [`jobs.<job_id>.defaults.run`](workflow-syntax.md#jobsjob_iddefaultsrun) ou por [`jobs.<job_id>.steps[*].shell`](/pt/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsshell).

### Exemplo: Executar um trabalho dentro de um contêiner

```
name: CI
on:
  push:
    branches: [ main ]
jobs:
  container-test-job:
    runs-on: ubuntu-latest
    container:
      image: node:18
      env:
        NODE_ENV: development
      ports:
        - 80
      volumes:
        - my_docker_volume:/volume_mount
      options: --cpus 1
    steps:
      - name: Check for dockerenv file
        run: (ls /.dockerenv && echo Found dockerenv) || (echo No dockerenv)
```

Quando você especifica apenas uma imagem de contêiner, pode omitir a palavra-chave `image`.

```
jobs:
  container-test-job:
    runs-on: ubuntu-latest
    container: node:18
```

## `jobs.<job_id>.container.image`

Use `jobs.<job_id>.container.image` para definir a imagem do Docker a ser usada como o contêiner para executar a ação. O valor pode ser o nome da imagem do Docker Hub ou um nome de registro.

!!! note
    O Docker Hub normalmente impõe limites de taxa em operações de push e pull, o que afetará os trabalhos em executores auto-hospedados. No entanto, executores hospedados pelo GitHub não estão sujeitos a esses limites com base em um contrato entre o GitHub e o Docker.

## `jobs.<job_id>.container.credentials`

Se o registro de contêiner da imagem exigir autenticação para efetuar pull da imagem, use `jobs.<job_id>.container.credentials` para definir um `map` do `username` e da `password`. As credenciais são os mesmos valores que você fornecerá ao comando [`docker login`](https://docs.docker.com/engine/reference/commandline/login/).

### Exemplo: Definindo credenciais para o registro de um contêiner

```
container:
  image: ghcr.io/owner/image
  credentials:
     username: ${{ github.actor }}
     password: ${{ secrets.github_token }}
```

## `jobs.<job_id>.container.env`

Use `jobs.<job_id>.container.env` para definir um `map` das variáveis de ambiente no contêiner.

## `jobs.<job_id>.container.ports`

Use `jobs.<job_id>.container.ports` para definir uma `array` das portas a serem expostas no contêiner.

## `jobs.<job_id>.container.volumes`

Use `jobs.<job_id>.container.volumes` para definir uma `array` de volumes para uso do contêiner. É possível usar volumes para compartilhar dados entre serviços ou outras etapas em um trabalho. Você pode especificar volumes de nome Docker, volumes Docker anônimos ou vincular montagens no host.

Para especificar um volume, especifique o caminho de origem e destino:

`<source>:<destinationPath>`.

`<source>` é um nome de volume ou um caminho absoluto no computador host, e `<destinationPath>` é um caminho absoluto no contêiner.

### Exemplo: Montando volumes em um contêiner

```
volumes:
  - my_docker_volume:/volume_mount
  - /data/my_data
  - /source/directory:/destination/directory
```

## `jobs.<job_id>.container.options`

Use `jobs.<job_id>.container.options` para configurar opções adicionais de recurso de contêiner do Docker. Para ver uma lista de opções, confira [Opções de `docker create`](https://docs.docker.com/engine/reference/commandline/create/#options).

!!! warning
    As opções `--network` e `--entrypoint` não têm suporte.

## `jobs.<job_id>.services`

!!! note
    Se os fluxos de trabalho usarem ações de contêiner do Docker, contêineres de trabalho ou contêineres de serviço, você precisará usar um executor do Linux:

    * Se você estiver usando executores hospedados em GitHub, você deverá usar um executor do Ubuntu.
    * Se você estiver usando executores auto-hospedados, você deve usar uma máquina Linux, pois seu executor e o Docker precisam ser instalados.

Usado para hospedar contêineres de serviço para um trabalho em um fluxo de trabalho. Contêineres de serviço são úteis para a criação de bancos de dados ou serviços armazenamento em cache como o Redis. O executor cria automaticamente uma rede do Docker e gerencia o ciclo de vida dos contêineres do serviço.

Se você configurar seu trabalho para ser executado em um contêiner, ou a sua etapa usar ações ao contêiner, você não precisará mapear as portas para acessar o serviço ou a ação. O Docker expõe automaticamente todas as portas entre os contêineres da mesma rede de ponte definida pelo usuário. Você pode fazer referência ao contêiner de serviço diretamente pelo seu nome de host. O nome do host é mapeado automaticamente com o nome da etiqueta que você configurar para o serviço no fluxo de trabalho.

Se você configurar a tarefa para executar diretamente na máquina do executor e sua etapa não usar uma ação de contêiner, você deverá mapear todas as portas de contêiner de serviço do Docker necessárias para o host do Docker (a máquina do executor). Você pode acessar o contêiner de serviço usando host local e a porta mapeada.

Para obter mais informações sobre as diferenças entre os contêineres de serviço de rede, consulte [Comunicar-se com os contêineres de serviço do Docker](../../tutorials/use-containerized-services/use-docker-service-containers.md).

### Exemplo: Usando host local

Este exemplo cria dois serviços: nginx e redis. Quando você especifica a porta do contêiner, mas não a porta do host, a porta do contêiner é atribuída aleatoriamente a uma porta livre no host.
GitHub define a porta de host atribuída no contexto `${{job.services.<service_name>.ports}}`. Neste exemplo, você pode acessar as portas de host de serviço usando os `${{ job.services.nginx.ports['80'] }}` e `${{ job.services.redis.ports['6379'] }}` contextos.

```
services:
  nginx:
    image: nginx
    # Map port 8080 on the Docker host to port 80 on the nginx container
    ports:
      - 8080:80
  redis:
    image: redis
    # Map random free TCP port on Docker host to port 6379 on redis container
    ports:
      - 6379/tcp
steps:
  - run: |
      echo "Redis available on 127.0.0.1:${{ job.services.redis.ports['6379'] }}"
      echo "Nginx available on 127.0.0.1:${{ job.services.nginx.ports['80'] }}"
```

## `jobs.<job_id>.services.<service_id>.image`

Imagem Docker a ser usada como contêiner de serviço para executar a ação. O valor pode ser o nome da imagem do Docker Hub ou um nome de registro.

Se uma sequência vazia for atribuída a `jobs.<job_id>.services.<service_id>.image`, o serviço não será iniciado. Você pode usar essa condição para configurar serviços condicionais, conforme o exemplo a seguir.

```
services:
  nginx:
    image: ${{ options.nginx == true && 'nginx' || '' }}
```

## `jobs.<job_id>.services.<service_id>.credentials`

Se o registro de contêiner da imagem exigir autenticação para efetuar pull da imagem, use `jobs.<job_id>.container.credentials` para definir um `map` do `username` e da `password`. As credenciais são os mesmos valores que você fornecerá ao comando [`docker login`](https://docs.docker.com/engine/reference/commandline/login/).

### Exemplo de `jobs.<job_id>.services.<service_id>.credentials`

```
services:
  myservice1:
    image: ghcr.io/owner/myservice1
    credentials:
      username: ${{ github.actor }}
      password: ${{ secrets.github_token }}
  myservice2:
    image: dockerhub_org/myservice2
    credentials:
      username: ${{ secrets.DOCKER_USER }}
      password: ${{ secrets.DOCKER_PASSWORD }}
```

## `jobs.<job_id>.services.<service_id>.env`

Define um `map` das variáveis de ambiente no contêiner de serviço.

## `jobs.<job_id>.services.<service_id>.ports`

Define uma `array` de portas a serem expostas no contêiner de serviço.

## `jobs.<job_id>.services.<service_id>.volumes`

Define uma `array` de volumes para uso do contêiner de serviço. É possível usar volumes para compartilhar dados entre serviços ou outras etapas em um trabalho. Você pode especificar volumes de nome Docker, volumes Docker anônimos ou vincular montagens no host.

Para especificar um volume, especifique o caminho de origem e destino:

`<source>:<destinationPath>`.

`<source>` é um nome de volume ou um caminho absoluto no computador host, e `<destinationPath>` é um caminho absoluto no contêiner.

### Exemplo de `jobs.<job_id>.services.<service_id>.volumes`

```
volumes:
  - my_docker_volume:/volume_mount
  - /data/my_data
  - /source/directory:/destination/directory
```

## `jobs.<job_id>.services.<service_id>.options`

Opções adicionais de recursos do contêiner Docker. Para obter uma lista de opções, consulte [`docker create` opções](https://docs.docker.com/engine/reference/commandline/create/#options).

!!! warning
    Não há suporte para a opção `--network`.

## `jobs.<job_id>.services.<service_id>.command`

Substitui o comando padrão da imagem do Docker (`CMD`). O valor é passado como argumentos após o nome da imagem no `docker create` comando. Se você também especificar `entrypoint`, `command` fornecerá os argumentos para esse ponto de entrada.

### Exemplo de `jobs.<job_id>.services.<service_id>.command`

```
services:
  mysql:
    image: mysql:8
    command: --sql_mode=STRICT_TRANS_TABLES --max_allowed_packet=512M
    env:
      MYSQL_ROOT_PASSWORD: test
    ports:
      - 3306:3306
```

## `jobs.<job_id>.services.<service_id>.entrypoint`

Substitui o padrão `ENTRYPOINT` da imagem do Docker. O valor é uma única cadeia de caracteres que define o executável a ser executado. Use isso quando precisar substituir totalmente o ponto de entrada da imagem. Você pode combinar `entrypoint` com `command` para passar argumentos para o ponto de entrada personalizado.

### Exemplo de `jobs.<job_id>.services.<service_id>.entrypoint`

```
services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.17
    entrypoint: etcd
    command: >-
      --listen-client-urls http://0.0.0.0:2379
      --advertise-client-urls http://0.0.0.0:2379
    ports:
      - 2379:2379
```

## `jobs.<job_id>.uses`

O local e a versão de um arquivo de fluxo de trabalho reutilizável para ser executado como trabalho. Use uma das seguintes sintaxes:

* `$/.github/workflows/{filename}` para um fluxo de trabalho reutilizável no mesmo repositório. Essa é a sintaxe recomendada para referenciar um fluxo de trabalho reutilizável no mesmo repositório. Essa sintaxe não está disponível em GitHub Enterprise Server.
* `{owner}/{repo}/.github/workflows/{filename}@{ref}` para fluxos de trabalho reutilizáveis em repositórios públicos e privados.
* `./.github/workflows/{filename}` para fluxos de trabalho reutilizáveis no mesmo repositório.

Quando você faz referência a um fluxo de trabalho reutilizável com `{owner}/{repo}` e `@{ref}`, pode `{ref}` ser um SHA, uma marca de versão ou um nome de branch. Se uma tag de release e uma ramificação tiverem o mesmo nome, a tag de release terá precedência sobre o nome da ramificação. Usar o commit SHA é a opção mais segura para fins de estabilidade e segurança. Para saber mais, confira [Referência de uso seguro](../security/secure-use.md#reusing-third-party-workflows).

Quando você faz referência a um fluxo de trabalho reutilizável no mesmo repositório usando `$/` ou `./` (sem `{owner}/{repo}` e `@{ref}`), o fluxo de trabalho chamado é da mesma confirmação que o fluxo de trabalho do chamador. Uma `$/` referência não deve incluir um `@{ref}` sufixo e `$/` não está disponível em GitHub Enterprise Server. Prefixos de referência como `refs/heads` e `refs/tags` não são permitidos. Você não pode usar contextos ou expressões nesta palavra-chave.

### Exemplo de `jobs.<job_id>.uses`

```
jobs:
  call-workflow-1-in-local-repo:
    uses: octo-org/this-repo/.github/workflows/workflow-1.yml@172239021f7ba04fe7327647b213799853a9eb89
  call-workflow-2-in-local-repo:
    uses: ./.github/workflows/workflow-2.yml
  # The `$/` syntax is not available in GitHub Enterprise Server.
  call-workflow-in-same-repo-at-running-commit:
    uses: $/.github/workflows/workflow-2.yml
  call-workflow-in-another-repo:
    uses: octo-org/another-repo/.github/workflows/workflow.yml@v1
```

Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

## `jobs.<job_id>.with`

Quando um trabalho é usado para chamar um fluxo de trabalho reutilizável, você pode usar `with` para fornecer um mapa das entradas que são transmitidas para o fluxo de trabalho chamado.

Qualquer entrada que você passe deve corresponder às especificações de entrada definidas no fluxo de trabalho de chamada.

Ao contrário de [`jobs.<job_id>.steps[*].with`](#jobsjob_idstepswith), as entradas transmitidas com `jobs.<job_id>.with` não estão disponíveis como variáveis de ambiente no fluxo de trabalho chamado. Você pode referenciar as entradas usando o contexto `inputs`.

### Exemplo de `jobs.<job_id>.with`

```
jobs:
  call-workflow:
    uses: octo-org/example-repo/.github/workflows/called-workflow.yml@main
    with:
      username: mona
```

## `jobs.<job_id>.with.<input_id>`

Um par composto de um identificador de string para a entrada e o valor da entrada. O identificador precisa corresponder ao nome de uma entrada definida por [`on.workflow_call.inputs.<inputs_id>`](metadata-syntax.md#inputsinput_id) no fluxo de trabalho chamado. O tipo de dados do valor precisa corresponder ao tipo definido por [`on.workflow_call.inputs.<input_id>.type`](#onworkflow_callinputsinput_idtype) no fluxo de trabalho chamado.

Contextos de expressão permitidos: `github` e `needs`.

## `jobs.<job_id>.secrets`

Quando um trabalho é usado para chamar um fluxo de trabalho reutilizável, você pode usar `secrets` para fornecer um mapa de segredos que são transmitidos para o fluxo de trabalho chamado.

Qualquer segredo que você passar deve corresponder aos nomes definidos no fluxo de trabalho chamado.

### Exemplo de `jobs.<job_id>.secrets`

```
jobs:
  call-workflow:
    uses: octo-org/example-repo/.github/workflows/called-workflow.yml@main
    secrets:
      access-token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
```

## `jobs.<job_id>.secrets.inherit`

Use a palavra-chave `inherit` para passar todos os segredos do fluxo de trabalho que faz a chamada para o fluxo de trabalho chamado. Isso inclui todos os segredos aos quais o fluxo de trabalho que faz a chamada tem acesso, ou seja, segredos de organização, repositório e ambiente. A palavra-chave `inherit` pode ser usada para passar segredos entre repositórios dentro da mesma organização ou entre organizações dentro da mesma empresa.

### Exemplo de `jobs.<job_id>.secrets.inherit`

```
on:
  workflow_dispatch:

jobs:
  pass-secrets-to-workflow:
    uses: ./.github/workflows/called-workflow.yml
    secrets: inherit
```

```
on:
  workflow_call:

jobs:
  pass-secret-to-action:
    runs-on: ubuntu-latest
    steps:
      - name: Use a repo or org secret from the calling workflow.
        run: echo ${{ secrets.CALLING_WORKFLOW_SECRET }}
```

## `jobs.<job_id>.secrets.<secret_id>`

Um par composto por um identificador string para o segredo e o valor do segredo. O identificador precisa corresponder ao nome de um segredo definido por [`on.workflow_call.secrets.<secret_id>`](#onworkflow_callsecretssecret_id) no fluxo de trabalho chamado.

Contextos de expressão permitidos: `github`, `needs` e `secrets`.

## Folha de dados de padrão de filtro

Você pode usar caracteres especiais em filtros de nome de caminho, branch, tag e fluxo de trabalho.

* `*`: corresponde a zero ou mais caracteres, mas não corresponde ao caractere `/`. Por exemplo, `Octo*` corresponde a `Octocat`.
* `**`: corresponde a zero ou mais de qualquer caractere.
* `?`: corresponde a zero ou a um dos caracteres anteriores.
* `+`: corresponde a um ou mais dos caracteres anteriores.
* `[]`: corresponde a um caractere alfanumérico listado entre colchetes ou incluído nos intervalos. Os intervalos só podem incluir `a-z`, `A-Z` e `0-9`. Por exemplo, o intervalo `[0-9a-z]` corresponde a qualquer dígito ou letra minúscula. Por exemplo, `[CB]at` corresponde a `Cat` ou `Bat` e `[1-2]00` correspondem a `100` e a `200`.
* `!`: no início de um padrão, faz com que ele anule os padrões positivos anteriores. Não tem nenhum significado especial caso não seja o primeiro caractere.

Os caracteres `*`, `[` e `!` são caracteres especiais no YAML. Se você iniciar um padrão com `*`, `[` ou `!`, precisará colocar o padrão entre aspas. Além disso, se você usar uma [sequência de fluxo](https://yaml.org/spec/1.2.2/#flow-sequences) com um padrão contendo `[` e/ou `]`, o padrão deverá estar entre aspas.

```
# Valid
paths:
  - '**/README.md'

# Invalid - creates a parse error that
# prevents your workflow from running.
paths:
  - **/README.md

# Valid
branches: [ main, 'release/v[0-9].[0-9]' ]

# Invalid - creates a parse error
branches: [ main, release/v[0-9].[0-9] ]
```

Para obter mais informações sobre a sintaxe de filtro de ramificação, marca e caminho, consulte [`on.<push>.<branches|tags>`](#onpushbranchestagsbranches-ignoretags-ignore), [`on.<pull_request>.<branches|tags>`](#onpull_requestpull_request_targetbranchesbranches-ignore) e [`on.<push|pull_request>.paths`](#onpushpull_requestpull_request_targetpathspaths-ignore).

### Padrões para corresponder branches e tags

| Padrão                                      | Descrição                                                                                                                                                                                | Correspondências de exemplo                                                                   |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `feature/*`                                 | O curinga `*` corresponde a qualquer caractere, mas não à barra (`/`).                                                                                                                   | `feature/my-branch`<br/><br/>`feature/your-branch`                                            |
| `feature/**`                                | O curinga `**` corresponde a qualquer caractere, incluindo a barra (`/`) em nomes de branches e marcas.                                                                                  | `feature/beta-a/my-branch`<br/><br/>`feature/your-branch`<br/><br/>`feature/mona/the/octocat` |
| `main`<br/><br/>`releases/mona-the-octocat` | Corresponde ao nome exato de um branch ou tag.                                                                                                                                           | `main`<br/><br/>`releases/mona-the-octocat`                                                   |
| `'*'`                                       | Corresponde a todos os nomes de branches e marcas que não contêm uma barra (`/`). O caractere `*` é um caractere especial no YAML. Ao inciar um padrão com `*`, você precisa usar aspas. | `main`<br/><br/>`releases`                                                                    |
| `'**'`                                      | Corresponde a todos os nomes de branches e tags. Esse é o comportamento padrão quando um filtro `branches` ou `tags` não é usado.                                                        | `all/the/branches`<br/><br/>`every/tag`                                                       |
| `'*feature'`                                | O caractere `*` é um caractere especial no YAML. Ao inciar um padrão com `*`, você precisa usar aspas.                                                                                   | `mona-feature`<br/><br/>`feature`<br/><br/>`ver-10-feature`                                   |
| `v2*`                                       | Corresponde aos nomes de branches e marcas que começam com `v2`.                                                                                                                         | `v2`<br/><br/>`v2.0`<br/><br/>`v2.9`                                                          |
| `v[12].[0-9]+.[0-9]+`                       | Corresponde a todas as marcas e a todos os branches de controle de versão semântica com a versão principal 1 ou 2.                                                                       | `v1.10.1`<br/><br/>`v2.0.0`                                                                   |

### Padrões para corresponder a caminhos de arquivos

Padrões de caminhos devem corresponder ao caminho completo e iniciar a partir da raiz do repositório.

| Padrão                                                            | Descrição das correspondências                                                                                                                                                                                             | Correspondências de exemplo                                                             |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `'*'`                                                             | O curinga `*` corresponde a qualquer caractere, mas não à barra (`/`). O caractere `*` é um caractere especial no YAML. Ao inciar um padrão com `*`, você precisa usar aspas.                                              | `README.md`<br/><br/>`server.rb`                                                        |
| `'*.jsx?'`                                                        | O caractere `?` corresponde a zero ou um dos caracteres anteriores.                                                                                                                                                        | `page.js`<br/><br/>`page.jsx`                                                           |
| `'**'`                                                            | O curinga `**` corresponde a qualquer caractere, incluindo a barra (`/`). Esse é o comportamento padrão quando um filtro `path` não é usado.                                                                               | `all/the/files.md`                                                                      |
| `'*.js'`                                                          | O curinga `*` corresponde a qualquer caractere, mas não à barra (`/`). Corresponde a todos os arquivos `.js` na raiz do repositório.                                                                                       | `app.js`<br/><br/>`index.js`                                                            |
| `'**.js'`                                                         | Corresponde a todos os arquivos `.js` do repositório.                                                                                                                                                                      | `index.js`<br/><br/>`js/index.js`<br/><br/>`src/js/app.js`                              |
| `docs/*`                                                          | Somente os arquivos localizados na raiz do diretório `docs`, na raiz do repositório.                                                                                                                                       | `docs/README.md`<br/><br/>`docs/file.txt`                                               |
| `docs/**`                                                         | Qualquer arquivo no diretório `docs` e seus subdiretórios na raiz do repositório.                                                                                                                                          | `docs/README.md`<br/><br/>`docs/mona/octocat.txt`                                       |
| `docs/**/*.md`                                                    | Um arquivo com um sufixo `.md` em qualquer lugar do diretório `docs`.                                                                                                                                                      | `docs/README.md`<br/><br/>`docs/mona/hello-world.md`<br/><br/>`docs/a/markdown/file.md` |
| `'**/docs/**'`                                                    | Qualquer arquivo no diretório `docs`, em qualquer lugar do repositório.                                                                                                                                                    | `docs/hello.md`<br/><br/>`dir/docs/my-file.txt`<br/><br/>`space/docs/plan/space.doc`    |
| `'**/README.md'`                                                  | Um arquivo README.md em qualquer local do repositório.                                                                                                                                                                     | `README.md`<br/><br/>`js/README.md`                                                     |
| `'**/*src/**'`                                                    | Qualquer arquivo em uma pasta com o sufixo `src` em qualquer lugar do repositório.                                                                                                                                         | `a/src/app.js`<br/><br/>`my-src/code/js/app.js`                                         |
| `'**/*-post.md'`                                                  | Um arquivo com o sufixo `-post.md` em qualquer lugar no repositório.                                                                                                                                                       | `my-post.md`<br/><br/>`path/their-post.md`                                              |
| `'**/migrate-*.sql'`                                              | Um arquivo com o prefixo `migrate-` e o sufixo `.sql` em qualquer lugar no repositório.                                                                                                                                    | `migrate-10909.sql`<br/><br/>`db/migrate-v1.0.sql`<br/><br/>`db/sept/migrate-v1.sql`    |
| `'*.md'`<br/><br/>`'!README.md'`                                  | O uso de um sinal de exclamação (`!`) na frente de um padrão o anula. Quando um arquivo corresponde a um padrão e também corresponde a um padrão negativo definido posteriormente no arquivo, o arquivo não será incluído. | `hello.md`<br/><br/>                                                                    |
| *Não corresponde a*<br/><br/>`README.md`<br/><br/>`docs/hello.md` |                                                                                                                                                                                                                            |                                                                                         |
| `'*.md'`<br/><br/>`'!README.md'`<br/><br/>`README*`               | Os padrões são verificados sequencialmente. Um padrão que anula um padrão anterior irá incluir caminhos de arquivos novamente.                                                                                             | `hello.md`<br/><br/>`README.md`<br/><br/>`README.doc`                                   |
