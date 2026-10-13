---
title: Reutilizar fluxos de trabalho
description: Aprenda a evitar a duplicação ao criar um fluxo de trabalho reutilizando os fluxos de trabalho existentes.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/reuse-automations/reuse-workflows
captured: '2026-10-13'
section: How tos / Reuse automations
---

# Reutilizar fluxos de trabalho { #reuse-workflows }

_Aprenda a evitar a duplicação ao criar um fluxo de trabalho reutilizando os fluxos de trabalho existentes._

## Criar um fluxo de trabalho reutilizável { #creating-a-reusable-workflow }

Os fluxos de trabalho reutilizáveis são arquivos formatados com YAML, muito semelhantes a qualquer outro arquivo de fluxo de trabalho. Assim como acontece com outros arquivos de fluxo de trabalho, você localiza fluxos de trabalho reutilizáveis no diretório `.github/workflows` de um repositório. Não há suporte para subdiretórios do diretório `workflows`.

Para que um fluxo de trabalho seja reutilizável, os valores de `on` precisam incluir `workflow_call`:

```yaml
on:
  workflow_call:
```

## Usando entradas e segredos em um fluxo de trabalho reutilizável { #using-inputs-and-secrets-in-a-reusable-workflow }

Você pode definir entradas e segredos, que podem ser passados do fluxo de trabalho de de chamada e, em seguida, usados no fluxo de trabalho chamado. Há três etapas para usar uma entrada ou um segredo em um fluxo de trabalho reutilizável.

1. No fluxo de trabalho reutilizável, use as palavras-chave `inputs` e `secrets` para definir entradas ou segredos que serão transmitidos de um fluxo de trabalho do chamador.

            ```yaml
   on:
     workflow_call:
       inputs:
         config-path:
           required: true
           type: string
       secrets:
         personal_access_token:
           required: true
            ```

   Para obter detalhes da sintaxe para definir entradas e segredos, consulte [`on.workflow_call.inputs`](../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callinputs) e [`on.workflow_call.secrets`](../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callsecrets).

2. No fluxo de trabalho reutilizável, faça referência à entrada ou ao segredo que você definiu na chave `on` na etapa anterior.

!!! note

   > Se os segredos forem herdados usando `secrets: inherit` no fluxo de trabalho de chamada, você poderá referenciá-los mesmo que não estejam explicitamente definidos na chave `on`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsecretsinherit).

            ```yaml
   jobs:
     reusable_workflow_job:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/labeler@v6
         with:
           repo-token: ${{ secrets.personal_access_token }}
           configuration-path: ${{ inputs.config-path }}
            ```

   No exemplo acima, `personal_access_token` é um segredo definido no nível do repositório ou da organização.

   Para usar um segredo de ambiente em um fluxo de trabalho reutilizável, defina `environment` no trabalho no fluxo de trabalho reutilizável. O trabalho que chama o fluxo de trabalho reutilizável não pode usar a `environment` palavra-chave. Para saber mais, confira [Gerenciar ambientes para implantação](../deploy/configure-and-manage-deployments/manage-environments.md).

   O fluxo de trabalho do chamador ainda deve passar o secret. Use `secrets: inherit` ou passe o segredo pelo nome, por exemplo `MY_SECRET: ${{ secrets.MY_SECRET }}`. Você pode passar um segredo pelo nome, mesmo que só exista no ambiente.

   Se um segredo de ambiente tiver o mesmo nome de um repositório ou segredo da organização, o segredo do ambiente terá precedência. Isso se aplica quando o chamador usa `secrets: inherit` ou `${{ secrets.MY_SECRET }}`. O trabalho que define `environment` recebe o valor do segredo do ambiente.

!!! warning

   > Se o fluxo de trabalho do chamador não passar um segredo de ambiente, o segredo será resolvido para uma cadeia de caracteres vazia no fluxo de trabalho reutilizável. A execução do workflow não exibe nenhum erro. Em vez disso, para fazer a execução do fluxo de trabalho falhar, defina `required: true` no segredo em [`on.workflow_call.secrets`](../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callsecrets). Essa configuração verifica apenas se o workflow chamador fornece o segredo. Ele não verifica se o segredo tem um valor.

