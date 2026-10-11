#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_site.py — Gera a estrutura MkDocs da base de conhecimento.

Responsabilidades:
  1. Lê os manifestos (`knowledge/<lang>/manifest.json`) e a árvore de `.md`;
  2. Reconstrói a ordem oficial da sidebar a partir do frontmatter `children`
     do espelho inglês (source-of-truth do github/docs) — fallback: alfabética;
  3. Gera páginas índice (raiz, por idioma e por seção) com título + descrição;
  4. Sincroniza a documentação da skill (SKILL.md, references, templates) em
     `knowledge/skill/**` para que tudo seja navegável no mesmo site;
  5. Reescreve o bloco `nav:` do `mkdocs.yml` entre os marcadores
     `# BEGIN GENERATED NAV` / `# END GENERATED NAV`.

Uso:
  python3 scripts/build_site.py                 # usa knowledge/ e mkdocs.yml do repositório
  python3 scripts/build_site.py --dry-run       # mostra o nav sem gravar
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML é obrigatório: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"
SKILL_DIR = ROOT / "skills" / "github-actions"
MKDOCS_YML = ROOT / "mkdocs.yml"
NAV_BEGIN = "# BEGIN GENERATED NAV"
NAV_END = "# END GENERATED NAV"
REPO_URL = "https://github.com/camillanapoles/github_actions_docs_skill"
BRANCH = "arena/c91bd6a1-github-actions-docs-skill"

LANG_LABELS = {"pt": "Português (pt-BR)", "en": "English (source-of-truth)"}
SECTION_LABELS = {
    "actions": "GitHub Actions",
    "get-started": "Introdução",
    "concepts": "Conceitos",
    "how-tos": "How-tos",
    "reference": "Referência",
    "tutorials": "Tutoriais",
    "skill": "Skill",
}


# --------------------------------------------------------------------------- #
# Leitura de páginas
# --------------------------------------------------------------------------- #

def read_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"title": path.stem.replace("-", " ").capitalize(), "body_preview": ""}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"title": path.stem}
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        fm = {}
    body = parts[2].lstrip()
    fm.setdefault("title", path.stem.replace("-", " ").capitalize())
    fm["body_preview"] = body[:400]
    return fm


def load_tree(lang_root: Path) -> dict[str, dict[str, Any]]:
    """{caminho relativo sem extensão: {file, fm, children}}"""
    pages: dict[str, dict[str, Any]] = {}
    for md in sorted(lang_root.rglob("*.md")):
        rel = md.relative_to(lang_root).with_suffix("").as_posix()
        fm = read_front_matter(md)
        pages[rel] = {"file": md, "rel": rel, "fm": fm}
    return pages


def load_manifest(lang_root: Path) -> dict[str, Any]:
    path = lang_root / "manifest.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[warn] manifesto inválido em {path}: {exc}", file=sys.stderr)
        return {}


# --------------------------------------------------------------------------- #
# Ordem oficial (children do source-of-truth)
# --------------------------------------------------------------------------- #

def build_order_map(en_root: Path) -> dict[str, list[str]]:
    """Mapa `página pai` → `[páginas filhas]` na ordem oficial da sidebar."""
    order: dict[str, list[str]] = {}
    manifest = load_manifest(en_root)
    entries = manifest.get("pages", []) if manifest else []
    known: set[str] = set()
    for md in en_root.rglob("*.md"):
        rel = md.relative_to(en_root).with_suffix("").as_posix()
        known.add(rel)
        if rel.endswith("/index"):
            known.add(rel[: -len("/index")])
    for entry in entries:
        children = entry.get("children") or []
        if not children:
            continue
        parent_rel = re.sub(r"\.md$", "", entry.get("path", ""))
        parent_rel = re.sub(r"^actions/", "", parent_rel)
        parent_dir = str(Path(parent_rel).parent)
        resolved: list[str] = []
        for child in children:
            child = str(child).strip()
            if not child:
                continue
            candidates = []
            if child.startswith("/actions/"):
                base = child[len("/actions/"):]
            elif child.startswith("/"):
                base = f"{parent_dir}/{child[1:]}" if parent_dir not in (".", "") else child[1:]
            else:
                base = f"{parent_dir}/{child}" if parent_dir not in (".", "") else child
            base = re.sub(r"^\./", "", base).strip("/")
            candidates += [base, f"{base}/index", re.sub(r"/index$", "", base)]
            for cand in candidates:
                if cand in known:
                    key = re.sub(r"/index$", "", cand)
                    if key not in resolved:
                        resolved.append(key)
                    break
        if resolved:
            order[re.sub(r"/index$", "", parent_rel)] = resolved
    return order


