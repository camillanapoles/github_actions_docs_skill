---
title: Reusable workflows e actions compostas (reuso de pipelines)
description: Como criar, chamar, versionar e testar reusable workflows; inputs, outputs,
  secrets, herança e armadilhas.
source_page: knowledge/pt/actions/how-tos/reuse-automations.md
generated: true
canonical: https://github.com/camillanapoles/github_actions_docs_skill/blob/arena/c91bd6a1-github-actions-docs-skill/skills/github-actions/references/reusable-workflows.md
---

# Reuso de automações

> Fontes oficiais capturadas: `knowledge/pt/actions/how-tos/reuse-automations.md` ·
> `knowledge/pt/actions/how-tos/reuse-automations/reuse-workflows.md` ·
> `knowledge/pt/actions/tutorials/create-actions/create-a-composite-action.md`

## 1. Qual mecanismo escolher

| Necessidade | Mecanismo |
| --- | --- |
| Repetir **jobs inteiros** (build+test+deploy) em vários repositórios | reusable workflow (`workflow_call`) |
| Repetir **passos** com lógica (shell/script) dentro de um job | composite action (`runs.using: composite`) |
| Repetir passos com **runtime Node** (SDK do GitHub, API rica) | JavaScript action (`node20`) |
| Empacotar ferramenta/imagem específica | Docker container action |
| Compartilhar só variáveis/labels de runner | `vars` + runner labels |

## 2. Reusable workflow (callee)

```yaml
# .github/workflows/reusable-ci.yml   (no repo PROVIDER, ex.: octo-org/.github)
name: CI reutilizável
on:
  workflow_call:
    inputs:
      node-version:
        description: "Versão do Node"
        type: string
        default: "22"
      coverage:
        description: "Gerar cobertura"
        type: boolean
        default: false
      working-directory:
        type: string
        default: "."
    outputs:
      version:
        description: "Versão construída"
        value: ${{ jobs.build.outputs.version }}
      test-summary:
        value: ${{ jobs.test.outputs.summary }}
    secrets:
      SONAR_TOKEN:
        required: false
      REGISTRY_PASSWORD:
        required: true

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    defaults:
      run:
        working-directory: ${{ inputs.working-directory }}
    outputs:
      version: ${{ steps.v.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
          cache: npm
          cache-dependency-path: ${{ inputs.working-directory }}/package-lock.json
      - run: npm ci
      - id: v
        run: echo "version=$(node -p 'require("./package.json").version')" >> "$GITHUB_OUTPUT"
      - uses: actions/upload-artifact@v4
        with:
          name: dist-${{ inputs.node-version }}
          path: ${{ inputs.working-directory }}/dist

  test:
    needs: build
    runs-on: ubuntu-latest
    timeout-minutes: 25
    outputs:
      summary: ${{ steps.sum.outputs.summary }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: dist-${{ inputs.node-version }}
      - run: npm ci && npm test -- --coverage=${{ inputs.coverage }}
      - id: sum
        run: echo "summary=ok" >> "$GITHUB_OUTPUT"
      - if: ${{ inputs.coverage && secrets.SONAR_TOKEN != '' }}
        run: ./sonar-scan.sh
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Regras do callee:

- `on: workflow_call` (pode coexistir com `push`/`workflow_dispatch` para testar o
  próprio reusable).
- Tipos de input: `string`, `number`, `boolean`, `choice` (via `enum`? use
  `string` + validação), `environment`? (não — use string).
- `secrets:` precisa ser declarado; sem declaração, o caller não consegue passar.
- `outputs:` só podem referenciar outputs de **jobs** (não de steps diretamente).
- Um callee **não pode chamar outro callee** (aninhamento não suportado).
- Máx. de `inputs`: 10 por `workflow_call`? (limite prático: mantenha enxuto;
  valide em `jobs.<id>.if` se necessário).
- `GITHUB_TOKEN` do callee tem as permissões do **repositório chamador** se o
  caller for do mesmo owner; caso contrário, é o token do repo callee com escopo
  limitado — declare `permissions:` explícito.

## 3. Caller

```yaml
name: Pipeline do app
on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  ci:
    uses: octo-org/.github/.github/workflows/reusable-ci.yml@v1
    with:
      node-version: "22"
      coverage: ${{ github.ref_name == 'main' }}
      working-directory: apps/web
    secrets:
      REGISTRY_PASSWORD: ${{ secrets.REGISTRY_PASSWORD }}
      SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

  # mesma org/owner: pode herdar todos os segredos
  ci-lib:
    uses: ./.github/workflows/reusable-ci.yml
    secrets: inherit

  release:
    needs: ci
    if: github.ref_name == 'main' && needs.ci.result == 'success'
    uses: octo-org/.github/.github/workflows/reusable-release.yml@v1
    permissions:
      contents: write
      id-token: write
    with:
      version: ${{ needs.ci.outputs.version }}
