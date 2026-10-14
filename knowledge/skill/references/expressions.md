---
title: Expressões e funções (${{ }})
description: Sintaxe, tipos, coerção, operadores, todas as funções de expressão e
  de status, filtros de objeto e armadilhas.
source_page: knowledge/pt/actions/reference/workflows-and-actions/expressions.md
generated: true
canonical: https://github.com/camillanapoles/github_actions_docs_skill/blob/arena/c91bd6a1-github-actions-docs-skill/skills/github-actions/references/expressions.md
---

# Expressões — `${{ }}`

Uma expressão pode ser um **literal**, uma **referência a contexto/função** ou uma
**combinação** com operadores. Limite: 4096 caracteres por expressão.

> Fonte oficial capturada: `knowledge/pt/actions/reference/workflows-and-actions/expressions.md`

## 1. Onde usar

| Situação | Exemplo |
| --- | --- |
| `if:` de job/step | `if: github.event_name == 'push'` (o `${{ }}` é opcional aqui) |
| `run:` | `run: echo "${{ matrix.node }}"` (**obrigatório** `${{ }}`) |
| `with:` de action | `with: { node-version: "${{ matrix.node }}" }` |
| `env:` | `env: { IMAGE: "ghcr.io/${{ github.repository }}" }` |
| `name:`, `run-name:` | `name: "Build ${{ github.ref_name }}"` |
| `runs-on:`, `needs:`, `outputs:` | `runs-on: ${{ matrix.os }}` |
| `concurrency.group` | `group: ci-${{ github.ref }}` |

Em `if:`, o GitHub envolve a expressão implicitamente em `${{ }}`; por clareza e
para evitar surpresas com `:` e `{}`, prefira **sempre** escrever `${{ }}`.

## 2. Tipos e coerção

| Tipo | Comportamento |
| --- | --- |
| `null` | vira `0` em comparação numérica; string vazia em concatenação |
| `boolean` | `true` → `1`, `false` → `0` |
| `number` | formato JSON; comparação numérica |
| `string` | comparação **case-insensitive**; para comparar como número use `fromJSON()` |

Comparação de igualdade é **solta**: se os tipos diferirem, o GitHub coage para
número. `'' == 0` → verdadeiro (cuidado!). Para comparação estrita de strings,
compare `toJSON(a) == toJSON(b)` ou normalize antes.

## 3. Operadores

| Operador | Significado |
| --- | --- |
| `( )` | agrupamento |
| `[ ]` | índice |
| `.` | desreferência de propriedade |
| `!` | não |
| `<`, `<=`, `>`, `>=` | comparação numérica |
| `==`, `!=` | igualdade / diferença |
| `&&`, `\|\|` | e / ou |

Não há operador ternário: use `A && B || C` (com `B` sempre verdadeiro) ou `if/else`
em steps separados.

## 4. Funções de expressão

| Função | Assinatura | Observações |
| --- | --- | --- |
| `contains` | `contains(search, item)` | Em string: substring (case-insensitive). Em array: membro. Ex.: `contains(github.event.labels.*.name, 'bug')` |
| `startsWith` | `startsWith(searchString, searchValue)` | case-insensitive |
| `endsWith` | `endsWith(searchString, searchValue)` | case-insensitive |
| `format` | `format(string, ...replaceValues)` | usa `{0}`, `{1}`; `{{` e `}}` são literais |
| `join` | `join(array, separator)` | concatenar com separador opcional |
| `toJSON` | `toJSON(value)` | serializa objeto/array (ótimo para depurar: `run: echo '${{ toJSON(github.event) }}'`) |
| `fromJSON` | `fromJSON(string)` | parseia JSON → objeto/número (essencial para saídas de step) |
| `hashFiles` | `hashFiles(paths, [algorithm], [followSymbolicLinks])` | SHA-256 (ou SHA-512) dos arquivos; `''` se nada casar. Padrões usam `**`, `*`, `!` |

### Funções de status (somente em `if:`)

| Função | Verdadeiro quando |
| --- | --- |
| `success()` | nenhum step anterior falhou/cancelou (default implícito) |
| `always()` | sempre — executa mesmo com falha/cancelamento anteriores |
| `cancelled()` | o workflow foi cancelado |
| `failure()` | algum step anterior do job falhou |

`failure()` em `if:` de **job** considera `needs.*.result == 'failure'`; para
qualquer resultado diferente de sucesso use `!success()` ou liste com
`contains(needs.*.result, 'failure')`.

### Filtros de objeto

```yaml
${{ contains(github.event.*.name, 'deploy') }}        # aplica .name a cada elemento
${{ join(needs.*.outputs.url, ' ') }}                  # todos os outputs dos jobs em needs
${{ hashFiles('**/lock', 'hashFiles', '**/src/**') }}  # múltiplos padrões
```

## 5. `hashFiles` e cache — padrão correto

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-npm-
```

- `hashFiles` ignora o diretório `.git` e considera apenas arquivos existentes.
- Use `restore-keys` para cache parcial; `key` exata para reprodutibilidade.
- Para múltiplas linguagens, inclua o nome do SO e a versão da ferramenta na chave.

## 6. Depuração de expressões

```yaml
- name: Dump do contexto
  if: always()
  env:
    GITHUB_CTX: ${{ toJSON(github) }}
    NEEDS_CTX: ${{ toJSON(needs) }}
    MATRIX: ${{ toJSON(matrix) }}
    VARS: ${{ toJSON(vars) }}
  run: |
    echo "$GITHUB_CTX" | jq .
    echo "$NEEDS_CTX"  | jq .
    echo "$MATRIX"     | jq .
    # segredos NUNCA entram em toJSON(secrets) — não faça isso
```

Use `ACTIONS_STEP_DEBUG=true` (secret/variable) para logs verbosos do runner.

## 7. Armadilhas clássicas

| Erro | Consequência | Correto |
| --- | --- | --- |
| `if: github.event_name == push` | compara com variável inexistente → sempre falso | `== 'push'` (string entre aspas) |
| `run: echo ${{ github.event.issue.title }}` | **injeção de shell** | `env: { TITLE: ${{ ... }} }` + `echo "$TITLE"` |
| `if: ${{ steps.x.outputs.ok }}` com valor `"false"` | string não vazia → verdadeiro | `== 'true'` explícito |
| Comparar números de outputs sem `fromJSON` | comparação de string | `${{ fromJSON(steps.x.outputs.count) > 10 }}` |
| `hashFiles` em `runs-on:` | função indisponível ali | calcule em step anterior ou use `vars` |
| `contains(github.event.labels.*.name, 'X')` em evento que não é PR | `null` → falso silencioso | confirme o evento no `on:` |
| Aspas duplas dentro de `run:` com `${{ }}` | quebra de shell | use aspas simples no YAML ou `env:` |
| `${{ secrets.X }}` em `name:` de step | valor aparece no título do step (log) | não use segredos fora de `env`/`with` |
