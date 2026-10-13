## [gate:capture] Captura completa (inventário pt-BR)

**Gate:** `capture` · **Direção:** `fix` · **Chave determinística:** `capture:fix:faa5f8d5`
**Motivo:** gate 'capture' reprovado (status 1): score de qualidade 46 ≠ 0 (markdown não impecável)

### Instruções (ordem determinística)

1. executar: `scripts/extract.py (relatório em .ci/extract-report.md)`
2. 247/247 páginas pt capturadas, 0 falhas (relatório .ci/extract-report.md)
3. score de qualidade = 0 em todas as páginas (0 = impecável)
4. nenhuma página com aviso de cura via HTML pendente
5. após aprovar, o próximo gate indexado é 'conformity' (Completude e conformidade (mandato de validação))

### Critérios de aceite

- [ ] 247/247 páginas pt capturadas, 0 falhas (relatório .ci/extract-report.md)
- [ ] score de qualidade = 0 em todas as páginas (0 = impecável)
- [ ] nenhuma página com aviso de cura via HTML pendente

### Saída obrigatória (contrato do envelope JSON)

```json
{
  "id": "<gate>:<hash>",
  "gate": "capture",
  "status": 0,
  "message": "<mensagem>",
  "direction": "fix",
  "addenda": [
    {
      "kind": "report",
      "path": "<caminho>"
    }
  ],
  "next_issue": {
    "key": "capture:fix:faa5f8d5",
    "gate": "capture"
  }
}
```

### Estado medido nesta execução

| Gate | Status | Mensagem |
| --- | --- | --- |
| `tests` | 0 (continue) | 25 passed in 0.28s |
| `capture` | 1 (fix) | score de qualidade 46 ≠ 0 (markdown não impecável) |
| `conformity` | 1 (fix) | 7 falha(s) de conformidade |
| `site` | 1 (fix) | Aborted with 677 warnings in strict mode! (677 avisos) |
| `skill` | 3 (continue) | skill incompleta (references: 7, templates: 24, scripts: 4 pendentes) |
| `ci-issues` | 4 (continue) | verificação de CI/issues requer gh + rede (roda no workflow gate-pipeline.yml) |
| `release` | 1 (fix) | produção bloqueada por 'capture': score de qualidade 46 ≠ 0 (markdown não impecável) |

_Gerado por `pipeline.factory` em 2026-10-13T18:16:22+00:00 — blueprint github-actions-docs-skill/gate-driven/1._