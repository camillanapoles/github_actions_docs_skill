---
title: Injeções de script
description: Entenda os riscos de segurança associados a injeções de script e GitHub Actions fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/script-injections
captured: '2026-10-26'
section: Concepts / Security
---

# Injeções de script

_Entenda os riscos de segurança associados a injeções de script e GitHub Actions fluxos de trabalho._

## Entendendo o risco de injeções de script

Ao criar fluxos de trabalho, [ações personalizadas](../workflows-and-actions/custom-actions.md) e [ações compostas](../../tutorials/create-actions/create-a-composite-action.md), você sempre deve considerar se o seu código pode executar entradas não confiáveis de invasores. Isso pode ocorrer quando um invasor adiciona comandos maliciosos e scripts em um contexto. Quando seu fluxo de trabalho é executado, essas strings podem ser interpretadas como código, que então é executado no runner.

Os invasores podem adicionar um conteúdo próprio mal-intencionado ao [contexto `github`](../../reference/workflows-and-actions/contexts.md#github-context), que deve ser tratado como uma entrada potencialmente não confiável. Esses contextos geralmente terminam com `body`, `default_branch`, `email`, `head_ref`, `label`, `message`, `name`, `page_name`,`ref` e `title`. Por exemplo: `github.event.issue.title` ou `github.event.pull_request.body`.

Você deve garantir que esses valores não fluam diretamente para fluxos de trabalho, ações, chamadas de API ou para qualquer outro lugar onde possam ser interpretados como código executável. Ao adotar a mesma postura de programação defensiva que você usaria para qualquer outro código de aplicação privilegiada, você pode ajudar a reforçar a segurança do seu uso de GitHub Actions. Para obter mais informações sobre algumas das etapas que um invasor pode executar, confira [Referência de uso seguro](../../reference/security/secure-use.md).

Além disso, há outras fontes menos óbvias de entrada potencialmente não confiável como, por exemplo, nomes de branches e endereços de e-mail, que podem ser bastante flexíveis em termos de conteúdo permitido. Por exemplo, `zzz";echo${IFS}"hello";#` será um nome de branch válido e um possível vetor de ataque em um repositório de destino.

As seções a seguir explicam como você pode ajudar a mitigar o risco de injeção de scripts.

### Exemplo de um ataque de injeção de script

Um ataque de injeção de script pode ocorrer diretamente dentro do script embutido de um fluxo de trabalho. No exemplo a seguir, uma ação usa uma expressão para testar a validade de um título de pull request mas também adiciona o risco de injeção de script:

```yaml
      - name: Check PR title
        run: |
          title="${{ github.event.pull_request.title }}"
          if [[ $title =~ ^octocat ]]; then
          echo "PR title starts with 'octocat'"
          exit 0
          else
          echo "PR title did not start with 'octocat'"
          exit 1
          fi
```

Este exemplo é vulnerável à injeção do script porque o comando `run` é executado dentro de um script de shell temporário no executor. Antes que o script do shell seja executado, as expressões internas `${{ }}` são avaliadas e substituídas pelos valores resultantes, o que pode torná-lo vulnerável à injeção de comando do shell.

Para injetar comandos neste fluxo de trabalho, o invasor pode criar uma solicitação de pull com o título `a"; ls $GITHUB_WORKSPACE"`:

![Captura de tela do título de uma solicitação de pull no modo de edição. Um novo título foi inserido no campo: a"; ls $GITHUB_WORKSPACE".](https://docs.github.com/assets/images/help/actions/example-script-injection-pr-title.png)

Neste exemplo, o caractere `"` é usado para interromper a instrução `title="${{ github.event.pull_request.title }}"`, permitindo que o comando `ls` seja executado no runner. Você poderá ver a saída do comando `ls` no log:

```shell
Run title="a"; ls $GITHUB_WORKSPACE""
README.md
code.yml
example.js
```

Para obter as práticas recomendadas para manter a segurança dos runners, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).
