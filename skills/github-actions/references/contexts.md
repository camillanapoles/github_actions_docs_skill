---
title: Contextos (github, secrets, vars, env, needs, matrix, steps, runner, inputs, jobs, strategy, job)
description: Tabela de decisão de contextos do GitHub Actions, disponibilidade por chave do workflow e receitas seguras.
source_page: knowledge/pt/actions/reference/workflows-and-actions/contexts.md
---

# Contextos — referência de decisão

Contextos são coleções de variáveis disponíveis em expressões `${{ }}`. Diferem das
**variáveis de ambiente padrão** (`$GITHUB_SHA`, `$RUNNER_OS`): estas só existem **no
runner**, durante a execução do step; contextos existem **antes** do job ir para o
runner (por isso funcionam em `if:`, `runs-on:`, `name:`, `concurrency:`).

> Fonte oficial capturada: `knowledge/pt/actions/reference/workflows-and-actions/contexts.md`
> Variáveis de ambiente padrão: `knowledge/pt/actions/reference/workflows-and-actions/variables.md`

## 1. Tabela de contextos

| Contexto | Tipo | O que contém |
| --- | --- | --- |
| `github` | object | `sha`, `ref`, `ref_name`, `ref_type`, `ref_protected`, `repository`, `repository_owner`, `repository_visibility`, `actor`, `actor_id`, `triggering_actor`, `event`, `event_name`, `event_path`, `workflow`, `workflow_ref`, `workflow_sha`, `run_id`, `run_number`, `run_attempt`, `job`, `server_url`, `api_url`, `graphql_url`, `token`, `workspace`, `action`, `action_path`, `action_repository`, `action_ref`, `action_status`, `step`, `triggering_payload`, `retention_days`, `head_ref`, `base_ref`, `path`, `output`? (não: use `GITHUB_OUTPUT`) |
| `env` | object | Variáveis definidas em `env:` de workflow, job ou step |
| `vars` | object | Configuration variables de repositório, organização e ambiente |
| `secrets` | object | Segredos (repo/org/ambiente) + `GITHUB_TOKEN` |
| `job` | object | `job.status`: `success`, `failure`, `cancelled`, `skipped` |
| `jobs` | object | Saídas de jobs de um **reusable workflow** (só em `workflow_call`) |
| `steps` | object | `steps.<id>.outputs.<name>`, `steps.<id>.outcome`, `steps.<id>.conclusion` |
| `runner` | object | `runner.os`, `runner.arch`, `runner.name`, `runner.environment`, `runner.temp`, `runner.tool_cache` |
| `strategy` | object | `strategy.fail-fast`, `strategy.job-index`, `strategy.job-total`, `strategy.max-parallel` |
| `matrix` | object | Valores da matriz do job atual |
| `needs` | object | `needs.<job_id>.outputs.<name>`, `needs.<job_id>.result` |
| `inputs` | object | Inputs de `workflow_dispatch` e de `workflow_call` |

## 2. Disponibilidade por chave do workflow

Regra prática: **quanto mais cedo no pipeline, menos contextos**.

| Chave | Contextos permitidos | Funções de status |
| --- | --- | --- |
| `run-name`, `concurrency` | `github`, `inputs`, `vars` | — |
| `env` (workflow) | `github`, `secrets`, `inputs`, `vars` | — |
| `jobs.<id>.if` | `github`, `needs`, `vars`, `inputs` | `always`, `cancelled`, `success`, `failure` |
| `jobs.<id>.runs-on` | `github`, `needs`, `strategy`, `matrix`, `vars`, `inputs` | — |
| `jobs.<id>.name`, `environment`, `container`, `services`, `concurrency`, `continue-on-error` | `github`, `needs`, `strategy`, `matrix`, `vars`, `inputs` | — |
| `jobs.<id>.container.credentials`, `services.<id>.credentials` | + `env`, `secrets` | — |
| `jobs.<id>.env`, `outputs.<id>`, `secrets.<id>`, `defaults.run` | `github`, `needs`, `strategy`, `matrix`, `vars`, `secrets`, `inputs` (+`env`, `job`, `runner`, `steps` em `outputs`) | — |
| `jobs.<id>.environment.url` | + `job`, `runner`, `env`, `steps` | — |
| `jobs.<id>.steps.<id>.if` | `github`, `needs`, `strategy`, `matrix`, `job`, `runner`, `env`, `vars`, `secrets`, `inputs`, `steps` | `always`, `cancelled`, `success`, `failure` |
| `jobs.<id>.steps.<id>.run`, `.with`, `.env`, `.name` | idem ao `if` do step | — |

`hashFiles()` só pode ser usada onde o workspace já existe (steps), nunca em
`runs-on:` ou `if:` de job.

Tabela oficial completa, chave por chave:
`knowledge/pt/actions/reference/workflows-and-actions/contexts.md` (seção
*Disponibilidade do contexto*).

## 3. Duas sintaxes de acesso

```yaml
${{ github.sha }}            # desreferência de propriedade
${{ github['sha'] }}         # índice (obrigatório para chaves com -, espaços, etc.)
${{ env['MINHA-VAR'] }}
${{ needs['build-job'].outputs['artifact-id'] }}
```

- Nome de propriedade para desreferência: começa com letra ou `_`, contém apenas
  alfanuméricos, `-` ou `_`.
