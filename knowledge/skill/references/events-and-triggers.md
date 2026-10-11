---
title: Eventos e gatilhos — qual usar e com quais filtros
description: Matriz de decisão de eventos do GitHub Actions, types, filtros de branch/path,
  agendamentos, workflow_dispatch e workflow_call.
source_page: knowledge/pt/actions/reference/workflows-and-actions/events-that-trigger-workflows.md
generated: true
canonical: https://github.com/camillanapoles/github_actions_docs_skill/blob/arena/c91bd6a1-github-actions-docs-skill/skills/github-actions/references/events-and-triggers.md
---

# Eventos e gatilhos

> Fonte oficial capturada: `knowledge/pt/actions/reference/workflows-and-actions/events-that-trigger-workflows.md`

## 1. Matriz de decisão

| Objetivo | Evento | Configuração essencial |
| --- | --- | --- |
| CI em cada commit | `push` | `branches` + `paths` (ou `paths-ignore`) |
| CI em PR (com checks) | `pull_request` | `types: [opened, synchronize, reopened]` |
| CI em PR que precisa de segredos | `pull_request_target` | **com gate** (label/revisão); nunca execute código do head |
| Gate de merge (branch protection) | `merge_group` | `types: [checks_requested]` |
| Release/publicação | `release` | `types: [published]` |
| Deploy manual | `workflow_dispatch` | `inputs` com `type`, `default`, `options` |
| Pipeline compartilhado (reuso) | `workflow_call` | `inputs`, `outputs`, `secrets` |
| Reagir a outro workflow | `workflow_run` | `workflows: [...]`, `types: [completed]`, `branches` |
| Tarefa periódica | `schedule` | `cron` em UTC; só roda no branch padrão |
| Publicação de pacote | `registry_package` | `types: [published, updated]` |
| Automação de issues/PRs | `issues`, `issue_comment`, `pull_request_review`, `pull_request_review_comment` | `types` específicos |
| Deploy a partir de status | `deployment`, `deployment_status` | integração com deployments API |
| Forks de PR prontos para CI pesada | `pull_request` + `types: [ready_for_review]` | evite rodar em draft |
| Novo membro/label | `label`, `milestone`, `member`, `project_card` | automação leve |
| Push em outro repositório | não há evento direto | use `repository_dispatch` via API |
| Disparo externo (API/webhook) | `repository_dispatch` | `types: [meu-evento]`, `client_payload` |

## 2. `pull_request` × `pull_request_target` × `push`

| Aspecto | `push` | `pull_request` | `pull_request_target` |
| --- | --- | --- | --- |
| Contexto do código | branch do commit | merge ref do PR (`refs/pull/N/merge`) | branch **base** (destino) |
| `github.ref` | `refs/heads/<branch>` | `refs/pull/N/merge` | `refs/heads/<base>` |
| Segredos | sim | **não** em fork | sim |
| `GITHUB_TOKEN` | permissões do repo | read-only em fork | permissões do repo |
| Risco | baixo | baixo | **alto** se fizer checkout do head |
| Checks aparecem no PR | não (só no commit) | sim | sim |

Padrão seguro para `pull_request_target` (quando é realmente necessário, ex.:
postar comentário, adicionar label, rodar deploy de preview):

```yaml
on:
  pull_request_target:
    types: [labeled]
permissions:
  contents: read
  pull-requests: write
jobs:
  preview:
    if: contains(github.event.pull_request.labels.*.name, 'safe-to-test')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}   # só após gate humano/label
      - run: npm ci && npm test
```

## 3. Filtros que evitam custo

```yaml
on:
  push:
    branches: [main]
    paths: ["api/**", "shared/**"]
  pull_request:
    paths-ignore: ["docs/**", "**/*.md", ".github/ISSUE_TEMPLATE/**"]
    types: [opened, synchronize, reopened, ready_for_review]
```

- `paths` e `paths-ignore` são **mutuamente exclusivos** no mesmo evento.
- `branches` e `branches-ignore` também.
- Em monorepo, combine `paths` com `dorny/paths-filter` ou com jobs condicionais
  (`if: steps.filter.outputs.api == 'true'`) para pipelines parciais.
- `tags` filtra só pushes de tag (`v*` é um padrão glob, não regex).

## 4. `workflow_dispatch` — inputs tipados

```yaml
on:
  workflow_dispatch:
    inputs:
      ambiente:
        description: "Ambiente de destino"
        type: choice
        required: true
        default: staging
        options: [staging, production]
      versao:
        description: "Tag/versão (vazio = HEAD)"
        type: string
        required: false
      dry_run:
        description: "Apenas simular"
        type: boolean
        default: false
      log_level:
        description: "Verbosidade"
        type: string
        default: info
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.ambiente }}
    steps:
      - run: echo "deploy ${{ inputs.versao || github.sha }} dry_run=${{ inputs.dry_run }}"
```

- Tipos suportados: `string`, `boolean`, `choice`, `environment`, `date`.
- `boolean` chega como **string** `'true'`/`'false'` → compare com `== true`? Não:
  use `${{ inputs.dry_run == true }}` (o GitHub converte) ou `== 'true'` se vier de
  API/CLI. Prefira testar as duas formas em `workflow_call`.
- Disparo via CLI: `gh workflow run deploy.yml -f ambiente=production -f versao=v1.2.3`
- Máx. 10 inputs.

## 5. `schedule` — cron

```yaml
on:
  schedule:
    - cron: "17 4 * * 1-5"   # 04:17 UTC, dias úteis
```

- Formato: `minuto hora dia-do-mês mês dia-da-semana` (**UTC**).
- Só o workflow do **branch padrão** é agendado.
- Atrasos são comuns em picos; não use para SLA rígido.
- O agendamento é **desativado automaticamente** se o repositório ficar 60 dias sem
  atividade (reative com um commit/`workflow_dispatch`).
- Evite `cron: "0 0 * * *"` (meia-noite exata concentra carga) — use minutos
  aleatórios, ex.: `17`, `42`.

## 6. `workflow_run` — encadeamento entre workflows

```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]
jobs:
  notificar:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - run: echo "CI ${{ github.event.workflow_run.id }} concluída"
```

- Roda no contexto do **branch padrão** e com as permissões do repositório base
  (por isso é útil para reagir a PRs de fork **depois** da validação).
- `github.event.workflow_run.head_sha` permite checkout do commit validado.
- Não encadeie mais de um nível (não dispara outro `workflow_run`).

## 7. `repository_dispatch` — gatilho externo

```bash
curl -L -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"deploy-preview","client_payload":{"pr":123,"env":"staging"}}'
```

```yaml
on:
  repository_dispatch:
    types: [deploy-preview]
jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - run: echo "PR ${{ github.event.client_payload.pr }}"
```

Exige token com `repo` (PAT clássico) ou fine-grained com `contents: write` no repo.

## 8. Checklist do gatilho

1. O evento entrega o código certo? (`push` vs `pull_request` vs `pull_request_target`)
2. Precisa de segredos? Fork bloqueia? Há gate seguro?
3. Filtros (`paths`, `branches`, `types`) reduzem execuções inúteis?
4. `concurrency` evita runs duplicados no mesmo ref?
5. `permissions` mínimo para o que o evento exige (ex.: `pull-requests: write` só
   se comentar no PR)?
6. `schedule` está no branch padrão e em UTC com minuto não-redondo?
7. `workflow_dispatch` tem inputs tipados com defaults sensatos?
