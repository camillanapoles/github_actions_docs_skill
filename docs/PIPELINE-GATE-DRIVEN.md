# Pipeline gate-driven (BPMN-like) — contrato, fluxo e continuidade

Backend **orientado a objetos + SQLite** (`pipeline/`) que orquestra os gates do
repositório e garante a regra de continuidade pedida:

> enquanto houver **issue aberta**, **CI/CD com erro** ou **ausência de testes**,
> o fluxo **não** está concluído — cada execução devolve o erro **e** a instrução
> da próxima issue indexada.

## 1. Contrato do envelope JSON (toda action devolve)

```json
{
  "id": "capture:9f2ab31c0d",
  "blueprint": "gate-driven-bpmn/1",
  "gate": "capture",
  "action": "scripts/extract.py (relatório em .ci/extract-report.md)",
  "status": 1,
  "status_label": "error_content",
  "message": "score de qualidade 46 ≠ 0 (markdown não impecável)",
  "direction": "fix",
  "addenda": [
    { "kind": "report", "path": ".ci/extract-report.md" },
    { "kind": "json",   "path": ".ci/validation.json", "note": "opcional" }
  ],
  "next_issue": {
    "key": "capture:fix:11ecbf57",
    "title": "[gate:capture] Captura completa (inventário pt-BR)",
    "gate": "capture",
    "direction": "fix",
    "reason": "gate 'capture' reprovado (status 1): score de qualidade 46 ≠ 0",
    "instructions": ["executar: `...`", "...", "após aprovar, o próximo gate indexado é 'conformity'"],
    "acceptance": ["247/247 páginas pt capturadas, 0 falhas", "score de qualidade = 0"]
  },
  "metrics": { "pages_ok": 247, "pages_failed": 0, "quality_score": 46 },
  "started_at": "2026-10-12T01:14:03+00:00",
  "finished_at": "2026-10-12T01:14:04+00:00",
  "duration_s": 0.842
}
```

### Códigos de status (`Status`, `pipeline/domain.py`)

| Código | Nome | Significado | `direction` |
| --- | --- | --- | --- |
| **0** | `SUCCESS` | gate aprovado, testes determinísticos verdes | `continue` (próxima issue indexada) |
| **1** | `ERROR_CONTENT` | erro tipo 1: conteúdo/qualidade/conformidade | `fix` (mesma issue/gate) |
| **2** | `ERROR_INFRA` | erro tipo 2: ambiente/rede/ferramenta ausente/timeout | `retry` |
| **3** | `PENDING` | entrega incompleta (escopo pendente, ex.: skill) | `continue` |
| **4** | `SKIPPED` | gate não aplicável neste contexto (ex.: `gh` offline) | `continue` |

Exit code do processo: **0** se todos os gates obrigatórios estão em 0/4; **1** caso
contrário (é isso que torna o workflow um *gate*).

## 2. Blueprint (nós e transições)

`python3 -m pipeline.cli blueprint` → JSON auditável (`.ci/blueprint.json`):

```
tests ──0──► capture ──0──► conformity ──0──► site ──0──► skill ──0──► ci-issues ──0──► release ──0──► END
  │1            │1              │1              │1           │3            │3              │1
  └─► issue:tests  └─► issue:capture  └─► issue:conformity  └─► issue:site └─► issue:skill └─► issue:ci-issues └─► issue:release
```

| # | Gate | Action (determinística) | Critério de aceite |
| --- | --- | --- | --- |
| 10 | `tests` | `python3 -m pytest tests/ -q` | 100% verde; defeito novo vira teste de regressão antes do fix |
| 20 | `capture` | `.ci/extract-report.md` + inventário `knowledge/{pt,en}` | 247/247 pt, 0 falhas, **score de qualidade 0** |
| 30 | `conformity` | `scripts/validate.py --langs pt,en --report ... --json ...` | 0 falhas nos 8 grupos |
| 40 | `site` | `python3 -m mkdocs build --strict` | 0 avisos (âncoras, links, nav, órfãos) |
| 50 | `skill` | inventário `SKILL.md` × disco (references/templates/scripts) | 14 references, 24 templates, 4 scripts entregues e válidos |
| 60 | `ci-issues` | `gh run list` + `gh issue list` (online) | nenhuma corrida `failure`, nenhuma issue `gate:*` aberta |
| 90 | `release` | **gateway exclusivo** (agrega os anteriores) | todos em 0 → produção; senão devolve erro + continuidade |

