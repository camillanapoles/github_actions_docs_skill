---
title: Avaliar expressões em fluxos de trabalho e ações
description: Encontre informações sobre expressões em GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/expressions
captured: '2026-10-11'
section: GitHub Actions
---

# Avaliar expressões em fluxos de trabalho e ações

_Encontre informações sobre expressões em GitHub Actions._

## Literais

Como parte de uma expressão, você pode usar os tipos de dados `boolean`, `null`, `number` ou `string`.

| Tipo de dados     | Valor literal                                                                                                                                                                                                                                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `boolean`         |                                                                                                                                                                                                                                                                                                                                   |
| `true` ou `false` |                                                                                                                                                                                                                                                                                                                                   |
| `null`            | `null`                                                                                                                                                                                                                                                                                                                            |
| `number`          | Qualquer formato de número aceito por JSON.                                                                                                                                                                                                                                                                                       |
| `string`          | Você não precisa colocar cadeias de caracteres em `${` e `}`. No entanto, se você fizer isso, deverá usar aspas simples (`'`) ao redor da cadeia de caracteres. Para usar uma aspa simples literal, não use as aspas simples literais e use as aspas simples adicionais (`''`). Encapsular com aspas duplas (`"`) gerará um erro. |

Note que em condicionais, valores falsos (`false`, `0`, `-0`, `""`, `''`, `null`) são coagidos para `false` e valores verdadeiros (`true` e outros valores não falsos) são coagidos para `true`.

### Exemplo de literais

```yaml
env:
  myNull: ${{ null }}
  myBoolean: ${{ false }}
  myIntegerNumber: ${{ 711 }}
  myFloatNumber: ${{ -9.2 }}
  myHexNumber: ${{ 0xff }}
  myExponentialNumber: ${{ -2.99e-2 }}
  myString: Mona the Octocat
  myStringInBraces: ${{ 'It''s open source!' }}
```

## Operadores

| Operador          | Descrição             |
| ----------------- | --------------------- |
| `( )`             | Agrupamento lógico    |
| `[ ]`             | Índice                |
| `.`               | Property de-reference |
| `!`               | Not                   |
| `<`               | Menor que             |
| `<=`              | Inferior ou igual     |
| `>`               | Maior que             |
| `>=`              | Maior ou igual a      |
| `==`              | Igual                 |
| `!=`              | Diferente             |
| `&&`              | E                     |
| <code>\|\|</code> | Ou                    |

