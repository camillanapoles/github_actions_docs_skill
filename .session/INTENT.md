# INTENT — objetivo global, escopo e critérios de aceite

## Objetivo
Base de conhecimento pt-BR do GitHub Actions (só o *main content* de
`docs.github.com/pt/actions`) organizada em MkDocs **com índice**, mais uma **skill**
com templates válidos de workflows/actions para CI/CD, GitOps e DevOps — tudo sob
**mandato de validação de completude e conformidade** e operação contínua gate-driven.

## Escopo
- Dentro: captura, polimento/qualidade do Markdown, site MkDocs, skill (references,
  templates, scripts), validador, testes, CI/CD (captura → gate → produção),
  governança (ruleset/Pages) e memória de sessão IGC v1.0.
- Fora: tradução própria de conteúdo, fork da documentação, código de aplicação.

## Critérios de aceite (mensuráveis)
1. 247/247 páginas pt capturadas, 0 falhas, **score de qualidade 0**.
2. `scripts/validate.py` → **0 falhas** nos 8 grupos.
3. `mkdocs build --strict` → **0 avisos**.
4. Skill: 14 references, 24 templates, 4 scripts — todos validados
   (`check-jsonschema` + `actionlint` + `bash -n`/`py_compile`).
5. Gates CI verdes: `tests`, `capture`, `conformity`, `site`, `skill`, `ci-issues`
   → `release = 0` ⇒ Pages publicado.
6. Governança: ruleset `main-gate-driven` ativo + Pages `build_type=workflow`.
7. IGC v1.0: `.session/` íntegro, WAL append-only, CHECKPOINT verificável,
   retomada a frio possível apenas lendo o repositório.

## Contrato operacional
`docs/PIPELINE-GATE-DRIVEN.md` (envelopes JSON, status 0-4, direção) e
`ENTREGA.md` (relatório de entrega + auditoria).

## IGC v2.1 — critérios adicionais (mensuráveis)

8. `.igc-profile.yml` válido (`profile_errors() == []`) e `.igc-registry.yml` com a linhagem
   ativa; divergência registry × CHECKPOINT ⇒ RECON + DEBT (D3), coberto por teste.
9. **M6 — skips justificados:** os 3 skips da suíte são `pandoc indisponível no ambiente`
   (marcador `requer_pandoc`, DEBT **D11**). Nenhum outro skip é aceito sem justificativa
   escrita aqui ou em DEBT.md; `skips_justificados()` reprova motivo desconhecido.
10. **C1-C4:** `gate-pipeline.yml` e `validate.yml` têm o step "Checkpoint IGC"; o commit do
    bot é `[igc-checkpoint]` e não reexecuta pipeline (C2); falha do step reprova o job (C3);
    linhagem sem `.session/` faz bootstrap naquele run (C4).
11. **E4/E5:** mesma chave `(event_id, checkpoint)` é recusada com `status 3`; todo EMIT é
    contraído (`contract_emit`) com a referência do efeito e resolve o débito correspondente.
12. **Art. 12:** fechamento só com nota ≥ 9.5 — abaixo disso a FSM volta a `EXEC`.
