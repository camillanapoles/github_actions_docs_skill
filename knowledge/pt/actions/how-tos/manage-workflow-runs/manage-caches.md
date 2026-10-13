---
title: Gerenciando caches
description: Você pode monitorar, filtrar e excluir caches de dependência criados com base em seus fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/manage-caches
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Gerenciando caches { #managing-caches }

_Você pode monitorar, filtrar e excluir caches de dependência criados com base em seus fluxos de trabalho._

Este artigo descreve o gerenciamento de caches com a interface da GitHub Web, mas você também pode gerenciá-los:

* Uso da API REST. Confira [Pontos de extremidade da API REST para o cache do GitHub Actions](https://docs.github.com/pt/rest/actions/cache).
* Com o subcomando `gh cache` da linha de comando. Confira a [Documentação da CLI do GitHub](https://cli.github.com/manual/gh_cache).

## Exibir entradas de cache { #viewing-cache-entries }

É possível usar a interface da Web para exibir uma lista das entradas de cache de um repositório. Na lista de cache, é possível ver quanto espaço em disco cada cache está usando, quando os caches foram criados e quando foram usados pela última vez.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **(cache) Caches**.
4. Revise a lista de entradas de cache do repositório.

   * Para pesquisar as entradas de cache usadas para um branch específico, clique no menu suspenso **Branch** e selecione um branch. A lista de cache exibirá todos os caches usados para o branch selecionado.
   * Para pesquisar entradas de cache com uma chave de cache específica, use a sintaxe `key: key-name` no campo **Filtrar caches**. A lista de cache exibirá caches de todos os ramos onde a chave foi usada.

   ![Captura de tela da lista de entradas de cache.](/assets/images/help/repository/actions-cache-entry-list.png)

## Excluir entradas de cache { #deleting-cache-entries }

Os usuários com `write` acesso a um repositório podem usar a interface da GitHub Web para excluir entradas de cache.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, na seção "Management", clique em **(cache) Caches**.
4. À direita da entrada de cache que você deseja excluir, clique em (Delete cache).

   ![Captura de tela da lista de entradas de cache. Um ícone de lixeira, usado para excluir um cache, é realçado com um contorno laranja escuro.](/assets/images/help/repository/actions-cache-delete.png)

## Forçar a exclusão de entradas de cache { #force-deleting-cache-entries }

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
