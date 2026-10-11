#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract.py — Extrator/conversor da documentação do GitHub Actions para Markdown (MkDocs-ready).

Duas fontes suportadas:

  --source site : captura https://docs.github.com/<lang>/actions/** (HTML) e converte
                  SOMENTE o conteúdo principal do artigo (ignora navegação, sidebars,
                  breadcrumbs, "Neste artigo", rodapé e botões), gerando GFM limpo.
  --source repo : converte o source-of-truth do repositório `github/docs`
                  (frontmatter YAML + Liquid) para GFM limpo, resolvendo
                  `{% data reusables.* %}`, `{% ifversion %}`, `{% note %}` etc.

Saída: árvore de `.md` + `manifest.json` (inventário auditável) + relatório opcional.

Exemplos
--------
  python3 scripts/extract.py --source site --lang pt --out knowledge/pt
  python3 scripts/extract.py --source site --lang pt --out knowledge/pt --limit 5 --report .ci/extract-report.md
  python3 scripts/extract.py --source repo --lang en --out knowledge/en --repo-dir /tmp/ghdocs

O script é idempotente e seguro para CI/CD (GitHub Actions): exit code != 0 quando
falhas de captura excedem `--max-failures`.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import html as html_mod
import json
import os
import re
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None

try:
    from bs4 import BeautifulSoup, Tag  # type: ignore
except ImportError:  # pragma: no cover
    BeautifulSoup = None
    Tag = None

DOCS_HOST = "https://docs.github.com"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) github-actions-kb-extractor/1.0 (+skill)"
TODAY = dt.date.today().isoformat()

# --------------------------------------------------------------------------- #
# Infra: download com retry/backoff
# --------------------------------------------------------------------------- #


def http_get(url: str, timeout: int = 60, retries: int = 4, accept: str = "*/*") -> tuple[bytes, int]:
    """GET com retry exponencial e User-Agent estável. Retorna (body, status)."""
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": accept,
                    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
                    "Accept-Encoding": "identity",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read(), resp.status
        except urllib.error.HTTPError as exc:  # 429/5xx → retry
            last_err = exc
            if exc.code in (403, 404, 410):
                raise
            time.sleep(min(2 ** attempt * 1.5, 20))
        except Exception as exc:  # rede/timeout → retry
            last_err = exc
            time.sleep(min(2 ** attempt * 1.5, 20))
    raise RuntimeError(f"GET falhou após {retries} tentativas: {url} ({last_err})")


def http_get_text(url: str, **kw: Any) -> str:
    body, _ = http_get(url, **kw)
    return body.decode("utf-8", "replace")


# --------------------------------------------------------------------------- #
# Modelo de página
# --------------------------------------------------------------------------- #


@dataclass
class PageResult:
    path: str = ""            # caminho relativo do .md gerado (ex.: actions/reference/.../contexts.md)
    url: str = ""             # URL de origem
    title: str = ""
    short_title: str = ""
    description: str = ""
    section: str = ""         # trilha de seções (ex.: "Reference / Workflows and actions")
    lang: str = "pt"
    source: str = "site"      # site | repo
    bytes: int = 0
    headings: int = 0
    h2: int = 0
    code_blocks: int = 0
    tables: int = 0
    admonitions: int = 0
    links_internal: int = 0
    links_external: int = 0
    images: int = 0
    children: list[str] = field(default_factory=list)
    captured: str = TODAY
    status: str = "ok"        # ok | skipped | error
    selector: str = ""
    warnings: list[str] = field(default_factory=list)
    error: str = ""


# --------------------------------------------------------------------------- #
# Utilidades de Markdown
# --------------------------------------------------------------------------- #

FENCE_RE = re.compile(r"^(```|~~~)")
UI_NOISE = {
    "neste artigo",
    "in this article",
    "copiar markdown",
    "copy markdown",
    "skip to main content",
    "skip to content",
    "barra lateral do recolhimento",
    "collapse sidebar",
    "expandir barra lateral",
    "expand sidebar",
    "contribuir",
    "contributing",
    "nesta página",
    "on this page",
    "editar",
    "edit",
    "adicionar feedback",
    "add feedback",
}


def slugify(text: str) -> str:
    """Slug no estilo GitHub (usado para âncoras internas)."""
    text = text.strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^\w\s\-À-ÿ]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", "-", text)
    return text


def normalize_markdown(md: str) -> str:
    """Polimento final: cercas consistentes, sem trailing space, blank lines ≤ 2."""
    lines = md.split("\n")
    out: list[str] = []
    fence_char: str | None = None
    for line in lines:
        stripped = line.rstrip()
        if FENCE_RE.match(stripped.lstrip()) and not stripped.lstrip().startswith("````"):
            token = stripped.lstrip()[0:3]
            if fence_char is None:
                fence_char = "```"
                info = stripped.lstrip()[3:].strip()
                stripped = ("    " * (len(line) - len(line.lstrip()))) + "```" + info
            elif token in ("```", "~~~"):
                indent = len(line) - len(line.lstrip())
                stripped = " " * indent + "```"
                fence_char = None
        if fence_char is None:
            stripped = stripped.rstrip()
        out.append(stripped)
    md = "\n".join(out)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    if not md.endswith("\n"):
        md += "\n"
    return md.strip() + "\n"


def heading_from_link_lines(md: str) -> str:
    """`## [Título](url)` → `## Título` (âncoras de heading do site)."""

    def repl(m: re.Match) -> str:
        hashes, label, target = m.group(1), m.group(2).strip(), m.group(3)
        label = label.replace("\\#", "#").replace("\\|", "|")
        if target.strip().startswith("#") or target.strip().endswith("\\#" + slugify(label)):
            return f"{hashes} {label}"
        return f"{hashes} {label}"

    md = re.sub(r"^(#{1,6})\s+\[([^\]]+)\]\(([^)]*)\)\\?\s*$", repl, md, flags=re.MULTILINE)
    # ancora "cabeça" vazia: "## Título [](url)"
    md = re.sub(r"^(#{1,6}\s+.+?)\s*\[\]\([^)]*\)\s*$", r"\1", md, flags=re.MULTILINE)
    md = re.sub(r"^(#{1,6}\s+.+?)\s*\[¶\]\([^)]*\)\s*$", r"\1", md, flags=re.MULTILINE)
    return md


