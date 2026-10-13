# Relatório de entrega — branch `arena/c91bd6a1-github-actions-docs-skill`

**Repositório:** `camillanapoles/github_actions_docs_skill`
**Data do relatório:** 2026-10-12
**Tip do branch:** `d3ae4d5` (23 commits, de `0ddafab` em 2026-10-11 17:47 a `d3ae4d5` em 2026-10-11 23:50)
**Estado:** base de conhecimento capturada e íntegra · skill **parcial** · gate de CI implementado e **vermelho** (lista exata do que falta na §9)

---

## 1. Sumário executivo

| Pedido | Estado | Evidência |
| --- | --- | --- |
| 1. Capturar só o *Main Content* de `docs.github.com/pt/actions`, página a página, em Markdown otimizado/impecável | ✅ **feito** | 247/247 páginas, 0 falhas · `.ci/extract-report.md` · `knowledge/pt/**` |
| 2. Organizar em pasta MkDocs **com índice** | ✅ **feito** | `mkdocs.yml` (nav gerado, 639 linhas) · `knowledge/index.md`, `pt/index.md`, `en/index.md`, índices por seção |
| 3. Criar **SKILL** (padrão Agent Skills) com templates completos e válidos de GitHub Actions para CI/CD, GitOps e DevOps + script da skill | ⚠️ **parcial (≈35%)** | `skills/github-actions/SKILL.md` + 7/14 references · **0 templates · 0 scripts** |
| 4. **Mandato de validação** de completude e conformidade | ✅ **mecanismo pronto e rodando**; ❌ **resultado ainda não aprova** | `scripts/validate.py` (8 grupos) → `knowledge/validation.md`, `.ci/validation.json` · **29 ok · 3 avisos · 7 falhas** |
| 5. CI/CD trigger → gate driven | ⚠️ **implementado e já exercido 1×**; reprovado | 3 workflows (§8) · run `38412451552`: pytest/Schema/actionlint/yamllint OK → falhou em `mkdocs build --strict` |

**Pronto para uso hoje:** a base de conhecimento pt-BR (247 páginas, artigo-only, navegável via MkDocs) e o pipeline de captura/validação automatizado.
**Não pronto:** a skill (faltam templates, scripts e 7 references) e a aprovação do gate.

---

## 2. O que foi solicitado (mandato original, sem reinterpretação)

1. Extrair e converter **apenas o "Main Content"** de `https://docs.github.com/pt/actions` — *"converts just the article — skips nav and sidebars"* — página por página / tópico por tópico, garantindo que **todo o conhecimento permaneça facilmente acessível**, em Markdown **otimizado e visualmente impecável**. Referência explícita do usuário: `.../reference/workflows-and-actions/contexts#secrets-context`.
2. Organizar segundo a **convenção MkDocs**: pasta com todo o conhecimento **e índice**.
3. Além da captura, criar uma **SKILL** (padrão Agent Skills: `SKILL.md` + references etc.) que mantenha **templates de uso completos e válidos de GitHub Actions em vários contextos — CI/CD, GitOps, DevOps** — repositório de referência + **script da skill** para "uso impecável".
4. **MANDATO DE VALIDAÇÃO DE COMPLETUDE E CONFORMIDADE COM A SOLICITAÇÃO** — demonstrado, não presumido.

Critérios de aceite implícitos: cobertura completa das páginas pt-BR do site vivo; Markdown só do artigo; árvore MkDocs buildável com índice; `SKILL.md` com references; templates realmente executáveis/validados por contexto; relatório explícito de validação.

---

## 3. O que foi **incrementado** à solicitação (decisões de escopo adicionadas durante a execução)

