---
title: Definindo códigos de saída para ações
description: Você pode usar códigos de saída para definir o status de uma ação. GitHub exibe status para indicar ações bem-sucedidas ou com falha.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/set-exit-codes
captured: '2026-10-19'
section: How tos / Create and publish actions
---

# Definindo códigos de saída para ações

_Você pode usar códigos de saída para definir o status de uma ação. GitHub exibe status para indicar ações bem-sucedidas ou com falha._

## Sobre os códigos de saída

GitHub usa o código de saída para definir o status de execução de verificação da ação, que pode ser `success` ou `failure`.

| Status da saída | Verificar status de execução | Descrição |
| --- | --- | --- |
| `0` | `success` | A ação foi concluída com êxito e outras tarefas que dependem dela podem começar. |
| Valor diferente de zero (qualquer número inteiro que não seja 0) | `failure` | Qualquer outro código de saída indica falha na ação. Quando uma ação falha, todas as ações simultâneas são canceladas e as ações futuras são ignoradas. O conjunto de verificação e a execução de verificação obtém um status `failure`. |

## Definir um código de saída de falha em uma ação JavaScript

Se você estiver criando uma ação do JavaScript, poderá usar o pacote do kit de ferramentas de ações [`@actions/core`](https://github.com/actions/toolkit/tree/main/packages/core) para registrar uma mensagem e definir um código de saída de falha. Por exemplo:

```javascript
try {
  // something
} catch (error) {
  core.setFailed(error.message);
}
```

Para saber mais, confira [Criando uma ação de JavaScript](../../tutorials/create-actions/create-a-javascript-action.md).

## Definir um código de saída de falha em uma ação de contêiner do Docker

Se você estiver criando uma ação de contêiner do Docker, poderá definir um código de saída de falha em seu script `entrypoint.sh`. Por exemplo:

```shell
if <condition> ; then
  echo "Game over!"
  exit 1
fi
```

Para saber mais, confira [Criando uma ação de contêiner do Docker](../../tutorials/use-containerized-services/create-a-docker-container-action.md).