def blockquotes_to_admonitions(md: str) -> tuple[str, int]:
    """`> **Nota** ...` (renderização de `{% note %}`) → admonição MkDocs."""
    labels = {
        "nota": "note", "note": "note",
        "dica": "tip", "tip": "tip",
        "aviso": "warning", "warning": "warning",
        "atenção": "warning", "atencao": "warning", "caution": "warning",
        "importante": "important", "important": "important",
        "observação": "note", "observacao": "note",
    }
    lines = md.split("\n")
    out: list[str] = []
    count = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^>\s*\*\*(Nota|Note|Dica|Tip|Aviso|Warning|Atenção|Cuidado|Caution|Importante|Important)\*\*:?\s*(.*)$", line)
        if m:
            kind = labels.get(m.group(1).lower(), "note")
            first = m.group(2).strip()
            block: list[str] = []
            if first:
                block.append(first)
            i += 1
            while i < len(lines) and (lines[i].startswith(">") or (lines[i].strip() == "" and i + 1 < len(lines) and lines[i + 1].startswith(">"))):
                if lines[i].startswith(">"):
                    block.append(re.sub(r"^>\s?", "", lines[i]))
                else:
                    block.append("")
                i += 1
            body = normalize_markdown("\n".join(block)).strip()
            out.append(f'!!! {kind}')
            for bl in (body.split("\n") if body else [""]):
                out.append(f"    {bl}".rstrip())
            out.append("")
            count += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out), count


def collapse_escapes(md: str) -> str:
    """Remove escapes excessivos que o pandoc injeta em texto simples."""
    md = re.sub(r"\\([#`])", r"\1", md)
    md = md.replace("\\<", "<").replace("\\>", ">")
    md = re.sub(r"\\(?=[_\[\]])", "", md) if False else md
    return md


# --------------------------------------------------------------------------- #
# MODO SITE — HTML → Markdown (somente conteúdo principal)
# --------------------------------------------------------------------------- #

MAIN_SELECTORS = [
    "main div.markdown-body",
    "div.markdown-body",
    "main article",
    "article",
    "main",
]

REMOVE_TAGS = ["script", "style", "noscript", "nav", "aside", "footer", "header", "form",
               "button", "svg", "iframe", "input", "select", "textarea", "dialog"]

REMOVE_CLASS_RE = re.compile(
    r"(breadcrumb|sidebar|in-this-article|table-of-contents|\btoc\b|edit-this-page|"
    r"page-footer|prev-next|support-feedback|feedback|copy-markdown|heading-link|"
    r"anchor|skip-|nav-|search|banner|survey|contribution|permission|version-picker|"
    r"picker|tabnav|subnav|kbd-nav|announcement)",
    re.I,
)


def absolutize_href(el: Any, base_url: str) -> None:
    href = el.get("href")
    if isinstance(href, str) and href and not href.startswith(("mailto:", "tel:", "javascript:")):
        el["href"] = urllib.parse.urljoin(base_url, href)
    src = el.get("src")
    if isinstance(src, str) and src:
        el["src"] = urllib.parse.urljoin(base_url, src)


def clean_fragment(root: Any, base_url: str = "") -> Any:
    """Remove navegação/ruído e normaliza blocos de código e notas."""
    for tag_name in REMOVE_TAGS:
        for el in root.find_all(tag_name):
            el.decompose()

    for el in list(root.find_all(True)):
        classes = " ".join(el.get("class") or [])
        el_id = el.get("id") or ""
        if REMOVE_CLASS_RE.search(classes) or REMOVE_CLASS_RE.search(el_id):
            el.decompose()
            continue
        txt = el.get_text(" ", strip=True)
        if txt and txt.lower() in UI_NOISE:
            el.decompose()
            continue

    # "Neste artigo" que sobreviveu como heading + lista de links
    for h in root.find_all(re.compile(r"^h[2-6]$")):
        if h.get_text(strip=True).lower().strip(":") in {"neste artigo", "in this article", "nesta página", "on this page"}:
            nxt = h.find_next_sibling()
            h.decompose()
            if nxt is not None and nxt.name in ("ul", "ol", "nav", "div"):
                nxt.decompose()

    # Âncoras de heading (<a class="heading-link"> / href="#...")
    for h in root.find_all(re.compile(r"^h[1-6]$")):
        for a in h.find_all("a"):
            href = a.get("href") or ""
            if str(href).startswith("#") or not a.get_text(strip=True):
                a.unwrap()

    # Blocos de código: GitHub usa data-snippet-clipboard-copy (texto exato)
    for div in root.find_all("div", attrs={"data-snippet-clipboard-copy": True}):
        code_text = div["data-snippet-clipboard-copy"]
        lang = ""
        inner = div.find("div", class_=re.compile(r"highlight-(\w+)"))
        if inner:
            m = re.search(r"highlight-([\w+-]+)", " ".join(inner.get("class") or []))
            if m:
                lang = m.group(1)
        new = root.new_tag("pre") if hasattr(root, "new_tag") else None
        if new is None:
            continue
        code = root.new_tag("code")
        if lang:
            code["class"] = [f"language-{lang}"]
        code.string = code_text
        new.append(code)
        div.replace_with(new)

    # Blocos highlight sem clipboard-copy
    for div in root.find_all("div", class_=re.compile(r"highlight-[\w+-]+")):
        classes = " ".join(div.get("class") or [])
        m = re.search(r"highlight-([\w+-]+)", classes)
        lang = m.group(1) if m else ""
        pre = div.find("pre")
        if pre is None:
            continue
        code = pre.find("code") or pre
        text = code.get_text()
        new_pre = root.new_tag("pre")
        new_code = root.new_tag("code")
        if lang:
            new_code["class"] = [f"language-{lang}"]
        new_code.string = text
        new_pre.append(new_code)
        div.replace_with(new_pre)

    # Notas/dicas/avisos → blockquote rotulado (vira admonição no pós-processamento)
    for div in root.find_all("div", class_=re.compile(r"^(note|tip|warning|caution|important)$")):
        kind = (div.get("class") or ["note"])[0]
        label = {"note": "Nota", "tip": "Dica", "warning": "Aviso", "caution": "Atenção", "important": "Importante"}.get(kind, "Nota")
        for t in div.find_all(class_=re.compile(r"title")):
            t.decompose()
        bq = root.new_tag("blockquote")
        p = root.new_tag("p")
        strong = root.new_tag("strong")
        strong.string = label
        p.append(strong)
        bq.append(p)
        for child in list(div.children):
            bq.append(child.extract() if hasattr(child, "extract") else child)
        div.replace_with(bq)

    # Links absolutos
    if base_url:
        for a in root.find_all("a"):
            absolutize_href(a, base_url)
        for img in root.find_all("img"):
            absolutize_href(img, base_url)

    return root