> \[!NOTE]
> \*
> GitHub ignora maiúsculas e minúsculas ao comparar cadeias de caracteres.
> \*
> `steps.<step_id>.outputs.<output_name>` é avaliada como cadeia de caracteres.
> É necessário usar uma sintaxe específica para avisar o GitHub para avaliar a expressão e não tratá-la como uma string. Para obter mais informações, consulte [Referência de contextos](contexts.md#steps-context).
>
> * Para comparação numérica, a função `fromJSON()` pode ser usada para converter uma cadeia de caracteres em um número. Para obter mais informações sobre a função `fromJSON()` confira [fromJSON](#fromjson).

GitHub executa comparações de igualdade soltas.

* Se os tipos não corresponderem, GitHub coagi o tipo a um número.
  GitHub converte tipos de dados em um número usando estas conversões:

  | Tipo     | Result |
  | -------- | ------ |
  | Nulo     | `0`    |
  | booleano |        |

`true` retorna `1` <br />
`false` retorna `0` |
\| String  | Analisado de qualquer formato de número JSON legal, caso contrário, `NaN`. <br /> Observação: a cadeia de caracteres vazia retorna `0`. |
\| Array   | `NaN` |
\| Objeto  | `NaN` |

* Quando `NaN` é um dos operandos de qualquer comparação relacional (`>`, `<`, `>=`, `<=`), o resultado é sempre `false`. Para obter mais informações, confira os [documentos do NaN Mozilla](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/NaN).
* GitHub ignora maiúsculas e minúsculas ao comparar cadeias de caracteres.
* Objetos e arrays só são considerados iguais quando forem a mesma instância.

## Functions

GitHub oferece um conjunto de funções internas que você pode usar em expressões. Algumas funções convertem valores em uma string para realizar comparações.
GitHub converte tipos de dados em uma cadeia de caracteres usando estas conversões:

| Tipo                  | Result                                          |
| --------------------- | ----------------------------------------------- |
| Nulo                  | `''`                                            |
| booleano              |                                                 |
| `'true'` ou `'false'` |                                                 |
| Número                | Formato decimal, exponencial para números altos |
| Array                 | Arrays não são convertidos em uma string        |
| Objeto                | Objetos não são convertidos em uma string       |

### contém

`contains( search, item )`

Retorna `true` se `search` contém `item`. Se `search` for uma matriz, essa função retornará `true` se o `item` for um elemento na matriz. Se `search` for uma cadeia de caracteres, essa função retornará `true` se `item` uma substring de `search`. Essa função não diferencia maiúsculas de minúsculas. Lança valores em uma string.

#### Exemplo de uso de string

`contains('Hello world', 'llo')` retorna `true`.

#### Exemplo de como usar um filtro de objeto

`contains(github.event.issue.labels.*.name, 'bug')` retornará `true` se o problema relacionado ao evento tiver um rótulo "bug".

Para obter mais informações, confira [Filtros de objeto](#object-filters).

#### Exemplo que corresponde a uma matriz de cadeias de caracteres

Em vez de escrever `github.event_name == "push" || github.event_name == "pull_request"`, você pode usar `contains()` com `fromJSON()` para verificar se uma matriz de cadeias de caracteres contém um `item`.

Por exemplo, `contains(fromJSON('["push", "pull_request"]'), github.event_name)` retornará `true` se `github.event_name` for "push" ou "pull\_request".

### startsWith

`startsWith( searchString, searchValue )`

Retorna `true` quando`searchString` começa com `searchValue`. Essa função não diferencia maiúsculas de minúsculas. Lança valores em uma string.

#### Exemplo de `startsWith`

`startsWith('Hello world', 'He')` retorna `true`.

### endsWith

`endsWith( searchString, searchValue )`

Retorna `true` se `searchString` termina com `searchValue`. Essa função não diferencia maiúsculas de minúsculas. Lança valores em uma string.

#### Exemplo de `endsWith`

`endsWith('Hello world', 'ld')` retorna `true`.

### formato

`format( string, replaceValue0, replaceValue1, ..., replaceValueN)`

Substitui os valores na `string`, com a variável `replaceValueN`. As variáveis na `string` são especificadas usando a sintaxe `{N}`, em que `N` é um inteiro. É necessário especificar pelo menos um `replaceValue` e uma `string`. Não há um máximo para o número de variáveis (`replaceValueN`) que você pode usar. Escape de chaves usando chaves duplas.

#### Exemplo de `format`

```javascript
format('Hello {0} {1} {2}', 'Mona', 'the', 'Octocat')
```

Retorna "Hello Mona the Octocat".

#### Exemplo de escape de chaves

```javascript
format('{{Hello {0} {1} {2}!}}', 'Mona', 'the', 'Octocat')
```

Retorna '{Hello Mona the Octocat!}'.

### ingressar

`join( array, optionalSeparator )`

O valor para `array` pode ser uma matriz ou uma cadeia de caracteres. Todos os valores em `array` são concatenados em uma cadeia de caracteres. Se você fornecer `optionalSeparator`, ele será inserido entre os valores concatenados. Caso contrário, o separador padrão `,` será usado. Lança valores em uma string.

#### Exemplo de `join`

`join(github.event.issue.labels.*.name, ', ')` pode retornar "bug, preciso de ajuda"

### toJSON

`toJSON(value)`

Retorna uma representação JSON recém-impressa de `value`. Você pode usar essa função para depurar as informações fornecidas em contextos.

#### Exemplo de `toJSON`

`toJSON(job)` pode retornar `{ "status": "success" }`

### fromJSON

`fromJSON(value)`

Retorna um objeto JSON ou um tipo de dados JSON para `value`. Você pode usar essa função para fornecer um objeto JSON como uma expressão avaliada ou para converter qualquer tipo de dados que possa ser representado em JSON ou JavaScript, como cadeias de caracteres, boolianos, valores nulos, matrizes e objetos.

#### Exemplo que retorna um objeto do JSON

Esse fluxo de trabalho define uma matriz JSON em um trabalho e a passa para o próximo trabalho usando uma saída e `fromJSON`.

```yaml copy
name: build
on: push
jobs:
  job1:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: echo "matrix={\"include\":[{\"project\":\"foo\",\"config\":\"Debug\"},{\"project\":\"bar\",\"config\":\"Release\"}]}" >> $GITHUB_OUTPUT
  job2:
    needs: job1
    runs-on: ubuntu-latest
    strategy:
      matrix: ${{ fromJSON(needs.job1.outputs.matrix) }}
    steps:
      - run: echo "Matrix - Project ${{ matrix.project }}, Config ${{ matrix.config }}"
```

#### Exemplo que retorna um tipo de dado do JSON

Esse fluxo de trabalho usa `fromJSON` para converter variáveis de ambiente de uma cadeia de caracteres em um booliano ou inteiro.

```yaml copy
name: print
on: push
env:
  continue: true
  time: 3
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - continue-on-error: ${{ fromJSON(env.continue) }}
        timeout-minutes: ${{ fromJSON(env.time) }}
        run: echo ...
```

O fluxo de trabalho usa a função `fromJSON()` para converter a variável de ambiente `continue` de uma cadeia de caracteres em um booliano, permitindo que ele determine se deve continuar no erro ou não. Da mesma forma, ele converte a variável de ambiente `time` de uma cadeia de caracteres em um inteiro, definindo o tempo limite para o trabalho em minutos.

### hashFiles

`hashFiles(path)`

Retorna um único hash para o conjunto de arquivos que corresponde ao padrão `path`. Você pode fornecer um único padrão `path` ou vários padrões `path` separados por vírgulas. O `path` é relativo ao diretório `GITHUB_WORKSPACE` e só pode incluir arquivos dentro do `GITHUB_WORKSPACE`. Essa função calcula uma hash SHA-256 individual para cada arquivo correspondente e, em seguida, usa esses hashes para calcular um hash SHA-256 final para o conjunto de arquivos. Se o padrão `path` não corresponder a nenhum arquivo, isso retornará uma cadeia de caracteres vazia. Para obter mais informações sobre SHA-256, consulte [SHA-2](https://en.wikipedia.org/wiki/SHA-2).

Você pode usar a correspondência de padrão de caracteres para corresponder os nomes dos arquivos. A correspondência de padrões para `hashFiles` segue a correspondência de padrão glob e não diferencia maiúsculas de minúsculas no Windows. Para obter mais informações sobre caracteres de correspondência de padrão com suporte, confira a seção [Padrões](https://www.npmjs.com/package/@actions/glob#patterns) na documentação `@actions/glob`.

#### Exemplos com um padrão único

Corresponde a qualquer arquivo `package-lock.json` no repositório.

`hashFiles('**/package-lock.json')`

Corresponde a todos os arquivos `.js` no diretório `src` no nível de raiz, mas ignora os subdiretórios de `src`.

`hashFiles('/src/*.js')`

Corresponde a todos os arquivos `.rb` no diretório `lib` no nível de raiz, incluindo os subdiretórios de `lib`.

`hashFiles('/lib/**/*.rb')`

#### Exemplos com vários padrões

Cria um hash para qualquer `package-lock.json` e arquivos `Gemfile.lock` no repositório.

`hashFiles('**/package-lock.json', '**/Gemfile.lock')`

Cria um hash para todos os arquivos `.rb` no diretório `lib` no nível de raiz, incluindo os subdiretórios de `lib`, mas não os arquivos `.rb` no subdiretório `foo`.

`hashFiles('/lib/**/*.rb', '!/lib/foo/*.rb')`

### caso

`case( pred1, val1, pred2, val2, ..., default )`

Avalia predicados em ordem e retorna o valor correspondente ao primeiro predicado que é avaliado como `true`. Se nenhum predicado corresponder, ele retornará o último argumento como o valor padrão.

#### Exemplo com um único predicado

```yaml
env:
  MY_ENV_VAR: ${{ case(github.ref == 'refs/heads/main', 'production', 'development') }}
```

Define `MY_ENV_VAR` como `production` quando o ref é `refs/heads/main`, caso contrário, define-o como `development`.

#### Exemplo com vários predicados

```yaml
env:
  MY_ENV_VAR: |-
    ${{ case(
      github.ref == 'refs/heads/main', 'production',
      github.ref == 'refs/heads/staging', 'staging',
      startsWith(github.ref, 'refs/heads/feature/'), 'development',
      'unknown'
    ) }}
```

Configura `MY_ENV_VAR` com base na ramificação: `production` para `main`, `staging` para `staging`, `development` para ramificações começando com `feature/`, ou `unknown` para todas as outras ramificações.

## Funções de verificação de status

Você pode usar as funções de verificação de status a seguir como expressões em condicionais `if`. Uma verificação de status `success()` padrão é aplicada, a menos que você inclua uma dessas funções. Para obter mais informações sobre condicionais `if`, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idif) e [Referência de sintaxe de metadados](metadata-syntax.md#runsstepsif).

Fora de condicionais `if`, você pode usar `job.status` para acessar o status do trabalho. Para saber mais, confira [Referência de contextos](contexts.md#job-context).

### sucesso

Retorna `true` quando todas as etapas anteriores forem bem-sucedidas.

#### Exemplo de `success`

```yaml
steps:
  ...
  - name: The job has succeeded
    if: ${{ success() }}
```

### sempre

Faz com que a etapa sempre seja executada e retorna `true`, mesmo quando cancelada. A expressão `always` é melhor usada no nível da etapa ou em tarefas que você espera executar mesmo quando um trabalho é cancelado. Por exemplo, você pode usar `always` para enviar logs mesmo quando um trabalho é cancelado.

> \[!WARNING]
> Evite usar `always` para qualquer tarefa que possa sofrer uma falha crítica, por exemplo, obtenção de fontes. Caso contrário, o fluxo de trabalho pode travar até atingir o tempo limite. Se você quiser executar um trabalho ou uma etapa independentemente de seu êxito ou falha, use a alternativa recomendada: `if: ${{ !cancelled() }}`

#### Exemplo de `always`

```yaml
if: ${{ always() }}
```

### cancelled

Retorna `true` se o fluxo de trabalho foi cancelado.

#### Exemplo de `cancelled`

```yaml
if: ${{ cancelled() }}
```

### falha

Retorna `true` quando qualquer etapa anterior de um trabalho falha. Se você tiver uma cadeia de trabalhos dependentes, `failure()` retornará `true` se algum trabalho ancestral falhar.

#### Exemplo de `failure`

```yaml
steps:
  ...
  - name: The job has failed
    if: ${{ failure() }}
```

#### falha com condições

Você pode incluir condições extras para uma etapa a ser executada após uma falha, mas ainda precisa incluir `failure()` para substituir a verificação de status padrão de `success()` que é aplicada automaticamente a condições `if` que não contêm uma função de verificação de status.

##### Exemplo de `failure` com condições

```yaml
steps:
  ...
  - name: Failing step
    id: demo
    run: exit 1
  - name: The demo step has failed
    if: ${{ failure() && steps.demo.conclusion == 'failure' }}
```

## Filtros de objeto

Você pode usar a sintaxe `*` para aplicar um filtro e selecionar itens de uma coleção correspondente.

Por exemplo, considere uma matriz de objetos chamados `fruits`.

```json
[
  { "name": "apple", "quantity": 1 },
  { "name": "orange", "quantity": 2 },
  { "name": "pear", "quantity": 1 }
]
```

O filtro `fruits.*.name` retorna a matriz `[ "apple", "orange", "pear" ]`.

Você também pode usar a sintaxe `*` em um objeto. Por exemplo, suponha que você tenha um objeto chamado `vegetables`.

```json

{
  "scallions":
  {
    "colors": ["green", "white", "red"],
    "ediblePortions": ["roots", "stalks"]
  },
  "beets":
  {
    "colors": ["purple", "red", "gold", "white", "pink"],
    "ediblePortions": ["roots", "stems", "leaves"]
  },
  "artichokes":
  {
    "colors": ["green", "purple", "red", "black"],
    "ediblePortions": ["hearts", "stems", "leaves"]
  }
}
```

O filtro `vegetables.*.ediblePortions` pode ser avaliado como:

```json

[
  ["roots", "stalks"],
  ["hearts", "stems", "leaves"],
  ["roots", "stems", "leaves"]
]
```

Como os objetos não preservam a ordem, a ordem da saída não pode ser garantida.
