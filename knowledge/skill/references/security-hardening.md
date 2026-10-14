---
title: Endurecimento de segurança (hardening) e OIDC
description: Menor privilégio, injeção de script, pull_request_target, supply chain
  (pin), OIDC por provedor, self-hosted runners e attestation.
source_page: knowledge/pt/actions/reference/security/secure-use.md
generated: true
canonical: https://github.com/camillanapoles/github_actions_docs_skill/blob/arena/c91bd6a1-github-actions-docs-skill/skills/github-actions/references/security-hardening.md
---

# Endurecimento de segurança

> Fontes oficiais capturadas:
> `knowledge/pt/actions/reference/security/secure-use.md` ·
> `knowledge/pt/actions/reference/security/oidc.md` ·
> `knowledge/pt/actions/reference/security/secure-use.md` ·
> `knowledge/pt/actions/how-tos/secure-your-work/**`

## 1. Os 8 controles inegociáveis

1. **Menor privilégio em `permissions:`** — declare no topo do workflow e reduza
   por job. Nunca `write-all`. `metadata: read` é implícito.
2. **Segredos fora do shell** — sempre via `env:`; nunca `${{ secrets.X }}`
   interpolado em `run:`.
3. **Inputs não confiáveis fora do shell** — título/corpo de issue, nome de branch,
   mensagem de commit, payload de `repository_dispatch` são **entrada de usuário**.
4. **Pin de actions por SHA** para actions de terceiros (tag maior para as oficiais
   `actions/*`).
5. **`pull_request_target` com gate** e sem executar código do head.
6. **OIDC em vez de chaves de nuvem de longa duração.**
7. **Self-hosted runners nunca em repositório público com `pull_request`**
   (execução de código arbitrário de terceiros).
8. **Ambientes protegidos** para deploy (revisores, branches, wait timer) e
   segredos por ambiente.

## 2. Injeção de script — o ataque nº 1

```yaml
# ❌ VULNERÁVEL: um título de issue como "; rm -rf / #" executa comandos
- run: echo "Processando ${{ github.event.issue.title }}"

# ✅ SEGURO: valor via env, referenciado como variável de shell
- name: Processa
  env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "Processando $TITLE"
```

Fontes não confiáveis mais exploradas:

| Contexto | Campo perigoso |
| --- | --- |
| `github.event.issue` | `title`, `body` |
| `github.event.comment` | `body` |
| `github.event.pull_request` | `title`, `body`, `head.ref`, `head.label` |
| `github.event.review` / `review_comment` | `body` |
| `github.event.head_commit` / `github.event.commits[]` | `message`, `author.email` |
| `github.ref_name` / `github.head_ref` | nome de branch criado por colaborador externo |
| `github.event.client_payload.*` | qualquer campo de `repository_dispatch` |
| `github.event.workflow_run.*` | `head_branch`, `display_title` |

Regra: **nenhum** desses valores entra diretamente em `run:`, `with:` de action
que evalua shell, ou em `gh api -f campo=${{ ... }}`. Passe por `env:` e cite como
`"$VAR"`. Se precisar em JSON, use `jq -n --arg`:

```yaml
- env:
    BODY: ${{ github.event.comment.body }}
  run: |
    jq -n --arg body "$BODY" '{body: $body}' > payload.json
    gh api repos/{owner}/{repo}/issues/${{ github.event.issue.number }}/comments \
      --input payload.json
```

## 3. `pull_request_target` — quando e como

Risco: roda no contexto do repositório **base**, com segredos e token com permissões
do repo, e dispara para PRs de forks.

| Cenário | Decisão |
| --- | --- |
| Só precisa ler/metadados (labels, comentário, checks) | ✅ use, sem checkout do head |
| Precisa rodar testes do código do PR com segredos | ⚠️ exija **label aplicada por maintainer** (`if: contains(github.event.pull_request.labels.*.name, 'safe-to-test')`) ou aprovação prévia |
| Precisa rodar o código do PR sem segredos | ❌ use `pull_request` |
| Deploy de preview com credenciais de nuvem | ⚠️ prefira `workflow_run` após CI verde + ambiente protegido |

Nunca combine: `pull_request_target` + `actions/checkout` do head + `npm ci && npm test`
+ segredos → execução de código arbitrário com credenciais (equivalente a RCE no repo).

## 4. Supply chain: pin e proveniência