def html_to_fragment(page_html: str, base_url: str) -> tuple[Any, str, list[str]]:
    """Retorna (fragmento limpo, seletor usado, avisos)."""
    warnings: list[str] = []
    soup = BeautifulSoup(page_html, "lxml")
    chosen, selector = None, ""
    for sel in MAIN_SELECTORS:
        cand = soup.select_one(sel)
        if cand is not None and len(cand.get_text(strip=True)) > 200:
            chosen, selector = cand, sel
            break
    if chosen is None:
        chosen = soup.select_one("main") or soup.body or soup
        selector = "fallback:main/body"
        warnings.append("seletor principal não encontrado; usado fallback")

    # remove elementos fora do artigo, se o seletor foi amplo
    for el in chosen.find_all(["nav", "aside", "footer"]):
        el.decompose()

    clean_fragment(chosen, base_url)
    return chosen, selector, warnings


def pandoc_html_to_gfm(fragment_html: str) -> str:
    """Converte HTML → GFM usando pandoc (pypandoc, pandoc no PATH ou markdownify)."""
    try:
        import pypandoc  # type: ignore
        return pypandoc.convert_text(
            fragment_html, "gfm-raw_html", format="html",
            extra_args=["--wrap=none"],
        )
    except Exception:
        pass
    from shutil import which
    if which("pandoc"):
        import subprocess
        proc = subprocess.run(
            ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
            input=fragment_html.encode("utf-8"), capture_output=True,
        )
        if proc.returncode == 0:
            return proc.stdout.decode("utf-8", "replace")
    from markdownify import markdownify as mdify  # type: ignore
    return mdify(fragment_html, heading_style="ATX", bullets="-", strip=["svg"])


def url_to_relpath(url: str, lang: str, scope: str = "actions") -> str:
    """https://docs.github.com/pt/actions/a/b → actions/a/b.md"""
    parsed = urllib.parse.urlparse(url)
    return normalize_docs_path(parsed.path, lang, scope) or "index.md"


def normalize_docs_path(path: str, lang: str, scope: str) -> str | None:
    """`/pt/actions/a/b`, `/actions/a/b`, `actions/a/b.md` → `actions/a/b.md` (ou None se fora do escopo)."""
    path = path.strip().split("#")[0].split("?")[0].strip("/")
    if path.startswith(f"{lang}/"):
        path = path[len(lang) + 1:]
    if path.startswith("en/") and lang != "en":
        path = path[3:]
    if not (path == scope or path.startswith(f"{scope}/")):
        return None
    if path == scope:
        return "index.md"
    path = re.sub(r"\.md$", "", path)
    if path.endswith("/index"):
        path = path[: -len("/index")]
    return path + ".md"


def rewrite_links(md: str, current_rel: str, lang: str, stats: dict[str, int], scope: str = "actions") -> str:
    """Converte links internos do docs em links relativos do knowledge base."""

    def repl(m: re.Match) -> str:
        label, target = m.group(1), m.group(2)
        if target.startswith(("mailto:", "#", "<")):
            return m.group(0)
        parsed = urllib.parse.urlparse(target)
        frag = ("#" + parsed.fragment) if parsed.fragment else ""
        if parsed.netloc and parsed.netloc != "docs.github.com":
            stats["external"] += 1
            return m.group(0)
        rel_target = normalize_docs_path(parsed.path, lang, scope)
        if rel_target is None:
            # documentação fora do escopo Actions → mantém URL absoluta do site
            stats["external"] += 1
            clean_path = parsed.path.strip("/")
            if parsed.netloc:
                return f"[{label}]({DOCS_HOST}/{clean_path}{frag})"
            return f"[{label}]({DOCS_HOST}/{clean_path}{frag})"
        rel = os.path.relpath(rel_target, start=str(Path(current_rel).parent)).replace(os.sep, "/")
        stats["internal"] += 1
        return f"[{label}]({rel}{frag})"

    return re.sub(r"(?<!\!)\[([^\]]*)\]\(([^)\s]+)\)", repl, md)


def title_from_fragment(fragment: Any, soup_title: str) -> tuple[str, str]:
    h1 = fragment.find("h1")
    if h1 is not None:
        return h1.get_text(" ", strip=True), ""
    return soup_title or "Sem título", ""


def extract_site_page(url: str, lang: str, out_dir: Path, results_root: Path) -> PageResult:
    res = PageResult(url=url, lang=lang, source="site")
    html_text = http_get_text(url, accept="text/html")
    soup = BeautifulSoup(html_text, "lxml")
    page_title = soup.title.get_text(strip=True) if soup.title else ""
    page_title = re.sub(r"\s*[-–]\s*(Documentos do GitHub|GitHub Docs).*$", "", page_title).strip()

    fragment, selector, warnings = html_to_fragment(html_text, url)
    res.selector = selector
    res.warnings.extend(warnings)

    title, _ = title_from_fragment(fragment, page_title)
    res.title = title or page_title

    frag_html = str(fragment)
    md = pandoc_html_to_gfm(frag_html)

    md = heading_from_link_lines(md)
    md = collapse_escapes(md)
    md, admon_count = blockquotes_to_admonitions(md)

    # remove o H1 duplicado se pandoc o emitiu; garantimos H1 único no cabeçalho
    lines = md.split("\n")
    body_lines: list[str] = []
    seen_h1 = False
    for line in lines:
        if re.match(r"^#\s+", line):
            if seen_h1:
                continue
            seen_h1 = True
            continue  # o H1 vem do frontmatter/cabeçalho gerado
        body_lines.append(line)
    body = normalize_markdown("\n".join(body_lines))

    # descrição = primeiro parágrafo real
    desc = ""
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if p and not p.startswith(("#", "|", "```", "!!!", "![", "-", "*", ">")):
            desc = re.sub(r"\s+", " ", re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p))[:300]
            break

    rel = url_to_relpath(url, lang)
    stats = {"internal": 0, "external": 0}
    body = rewrite_links(body, rel, lang, stats, "actions")
    res.links_internal = stats["internal"]
    res.links_external = stats["external"]

    section = " / ".join(seg.replace("-", " ").capitalize() for seg in Path(rel).parent.parts if seg not in ("actions",))
    res.section = section

    fm = {
        "title": res.title,
        "description": desc,
        "source": url,
        "lang": "pt-BR" if lang == "pt" else lang,
        "captured": TODAY,
        "section": section,
    }
    header = yaml_front_matter(fm)
    content = f"{header}\n# {res.title}\n\n"
    if desc:
        content += f"_{desc}_\n\n"
    content += body

    dest = results_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")

    res.path = rel
    res.description = desc
    res.bytes = len(content.encode("utf-8"))
    res.headings = len(re.findall(r"^#{1,6}\s", content, flags=re.M))
    res.h2 = len(re.findall(r"^##\s", content, flags=re.M))
    res.code_blocks = content.count("```") // 2
    res.tables = len(re.findall(r"^\|.*\|\s*$\n^\|[-: |]+\|\s*$", content, flags=re.M))
    res.admonitions = admon_count
    res.images = len(re.findall(r"!\[[^\]]*\]\(", content))
    if res.bytes < 500:
        res.warnings.append("conteúdo suspiciousamente curto")
    if res.headings < 2:
        res.warnings.append("poucos headings (verificar extração)")
    return res


