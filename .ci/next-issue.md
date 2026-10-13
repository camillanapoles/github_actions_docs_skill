## [gate:site] Site MkDocs buildável em modo estrito

**Gate:** `site` · **Direção:** `retry` · **Chave determinística:** `site:retry:55ae7573`
**Motivo:** gate 'site' reprovado (status 2): site: error_infra

### Instruções (ordem determinística)

1. executar: `python3 -m mkdocs build --strict --site-dir site`
2. mkdocs build --strict → 0 avisos (âncoras, links, nav, arquivos órfãos)
3. nav gerado por scripts/build_site.py cobre 100% das páginas
4. após aprovar, o próximo gate indexado é 'skill' (Skill completa (references, templates, scripts))

### Critérios de aceite

- [ ] mkdocs build --strict → 0 avisos (âncoras, links, nav, arquivos órfãos)
- [ ] nav gerado por scripts/build_site.py cobre 100% das páginas

### Saída obrigatória (contrato do envelope JSON)

```json
{
  "id": "<gate>:<hash>",
  "gate": "site",
  "status": 0,
  "message": "<mensagem>",
  "direction": "retry",
  "addenda": [
    {
      "kind": "report",
      "path": "<caminho>"
    }
  ],
  "next_issue": {
    "key": "site:retry:55ae7573",
    "gate": "site"
  }
}
```

### Estado medido nesta execução

| Gate | Status | Mensagem |
| --- | --- | --- |
| `tests` | 0 (continue) | tests: success |
| `capture` | 0 (continue) | capture: success |
| `conformity` | 0 (continue) | conformity: success |
| `site` | 2 (retry) | site: error_infra |
| `skill` | 0 (continue) | skill: success |
| `ci-issues` | 0 (continue) | ci-issues: success |
| `release` | 2 (retry) | produção bloqueada por 'site': site: error_infra |

_Gerado por `pipeline.factory` em 2026-10-13T23:54:05+00:00 — blueprint github-actions-docs-skill/gate-driven/1._