# CONTEXT — mapa de reconstrução (M3)

## Linhagem
- Branch da sessão: `arena/c91bd6a1-github-actions-docs-skill` (**fixa por contrato do
  runtime** — esta sessão não cria/empurra outras branches; equivale a `sessao/<id>/<slug>`).
- Base: `main` em `0ddafab` (Initial commit).
- Worktrees: convenção IGC `git worktree add ../wt-<sessao> -b sessao/<id>/<slug> <sha-verificado>`;
  neste runtime o worktree é o próprio checkout `/home/user/github_actions_docs_skill`.
  Sem submódulos no repo (W5 não se aplica).

## Bootstrap do ambiente (O(bootstrap), não O(adivinhação))
```bash
bash .session/bootstrap.sh          # instala deps, valida toolchain, roda smoke de testes
pip install --break-system-packages -r scripts/requirements.txt   # sandbox PEP 668
pip install --break-system-packages pytest check-jsonschema yamllint "mkdocs>=1.6" "mkdocs-material>=9.5"
```
Toolchain: Python 3.11/3.12, pandoc 3.9 (via `pypandoc-binary`), bs4+lxml, PyYAML,
pytest, jq, git, `gh` (autenticado), actionlint (só no CI: download bloqueado no sandbox).

## Arquivos-chave
| Caminho | Papel |
| --- | --- |
| `scripts/extract.py` | captura (Article API) + polish + `quality_score` + `heal_with_html` + `repair_fences` |
| `scripts/build_site.py` | nav/índices, espelho da skill, `normalize_assets`, `resolve_autotitle`, `align_anchors` (difflib) |
| `scripts/validate.py` | 8 grupos de completude/conformidade → `knowledge/validation.md`, `.ci/validation.json` |
| `pipeline/` | orquestrador gate-driven OO + SQLite (`domain`, `blueprint`, `store`, `engine`, `cli`, `igc`) |
| `tests/` | `test_extract.py` (9), `test_pipeline.py` (16), `test_workflows.py` (12), `test_igc.py` |
| `knowledge/{pt,en}` | 247 páginas cada; `knowledge/skill` = espelho navegável |
| `.github/workflows/` | `extract-docs`, `validate` (gate), `gate-pipeline` (orquestrador), `docs-publish` (Pages), `admin-bootstrap` (governança) |
| `.ci/` | diagnósticos commitados: `extract-report.md`, `validation.json`, `pipeline-state.json`, `next-issue.md`, `actionlint.txt`, `admin-bootstrap.log` |

## Invariantes do projeto
1. Nenhuma emissão ao GitHub sem commit anterior (A3) e sem rótulo de evento (A4).
2. Toda action devolve envelope JSON: `id, gate, status(0-4), message, direction,
   addenda, next_issue, metrics`.
3. Diagnóstico de CI é **commitado** em `.ci/` (logs do Actions são inacessíveis do sandbox).
4. `knowledge/**` é gerado: nunca editar à mão — regenerar via `extract.py`/`build_site.py`.
5. `mkdocs.yml` tem bloco `nav:` gerado entre marcadores `# BEGIN/END GENERATED NAV`.
6. Segredos nunca interpolados em `run:`; `inputs.*` só via `env:` + `github.event.inputs.*`.
7. Gates vermelhos são informação, não ruído: cada reprovação gera a próxima issue indexada.

## IGC v2.1 — linhagem, território e desvios declarados (A2'/W1'/Art. 12)

- **Contrato vigente:** IGC **v2.1** (substitui v1.0/v1.1/v2.0). Profile: `.igc-profile.yml`.
  Descoberta: `.igc-registry.yml` (Art. 7). Envelope mínimo: `status` + `message` +
  `checkpoint_ref` (E3, schema em `.ci/schema/envelope.schema.json`).
- **Linhagem (A2'):** este runtime **proíbe** criar/empurrar `sessao/<id>/<slug>`; a branch
  `arena/c91bd6a1-github-actions-docs-skill` foi **designada** como linhagem desta sessão e
  está registrada no `.igc-registry.yml` (slug `github-actions-docs-skill`, `ativa: true`).
- **Base (W1'/M7):** SHA-pinada `0ddafab815385d69ea8f70d93c3479daa7f50175`. Sanidade de base
  medida: `git diff --stat 0ddafab..origin/main` **vazio** (upstream = 1 commit, sem revert)
  → PASS, nenhuma anomalia do tipo EV-1.
- **Território (W1/W3/W4):** worktree único do runtime; nada de estado fora do repo; hooks e
  validações rodam como **gates de pipeline** (`validate`, `gate-pipeline`) porque o runtime
  não expõe `core.hooksPath` persistente — invariante preservado: nenhuma mutação entra sem check.
- **Protocolo de isolamento para runtime futuro (quando permitir branch própria):**
  `git worktree add ../<wt> -b sessao/<id>/<slug> 0ddafab815385d69ea8f70d93c3479daa7f50175`
  → `./.session/bootstrap.sh` → `.session/ci_checkpoint.py` a cada run (C1) → `git worktree prune`
  ao fechar (W6). Sem rsync: transporte por `git bundle` (W7/T8).
- **Desvios de convenção (obrigação do Art. 12):**
  - **DEV-1** — A2'/D1: o registry vive na linhagem e só chega ao *default branch* no merge
    (gate `release`), porque o runtime proíbe push em `main`. R1 usa o registry da linhagem.
  - **DEV-2** — C1: a persistência do bot no CI usa `GITHUB_TOKEN` (`contents: write`) na
    própria branch, não `ADMIN_TOKEN`; commits `[igc-checkpoint]` filtrados por `paths-ignore`
    (gate-pipeline) e por allowlist de `paths` (validate) para não reexecutar o pipeline (C2).
  - **DEV-3** — nomenclatura de branch `arena/*` em vez de `sessao/<id>/<slug>` (EV-6):
    declarado aqui, no profile e no registry.


## Ordem do ciclo (invariante M4 operacional)

`WAL appends → registry (D2) → write_checkpoint → medir (pytest, só leitura) →
closing_gate → contract_emit → commit → push`. `closing_gate` e `contract_emit`
acrescentam entradas ao WAL e por isso chamam `_refaz_checkpoint()`: nenhum append
fica depois do CHECKPOINT. `wal_append` permanece puro — é isso que permite a
`verify()` detectar adulteração (M4/T4).