def yaml_front_matter(data: dict[str, Any]) -> str:
    if yaml is None:
        body = "\n".join(f'{k}: "{v}"' for k, v in data.items() if v not in (None, "", []))
        return f"---\n{body}\n---\n"
    text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False).strip()
    return f"---\n{text}\n---\n"


def discover_site_urls(lang: str, scope: str = "actions", limit: int = 0,
                       version: str = "free-pro-team@latest") -> list[str]:
    """Inventário canônico de páginas.

    Ordem de preferência:
      1. ``GET /api/pagelist/<lang>/<version>``  — permalinks canônicos do próprio site;
      2. ``sitemap.xml``                          — filtrado e saneado;
      3. árvore ``content/<scope>`` do repo ``github/docs`` — fallback offline-ish.
    """
    paths: list[str] = []
    warnings: list[str] = []

    # 1) API pagelist
    try:
        raw = http_get_text(f"{DOCS_HOST}/api/pagelist/{lang}/{version}", timeout=120)
        if raw.strip().startswith("<") or raw.strip().startswith("{"):
            raise RuntimeError("resposta inesperada do /api/pagelist")
        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue
            if line == f"/{lang}/{scope}" or line.startswith(f"/{lang}/{scope}/"):
                paths.append(line.rstrip("/"))
        paths = sorted(dict.fromkeys(paths))
    except Exception as exc:
        warnings.append(f"pagelist indisponível ({exc})")

    # 2) sitemap
    if len(paths) < 5:
        try:
            sm = http_get_text(f"{DOCS_HOST}/sitemap.xml", timeout=180)
            urls = re.findall(r"<loc>(.*?)</loc>", sm)
            extra = []
            for u in urls:
                parsed = urllib.parse.urlparse(u)
                if parsed.netloc != "docs.github.com":
                    continue
                seg = parsed.path.strip("/").split("/")
                if len(seg) >= 2 and seg[0] == lang and seg[1] == scope:
                    if any(part.startswith("-") for part in seg):
                        continue  # alias legado (404)
                    extra.append(parsed.path.rstrip("/"))
            merged = sorted(dict.fromkeys(paths + extra))
            if merged:
                paths = merged
        except Exception as exc:
            warnings.append(f"sitemap indisponível ({exc})")

    # 3) árvore do repositório github/docs
    if len(paths) < 5:
        try:
            data = json.loads(http_get_text(
                f"https://api.github.com/repos/github/docs/git/trees/main:content/{scope}?recursive=1",
                accept="application/vnd.github+json"))
            for item in data.get("tree", []):
                pth = item["path"]
                if item["type"] != "blob" or not pth.endswith(".md"):
                    continue
                pth = re.sub(r"\.md$", "", pth[len(f"content/{scope}/"):])
                if pth == "index":
                    paths.append(f"/{lang}/{scope}")
                else:
                    paths.append(f"/{lang}/{scope}/" + re.sub(r"/index$", "", pth))
            paths = sorted(dict.fromkeys(paths))
        except Exception as exc:
            warnings.append(f"árvore do repositório indisponível ({exc})")

    for w in warnings:
        print(f"[warn] {w}", file=sys.stderr)
    print(f"[info] inventário: {len(paths)} páginas /{lang}/{scope} (version={version})", file=sys.stderr)
    return paths[:limit] if limit else paths


def extract_api_page(pathname: str, lang: str, scope: str, results_root: Path,
                     version: str = "free-pro-team@latest") -> PageResult:
    """Captura SOMENTE o conteúdo principal via Article API oficial do docs.github.com.

    ``GET /api/article?pathname=<path>`` → ``{"meta": {...}, "body": "<markdown>"}``
    (sem navegação, sidebar, breadcrumbs, TOC ou rodapé).
    """
    url = f"{DOCS_HOST}{pathname}"
    res = PageResult(url=url, lang=lang, source="api", selector="api:/api/article")
    api_url = f"{DOCS_HOST}/api/article?pathname={urllib.parse.quote(pathname, safe='/')}"
    try:
        payload = json.loads(http_get_text(api_url, accept="application/json"))
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            res.status = "skipped"
            res.error = "404 (página inexistente para este idioma/plano)"
            return res
        raise
    meta = payload.get("meta") or {}
    body = payload.get("body") or ""
    if payload.get("redirectedFrom"):
        res.warnings.append(f"redirecionado de {payload['redirectedFrom']}")
    title = str(meta.get("title") or "").strip()
    intro = re.sub(r"\s+", " ", str(meta.get("intro") or "").strip())
    res.title = title or pathname.rsplit("/", 1)[-1]
    res.short_title = str(meta.get("shortTitle") or "")
    res.description = intro[:300]

    rel = normalize_docs_path(pathname, lang, scope) or "index.md"
    res.path = rel
    res.section = str(meta.get("product") or "") or " / ".join(
        x.replace("-", " ").capitalize() for x in Path(rel).parent.parts if x != scope) or scope.capitalize()

    stats = {"internal": 0, "external": 0}
    body = heading_from_link_lines(body)
    body = collapse_escapes(body)
    body, adm = blockquotes_to_admonitions(body)
    body = rewrite_links(body, rel, lang, stats, scope)
    body = normalize_markdown(body)
    res.links_internal = stats["internal"]
    res.links_external = stats["external"]
    res.admonitions = adm + body.count("!!! ")

    fm = {
        "title": res.title,
        "description": res.description,
        "product": str(meta.get("product") or ""),
        "documentType": str(meta.get("documentType") or "article"),
        "lang": {"pt": "pt-BR"}.get(lang, lang),
        "plan": version,
        "source": url,
        "captured": TODAY,
        "section": res.section,
    }
    content = yaml_front_matter({k: v for k, v in fm.items() if v}) + f"\n# {res.title}\n\n"
    if intro:
        content += f"_{intro}_\n\n"
    content += body

    dest = results_root / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")

    res.bytes = len(content.encode("utf-8"))
    res.headings = len(re.findall(r"^#{1,6}\s", content, flags=re.M))
    res.h2 = len(re.findall(r"^##\s", content, flags=re.M))
    res.code_blocks = len(re.findall(r"^```", content, flags=re.M)) // 2
    res.tables = len(re.findall(r"^\|.*\|\s*$\n^\|[-: |]+\|\s*$", content, flags=re.M))
    res.images = len(re.findall(r"!\[[^\]]*\]\(", content))
    if res.bytes < 400:
        res.warnings.append("conteúdo curto")
    if res.headings < 2:
        res.warnings.append("poucos headings")
    if re.search(r"\{%-?\s*(data|ifversion|note|tip|warning)", body):
        res.warnings.append("liquid residual")
    return res


