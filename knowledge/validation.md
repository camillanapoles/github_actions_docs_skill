---
title: Validação e conformidade
description: Resultado automatizado das verificações de completude e conformidade da base de conhecimento e da skill.
generated: 2026-10-13T14:14:39+00:00
---

# Validação e conformidade

> Gerado por `scripts/validate.py` em **2026-10-13T14:14:39+00:00**  
> **27 verificações OK** · **3 avisos** · **9 falhas**

## Resumo da base de conhecimento

| Métrica | Valor |
| --- | --- |
| Páginas validadas | 496 |
| Bytes totais | 4,827,608 |
| Headings | 4,633 |
| Blocos de código | 2,592 |

## Verificações

| Grupo | Verificação | Status | Detalhe |
| --- | --- | --- | --- |
| inventory | pt: manifest presente | ✅ pass | 247 páginas declaradas, 247 ok, 248 arquivos .md em disco |
| inventory | pt: manifest ↔ disco | ✅ pass | todas as páginas declaradas existem em disco |
| inventory | pt: falhas de captura | ✅ pass | nenhuma falha de captura registrada |
| inventory | en: manifest presente | ✅ pass | 247 páginas declaradas, 247 ok, 248 arquivos .md em disco |
| inventory | en: manifest ↔ disco | ✅ pass | todas as páginas declaradas existem em disco |
| inventory | en: falhas de captura | ✅ pass | nenhuma falha de captura registrada |
| structure | frontmatter completo | ✅ pass | ok |
| structure | H1 único por página | ❌ fail | 2 ocorrência(s) — páginas com H1 duplicado/ausente |
| conversion | zero Liquid residual | ✅ pass | ok |
| conversion | zero HTML em bloco | ✅ pass | ok |
| conversion | cercas balanceadas | ❌ fail | 8 ocorrência(s) — arquivos com cerca não fechada |
| conversion | tabelas bem formadas | ❌ fail | 28 ocorrência(s) — linhas com nº de células inconsistente |
| conversion | sem ruído de UI | ✅ pass | ok |
| conversion | alertas convertidos | ✅ pass | ok |
| conversion | AUTOTITLE resolvido | ❌ fail | 1 ocorrência(s) — placeholders `[AUTOTITLE]` restantes |
| structure | tamanho mínimo | ❌ fail | 14 ocorrência(s) — páginas com menos de 400 bytes |
| links | links internos resolvem | ❌ fail | 3230 links internos, 278 quebrados |
| links | âncoras existem | ⚠️ warn | 920 âncoras sem heading correspondente |
| links | links externos bem formados | ❌ fail | 2419 links externos, 2 malformados |
| navigation | mkdocs.yml válido | ✅ pass | site_name='GitHub Actions — Base de Conhecimento & Skill' |
| navigation | nav aponta para arquivos existentes | ✅ pass | 548 entradas no nav, 0 quebradas |
| navigation | sem páginas órfãs | ✅ pass | 0 páginas fora do nav e sem link de entrada |
| navigation | índice index.md | ✅ pass | presente |
| navigation | índice pt/index.md | ✅ pass | presente |
| navigation | índice en/index.md | ✅ pass | presente |
| navigation | índice skill/index.md | ✅ pass | presente |
| skill | SKILL.md com frontmatter | ✅ pass | name='github-actions' description=681 chars |
| skill | name válido (≤64, [a-z0-9-]) | ✅ pass | github-actions |
| skill | description válida (≤1024, não vazia) | ✅ pass | 681 caracteres |
| skill | license declarado | ✅ pass | MIT |
| skill | referências do SKILL.md existem | ❌ fail | 21 caminhos citados, 14 ausentes |
| skill | pasta references/ | ✅ pass | 7 documentos de referência |
| skill | templates presentes | ❌ fail | 0 arquivos (0 YAML) |
| skill | templates YAML válidos | ✅ pass | 0 inválidos de 0 |
| skill | estrutura de workflows/actions | ✅ pass | 0 problemas estruturais |
| skill | permissions explícito | ✅ pass | 0 templates sem `permissions` |
| skill | actions pinadas (tag/SHA) | ✅ pass | 0 referências sem pin |
| tools | actionlint | ⚠️ warn | binário não encontrado (instalado no CI via .github/workflows/validate.yml) |
| tools | yamllint | ⚠️ warn | yamllint não instalado localmente (rodado no CI) |

