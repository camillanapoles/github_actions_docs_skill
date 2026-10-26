---
title: Grupos de runners
description: Use grupos de executores para controlar o acesso aos executores e organizar os executores em toda a sua organização ou empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/runner-groups
captured: '2026-10-26'
section: Concepts / Runners
---

# Grupos de runners

_Use grupos de executores para controlar o acesso aos executores e organizar os executores em toda a sua organização ou empresa._

## Sobre os grupos de executores

Para controlar o acesso aos executores no nível da organização, as organizações que usam o plano GitHub Team podem usar grupos de executores.Grupos de executores são usados para coletar grupos de executores e criar um limite de segurança em torno deles.

Quando você permite acesso a um grupo de executores, você pode ver o grupo de executores listado nas configurações do executor da organização. Como opção, você pode atribuir um repositório granular adicional ao grupo do executor.

Quando novos executores são criados, eles são atribuídos automaticamente ao grupo padrão, a menos que especificado de outra forma. Os executores só podem estar em um grupo por vez. Você pode mover os executores de um grupo para outro.

Os grupos de runners ajudam você a aplicar políticas de acesso consistentes para runners em toda a sua infraestrutura.

Com grupos de runners, você pode:

* Organizar executores avançados e auto-hospedar corredores
* Restringir quais organizações e repositórios podem usar executores específicos
* Rotear trabalhos para um grupo de executores específico em seu arquivo de fluxo de trabalho
* Definir limites de simultaneidade para controlar custos e capacidade

Você também pode desabilitar os executores padrão hospedados em GitHub, de modo que os trabalhos em Linux, Windows e macOS sejam executados por meio de grupos de executores em vez de rótulos padrão de executores. Para configurações de nível de organização, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization). Se você for um proprietário da empresa, consulte [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise).

## Próximas etapas

Para saber como usar grupos de executores para controlar o acesso a corredores maiores, consulte [Como controlar o acesso a executores maiores](../../how-tos/manage-runners/larger-runners/control-access.md).

Para obter informações sobre como rotear trabalhos para corredores em um grupo específico, confira [Escolhendo o executor para um trabalho](../../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#choosing-runners-in-a-group).
