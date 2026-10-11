#!/usr/bin/env python3
"""One-shot diagnostic probe for the docs.github.com extraction pipeline."""
from __future__ import annotations
import re, subprocess, sys, urllib.request, json

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) docs-kb-extractor/1.0"}
URL = "https://docs.github.com/pt/actions/reference/workflows-and-actions/contexts"

def get(url, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace"), r.status

def main():
    out = []
    p = out.append
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        p("FATAL: bs4 missing"); print("\n".join(out)); return
    html, status = get(URL)
    p(f"# Probe report\n\nHTTP {status}, {len(html)} bytes for {URL}\n")
    soup = BeautifulSoup(html, "lxml")
    p(f"TITLE: {soup.title.get_text(strip=True) if soup.title else None}")
    for tag in ("main", "article", "aside", "nav", "footer", "header"):
        els = soup.find_all(tag)
        p(f"{tag}: n={len(els)} -> " + json.dumps([[e.get("id"), e.get("class")] for e in els[:5]], ensure_ascii=False))
    for sel in ("div.markdown-body", "#main-content", "main > div", "h1", "h2", "[data-search-title]"):
        p(f"select '{sel}': n={len(soup.select(sel))}")
    mb = soup.select_one("div.markdown-body")
    p(f"\nmarkdown-body found: {bool(mb)}")
    if mb:
        kids = [(c.name, c.get("id"), c.get("class")) for c in mb.children if getattr(c, "name", None)]
        p("markdown-body first 15 children: " + json.dumps(kids[:15], ensure_ascii=False))
        txt = mb.get_text(" ", strip=True)
        p(f"markdown-body text length: {len(txt)}")
        p(f"markdown-body text head 300: {txt[:300]}")
        p(f"markdown-body text tail 300: {txt[-300:]}")
        h1 = soup.select_one("h1")
        p(f"H1 outside/inside? inside={bool(mb.select_one('h1'))} text={h1.get_text(strip=True) if h1 else None}")
    # code block shapes
    p("\n## Code blocks")
    p(f"div.highlight: {len(soup.select('div.highlight'))}")
    for hl in soup.select("div.highlight")[:3]:
        p("  classes=" + json.dumps(hl.get("class")) + " attrs=" + json.dumps(sorted(hl.attrs.keys())))
    p(f"div[data-snippet-clipboard-copy]: {len(soup.select('div[data-snippet-clipboard-copy]'))}")
    sn = soup.select_one("div[data-snippet-clipboard-copy]")
    if sn:
        p("  sample: " + sn["data-snippet-clipboard-copy"][:150].replace("\n", "\\n"))
    # tables
    p(f"\ntables: {len(soup.select('table'))}")
    tb = soup.select_one("table")
    if tb:
        p("  first table classes=" + json.dumps(tb.get("class")))
    # conversion trials
    frag_target = mb or soup.select_one("main")
    frag = str(frag_target)
    open("/tmp/frag.html", "w", encoding="utf-8").write(frag)
    p("\n## Conversion trials")
    r = subprocess.run(["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none", "-o", "/tmp/pandoc.md", "/tmp/frag.html"], capture_output=True, text=True)
    p(f"pandoc rc={r.returncode} err={r.stderr[:200]}")
    if r.returncode == 0:
        md = open("/tmp/pandoc.md", encoding="utf-8").read()
        p(f"pandoc md bytes={len(md)} fences={md.count('```')} pipes={len([l for l in md.splitlines() if l.startswith('|')])}")
        p("pandoc head 900:\n```markdown\n" + md[:900] + "\n```")
        i = md.find("```yaml")
        p("pandoc yaml fence sample:\n" + (md[i:i+400] if i >= 0 else "NONE"))
    try:
        from markdownify import markdownify as mdify
        m2 = mdify(frag, heading_style="ATX", bullets="-")
        p(f"\nmarkdownify bytes={len(m2)}")
        p("markdownify head 600:\n```markdown\n" + m2[:600] + "\n```")
    except Exception as e:
        p(f"markdownify FAILED: {e}")
    # sitemap
    p("\n## Sitemap")
    try:
        sm, st = get("https://docs.github.com/sitemap.xml", timeout=120)
        urls = re.findall(r"<loc>(.*?)</loc>", sm)
        pt = [u for u in urls if "/pt/actions" in u]
        en = [u for u in urls if "/en/actions" in u]
        p(f"sitemap http={st} total={len(urls)} pt_actions={len(pt)} en_actions={len(en)}")
        for u in pt[:15]:
            p(f"  pt: {u}")
        open("/tmp/pt_urls.txt", "w").write("\n".join(pt))
    except Exception as e:
        p(f"sitemap FAILED: {e}")
        pt = []
    # repo inventory via api.github.com (English source of truth)
    p("\n## github/docs repo inventory (en)")
    try:
        j, _ = get("https://api.github.com/repos/github/docs/git/trees/main:content/actions?recursive=1")
        data = json.loads(j)
        blobs = [t["path"] for t in data.get("tree", []) if t["type"] == "blob"]
        mds = [b for b in blobs if b.endswith(".md")]
        p(f"truncated={data.get('truncated')} blobs={len(blobs)} md={len(mds)}")
        for m in mds[:10]:
            p(f"  {m}")
        open("/tmp/en_paths.txt", "w").write("\n".join(mds))
    except Exception as e:
        p(f"repo inventory FAILED: {e}")
    # compare pt urls vs en paths
    if pt:
        pt_paths = {re.sub(r"^https://docs.github.com/pt/actions/?", "", u).rstrip("/") for u in pt}
        en_paths = {re.sub(r"^.*?content/actions/", "", m)[:-3] for m in open("/tmp/en_paths.txt").read().splitlines()}
        en_paths = {p2 if p2 != "index" else "" for p2 in en_paths}
        p(f"\npt urls={len(pt_paths)} en md={len(en_paths)} only_in_en={len(en_paths - pt_paths)} only_in_pt={len(pt_paths - en_paths)}")
        for x in sorted(en_paths - pt_paths)[:15]:
            p(f"  only_en: {x}")
        for x in sorted(pt_paths - en_paths)[:15]:
            p(f"  only_pt: {x}")
    print("\n".join(out))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback; traceback.print_exc()