| # | Incremento | Por que foi necessário |
| --- | --- | --- |
| I-1 | Fonte de captura = **Article API oficial** (`/api/pagelist`, `/api/article`) descoberta no código do `github/docs` (`src/article-api/`) | É exatamente o que o botão "Copiar Markdown" do site usa → **garante artigo-only por construção**, sem raspar nav/sidebar/rodapé |
| I-2 | **Espelho EN** (`knowledge/en`, 247 páginas, source-of-truth `github/docs`) | (a) âncoras oficiais em inglês — os links pt apontam para `#secrets-context`; (b) paridade 1:1 para detectar página faltante |
| I-3 | União de planos de versão (`free-pro-team@latest` + `enterprise-cloud@latest`) | O pagelist por plano não cobre tudo; a união fecha as 247 páginas |
| I-4 | **Camada de polimento** (`polish_markdown`): Liquid resolvido, HTML→pipe tables, alertas `> [!NOTE]`→admonitions `!!! note`, desescape de ruído, reparo de tabelas multi-linha, compactação | "Markdown visualmente impecável" não é opcional: a API devolve dano real em páginas pt |
| I-5 | **Score de qualidade mensurável** (`quality_score`, 7 sinais ponderados) + **auto-cura via HTML** (`heal_with_html`) | Transforma "impecável" em métrica auditável (0 = impecável) e recupera automaticamente páginas danificadas |
| I-6 | **Rate limiting educado** (throttle global, `Retry-After`, 3 passadas de retry) | 56 páginas falhavam com HTTP 429 (Fastly); sem isso a captura nunca fechava 247/247 |
| I-7 | **Suíte de testes offline** do extrator (`tests/test_extract.py`, 9 testes) | Regressões reais encontradas em produção (bs4 4.15/soupsieve 3, heal inseguro) |
| I-8 | **JSON Schemas oficiais vendados** (`.ci/schema/github-workflow.json`, `github-action.json`) | O sandbox não baixa o binário do `actionlint`; schemas permitem validação offline e são a mesma fonte do SchemaStore |
| I-9 | **Validador de 8 grupos** com relatório em Markdown + JSON | Atende o mandato de validação de forma reprodutível e legível por máquina |
| I-10 | **Espelho da skill dentro do site** (`knowledge/skill/**`, 8 páginas) | A skill vira navegável/consultável no MkDocs, não só um diretório solto |
| I-11 | **Gate de CI** (`validate.yml`) e **publicação em Pages** (`docs-publish.yml`) | "Produção" exige pipeline: trigger → verificação bloqueante → deploy |
| I-12 | Diagnóstico auto-publicado pelo CI (`.ci/extract-report.md`, `.ci/extract-log.tail.txt`) | Logs de Actions são inacessíveis do sandbox; o workflow passou a relatar a própria falha via commit |

Nada disso foi pedido pelo usuário; tudo foi necessário para cumprir o pedido.

---

## 4. Stack

| Camada | Tecnologia | Uso |
| --- | --- | --- |
| Captura | Python 3.11/3.12 stdlib (`urllib`, `concurrent.futures`, `re`, `json`) | Article API + pagelist + sitemap/Trees API como fallback |
| Conversão | **pandoc 3.9** via `pypandoc-binary` (writer `gfm-raw_html --wrap=none`), fallback `markdownify` | HTML → GFM de alta fidelidade |
| Parsing HTML | **BeautifulSoup 4.15 + lxml** | tabelas HTML → pipe tables GFM, limpeza de chrome |
| Site | **MkDocs 1.6 + Material for MkDocs 9.5** (`docs_dir: knowledge`, `use_directory_urls`) | navegação, busca, índices, tags |
| Config YAML | **PyYAML** + loader customizado (`_MaterialSafeLoader`) | Material usa tags `!!python/name:` que o `safe_load` rejeita |
| Validação de workflows | **JSON Schema oficial** (SchemaStore) via `check-jsonschema`; **actionlint** (CI); **yamllint** (CI) | conformidade sintática e semântica dos YAML |
| Testes | **pytest** (offline, sem rede) | regressões do extrator |
| CI/CD | **GitHub Actions** (`ubuntu-latest`), `actions/checkout@v4`, `setup-python@v5`, `upload-artifact@v4`, `configure-pages@v5`, `upload-pages-artifact@v3`, `deploy-pages@v4` | captura, gate e publicação |
| CLI GitHub | `gh` (API, runs, secrets) | operação e diagnóstico |

