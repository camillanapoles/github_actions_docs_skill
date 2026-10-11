#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate.py — Validador de COMPLETUDE e CONFORMIDADE da base de conhecimento + skill.

Implementa o mandato de validação do repositório em 8 grupos de verificação:

  1. inventory    — toda página do inventário (manifest/pagelist) foi capturada
  2. frontmatter  — metadados obrigatórios presentes e válidos
  3. structure    — H1 único, hierarquia de headings, tamanho mínimo
  4. conversion   — zero Liquid residual, zero HTML em bloco, cercas balanceadas,
                    tabelas bem formadas, sem ruído de UI do site
  5. links        — links internos resolvem, âncoras existem, externos bem formados
  6. navigation   — mkdocs.yml válido, nav aponta para arquivos existentes, sem órfãos
  7. skill        — SKILL.md conforme o padrão Agent Skills, referências e templates
                    existentes, YAML válido, workflows com estrutura mínima,
                    `permissions` explícito, actions pinadas
  8. tools        — actionlint / yamllint / mkdocs build --strict (quando disponíveis)

Saídas: console, `VALIDATION.md` (legível) e `.ci/validation.json` (máquina).
Exit code: 0 = tudo ok, 1 = há falhas, 2 = erro de execução.

Uso:
  python3 scripts/validate.py
  python3 scripts/validate.py --online --mkdocs --report VALIDATION.md
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML é obrigatório: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE = ROOT / "knowledge"
SKILLS = ROOT / "skills"
MKDOCS_YML = ROOT / "mkdocs.yml"

PASS, WARN, FAIL = "pass", "warn", "fail"
ICONS = {PASS: "✅", WARN: "⚠️", FAIL: "❌"}