## Detalhes das ocorrências

### ❌ structure — H1 único por página

- `pt/actions/reference/workflows-and-actions/workflow-syntax.md: 6 H1 (esperado 1)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md: 3 H1 (esperado 1)`

### ❌ conversion — cercas balanceadas

- `pt/actions/reference/workflows-and-actions/workflow-syntax.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bamboo-migration.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/gitlab-migration.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/jenkins-migration.md: cerca de código não fechada`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/travis-ci-migration.md: cerca de código não fechada`
- `en/actions/tutorials/build-and-test-code/rust.md: cerca de código não fechada`

### ❌ conversion — tabelas bem formadas

- `pt/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments.md: linha de tabela com 3 células (esperado 1)`
- `pt/actions/reference/limits.md: linha de tabela com 1 células (esperado 5)`
- `pt/actions/reference/runners/github-hosted-runners.md: linha de tabela com 3 células (esperado 6)`
- `pt/actions/reference/runners/larger-runners.md: linha de tabela com 7 células (esperado 5)`
- `pt/actions/reference/security/oidc.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/reference/workflows-and-actions/dependency-caching.md: linha de tabela com 3 células (esperado 2)`
- `pt/actions/reference/workflows-and-actions/events-that-trigger-workflows.md: linha de tabela com 3 células (esperado 4)`
- `pt/actions/reference/workflows-and-actions/variables.md: linha de tabela com 3 células (esperado 2)`
- `pt/actions/reference/workflows-and-actions/workflow-commands.md: linha de tabela com 4 células (esperado 2)`
- `pt/actions/reference/workflows-and-actions/workflow-syntax.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/build-and-test-code/python.md: linha de tabela com 2 células (esperado 4)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bitbucket-pipelines-migration.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/reference/runners/github-hosted-runners.md: linha de tabela com 3 células (esperado 6)`
- `en/actions/reference/runners/larger-runners.md: linha de tabela com 7 células (esperado 5)`
- `en/actions/reference/security/oidc.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/reference/workflows-and-actions/dependency-caching.md: linha de tabela com 3 células (esperado 2)`
- `en/actions/reference/workflows-and-actions/events-that-trigger-workflows.md: linha de tabela com 3 células (esperado 4)`
- `en/actions/reference/workflows-and-actions/variables.md: linha de tabela com 3 células (esperado 2)`
- `en/actions/reference/workflows-and-actions/workflow-commands.md: linha de tabela com 4 células (esperado 2)`
- `en/actions/reference/workflows-and-actions/workflow-syntax.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/tutorials/build-and-test-code/python.md: linha de tabela com 2 células (esperado 4)`
- `en/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/tutorials/migrate-to-github-actions/automated-migrations/bamboo-migration.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/tutorials/migrate-to-github-actions/automated-migrations/bitbucket-pipelines-migration.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md: linha de tabela com 2 células (esperado 3)`
- … e mais 3 ocorrências

### ❌ conversion — AUTOTITLE resolvido

- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-jfrog.md:25`

### ❌ structure — tamanho mínimo

