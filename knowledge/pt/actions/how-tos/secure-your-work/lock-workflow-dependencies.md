---
title: Bloqueio de dependências de ação nos fluxos de trabalho de um repositório
description: Gere um arquivo de bloqueio que fixe cada ação que seus fluxos de trabalho usam em um commit verificado e mantenha-o atual à medida que suas dependências são alteradas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/lock-workflow-dependencies
captured: '2026-11-09'
section: How tos / Secure your work
---

# Bloqueio de dependências de ação nos fluxos de trabalho de um repositório

_Gere um arquivo de bloqueio que fixe cada ação que seus fluxos de trabalho usam em um commit verificado e mantenha-o atual à medida que suas dependências são alteradas._

Bloquear as dependências dos fluxos de trabalho garante que as ações referenciadas contenham o mesmo código que foi originalmente revisado. Para obter mais informações, consulte [Arquivos de bloqueio de dependências do fluxo de trabalho](../../concepts/security/workflow-dependency-lockfiles.md).

## 1. Verifique suas referências da ação

A criação de um arquivo de bloqueio fixa suas dependências em commits com base na referência de branch ou marca atual. Verifique se essas são as versões que você deseja fixar no lugar.

Verifique se cada referência `uses` em seus fluxos de trabalho aponta para uma versão atual e suportada da ação. Para obter as práticas recomendadas, consulte [Referência de uso seguro](../../reference/security/secure-use.md#using-third-party-actions).

Se qualquer um de seus fluxos de trabalho chamar um fluxo de trabalho reutilizável em outro repositório, verifique essas referências também. As dependências de um fluxo de trabalho reutilizável são cobertas pelo arquivo de bloqueio do repositório em que ele é definido, não pelo seu arquivo de bloqueio. Esse repositório de origem precisa de seu próprio lockfile para cobertura completa. Se sua organização mantiver fluxos de trabalho compartilhados, integre esses repositórios primeiro. Consulte [Reutilizando configurações de fluxo de trabalho](../../concepts/workflows-and-actions/reusing-workflow-configurations.md).

Recomendamos deixar o Dependabot gerenciar suas dependências GitHub Actions. Se ele ainda não estiver habilitado, habilite-o antes de criar o arquivo de bloqueio. Consulte [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

## 2. Instalar a `actions-lock` extensão

1. Instale o [GitHub CLI](https://cli.github.com/).

2. Instale a extensão.

            ```bash copy
   gh extension install github/gh-actions-lock
   ```

> [!TIP] Para atualizar a extensão mais tarde, execute `gh extension upgrade gh-actions-lock`.

## 3. Gerar o arquivo de bloqueio

Na raiz do repositório, execute a extensão sem argumentos. Ele examinará todos os fluxos de trabalho em `.github/workflows/`, fixará cada ação resolvível em uma SHA do commit e gravará o arquivo de bloqueio.

```bash copy
gh actions-lock
```

Para adicionar um único fluxo de trabalho em vez de todo o diretório, passe seu caminho.

```bash copy
gh actions-lock .github/workflows/ci.yml
```

A extensão nunca segue ou trava uma ação de caminho local (`uses: ./…`). Um `./` caminho executa o que for verificado no workspace do executor, por isso a extensão não pode fixá-lo ou ver o que ele usa. Especificar um `$/` caminho executa a própria ação do repositório no commit do fluxo de trabalho, portanto, ele é fixado e as ações que ele usa podem ser bloqueadas. Para obter uma comparação dos dois, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#example-using-an-action-in-the-same-repository-as-the-workflow-at-the-running-commit-recommended).

Se uma ação local em seu checkout usar outras ações, a extensão relatará um erro de `local-action` e não gravará nada, pois essas ações falhariam em tempo de execução sem entradas no lockfile. Para bloquear a ação local como uma referência do mesmo repositório, execute:

```bash copy
gh actions-lock --migrate-local-actions
```

Para manter a `./` referência e relatá-la como um aviso, passe `--ignore-local-actions`. Consulte [Manter uma ação de caminho local](#keeping-a-local-path-action).

Para o conjunto completo de opções, execute `gh actions-lock --help`. Para obter ajuda com um erro ou aviso específico, consulte o [guia de solução de problemas do gh-actions-lock](https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md?utm_source=locking-action-dependencies-repo-workflow-doc-linking-gh\&utm_medium=docs\&utm_campaign=universe-2026).

### Manter uma ação de caminho local

Se você passar `--ignore-local-actions`, o que acontece em tempo de execução depende das ações que a ação local usa:

* **Ele não usa nenhuma outra ação**, por exemplo, somente `run:` etapas: o fluxo de trabalho é executado normalmente.
* **Ele usa ações que têm entradas de arquivo de bloqueio para o mesmo fluxo de trabalho**: o fluxo de trabalho é executado normalmente.
* **Ele usa uma ação que não tem nenhuma entrada de arquivo de bloqueio para esse fluxo de trabalho**: o trabalho falha quando chega à etapa da ação local, com um erro como `lockfile missing pin for octo-org/setup-tool@v2.0.0`. Etapas anteriores já foram executadas.

Recomendamos `--migrate-local-actions` para que a ação seja executada como uma referência fixada `$/`. Se você precisar manter a referência `./`, forneça as entradas do lockfile do fluxo de trabalho para as ações que a ação local usa. Adicione uma ação composta que use as mesmas ações, com as mesmas referências, e chame-a do fluxo de trabalho em uma etapa que nunca é executada. Em seguida, execute `gh actions-lock --ignore-local-actions`.

```yaml
```
# .github/actions/lock-local-deps/action.yml
name: Lock local action dependencies
description: Never runs. Lists the actions that ./.github/actions/build uses.
runs:
  using: composite
  steps:
    - uses: octo-org/setup-tool@v2.0.0
```

```
```
# In the workflow
steps:
  - uses: actions/checkout@v6
  - if: false
    uses: $/.github/actions/lock-local-deps
  - uses: ./.github/actions/build
```

As entradas devem ser registradas para o mesmo fluxo de trabalho. Uma entrada registrada apenas para um fluxo de trabalho diferente não conta. Quando as dependências da ação local forem alteradas, atualize a ação composta e execute `gh actions-lock --ignore-local-actions` novamente.

```
## 4. Examine as alterações e confirme

A extensão altera mais do que o arquivo de bloqueio, portanto, examine a diferença completa antes de fazer commit. Ele também reescreve as referências `uses` do seu fluxo de trabalho para a versão específica que ele resolveu, de modo que uma referência como `octo-org/deploy-action@v3` pode se tornar `octo-org/deploy-action@v3.1.0`. Isso torna a referência mais específica sem alterar o commit ao qual ela se refere.

!!! important
    Se o repositório, a organização ou a empresa permitirem apenas ações especificadas, verifique a lista de permissões antes de fazer commit. Depois que um fluxo de trabalho é incorporado, a lista de permissões é verificada em relação a SHAs de commit bloqueadas em vez de tags, porque uma tag pode ser movida para um código diferente, mas uma SHA bloqueada não pode. As entradas fixadas em uma tag, como `actions/checkout@v6`, não correspondem mais depois que um fluxo de trabalho é incorporado ao sistema. Em vez disso, use um curinga ou o SHA completo do commit. Consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-select-actions-and-reusable-workflows-to-run).

Se você forneceu `--migrate-local-actions`, a extensão também reescreve referências a ações em seu próprio repositório, de `uses: ./…` para `uses: $/…`, em seus fluxos de trabalho e nos arquivos `action.yml` do seu repositório. Ele só faz isso quando você passa a opção, porque as duas formas se comportam de forma diferente. Um `./` caminho é resolvido em relação ao que está no workspace do executor, enquanto uma `$/…` referência sempre é executada no próprio commit do fluxo de trabalho, portanto, não precisa de nenhuma entrada de arquivo de bloqueio. Examine cada linha reescrita.

## 5. Manter o lockfile atualizado

Mantenha o arquivo de bloqueio atualizado com os arquivos de fluxo de trabalho e as atualizações de segurança do repositório.

1. **Execute novamente a extensão quando você alterar as dependências.** Execute `gh actions-lock` novamente sempre que você adicionar um fluxo de trabalho que tenha `uses` dependências ou adicionar ou remover `uses` dependências em um fluxo de trabalho existente.

2. **Deixe Dependabot lidar com incrementos de versão.** Quando Dependabot abre uma atualização de versão para uma ação em um fluxo de trabalho que você integrou, ela também regenera a entrada de lockfile correspondente no mesmo pull request. O arquivo de fluxo de trabalho e o arquivo de bloqueio não podem divergir.

Dependabot atualiza apenas as entradas de lockfile para fluxos de trabalho que já estão integrados. Se ele atualizar uma ação em um fluxo de trabalho que não está no arquivo de bloqueio, ele atualizará o arquivo de fluxo de trabalho normalmente e deixará o arquivo de bloqueio inalterado.

1. **Ressolva as referências que foram movidas.** A forma como a extensão lida com uma referência movida depende da referência:

   * **Uma ramificação ou versão parcial**, como `main` ou `v3`, mantém seu commit bloqueado, e a extensão relata um aviso de `ref-moved`. Para avançar, verifique o histórico de upstream e execute `gh actions-lock --relock`.
   * **Uma marca de versão completa**, como `v3.1.0`, deve apontar para seu commit bloqueado. Se a tag for movida, a extensão relatará um erro até que você execute `gh actions-lock --relock` ou altere a linha `uses:`.
   * **Um histórico reescrito**, em que o commit bloqueado não está mais no histórico da referência, por exemplo, após um force-push, é um erro que `--relock` não corrige. Depois de examinar o histórico de upstream, execute `gh actions-lock --accept-moved`. Não use `--accept-moved` na automação.

### Revisando alterações no lockfile

Examine as alterações no arquivo de bloqueio, como qualquer outra alteração de dependência:

* **Um código alterado `commit`** é o código que seus fluxos de trabalho executarão. Trate-o da maneira como você trataria qualquer outra atualização de versão de dependência.
* **Um(a) `owner_id` ou `repo_id` alterado(a)** deve ser raro. Isso significa que o repositório por trás desse nome **não** é aquele que você bloqueou originalmente, portanto, investigue antes de fazer merge.

Se um arquivo de bloqueio parecer errado, corrija os arquivos de fluxo de trabalho e regenere-o. Nunca edite o lockfile manualmente.

## Próximas Etapas

Depois de gerar um arquivo de bloqueio para um repositório, verifique se ele é aplicado e atualizado sem que os desenvolvedores precisem lembrar de executar comandos. Consulte [Aplicar lockfiles para dependências de ação](../administer/enforce-workflow-lockfiles.md).