---

## 5. O que foi implementado (mapa do repositório)

```
github_actions_docs_skill/
├── ENTREGA.md                  ← este relatório
├── README.md                   ← ponto de entrada
├── mkdocs.yml                  ← Material; bloco `nav:` GERADO entre marcadores
├── .yamllint                   ← regras para workflows/templates
├── .ci/
│   ├── schema/github-workflow.json (118.601 B) · github-action.json (31.255 B)
│   ├── extract-report.md       ← relatório da última captura (commitado pelo CI)
│   ├── extract-log.tail.txt    ← cauda do log de extração
│   └── validation.json         ← saída legível por máquina do validador
├── .github/workflows/
│   ├── extract-docs.yml        ← CAPTURA (push/dispatch) → commita knowledge/ + .ci/
│   ├── validate.yml            ← GATE (PR/push/dispatch): pytest, schemas, actionlint,
│   │                              yamllint, validate.py --mkdocs, mkdocs build --strict
│   └── docs-publish.yml        ← PRODUÇÃO: build MkDocs → GitHub Pages (environment)
├── knowledge/                  ← docs_dir do MkDocs
│   ├── index.md · tags.md · validation.md · assets/extra.css
│   ├── pt/  (248 .md = 247 capturadas + índice) ← ENTREGA PRINCIPAL
│   ├── en/  (248 .md) ← espelho source-of-truth / âncoras
│   └── skill/ (8 .md) ← espelho navegável da skill
├── scripts/
│   ├── extract.py   (2.108 linhas) captura + polimento + score + cura + relatório
│   ├── build_site.py  (692 linhas) nav, índices, espelho da skill, alinhamento de âncoras
│   ├── validate.py    (810 linhas) 8 grupos de completude/conformidade
│   └── requirements.txt
├── skills/github-actions/
│   ├── SKILL.md                ← contrato da skill (catálogo, 12 inegociáveis, anti-patterns)
│   └── references/ (7/14)      ← contexts, expressions, workflow-syntax, events-and-triggers,
│                                  secrets-and-variables, security-hardening, reusable-workflows
└── tests/test_extract.py (165 linhas, 9 testes)
```

### 5.1 Pipeline de captura (`scripts/extract.py`)

```
discover_pagelist(lang, plan)            GET /api/pagelist/{lang}/{version}  (união de planos)
  └─ fallback: sitemap.xml (filtra aliases legados "-") → Trees API do github/docs
extract_api_page(pathname)               GET /api/article?pathname=...
  ├─ frontmatter: title, description(=intro), product, documentType, lang, plan,
  │               source, captured, section
  ├─ heading_from_link_lines → collapse_escapes → polish_markdown → rewrite_links
  │   → strip_duplicate_title → normalize_markdown
  ├─ quality_score(text) → (score, counts)      # 0 = impecável
  └─ if score > 0: heal_with_html()             # recaptura pelo HTML renderizado,
                                                # só aceita se score menor E ≥60% do conteúdo
relink_tree(root)                              # integridade de links internos
write_report() / write_manifest()              # .ci/extract-report.md, manifest.json
```

Ordem do `polish_markdown`: `octicons_to_text` → `html_regions_to_markdown` (tabelas HTML → pipe tables via BeautifulSoup, `<br>` preservado com `BR_TOKEN`) → `alerts_to_admonitions` → `blockquotes_to_admonitions` → `unescape_noise` → `merge_multiline_cells` → `repair_table_rows` → `compact_tables`.

### 5.2 Validador (`scripts/validate.py`) — 8 grupos