```yaml
# ações oficiais do GitHub: tag maior é aceitável
- uses: actions/checkout@v4
- uses: actions/setup-node@v4
- uses: actions/upload-artifact@v4

# terceiros: pin por SHA + comentário de versão (imutável)
- uses: docker/setup-buildx-action@18ce135bb5112fa8ce4ed1d75f8e0d5a6e8f5f1b  # v3.11.1
- uses: aquasecurity/trivy-action@a2d0bc03b8dc9b8f0a84d9c4bc8f30ba3a1a0f7b      # 0.33.1

# dependabot mantém os pins atualizados
```

`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
    groups:
      actions:
        patterns: ["*"]
```

Verificação adicional: `actions/dependency-review-action` em PRs bloqueia
dependências e actions com vulnerabilidade/licença proibida; e
`actions/attest-build-provenance` gera attestation SLSA para artefatos/imagens.

## 5. OIDC — autenticação sem segredo de nuvem

Pré-requisitos: `permissions: id-token: write` + `contents: read`, e uma **trust
policy** no provedor validando `sub` (e `iss`).

```yaml
permissions:
  id-token: write
  contents: read
```

### AWS

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: ${{ vars.AWS_ROLE_ARN }}
    aws-region: ${{ vars.AWS_REGION }}
    role-session-name: gh-actions-${{ github.run_id }}
```

Trust policy (condição recomendada — restrinja por repo, ref e ambiente):

```json
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
  },
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-app:environment:production"
  }
}
```

### Azure

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
```

### Google Cloud

```yaml
- id: auth
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ vars.GCP_WIP }}
    service_account: ${{ vars.GCP_SA }}
```

### Claims e `sub` personalizável

O claim `sub` padrão é `repo:<owner>/<repo>:ref:refs/heads/main` (push),
`repo:<owner>/<repo>:pull_request`, `repo:<owner>/<repo>:environment:<nome>`
(quando há `environment:`), `repo:<owner>/<repo>:job_workflow_ref:...`.
Sempre restrinja a trust policy pelo `sub` mais específico possível — nunca
`repo:org/*` (qualquer repo da org conseguiria assumir o papel).

## 6. Self-hosted runners

- **Nunca** use self-hosted runners em repositórios **públicos** com `pull_request`
  (fork malicioso executa código no seu host persistente).
- Prefira runners **efêmeros** (`--ephemeral`) + labels dedicadas + runner groups.
- Restrinja quem pode registrar runners (org/enterprise runner groups com política).
- Limpe o workspace entre jobs (runner efêmero resolve); não reutilize credenciais
  do host em jobs.
- Para Kubernetes: use **Actions Runner Controller (ARC)** com
  `ScaleSet`/`RunnerScaleSet` e imagens imutáveis
  (`knowledge/pt/actions/concepts/runners/actions-runner-controller.md`).

## 7. Checklist de revisão de segurança (PR de workflow)

- [ ] `permissions:` presente e mínimo (workflow e/ou job)?
- [ ] Algum `${{ }}` com input não confiável dentro de `run:`? → mover para `env:`
- [ ] `pull_request_target` justificado e com gate?
- [ ] Actions de terceiros pinadas por SHA? Dependabot habilitado?
- [ ] Segredos usados apenas em `env:`/`with:`? Nenhum `echo`/URL com segredo?
- [ ] `id-token: write` apenas onde há OIDC? `sub` restrito na trust policy?
- [ ] Deploy passa por `environment:` com revisores?
- [ ] Artefatos/caches não contêm credenciais (`.npmrc`, `.env`, `kubeconfig`)?
- [ ] `timeout-minutes` e `concurrency` definidos (custo + abuso)?
- [ ] Logs não expõem tokens derivados (use `::add-mask::`)?
- [ ] Self-hosted runner (se houver) não recebe PR de fork?
- [ ] Attestations/assinaturas para imagens e artefatos publicados?

## 8. Resposta a incidente

1. Rotacione o segredo exposto imediatamente (`gh secret set ...`).
2. Revogue tokens de nuvem/sessions (AWS: revoke-sessions; Azure: delete
   federated credential; GCP: delete SA key/WIP binding).
3. Cancele runs ativos: `gh run cancel <id>`; desabilite o workflow:
   `gh workflow disable <name>`.
4. Audite: `gh api repos/{owner}/{repo}/actions/runs` + logs de acesso do provedor.
5. Verifique commits/tags maliciosos criados com o token e force-push correções.
6. Habilite push protection/secret scanning e bloqueie workflows não revisados
   (branch protection em `.github/workflows/**`).
