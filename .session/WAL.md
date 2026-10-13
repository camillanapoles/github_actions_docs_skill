# WAL — log append-only de decisões e eventos (M1)

Formato: `timestamp | evento | classe | causa | ação | resultado | sha_commit`
Nunca editar/apagar entrada — correção é entrada nova.

| timestamp | evento | classe | causa | ação | resultado | sha_commit |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-10-11T17:47Z | BOOT | IMPLEMENT | repo vazio (só README) | clone + reconhecimento do escopo | base identificada | 0ddafab |
| 2026-10-11T18:24Z | EXEC | IMPLEMENT | pedido 1: capturar main content pt-BR | `scripts/extract.py` + CI de captura | pipeline de captura criado | 34af55a |
| 2026-10-11T18:26Z | FIX | FIX | `DO_COMMIT` ficava 'no' em push (inputs nulos) | gate por `github.event_name` | CI passou a commitar a base | 7233971 |
| 2026-10-11T18:35Z | EXEC | IMPLEMENT | scraping HTML trazia nav/sidebar | descoberta da Article API oficial (`/api/pagelist`, `/api/article`) | captura artigo-only por construção | e0b78b3 |
| 2026-10-11T18:39Z | VERIFY | IMPLEMENT | cobertura incompleta por plano de versão | união fpt+ghec, fallback sitemap/Trees | 247 páginas pt | 323eca4 |
| 2026-10-11T19:07Z | EXEC | IMPLEMENT | markdown da API com Liquid/alertas/HTML | camada `polish_markdown` | admonitions + pipe tables | ebc10bb |
| 2026-10-11T19:13Z | FIX | FIX | pandoc corrompia paridade de cercas em tabelas HTML | BeautifulSoup → pipe table + `BR_TOKEN` | 0 HTML residual no espelho EN | fadb245 |
| 2026-10-11T19:20Z | FIX | FIX | logs do Actions inacessíveis do sandbox | workflow auto-reportável (`.ci/extract-report.md`, log tail) | diagnóstico via commit | 858da05 |
| 2026-10-11T19:25Z | IMPLEMENT | IMPLEMENT | "impecável" não era mensurável | `quality_score` (7 sinais) + `heal_with_html` + `repair_table_rows` | métrica auditável | 1993464 |
| 2026-10-11T19:26Z | FIX | FIX | HTTP 429 (Fastly) derrubava 56 páginas | throttle global + `Retry-After` + `--passes 3` | robustez de captura | d3ecfc1 |
| 2026-10-11T23:39Z | FIX | FIX | soupsieve 3.0.1 × bs4 4.15 quebrava TODO seletor CSS | `find_chain` (sem CSS) + pin `soupsieve<3` | cura via HTML funcional | 7479058 |
| 2026-10-11T23:40Z | VERIFY | CONTINUE | captura incompleta no tip | recaptura com throttle | **247/247, 0 falhas** | eda67fa |
| 2026-10-11T23:48Z | IMPLEMENT | IMPLEMENT | mandato de validação sem testes | `tests/test_extract.py` (9) + heal seguro + alertas escapados + nav YAML | 9 testes verdes | f79e66d |
| 2026-10-12T00:10Z | IMPLEMENT | IMPLEMENT | pedido: relatório de entrega documentado | `ENTREGA.md` (13 seções), `README.md`, gate `validate.yml`, `docs-publish.yml` | relatório + gate + Pages | dba612a |
| 2026-10-12T01:05Z | FIX | FIX | 8 cercas não fechadas, 278 links, 1 AUTOTITLE, âncoras | `repair_fences`, `rewrite_asset_links`, `resolve_autotitle`, `align_anchors` (difflib) | 29 ok / 7 falhas | ed30dba |
| 2026-10-12T02:20Z | IMPLEMENT | IMPLEMENT | pedido: fluxo gate-driven OO+SQLite com envelopes JSON | `pipeline/` (6 módulos) + `gate-pipeline.yml` + 16 testes | 25 testes; issue #1 criada pela factory | d89398f |
| 2026-10-12T03:10Z | DEBT | DEBT | 403 em rulesets/pages/protection (sem `Administration: write`) | `admin-bootstrap.yml` idempotente + envelope status 3 | débito D5/D6 registrado | 3a4afd5 |
| 2026-10-12T03:40Z | FIX | FIX | envelope jq sem `end` e `$REPO` colado no programa | `--arg repo` + `end`; validado localmente | envelope de 11 chaves OK | 2b651f2 |
| 2026-10-12T04:05Z | FIX | FIX | `bash -e {0}` (default do Actions) abortava no 1º 403 | `set +e` + captura de `rc` + `.ci/admin-bootstrap.log` | passo passou a relatar | 926945e |
| 2026-10-12T04:40Z | FIX | FIX | actionlint vermelho: `${{ inputs.* }}` em push/issues | `github.event.inputs.*` via `env:` | actionlint **success** | 583d19a |
| 2026-10-12T04:55Z | IMPLEMENT | IMPLEMENT | "verde precisa significar verde" | `tests/test_workflows.py` (12) + schema via check-jsonschema | 31 passed, 1 skipped | 0a9d146 |
| 2026-10-12T05:10Z | IMPLEMENT | IMPLEMENT | diagnóstico do actionlint ilegível sem logs | `validate.yml` commita `.ci/actionlint.txt` | auto-relato do gate | 534af49 |
| 2026-10-12T05:40Z | RESUME | CONTINUE | sandbox re-clonado (HEAD→0ddafab, deps perdidas) | `fetch` + `reset --mixed` na linhagem remota | estado reconstruído do repo (A1/A5) | (este commit) |
| 2026-10-12T05:41Z | IMPLEMENT | IMPLEMENT | contrato IGC v1.0 recebido | `.session/{WAL,STATE,INTENT,CONTEXT,DEBT,CHECKPOINT}` + `bootstrap.sh` + `pipeline/igc.py` + testes | memória de sessão versionada | (este commit) |