| Grupo | Checagens |
| --- | --- |
| 1 inventário | manifest ↔ disco, capturas com falha, (opcional `--online`) paridade com `/api/pagelist` |
| 2 estrutura | frontmatter obrigatório, H1 único, hierarquia, tamanho mínimo |
| 3 conversão | zero Liquid residual, zero HTML em bloco, cercas balanceadas, tabelas bem formadas, sem ruído de UI, alertas convertidos, `[AUTOTITLE]` resolvido |
| 4 links | internos resolvem, âncoras existem, externos bem formados |
| 5 navegação | `mkdocs.yml` válido (loader Material), nav ↔ arquivos, órfãos, índices obrigatórios |
| 6 skill | frontmatter do `SKILL.md`, paths citados existem, references não vazias, templates YAML parseiam, `on`+`jobs`, `runs-on`/`steps`, `permissions` no topo, `uses:` pinado (tag ou SHA de 40 hex), `action.yml` válido |
| 7 ferramentas | `actionlint`, `yamllint`, `mkdocs build --strict` |
| 8 saída | `knowledge/validation.md` + `.ci/validation.json`, exit code ≠ 0 se houver falha |

---

## 6. Testado

| O quê | Como | Resultado |
| --- | --- | --- |
| Extrator (polimento, score, cura) | `python3 -m pytest tests/ -q` — offline, sem rede | **9 passed** |
| Regressão bs4 4.15 / `decompose()` | `test_clean_fragment_nao_quebra_com_ancestral_decomposto` | passa (antes: `AttributeError` em 3 páginas reais) |
| Cura via HTML aceita/rejeita | `test_heal_with_html_melhora_pagina_danificada`, `test_heal_preserva_versao_melhor_da_api` | passa (score 5 → 0; versão boa preservada) |
| Workflows YAML | `python -m check_jsonschema --schemafile .ci/schema/github-workflow.json` | `ok -- validation done` |
| Compilação | `python -m py_compile scripts/*.py` | ok |
| Captura em produção | CI GitHub Actions (5 corridas, sendo 4 verdes consecutivas) | **247/247, 0 falhas** |
| Geração do site | `python3 scripts/build_site.py` | nav 639 linhas, 4 índices, skill espelhada (8 páginas) |

Bugs reais encontrados pelos testes/CI e **já corrigidos**:

1. `soupsieve 3.0.1` × `bs4 4.15` → `SelectorSyntaxError` em **qualquer** seletor CSS (quebrava a cura via HTML). Trocado por cadeias `(tag, classe)` com `find()` + pin `soupsieve<3`.
2. `AttributeError: 'NoneType' object has no attribute 'get'` em `clean_fragment` (elementos decompostos). Guarda `_alive()`.
3. **Cura insegura**: trocava Markdown bom por HTML minúsculo (score menor ≠ conteúdo melhor). Exigência de ≥60% de volume e de headings.
4. Alertas escapados `\[!NOTE\]` não viravam admonition (regex esperava `]` sem barra).
5. **CI perdia a captura inteira**: `pull --rebase` conflitava e o `push` virava no-op. Job agora parte da ponta do branch (`reset --hard FETCH_HEAD`) + push com retry (`-X theirs`).
6. `mkdocs.yml` inválido por labels de nav com `:` / longos (`yaml.safe_dump` quebrava a linha). `yaml_label()` com aspas e largura infinita.
7. HTTP 429 (Fastly) derrubava 56 páginas → throttle global + `Retry-After` + 3 passadas.
8. Tabelas HTML com células em bloco corrompiam a paridade de cercas no pandoc → caminho BeautifulSoup → pipe table.

---

## 7. Validado (números do mandato)

### 7.1 Captura (`​.ci/extract-report.md`, execução 2026-10-11T23:50:09Z)

