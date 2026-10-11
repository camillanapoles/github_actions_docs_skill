---
title: Usando tarefas em um fluxo de trabalho
description: Use fluxos de trabalho para executar vários trabalhos.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs
captured: '2026-10-11'
section: GitHub Actions
---

# Usando tarefas em um fluxo de trabalho

_Use fluxos de trabalho para executar vários trabalhos._

## Pré-requisitos

Para implementar trabalhos em seus fluxos de trabalho, você precisa entender quais são os trabalhos. Confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md#jobs).

## Configurando um ID para um trabalho

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

## Definir um nome para um trabalho

Use `jobs.<job_id>.name` para definir um nome para o trabalho, que é exibido na interface do usuário do GitHub.

## Definindo trabalhos dos pré-requisitos

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

Neste exemplo, `job3` usa a expressão condicional `always()` para que ela sempre seja executada após a conclusão de `job1` e de `job2`, independentemente de elas terem sido bem-sucedidas. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md#status-check-functions).

## Como usar uma matriz para executar trabalhos com variáveis diferentes

Para executar automaticamente um trabalho com diferentes combinações de variáveis, como sistemas operacionais ou versões de linguagem, defina uma estratégia de `matrix` em seu fluxo de trabalho.

Para saber mais, confira [Executando variações de tarefas em um workflow](run-job-variations.md).