# --------------------------------------------------------------------------- #
# MODO REPO — github/docs (frontmatter + Liquid) → Markdown
# --------------------------------------------------------------------------- #

TAG_RE = re.compile(r"\{%-?\s*([A-Za-z_][\w]*)\s*([^%]*?)\s*-?%\}")

# tags cujo conteúdo vira bloco de código cercado
CODE_TAB_TAGS = {
    "bash": "bash", "shell": "shell", "powershell": "powershell", "pwsh": "powershell",
    "javascript": "javascript", "js": "javascript", "json": "json", "yaml": "yaml",
    "yml": "yaml", "http": "http", "groovy": "groovy", "java": "java", "csharp": "csharp",
    "go": "go", "python": "python", "ruby": "ruby", "dockerfile": "dockerfile",
    "sql": "sql", "text": "text", "ini": "ini", "toml": "toml", "hcl": "hcl",
}
# tags "transparentes": mantém o conteúdo, descarta o marcador
LABEL_TAB_TAGS = {
    "cli": "**Usando a CLI do GitHub**",
    "webui": "**Usando a interface do GitHub**",
    "linux": "**Linux**",
    "mac": "**macOS**",
    "macos": "**macOS**",
    "windows": "**Windows**",
}
DROP_TAGS = {
    "comment", "endcomment", "raw", "endraw", "capture", "endcapture", "rowheaders",
    "endrowheaders", "row", "endrow", "column", "endcolumn", "octicon", "include",
    "highlight", "endhighlight", "api", "rest", "release", "defaultTab", "tab", "endtab",
    "endif", "else", "elsif", "unless", "endunless", "assign", "echo", "version",
}
ADMONITION_TAGS = {"note": "note", "tip": "tip", "warning": "warning", "caution": "warning", "important": "important"}
DATA_TAG_RE = re.compile(r"^data$")
INDENTED_TAG_RE = re.compile(r"^indented_data_reference$")
AUTOTITLE_RE = re.compile(r"\[AUTOTITLE\]\(([^)\s]+)\)")
PLAN_PRIORITY = ["fpt", "ghec", "ghes"]


