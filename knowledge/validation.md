---
title: Validação e conformidade
description: Resultado automatizado das verificações de completude e conformidade da base de conhecimento e da skill.
generated: 2026-10-13T18:22:12+00:00
---

# Validação e conformidade

> Gerado por `scripts/validate.py` em **2026-10-13T18:22:12+00:00**  
> **29 verificações OK** · **3 avisos** · **7 falhas**

## Resumo da base de conhecimento

| Métrica | Valor |
| --- | --- |
| Páginas validadas | 500 |
| Bytes totais | 4,891,081 |
| Headings | 5,445 |
| Blocos de código | 2,730 |

## Verificações

| Grupo | Verificação | Status | Detalhe |
| --- | --- | --- | --- |
| inventory | pt: manifest presente | ✅ pass | 251 páginas declaradas, 251 ok, 252 arquivos .md em disco |
| inventory | pt: manifest ↔ disco | ✅ pass | todas as páginas declaradas existem em disco |
| inventory | pt: falhas de captura | ✅ pass | nenhuma falha de captura registrada |
| inventory | en: manifest presente | ✅ pass | 247 páginas declaradas, 247 ok, 248 arquivos .md em disco |
| inventory | en: manifest ↔ disco | ✅ pass | todas as páginas declaradas existem em disco |
| inventory | en: falhas de captura | ✅ pass | nenhuma falha de captura registrada |
| structure | frontmatter completo | ✅ pass | ok |
| structure | H1 único por página | ❌ fail | 77 ocorrência(s) — páginas com H1 duplicado/ausente |
| conversion | zero Liquid residual | ✅ pass | ok |
| conversion | zero HTML em bloco | ❌ fail | 84 ocorrência(s) — tags HTML de bloco fora de cercas de código |
| conversion | cercas balanceadas | ❌ fail | 5 ocorrência(s) — arquivos com cerca não fechada |
| conversion | tabelas bem formadas | ❌ fail | 34 ocorrência(s) — linhas com nº de células inconsistente |
| conversion | sem ruído de UI | ✅ pass | ok |
| conversion | alertas convertidos | ✅ pass | ok |
| conversion | AUTOTITLE resolvido | ✅ pass | ok |
| structure | tamanho mínimo | ✅ pass | ok |
| links | links internos resolvem | ❌ fail | 2975 links internos, 1 quebrados |
| links | âncoras existem | ⚠️ warn | 804 âncoras sem heading correspondente |
| links | links externos bem formados | ✅ pass | 2685 links externos, 0 malformados |
| navigation | mkdocs.yml válido | ✅ pass | site_name='GitHub Actions — Base de Conhecimento & Skill' |
| navigation | nav aponta para arquivos existentes | ✅ pass | 553 entradas no nav, 0 quebradas |
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

- `pt/actions/concepts/runners/actions-runner-controller.md: 7 H1 (esperado 1)`
- `pt/actions/concepts/security/workflow-dependency-lockfiles.md: 3 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/azure-kubernetes-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/azure-static-web-app.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/docker-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/google-kubernetes-engine.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/java-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/net-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/nodejs-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/php-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/deploy/deploy-to-third-party-platforms/python-to-azure-app-service.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md: 4 H1 (esperado 1)`
- `pt/actions/how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md: 2 H1 (esperado 1)`
- `pt/actions/how-tos/monitor-workflows/use-workflow-run-logs.md: 5 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws.md: 8 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure.md: 5 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-docker.md: 5 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform.md: 5 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-hashicorp-vault.md: 9 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-jfrog.md: 9 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-octopus-deploy.md: 5 H1 (esperado 1)`
- `pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-pypi.md: 5 H1 (esperado 1)`
- `pt/actions/reference/security/securely-using-pull_request_target.md: 2 H1 (esperado 1)`
- `pt/actions/reference/workflows-and-actions/contexts.md: 2 H1 (esperado 1)`
- … e mais 15 ocorrências

### ❌ conversion — zero HTML em bloco

- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:438: | condição | <ul><li>`jobs.<job_id>.if`</li><li>`jobs.<job_id>.steps[*].if`</li></ul> | Co`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:439: | contêiner | <ul><li>`jobs.<job_id>.container`</li><li>`jobs.<job_id>.name`</li></ul> | C`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:440: | integração contínua | <ul><li>`on.<push>.<branches>`</li><li>`on.<push>.<tags>`</li><li>`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:441: | cargo | <ul><li>`jobs.<job_id>`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:442: | solicitação de pull | <ul><li>`on.<pull_request>.<branches>`</li><li>`on.<pull_request>.`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:443: | fase | <ul><li>`jobs`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:444: | etapas | <ul><li>`jobs.<job_id>.steps`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:445: | estratégia | <ul><li>`jobs.<job_id>.strategy.fail-fast`</li><li>`jobs.<job_id>.strategy.`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:446: | timeoutInMinutes | <ul><li>`jobs.<job_id>.timeout-minutes`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:447: | variáveis | <ul><li>`env`</li><li>`jobs.<job_id>.env`</li><li>`jobs.<job_id>.steps.env`<`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:448: | implantação manual | <ul><li>`jobs.<job_id>.environment`</li></ul> | Suporte parcial |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:449: | pool | <ul><li>`runners`</li><li>`self hosted runners`</li></ul> | Suporte parcial |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:450: | serviços | <ul><li>`jobs.<job_id>.services`</li></ul> | Suporte parcial |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:451: | estratégia | <ul><li>`jobs.<job_id>.strategy`</li></ul> | Suporte parcial |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:452: | disparadores | <ul><li>`on`</li></ul> | Suporte parcial |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:453: | solicitação de pull | <ul><li>`on.<pull_request>.<tags>`</li></ul> | Sem suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:454: | schedules | <ul><li>`on.schedule`</li><li>`on.workflow_run`</li></ul> | Sem suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md:455: | disparadores | <ul><li>`on.<event_name>.types`</li></ul> | Sem suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:397: | gatilhos cron | <ul><li>`on.schedule`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:398: | ambiente | <ul><li>`env`</li><li>`jobs.<job_id>.env`</li><li>`jobs.<job_id>.steps.env`</`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:399: | executors | <ul><li>`runs-on`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:400: | trabalhos | <ul><li>`jobs`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:401: | cargo | <ul><li>`jobs.<job_id>`</li><li>`jobs.<job_id>.name`</li></ul> | Com suporte |`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:402: | matriz | <ul><li>`jobs.<job_id>.strategy`</li><li>`jobs.<job_id>.strategy.matrix`</li></`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md:403: | parâmetros | <ul><li>`env`</li><li>`workflow-dispatch.inputs`</li></ul> | Com suporte |`
- … e mais 15 ocorrências

### ❌ conversion — cercas balanceadas

