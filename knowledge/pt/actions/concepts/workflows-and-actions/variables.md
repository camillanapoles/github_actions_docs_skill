---
title: Variáveis
description: Saiba mais sobre variáveis em GitHub Actions fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/variables
captured: '2026-10-26'
section: Concepts / Workflows and actions
---

# Variáveis

_Saiba mais sobre variáveis em GitHub Actions fluxos de trabalho._

## Sobre

As variáveis fornecem uma forma de armazenar e reutilizar informações de configuração não confidenciais. Você pode armazenar quaisquer dados de configuração, como sinalizadores de compilador, nomes de usuário ou nomes de servidor como variáveis. As variáveis são interpoladas no computador executor que executa seu fluxo de trabalho. Os comandos que são executados em ações ou etapas do fluxo de trabalho podem criar, ler e modificar variáveis.

Você pode definir suas próprias variáveis personalizadas ou usar as variáveis de ambiente padrão definidas GitHub automaticamente.

Você pode definir uma variável personalizada de duas maneiras.

* Para definir uma variável de ambiente para uso em um só fluxo de trabalho, você pode usar a chave `env` do arquivo do fluxo de trabalho. Para obter mais informações, confira [Como definir variáveis de ambiente para um fluxo de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-environment-variables-for-a-single-workflow).
* Ao definir uma variável de configuração para vários fluxos de trabalho, é possível fazê-lo no nível da organização, do repositório ou do ambiente. Ao criar uma variável em uma organização, você pode usar uma política para limitar o acesso por repositório. Por exemplo, você pode conceder acesso a todos os repositórios ou limitar o acesso a apenas repositórios privados ou a uma lista específica de repositórios. Para obter mais informações, confira [Como definir variáveis de configuração para vários fluxos de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md#defining-configuration-variables-for-multiple-workflows).

!!! warning
    Por padrão, as variáveis são renderizadas sem máscaras nas saídas do build. Se você precisar de mais segurança para informações confidenciais, como senhas, use segredos. Para saber mais, confira [Segredos](../security/secrets.md).

Para obter a documentação de referência, confira [Referência de variáveis](../../reference/workflows-and-actions/variables.md).