class LiquidResolver:
    """Resolve os costrutores Liquid usados pelo repositório `github/docs`.

    Estratégia de versão (`--version-profile`):
      * ``auto``    – avalia `{% ifversion %}` para o plano da página (frontmatter
                      `versions:`), reproduzindo o que o site renderiza;
      * ``fpt``     – força GitHub.com (fpt);
      * ``flatten`` – mantém todos os ramos (útil para auditoria de conteúdo).
    """

    def __init__(self, repo_dir: Path, version_profile: str = "auto"):
        self.repo_dir = repo_dir
        self.version_profile = version_profile
        self._variables: dict[str, Any] = {}
        self.missing: list[str] = []
        self.unknown_tags: dict[str, int] = {}

    # ------------------------------------------------------------------ dados
    def variable(self, dotted: str) -> str:
        parts = [p for p in dotted.split() if p]
        if not parts:
            return ""
        dotted = parts[0]
        parts = dotted.split(".")
        kind = parts[0] if parts[0] in ("variables", "reusables") else "variables"
        rest = parts[1:] if kind in ("variables", "reusables") else parts
        if kind == "variables":
            if not rest:
                return ""
            file_name, key_path = rest[0], rest[1:]
            if file_name not in self._variables:
                path = self.repo_dir / "data" / "variables" / f"{file_name}.yml"
                try:
                    self._variables[file_name] = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
                except Exception:
                    self._variables[file_name] = {}
            node: Any = self._variables[file_name]
            for k in key_path:
                if isinstance(node, dict) and k in node:
                    node = node[k]
                else:
                    self.missing.append(dotted)
                    return ""
            if isinstance(node, dict):
                return str(node.get("value", ""))
            return "" if node is None else str(node)
        rel = "/".join(rest)
        path = self.repo_dir / "data" / "reusables" / f"{rel}.md"
        if not path.exists():
            self.missing.append(dotted)
            return ""
        return path.read_text(encoding="utf-8").strip()

    # --------------------------------------------------------------- versões
    @staticmethod
    def plan_from_frontmatter(fm: dict[str, Any]) -> str:
        versions = fm.get("versions") or {}
        if isinstance(versions, str):
            return "fpt"
        for plan in PLAN_PRIORITY:
            if plan in versions:
                return plan
        return next(iter(versions), "fpt") if versions else "fpt"

    def version_true(self, condition: str, plan: str) -> bool:
        condition = condition.strip()
        if not condition:
            return True
        if self.version_profile == "flatten":
            return True
        # "or" tem precedência menor que "and"
        for or_part in re.split(r"\s+or\s+", condition):
            value = True
            for term in re.split(r"\s+and\s+", or_part.strip()):
                value = value and self._term_true(term.strip(), plan)
            if value:
                return True
        return False

    def _term_true(self, term: str, plan: str) -> bool:
        neg = False
        while term.startswith("not "):
            neg = not neg
            term = term[4:].strip()
        token = re.split(r"[<>=!]+", term)[0].strip()
        m = re.match(r"^(fpt|ghec|ghes|ghae)(?:\s*([<>=!]+)\s*([\d.]+))?$", term.strip())
        if m:
            base, op, ver = m.group(1), m.group(2), m.group(3)
            result = base == plan
            if result and op and base == "ghes" and ver:
                result = self._cmp_version(plan_version="3.99", op=op, other=ver)
        else:
            result = token == plan
        return (not result) if neg else result

    @staticmethod
    def _cmp_version(plan_version: str, op: str, other: str) -> bool:
        def tup(v: str) -> tuple[int, ...]:
            return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) or (0,)
        a, b = tup(plan_version), tup(other)
        if op == ">":
            return a > b
        if op == ">=":
            return a >= b
        if op == "<":
            return a < b
        if op == "<=":
            return a <= b
        return a == b

    # ---------------------------------------------------------------- blocos
    #: tag de fechamento de blocos cujo nome não segue o padrão `end<name>`
    CLOSE_TAG_MAP = {"ifversion": "endif", "unless": "endunless", "if": "endif", "case": "endcase"}

    @classmethod
    def _scan_block(cls, text: str, start: int, name: str) -> tuple[str, int]:
        """Retorna (conteúdo interno, índice logo após a tag de fechamento), tratando aninhamento."""
        depth = 1
        pos = start
        close_name = cls.CLOSE_TAG_MAP.get(name.lower(), "end" + name)
        open_re = re.compile(r"\{%-?\s*" + re.escape(name) + r"\b[^%]*?-?%\}")
        close_re = re.compile(r"\{%-?\s*" + re.escape(close_name) + r"\s*-?%\}")
        while pos < len(text):
            next_open = open_re.search(text, pos)
            next_close = close_re.search(text, pos)
            if next_close is None:
                break
            if next_open is not None and next_open.start() < next_close.start():
                depth += 1
                pos = next_open.end()
                continue
            depth -= 1
            pos = next_close.end()
            if depth == 0:
                return text[start:next_close.start()], pos
        return text[start:], len(text)

    @classmethod
    def _split_branches(cls, block: str) -> list[tuple[str | None, str]]:
        """Divide um bloco em ramos [(condição|None para else, corpo)] respeitando aninhamento."""
        branches: list[tuple[str | None, str]] = []
        current_cond: str | None = None
        buf: list[str] = []
        pos = 0
        marker = re.compile(r"\{%-?\s*(elsif\s+[^%]*?|else)\s*-?%\}")
        while pos < len(block):
            m = marker.search(block, pos)
            if m is None:
                buf.append(block[pos:])
                break
            # ignora marcadores aninhados dentro de ifversion internos
            nested_open = re.compile(r"\{%-?\s*ifversion\b").search(block, pos)
            if nested_open and nested_open.start() < m.start():
                _, after = cls._scan_block(block, nested_open.end(), "ifversion")
                buf.append(block[pos:after])
                pos = after
                continue
            buf.append(block[pos:m.start()])
            branches.append((current_cond, "".join(buf)))
            buf = []
            if m.group(1).strip() == "else":
                current_cond = None
            else:
                current_cond = m.group(1).strip()[len("elsif"):].strip()
            pos = m.end()
        branches.append((current_cond, "".join(buf)))
        return branches

    # ------------------------------------------------------------ conversão
    def resolve(self, text: str, plan: str = "fpt", depth: int = 0) -> str:
        if depth > 12:
            return text
        out: list[str] = []
        i = 0
        while i < len(text):
            m = TAG_RE.search(text, i)
            if m is None:
                out.append(text[i:])
                break
            out.append(text[i:m.start()])
            tag, args = m.group(1), (m.group(2) or "").strip()
            low = tag.lower()

            if low == "raw":
                block, i = self._scan_block(text, m.end(), tag)
                out.append(block)
                continue
            if low == "ifversion":
                block, i = self._scan_block(text, m.end(), tag)
                branches = self._split_branches(block)
                chosen = ""
                if self.version_profile == "flatten":
                    chosen = "\n\n".join(b.strip() for _, b in branches if b.strip())
                else:
                    fallback = ""
                    for cond, body in branches:
                        if cond is None:
                            fallback = body
                        elif self.version_true(cond, plan):
                            chosen = body
                            break
                    chosen = chosen or fallback
                out.append(self.resolve(chosen, plan, depth + 1))
                continue
            if low == "unless":
                block, i = self._scan_block(text, m.end(), tag)
                keep = not self.version_true(args, plan)
                out.append(self.resolve(block, plan, depth + 1) if keep else "")
                continue
            if low in ADMONITION_TAGS:
                block, i = self._scan_block(text, m.end(), tag)
                body = self.resolve(block, plan, depth + 1).strip()
                indented = "\n".join(("    " + ln).rstrip() if ln.strip() else "" for ln in body.split("\n"))
                out.append(f"\n\n!!! {ADMONITION_TAGS[low]}\n{indented}\n\n")
                continue
            if low in CODE_TAB_TAGS:
                block, i = self._scan_block(text, m.end(), tag)
                body = self.resolve(block, plan, depth + 1).strip()
                if body:
                    out.append(f"\n\n```{CODE_TAB_TAGS[low]}\n{body}\n```\n\n")
                continue
            if low in LABEL_TAB_TAGS:
                block, i = self._scan_block(text, m.end(), tag)
                body = self.resolve(block, plan, depth + 1).strip()
                if body:
                    out.append(f"\n\n{LABEL_TAB_TAGS[low]}\n\n{body}\n\n")
                continue
            if DATA_TAG_RE.match(low):
                value = self.variable(args)
                out.append(self.resolve(value, plan, depth + 1) if value else "")
                i = m.end()
                continue
            if INDENTED_TAG_RE.match(low):
                parts = args.split()
                dotted = parts[0] if parts else ""
                spaces = 0
                for tok in parts[1:]:
                    if tok.startswith("spaces="):
                        spaces = int(tok.split("=", 1)[1] or 0)
                value = self.resolve(self.variable(dotted), plan, depth + 1)
                pad = " " * spaces
                out.append("\n".join((pad + ln).rstrip() if ln.strip() else ln for ln in value.split("\n")))
                i = m.end()
                continue
            if low in DROP_TAGS or low.startswith(("end",)):
                i = m.end()
                continue
            # tag desconhecida → descarta e registra
            self.unknown_tags[tag] = self.unknown_tags.get(tag, 0) + 1
            i = m.end()
        return "".join(out)