# --------------------------------------------------------------------------- #
# Árvore de navegação
# --------------------------------------------------------------------------- #

class Node:
    def __init__(self, name: str, rel: str = ""):
        self.name = name
        self.dir_key = ""
        self.rel = rel            # caminho da página (sem .md) quando é folha/índice
        self.children: list[Node] = []

def build_tree(pages: dict[str, dict[str, Any]], lang_root: Path, order_map: dict[str, list[str]]) -> Node:
    """Monta a árvore de navegação a partir dos caminhos de arquivo."""
    root = Node("root")
    root.dir_key = ""
    index_map: dict[str, Node] = {"": root}

    def ensure_dir(parts: tuple[str, ...]) -> Node:
        cur = root
        acc = ""
        for part in parts:
            acc = f"{acc}/{part}" if acc else part
            if acc not in index_map:
                node = Node(SECTION_LABELS.get(part, part.replace("-", " ").capitalize()), acc)
                node.dir_key = acc
                cur.children.append(node)
                index_map[acc] = node
            cur = index_map[acc]
        return cur

    for rel, info in sorted(pages.items()):
        parts = rel.split("/")
        leaf_name = parts[-1]
        parent = ensure_dir(tuple(parts[:-1]))
        if leaf_name == "index":
            parent.rel = rel
            parent.fm = info["fm"]
            parent.dir_key = parent.dir_key or str(Path(rel).parent)
            continue
        node = Node(str(info["fm"].get("title") or leaf_name.replace("-", " ").capitalize()), rel)
        node.fm = info["fm"]
        node.dir_key = rel
        parent.children.append(node)

    # página-irmã (ex.: `actions/concepts.md` + diretório `actions/concepts/`) vira índice da seção
    for key, node in list(index_map.items()):
        if not key or node.rel or key not in pages:
            continue
        node.rel = key
        node.fm = pages[key]["fm"]
        parent_key = str(Path(key).parent)
        parent_key = "" if parent_key == "." else parent_key
        parent = index_map.get(parent_key)
        if parent is not None:
            parent.children = [c for c in parent.children if c.rel != key]

    apply_order(root, order_map)
    prune_empty(root)
    return root


def apply_order(node: Node, order_map: dict[str, list[str]]) -> None:
    order = order_map.get(node.rel or node.name.lower(), [])
    if not order and node.rel:
        order = order_map.get(re.sub(r"/index$", "", node.rel), [])
    if order:
        rank = {key: i for i, key in enumerate(order)}
        node.children.sort(key=lambda n: (rank.get(re.sub(r"/index$", "", n.rel or ""), 10_000),
                                          rank.get(n.name.lower(), 10_000), n.name.lower()))
    for child in node.children:
        apply_order(child, order_map)


def prune_empty(node: Node) -> None:
    node.children = [c for c in node.children if c.rel or c.children]
    for child in node.children:
        prune_empty(child)


# --------------------------------------------------------------------------- #
# Emissão do nav YAML
# --------------------------------------------------------------------------- #