- `en/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md: cerca de código não fechada`
- `en/actions/how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md: cerca de código não fechada`
- `en/actions/reference/workflows-and-actions/dockerfile-support.md: cerca de código não fechada`
- `en/actions/tutorials/build-and-test-code/ruby.md: cerca de código não fechada`
- `en/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md: cerca de código não fechada`

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
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bamboo-migration.md: linha de tabela com 3 células (esperado 4)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/bitbucket-pipelines-migration.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/gitlab-migration.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/jenkins-migration.md: linha de tabela com 2 células (esperado 3)`
- `pt/actions/tutorials/migrate-to-github-actions/automated-migrations/travis-ci-migration.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/reference/runners/github-hosted-runners.md: linha de tabela com 3 células (esperado 6)`
- `en/actions/reference/runners/larger-runners.md: linha de tabela com 7 células (esperado 5)`
- `en/actions/reference/security/oidc.md: linha de tabela com 2 células (esperado 3)`
- `en/actions/reference/workflows-and-actions/dependency-caching.md: linha de tabela com 3 células (esperado 2)`
- `en/actions/reference/workflows-and-actions/events-that-trigger-workflows.md: linha de tabela com 3 células (esperado 4)`
- `en/actions/reference/workflows-and-actions/variables.md: linha de tabela com 3 células (esperado 2)`
- `en/actions/reference/workflows-and-actions/workflow-commands.md: linha de tabela com 4 células (esperado 2)`
- … e mais 9 ocorrências

### ❌ links — links internos resolvem

- `en/actions/concepts/runners/support-for-arc.md:5: /support/contacting-github-support`

### ⚠️ links — âncoras existem

- `pt/actions/concepts/about-actions-policies.md:31: ../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target (âncora inexistente)`
- `pt/actions/concepts/security/compromised-runners.md:42: ../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token (âncora inexistente)`
- `pt/actions/concepts/security/secrets.md:25: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsenv (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/contexts.md:11: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategymatrix (âncora inexistente)`
- `pt/actions/concepts/workflows-and-actions/expressions.md:18: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idif (âncora inexistente)`
- `pt/actions/get-started/understand-github-actions.md:45: ../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsbackground (âncora inexistente)`
- `pt/actions/how-tos/administer/control-workflow-execution.md:11: ../../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target (âncora inexistente)`
- `pt/actions/how-tos/administer/enforce-workflow-lockfiles.md:75: ../secure-your-work/lock-workflow-dependencies.md#reviewing-lockfile-changes (âncora inexistente)`
- `pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions.md:54: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch (âncora inexistente)`
- `pt/actions/how-tos/create-and-publish-actions/release-and-maintain-actions.md:54: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target (âncora inexistente)`
- `pt/actions/how-tos/manage-runners/larger-runners/use-larger-runners.md:213: ../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on (âncora inexistente)`
- `pt/actions/how-tos/manage-runners/self-hosted-runners/apply-labels.md:19: #creating-a-custom-label-for-a-repository-runner`
- `pt/actions/how-tos/manage-runners/self-hosted-runners/run-scripts.md:34: ../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontinue-on-error (âncora inexistente)`
- `pt/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md:24: ../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on (âncora inexistente)`
- `pt/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md:989: deploy-runner-scale-sets.md#high-availability-and-automatic-failover (âncora inexistente)`
- `pt/actions/how-tos/manage-workflow-runs/manage-caches.md:50: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#pull_request_target (âncora inexistente)`
- `pt/actions/how-tos/manage-workflow-runs/manually-run-a-workflow.md:11: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch (âncora inexistente)`
- `pt/actions/how-tos/manage-workflow-runs/manually-run-a-workflow.md:31: ../../reference/workflows-and-actions/events-that-trigger-workflows.md#workflow_dispatch (âncora inexistente)`
- `pt/actions/how-tos/manage-workflow-runs/skip-workflow-runs.md:8: ../../reference/workflows-and-actions/workflow-syntax.md#onpushpull_requestpull_request_targetpathspaths-ignore (âncora inexistente)`
- `pt/actions/how-tos/manage-workflow-runs/skip-workflow-runs.md:8: ../../reference/workflows-and-actions/workflow-syntax.md#onpull_requestpull_request_targetbranchesbranches-ignore (âncora inexistente)`
- `pt/actions/how-tos/reuse-automations/reuse-workflows.md:36: ../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callinputs (âncora inexistente)`
- `pt/actions/how-tos/reuse-automations/reuse-workflows.md:36: ../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callsecrets (âncora inexistente)`
- `pt/actions/how-tos/reuse-automations/reuse-workflows.md:42: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsecretsinherit (âncora inexistente)`
- `pt/actions/how-tos/reuse-automations/reuse-workflows.md:65: ../../reference/workflows-and-actions/workflow-syntax.md#onworkflow_callsecrets (âncora inexistente)`
- `pt/actions/how-tos/reuse-automations/reuse-workflows.md:123: ../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_iduses (âncora inexistente)`
- … e mais 15 ocorrências

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
