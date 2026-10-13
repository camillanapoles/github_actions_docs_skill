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