def nav_yaml(node: Node, lang_prefix: str, indent: int = 0) -> list[str]:
    lines: list[str] = []
    pad = "  " * indent
    for child in node.children:
        label = yaml.safe_dump(str(child.name), allow_unicode=True, default_style=None).strip()
        if child.children:
            lines.append(f"{pad}- {label}:")
            if child.rel:
                lines.append(f"{pad}  - Visão geral: {lang_prefix}{child.rel}.md")
            lines += nav_yaml(child, lang_prefix, indent + 1)
        elif child.rel:
            lines.append(f"{pad}- {label}: {lang_prefix}{child.rel}.md")
    return lines


# --------------------------------------------------------------------------- #
# Páginas índice geradas
# --------------------------------------------------------------------------- #

def write_section_indexes(node: Node, lang_root: Path, lang: str, pages: dict[str, dict[str, Any]]) -> list[str]:
    """Gera `index.md` para diretórios sem página-índice. Retorna os caminhos criados."""
    created: list[str] = []
    for child in node.children:
        if child.children and not child.rel:
            dir_key = getattr(child, "dir_key", "")
            if not dir_key:
                first = next((c.rel for c in child.children if c.rel), None)
                dir_key = str(Path(first).parent) if first else ""
            idx_rel = f"{dir_key}/index.md" if dir_key else None
            if idx_rel:
                dest = lang_root / idx_rel
                if not dest.exists():
                    rows = []
                    for c in child.children:
                        if not c.rel:
                            continue
                        fm = pages.get(c.rel, {}).get("fm", {})
                        desc = str(fm.get("description") or "")[:160]
                        rows.append(f"- [**{c.name}**]({Path(c.rel).name}.md)" + (f" — {desc}" if desc else ""))
                    dest.write_text(
                        "---\n"
                        + yaml.safe_dump({"title": child.name, "lang": lang, "generated": True},
                                         allow_unicode=True, sort_keys=False).strip()
                        + "\n---\n\n"
                        + f"# {child.name}\n\n"
                        + "\n".join(rows)
                        + "\n",
                        encoding="utf-8")
                    created.append(idx_rel)
                    child.rel = idx_rel[:-3]
        write_section_indexes(child, lang_root, lang, pages)
    return created