def resolve_autotitles(text: str, title_map: dict[str, str]) -> str:
    """Substitui `[AUTOTITLE](/caminho)` pelo título real da página de destino."""

    def repl(m: re.Match) -> str:
        target = m.group(1)
        parsed = urllib.parse.urlparse(target)
        frag = ("#" + parsed.fragment) if parsed.fragment else ""
        path = parsed.path.strip("/")
        path = re.sub(r"^(en|pt|free-pro-team@latest|enterprise-server@[^/]+|enterprise-cloud@[^/]+)/", "", path)
        rel = normalize_docs_path(path, "", "actions")
        title = title_map.get(rel or "") if rel else None
        if not title:
            guess = (rel or path).replace(".md", "").rstrip("/").split("/")[-1]
            title = re.sub(r"[-_]+", " ", guess).strip().capitalize() or path
        if rel:
            return f"[{title}]({target}{frag})"
        return f"[{title}]({target}{frag})"

    return AUTOTITLE_RE.sub(repl, text)


def extract_repo_tree(repo_dir: Path, scope: str, out_root: Path, version_profile: str) -> list[PageResult]:
    """Converte `content/<scope>/**.md` do repositório github/docs em Markdown limpo (2 passadas)."""
    if yaml is None:
        raise SystemExit("PyYAML é obrigatório no modo repo: pip install pyyaml")
    resolver = LiquidResolver(repo_dir, version_profile)
    content_root = repo_dir / "content" / scope
    md_files = sorted(content_root.rglob("*.md"))

    # ---------------- passada 1: frontmatter + Liquid ---------------- #
    staged: list[tuple[Path, str, dict[str, Any], str, str, str]] = []
    results: list[PageResult] = []
    for src in md_files:
        rel = src.relative_to(content_root)
        out_rel = str(Path(scope) / rel).replace(os.sep, "/")
        res = PageResult(source="repo", lang="en", path=out_rel,
                         url=f"https://github.com/github/docs/blob/main/content/{scope}/{rel.as_posix()}")
        try:
            raw = src.read_text(encoding="utf-8")
            fm: dict[str, Any] = {}
            body = raw
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3:
                    try:
                        fm = yaml.safe_load(parts[1]) or {}
                    except Exception as exc:
                        res.warnings.append(f"frontmatter inválido: {exc}")
                        fm = {}
                    body = parts[2]
            plan = resolver.plan_from_frontmatter(fm)
            title = resolver.resolve(str(fm.get("title") or rel.stem), plan).strip()
            short = resolver.resolve(str(fm.get("shortTitle") or ""), plan).strip()
            intro = resolver.resolve(str(fm.get("intro") or ""), plan).strip()
            body = resolver.resolve(body, plan)
            res.title = title
            res.short_title = short
            res.description = intro[:300]
            res.section = " / ".join(x.replace("-", " ").capitalize() for x in rel.parent.parts) or scope.capitalize()
            staged.append((src, out_rel, fm, title, intro, body))
            results.append(res)
            res_by_path = res
        except Exception as exc:
            res.status = "error"
            res.error = f"{type(exc).__name__}: {exc}"
            results.append(res)

    # ---------------- passada 2: AUTOTITLE + links + escrita ---------------- #
    title_map = {out_rel: title for _, out_rel, _, title, _, _ in staged}
    index_by_path = {r.path: r for r in results}
    for src, out_rel, fm, title, intro, body in staged:
        res = index_by_path[out_rel]
        try:
            rel = src.relative_to(content_root)
            title = resolve_autotitles(title, title_map)
            intro = resolve_autotitles(intro, title_map)
            body = resolve_autotitles(body, title_map)
            stats = {"internal": 0, "external": 0}
            body = rewrite_links(body, out_rel, "en", stats, scope)
            body = normalize_markdown(body)
            body, _adm = blockquotes_to_admonitions(body)

            content_md = (
                yaml_front_matter({
                    "title": title,
                    "description": re.sub(r"\s+", " ", intro)[:300],
                    "lang": "en",
                    "plan": resolver.plan_from_frontmatter(fm),
                    "source": res.url,
                    "captured": TODAY,
                    "section": res.section,
                })
                + f"\n# {title}\n\n"
            )
            if intro:
                content_md += f"_{re.sub(chr(10) + '+', ' ', intro)}_\n\n"
            content_md += body

            dest = out_root / out_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content_md, encoding="utf-8")

            res.title = title
            res.bytes = len(content_md.encode("utf-8"))
            res.headings = len(re.findall(r"^#{1,6}\s", content_md, flags=re.M))
            res.h2 = len(re.findall(r"^##\s", content_md, flags=re.M))
            res.code_blocks = content_md.count("```") // 2
            res.tables = len(re.findall(r"^\|.*\|\s*$\n^\|[-: |]+\|\s*$", content_md, flags=re.M))
            res.images = len(re.findall(r"!\[[^\]]*\]\(", content_md))
            res.links_internal = stats["internal"]
            res.links_external = stats["external"]
            res.children = [str(c) for c in (fm.get("children") or [])]
            if re.search(r"\{%-?\s*[A-Za-z_]", body):
                res.warnings.append("liquid residual")
            if "AUTOTITLE" in body:
                res.warnings.append("AUTOTITLE não resolvido")
        except Exception as exc:
            res.status = "error"
            res.error = f"{type(exc).__name__}: {exc}"

    if resolver.missing:
        uniq = sorted(set(resolver.missing))
        print(f"[warn] {len(uniq)} referências de dados ausentes no checkout (amostra): {uniq[:6]}", file=sys.stderr)
    if resolver.unknown_tags:
        print(f"[warn] tags Liquid desconhecidas descartadas: {dict(sorted(resolver.unknown_tags.items(), key=lambda x: -x[1])[:10])}", file=sys.stderr)
    return results


# --------------------------------------------------------------------------- #
# Manifesto + relatório
# --------------------------------------------------------------------------- #