- Propriedade inexistente → **string vazia** (não erro).

## 4. `secrets` — regras que mais causam incidente

1. `secrets.GITHUB_TOKEN` existe sempre, sem configuração. Escopo: o próprio
   repositório. Permissões controladas por `permissions:`.
2. **Actions compostas não recebem o contexto `secrets`.** Passe explicitamente:

   ```yaml
   # no workflow
   - uses: ./.github/actions/publicar
     with:
       token: ${{ secrets.PUBLISH_TOKEN }}
   ```

   ```yaml
   # .github/actions/publicar/action.yml
   inputs:
     token:
       description: "Token usado para publicar"
       required: true
   runs:
     using: composite
     steps:
       - run: echo "$INPUT_TOKEN" | gh auth login --with-token
         shell: bash
   ```

3. **Reusable workflows não herdam segredos automaticamente**:

   ```yaml
   # caller
   jobs:
     chamar:
       uses: octo-org/.github/.github/workflows/deploy.yml@v1
       with:
         ambiente: production
       secrets:
         AWS_ROLE_ARN: ${{ secrets.AWS_ROLE_ARN }}
       # ou, somente para repositório do mesmo owner/org:
       # secrets: inherit
   ```

4. `secrets` **não** está disponível em: `run-name`, `concurrency`,
   `jobs.<id>.if`, `runs-on`, `strategy`, `matrix`, `environment`, `env` de
   workflow (está em `env` de job/step), `container.image`.
5. Segredos de **ambiente** só existem se o job declarar `environment: <nome>` —
   e respeitam protection rules (revisores, branches, wait timer).
6. Nunca faça `echo` de segredo. Para valores derivados:
   `echo "::add-mask::${VALOR_DERIVADO}"` antes de usá-lo.
7. **Forks**: workflows disparados por `pull_request` de fork não recebem segredos
   nem `write` no `GITHUB_TOKEN`. Se precisar de segredos, use
   `pull_request_target` com gate de revisão ou `environment` protegido — e jamais
   faça checkout + execução do código do PR nesse job.

## 5. `vars` × `env` × variáveis padrão

| Mecanismo | Definido em | Acesso | Precedência |
| --- | --- | --- | --- |
| `vars.X` | Settings → Secrets and variables → Actions → Variables | `${{ vars.X }}` | ambiente > repositório > organização |
| `env.X` | `env:` no workflow, job ou step | `${{ env.X }}` ou `$X` no shell | step > job > workflow |
| `GITHUB_*` | injetadas pelo runner | `$GITHUB_SHA`, `$GITHUB_ENV`, `$GITHUB_OUTPUT`, `$GITHUB_PATH`, … | — |

Persistência entre steps:

```yaml
- name: Calcula versão
  id: ver
  run: |
    echo "version=$(node -p 'require("./package.json").version')" >> "$GITHUB_OUTPUT"
    echo "BUILD_DATE=$(date -u +%F)" >> "$GITHUB_ENV"
    echo "bin/" >> "$GITHUB_PATH"

- run: echo "${{ steps.ver.outputs.version }} em $BUILD_DATE"
```

## 6. Receitas rápidas

```yaml
# Só na branch padrão
if: github.ref == format('refs/heads/{0}', github.event.repository.default_branch)

# Só quando a API muda
on:
  pull_request:
    paths: ["api/**", "openapi.yaml"]

# Nome de execução legível
run-name: "${{ github.event_name }} · ${{ github.actor }} · ${{ inputs.env || github.ref_name }}"

# Matriz com include explícito
strategy:
  fail-fast: false
  matrix:
    include:
      - os: ubuntu-24.04
        node: 22
      - os: macos-14
        node: 22
runs-on: ${{ matrix.os }}

# Propagar saída entre jobs
jobs:
  build:
    outputs:
      image: ${{ steps.meta.outputs.image }}
    steps:
      - id: meta
        run: echo "image=ghcr.io/${{ github.repository }}:${{ github.sha }}" >> "$GITHUB_OUTPUT"
  deploy:
    needs: build
    if: needs.build.result == 'success'
    steps:
      - run: echo "deployando ${{ needs.build.image }}"

# Job-resumo que falha se qualquer dependência falhou
  report:
    if: always()
    needs: [build, test, deploy]
    steps:
      - name: Conclui
        run: |
          if [[ "${{ contains(needs.*.result, 'failure') }}" == "true" ]]; then
            echo "há jobs com falha"; exit 1
          fi
```

## 7. Armadilhas

- Em `pull_request`, `github.ref` é `refs/pull/<n>/merge` — use `github.base_ref`
  (destino) e `github.head_ref` (origem).
- `github.event.pull_request.*` só existe em eventos de PR; em `push` é `null`.
- `github.token` é o mesmo valor de `secrets.GITHUB_TOKEN` (prefira `secrets.`).
- Saídas de step são **strings**: use `fromJSON()` para comparar números.
- `hashFiles()` retorna string vazia se nada casar — combine: 
  `key: deps-${{ hashFiles('**/package-lock.json') || 'sem-lock' }}`.
- Expressões em `if:` de step/job não precisam de `${{ }}` (mas podem ter);
  em `run:` é **obrigatório** usar `${{ }}` ou variável de ambiente.
- Contextos não são expandidos dentro de `with:` de actions Docker de forma
  diferente: vale a mesma regra de disponibilidade da tabela §2.
