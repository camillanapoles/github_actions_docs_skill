---
title: Managing caches
description: You can monitor, filter, and delete dependency caches created from your workflows.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-workflow-runs/manage-caches.md
captured: '2026-10-11'
section: How tos / Manage workflow runs
---

# Managing caches

_You can monitor, filter, and delete dependency caches created from your workflows._

This article describes managing caches with the GitHub web interface, but you can also manage them:

* Using the REST API. See [Cache](https://docs.github.com/rest/actions/cache).
* With the `gh cache` subcommand from the command line. See the [GitHub CLI documentation](https://cli.github.com/manual/gh_cache).

## Viewing cache entries

You can use the web interface to view a list of cache entries for a repository. In the cache list, you can see how much disk space each cache is using, when the cache was created, and when the cache was last used.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, under the "Management" section, click ** Caches**.
1. Review the list of cache entries for the repository.

   * To search for cache entries used for a specific branch, click the **Branch** dropdown menu and select a branch. The cache list will display all of the caches used for the selected branch.
   * To search for cache entries with a specific cache key, use the syntax `key: key-name` in the **Filter caches** field. The cache list will display caches from all branches where the key was used.

   ![Screenshot of the list of cache entries.](https://docs.github.com/assets/images/help/repository/actions-cache-entry-list.png)

## Deleting cache entries

Users with `write` access to a repository can use the GitHub web interface to delete cache entries.

1. On GitHub, navigate to the main page of the repository.
1. Under your repository name, click ** Actions**.

   ![Screenshot of the tabs for the "github/docs" repository. The "Actions" tab is highlighted with an orange outline.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
1. In the left sidebar, under the "Management" section, click ** Caches**.
1. To the right of the cache entry you want to delete, click .

   ![Screenshot of the list of cache entries. A trash can icon, used to delete a cache, is highlighted with a dark orange outline.](https://docs.github.com/assets/images/help/repository/actions-cache-delete.png)

## Force deleting cache entries

Caches have branch scope restrictions in place, which means some caches have limited usage options. For more information on cache scope restrictions, see [Dependency caching reference](../../reference/workflows-and-actions/dependency-caching.md). If caches limited to a specific branch are using a lot of storage quota, it may cause caches from the `default` branch to be created and deleted at a high frequency.

For example, a repository could have many new pull requests opened, each with their own caches that are restricted to that branch. These caches could take up the majority of the cache storage for that repository. Once a repository has reached its maximum cache storage, the cache eviction policy will create space by deleting the caches in order of last access date, from oldest to most recent. In order to prevent cache thrashing when this happens, you can set up workflows to delete caches on a faster cadence than the cache eviction policy will. You can use the GitHub CLI to delete caches for specific branches.

The following example workflow uses `gh cache` to delete up to 100 caches created by a branch once a pull request is closed.

To run the following example on cross-repository pull requests or pull requests from forks, you can trigger the workflow with the `pull_request_target` event. If you do use `pull_request_target` to trigger the workflow, there are security considerations to keep in mind. For more information, see [Events that trigger workflows](../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target#pull_request_target).

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

Alternatively, you can use the API to automatically list or delete all caches on your own cadence. For more information, see [Cache](https://docs.github.com/rest/actions/cache#about-the-cache-in-github-actions#about-the-cache-in-github-actions).