def write_manifest(results: list[PageResult], dest: Path, meta: dict[str, Any]) -> None:
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": meta.get("source"),
        "lang": meta.get("lang"),
        "page_count": len([r for r in results if r.status == "ok"]),
        "total_bytes": sum(r.bytes for r in results),
        "pages": [asdict(r) for r in results],
        **{k: v for k, v in meta.items() if k not in ("source", "lang")},
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_report(results: list[PageResult], dest: Path, meta: dict[str, Any]) -> None:
    ok = [r for r in results if r.status == "ok"]
    bad = [r for r in results if r.status != "ok"]
    warn = [r for r in ok if r.warnings]
    lines = [
        "# Relatório de extração",
        "",
        f"- **Fonte:** `{meta.get('source')}`  ",
        f"- **Idioma:** `{meta.get('lang')}`  ",
        f"- **Executado em:** {dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')}  ",
        f"- **Páginas OK:** {len(ok)}  ",
        f"- **Falhas:** {len(bad)}  ",
        f"- **Com avisos:** {len(warn)}  ",
        f"- **Bytes totais:** {sum(r.bytes for r in results):,}  ",
        f"- **Headings totais:** {sum(r.headings for r in results):,}  ",
        f"- **Blocos de código:** {sum(r.code_blocks for r in results):,}  ",
        f"- **Tabelas:** {sum(r.tables for r in results):,}  ",
        "",
        "## Seletor de conteúdo principal",
        "",
    ]
    sel_count: dict[str, int] = {}
    for r in ok:
        sel_count[r.selector or "-"] = sel_count.get(r.selector or "-", 0) + 1
    for k, v in sorted(sel_count.items(), key=lambda x: -x[1]):
        lines.append(f"- `{k}`: {v} página(s)")
    lines += ["", "## Páginas com aviso", "", "| Página | Avisos | Bytes |", "| --- | --- | --- |"]
    for r in warn[:80]:
        lines.append(f"| `{r.path}` | {'; '.join(r.warnings)} | {r.bytes:,} |")
    if bad:
        lines += ["", "## Falhas", "", "| URL | Erro |", "| --- | --- |"]
        for r in bad[:80]:
            lines.append(f"| {r.url} | `{r.error[:160]}` |")
    lines += ["", "## Amostra (10 primeiras páginas)", "", "| Página | Título | H | Code | Tabelas | Bytes |", "| --- | --- | --- | --- | --- | --- |"]
    for r in ok[:10]:
        lines.append(f"| `{r.path}` | {r.title[:60]} | {r.headings} | {r.code_blocks} | {r.tables} | {r.bytes:,} |")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Extrator da documentação do GitHub Actions → Markdown MkDocs-ready")
    ap.add_argument("--source", choices=["api", "site", "html", "repo"], default="api",
                    help="api = Article API oficial (markdown do artigo); html = scraping do HTML; repo = github/docs")
    ap.add_argument("--lang", default="pt", help="idioma do site (pt|en|es|...)")
    ap.add_argument("--scope", default="actions")
    ap.add_argument("--out", required=True, help="diretório de destino (raiz do idioma)")
    ap.add_argument("--repo-dir", default="", help="checkout do github/docs (modo repo)")
    ap.add_argument("--limit", type=int, default=0, help="capturar apenas N páginas (smoke test)")
    ap.add_argument("--jobs", type=int, default=4, help="paralelismo da captura")
    ap.add_argument("--report", default="", help="caminho do relatório markdown")
    ap.add_argument("--manifest", default="", help="caminho do manifest.json")
    ap.add_argument("--version-profile", default="auto", choices=["auto", "flatten", "fpt"])
    ap.add_argument("--plan", default="free-pro-team@latest",
                    help="plano/versão do docs (free-pro-team@latest, enterprise-cloud@latest, enterprise-server@3.x)")
    ap.add_argument("--max-failures", type=int, default=5)
    ap.add_argument("--fail-on-warning", action="store_true")
    args = ap.parse_args(argv)

    out_root = Path(args.out).resolve()
    results_root = out_root
    results: list[PageResult] = []

    if args.source in ("api", "site"):
        paths = discover_site_urls(args.lang, args.scope, args.limit, args.plan)
        print(f"[info] {len(paths)} páginas descobertas para /{args.lang}/{args.scope}", file=sys.stderr)
        started = time.time()

        def work(pathname: str) -> PageResult:
            try:
                return extract_api_page(pathname, args.lang, args.scope, results_root, args.plan)
            except Exception as exc:
                res = PageResult(url=f"{DOCS_HOST}{pathname}", lang=args.lang, source="api", status="error")
                res.error = f"{type(exc).__name__}: {exc}"
                return res

        with cf.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            for idx, res in enumerate(pool.map(work, paths), start=1):
                results.append(res)
                mark = {"ok": "ok ", "skipped": "skip"}[res.status] if res.status in ("ok", "skipped") else "ERR"
                print(f"[{idx:>4}/{len(paths)}] {mark} {res.path or res.url} ({res.bytes} bytes)", file=sys.stderr)
        print(f"[info] captura em {time.time() - started:.1f}s", file=sys.stderr)
    elif args.source == "html":
        repo_dir = Path(args.repo_dir or os.environ.get("GITHUB_DOCS_DIR", "/tmp/ghdocs"))
        if not (repo_dir / "content" / args.scope).exists():
            raise SystemExit(f"repo-dir inválido: {repo_dir} (esperado content/{args.scope})")
        results = extract_repo_tree(repo_dir, args.scope, results_root, args.version_profile)
    else:
        urls = [f"{DOCS_HOST}{p}" for p in discover_site_urls(args.lang, args.scope, args.limit, args.plan)]
        print(f"[info] {len(urls)} URLs descobertas para /{args.lang}/{args.scope}", file=sys.stderr)
        started = time.time()

        def work(url: str) -> PageResult:
            res = PageResult(url=url, lang=args.lang, source="site")
            try:
                return extract_site_page(url, args.lang, out_root, results_root)
            except Exception as exc:
                res.status = "error"
                res.error = f"{type(exc).__name__}: {exc}"
                return res

        with cf.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
            for idx, res in enumerate(pool.map(work, urls), start=1):
                results.append(res)
                mark = "ok " if res.status == "ok" else "ERR"
                print(f"[{idx:>4}/{len(urls)}] {mark} {res.path or res.url} ({res.bytes} bytes)", file=sys.stderr)
        print(f"[info] captura em {time.time() - started:.1f}s", file=sys.stderr)

    meta = {"source": args.source, "lang": args.lang, "scope": args.scope, "out": str(out_root),
            "plan": args.plan}
    manifest_path = Path(args.manifest) if args.manifest else out_root / "manifest.json"
    write_manifest(results, manifest_path, meta)
    if args.report:
        write_report(results, Path(args.report), meta)

    failures = [r for r in results if r.status != "ok"]
    warned = [r for r in results if r.warnings]
    print(f"[done] {len(results) - len(failures)} ok / {len(failures)} falhas / {len(warned)} avisos → {out_root}")
    if len(failures) > args.max_failures:
        return 2
    if args.fail_on_warning and warned:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
