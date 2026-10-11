---
title: Sintaxe de workflow (YAML) — mapa completo de chaves
description: Todas as chaves de um workflow e de um job/step do GitHub Actions, com tipos, defaults e exemplos mínimos válidos.
source_page: knowledge/pt/actions/reference/workflows-and-actions/workflow-syntax.md
---

# Sintaxe de workflow — mapa de chaves

> Fonte oficial capturada: `knowledge/pt/actions/reference/workflows-and-actions/workflow-syntax.md`
> Metadados de actions: `knowledge/pt/actions/reference/workflows-and-actions/metadata-syntax.md`

## 1. Esqueleto mínimo válido

```yaml
name: CI
on: push
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - run: echo "ok"
```

`name` é opcional (o GitHub usa o caminho do arquivo), mas **sempre** o defina:
aparece na UI, nos badges e nos logs.

## 2. Chaves de topo

| Chave | Tipo | Notas |
| --- | --- | --- |
| `name` | string | nome exibido |
| `run-name` | string | nome da execução (aceita expressões com `github`, `inputs`, `vars`) |
| `on` | string \| array \| map | gatilhos (YAML converte `on` em `true` — use `"on":` se houver ambiguidade) |
| `permissions` | map | escopo do `GITHUB_TOKEN` (`contents`, `issues`, `pull-requests`, `id-token`, `packages`, `deployments`, `actions`, `checks`, `statuses`, `metadata` (sempre read), `security-events`, `packages`, `pages`, `attestations`, …) |
| `env` | map | variáveis para todos os jobs (aceita `github`, `secrets`, `inputs`, `vars`) |
| `defaults` | map | `run.shell`, `run.working-directory` padrão |
| `concurrency` | string \| map | `group`, `cancel-in-progress` |
| `jobs` | map | obrigatório; máx. 256 jobs por matriz, 500 KB por arquivo |

## 3. `on` — formas

```yaml
on: push                                   # 1) evento único
on: [push, pull_request]                   # 2) lista
on:                                        # 3) mapa com filtros
  push:
    branches: [main, "release/**"]
    branches-ignore: ["experiment/**"]     # mutually exclusive com branches
    tags: ["v*"]
    paths: ["src/**", "pyproject.toml"]
    paths-ignore: ["docs/**", "**/*.md"]   # mutually exclusive com paths
  pull_request:
    types: [opened, synchronize, reopened, labeled, ready_for_review]
  schedule:
    - cron: "17 4 * * 1"                   # UTC; máx. 12 execuções/hora por repo
  workflow_dispatch:
    inputs:
      ambiente:
        description: "Ambiente de destino"
        required: true
        type: choice
        default: staging
        options: [staging, production]
      dry_run:
        description: "Simular"
        type: boolean
        default: false
      versao:
        description: "Tag a publicar"
        type: string
  workflow_call:                           # reusable workflow
    inputs: { versao: { type: string, required: true } }
    outputs: { url: { value: ${{ jobs.deploy.outputs.url }} } }
    secrets:
      DEPLOY_KEY:
        required: true
  release:
    types: [published]
  workflow_run:
    workflows: ["CI"]
    types: [completed]
  registry_package:
    types: [published]
  deployment_status: {}
  issue_comment:
    types: [created]
  label:
    types: [labeled]
  merge_group:
    types: [checks_requested]
```

Regras importantes:

- `paths-ignore` + `paths` no mesmo evento = erro de validação.
- `schedule` roda **apenas no branch padrão** (o arquivo precisa existir lá) e usa UTC.
- `workflow_run` não herda permissões do workflow disparador e não roda em fork.
- `pull_request` de fork: sem segredos, `GITHUB_TOKEN` read-only.
- Eventos com `types` exigem o tipo certo — `push` **não** tem `types`.

## 4. `jobs.<job_id>`

| Chave | Tipo | Notas |
| --- | --- | --- |
| `name` | string | exibição |
| `if` | expressão | `github`, `needs`, `vars`, `inputs` + funções de status |
| `needs` | string \| array \| map | dependências; aceita `needs: [a, b]` ou `needs: { a: { outputs: { x: ${{ ... } } } }` (fine-grained) |
| `runs-on` | string \| array | labels de runner; array = deve ter TODAS; grupos com `runs-on: [self-hosted, linux, gpu]`; larger runners: `ubuntu-24.04-16core`; `runs-on: ${{ matrix.os }}` |
| `permissions` | map | sobrescreve o topo |
| `environment` | string \| map | `{ name: production, url: https://… }` — habilita protection rules e segredos de ambiente |
| `concurrency` | string \| map | por job |
| `outputs` | map | `saida: ${{ steps.x.outputs.y }}` |
| `env` | map | variáveis do job |
| `defaults` | map | `run.shell` / `run.working-directory` |
| `steps` | array | obrigatório, exceto para jobs que chamam reusable (`uses:`) |
| `timeout-minutes` | int | default 360 (6 h) em hosted; defina sempre |
| `strategy` | map | `matrix`, `fail-fast` (default true), `max-parallel` |
| `continue-on-error` | bool | job falho não reprova o run |
| `container` | map | `image`, `credentials`, `env`, `ports`, `volumes`, `options` |
| `services` | map | containers auxiliares (postgres, redis, …) com `image`, `ports`, `env`, `healthcheck`, `options` |
| `uses` | string | caminho de reusable workflow: `owner/repo/.github/workflows/x.yml@ref` ou `./.github/workflows/x.yml` |
| `with` | map | inputs do reusable |
| `secrets` | map \| `inherit` | segredos passados ao reusable |

