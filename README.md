# GitHub Actions — Base de Conhecimento + Skill

Documentação oficial do **GitHub Actions em pt-BR** capturada página a página
(somente o conteúdo principal do artigo — sem navegação, sidebars, "Neste artigo"
ou rodapé), organizada como site **MkDocs Material**, mais uma **skill** com
templates válidos de workflows e actions para CI/CD, GitOps e DevOps.

> 📋 **Relatório completo de entrega, stack, testes, validação e auditoria do que
> falta:** [`ENTREGA.md`](ENTREGA.md)
> 🔁 **Pipeline gate-driven (BPMN, backend OO + SQLite, envelopes JSON):** [`docs/PIPELINE-GATE-DRIVEN.md`](docs/PIPELINE-GATE-DRIVEN.md)
> ✅ **Relatório de validação (mandato de completude e conformidade):**
> [`knowledge/validation.md`](knowledge/validation.md)

## Estado atual

| Entrega | Status |
| --- | --- |
| Captura pt-BR (`knowledge/pt`) | ✅ **247/247 páginas, 0 falhas** |
| Espelho source-of-truth EN (`knowledge/en`) | ✅ 247 páginas |
| Site MkDocs com índices e nav gerado | ✅ `mkdocs.yml` válido, nav com 639 linhas |
| Validador de completude/conformidade | ✅ 8 grupos · **27 ok · 3 avisos · 9 falhas** |
| Testes offline do extrator | ✅ 9 testes passando |
| Skill (`skills/github-actions`) | ⚠️ `SKILL.md` + 7/14 references · templates e scripts pendentes |
| CI/CD (captura → gate → publicação) | ⚠️ 3 workflows prontos; gate vermelho até fechar as 9 falhas |

## Uso rápido

```bash
# 1. dependências
pip install -r scripts/requirements.txt
pip install pytest check-jsonschema "mkdocs-material>=9.5"

# 2. site local (busca, nav, índices)
mkdocs serve -a 0.0.0.0:8000

# 3. mandato de validação
python3 scripts/validate.py --langs pt,en \
  --report knowledge/validation.md --json .ci/validation.json --mkdocs

# 4. testes do extrator
python3 -m pytest tests/ -q

# 5. regenerar nav/índices/espelho da skill
python3 scripts/build_site.py
```

## Estrutura

```
knowledge/           docs_dir do MkDocs
├── index.md         índice geral
├── pt/              247 páginas capturadas de docs.github.com/pt/actions  ← entrega principal
├── en/              espelho source-of-truth (github/docs) — âncoras oficiais
├── skill/           espelho navegável da skill
├── validation.md    relatório do mandato de validação
└── tags.md · assets/extra.css

scripts/
├── extract.py       captura (Article API) + polimento + score de qualidade + auto-cura
├── build_site.py    gera nav, índices e espelho da skill; alinha âncoras pt↔en
└── validate.py      8 grupos de completude/conformidade → validation.md + .ci/validation.json

skills/github-actions/
├── SKILL.md         contrato da skill: catálogo, 12 inegociáveis, anti-patterns
├── references/      conhecimento destilado (contextos, expressões, sintaxe, segurança…)
├── templates/       workflows/actions prontos por contexto (CI/CD, GitOps, DevOps)
└── scripts/         utilitários de validação e scaffolding

.github/workflows/
├── extract-docs.yml captura automatizada → commita knowledge/ (relatório incluso)
├── validate.yml     GATE: pytest · JSON Schema · actionlint · yamllint · validate.py · mkdocs --strict
└── docs-publish.yml PRODUÇÃO: build MkDocs → GitHub Pages

tests/               suíte offline do extrator (pytest)
.ci/schema/          JSON Schemas oficiais vendados (validação sem rede)
```

## Pipeline (trigger → gate → produção)

```
push / workflow_dispatch
   └─► extract-docs.yml ── captura 247 páginas ──► commit knowledge/ + .ci/extract-report.md
pull_request / push
   └─► validate.yml ────── pytest + schemas + actionlint + validate.py + mkdocs --strict
                            └─► exit 1 se houver falha  (GATE)
push em main
   └─► docs-publish.yml ── valida ──► mkdocs build --strict ──► GitHub Pages
```

## Fontes e atribuição

- Conteúdo: [docs.github.com/pt/actions](https://docs.github.com/pt/actions), capturado pela
  **Article API oficial** (`/api/pagelist`, `/api/article`) — a mesma usada pelo botão
  "Copiar Markdown" do site.
- Espelho/âncoras: [github/docs](https://github.com/github/docs).
- A documentação do GitHub é © GitHub, Inc. e distribuída sob
  [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/); este repositório é um
  derivado para estudo/consulta e mantém a atribuição. Código próprio (scripts,
  workflows, skill): MIT — veja `NOTICE.md`.