| Métrica | Valor |
| --- | --- |
| Páginas OK | **247** |
| Falhas | **0** |
| Páginas com aviso | 16 |
| Bytes totais | 2.505.131 |
| Headings | 2.713 |
| Blocos de código | 1.057 |
| Tabelas | 130 |
| Links internos íntegros | 1.724 (7 revertidos para URL absoluta) |
| Score de qualidade (0 = impecável) | 46 em 3 páginas |
| Seletor de conteúdo principal | `api:/api/article` (100% das páginas) |

### 7.2 Conformidade (`scripts/validate.py --langs pt,en`)

**29 ok · 3 avisos · 7 falhas** → `knowledge/validation.md` + `.ci/validation.json`

Aprovado: inventário EN, zero Liquid residual, zero HTML em bloco, alertas convertidos, estrutura de árvore, nav consistente com arquivos, índices presentes, frontmatter, espelho da skill, `mkdocs.yml` válido.

Reprovado (detalhamento e plano na §9): 8 arquivos com cerca não fechada, 28 linhas de tabela inconsistentes, 2 H1 duplicados, 1 `[AUTOTITLE]`, 278 links internos quebrados (imagens `/assets/**`), 14 páginas abaixo de 400 B, 2 links `http://`, 14 paths citados no `SKILL.md` inexistentes, 0 templates.

---

## 8. CI/CD — trigger → gate driven? (resposta objetiva)

**Hoje: trigger-driven com verificação bloqueante; gate de PR implementado mas ainda não exercido nem obrigatório.**

| Workflow | Trigger | O que faz | Bloqueia? |
| --- | --- | --- | --- |
| `extract-docs.yml` | `push` (paths de captura) + `workflow_dispatch` (`lang`, `limit`, `jobs`, `plan`, `commit`) | captura 247 páginas → reporta (`.ci/extract-report.md`, log) → **commita** `knowledge/` + `.ci/` com `[skip ci]`; `concurrency` serializa; `--max-failures 10` → exit 2 | sim, falha se >10 páginas falharem |
| `validate.yml` (**gate**) | `pull_request` → `main`; `push` → `main`, `arena/**`; `workflow_dispatch` | pytest → JSON Schema oficial → actionlint → yamllint → `validate.py --mkdocs` → `mkdocs build --strict` → resumo + artefato → **`exit 1` se o validador reprovar** | sim (`cancel-in-progress: true`, `timeout-minutes: 25`) |
| `docs-publish.yml` (**produção**) | `push` → `main`; `workflow_dispatch` (`ref`) | valida (bloqueante) → regenera nav/índices → `mkdocs build --strict` → `configure-pages` → `upload-pages-artifact` → **`deploy-pages`** em `environment: github-pages` | sim (`needs: build`, `concurrency: pages`, `cancel-in-progress: false`) |

**Para ser gate-driven de verdade faltam 3 coisas** (nenhuma é código):

1. O `validate.yml` precisa **rodar em um PR** e ficar **verde** (hoje reprova pelas 9 falhas da §7.2).
2. Precisa ser marcado como **required status check** na branch protection de `main` — isso é configuração do GitHub (Settings → Branches) e exige permissão `administration: write`, que o token disponível nesta sessão **não tem** (`gh run cancel` respondeu `HTTP 403: Resource not accessible by integration`).
3. O `docs-publish.yml` só dispara em `main` → depende do **merge** deste branch.

Boas práticas já aplicadas nos três: `permissions` mínimos e explícitos (`contents: read`; `pages: write` + `id-token: write` só no job de deploy), `timeout-minutes` em todos os jobs, `concurrency` com política correta por contexto (cancela validação, **não** cancela deploy), actions oficiais em tag maior, `environment` para publicação, `[skip ci]` no commit de captura para evitar loop, segredos nunca interpolados em `run:`.

---

## 9. Auditoria — o que falta (com severidade e plano)

### P0 — bloqueia o pedido 3 (skill) e o gate