def render_landing(lang: str, node: Node, pages: dict[str, dict[str, Any]], manifest: dict[str, Any],
                   lang_root: Path) -> None:
    stats = {
        "pages": manifest.get("page_count", len(pages)),
        "bytes": manifest.get("total_bytes", 0),
        "captured": manifest.get("generated", "")[:10],
        "plan": manifest.get("plan", ""),
        "source": manifest.get("source", ""),
    }
    lines = [
        "---",
        yaml.safe_dump({
            "title": f"Documentação do GitHub Actions — {LANG_LABELS.get(lang, lang)}",
            "description": "Índice da base de conhecimento capturada de docs.github.com (conteúdo principal de cada página).",
            "lang": lang,
            "generated": True,
        }, allow_unicode=True, sort_keys=False).strip(),
        "---",
        "",
        f"# GitHub Actions — {LANG_LABELS.get(lang, lang)}",
        "",
        f"> **{stats['pages']} páginas** · {stats['bytes']:,} bytes · capturado em **{stats['captured']}** · "
        f"fonte `{stats['source']}` · plano `{stats['plan']}`",
        "",
        "Cada página contém **somente o conteúdo principal do artigo** — navegação, sidebars, breadcrumbs,",
        "sumário \"Neste artigo\" e rodapé são removidos na captura.",
        "",
        "## Seções",
        "",
    ]
    for child in node.children:
        lines.append(f"### {child.name}")
        lines.append("")
        if child.rel:
            fm = pages.get(child.rel, {}).get("fm", {})
            if fm.get("description"):
                lines.append(f"_{fm['description']}_")
                lines.append("")
            lines.append(f"- [Visão geral]({child.rel}.md)")
        for sub in child.children[:60]:
            if sub.rel:
                fm = pages.get(sub.rel, {}).get("fm", {})
                desc = str(fm.get("description") or "")[:140]
                lines.append(f"- [{sub.name}]({sub.rel}.md)" + (f" — {desc}" if desc else ""))
            elif sub.children:
                lines.append(f"- **{sub.name}/** ({len(sub.children)} páginas)")
        lines.append("")
    (lang_root / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# Skill → páginas navegáveis
# --------------------------------------------------------------------------- #

def sync_skill(knowledge: Path) -> list[str]:
    """Copia/gera as páginas da skill dentro de knowledge/skill para navegação MkDocs."""
    created: list[str] = []
    if not SKILL_DIR.exists():
        return created
    dest_root = knowledge / "skill"
    if dest_root.exists():
        shutil.rmtree(dest_root)
    dest_root.mkdir(parents=True, exist_ok=True)

    skill_md = SKILL_DIR / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        fm: dict[str, Any] = {}
        if text.startswith("---"):
            parts = text.split("---", 2)
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except Exception:
                fm = {}
            text = parts[2]
        fm_out = {"title": fm.get("name", "Skill GitHub Actions"), "description": fm.get("description", ""),
                  "generated": True, "canonical": f"{REPO_URL}/blob/{BRANCH}/skills/github-actions/SKILL.md"}
        (dest_root / "index.md").write_text(
            "---\n" + yaml.safe_dump(fm_out, allow_unicode=True, sort_keys=False).strip() + "\n---\n\n" + text.lstrip(),
            encoding="utf-8")
        created.append("skill/index.md")

    refs = SKILL_DIR / "references"
    if refs.exists():
        out_refs = dest_root / "references"
        out_refs.mkdir(exist_ok=True)
        for ref in sorted(refs.rglob("*.md")):
            text = ref.read_text(encoding="utf-8")
            fm = {}
            if text.startswith("---"):
                parts = text.split("---", 2)
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                except Exception:
                    fm = {}
                text = parts[2]
            fm.setdefault("title", ref.stem.replace("-", " ").capitalize())
            fm["generated"] = True
            fm["canonical"] = f"{REPO_URL}/blob/{BRANCH}/skills/github-actions/references/{ref.relative_to(refs).as_posix()}"
            dest = out_refs / ref.relative_to(refs)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("---\n" + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
                            + "\n---\n\n" + text.lstrip(), encoding="utf-8")
            created.append(f"skill/references/{ref.relative_to(refs).as_posix()}")

    templates = SKILL_DIR / "templates"
    if templates.exists():
        cat = ["---", yaml.safe_dump({"title": "Catálogo de templates", "generated": True},
                                     allow_unicode=True, sort_keys=False).strip(), "---", "",
               "# Catálogo de templates prontos para uso", "",
               "Todos os templates abaixo são validados em CI por `actionlint` + `yamllint` + validação de esquema.",
               ""]
        for tpl in sorted(templates.rglob("*")):
            if tpl.is_dir() or tpl.suffix not in (".yml", ".yaml", ".md", ".json", ".sh"):
                continue
            rel = tpl.relative_to(templates).as_posix()
            cat.append(f"## `{rel}`")
            cat.append("")
            cat.append(f"[Abrir no repositório]({REPO_URL}/blob/{BRANCH}/skills/github-actions/templates/{rel})")
            cat.append("")
            lang = {"yml": "yaml", "yaml": "yaml", "md": "markdown", "json": "json", "sh": "bash"}.get(tpl.suffix[1:], "")
            content = tpl.read_text(encoding="utf-8")
            if tpl.suffix in (".yml", ".yaml"):
                try:
                    meta = yaml.safe_load(content) or {}
                    name = meta.get("name", "")
                    triggers = list((meta.get("on") or meta.get(True) or {}).keys()) if isinstance(meta.get("on") or meta.get(True), dict) else []
                    if name:
                        cat.append(f"**{name}**" + (f" · gatilhos: {', '.join(f'`{t}`' for t in triggers)}" if triggers else ""))
                        cat.append("")
                except Exception:
                    pass
            fence = "```" + lang
            cat.append(fence)
            cat.append(content.rstrip("\n"))
            cat.append("```")
            cat.append("")
        (dest_root / "templates.md").write_text("\n".join(cat), encoding="utf-8")
        created.append("skill/templates.md")
    return created


# --------------------------------------------------------------------------- #
# mkdocs.yml
# --------------------------------------------------------------------------- #

def render_nav(knowledge: Path, langs: list[str]) -> str:
    lines = ["nav:", "  - Início: index.md"]
    for lang in langs:
        lang_root = knowledge / lang
        if not lang_root.exists():
            continue
        label = "Documentação oficial (pt-BR)" if lang == "pt" else "Espelho do source-of-truth (en)"
        lines.append(f"  - {label}:")
        lines.append(f"      - Visão geral: {lang}/index.md")
        pages = load_tree(lang_root)
        order_map = build_order_map(knowledge / "en") if lang == "pt" else build_order_map(knowledge / "en")
        tree = build_tree(pages, lang_root, order_map)
        sub = nav_yaml(tree, f"{lang}/", indent=3)
        lines += sub
    skill_root = knowledge / "skill"
    if skill_root.exists():
        lines.append("  - Skill (padrão Agent Skills):")
        lines.append("      - SKILL.md: skill/index.md")
        refs_dir = skill_root / "references"
        if refs_dir.exists():
            lines.append("      - Referências:")
            for ref in sorted(refs_dir.rglob("*.md")):
                rel = ref.relative_to(skill_root).as_posix()
                fm = read_front_matter(ref)
                title = str(fm.get("title") or ref.stem.replace("-", " ").capitalize())
                lines.append(f"          - {yaml.safe_dump(title, allow_unicode=True).strip()}: skill/{rel}")
        if (skill_root / "templates.md").exists():
            lines.append("      - Catálogo de templates: skill/templates.md")
    lines.append("  - Validação e conformidade: validation.md")
    return "\n".join(lines) + "\n"


def update_mkdocs(nav_block: str, dry_run: bool = False) -> None:
    if not MKDOCS_YML.exists():
        print(f"[warn] {MKDOCS_YML} não existe; nada a atualizar", file=sys.stderr)
        return
    text = MKDOCS_YML.read_text(encoding="utf-8")
    block = f"{NAV_BEGIN}\n{nav_block}{NAV_END}\n"
    if NAV_BEGIN in text and NAV_END in text:
        new = re.sub(re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END) + r"\n?", block, text, flags=re.S)
    else:
        new = text.rstrip("\n") + "\n\n" + block
    if dry_run:
        print(nav_block)
        return
    MKDOCS_YML.write_text(new, encoding="utf-8")