REQUIRED_FRONTMATTER = ("title", "source", "captured", "lang")
UI_NOISE_PATTERNS = (
    "skip to main content", "pular para o conteúdo principal", "neste artigo",
    "in this article", "copiar markdown", "copy markdown", "barra lateral do recolhimento",
    "expandir barra lateral", "collapse sidebar", "expand sidebar",
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
LIQUID_RE = re.compile(r"\{%-?\s*[a-zA-Z_]")
BLOCK_HTML_RE = re.compile(r"</?\s*(div|table|thead|tbody|tfoot|tr|td|th|ul|ol|li|dl|dt|dd|svg|path|section|article|nav|aside|header|footer|iframe|span)\b", re.I)
ESCAPED_ALERT_RE = re.compile(r"\\\[!(NOTE|TIP|WARNING|IMPORTANT|CAUTION)\]", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
EXPLICIT_ID_RE = re.compile(r"\{\s*#([A-Za-z0-9_.:\-]+)\s*\}\s*$")
LINK_RE = re.compile(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)\)")
IMAGE_RE = re.compile(r"\!\[([^\]]*)\]\(([^)\s]+)\)")
SLUG_STRIP_RE = re.compile(r"[^\w\s\-]", re.UNICODE)


# --------------------------------------------------------------------------- #
# YAML loader tolerante aos tags `!!python/...` do MkDocs Material
# --------------------------------------------------------------------------- #

class _MaterialSafeLoader(yaml.SafeLoader):
    pass


def _ignore_unknown(loader: yaml.SafeLoader, suffix: str, node: Any) -> Any:
    return None


_MaterialSafeLoader.add_multi_constructor("tag:yaml.org,2002:python/", _ignore_unknown)


def load_yaml_lenient(text: str) -> Any:
    return yaml.load(text, Loader=_MaterialSafeLoader)  # noqa: S506 (loader custom, sem exec)


# --------------------------------------------------------------------------- #
# Modelo de resultado
# --------------------------------------------------------------------------- #


@dataclass
class Check:
    group: str
    name: str
    status: str
    message: str = ""
    details: list[str] = field(default_factory=list)


class Report:
    def __init__(self) -> None:
        self.checks: list[Check] = []

    def add(self, group: str, name: str, status: str, message: str = "", details: Iterable[str] = ()) -> None:
        self.checks.append(Check(group, name, status, message, [str(d) for d in details][:40]))

    @property
    def failures(self) -> list[Check]:
        return [c for c in self.checks if c.status == FAIL]

    @property
    def warnings(self) -> list[Check]:
        return [c for c in self.checks if c.status == WARN]

    @property
    def passes(self) -> list[Check]:
        return [c for c in self.checks if c.status == PASS]


# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #


def github_slug(text: str) -> str:
    """Slug de heading no estilo GitHub/docs (usado nas âncoras capturadas)."""
    text = EXPLICIT_ID_RE.sub("", text).strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = SLUG_STRIP_RE.sub("", text)
    return re.sub(r"\s+", "-", text).strip("-")


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = load_yaml_lenient(parts[1]) or {}
    except Exception:
        fm = {}
    return (fm if isinstance(fm, dict) else {}), parts[2]


def lines_outside_fences(text: str) -> Iterable[tuple[int, str, bool]]:
    """Yield (nº da linha, linha, dentro_de_cerca)."""
    fence = False
    fence_char = ""
    for i, line in enumerate(text.split("\n"), start=1):
        m = FENCE_RE.match(line)
        if m:
            if not fence:
                fence, fence_char = True, m.group(1)
                yield i, line, True
                continue
            if m.group(1) == fence_char:
                fence = False
                yield i, line, True
                continue
        yield i, line, fence


def fence_parity_ok(text: str) -> bool:
    return not any(inside for _, _, inside in [next(iter(()), (0, "", False))] ) and _count_unclosed(text) == 0


def _count_unclosed(text: str) -> int:
    fence = False
    fence_char = ""
    unclosed = 0
    for line in text.split("\n"):
        m = FENCE_RE.match(line)
        if not m:
            continue
        if not fence:
            fence, fence_char = True, m.group(1)
        elif m.group(1) == fence_char:
            fence = False
    if fence:
        unclosed += 1
    return unclosed


def collect_md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def page_anchor_index(path: Path) -> set[str]:
    """Âncoras disponíveis numa página (explícitas `{ #id }` + slugs de heading)."""
    text = path.read_text(encoding="utf-8")
    _, body = split_front_matter(text)
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for _lineno, line, inside in lines_outside_fences(body):
        if inside:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        explicit = EXPLICIT_ID_RE.search(line)
        slug = explicit.group(1) if explicit else github_slug(m.group(2))
        counts[slug] = counts.get(slug, 0) + 1
        anchors.add(slug if counts[slug] == 1 else f"{slug}-{counts[slug] - 1}")
    return anchors


# --------------------------------------------------------------------------- #
# 1. Inventário / completude
# --------------------------------------------------------------------------- #


def check_inventory(rep: Report, langs: list[str], online: bool) -> dict[str, dict[str, Any]]:
    manifests: dict[str, dict[str, Any]] = {}
    for lang in langs:
        root = KNOWLEDGE / lang
        mpath = root / "manifest.json"
        if not root.exists():
            rep.add("inventory", f"knowledge/{lang}", FAIL, "diretório de idioma ausente")
            continue
        manifest = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {}
        manifests[lang] = manifest
        pages = manifest.get("pages", [])
        files = {p.relative_to(root).as_posix() for p in collect_md_files(root)}
        declared = {p.get("path") for p in pages if p.get("path")}
        missing_files = sorted(declared - files)
        ok_pages = [p for p in pages if p.get("status") == "ok"]
        failed_pages = [p for p in pages if p.get("status") not in ("ok", "skipped")]
        rep.add("inventory", f"{lang}: manifest presente",
                PASS if manifest else WARN,
                f"{len(pages)} páginas declaradas, {len(ok_pages)} ok, {len(files)} arquivos .md em disco")
        rep.add("inventory", f"{lang}: manifest ↔ disco",
                FAIL if missing_files else PASS,
                f"{len(missing_files)} páginas declaradas sem arquivo" if missing_files else "todas as páginas declaradas existem em disco",
                missing_files)
        rep.add("inventory", f"{lang}: falhas de captura",
                FAIL if failed_pages else PASS,
                f"{len(failed_pages)} páginas com erro na captura" if failed_pages else "nenhuma falha de captura registrada",
                [f"{p.get('url')}: {p.get('error')}" for p in failed_pages])
        if online:
            try:
                sys.path.insert(0, str(ROOT / "scripts"))
                import extract  # type: ignore
                plan = manifest.get("plan", "free-pro-team@latest")
                first_plan = str(plan).split(",")[0]
                paths = extract.discover_pagelist(lang, first_plan, "actions")
                expected = {extract.normalize_docs_path(p, lang, "actions") for p in paths}
                expected.discard(None)
                missing = sorted(expected - declared)
                rep.add("inventory", f"{lang}: completude vs /api/pagelist",
                        FAIL if missing else PASS,
                        f"pagelist={len(expected)} capturadas={len(declared)} faltando={len(missing)}",
                        missing)
            except Exception as exc:
                rep.add("inventory", f"{lang}: completude vs /api/pagelist", WARN,
                        f"verificação online indisponível: {exc}")
    return manifests


# --------------------------------------------------------------------------- #
# 2-4. Frontmatter, estrutura e conversão
# --------------------------------------------------------------------------- #


def check_pages(rep: Report, langs: list[str]) -> dict[str, int]:
    stats = {"pages": 0, "bytes": 0, "headings": 0, "code_blocks": 0, "tables": 0}
    problems: dict[str, list[str]] = {
        "frontmatter": [], "h1": [], "liquid": [], "html": [], "fence": [],
        "table": [], "noise": [], "alert": [], "autotitle": [], "small": [], "anchor_dup": [],
    }
    for lang in langs:
        root = KNOWLEDGE / lang
        if not root.exists():
            continue
        for md in collect_md_files(root):
            text = md.read_text(encoding="utf-8")
            rel = md.relative_to(KNOWLEDGE).as_posix()
            fm, body = split_front_matter(text)
            stats["pages"] += 1
            stats["bytes"] += len(text.encode("utf-8"))

            # 2. frontmatter (páginas geradas pelo build_site não são capturas)
            generated = bool(fm.get("generated"))
            missing = [k for k in REQUIRED_FRONTMATTER if not fm.get(k)]
            if missing and not generated:
                problems["frontmatter"].append(f"{rel}: faltam {missing}")

            # 3. estrutura
            h1_count = 0
            headings = 0
            code_blocks = 0
            fence_open = False
            fence_char = ""
            table_lines: list[tuple[int, list[int]]] = []
            for lineno, line, inside in lines_outside_fences(body):
                m = HEADING_RE.match(line)
                if not inside and m:
                    headings += 1
                    if len(m.group(1)) == 1:
                        h1_count += 1
                fm_match = FENCE_RE.match(line)
                if fm_match:
                    if not fence_open:
                        fence_open, fence_char = True, fm_match.group(1)
                        code_blocks += 1
                    elif fm_match.group(1) == fence_char:
                        fence_open = False
                    continue
                if inside:
                    continue
                if re.match(r"^\s*\|.*\|\s*$", line):
                    cells = len(re.split(r"(?<!\\)\|", line.strip().strip("|")))
                    table_lines.append((lineno, [cells]))
                if LIQUID_RE.search(line):
                    problems["liquid"].append(f"{rel}:{lineno}: {line.strip()[:90]}")
                if BLOCK_HTML_RE.search(line):
                    problems["html"].append(f"{rel}:{lineno}: {line.strip()[:90]}")
                if ESCAPED_ALERT_RE.search(line):
                    problems["alert"].append(f"{rel}:{lineno}: alerta escapado")
                if "AUTOTITLE" in line:
                    problems["autotitle"].append(f"{rel}:{lineno}")
                low = line.strip().lower()
                if not generated and low and any(noise in low for noise in UI_NOISE_PATTERNS) and len(low) < 60:
                    problems["noise"].append(f"{rel}:{lineno}: {line.strip()[:70]}")
            if fence_open:
                problems["fence"].append(f"{rel}: cerca de código não fechada")
            if h1_count != 1:
                problems["h1"].append(f"{rel}: {h1_count} H1 (esperado 1)")
            if len(text.encode("utf-8")) < 400 and not generated:
                problems["small"].append(f"{rel}: {len(text.encode('utf-8'))} bytes")
            stats["headings"] += headings
            stats["code_blocks"] += code_blocks

            # tabelas: mesma contagem de células em linhas consecutivas
            block: list[int] = []
            for lineno, (cells,) in table_lines:
                block.append(cells)
            for i in range(1, len(block)):
                if block[i] != block[i - 1]:
                    problems["table"].append(f"{rel}: linha de tabela com {block[i]} células (esperado {block[i - 1]})")
                    break

    checks = [
        ("frontmatter", "frontmatter completo", f"páginas sem {REQUIRED_FRONTMATTER}"),
        ("h1", "H1 único por página", "páginas com H1 duplicado/ausente"),
        ("liquid", "zero Liquid residual", "tags `{% %}` fora de cercas de código"),
        ("html", "zero HTML em bloco", "tags HTML de bloco fora de cercas de código"),
        ("fence", "cercas balanceadas", "arquivos com cerca não fechada"),
        ("table", "tabelas bem formadas", "linhas com nº de células inconsistente"),
        ("noise", "sem ruído de UI", "restos de navegação do site"),
        ("alert", "alertas convertidos", "`> \\[!NOTE]` escapado (não vira admonition)"),
        ("autotitle", "AUTOTITLE resolvido", "placeholders `[AUTOTITLE]` restantes"),
        ("small", "tamanho mínimo", "páginas com menos de 400 bytes"),
    ]
    for key, name, why in checks:
        items = problems[key]
        rep.add("conversion" if key in ("liquid", "html", "fence", "table", "noise", "alert", "autotitle") else "structure",
                name, FAIL if items else PASS,
                f"{len(items)} ocorrência(s) — {why}" if items else "ok", items)
    return stats


# --------------------------------------------------------------------------- #
# 5. Links e âncoras
# --------------------------------------------------------------------------- #


def check_links(rep: Report, langs: list[str]) -> None:
    broken: list[str] = []
    broken_anchors: list[str] = []
    external_malformed: list[str] = []
    total_internal = total_external = 0
    anchor_cache: dict[Path, set[str]] = {}
    for lang in langs:
        root = KNOWLEDGE / lang
        if not root.exists():
            continue
        for md in collect_md_files(root):
            text = md.read_text(encoding="utf-8")
            _, body = split_front_matter(text)
            rel = md.relative_to(KNOWLEDGE).as_posix()
            for lineno, line, inside in lines_outside_fences(body):
                if inside:
                    continue
                for m in list(LINK_RE.finditer(line)) + list(IMAGE_RE.finditer(line)):
                    target = m.group(2)
                    if target.startswith("mailto:"):
                        continue
                    if target.startswith("#"):
                        if md not in anchor_cache:
                            anchor_cache[md] = page_anchor_index(md)
                        if target[1:] not in anchor_cache[md]:
                            broken_anchors.append(f"{rel}:{lineno}: {target}")
                        continue
                    if target.startswith(("http://", "https://")):
                        total_external += 1
                        if not re.match(r"^https://[^\s]+$", target):
                            external_malformed.append(f"{rel}:{lineno}: {target[:80]}")
                        continue
                    total_internal += 1
                    path_part, _, frag = target.partition("#")
                    dest = (md.parent / path_part).resolve()
                    if not dest.exists():
                        broken.append(f"{rel}:{lineno}: {target}")
                        continue
                    if frag and dest.suffix == ".md":
                        if dest not in anchor_cache:
                            anchor_cache[dest] = page_anchor_index(dest)
                        if frag not in anchor_cache[dest]:
                            broken_anchors.append(f"{rel}:{lineno}: {target} (âncora inexistente)")
    rep.add("links", "links internos resolvem",
            FAIL if broken else PASS,
            f"{total_internal} links internos, {len(broken)} quebrados", broken)
    rep.add("links", "âncoras existem",
            WARN if broken_anchors else PASS,
            f"{len(broken_anchors)} âncoras sem heading correspondente", broken_anchors)
    rep.add("links", "links externos bem formados",
            FAIL if external_malformed else PASS,
            f"{total_external} links externos, {len(external_malformed)} malformados", external_malformed)


# --------------------------------------------------------------------------- #
# 6. Navegação MkDocs
# --------------------------------------------------------------------------- #


def walk_nav(node: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    """Percorre o `nav:` do mkdocs.yml yieldando (rótulo, arquivo)."""
    if isinstance(node, str):
        yield prefix, node
    elif isinstance(node, dict):
        for label, value in node.items():
            if isinstance(value, str):
                yield str(label), value
            elif isinstance(value, list):
                yield from walk_nav(value, str(label))
    elif isinstance(node, list):
        for item in node:
            yield from walk_nav(item, prefix)


def check_navigation(rep: Report) -> None:
    if not MKDOCS_YML.exists():
        rep.add("navigation", "mkdocs.yml presente", FAIL, "arquivo ausente")
        return
    text = MKDOCS_YML.read_text(encoding="utf-8")
    try:
        cfg = load_yaml_lenient(text) or {}
    except Exception as exc:
        rep.add("navigation", "mkdocs.yml válido", FAIL, f"YAML inválido: {exc}")
        return
    rep.add("navigation", "mkdocs.yml válido", PASS, f"site_name={cfg.get('site_name')!r}")
    docs_dir = ROOT / str(cfg.get("docs_dir", "docs"))
    nav = cfg.get("nav")
    if not nav:
        rep.add("navigation", "nav definido", FAIL, "mkdocs.yml sem bloco nav")
        return
    entries = list(walk_nav(nav))
    missing = []
    for _label, target in entries:
        if not isinstance(target, str):
            continue
        if not (docs_dir / target).exists():
            missing.append(f"{_label} → {target}")
    rep.add("navigation", "nav aponta para arquivos existentes",
            FAIL if missing else PASS,
            f"{len(entries)} entradas no nav, {len(missing)} quebradas", missing)

    # órfãos: todo .md deve estar no nav ou ser referenciado por alguma página
    nav_targets = {t for _, t in entries if isinstance(t, str)}
    referenced: set[str] = set()
    for md in collect_md_files(docs_dir):
        rel = md.relative_to(docs_dir).as_posix()
        if rel in nav_targets:
            continue
        body = md.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(body):
            target = m.group(2)
            if target.startswith(("http", "mailto:", "#")):
                continue
            dest = (md.parent / target.partition("#")[0]).resolve()
            try:
                referenced.add(dest.relative_to(docs_dir).as_posix())
            except ValueError:
                pass
    orphans = []
    for md in collect_md_files(docs_dir):
        rel = md.relative_to(docs_dir).as_posix()
        if rel in nav_targets or rel in referenced:
            continue
        if rel.endswith("tags.md") or rel.endswith("validation.md"):
            continue
        orphans.append(rel)
    rep.add("navigation", "sem páginas órfãs",
            WARN if orphans else PASS,
            f"{len(orphans)} páginas fora do nav e sem link de entrada", orphans)
    for required in ("index.md", "pt/index.md", "en/index.md", "skill/index.md"):
        rep.add("navigation", f"índice {required}",
                PASS if (docs_dir / required).exists() else WARN,
                "presente" if (docs_dir / required).exists() else "ausente")


# --------------------------------------------------------------------------- #
# 7. Skill
# --------------------------------------------------------------------------- #


def check_skill(rep: Report) -> list[Path]:
    workflow_files: list[Path] = []
    skill_root = SKILLS / "github-actions"
    skill_md = skill_root / "SKILL.md"
    if not skill_md.exists():
        rep.add("skill", "SKILL.md presente", FAIL, f"{skill_md} não encontrado")
        return workflow_files
    text = skill_md.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    name = str(fm.get("name", ""))
    description = str(fm.get("description", ""))
    rep.add("skill", "SKILL.md com frontmatter", PASS if fm else FAIL,
            f"name={name!r} description={len(description)} chars")
    rep.add("skill", "name válido (≤64, [a-z0-9-])",
            PASS if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64 else FAIL,
            name or "(vazio)")
    rep.add("skill", "description válida (≤1024, não vazia)",
            PASS if 0 < len(description) <= 1024 else FAIL,
            f"{len(description)} caracteres")
    if fm.get("license"):
        rep.add("skill", "license declarado", PASS, str(fm.get("license")))
    if fm.get("allowed-tools"):
        rep.add("skill", "allowed-tools declarado", PASS, str(fm.get("allowed-tools"))[:120])

    # arquivos referenciados no corpo do SKILL.md existem
    referenced = set(re.findall(r"(?:references|templates|scripts|assets)/[\w./\-]+", body))
    missing_refs = sorted(r for r in referenced if not (skill_root / r).exists())
    rep.add("skill", "referências do SKILL.md existem",
            FAIL if missing_refs else PASS,
            f"{len(referenced)} caminhos citados, {len(missing_refs)} ausentes", missing_refs)

    # references/*.md
    refs = sorted((skill_root / "references").rglob("*.md")) if (skill_root / "references").exists() else []
    rep.add("skill", "pasta references/", PASS if refs else WARN, f"{len(refs)} documentos de referência")
    for ref in refs:
        rtext = ref.read_text(encoding="utf-8")
        rfm, rbody = split_front_matter(rtext)
        if not rbody.strip():
            rep.add("skill", f"reference {ref.name}", FAIL, "arquivo vazio")

    # templates
    templates_root = skill_root / "templates"
    templates = sorted(p for p in templates_root.rglob("*") if p.is_file()) if templates_root.exists() else []
    yaml_templates = [p for p in templates if p.suffix in (".yml", ".yaml")]
    rep.add("skill", "templates presentes", PASS if templates else FAIL,
            f"{len(templates)} arquivos ({len(yaml_templates)} YAML)")

    bad_yaml: list[str] = []
    structural: list[str] = []
    perms: list[str] = []
    unpinned: list[str] = []
    for tpl in yaml_templates:
        try:
            data = load_yaml_lenient(tpl.read_text(encoding="utf-8"))
        except Exception as exc:
            bad_yaml.append(f"{tpl.relative_to(skill_root)}: {exc}")
            continue
        if not isinstance(data, dict):
            structural.append(f"{tpl.name}: YAML não é um mapeamento")
            continue
        rel = tpl.relative_to(skill_root).as_posix()
        is_action = tpl.name in ("action.yml", "action.yaml")
        if is_action:
            if not data.get("name") or not data.get("description"):
                structural.append(f"{rel}: action sem name/description")
            runs = data.get("runs") or {}
            if not runs.get("using"):
                structural.append(f"{rel}: action sem runs.using")
            if runs.get("using") == "composite" and not runs.get("steps"):
                structural.append(f"{rel}: composite action sem steps")
            continue
        # workflow
        on = data.get("on", data.get(True))
        jobs = data.get("jobs") or {}
        if not on:
            structural.append(f"{rel}: sem gatilho `on`")
        if not jobs:
            structural.append(f"{rel}: sem `jobs`")
        if "permissions" not in data:
            perms.append(f"{rel}: sem `permissions` no topo (princípio do menor privilégio)")
        for job_id, job in (jobs.items() if isinstance(jobs, dict) else []):
            if not isinstance(job, dict):
                continue
            if not job.get("runs-on") and not job.get("uses"):
                structural.append(f"{rel}: job `{job_id}` sem runs-on/uses")
            if job.get("steps") is not None and not job.get("steps"):
                structural.append(f"{rel}: job `{job_id}` com steps vazio")
            for step in job.get("steps") or []:
                uses = str(step.get("uses", "")) if isinstance(step, dict) else ""
                if not uses:
                    continue
                ref = uses.split("@")[-1] if "@" in uses else ""
                if not ref or (re.fullmatch(r"[A-Za-z0-9_.\-/]+", ref) and not re.fullmatch(r"v?\d+(\.\d+){0,2}", ref)
                               and not re.fullmatch(r"[0-9a-f]{40}", ref) and not ref.startswith("v")):
                    unpinned.append(f"{rel}: `uses: {uses}` (pin por tag/SHA recomendado)")
                if "@" not in uses and "/" in uses:
                    unpinned.append(f"{rel}: `uses: {uses}` sem @ref")
        workflow_files.append(tpl)

    rep.add("skill", "templates YAML válidos", FAIL if bad_yaml else PASS,
            f"{len(bad_yaml)} inválidos de {len(yaml_templates)}", bad_yaml)
    rep.add("skill", "estrutura de workflows/actions", FAIL if structural else PASS,
            f"{len(structural)} problemas estruturais", structural)
    rep.add("skill", "permissions explícito", WARN if perms else PASS,
            f"{len(perms)} templates sem `permissions`", perms)
    rep.add("skill", "actions pinadas (tag/SHA)", WARN if unpinned else PASS,
            f"{len(unpinned)} referências sem pin", unpinned)

    # scripts da skill executáveis/sintaticamente válidos
    scripts_dir = skill_root / "scripts"
    if scripts_dir.exists():
        bad_scripts: list[str] = []
        for script in sorted(scripts_dir.rglob("*")):
            if not script.is_file():
                continue
            if script.suffix == ".py":
                proc = subprocess.run([sys.executable, "-m", "py_compile", str(script)], capture_output=True, text=True)
                if proc.returncode:
                    bad_scripts.append(f"{script.name}: {proc.stderr.strip()[:120]}")
            elif script.suffix == ".sh":
                proc = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
                if proc.returncode:
                    bad_scripts.append(f"{script.name}: {proc.stderr.strip()[:120]}")
        rep.add("skill", "scripts da skill válidos", FAIL if bad_scripts else PASS,
                f"{len(bad_scripts)} scripts com erro de sintaxe", bad_scripts)
    return workflow_files


# --------------------------------------------------------------------------- #
# 8. Ferramentas externas
# --------------------------------------------------------------------------- #


def check_tools(rep: Report, workflow_files: list[Path], run_mkdocs: bool, actionlint_bin: str = "") -> None:
    # actionlint
    binary = actionlint_bin or shutil.which("actionlint") or ""
    if not binary:
        candidate = ROOT / ".ci" / "bin" / "actionlint"
        if candidate.exists():
            binary = str(candidate)
    if binary and workflow_files:
        proc = subprocess.run([binary, "-color=never", *map(str, workflow_files)], capture_output=True, text=True)
        output = (proc.stdout + proc.stderr).strip()
        issues = [ln for ln in output.splitlines() if ln.strip()]
        rep.add("tools", "actionlint", FAIL if proc.returncode else PASS,
                f"{len(issues)} apontamento(s)" if issues else "sem apontamentos", issues)
    else:
        rep.add("tools", "actionlint", WARN, "binário não encontrado (instalado no CI via .github/workflows/validate.yml)")

    # yamllint
    yamllint = shutil.which("yamllint")
    yaml_targets = [p for p in (SKILLS / "github-actions" / "templates").rglob("*.yml")] if (SKILLS / "github-actions" / "templates").exists() else []
    yaml_targets += sorted((ROOT / ".github" / "workflows").glob("*.yml")) if (ROOT / ".github" / "workflows").exists() else []
    if yamllint and yaml_targets:
        cfg = ROOT / ".yamllint"
        cmd = [yamllint, "-f", "parsable"]
        if cfg.exists():
            cmd += ["-c", str(cfg)]
        cmd += [str(p) for p in yaml_targets]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        errors = [ln for ln in proc.stdout.splitlines() if "(error)" in ln]
        warnings = [ln for ln in proc.stdout.splitlines() if "(warning)" in ln]
        rep.add("tools", "yamllint", FAIL if errors else (WARN if warnings else PASS),
                f"{len(errors)} erro(s), {len(warnings)} aviso(s) em {len(yaml_targets)} arquivos",
                errors[:20] or warnings[:20])
    else:
        rep.add("tools", "yamllint", WARN, "yamllint não instalado localmente (rodado no CI)")

    # mkdocs build --strict
    if run_mkdocs:
        mkdocs = shutil.which("mkdocs")
        if not mkdocs:
            rep.add("tools", "mkdocs build --strict", WARN, "mkdocs não instalado localmente")
        else:
            proc = subprocess.run([mkdocs, "build", "--strict"], cwd=str(ROOT), capture_output=True, text=True)
            tail = [ln for ln in (proc.stderr or proc.stdout).splitlines() if ln.strip()][-25:]
            rep.add("tools", "mkdocs build --strict", FAIL if proc.returncode else PASS,
                    "build ok" if not proc.returncode else f"exit {proc.returncode}", tail)


# --------------------------------------------------------------------------- #
# Relatórios
# --------------------------------------------------------------------------- #


def render_markdown(rep: Report, stats: dict[str, int], generated_files: dict[str, str]) -> str:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = [
        "---",
        "title: Validação e conformidade",
        "description: Resultado automatizado das verificações de completude e conformidade da base de conhecimento e da skill.",
        f"generated: {now}",
        "---",
        "",
        "# Validação e conformidade",
        "",
        f"> Gerado por `scripts/validate.py` em **{now}**  ",
        f"> **{len(rep.passes)} verificações OK** · **{len(rep.warnings)} avisos** · **{len(rep.failures)} falhas**",
        "",
        "## Resumo da base de conhecimento",
        "",
        "| Métrica | Valor |",
        "| --- | --- |",
        f"| Páginas validadas | {stats.get('pages', 0)} |",
        f"| Bytes totais | {stats.get('bytes', 0):,} |",
        f"| Headings | {stats.get('headings', 0):,} |",
        f"| Blocos de código | {stats.get('code_blocks', 0):,} |",
        "",
        "## Verificações",
        "",
        "| Grupo | Verificação | Status | Detalhe |",
        "| --- | --- | --- | --- |",
    ]
    for c in rep.checks:
        msg = c.message.replace("|", "\\|").replace("\n", " ")[:220]
        lines.append(f"| {c.group} | {c.name} | {ICONS[c.status]} {c.status} | {msg} |")
    details = [c for c in rep.checks if c.details and c.status != PASS]
    if details:
        lines += ["", "## Detalhes das ocorrências", ""]
        for c in details:
            lines.append(f"### {ICONS[c.status]} {c.group} — {c.name}")
            lines.append("")
            for d in c.details[:25]:
                lines.append(f"- `{d}`")
            if len(c.details) > 25:
                lines.append(f"- … e mais {len(c.details) - 25} ocorrências")
            lines.append("")
    lines += ["", "## Artefatos", "", "| Arquivo | Descrição |", "| --- | --- |"]
    for path, desc in generated_files.items():
        lines.append(f"| `{path}` | {desc} |")
    lines += [
        "",
        "## Como reproduzir",
        "",
        "```bash",
        "python3 scripts/validate.py --report knowledge/validation.md --json .ci/validation.json",
        "# com verificações online (completude vs docs.github.com) e build estrito:",
        "python3 scripts/validate.py --online --mkdocs",
        "```",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validação de completude e conformidade")
    ap.add_argument("--langs", default="pt,en")
    ap.add_argument("--report", default=str(KNOWLEDGE / "validation.md"))
    ap.add_argument("--json", default=str(ROOT / ".ci" / "validation.json"))
    ap.add_argument("--online", action="store_true", help="confere completude contra /api/pagelist")
    ap.add_argument("--mkdocs", action="store_true", help="executa mkdocs build --strict")
    ap.add_argument("--actionlint-bin", default="")
    args = ap.parse_args(argv)

    langs = [x.strip() for x in args.langs.split(",") if x.strip()]
    rep = Report()
    manifests = check_inventory(rep, langs, args.online)
    stats = check_pages(rep, langs)
    check_links(rep, langs)
    check_navigation(rep)
    workflow_files = check_skill(rep)
    check_tools(rep, workflow_files, args.mkdocs, args.actionlint_bin)

    generated = {
        "knowledge/pt/manifest.json": "inventário da captura pt-BR (por página: título, bytes, headings, avisos)",
        "knowledge/en/manifest.json": "inventário do espelho inglês (source-of-truth github/docs)",
        ".ci/extract-report.md": "relatório de execução da captura",
        ".ci/validation.json": "resultado desta validação em JSON",
        "knowledge/validation.md": "este relatório em Markdown (navegável no MkDocs)",
    }
    report_md = render_markdown(rep, stats, generated)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_md, encoding="utf-8")

    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps({
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "pass": len(rep.passes), "warn": len(rep.warnings), "fail": len(rep.failures),
            "pages": stats.get("pages", 0), "bytes": stats.get("bytes", 0),
            "headings": stats.get("headings", 0), "code_blocks": stats.get("code_blocks", 0),
        },
        "checks": [asdict(c) for c in rep.checks],
        "manifests": {k: {kk: vv for kk, vv in v.items() if kk != "pages"} for k, v in manifests.items()},
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    for c in rep.checks:
        if c.status != PASS:
            print(f"{ICONS[c.status]} [{c.group}] {c.name}: {c.message}")
    print(f"\n{len(rep.passes)} ok · {len(rep.warnings)} avisos · {len(rep.failures)} falhas "
          f"→ {report_path} e {json_path}")
    return 1 if rep.failures else 0


if __name__ == "__main__":
    sys.exit(main())