| # | Item | Estado | Ação |
| --- | --- | --- | --- |
| A1 | `skills/github-actions/references/` | **7 de 14** (`runners`, `gitops-patterns`, `troubleshooting`, `migration`, `templates-catalog`, `checklists`, `knowledge-base-map` faltando) | escrever as 7 (fontes já capturadas em `knowledge/pt/**`) |
| A2 | `skills/github-actions/templates/workflows/*.yml` | **0 de 21** prometidos no `SKILL.md` (ci-node, ci-python, ci-go, ci-java, ci-matrix-cache-concurrency, docker-publish, release-please, deploy-pages-mkdocs, deploy-oidc-{aws,azure,gcp}, deploy-environments-approval, gitops-argocd-sync, gitops-flux-image-automation, gitops-kustomize-bump, terraform-plan-apply, security-scanning, reusable-{callee,caller}, actionlint-ci, pr-automation, docs-knowledge-pipeline) | escrever + validar com `check-jsonschema` e `actionlint` |
| A3 | `templates/gitops/*.yaml` (Application, AppProject, Kustomization, ImagePolicy) | **0 de 4** | escrever |
| A4 | `templates/actions/{composite,javascript,docker}/` | **0 de 3** | escrever (`action.yml` validado contra `github-action.json`) |
| A5 | `skills/github-actions/scripts/` (`lint_workflows.sh`, `new_workflow.py`, `validate_skill.py`, `install_tools.sh`) | **0 de 4** | escrever + `bash -n` / `py_compile` |

### P1 — qualidade da base capturada (defeitos reais, causa raiz conhecida)

| # | Item | Ocorrências | Causa raiz | Ação |
| --- | --- | --- | --- | --- |
| B1 | Cercas não fechadas | 8 arquivos (7× `automated-migrations/*` + `workflow-syntax.md` pt + `build-and-test-code/rust.md` en) | fences **indentadas** dentro de listas numeradas (abre com 12 espaços, fecha com 3) → 31 linhas de cerca (ímpar) | `repair_fences()`: reindentar fecho para a abertura; se faltar fecho, inserir antes do próximo heading/lista |
| B2 | H1 duplicado | 2 páginas | cascata de B1 (linhas `# comentário` de YAML fora de cerca) | resolvido por B1 |
| B3 | Tabelas inconsistentes | 28 linhas | cascata de B1 | resolvido por B1 |
| B4 | Links internos quebrados | 278 | imagens `/assets/images/help/**` tratadas como link interno | absolutizar para `https://docs.github.com/assets/**` (ou baixar para `knowledge/assets/images/`) |
| B5 | `[AUTOTITLE]` | 1 (`oidc-in-jfrog.md:25`) | placeholder da API não resolvido | resolver pelo título do destino (manifest) ou humanizar o último segmento |
| B6 | Âncoras sem heading | 920 avisos | `align_anchors` alinhou só **1/496** páginas (27 sem par 1:1 pt↔en) | revisar o pareamento (contagem+nível) e o fallback (slug pt + mapa de âncoras en) |
| B7 | Score de qualidade ≠ 0 | 3 páginas (46 pontos) | cura via HTML falhava (bugs 1–3 da §6, já corrigidos) | **recapturar** e confirmar 0 |

### P2 — conformidade, produção e falso-positivos do validador

| # | Item | Ação |
| --- | --- | --- |
| C1 | 14 páginas `<400 B` são **landing pages** capturadas (`en/**/index.md`, 321–395 B) | recalibrar: threshold 200 B + isentar `documentType: landing` |
| C2 | 2 links `http://man7.org/...` marcados "malformados" | aceitar `http://` e `https://` (rejeitar só `javascript:`/vazio) |
| C3 | `mkdocs build --strict` nunca rodou localmente (mkdocs não instalado no sandbox) | roda no gate `validate.yml`; verificar primeiro run |
| C4 | `README.md` só tem título; faltam `LICENSE` e `NOTICE.md` | escrever README de entrada + MIT para o código + NOTICE com atribuição do conteúdo (documentação GitHub, © GitHub Inc., licenciada CC-BY-4.0 no `github/docs`) |
| C5 | Branch protection / required check | depende de permissão `administration: write` (não disponível nesta sessão) → instrução documentada para o usuário |
| C6 | Nenhum PR aberto a partir do branch | abrir PR para exercitar o gate (decisão do usuário: merge squash/rebase) |
| C7 | `actionlint` e `yamllint` não rodam localmente | já instalados pelo gate no CI |