### Matriz

```yaml
strategy:
  fail-fast: false
  max-parallel: 4
  matrix:
    os: [ubuntu-24.04, macos-14, windows-2025]
    node: [20, 22]
    exclude:
      - os: macos-14
        node: 20
    include:
      - os: ubuntu-24.04
        node: 22
        coverage: true          # chave extra só nesta combinação
runs-on: ${{ matrix.os }}
```

- `include` adiciona combinações ou enriquece existentes (match por todas as chaves
  originais presentes).
- `exclude` remove antes do `include`.
- Limite: 256 jobs por execução.

## 5. `jobs.<job_id>.steps.<step>`

| Chave | Notas |
| --- | --- |
| `id` | necessário para `steps.<id>.outputs.*` e `steps.<id>.conclusion` |
| `name` | sempre defina (legibilidade no log) |
| `if` | aceita `github`, `needs`, `strategy`, `matrix`, `job`, `runner`, `env`, `vars`, `secrets`, `inputs`, `steps` + status functions |
| `uses` | action: `actions/checkout@v4`, `./.github/actions/local`, `docker://alpine:3.20`, `owner/repo/path@ref` |
| `with` | inputs da action |
| `run` | comando shell (uma linha ou bloco `|`) |
| `shell` | `bash` (default em Linux/mac), `pwsh` (default em Windows), `python`, `sh`, `cmd`, `powershell` |
| `working-directory` | diretório do step |
| `env` | variáveis do step |
| `continue-on-error` | step falho não reprova o job |
| `timeout-minutes` | limite do step |

**Default do shell bash no Actions**: `bash -e {0}` (falha no primeiro erro).
Para pipelines com `set -euo pipefail` explícito:

```yaml
defaults:
  run:
    shell: bash
    working-directory: backend
```

ou por step: `shell: bash --noprofile --norc -eo pipefail {0}`.

## 6. Services e containers

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: app_test
        ports: ["5432:5432"]
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    container:
      image: node:22-bookworm
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
        env:
          DATABASE_URL: postgres://postgres:postgres@postgres:5432/app_test
```

- Dentro de `container:`, o workspace é montado e o `actions/checkout` funciona,
  mas ferramentas do runner (ex.: `setup-node`) podem não existir na imagem.
- Hostname do service = nome da chave (`postgres`), não `localhost`.

## 7. Saídas, artefatos e dependências

```yaml
jobs:
  build:
    outputs:
      version: ${{ steps.v.outputs.version }}
      artifact-id: ${{ steps.up.outputs.artifact-id }}
    steps:
      - id: v
        run: echo "version=$(git describe --tags --always)" >> "$GITHUB_OUTPUT"
      - id: up
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
          retention-days: 5
          if-no-files-found: error

  release:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      - run: echo "publicando ${{ needs.build.outputs.version }}"
```

- Artefatos são imutáveis por nome; `upload-artifact@v4` não permite sobrescrever
  (use nomes distintos por matriz: `name: dist-${{ matrix.os }}`).
- `merge-multiple: true` no download junta artefatos de vários jobs.
- Retenção: 90 dias (público) / 400 dias (privado), configurável.

## 8. Concorrência

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}
```

- `cancel-in-progress: false` para deploy/release (fila e executa em ordem).
- Grupo por PR (não por branch) evita cancelar deploy de main.
- Máx. 100 runs em fila por grupo de concorrência.

## 9. Limites que afetam o desenho

| Item | Limite |
| --- | --- |
| Duração do workflow run | 35 dias |
| Duração de job (GitHub-hosted) | 6 horas |
| Duração de job (self-hosted) | 5 dias |
| Jobs por matriz | 256 |
| Tamanho do arquivo de workflow | 500 KB |
| Re-execuções por run | 50 |
| Fila de espera por job | 24 h |
| Aprovação de ambiente | 30 dias |
| Trigger events | 1500 eventos / 10 s / repositório |
| Jobs simultâneos (hosted padrão) | Free 20 · Pro 40 · Team 60 · Enterprise 500 (macOS: 5/5/5/50) |
| Cache: uploads/downloads/deletes | 200 / 1500 / 400 por minuto |

Detalhes: `knowledge/pt/actions/reference/limits.md`.

## 10. Metadados de action (`action.yml`)

```yaml
name: "Publica pacote"
description: "Publica o pacote no registro interno e comenta no PR"
author: "seu-time"
branding:
  icon: "package"
  color: "blue"
inputs:
  registry:
    description: "URL do registro"
    required: true
    default: "https://npm.pkg.github.com"
  token:
    description: "Token com permissão de publicação"
    required: true
outputs:
  version:
    description: "Versão publicada"
    value: ${{ steps.publish.outputs.version }}
runs:
  using: "composite"          # ou "node20" | "docker"
  steps:
    - id: publish
      shell: bash
      run: |
        VERSION=$(node -p 'require("./package.json").version')
        echo "version=$VERSION" >> "$GITHUB_OUTPUT"
```

- Composite: inputs viram `$INPUT_<NOME>` (maiúsculas, `-` → `_`); **sem** acesso a
  `secrets` (receba por input).
- Node: `using: node20`, `main: dist/index.js` (pré-compilado e commitado).
- Docker: `using: docker`, `image: Dockerfile`, `args`, `env`, `pre-entrypoint`,
  `post-entrypoint`; só roda em runner Linux.
