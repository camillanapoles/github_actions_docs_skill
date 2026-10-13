#!/usr/bin/env bash
# IGC v1.0 — W2: bootstrap obrigatório de worktree/sessão.
# Sem bootstrap verde a FSM não sai de BOOT.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2
PIP=(pip install --break-system-packages -q)
command -v python3 >/dev/null || { echo '{"status":2,"message":"python3 ausente"}'; exit 2; }

# W4 — hooks isolados por worktree (extensions.worktreeConfig)
if git rev-parse --git-dir >/dev/null 2>&1; then
  git config extensions.worktreeConfig true 2>/dev/null
  mkdir -p .session/hooks
  git config --worktree core.hooksPath .session/hooks 2>/dev/null
fi

# dependências
"${PIP[@]}" -r scripts/requirements.txt >/dev/null 2>&1
"${PIP[@]}" pytest check-jsonschema yamllint "mkdocs>=1.6" "mkdocs-material>=9.5" >/dev/null 2>&1

# validação de toolchain
missing=()
python3 -c "import bs4, yaml" 2>/dev/null || missing+=("bs4/yaml")
python3 -c "import pypandoc; pypandoc.get_pandoc_version()" 2>/dev/null || missing+=("pandoc")
python3 -c "import pytest" 2>/dev/null || missing+=("pytest")
command -v jq >/dev/null || missing+=("jq")

status=0; direction=continue; message="bootstrap verde"
if [ "${#missing[@]}" -gt 0 ]; then
  status=2; direction=retry; message="toolchain incompleto: ${missing[*]}"
fi

# smoke: testes rápidos (sem rede)
if [ "$status" -eq 0 ]; then
  if out=$(python3 -m pytest tests/ -q 2>&1 | tail -1); then
    message="bootstrap verde; testes: ${out}"
  else
    status=1; direction=fix; message="testes falharam: ${out}"
  fi
fi

cat <<JSON
{"id":"bootstrap:$(date -u +%FT%TZ)","gate":"bootstrap","status":${status},
 "direction":"${direction}","message":"${message}",
 "addenda":[{"kind":"log","path":".session/WAL.md"}]}
JSON
[ "$status" -eq 0 ]