def render_root_index(knowledge: Path, langs: list[str], manifests: dict[str, dict[str, Any]]) -> None:
    total_pages = sum(m.get("page_count", 0) for m in manifests.values())
    total_bytes = sum(m.get("total_bytes", 0) for m in manifests.values())
    lines = [
        "---",
        yaml.safe_dump({
            "title": "GitHub Actions — Base de Conhecimento & Skill",
            "description": "Documentação oficial do GitHub Actions capturada página a página (pt-BR) + skill com templates validados de CI/CD, GitOps e DevOps.",
            "generated": True,
        }, allow_unicode=True, sort_keys=False).strip(),
        "---",
        "",
        "# GitHub Actions — Base de Conhecimento & Skill",
        "",
        "Repositório de referência construído em três camadas:",
        "",
        "| Camada | O que é | Onde está |",
        "| --- | --- | --- |",
        "| **Captura** | Conteúdo principal de cada página de `docs.github.com/pt/actions` (sem nav/sidebar), página a página | `knowledge/pt/` |",
        "| **Espelho** | Source-of-truth `github/docs` convertido (Liquid resolvido) para comparação/auditoria | `knowledge/en/` |",
        "| **Skill** | `SKILL.md` + referências + templates de workflows/actions validados em CI | `skills/github-actions/` |",
        "",
        f"> **{total_pages} páginas** · {total_bytes:,} bytes · atualizado em {dt.date.today().isoformat()}",
        "",
        "## Comece por aqui",
        "",
    ]
    for lang in langs:
        m = manifests.get(lang, {})
        lines.append(f"- [{LANG_LABELS.get(lang, lang)}]({lang}/index.md) — {m.get('page_count', 0)} páginas"
                     f" (fonte `{m.get('source', '-')}`, plano `{m.get('plan', '-')}`)")
    lines += [
        "- [Skill: SKILL.md](skill/index.md) — como usar este repositório como skill de agente",
        "- [Catálogo de templates](skill/templates.md) — workflows prontos por contexto (CI/CD, GitOps, DevOps, segurança)",
        "- [Validação e conformidade](validation.md) — resultado automatizado dos checadores",
        "",
        "## Páginas mais consultadas",
        "",
        "- [Referência de contextos](pt/actions/reference/workflows-and-actions/contexts.md) — `github`, `secrets`, `vars`, `needs`, `matrix`…",
        "- [Sintaxe de fluxo de trabalho](pt/actions/reference/workflows-and-actions/workflow-syntax.md)",
        "- [Expressões](pt/actions/reference/workflows-and-actions/expressions.md)",
        "- [Variáveis](pt/actions/reference/workflows-and-actions/variables.md) · [Usar segredos](pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)",
        "- [Eventos que disparam fluxos de trabalho](pt/actions/reference/workflows-and-actions/events-that-trigger-workflows.md)",
        "- [Reutilizar fluxos de trabalho](pt/actions/how-tos/reuse-automations/reuse-workflows.md)",
        "- [Segurança: hardening](pt/actions/reference/security/security-hardening-for-github-actions.md) · [OIDC](pt/actions/reference/security/oidc.md)",
        "",
        "## Como reproduzir",
        "",
        "```bash",
        "# 1) capturar (requer acesso a docs.github.com — em CI roda automaticamente)",
        "python3 scripts/extract.py --source api --lang pt --out knowledge/pt \\",
        "  --plan free-pro-team@latest,enterprise-cloud@latest",
        "",
        "# 2) gerar nav + índices do MkDocs",
        "python3 scripts/build_site.py",
        "",
        "# 3) validar completude/conformidade",
        "python3 scripts/validate.py --report VALIDATION.md",
        "",
        "# 4) servir localmente",
        "mkdocs serve -a 0.0.0.0:8000",
        "```",
        "",
    ]
    (knowledge / "index.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera nav/índices do MkDocs para a base de conhecimento")
    ap.add_argument("--knowledge", default=str(KNOWLEDGE))
    ap.add_argument("--langs", default="pt,en")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-skill", action="store_true")
    args = ap.parse_args(argv)

    knowledge = Path(args.knowledge).resolve()
    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    manifests: dict[str, dict[str, Any]] = {}

    if not args.no_skill:
        created = sync_skill(knowledge)
        print(f"[info] skill sincronizada em knowledge/skill ({len(created)} páginas)")

    for lang in langs:
        lang_root = knowledge / lang
        if not lang_root.exists():
            print(f"[warn] {lang_root} não existe — pulando idioma {lang}", file=sys.stderr)
            continue
        manifests[lang] = load_manifest(lang_root)
        pages = load_tree(lang_root)
        order_map = build_order_map(knowledge / "en")
        tree = build_tree(pages, lang_root, order_map)
        created = write_section_indexes(tree, lang_root, lang, pages)
        if created:
            print(f"[info] {lang}: {len(created)} índices de seção gerados")
            pages = load_tree(lang_root)
            tree = build_tree(pages, lang_root, order_map)
        render_landing(lang, tree, pages, manifests[lang], lang_root)

    render_root_index(knowledge, langs, manifests)
    nav_block = render_nav(knowledge, langs)
    update_mkdocs(nav_block, dry_run=args.dry_run)
    (knowledge / "nav.generated.yml").write_text(nav_block, encoding="utf-8")
    print(f"[done] nav gerado ({len(nav_block.splitlines())} linhas) → {MKDOCS_YML}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
