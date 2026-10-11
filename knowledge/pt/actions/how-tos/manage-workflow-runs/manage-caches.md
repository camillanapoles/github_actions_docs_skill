---
title: Gerenciando caches
description: Você pode monitorar, filtrar e excluir caches de dependência criados com base em seus fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/manage-caches
captured: '2026-10-11'
section: GitHub Actions
---

# Gerenciando caches

_Você pode monitorar, filtrar e excluir caches de dependência criados com base em seus fluxos de trabalho._

Este artigo descreve o gerenciamento de caches com a interface da GitHub Web, mas você também pode gerenciá-los:

* Uso da API REST. Confira [Pontos de extremidade da API REST para o cache do GitHub Actions](https://docs.github.com/pt/rest/actions/cache).
* Com o subcomando `gh cache` da linha de comando. Confira a [Documentação da CLI do GitHub](https://cli.github.com/manual/gh_cache).

## Exibir entradas de cache

É possível usar a interface da Web para exibir uma lista das entradas de cache de um repositório. Na lista de cache, é possível ver quanto espaço em disco cada cache está usando, quando os caches foram criados e quando foram usados pela última vez.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-cache" aria-label="cache" role="img"><path d="M2.5 5.724V8c0 .248.238.7 1.169 1.159.874.43 2.144.745 3.62.822a.75.75 0 1 1-.078 1.498c-1.622-.085-3.102-.432-4.204-.975a5.565 5.565 0 0 1-.507-.28V12.5c0 .133.058.318.282.551.227.237.591.483 1.101.707 1.015.447 2.47.742 4.117.742.406 0 .802-.018 1.183-.052a.751.751 0 1 1 .134 1.494C8.89 15.98 8.45 16 8 16c-1.805 0-3.475-.32-4.721-.869-.623-.274-1.173-.619-1.579-1.041-.408-.425-.7-.964-.7-1.59v-9c0-.626.292-1.165.7-1.591.406-.42.956-.766 1.579-1.04C4.525.32 6.195 0 8 0c1.806 0 3.476.32 4.721.869.623.274 1.173.619 1.579 1.041.408.425.7.964.7 1.59 0 .626-.292 1.165-.7 1.591-.406.42-.956.766-1.578 1.04C11.475 6.68 9.805 7 8 7c-1.805 0-3.475-.32-4.721-.869a6.15 6.15 0 0 1-.779-.407Zm0-2.224c0 .133.058.318.282.551.227.237.591.483 1.101.707C4.898 5.205 6.353 5.5 8 5.5c1.646 0 3.101-.295 4.118-.742.508-.224.873-.471 1.1-.708.224-.232.282-.417.282-.55 0-.133-.058-.318-.282-.551-.227-.237-.591-.483-1.101-.707C11.102 1.795 9.647 1.5 8 1.5c-1.646 0-3.101.295-4.118.742-.508.224-.873.471-1.1.708-.224.232-.282.417-.282.55Z"></path><path d="M14.49 7.582a.375.375 0 0 0-.66-.313l-3.625 4.625a.375.375 0 0 0 .295.606h2.127l-.619 2.922a.375.375 0 0 0 .666.304l3.125-4.125A.375.375 0 0 0 15.5 11h-1.778l.769-3.418Z"></path></svg> Caches**.
4. Revise a lista de entradas de cache do repositório.

   * Para pesquisar as entradas de cache usadas para um branch específico, clique no menu suspenso **Branch** e selecione um branch. A lista de cache exibirá todos os caches usados para o branch selecionado.
   * Para pesquisar entradas de cache com uma chave de cache específica, use a sintaxe `key: key-name` no campo **Filtrar caches**. A lista de cache exibirá caches de todos os ramos onde a chave foi usada.

   ![Captura de tela da lista de entradas de cache.](/assets/images/help/repository/actions-cache-entry-list.png)

## Excluir entradas de cache

Os usuários com `write` acesso a um repositório podem usar a interface da GitHub Web para excluir entradas de cache.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-cache" aria-label="cache" role="img"><path d="M2.5 5.724V8c0 .248.238.7 1.169 1.159.874.43 2.144.745 3.62.822a.75.75 0 1 1-.078 1.498c-1.622-.085-3.102-.432-4.204-.975a5.565 5.565 0 0 1-.507-.28V12.5c0 .133.058.318.282.551.227.237.591.483 1.101.707 1.015.447 2.47.742 4.117.742.406 0 .802-.018 1.183-.052a.751.751 0 1 1 .134 1.494C8.89 15.98 8.45 16 8 16c-1.805 0-3.475-.32-4.721-.869-.623-.274-1.173-.619-1.579-1.041-.408-.425-.7-.964-.7-1.59v-9c0-.626.292-1.165.7-1.591.406-.42.956-.766 1.579-1.04C4.525.32 6.195 0 8 0c1.806 0 3.476.32 4.721.869.623.274 1.173.619 1.579 1.041.408.425.7.964.7 1.59 0 .626-.292 1.165-.7 1.591-.406.42-.956.766-1.578 1.04C11.475 6.68 9.805 7 8 7c-1.805 0-3.475-.32-4.721-.869a6.15 6.15 0 0 1-.779-.407Zm0-2.224c0 .133.058.318.282.551.227.237.591.483 1.101.707C4.898 5.205 6.353 5.5 8 5.5c1.646 0 3.101-.295 4.118-.742.508-.224.873-.471 1.1-.708.224-.232.282-.417.282-.55 0-.133-.058-.318-.282-.551-.227-.237-.591-.483-1.101-.707C11.102 1.795 9.647 1.5 8 1.5c-1.646 0-3.101.295-4.118.742-.508.224-.873.471-1.1.708-.224.232-.282.417-.282.55Z"></path><path d="M14.49 7.582a.375.375 0 0 0-.66-.313l-3.625 4.625a.375.375 0 0 0 .295.606h2.127l-.619 2.922a.375.375 0 0 0 .666.304l3.125-4.125A.375.375 0 0 0 15.5 11h-1.778l.769-3.418Z"></path></svg> Caches**.
4. À direita da entrada de cache que você deseja excluir, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-trash" aria-label="Delete cache" role="img"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"></path></svg>.

   ![Captura de tela da lista de entradas de cache. Um ícone de lixeira, usado para excluir um cache, é realçado com um contorno laranja escuro.](/assets/images/help/repository/actions-cache-delete.png)

## Forçar a exclusão de entradas de cache

Os caches têm restrições de escopo de ramificação em vigor, o que significa que alguns caches têm opções de uso limitadas. Para obter mais informações sobre as restrições do escopo de cache, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md). Se caches limitados a um branch específico estiverem usando um excesso de cota de armazenamento, isso poderá fazer com que os caches do branch `default` sejam criados e excluídos com alta frequência.

Por exemplo, um repositório pode ter muitas novas solicitações de pull abertas, cada qual com caches próprios restritos a um branch específico. Esses caches podem ocupar a maior parte do armazenamento em cache do repositório em questão.
Após um repositório atingir seu volume máximo de armazenamento em cache, a política de remoção de cache criará espaço excluindo os caches na ordem da última data de acesso, da mais antiga para a mais recente. Para evitar a eliminação de cache nessa situação, você pode configurar fluxos de trabalho que excluam caches em uma cadência mais rápida do que a política de remoção de cache. Você pode usar o GitHub CLI para excluir caches de ramificações específicas.

O fluxo de trabalho de exemplo a seguir usa `gh cache` para excluir até 100 caches criados por uma ramificação depois que uma pull request é fechada.

Para executar o exemplo a seguir em solicitações de pull entre repositórios ou solicitações de pull de bifurcação, acione o fluxo de trabalho com o evento `pull_request_target`. Quando você usa `pull_request_target` para acionar o fluxo de trabalho, algumas considerações de segurança são necessárias. Para saber mais, confira [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target).

```yaml
name: Cleanup github runner caches on closed pull requests
on:
  pull_request:
    types:
      - closed

jobs:
  cleanup:
    runs-on: ubuntu-latest
    permissions:
      actions: write
    steps:
      - name: Cleanup
        run: |
          echo "Fetching list of cache keys"
          cacheKeysForPR=$(gh cache list --ref $BRANCH --limit 100 --json id --jq '.[].id')

          ## Setting this to not fail the workflow while deleting cache keys.
          set +e
          echo "Deleting caches..."
          for cacheKey in $cacheKeysForPR
          do
              gh cache delete $cacheKey
          done
          echo "Done"
        env:
          GH_TOKEN: ${{ github.token }}
          GH_REPO: ${{ github.repository }}
          BRANCH: refs/pull/${{ github.event.pull_request.number }}/merge
```

Como alternativa, você pode usar a API para listar ou excluir automaticamente todos os caches em sua cadência. Para saber mais, confira [Pontos de extremidade da API REST para o cache do GitHub Actions](https://docs.github.com/pt/rest/actions/cache#about-the-cache-in-github-actions).