```

Regras do caller:

- O job que chama **não pode ter `steps:`** (só `uses`, `with`, `secrets`,
  `permissions`, `if`, `needs`, `concurrency`, `secrets`).
- Caminho completo obrigatório: `owner/repo/.github/workflows/arquivo.yml@ref`
  (note o `/.github/` duplicado quando o reusable vive no repo `.github` da org)
  ou caminho local `./.github/workflows/arquivo.yml`.
- `ref` pode ser branch, tag ou SHA — **pin por tag/SHA** para produção.
- `secrets: inherit` funciona apenas para reusables do **mesmo** owner (user/org).
  Para repositório de terceiro, liste segredos explicitamente.
- Outputs: `${{ needs.<job>.outputs.<nome> }}`.
- O `GITHUB_TOKEN` usado pelo callee vem do **repositório chamador** quando o
  callee está no mesmo owner; permissões definidas no caller valem.
- `concurrency` no caller não cancela automaticamente jobs do callee — defina no
  callee também se necessário.

## 4. Matriz em reusable workflow

```yaml
# callee
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        node: ${{ fromJSON(inputs.node-versions) }}   # input string JSON
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

```yaml
# caller
    with:
      node-versions: '["20","22","24"]'
```

`inputs` de matriz precisam ser serializados: envie JSON string e use `fromJSON()`.

## 5. Composite actions

```yaml
# .github/actions/qualidade/action.yml
name: "Qualidade"
description: "Instala deps, roda lint e testes com cache"
inputs:
  node-version:
    description: "Versão do Node"
    default: "22"
  test-command:
    description: "Comando de teste"
    default: "npm test"
outputs:
  duration:
    description: "Duração em segundos"
    value: ${{ steps.t.outputs.duration }}
runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: npm
    - run: npm ci
      shell: bash
    - id: t
      run: |
        START=$SECONDS
        ${{ inputs.test-command }}
        echo "duration=$((SECONDS - START))" >> "$GITHUB_OUTPUT"
      shell: bash
```

Regras do composite:

- Cada step **exige** `shell:` (não há default).
- **Sem acesso a `secrets`** — receba por `inputs` (e nunca faça `echo`).
- Sem `run:` multi-linha com `|` e `shell: bash` ao mesmo tempo? É permitido;
  mas evite interpolar `${{ inputs.x }}` dentro de `run:` (injeção) → passe por
  `env:`.
- Pode usar `uses:` (inclusive outras actions locais e Docker em Linux).
- Outputs via `GITHUB_OUTPUT`; inputs viram `$INPUT_<NOME_UPPER_SNAKE>`.

## 6. Versionamento e distribuição

| Estratégia | Quando |
| --- | --- |
| Branch `main` | desenvolvimento interno, tolerância a mudanças |
| Tag `v1` / `v1.4.2` | consumidores externos; atualize com Dependabot |
| SHA imutável | produção crítica, auditoria |
| Repo `.github` da org | reusables compartilhados por toda a organização |

Boas práticas: changelog no repo provider, testes do próprio reusable com
`push`/`workflow_dispatch`, semântica de breaking changes (novo major), e
`permissions:` mínimas no callee.

## 7. Armadilhas

- Esquecer `secrets:` no callee → caller falha silenciosamente com valor vazio.
- `outputs:` no callee referenciando step (não job) → saída sempre vazia.
- Chamar reusable de repositório privado a partir de repo público → negado.
- `uses:` com caminho errado (`owner/repo/.github/workflows/x.yml` sem o segundo
  `.github/`) → "workflow file not found".
- Aninhamento de callables → não suportado.
- `if:` no job caller com `needs` de outro reusable → verifique `result`
  (`success`, `failure`, `cancelled`, `skipped`).
- Alterar o reusable na branch do PR afeta todos os callers que apontam para essa
  branch — pin por tag em produção.