3. Passe a entrada ou o segredo do fluxo de trabalho da chamada.

   Para transmitir entradas nomeadas para um fluxo de trabalho chamado, use a palavra-chave `with` em um trabalho. Use a palavra-chave `secrets` para transmitir segredos nomeados. Para entradas, o tipo de dado do valor de entrada deve corresponder ao tipo especificado no fluxo de trabalho chamado (booleano, número ou string).

            ```yaml
   jobs:
     call-workflow-passing-data:
       uses: octo-org/example-repo/.github/workflows/reusable-workflow.yml@main
       with:
         config-path: .github/labeler.yml
       secrets:
         personal_access_token: ${{ secrets.token }}
            ```

   Fluxos de trabalho que chamam fluxos de trabalho reutilizáveis na mesma organização ou empresa podem usar a palavra-chave `inherit` para passar implicitamente os segredos.

            ```yaml
   jobs:
     call-workflow-passing-data:
       uses: octo-org/example-repo/.github/workflows/reusable-workflow.yml@main
       with:
         config-path: .github/labeler.yml
       secrets: inherit
            ```

### Exemplo de fluxo de trabalho reutilizável { #example-reusable-workflow }

Esse arquivo de fluxo de trabalho reutilizável chamado `workflow-B.yml` (vamos nos referir a ele mais adiante no [exemplo de fluxo de trabalho do chamador](#example-caller-workflow)) usa uma cadeia de caracteres de entrada e um segredo do fluxo de trabalho do chamador e os usa em uma ação.

```yaml copy
name: Reusable workflow example

on:
  workflow_call:
    inputs:
      config-path:
        required: true
        type: string
    secrets:
      token:
        required: true

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/labeler@v6
      with:
        repo-token: ${{ secrets.token }}
        configuration-path: ${{ inputs.config-path }}
```

## Chamando um fluxo de trabalho reutilizável { #calling-a-reusable-workflow }

Um fluxo de trabalho reutilizável é chamado por meio da palavra-chave `uses`. Ao contrário de quando você usa ações em um fluxo de trabalho, você chama os fluxos de trabalho reutilizáveis diretamente em um trabalho, e não de dentro de etapas de trabalho.

[`jobs.<job_id>.uses`](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_iduses)

Para fazer referência a arquivos reutilizáveis do fluxo de trabalho, use uma destas sintaxes:

* `$/.github/workflows/{filename}` para um fluxo de trabalho reutilizável no mesmo repositório. Essa é a sintaxe recomendada para referenciar um fluxo de trabalho reutilizável no mesmo repositório. Essa sintaxe não está disponível em GitHub Enterprise Server.
* `{owner}/{repo}/.github/workflows/{filename}@{ref}` para fluxos de trabalho reutilizáveis em repositórios públicos e privados.
* `./.github/workflows/{filename}` para fluxos de trabalho reutilizáveis no mesmo repositório.

Quando você faz referência a um fluxo de trabalho reutilizável com `{owner}/{repo}` e `@{ref}`, pode `{ref}` ser um SHA, uma marca de versão ou um nome de branch. Se uma tag de release e uma ramificação tiverem o mesmo nome, a tag de release terá precedência sobre o nome da ramificação. Usar o commit SHA é a opção mais segura para fins de estabilidade e segurança. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#reusing-third-party-workflows).

Quando você faz referência a um fluxo de trabalho reutilizável no mesmo repositório usando `$/` ou `./` (sem `{owner}/{repo}` e `@{ref}`), o fluxo de trabalho chamado é da mesma confirmação que o fluxo de trabalho do chamador. Uma `$/` referência não deve incluir um `@{ref}` sufixo e `$/` não está disponível em GitHub Enterprise Server. Prefixos de referência como `refs/heads` e `refs/tags` não são permitidos. Você não pode usar contextos ou expressões nesta palavra-chave.

Você pode chamar vários fluxos de trabalho, fazendo referência a cada um em um trabalho separado.

```yaml
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

### Exemplo de fluxo de trabalho do chamador { #example-caller-workflow }

Este arquivo de fluxo de trabalho chama dois arquivos de fluxo de trabalho. O segundo deles, `workflow-B.yml` (mostrado no [exemplo de fluxo de trabalho reutilizável](#example-reusable-workflow)), recebe uma entrada (`config-path`) e um segredo (`token`).

```yaml copy
name: Call a reusable workflow

on:
  pull_request:
    branches:
      - main

jobs:
  call-workflow:
    uses: octo-org/example-repo/.github/workflows/workflow-A.yml@v1

  call-workflow-passing-data:
    permissions:
      contents: read
      pull-requests: write
    uses: octo-org/example-repo/.github/workflows/workflow-B.yml@main
    with:
      config-path: .github/labeler.yml
    secrets:
      token: ${{ secrets.GITHUB_TOKEN }}
```

## Passando entradas e segredos para um fluxo de trabalho reutilizável { #passing-inputs-and-secrets-to-a-reusable-workflow }

Para transmitir entradas nomeadas para um fluxo de trabalho chamado, use a palavra-chave `with` em um trabalho. Use a palavra-chave `secrets` para transmitir segredos nomeados. Para entradas, o tipo de dado do valor de entrada deve corresponder ao tipo especificado no fluxo de trabalho chamado (booleano, número ou string).

```yaml
jobs:
  call-workflow-passing-data:
    uses: octo-org/example-repo/.github/workflows/reusable-workflow.yml@main
    with:
      config-path: .github/labeler.yml
    secrets:
      personal_access_token: ${{ secrets.token }}
```

Fluxos de trabalho que chamam fluxos de trabalho reutilizáveis na mesma organização ou empresa podem usar a palavra-chave `inherit` para passar implicitamente os segredos.

```yaml
jobs:
  call-workflow-passing-data:
    uses: octo-org/example-repo/.github/workflows/reusable-workflow.yml@main
    with:
      config-path: .github/labeler.yml
    secrets: inherit
```

## Como usar uma estratégia de matriz com um fluxo de trabalho reutilizável { #using-a-matrix-strategy-with-a-reusable-workflow }

Trabalhos que usam a estratégia de matriz podem chamar um fluxo de trabalho reutilizável.

Uma estratégia de matriz permite que você use variáveis em uma única definição de trabalho para criar automaticamente várias execuções de trabalho baseadas nas combinações das variáveis. Por exemplo, você pode usar uma estratégia de matriz a fim de passar entradas diferentes para um fluxo de trabalho reutilizável. Para obter mais informações sobre matrizes, confira [Executando variações de tarefas em um workflow](../write-workflows/choose-what-workflows-do/run-job-variations.md).

Este trabalho de exemplo abaixo chama um fluxo de trabalho reutilizável e faz referência ao contexto de matriz definindo a variável `target` com os valores `[dev, stage, prod]`. Ele executará três trabalhos, um para cada valor na variável.

```yaml copy
jobs:
  ReusableMatrixJobForDeployment:
    strategy:
      matrix:
        target: [dev, stage, prod]
    uses: octocat/octo-repo/.github/workflows/deployment.yml@main
    with:
      target: ${{ matrix.target }}
```

## Como aninhar fluxos de trabalho reutilizáveis { #nesting-reusable-workflows }

Você pode conectar no máximo dez níveis de fluxos de trabalho, ou seja, o fluxo de trabalho de chamadas de nível superior e até nove níveis de fluxos de trabalho reutilizáveis. Por exemplo: *caller-workflow\.yml\_\_→ called-workflow-1.yml\_\_→ called-workflow-2.yml* → *called-workflow-3.yml* →... → *called-workflow-9.yml*.

Loops na árvore de fluxo de trabalho não são permitidos.

> [!NOTE] Fluxos de trabalho reutilizáveis aninhados exigem que todos os fluxos de trabalho na cadeia sejam acessíveis ao chamador, e as permissões só podem ser mantidas ou reduzidas, e não elevadas, em toda a cadeia. Para saber mais, confira [Reutilizando configurações de fluxo de trabalho](../../reference/workflows-and-actions/reusing-workflow-configurations.md).

De dentro de um fluxo de trabalho reutilizável, você pode chamar outro fluxo de trabalho reutilizável.

```yaml copy
name: Reusable workflow

on:
  workflow_call:

jobs:
  call-another-reusable:
    uses: octo-org/example-repo/.github/workflows/another-reusable.yml@v1
```

## Como passar informações confidenciais para fluxos de trabalho aninhados { #passing-secrets-to-nested-workflows }

Você pode usar `jobs.<job_id>.secrets` em um fluxo de trabalho de chamada para passar segredos nomeados para um fluxo de trabalho chamado diretamente. Como alternativa, você pode usar `jobs.<job_id>.secrets.inherit` para passar todos os segredos do fluxo de trabalho que efetuou a chamada para um fluxo de trabalho chamado diretamente. Para saber mais, confira a seção [Reutilizar fluxos de trabalho](reuse-workflows.md#passing-inputs-and-secrets-to-a-reusable-workflow) acima e o artigo de referência [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsecretsinherit). Os segredos são passados apenas para o fluxo de trabalho chamado diretamente, portanto, na cadeia de fluxo de trabalho A > B > C, o fluxo de trabalho C só receberá segredos de A se tiverem sido passados de A para B e, em seguida, de B para C.

No exemplo a seguir, o fluxo de trabalho A passa todos os segredos dele para o fluxo de trabalho B, usando a palavra-chave `inherit`, mas o fluxo de trabalho B passa apenas um segredo para o fluxo de trabalho C. Qualquer um dos outros segredos passados para o fluxo de trabalho B não está disponível para o fluxo de trabalho C.

```yaml
jobs:
  workflowA-calls-workflowB:
    uses: octo-org/example-repo/.github/workflows/B.yml@main
    secrets: inherit # pass all secrets
```

```yaml
jobs:
  workflowB-calls-workflowC:
    uses: different-org/example-repo/.github/workflows/C.yml@main
    secrets:
      repo-token: ${{ secrets.personal_access_token }} # pass just this secret
```

## Usando saídas de um fluxo de trabalho reutilizável { #using-outputs-from-a-reusable-workflow }

Um fluxo de trabalho reutilizável pode gerar dados que você deseja usar no fluxo de trabalho da chamada. Para usar essas saídas, você deve especificá-las como saídas do fluxo de trabalho reutilizável.

Se um fluxo de trabalho reutilizável que define uma saída for executado com uma estratégia de matriz, a saída será aquela definida pelo último fluxo de trabalho reutilizável que foi concluído com sucesso na matriz e que realmente definiu um valor.
Isso significa que se o último fluxo de trabalho reutilizável bem-sucedido definir uma cadeia de caracteres vazia para sua saída e a segunda última conclusão bem-sucedida do fluxo de trabalho reutilizável definir um valor real para sua saída, a saída conterá o valor do segundo último fluxo de trabalho reutilizável.

O seguinte fluxo de trabalho reutilizável tem um único trabalho que contém duas etapas. Em cada uma dessas etapas, definimos uma única palavra como a saída: "olá" e "mundo". Na seção `outputs` do trabalho, mapeamos essas saídas de etapa para saídas de trabalho chamadas: `output1` e `output2`. Na seção `on.workflow_call.outputs`, definimos duas saídas para o fluxo de trabalho em si, uma chamada `firstword`, que mapeamos para `output1`, e outra chamada `secondword`, que mapeamos para `output2`.

O `value` deve ser definido como o valor de uma saída de nível de trabalho no fluxo de trabalho chamado. As saídas em nível de etapa devem primeiro ser mapeadas às saídas em nível de trabalho, conforme mostrado abaixo.

Para saber mais, confira [Passando informações entre tarefas](../write-workflows/choose-what-workflows-do/pass-job-outputs.md) e [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_calloutputs).

```yaml copy
name: Reusable workflow

on:
  workflow_call:
    # Map the workflow outputs to job outputs
    outputs:
      firstword:
        description: "The first output string"
        value: ${{ jobs.example_job.outputs.output1 }}
      secondword:
        description: "The second output string"
        value: ${{ jobs.example_job.outputs.output2 }}

jobs:
  example_job:
    name: Generate output
    runs-on: ubuntu-latest
    # Map the job outputs to step outputs
    outputs:
      output1: ${{ steps.step1.outputs.firstword }}
      output2: ${{ steps.step2.outputs.secondword }}
    steps:
      - id: step1
        run: echo "firstword=hello" >> $GITHUB_OUTPUT
      - id: step2
        run: echo "secondword=world" >> $GITHUB_OUTPUT
```

Agora podemos usar as saídas no fluxo de trabalho da chamada, da mesma forma que você usaria as saídas de um trabalho dentro do mesmo fluxo de trabalho. Referenciamos as saídas usando os nomes definidos no nível do fluxo de trabalho no fluxo de trabalho reutilizável: `firstword` e `secondword`. Nesse fluxo de trabalho, `job1` chama o fluxo de trabalho reutilizável e `job2` imprime as saídas do fluxo de trabalho reutilizável ("olá, mundo") para a saída padrão no log do fluxo de trabalho.

```yaml copy
name: Call a reusable workflow and use its outputs

on:
  workflow_dispatch:

jobs:
  job1:
    uses: octo-org/example-repo/.github/workflows/called-workflow.yml@v1

  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - run: echo ${{ needs.job1.outputs.firstword }} ${{ needs.job1.outputs.secondword }}
```

Para saber mais sobre como usar saídas de trabalho, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs). Se você desejar compartilhar algo diferente de uma variável (por exemplo, um artefato de criação) entre fluxos de trabalho, consulte [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../tutorials/store-and-share-data.md).

## Controlando o acesso ao cache em fluxos de trabalho reutilizáveis { #controlling-cache-access-in-reusable-workflows }

Você pode usar a chave `cache-mode` para conceder a um fluxo de trabalho reutilizável o nível mínimo de acesso ao cache GitHub Actions de que ele precisa. O valor pode ser `read`, `write`, `write-only`ou `none`. Se você omitir `cache-mode`, um `read` ou `write` padrão será usado com base no tipo de gatilho. Para obter a sintaxe completa e o significado de cada valor, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#cache-mode). Para valores padrão dependentes do acionador, consulte [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md#defaults).

Quando um fluxo de trabalho chamador chama um fluxo de trabalho reutilizável, `cache-mode` é propagado para o fluxo de trabalho chamado. Uma especificação explícita de `cache-mode` no job chamador, ou herdada do workflow chamador, limita o acesso ao cache que o workflow chamado pode solicitar.

Se o job chamador não definir nem herdar um `cache-mode` explícito, o workflow chamado poderá solicitar explicitamente `write`, mesmo quando o gatilho de baixa confiança do chamador utilizar o padrão `read`. Para restringir um fluxo de trabalho chamado ao acesso somente leitura, defina `cache-mode: read` no job que o chama.

Se um fluxo de trabalho chamado declarar um `cache-mode` que solicite acesso além desse limite explícito, a execução não será iniciada e GitHub informará um erro de validação. Por exemplo, um chamador que permite, no máximo, `read` não pode chamar um fluxo de trabalho que declare `write`. Como `read` concede acesso de restauração e `write-only` concede acesso de salvamento, os dois são recursos não sobrepostos, portanto, uma incompatibilidade entre eles também é uma solicitação excessiva. Por exemplo, um `write-only` chamador não pode chamar um fluxo de trabalho que declare `read`.

Para obter mais informações sobre o acesso ao cache e os quatro modos, consulte [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md#controlling-cache-access-with-cache-mode).

## Monitorando quais fluxos de trabalho estão sendo utilizados { #monitoring-which-workflows-are-being-used }

As organizações que usam GitHub Enterprise Cloud podem interagir com o log de auditoria por meio da GitHub API REST para monitorar quais fluxos de trabalho estão sendo usados. Para obter mais informações, consulte [a GitHub Enterprise Cloud documentação](https://docs.github.com/pt/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/reviewing-the-audit-log-for-your-organization#using-the-audit-log-api).

## Próximas etapas { #next-steps }

Para encontrar informações sobre os meandros da reutilização de fluxos de trabalho, consulte [Reutilizando configurações de fluxo de trabalho](../../reference/workflows-and-actions/reusing-workflow-configurations.md).