---

## 10. Como reproduzir localmente

```bash
# dependências (Python 3.11+)
pip install -r scripts/requirements.txt
pip install pytest check-jsonschema yamllint "mkdocs-material>=9.5" "mkdocs>=1.6"

# testes do extrator (offline, sem rede)
python3 -m pytest tests/ -q                       # → 9 passed

# regenera nav, índices e espelho da skill
python3 scripts/build_site.py                     # → mkdocs.yml + knowledge/{index,pt/index,en/index}.md

# mandato de validação (completude + conformidade)
python3 scripts/validate.py --langs pt,en \
  --report knowledge/validation.md --json .ci/validation.json --mkdocs
# → knowledge/validation.md · exit code ≠ 0 se houver falha

# site local
mkdocs serve -a 0.0.0.0:8000

# validação offline de um workflow/template (sem actionlint)
python -m check_jsonschema --schemafile .ci/schema/github-workflow.json \
  .github/workflows/validate.yml

# recaptura (requer acesso a docs.github.com — no sandbox é bloqueado; no CI funciona)
python3 scripts/extract.py --source api --lang pt --scope actions \
  --out knowledge/pt --plan free-pro-team@latest,enterprise-cloud@latest \
  --report .ci/extract-report.md --manifest knowledge/pt/manifest.json
```

---

## 11. Riscos e limitações conhecidas

1. **Conteúdo de terceiros**: a base é derivada da documentação oficial do GitHub. Precisa de `NOTICE.md`/atribuição (C4) antes de redistribuição.
2. **Âncoras**: links pt usam âncoras em inglês; enquanto B6 não fechar, 920 âncoras não resolvem dentro do MkDocs (os links externos para `docs.github.com` continuam corretos).
3. **Volatilidade do sandbox**: o ambiente é re-clonado entre turnos (branch local volta a `0ddafab`, pacotes pip somem). Fonte de verdade = **remote + CI**; nada depende do estado local.
4. **Rate limit do docs.github.com**: captura completa leva ~5 min com throttle; agressividade maior volta a gerar 429.
5. **Sem `administration: write`**: não é possível marcar required checks, cancelar runs ou abrir/mergear PR com merge automático a partir desta sessão sem ação do usuário.
---

## 12. Delta da mesma sessão (correções aplicadas após a primeira auditoria)

Medido depois das correções abaixo (mesmo commit do relatório):

| Defeito (item da §9) | Antes | Depois | O que foi feito |
| --- | --- | --- | --- |
| B1 cercas não fechadas | 8 arquivos | **0** | `repair_fences()` no extrator + `repair_fences_tree()` no build: **332 cercas reparadas em pt, 338 em en** (reindentação de fecho, fecho antes de heading, fecho no EOF) |
| B2 H1 duplicado | 2 páginas | **0** | consequência direta de B1 |
| B4 links internos quebrados | 278 | **1** | `rewrite_asset_links()` no extrator + `normalize_assets()` no build: **277 assets** (`/assets/images/help/**`) absolutizados para `https://docs.github.com` |
| B5 `[AUTOTITLE]` | 1 → 4 (revelados por B1) | **0** | `resolve_autotitle()` usa o título real do destino (frontmatter) ou humaniza o slug (**6 resolvidos**) |
| B6 âncoras | 920 sem heading | **803** | `align_anchors` trocou a paridade 1:1 rígida por alinhamento de sequência de níveis (`difflib`): **893 headings pt com ID explícito**, 60 páginas realinhadas nesta rodada, 0 páginas sem par |
| C1 páginas <400 B | 14 falhas | **0** | mínimo 150 B para `index.md` de seção (landing pages capturadas), 400 B para as demais |
| C2 links `http://` | 2 falhas | **0** | validador aceita `http://` e `https://` (rejeita os demais esquemas) |
| Config do MkDocs | build abortava | build roda | `validation.absolute_links: relative_to_docs` (valor inválido `relative_to_docs_dir`) e plugin `tags` sem a opção deprecated `tags_file` (Material 9.7 usa `listings` + diretiva `<!-- material/tags -->`); `tags.md` entrou no nav |
| Validador (geral) | 27 ok / 9 falhas | **29 ok / 7 falhas** | — |
| `mkdocs build --strict` | 783 avisos → aborta | **677 avisos → aborta** | medição local agora possível (MkDocs instalado no sandbox); ~640 são âncoras (B6), o resto são links absolutos sem `.md` no espelho EN |

