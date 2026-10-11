---
title: Expressões
description: Você pode avaliar expressões em fluxos de trabalho e ações.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/expressions
captured: '2026-10-11'
section: GitHub Actions
---

# Expressões

_Você pode avaliar expressões em fluxos de trabalho e ações._

## Sobre as expressões

Você pode usar expressões para definir variáveis de ambiente programaticamente em arquivos de fluxo de trabalho e contextos de acesso. Uma expressão pode ser qualquer combinação de valores literais, referências a um contexto ou funções. É possível combinar literais, referências de contexto e funções usando operadores. Para obter mais informações sobre contextos, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md).

As expressões são normalmente usadas com a palavra-chave `if` condicional em um arquivo de fluxo de trabalho para determinar se uma etapa deve ser executada. Quando um condicional `if` for `true`, a etapa será executada.

É necessário usar uma sintaxe específica para avisar o GitHub para avaliar a expressão e não tratá-la como uma string.

`${{ <expression> }}`

> \[!NOTE]
> A exceção a essa regra é quando você estiver usando expressões em uma cláusula `if`, na qual, opcionalmente, geralmente é possível omitir `${{` e `}}`. Para obter mais informações sobre condicionais `if`, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif).

> \[!WARNING]
> Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

### Exemplo de configuração de variável de ambiente

```yaml
env:
  MY_ENV_VAR: ${{ <expression> }}
```

## Leitura adicional

Para obter informações de referência técnica sobre expressões que você pode usar em fluxos de trabalho e ações, confira [Avaliar expressões em fluxos de trabalho e ações](../../reference/workflows-and-actions/expressions.md).
