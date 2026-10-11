---
title: Controlar a simultaneidade de fluxos de trabalho e tarefas
description: Gerencie os fluxos de trabalho e os trabalhos que podem ser executados juntos.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency
captured: '2026-10-11'
section: GitHub Actions
---

# Controlar a simultaneidade de fluxos de trabalho e tarefas

_Gerencie os fluxos de trabalho e os trabalhos que podem ser executados juntos._

## Usar a simultaneidade em diferentes cenários

Você pode usar `jobs.<job_id>.concurrency` para garantir que apenas um trabalho ou fluxo de trabalho que usa o mesmo grupo de simultaneidade seja executado por vez. Um grupo de concorrência pode ser qualquer string ou expressão. Contextos de expressão permitidos: [`github`](../../../reference/workflows-and-actions/contexts.md#github-context), [`inputs`](../../../reference/workflows-and-actions/contexts.md#inputs-context), [`vars`](../../../reference/workflows-and-actions/contexts.md#vars-context), [`needs`](../../../reference/workflows-and-actions/contexts.md#needs-context), [`strategy`](../../../reference/workflows-and-actions/contexts.md#strategy-context) e [`matrix`](../../../reference/workflows-and-actions/contexts.md#matrix-context). Para obter mais informações sobre expressões, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md).

Especifique também `concurrency` no nível do fluxo de trabalho. Para obter mais informações, confira [`concurrency`](../../../reference/workflows-and-actions/workflow-syntax.md#concurrency).

Isso significa que pode haver no máximo um trabalho ou fluxo de trabalho em execução em um grupo de concorrência a qualquer momento. Quando um trabalho ou um fluxo de trabalho simultâneo é colocado na fila, se outro trabalho ou fluxo de trabalho que usa o mesmo grupo de simultaneidade no repositório estiver em andamento, o trabalho ou o fluxo de trabalho na fila ficará `pending`. Por padrão, qualquer trabalho ou fluxo de trabalho existente `pending` no mesmo grupo de simultaneidade será cancelado e o novo trabalho ou fluxo de trabalho em fila tomará seu lugar.

Para também cancelar qualquer trabalho ou fluxo de trabalho em execução no mesmo grupo de concorrência, especifique `cancel-in-progress: true`. Para cancelar condicionalmente trabalhos ou fluxos de trabalho em execução no mesmo grupo de simultaneidade, é possível especificar `cancel-in-progress` como uma expressão com qualquer um dos contextos de expressão permitidos.

Para permitir que mais de uma tarefa ou execução de fluxo de trabalho aguardem no mesmo grupo de simultaneidade, use a propriedade opcional `queue`. A `queue` propriedade aceita os seguintes valores:

* `single` (padrão): no máximo uma execução de tarefa ou de fluxo de trabalho pode ser `pending` no grupo de simultaneidade. Quando uma nova execução de trabalho ou fluxo de trabalho é enfileirada, qualquer execução existente de trabalho ou fluxo de trabalho `pending` no mesmo grupo é cancelada e substituída.
* `max`: até 100 trabalhos ou execuções de fluxo de trabalho podem ser incluídos no grupo de simultaneidade. Quando a fila estiver cheia, quaisquer trabalhos adicionais ou execuções de fluxo de trabalho serão cancelados.

A combinação de `queue: max` e `cancel-in-progress: true` não é permitida e resultará em um erro de validação de fluxo de trabalho.

> \[!NOTE]
>
> * O nome do grupo de simultaneidade não diferencia maiúsculas de minúsculas. Por exemplo, `prod` e `Prod` serão tratados como o mesmo grupo de simultaneidade.
> * Trabalhos ou execuções de fluxo de trabalho no mesmo grupo de simultaneidade são processados na ordem de primeiro a entrar em primeiro lugar (FIFO), de acordo com o momento em que cada um começou a esperar no grupo de simultaneidade, não o tempo em que cada fluxo de trabalho foi expedido. Como o horário de início efetivo de um trabalho ou execução pode variar, a ordenação não é garantida.

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

## Monitorando os seus trabalhos atuais na sua organização ou empresa

Para identificar quaisquer restrições com simultaneidade ou enfileiramento, você pode verificar quantos trabalhos estão sendo processados atualmente nos GitHubexecutores hospedados em sua organização ou empresa. Para saber mais, confira [Visualizando suas tarefas atuais](../../manage-runners/github-hosted-runners/view-current-jobs.md).