- `en/actions/concepts/index.md: 377 bytes`
- `en/actions/concepts/runners/index.md: 351 bytes`
- `en/actions/concepts/security/index.md: 359 bytes`
- `en/actions/get-started/index.md: 321 bytes`
- `en/actions/how-tos/administer/index.md: 395 bytes`
- `en/actions/how-tos/deploy/index.md: 363 bytes`
- `en/actions/how-tos/index.md: 351 bytes`
- `en/actions/how-tos/manage-runners/index.md: 395 bytes`
- `en/actions/reference/index.md: 359 bytes`
- `en/actions/reference/runners/index.md: 375 bytes`
- `en/actions/reference/security/index.md: 377 bytes`
- `en/actions/tutorials/create-actions/index.md: 379 bytes`
- `en/actions/tutorials/index.md: 393 bytes`
- `en/actions/tutorials/publish-packages/index.md: 379 bytes`

### ❌ links — links internos resolvem

- `pt/actions/concepts/runners/actions-runner-controller.md:18: /assets/images/help/actions/arc-diagram.png`
- `pt/actions/concepts/security/openid-connect.md:27: /assets/images/help/actions/oidc-architecture.png`
- `pt/actions/concepts/security/script-injections.md:40: /assets/images/help/actions/example-script-injection-pr-title.png`
- `pt/actions/concepts/workflows-and-actions/reusing-workflow-configurations.md:23: /assets/images/help/actions/reusable-workflows-ci-cd.png`
- `pt/actions/concepts/workflows-and-actions/workflows.md:27: /assets/images/help/actions/overview-actions-simple.png`
- `pt/actions/get-started/quickstart.md:82: /assets/images/help/repository/actions-quickstart-commit-new-file.png`
- `pt/actions/get-started/quickstart.md:94: /assets/images/help/repository/actions-tab-global-nav-update.png`
- `pt/actions/get-started/quickstart.md:98: /assets/images/help/repository/actions-quickstart-workflow-sidebar.png`
- `pt/actions/get-started/quickstart.md:104: /assets/images/help/repository/actions-quickstart-job.png`
- `pt/actions/get-started/quickstart.md:108: /assets/images/help/repository/actions-quickstart-logs.png`
- `pt/actions/get-started/quickstart.md:112: /assets/images/help/repository/actions-quickstart-log-detail.png`
- `pt/actions/get-started/understand-github-actions.md:19: /assets/images/help/actions/overview-actions-simple.png`
- `pt/actions/how-tos/administer/view-metrics.md:16: /assets/images/help/organizations/org-nav-insights-tab.png`
- `pt/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace.md:63: /assets/images/help/releases/release-link.png`
- `pt/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace.md:66: /assets/images/help/releases/edit-release-pencil.png`
- `pt/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace.md:85: /assets/images/marketplace/verified-creator-badge-for-actions.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules.md:46: /assets/images/help/repository/repo-actions-settings.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments.md:209: /assets/images/help/repository/actions-workflow-status-badge.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules.md:21: /assets/images/help/actions/actions-repo-permissions-read-only.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules.md:25: /assets/images/help/actions/actions-deployments-repo-permissions-read-and-write.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules.md:29: /assets/images/help/actions/actions-subscribe-to-events-deployment-protection-rules.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments.md:28: /assets/images/help/repository/repo-actions-settings.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments.md:85: /assets/images/help/repository/repo-actions-settings.png`
- `pt/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments.md:30: /assets/images/actions-bypass-env-protection-rules.png`
- `pt/actions/how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md:13: /assets/images/help/actions/actions-oidc-gateway.png`
- … e mais 15 ocorrências

### ⚠️ links — âncoras existem

