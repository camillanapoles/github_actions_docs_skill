"""Testes offline do extrator (sem rede): polish, quality_score, heal e clean_fragment.

Rodar:  python3 -m pytest tests/ -q
"""
from __future__ import annotations

import pathlib
import re
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

pytest.importorskip("bs4", reason="beautifulsoup4 ausente (pip install -r scripts/requirements.txt)")
pytest.importorskip("markdownify", reason="markdownify ausente")

import extract  # noqa: E402

pandoc_disponivel = True
try:
    import pypandoc  # noqa: F401
    pypandoc.get_pandoc_version()
except Exception:  # pragma: no cover
    pandoc_disponivel = False

requer_pandoc = pytest.mark.skipif(not pandoc_disponivel, reason="pandoc indisponível no ambiente")

LONG_TEXT = "conteúdo suficientemente longo " * 20


# --------------------------------------------------------------------------- #
# polish_markdown
# --------------------------------------------------------------------------- #

@requer_pandoc
def test_html_table_vira_pipe_table():
    md, _ = extract.polish_markdown(
        "<table><thead><tr><th>Contexto</th><th>Disponível</th></tr></thead>"
        "<tbody><tr><td><code>github</code></td><td>sim</td></tr></tbody></table>"
    )
    linhas = [l for l in md.split("\n") if l.strip().startswith("|")]
    assert linhas[0].strip() == "| Contexto | Disponível |"
    assert re.fullmatch(r"\|[\s:-]+\|[\s:-]+\|", linhas[1].strip()), linhas[1]
    assert "`github`" in md
    assert "<table>" not in md


def test_alerta_escapado_vira_admonition():
    md, adm = extract.polish_markdown("> \\[!NOTE\\]\n> Um aviso importante.")
    assert "!!! note" in md
    assert "\\[!NOTE\\]" not in md
    assert adm


def test_celula_multilinha_e_linha_sem_fecho():
    danificado = (
        "| Tipo | Valor |\n"
        "| --- | --- |\n"
        "| booleano |\n"
        "\n"
        "`true` retorna `1`\n"
        "| string | texto |\n"
        "| number | 1\n"
    )
    md, _ = extract.polish_markdown(danificado)
    linhas = [l for l in md.split("\n") if l.strip().startswith("|")]
    celulas = {l.count("|") for l in linhas}
    assert len(celulas) == 1, f"células inconsistentes: {linhas}"


def test_bullets_escapados_no_inicio_da_linha():
    md, _ = extract.polish_markdown("Intro:\n\n    \\* primeiro item\n    \\* segundo item\n")
    assert "\\*" not in md
    assert "- primeiro item" in md or "* primeiro item" in md


# --------------------------------------------------------------------------- #
# quality_score
# --------------------------------------------------------------------------- #

def test_quality_score_detecta_dano_e_limpo():
    limpo = "# Título\n\nTexto normal.\n\n```yaml\non: push\n```\n\n| a | b |\n| --- | --- |\n| 1 | 2 |\n"
    danificado = "# Título\n\n| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n\n\\* bullet\n"
    assert extract.quality_score(limpo)[0] == 0
    score, counts = extract.quality_score(danificado)
    assert score > 0 and counts["table"] >= 1 and counts["bullet"] >= 1


def test_quality_score_ignora_conteudo_dentro_de_cerca():
    com_cerca = "# T\n\n```text\n| a | b |\n| --- |\n\\* x\n```\n"
    assert extract.quality_score(com_cerca)[0] == 0


# --------------------------------------------------------------------------- #
# clean_fragment / heal_with_html (regressão: bs4 4.15 + decompose)
# --------------------------------------------------------------------------- #

def _page_html(body_inner: str) -> str:
    return (
        "<!doctype html><html><head><title>Página — Docs</title></head><body>"
        '<div class="sidebar"><nav>navegação</nav></div>'
        f'<main><div class="markdown-body">{body_inner}</div></main>'
        '<footer class="footer">rodapé</footer></body></html>'
    )


def test_clean_fragment_nao_quebra_com_ancestral_decomposto():
    """Filhos de um ancestral removido continuam na lista pré-coletada do find_all.

    No bs4 4.15 o decompose() invalida o elemento; sem a guarda `_alive()` isso
    levava a `AttributeError: 'NoneType' object has no attribute 'get'`.
    """
    html = _page_html(
        '<div class="sidebar"><nav>x</nav><a href="/pt/actions/a">link</a>'
        '<div class="table-of-contents"><a href="#s">s</a></div></div>'
        f"<h2>Seção</h2><p>{LONG_TEXT}</p>"
        '<div class="note"><p>Uma nota.</p></div>'
        '<div data-snippet-clipboard-copy="on: push"><div class="highlight-source-yaml">'
        "<pre>on: push</pre></div></div>"
    )
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "lxml")
    root = extract.clean_fragment(soup, "https://docs.github.com/pt/actions/x")
    texto = root.get_text(" ", strip=True)
    assert "navegação" not in texto and "rodapé" not in texto
    assert "Seção" in texto


@requer_pandoc
def test_heal_with_html_melhora_pagina_danificada(tmp_path, monkeypatch):
    html = _page_html(
        f"<h2>Limites</h2><p>{LONG_TEXT}</p>"
        "<table><thead><tr><th>Limite</th><th>Valor</th></tr></thead>"
        "<tbody><tr><td>Job</td><td>6 horas</td></tr></tbody></table>"
    )
    monkeypatch.setattr(extract, "http_get_text", lambda url, **kw: html)

    dest = tmp_path / "limits.md"
    dest.write_text(
        "---\ntitle: Limites\nsource: https://docs.github.com/pt/actions/x\n"
        "captured: '2026-10-11'\nlang: pt-BR\n---\n\n# Limites\n\n"
        "| Limite | Valor |\n| --- | --- |\n| Job | 6 horas | extra |\n\n\\* item escapado\n",
        encoding="utf-8",
    )
    antes = extract.quality_score(dest.read_text(encoding="utf-8"))[0]
    assert antes > 0

    res = extract.PageResult(url="https://docs.github.com/pt/actions/x", lang="pt",
                             source="api", status="ok")
    res.path, res.title, res.description = "actions/x.md", "Limites", "Limites de uso"
    extract.heal_with_html(res, dest, "pt", "actions")

    depois = extract.quality_score(dest.read_text(encoding="utf-8"))[0]
    assert depois < antes
    assert res.selector.startswith("api+html-heal(")
    assert any("curada via HTML" in w for w in res.warnings)


@requer_pandoc
def test_heal_preserva_versao_melhor_da_api(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "http_get_text", lambda url, **kw: _page_html("<p>curto</p>"))
    dest = tmp_path / "p.md"
    dest.write_text(
        "---\ntitle: P\nsource: s\ncaptured: '2026-10-11'\nlang: pt-BR\n---\n\n# P\n\n"
        "| a | b |\n| --- | --- |\n| 1 | 2 | 3 |\n",
        encoding="utf-8",
    )
    original = dest.read_text(encoding="utf-8")
    res = extract.PageResult(url="https://docs.github.com/pt/p", lang="pt", source="api", status="ok")
    res.path, res.title = "p.md", "P"
    extract.heal_with_html(res, dest, "pt", "actions")
    # HTML sem conteúdo útil → mantém a versão da API
    assert dest.read_text(encoding="utf-8") == original
    assert any(("não melhorou" in w) or ("não preservou" in w) for w in res.warnings)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(pytest.main([__file__, "-q"]))
