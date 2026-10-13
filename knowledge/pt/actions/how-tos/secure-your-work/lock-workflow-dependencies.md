---
title: Bloqueio de dependências de ação nos fluxos de trabalho de um repositório
description: Gere um arquivo de bloqueio que fixe cada ação que seus fluxos de trabalho usam em um commit verificado e mantenha-o atual à medida que suas dependências são alteradas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/lock-workflow-dependencies
captured: '2026-10-13'
section: How tos / Secure your work
---

# Bloqueio de dependências de ação nos fluxos de trabalho de um repositório

_Gere um arquivo de bloqueio que fixe cada ação que seus fluxos de trabalho usam em um commit verificado e mantenha-o atual à medida que suas dependências são alteradas._

> [!NOTE] Os arquivos de bloqueio de dependência de fluxo de trabalho estão em prévia pública e sujeitos a alterações.

Bloquear as dependências dos fluxos de trabalho garante que as ações referenciadas contenham o mesmo código que foi originalmente revisado. Para obter mais informações, consulte [Arquivos de bloqueio de dependências do fluxo de trabalho](../../concepts/security/workflow-dependency-lockfiles.md).

## 1. Verifique suas referências da ação

A criação de um arquivo de bloqueio fixa suas dependências em commits com base na referência de branch ou marca atual. Verifique se essas são as versões que você deseja fixar no lugar.

Verifique se cada referência `uses` em seus fluxos de trabalho aponta para uma versão atual e suportada da ação. Para obter as práticas recomendadas, consulte [Referência de uso seguro](../../reference/security/secure-use.md#using-third-party-actions).

Se qualquer um de seus fluxos de trabalho chamar um fluxo de trabalho reutilizável em outro repositório, verifique essas referências também. As dependências de fluxos de trabalho reutilizáveis são cobertas pelo arquivo de bloqueio do repositório em que o fluxo de trabalho reutilizável é definido. Se sua organização mantiver fluxos de trabalho compartilhados, recomendamos integrar esses repositórios primeiro. Consulte [Reutilizando configurações de fluxo de trabalho](../../concepts/workflows-and-actions/reusing-workflow-configurations.md).

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

Se a extensão relatar que ignorou um fluxo de trabalho porque não há suporte para ações de caminho local, isso significa que uma `uses: ./…` referência nesse fluxo de trabalho não foi resolvida para um arquivo de ação real. Os caminhos locais são resolvidos da raiz do repositório, **não** do diretório do arquivo que os contém, portanto, um caminho que parece bem ao lado de seu próprio arquivo pode não ser resolvido. Corrija o caminho e execute o comando novamente.

Para o conjunto completo de opções, execute `gh actions-lock --help`.

## 4. Examine as alterações e confirme

A extensão altera mais do que o arquivo de bloqueio, portanto, examine a diferença completa antes de fazer commit. Ele também reescreve as referências `uses` do seu fluxo de trabalho para a versão específica que ele resolveu, de modo que uma referência como `octo-org/deploy-action@v3` pode se tornar `octo-org/deploy-action@v3.1.0`. Isso torna a referência mais específica sem alterar o commit ao qual ela se refere.

Se o repositório, a organização ou a empresa permitirem apenas ações especificadas, verifique a lista de permissões antes de fazer commit. Depois que um fluxo de trabalho é adicionado, a lista de permissões é verificada em relação a SHAs de commit bloqueadas, porque uma tag pode ser movida para um código diferente, mas uma SHA bloqueada não pode. As entradas fixadas em uma tag, como `actions/checkout@v6`, não correspondem mais. Em vez disso, use um curinga ou o SHA completo do commit. Consulte [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-select-actions-and-reusable-workflows-to-run).

As referências a ações em seu próprio repositório também são reescritas, de `uses: ./…` para o equivalente `uses: $/…`, em seus fluxos de trabalho e em seus arquivos no repositório `action.yml` . Uma referência `$/…` sempre é resolvida para o commit em execução, portanto, ela é inerentemente fixada e não precisa de nenhuma entrada de lockfile.

## 5. Manter o lockfile atualizado

Mantenha o arquivo de bloqueio atualizado com os arquivos de fluxo de trabalho e as atualizações de segurança do repositório.

1. **Execute novamente a extensão quando você alterar as dependências.** Execute `gh actions-lock` novamente sempre que você adicionar um fluxo de trabalho que tenha `uses` dependências ou adicionar ou remover `uses` dependências em um fluxo de trabalho existente.

2. **Deixe Dependabot lidar com incrementos de versão.** Quando Dependabot abrir uma atualização de versão para uma ação em um workflow que você adicionou, ela também regenerará a entrada de arquivo de bloqueio correspondente na mesma pull request, para que o arquivo de workflow e o arquivo de bloqueio não possam se separar.

Dependabot
**não** configurará um fluxo de trabalho para você. Se ele atualizar uma dependência em um fluxo de trabalho sem entrada de arquivo de bloqueio, ele apenas relatará que a configuração inicial é necessária.

1. **Ressolva as referências que foram movidas.** As referências a branches ou versões parciais, como `main` ou `v3`, são confiáveis do arquivo de bloqueio e não têm a resolução refeita em uma execução normal. Se a extensão relatar um erro porque uma tag agora aponta para um commit upstream diferente, verifique primeiro o histórico do repositório upstream. Se a mudança for legítima, resolva novamente a referência com `gh actions-lock --relock`. Se o commit que você bloqueou originalmente não for mais acessível de forma alguma, por exemplo, porque o repositório upstream fez um push forçado ou o excluiu, `--relock` ainda relatará um erro. Para aceitar o novo commit, execute `gh actions-lock --relock --accept-moved`.

### Revisando alterações no lockfile

Examine as alterações no arquivo de bloqueio, como qualquer outra alteração de dependência:

* **Um código alterado `commit`** é o código que seus fluxos de trabalho executarão. Trate-o da maneira como você trataria qualquer outra atualização de versão de dependência.
* **Um(a) `owner_id` ou `repo_id` alterado(a)** deve ser raro. Isso significa que o repositório por trás desse nome **não** é aquele que você bloqueou originalmente, portanto, investigue antes de fazer merge.

Se um arquivo de bloqueio parecer errado, corrija os arquivos de fluxo de trabalho e regenere-o. Nunca edite o lockfile manualmente.

## Próximas Etapas

Depois de gerar um arquivo de bloqueio para um repositório, verifique se ele é aplicado e atualizado sem que os desenvolvedores precisem lembrar de executar comandos. Consulte [Aplicar lockfiles para dependências de ação](../administer/enforce-workflow-lockfiles.md).