- `pt/actions/concepts/about-actions-policies.md:31: ../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target (âncora inexistente)`
- `pt/actions/concepts/billing-and-usage.md:9: ../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#standard-github-hosted-runners-for-public-repositories (âncora inexistente)`
- `pt/actions/concepts/runners/github-hosted-runners.md:35: ../../reference/security/secure-use.md#reviewing-the-supply-chain-for-github-hosted-runners (âncora inexistente)`
- `pt/actions/concepts/runners/runner-groups.md:30: ../../how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#choosing-runners-in-a-group (âncora inexistente)`
- `pt/actions/concepts/security/compromised-runners.md:42: ../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token (âncora inexistente)`
- `pt/actions/concepts/security/openid-connect.md:80: ../../reference/security/oidc.md#immutable-subject-claims (âncora inexistente)`
- `pt/actions/concepts/security/openid-connect.md:86: ../../reference/security/oidc.md#methods-for-requesting-the-oidc-token (âncora inexistente)`
- `pt/actions/concepts/security/openid-connect.md:100: ../../reference/security/oidc.md#including-repository-custom-properties-in-oidc-tokens (âncora inexistente)`
- `pt/actions/concepts/security/openid-connect.md:136: ../../reference/security/oidc.md#including-repository-custom-properties-in-oidc-tokens (âncora inexistente)`
- `pt/actions/concepts/security/script-injections.md:51: ../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks (âncora inexistente)`
- `pt/actions/concepts/security/secrets.md:25: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsenv (âncora inexistente)`
- `pt/actions/concepts/security/secrets.md:41: ../../reference/security/secure-use.md#use-secrets-for-sensitive-information (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/contexts.md:11: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrix (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/contexts.md:18: ../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/expressions.md:18: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/expressions.md:21: ../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/reusing-workflow-configurations.md:60: ../../reference/security/secure-use.md#reusing-third-party-workflows (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/reusing-workflow-configurations.md:84: ../../reference/workflows-and-actions/reusing-workflow-configurations.md#yaml-anchors-and-aliases (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/workflows.md:25: ../../get-started/understand-github-actions.md#the-components-of-github-actions (âncora inexistente)`
- `pt/actions/get-started/understand-github-actions.md:45: ../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsbackground (âncora inexistente)`
- `pt/actions/how-tos/administer/control-workflow-execution.md:11: ../../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target (âncora inexistente)`
- `pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions.md:54: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch (âncora inexistente)`
- `pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions.md:54: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target (âncora inexistente)`
- `pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions.md:78: ../../reference/security/secure-use.md#protecting-actions-youve-created (âncora inexistente)`
- `pt/actions/how-tos/get-support.md:23: manage-runners/self-hosted-runners/monitor-and-troubleshoot.md#reviewing-the-self-hosted-runner-application-log-files (âncora inexistente)`
- … e mais 15 ocorrências

### ❌ links — links externos bem formados

- `pt/actions/reference/workflows-and-actions/dockerfile-support.md:97: http://man7.org/linux/man-pages/man7/capabilities.7.html`
- `en/actions/reference/workflows-and-actions/dockerfile-support.md:100: http://man7.org/linux/man-pages/man7/capabilities.7.html`

### ❌ skill — referências do SKILL.md existem

- `references/checklists.md`
- `references/gitops-patterns.md`
- `references/knowledge-base-map.md`
- `references/migration.md`
- `references/runners.md`
- `references/templates-catalog.md`
- `references/troubleshooting.md`
- `scripts/build_site.py`
- `scripts/extract.py`
- `scripts/install_tools.sh`
- `scripts/lint_workflows.sh`
- `scripts/new_workflow.py`
- `scripts/validate.py`
- `scripts/validate_skill.py`


## Artefatos

| Arquivo | Descrição |
| --- | --- |
| `knowledge/pt/manifest.json` | inventário da captura pt-BR (por página: título, bytes, headings, avisos) |
| `knowledge/en/manifest.json` | inventário do espelho inglês (source-of-truth github/docs) |
| `.ci/extract-report.md` | relatório de execução da captura |
| `.ci/validation.json` | resultado desta validação em JSON |
| `knowledge/validation.md` | este relatório em Markdown (navegável no MkDocs) |

## Como reproduzir

```bash
python3 scripts/validate.py --report knowledge/validation.md --json .ci/validation.json
# com verificações online (completude vs docs.github.com) e build estrito:
python3 scripts/validate.py --online --mkdocs
```
