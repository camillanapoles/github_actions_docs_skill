---
title: GitHub Actions — Base de Conhecimento & Skill
description: Documentação oficial do GitHub Actions capturada página a página (pt-BR)
  + skill com templates validados de CI/CD, GitOps e DevOps.
generated: true
---

# GitHub Actions — Base de Conhecimento & Skill

Repositório de referência construído em três camadas:

| Camada | O que é | Onde está |
| --- | --- | --- |
| **Captura** | Conteúdo principal de cada página de `docs.github.com/pt/actions` (sem nav/sidebar), página a página | `knowledge/pt/` |
| **Espelho** | Source-of-truth `github/docs` convertido (Liquid resolvido) para comparação/auditoria | `knowledge/en/` |
| **Skill** | `SKILL.md` + referências + templates de workflows/actions validados em CI | `skills/github-actions/` |

> **494 páginas** · 4,766,213 bytes · atualizado em 2026-10-11

## Comece por aqui

- [Português (pt-BR)](pt/index.md) — 247 páginas (fonte `api`, plano `free-pro-team@latest,enterprise-cloud@latest`)
- [English (source-of-truth)](en/index.md) — 247 páginas (fonte `repo`, plano `free-pro-team@latest`)
- [Skill: SKILL.md](skill/index.md) — como usar este repositório como skill de agente
- [Catálogo de templates](skill/templates.md) — workflows prontos por contexto (CI/CD, GitOps, DevOps, segurança)
- [Validação e conformidade](validation.md) — resultado automatizado dos checadores

## Páginas mais consultadas

- [Referência de contextos](pt/actions/reference/workflows-and-actions/contexts.md) — `github`, `secrets`, `vars`, `needs`, `matrix`…
- [Sintaxe de fluxo de trabalho](pt/actions/reference/workflows-and-actions/workflow-syntax.md)
- [Expressões](pt/actions/reference/workflows-and-actions/expressions.md)
- [Variáveis](pt/actions/reference/workflows-and-actions/variables.md) · [Usar segredos](pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
- [Eventos que disparam fluxos de trabalho](pt/actions/reference/workflows-and-actions/events-that-trigger-workflows.md)
- [Reutilizar fluxos de trabalho](pt/actions/how-tos/reuse-automations/reuse-workflows.md)
- [Segurança: hardening](pt/actions/reference/security/security-hardening-for-github-actions.md) · [OIDC](pt/actions/reference/security/oidc.md)

## Como reproduzir

```bash
# 1) capturar (requer acesso a docs.github.com — em CI roda automaticamente)
python3 scripts/extract.py --source api --lang pt --out knowledge/pt \
  --plan free-pro-team@latest,enterprise-cloud@latest

# 2) gerar nav + índices do MkDocs
python3 scripts/build_site.py

# 3) validar completude/conformidade
python3 scripts/validate.py --report VALIDATION.md

# 4) servir localmente
mkdocs serve -a 0.0.0.0:8000
```