**Restam 7 falhas no validador:** 34 linhas de tabela inconsistentes (dano real revelado por B1),
1 link interno quebrado, 14 paths citados no `SKILL.md` (A1), 0 templates (A2–A4) e 0 scripts da
skill (A5) — ou seja, **2 defeitos de conteúdo + 5 itens de entrega da skill**.

**Primeira execução real do gate** (`validate.yml`, run `38412451552`): pytest ✅ · JSON Schema ✅ ·
actionlint ✅ · yamllint ✅ · `validate.py` (continue-on-error, relatório publicado) · 
`mkdocs build --strict` ❌ (677 avisos) → gate **reprovado** e artefato `validation-report` publicado.
O gate funciona como projetado: ele reprova e aponta exatamente o que falta.

---

## 13. Pipeline gate-driven (BPMN-like) — backend OO + SQLite

Pedido adicional: gatilho que verifica **não existência de issues abertas**, **CI/CD sem
erros** e **presença de testes**; enquanto não positivo → **continuidade**, com instrução
por issue pendente e **toda action devolvendo objeto JSON** (`id`, `message`, `addenda`,
`status`, `next_issue`, `direction`).

Contrato, fluxo e medições: [`docs/PIPELINE-GATE-DRIVEN.md`](docs/PIPELINE-GATE-DRIVEN.md).

| Componente | Estado |
| --- | --- |
| `pipeline/` — `domain` (Status 0-4, Envelope, Addendum, NextIssue, GateSpec), `blueprint` (7 gates + gateway), `store` (SQLite: runs/envelopes/addenda/issues), `engine` (7 actions OO + IssueFactory + Orchestrator), `cli` (run/blueprint/state) | ✅ implementado (6 módulos) |
| Gates: `tests` → `capture` → `conformity` → `site` → `skill` → `ci-issues` → `release` | ✅ blueprint auditável em JSON |
| Envelope JSON por action: `status` 0=sucesso · 1=erro de conteúdo (fix) · 2=erro de infra (retry) · 3=pendência (continue) · 4=ignorado | ✅ contrato testado |
| `IssueFactory`: chave determinística `gate:direction:sha1(estado)[:8]`, corpo com instruções + critérios de aceite + próximo gate indexado; idempotente | ✅ testado |
| `.github/workflows/gate-pipeline.yml`: push · PR · **`issues: [closed, labeled, reopened]`** · schedule 6/6h · dispatch; garante **uma** issue por gate (`gate:<id>`, `pipeline:next`, `status:<n>`); exit code = gate | ✅ validado contra o JSON Schema oficial |
| Testes | ✅ **25 passando** (9 extrator + 16 pipeline) |
| Última execução medida | status **1** (fix) · 2/7 gates aprovados · `next_issue: capture:fix:11ecbf57` |

Após recaptura da CI + `build_site.py`: **218 cercas reparadas**, **205/500 páginas com
âncoras alinhadas (2.277 headings com ID oficial)** · validador **29 ok · 3 avisos · 7 falhas**.
