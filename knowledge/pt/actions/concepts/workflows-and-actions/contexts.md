---
title: Contextos
description: Saiba mais sobre contextos em GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/contexts
captured: '2026-10-11'
section: GitHub Actions
---

# Contextos

_Saiba mais sobre contextos em GitHub Actions._

## Sobre os contextos

Os contextos são uma forma de acessar informações sobre execuções de fluxo de trabalho, variáveis, ambientes dos executores, trabalhos e etapas. Cada contexto é um objeto que contém propriedades, que podem ser cadeias de caracteres ou outros objetos.

Os contextos, objetos e propriedades variarão significativamente em diferentes condições de execução do fluxo de trabalho. Por exemplo, o contexto `matrix` só é preenchido para trabalhos em uma [matriz](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrix).

Você pode acessar contextos usando a sintaxe da expressão. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../reference/workflows-and-actions/expressions.md).

`${{ <context> }}`

> \[!WARNING]
> Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

## Determinar quando usar contextos

GitHub Actions inclui uma coleção de variáveis chamadas *contextos* e uma coleção semelhante de variáveis chamadas *variáveis padrão*. Estas variáveis são destinadas a serem usadas em diferentes pontos do fluxo de trabalho:

* **Variáveis de ambiente padrão:** essas variáveis de ambiente existem apenas no executor que está executando seu trabalho. Para saber mais, confira [Referência de variáveis](../../reference/workflows-and-actions/variables.md#default-environment-variables).
* **Contextos:** você pode usar a maioria dos contextos em qualquer ponto do fluxo de trabalho, inclusive quando as *variáveis padrão* não estão disponíveis. Por exemplo, você pode usar contextos com expressões para executar o processamento inicial antes que o trabalho seja encaminhado para um executor para execução. Isso permite que você use um contexto com a palavra-chave `if` condicional para determinar se uma etapa deve ser executada. Depois que o trabalho estiver em execução, você também poderá recuperar variáveis de contexto do executor que está executando o trabalho, como `runner.os`. Para obter detalhes sobre quando usar vários contextos em um fluxo de trabalho, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md#context-availability).

O seguinte exemplo demonstra como esses diferentes tipos de variáveis podem ser usados juntos em um trabalho:

```yaml copy
name: CI
on: push
jobs:
  prod-check:
    if: ${{ github.ref == 'refs/heads/main' }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to production server on branch $GITHUB_REF"
```

Neste exemplo, a instrução `if` verifica o contexto [`github.ref`](../../reference/workflows-and-actions/contexts.md#github-context) para determinar o nome do branch atual. Se o nome for `refs/heads/main`, as etapas seguintes serão executadas. A `if` verificação é processada por GitHub Actions, e o trabalho só é enviado para o executor se o resultado for `true`. Depois que o trabalho é enviado para o executor, a etapa é executada e refere-se à variável [`$GITHUB_REF`](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md) do executor.