## 3. Componentes (OOM)

| Módulo | Responsabilidade |
| --- | --- |
| `pipeline/domain.py` | `Status` (IntEnum), `Addendum`, `NextIssue`, `Envelope`, `GateSpec` — o contrato |
| `pipeline/blueprint.py` | `GATES`, `ordered()`, `after(gate)`, `as_bpmn_dict()` — o fluxo |
| `pipeline/store.py` | `PipelineStore` (Repository SQLite): `runs`, `envelopes`, `addenda`, `issues` |
| `pipeline/engine.py` | `Action` (base: mede tempo, exceção → status 2) + `TestsAction`, `CaptureAction`, `ConformityAction`, `SiteAction`, `SkillAction`, `CiIssuesAction`, `ReleaseGateway`; `IssueFactory`; `Orchestrator` |
| `pipeline/cli.py` | `run` / `blueprint` / `state` — saída JSON ou NDJSON (`--envelopes`) |
| `tests/test_pipeline.py` | 16 testes: contrato, códigos, store, blueprint, fábrica (determinismo/idempotência/roteamento), actions, orquestrador |

## 4. Continuidade (o que o gatilho garante)

1. **Executa** os gates em ordem e persiste cada envelope no SQLite.
2. **Agrega** no gateway `release`: primeiro gate não-aprovado define `status`,
   `direction` e a **chave determinística** da próxima issue
   (`gate:direction:sha1(estado)[:8]`).
3. **Publica** a instrução completa em `.ci/next-issue.md` (contexto, comandos,
   critérios de aceite, envelope esperado, estado medido).
4. **Garante uma única issue aberta por gate** (idempotente): se já existe issue
   com o rótulo `gate:<id>`, comenta a instrução atualizada; senão cria com os
   rótulos `gate:<id>`, `pipeline:next`, `status:<n>`.
5. **Event-driven**: `issues: [closed, labeled, reopened]` → ao fechar uma issue o
   fluxo re-executa e **constrói a seguinte indexada**; com tudo em 0, fecha as
   issues `pipeline:next` remanescentes e libera `docs-publish.yml` (produção).

## 5. Como executar

```bash
python3 -m pipeline.cli run                     # todos os gates → .ci/pipeline-state.json
python3 -m pipeline.cli run --gate skill        # gate único
python3 -m pipeline.cli run --online            # consulta gh (runs/issues) — usado no CI
python3 -m pipeline.cli run --envelopes         # NDJSON: 1 envelope por linha
python3 -m pipeline.cli blueprint               # fluxo BPMN em JSON
python3 -m pipeline.cli state                   # estado acumulado no SQLite
```

## 6. Última execução medida (estado real)

```
status 1 (error_content) · direção fix · 2/7 gates aprovados
  tests        0 continue  25 passed in 0.34s
  capture      1 fix       score de qualidade 46 ≠ 0 (markdown não impecável)
  conformity   1 fix       7 falha(s) de conformidade
  site         1 fix       Aborted with 677 warnings in strict mode!
  skill        3 continue  skill incompleta (references: 7, templates: 24, scripts: 4 pendentes)
  ci-issues    4 continue  requer gh + rede (roda no workflow gate-pipeline.yml)
  release      1 fix       produção bloqueada por 'capture'
next_issue: capture:fix:11ecbf57 — [gate:capture] Captura completa (inventário pt-BR)
```

Interpretação: o fluxo **não** está concluído e diz exatamente por onde continuar
(`capture` → `conformity` → `site` → `skill`), com a instrução da próxima issue gerada.

## 7. Workflows associados

| Workflow | Papel |
| --- | --- |
| `gate-pipeline.yml` | orquestra os gates, publica envelopes, garante a próxima issue (trigger: push, PR, `issues`, schedule 6/6h, dispatch) |
| `validate.yml` | gate de conformidade "clássico" (pytest, JSON Schema, actionlint, yamllint, `validate.py`, `mkdocs --strict`) |
| `extract-docs.yml` | captura da documentação → commit de `knowledge/` (alimenta o gate `capture`) |
| `docs-publish.yml` | produção: build MkDocs → GitHub Pages (só faz sentido com `release` em 0) |
