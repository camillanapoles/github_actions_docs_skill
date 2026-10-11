---
title: Segredos e variáveis (secrets, vars, GITHUB_TOKEN, ambientes)
description: Escopos, precedência, herança e boas práticas para segredos e configuration
  variables no GitHub Actions.
source_page: knowledge/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets.md
generated: true
canonical: https://github.com/camillanapoles/github_actions_docs_skill/blob/arena/c91bd6a1-github-actions-docs-skill/skills/github-actions/references/secrets-and-variables.md
---

# Segredos e variáveis

> Fontes oficiais capturadas:
> `knowledge/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets.md` ·
> `knowledge/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables.md` ·
> `knowledge/pt/actions/tutorials/authenticate-with-github_token.md`

## 1. O que usar para cada caso

| Necessidade | Mecanismo | Exemplo |
| --- | --- | --- |
| Credencial sensível (token, senha, chave) | **secret** | `secrets.NPM_TOKEN` |
| Valor de configuração não sensível (região, cluster, imagem base) | **variable** (`vars`) | `vars.AWS_REGION` |
| Autenticar no próprio repositório (push de tag, release, package) | **`GITHUB_TOKEN`** | `secrets.GITHUB_TOKEN` |
| Autenticar em outro repositório/org | PAT fino ou **GitHub App** | `secrets.CROSS_REPO_PAT` |
| Autenticar em nuvem (AWS/Azure/GCP/OCI) sem chave estática | **OIDC** (`id-token: write`) | ver `security-hardening.md` |
| Valor calculado durante o run | `GITHUB_OUTPUT` / `GITHUB_ENV` | ver `contexts.md` §5 |

## 2. Escopos e precedência

| Escopo | Onde configurar | Disponível para |
| --- | --- | --- |
| Repositório | Settings → Secrets and variables → Actions | todos os workflows do repo |
| Organização | Org → Settings → Secrets and variables → Actions | repos selecionados (all / selected / private) |
| Ambiente | Repo → Settings → Environments → `<env>` | somente jobs com `environment: <env>` |
| `GITHUB_TOKEN` | automático | somente o run atual, somente o repo atual |

Precedência: **ambiente > repositório > organização** (mesmo nome).

Variáveis (`vars`) seguem os mesmos escopos e a mesma precedência, mas **não** são
secretas: aparecem em logs se você as imprimir. Nunca coloque credencial em `vars`.

## 3. `GITHUB_TOKEN` na prática

```yaml
permissions:
  contents: write        # criar tag/release
  pull-requests: write   # comentar em PR
  id-token: write        # OIDC (só se usar)

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: true      # default; permite push com o token
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git tag -a "v$VERSION" -m "release" && git push origin "v$VERSION"
```

Fatos que evitam 90% dos erros:

- Criado automaticamente a cada run; expira ao fim do run (máx. 24 h).
- **Não** aciona novos workflows quando usado para `git push` (evita loops).
- Permissões vêm de `permissions:` (workflow/job). Se ausente, usa o default do
  repositório — defina sempre.
- Não atravessa repositórios: para push em outro repo, use PAT/App.
- Em `pull_request` de fork: read-only, sem acesso a segredos.
- `metadata: read` é implícito e não pode ser removido.

## 4. Padrões seguros de uso

```yaml
# ✅ correto: segredo via env, nunca interpolado no script
- name: Publica
  env:
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
    REGISTRY: ${{ vars.NPM_REGISTRY }}
  run: |
    echo "//${REGISTRY#https://}/:_authToken=${NPM_TOKEN}" > ~/.npmrc
    npm publish --registry "https://${REGISTRY}"

# ❌ errado: injeção + possível vazamento em log
- run: npm publish --token ${{ secrets.NPM_TOKEN }}
```

Regras:

1. Segredo **sempre** por `env:` (workflow/job/step) ou `with:` de action.
2. Nunca em `echo`, `printf`, URL, linha de comando visível, `name:` de step/job.
3. Nunca em artefatos, caches ou logs (`actions/upload-artifact` de `.npmrc` = vazamento).
4. Segredos não são passados a **composite actions** — use `inputs` explícitos.
5. Reusable workflows precisam de `secrets:` explícito (ou `inherit` no mesmo owner).
6. Rotacione em 90 dias; registre dono e finalidade no próprio nome
   (`NPM_TOKEN_PACKAGES_CI`).
7. Máscara automática: o runner mascara o valor do segredo nos logs. Valores
   derivados (ex.: base64 do segredo) **não** são mascarados — use
   `echo "::add-mask::$VALOR"`.
8. `secrets` não está disponível em `run-name`, `concurrency`, `if:` de job,
   `runs-on`, `strategy`, `matrix`, `environment`.

## 5. Segredos por ambiente (deploy com aprovação)

```yaml
jobs:
  deploy-prod:
    needs: [build, test]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
        env:
          DB_PASSWORD: ${{ secrets.DB_PASSWORD }}   # segredo DO AMBIENTE production
```

Configure em Settings → Environments: required reviewers, wait timer, branches
permitidos, deployment branches, e segredos/variáveis específicos. Segredos de
ambiente só são injetados quando o job declara `environment:`.

## 6. Como criar/configurar (CLI)

```bash
# segredo de repositório
gh secret set NPM_TOKEN --body "npm_..."
gh secret set AWS_ROLE_ARN --body "arn:aws:iam::123456789012:role/github-actions"

# segredo de ambiente
gh secret set DB_PASSWORD --env production --body "..."

# variável (não sensível)
gh variable set DEPLOY_CLUSTER --body "prod-eu-west-1"

# organização (repos selecionados)
gh secret set ORG_TOKEN --org minha-org --repos "repo-a,repo-b"

# listar
gh secret list
gh variable list
```

## 7. Diagnóstico rápido

| Sintoma | Causa provável | Correção |
| --- | --- | --- |
| `Error: Input required and not supplied: token` | segredo ausente/escopo errado | confira `gh secret list` e o escopo (repo/org/ambiente) |
| Segredo vazio só em PR de fork | comportamento esperado | use `pull_request_target` com gate, ou rode após merge |
| `Resource not accessible by integration` | `permissions:` insuficiente | adicione a permissão necessária no job |
| Segredo vazio em composite action | `secrets` não é exposto a composite | passe via `inputs` |
| Segredo vazio em reusable workflow | sem `secrets:`/`inherit` | declare `secrets:` no job `uses:` |
| Valor mascarado aparece como `***` no meio do log | esperado (máscara) | não tente "desmascarar"; use `add-mask` para derivados |
| `403` ao criar release com `GITHUB_TOKEN` | `permissions: contents: read` | mude para `contents: write` |
