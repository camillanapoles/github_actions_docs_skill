---
title: Aprovando execuções de fluxo de trabalho de forks
description: Você pode aprovar manualmente as execuções de fluxo de trabalho disparadas pela solicitação de pull de um colaborador.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/approve-runs-from-forks
captured: '2026-10-26'
section: How tos / Manage workflow runs
---

# Aprovando execuções de fluxo de trabalho de forks

_Você pode aprovar manualmente as execuções de fluxo de trabalho disparadas pela solicitação de pull de um colaborador._

As execuções de fluxo de trabalho disparadas pela pull request de um colaborador em um fork podem exigir aprovação manual de um mantenedor com acesso de gravação. Você pode configurar os requisitos de aprovação de fluxo de trabalho para um [repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#controlling-changes-from-forks-to-workflows-in-public-repositories), uma [organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#configuring-required-approval-for-workflows-from-public-forks) ou uma [empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#fork-pull-request-workflows-from-outside-collaborators).

As execuções de fluxo de trabalho que aguardam aprovação há mais de 30 dias expiram e são marcadas como com falha. Uma anotação explica que a aprovação expirou.

## Aprovando as execuções do fluxo de trabalho em um pull request a partir de uma bifurcação pública

Os mantenedores com permissão de gravação a um repositório podem usar o seguinte procedimento para revisar e executar workflows em pull requests de colaboradores que exigem aprovação.

1. No nome do repositório, clique em **(git-pull-request) Solicitações pull**.
2. Na lista de solicitações pull, clique na solicitação pull que você quer revisar.
3. Na pull request, clique em **(file-diff) Files changed**.

   ![Captura de tela das guias de uma solicitação de pull. A guia "Arquivos alterados" está contornada em laranja escuro.](https://docs.github.com/assets/images/help/pull_requests/pull-request-tabs-changed-files.png)
4. Inspecione as alterações propostas no pull request e certifique-se de que você esteja confortável em executar seus fluxos de trabalho no branch do pull request. Você deve ficar especialmente atento para todas as alterações propostas no diretório `.github/workflows/` que afetem arquivos de fluxo de trabalho.
5. Se você se sentir à vontade com a execução de fluxos de trabalho no branch do pull request, clique no botão no canto superior direito rotulado Aguardando aprovação, o que abrirá o painel de status de mesclagem .
6. Localize e clique **em Aprovar fluxos de trabalho para serem executados**.
