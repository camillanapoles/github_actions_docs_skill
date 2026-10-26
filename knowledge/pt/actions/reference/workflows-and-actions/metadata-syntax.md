---
title: Referência de sintaxe de metadados
description: É possível criar ações para realizar tarefas no repositório. Se você estiver fazendo uma ação personalizada, ela exigirá um arquivo de metadados que use a sintaxe YAML.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/metadata-syntax
captured: '2026-10-26'
section: Reference / Workflows and actions
---

# Referência de sintaxe de metadados

_É possível criar ações para realizar tarefas no repositório. Se você estiver fazendo uma ação personalizada, ela exigirá um arquivo de metadados que use a sintaxe YAML._

!!! note
    Você pode criar um contêiner do Docker, JavaScript e ações compostas. As ações exigem um arquivo de metadados para definir a configuração de entradas, saídas e execuções para sua ação. Os arquivos de metadados de ação usam a sintaxe YAML e o nome do arquivo de metadados deve ser `action.yml` ou `action.yaml`. O formato preferencial é `action.yml`.

## `name`

**Obrigatório** O nome da sua ação.
GitHub exibe `name` na guia **Ações** para ajudar a identificar visualmente as ações em cada tarefa.

## `author`

**Opcional** O nome do autor da ação.

## `description`

**Obrigatório** Uma breve descrição da ação.

## `inputs`

**Opcional** Os parâmetros de entrada permitem que você especifique os dados que a ação espera usar durante o runtime.
GitHub armazena parâmetros de entrada como variáveis de ambiente. Recomenda-se usar identificações de entrada com letras minúsculas.

### Exemplo: Especificando entradas

Este exemplo configura duas entradas: `num-octocats` e `octocat-eye-color`. A entrada `num-octocats` não é obrigatória e usará o valor `1` como padrão.
`octocat-eye-color` é obrigatório e não tem valor padrão.

!!! note
    As ações que usam `required: true` não retornarão automaticamente um erro se a entrada não for especificada.

Os arquivos de fluxo de trabalho que usam essa ação podem usar a palavra-chave `with` a fim de definir um valor de entrada para `octocat-eye-color`. Para obter mais informações sobre a sintaxe `with`, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idstepswith).

```yaml
inputs:
  num-octocats:
    description: 'Number of Octocats'
    required: false
    default: '1'
  octocat-eye-color:
    description: 'Eye color of the Octocats'
    required: true
```

Quando você especifica uma entrada, GitHub cria uma variável de ambiente para a entrada com o nome `INPUT_<VARIABLE_NAME>`. A variável de ambiente criada converte os nomes de entrada em letras maiúsculas e substitui os espaços por caracteres `_`.

Se a ação for escrita usando um [composite](../../tutorials/create-actions/create-a-composite-action.md), ela não obterá `INPUT_<VARIABLE_NAME>` automaticamente. Com ações compostas, você pode usar o [`inputs` contexto](contexts.md#inputs-context) para acessar entradas de ação.

Para acessar a variável de ambiente em uma ação de contêiner do Docker, você precisará transmitir a entrada usando a palavra-chave `args` no arquivo de metadados da ação. Para obter mais informações sobre o arquivo de metadados de ação das ações de contêiner do Docker, confira [Criando uma ação de contêiner do Docker](../../tutorials/use-containerized-services/create-a-docker-container-action.md#creating-an-action-metadata-file).

Por exemplo, se um fluxo de trabalho definir as entradas `num-octocats` e `octocat-eye-color`, o código da ação poderá ler os valores das entradas usando as variáveis de ambiente `INPUT_NUM-OCTOCATS` e `INPUT_OCTOCAT-EYE-COLOR`.

### `inputs.<input_id>`

**Obrigatório** Um identificador `string` a ser associado à entrada. O valor de `<input_id>` é um mapa dos metadados da entrada. A `<input_id>` precisa ser um identificador exclusivo dentro do objeto `inputs`. A `<input_id>` precisa começar com uma letra ou `_` e conter apenas caracteres alfanuméricos, `-` ou `_`.

### `inputs.<input_id>.description`

**Obrigatório** Uma descrição `string` dos parâmetros de entrada.

### `inputs.<input_id>.required`

**Opcional** Um `boolean` para indicar se a ação exige o parâmetro de entrada. Defina-o como `true` quando o parâmetro for obrigatório.

### `inputs.<input_id>.default`

**Opcional** uma `string` que representa o valor padrão. O valor padrão é usado quando um parâmetro de entrada não é especificado em um arquivo de fluxo de trabalho.

### `inputs.<input_id>.deprecationMessage`

**Opcional** se o parâmetro de entrada for usado, essa `string` será registrada em log como uma mensagem de aviso. Você pode usar esse aviso para notificar os usuários de que a entrada é encerrando e mencionar quaisquer alternativas.

## `outputs` para ações de contêiner do Docker e de JavaScript

**Opcional** Os parâmetros de saída permitem que você declare os dados definidos por uma ação. As ações executadas posteriormente em um fluxo de trabalho podem usar os dados de saída definidos em ações executadas anteriormente. Por exemplo, se uma ação executou a adição de duas entradas (x + y = z), a ação poderia usar o resultado da soma (z) como entrada em outras ações.

As saídas podem ter no máximo 1 MB por trabalho. O total de todas as saídas em uma execução de fluxo de trabalho pode ter no máximo 50 MB. O tamanho é aproximado com base na codificação UTF-16.

Se você não declarar uma saída no seu arquivo de metadados de ação, você ainda poderá definir as saídas e usá-las no seu fluxo de trabalho. Para obter mais informações sobre como definir saídas em uma ação, consulte [Comandos de fluxo de trabalho para o GitHub Actions](workflow-commands.md#setting-an-output-parameter).

### Exemplo: Declarando saídas para contêiner Docker e ações JavaScript

```yaml
outputs:
  sum: # id of the output
    description: 'The sum of the inputs'
```

### `outputs.<output_id>`

**Obrigatório** Um identificador `string` a ser associado à saída. O valor de `<output_id>` é um mapa dos metadados da saída. A `<output_id>` precisa ser um identificador exclusivo dentro do objeto `outputs`. A `<output_id>` precisa começar com uma letra ou `_` e conter apenas caracteres alfanuméricos, `-` ou `_`.

### `outputs.<output_id>.description`

**Obrigatório** Uma descrição `string` do parâmetro de saída.

## `outputs` para ações compostas

**Opcional**`outputs` usa os mesmos parâmetros que `outputs.<output_id>` e `outputs.<output_id>.description` (confira [`outputs` para ações de contêiner do Docker e de JavaScript](#outputs-for-docker-container-and-javascript-actions)), mas também inclui o token `value`.

As saídas podem ter no máximo 1 MB por trabalho. O total de todas as saídas em uma execução de fluxo de trabalho pode ter no máximo 50 MB. O tamanho é aproximado com base na codificação UTF-16.

### Exemplo: Declarando saídas para ações compostas

```yaml
outputs:
  random-number:
    description: "Random number"
    value: ${{ steps.random-number-generator.outputs.random-id }}
runs:
  using: "composite"
  steps:
    - id: random-number-generator
      run: echo "random-id=$(echo $RANDOM)" >> $GITHUB_OUTPUT
      shell: bash
```

### `outputs.<output_id>.value`

**Obrigatório** O valor para o qual o parâmetro de saída será mapeado. Defina isso como uma `string` ou uma expressão com um contexto. Por exemplo, você pode usar o contexto `steps` para definir o `value` de uma saída como o valor de saída de uma etapa.

Para obter mais informações sobre como usar a sintaxe de contexto, consulte [Referência de contextos](contexts.md).

## `runs`

**Obrigatório** Especifica se esta é uma ação de JavaScript, uma ação composta ou uma ação de contêiner do Docker e como a ação é executada.

## `runs` para ações de JavaScript

**Obrigatório** Configura o caminho para o código da ação e o runtime usado para executar o código.

### Exemplo: usar o Node.js v24

```yaml
runs:
  using: 'node24'
  main: 'main.js'
```

### `runs.using` para ações de JavaScript

**Obrigatório** O runtime usado para executar o código especificado em [`main`](#runsmain).

* Use `node20` para Node.js v20.
* Usar `node24` para Node.js v24.

### `runs.main`

**Obrigatório** O arquivo que contém o código de ação. O runtime especificado em [`using`](#runsusing-for-javascript-actions) executa este arquivo.

### `runs.pre`

**Opcional** Permite que você execute um script no início de um trabalho, antes do início da ação `main:`. Por exemplo, você pode usar `pre:` para executar um script de configuração de pré-requisito. O runtime especificado com a sintaxe [`using`](#runsusing-for-javascript-actions) executará esse arquivo. A ação `pre:` sempre é executada por padrão, mas você pode substituir isso usando [`runs.pre-if`](#runspre-if).

!!! note
    `runs.pre` não tem suporte para ações locais.

Neste exemplo, a ação `pre:` executa um script chamado `setup.js`:

```yaml
runs:
  using: 'node24'
  pre: 'setup.js'
  main: 'index.js'
  post: 'cleanup.js'
```

### `runs.pre-if`

**Opcional** Permite definir condições para a execução da ação `pre:`. A ação `pre:` só será executada se as condições em `pre-if` forem atendidas. Se isso não estiver definido, `pre-if` usará `always()` como padrão. Em `pre-if`, as funções de verificação de status são avaliadas em relação ao status do trabalho, não ao status próprio da ação.

Observe que o contexto `step` não está disponível, pois nenhuma etapa foi executada ainda.

Neste exemplo, `cleanup.js` só é executado em executores baseados em Linux:

```yaml
  pre: 'cleanup.js'
  pre-if: runner.os == 'linux'
```

### `runs.post`

**Opcional** Permite que você execute um script no final de um trabalho, depois que a ação `main:` for concluída. Por exemplo, você pode usar `post:` para encerrar alguns processos ou remover arquivos desnecessários. O runtime especificado com a sintaxe [`using`](#runsusing-for-javascript-actions) executará esse arquivo.

Neste exemplo, a ação `post:` executa um script chamado `cleanup.js`:

```yaml
runs:
  using: 'node24'
  main: 'index.js'
  post: 'cleanup.js'
```

A ação `post:` sempre é executada por padrão, mas você pode substituir isso usando `post-if`.

### `runs.post-if`

**Opcional** Permite definir condições para a execução da ação `post:`. A ação `post:` só será executada se as condições em `post-if` forem atendidas. Se isso não estiver definido, `post-if` usará `always()` como padrão. Em `post-if`, as funções de verificação de status são avaliadas em relação ao status do trabalho, não ao status próprio da ação.

Por exemplo, este `cleanup.js` só será executado em executores baseados em Linux:

```yaml
  post: 'cleanup.js'
  post-if: runner.os == 'linux'
```

## `runs` para ações compostas

**Obrigatório** Configura o caminho para a ação composta.

### `runs.using` para ações compostas

**Obrigatório** Você precisa definir esse valor como `'composite'`.

### `runs.steps`

**Obrigatório** As etapas que você pretende executar nesta ação. Elas podem ser etapas `run` ou etapas `uses`.

#### `runs.steps[*].run`

**Opcional** O comando que você deseja executar. Essa opção pode ser embutida ou um script no repositório de ação:

```yaml
runs:
  using: "composite"
  steps:
    - run: ${{ github.action_path }}/test/script.sh
      shell: bash
```

Como alternativa, você pode usar `$GITHUB_ACTION_PATH`:

```yaml
runs:
  using: "composite"
  steps:
    - run: $GITHUB_ACTION_PATH/script.sh
      shell: bash
```

Para saber mais, confira [Referência de contextos](contexts.md#github-context).

#### `runs.steps[*].shell`

**Opcional** O shell no qual você deseja executar o comando. Você pode usar qualquer um dos shells listados em [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#jobsjob_idstepsshell). Obrigatório se `run` for definido.

#### `runs.steps[*].if`

**Opcional** Use o condicional `if` para impedir que uma etapa seja executada, a não ser que uma condição seja atendida. Você pode usar qualquer contexto e expressão compatível para criar uma condicional.

Ao usar expressões em um condicional `if`, opcionalmente, você poderá omitir a sintaxe de expressão `${{ }}`, pois o GitHub Actions avalia automaticamente o condicional `if` como uma expressão. No entanto, essa exceção não se aplica a todos os lugares.

Você sempre deverá usar a sintaxe de expressão `${{ }}` ou escapar com `''`, `""` ou `()` quando a expressão começar com `!`, já que `!` é a notação reservada no formato YAML. Por exemplo:

```yaml
if: ${{ ! startsWith(github.ref, 'refs/tags/') }}
```

Para obter mais informações, consulte [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

**Exemplo: Usando contextos**

Essa etapa só é executada quando o tipo de evento é uma `pull_request` e a ação do evento é `unassigned`.

```yaml
steps:
  - run: echo This event is a pull request that had an assignee removed.
    if: ${{ github.event_name == 'pull_request' && github.event.action == 'unassigned' }}
```

**Exemplo: Usando funções de verificação de status**

O `my backup step` só é executado quando o passo anterior de uma ação composta falha. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](expressions.md#status-check-functions).

```yaml
steps:
  - name: My first step
    uses: octo-org/action-name@main
  - name: My backup step
    if: ${{ failure() }}
    uses: actions/heroku@1.0.0
```

#### `runs.steps[*].name`

**Opcional** O nome da etapa composta.

#### `runs.steps[*].id`

**Opcional** Um identificador exclusivo da etapa. Use a `id` para referenciar a etapa em contextos. Para saber mais, confira [Referência de contextos](contexts.md).

#### `runs.steps[*].env`

**Opcional** Define um conjunto de variáveis de ambiente somente para essa etapa. Caso deseje modificar a variável de ambiente armazenada no fluxo de trabalho, use `echo "{name}={value}" >> $GITHUB_ENV` em uma etapa composta.

#### `runs.steps[*].working-directory`

**Opcional** Especifica o diretório de trabalho em que o comando é executado.

#### `runs.steps[*].uses`

**Opcional** Seleciona uma ação para executá-la como parte de uma etapa no trabalho. A ação é uma unidade reutilizável de código. Você pode usar uma ação definida no mesmo repositório do fluxo de trabalho, um repositório público ou em uma [imagem publicada de um contêiner do Docker](https://hub.docker.com/).

É altamente recomendável incluir a versão da ação que você está usando ao especificar um ref do Git, SHA ou número de tag do Docker. Se você não especificar uma versão, ela poderá interromper seus fluxos de trabalho ou causar um comportamento inesperado quando o proprietário da ação publicar uma atualização.

* Usar o commit SHA de uma versão de ação lançada é a maneira mais garantida de obter estabilidade e segurança.
* Usar a versão principal da ação permite receber correções importantes e patches de segurança sem perder a compatibilidade. Fazer isso também garante o funcionamento contínuo do fluxo de trabalho.
* Usar o branch-padrão de uma ação pode ser conveniente, mas se alguém lançar uma nova versão principal com uma mudança significativa, seu fluxo de trabalho poderá ter problemas.

Algumas ações exigem entradas que precisam ser definidas com a palavra-chave [`with`](workflow-syntax.md#jobsjob_idstepswith). Revise o arquivo README da ação para determinar as entradas obrigatórias.

```yaml
runs:
  using: "composite"
  steps:
    # Reference a specific commit
    - uses: actions/checkout@8f4b7f84864484a7bf31766abe9204da3cbe65b3
    # Reference the major version of a release
    - uses: actions/checkout@v6
    # Reference a specific version
    - uses: actions/checkout@v6.2.0
    # Reference a branch
    - uses: actions/checkout@main
    # References a subdirectory in a public GitHub repository at a specific branch, ref, or SHA
    - uses: actions/aws/ec2@main
    # References an action in the same repository at the running commit
    - uses: $/.github/actions/my-action
    # References a local action
    - uses: ./.github/actions/my-action
    # References a docker public registry action
    - uses: docker://gcr.io/cloud-builders/gradle
    # Reference a docker image published on docker hub
    - uses: docker://alpine:3.8
```

Para referenciar uma ação armazenada no mesmo repositório que sua ação composta, use a referência ao próprio repositório `$/`, conforme mostrado no `$/.github/actions/my-action` exemplo acima. Isso aponta para esse repositório no commit em uso, portanto você não precisa fazer checkout do repositório primeiro, e ele não deve incluir o sufixo `@{ref}`. A `$/` sintaxe não está disponível em GitHub Enterprise Server.

Para obter uma comparação de `$/`, `{owner}/{repo}@{ref}`e `./`, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#example-using-an-action-in-the-same-repository-as-the-workflow-at-the-running-commit-recommended).

#### `runs.steps[*].with`

**Opcional** Um `map` dos parâmetros de entrada definidos pela ação. Cada parâmetro de entrada é um par chave/valor. Para obter mais informações, confira [Exemplo: como especificar entradas](#example-specifying-inputs).

```yaml
runs:
  using: "composite"
  steps:
    - name: My first step
      uses: actions/hello_world@main
      with:
        first_name: Mona
        middle_name: The
        last_name: Octocat
```

#### `runs.steps[*].continue-on-error`

**Opcional** Impede que a ação falhe quando uma etapa falha. Defina como `true` para permitir que a ação continue se esta etapa falhar.

## `runs` para ações de contêiner do Docker

**Obrigatório** Configura a imagem usada para a ação de contêiner do Docker.

### Exemplo: Usando um arquivo do Dockerfile no seu repositório

```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
```

### Exemplo: Usando o contêiner de registro público do Docker

```yaml
runs:
  using: 'docker'
  image: 'docker://debian:stretch-slim'
```

### `runs.using` para ações de contêiner do Docker

**Obrigatório** Você precisa definir esse valor como `'docker'`.

### `runs.pre-entrypoint`

**Opcional** Permite que você execute um script antes do início da ação `entrypoint`. Por exemplo, você pode usar `pre-entrypoint:` para executar um script de configuração de pré-requisito.
GitHub Actions usa `docker run` para iniciar essa ação e executa o script dentro de um novo contêiner que usa a mesma imagem base. Isso significa que o estado de runtime é diferente do contêiner `entrypoint` principal, e todos os status que você exigir precisarão ser acessados no workspace, `HOME`, ou como uma variável `STATE_`. A ação `pre-entrypoint:` sempre é executada por padrão, mas você pode substituir isso usando [`runs.pre-if`](#runspre-if-for-docker-container-actions).

O runtime especificado com a sintaxe [`using`](#runsusing-for-docker-container-actions) executará esse arquivo.

Neste exemplo, a ação `pre-entrypoint:` executa um script chamado `setup.sh`:

```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - 'bzz'
  pre-entrypoint: 'setup.sh'
  entrypoint: 'main.sh'
```

### `runs.pre-if` para ações de contêiner do Docker

**Opcional** Permite definir condições para a execução da ação `pre-entrypoint:`. A ação `pre-entrypoint:` só será executada se as condições em `pre-if` forem atendidas. Se isso não estiver definido, `pre-if` usará `always()` como padrão.

Neste exemplo, a ação `pre-entrypoint:` é executada somente em executores baseados em Linux:

```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
  pre-entrypoint: 'setup.sh'
  pre-if: runner.os == 'linux'
  entrypoint: 'main.sh'
```

### `runs.image`

**Obrigatório** A imagem Docker a ser usada como contêiner para executar a ação. O valor pode ser o nome da imagem base do Docker, um `Dockerfile` local no seu repositório ou uma imagem pública do Docker Hub ou de outro registro. Para referenciar um `Dockerfile` local no seu repositório, o arquivo precisa ser nomeado `Dockerfile` e você precisa usar um caminho relativo ao arquivo de metadados da ação. O aplicativo `docker` executará esse arquivo.

### `runs.env`

**Opcional** Especifica um mapa de chave/valor das variáveis do ambiente a serem definidas no ambiente do contêiner.

### `runs.entrypoint`

**Opcional** Substitui o `ENTRYPOINT` do Docker no `Dockerfile` ou define-o caso ainda não tenha sido especificado. Use `entrypoint` quando `Dockerfile` não especificar um `ENTRYPOINT` ou você desejar substituir a instrução `ENTRYPOINT`. Se você omitir `entrypoint`, os comandos especificados na instrução `ENTRYPOINT` do Docker serão executados. A instrução `ENTRYPOINT` do Docker tem um formulário de *shell* e um formulário de *execução*. A documentação de `ENTRYPOINT` do Docker recomenda o uso da forma *exec* da instrução `ENTRYPOINT`.

Para obter mais informações sobre como `entrypoint` é executado, confira [Suporte do Dockerfile para GitHub Actions](dockerfile-support.md#entrypoint).

### `runs.post-entrypoint`

**Opcional** Permite executar um script de limpeza depois que a ação `runs.entrypoint` for concluída.
GitHub Actions usa `docker run` para iniciar essa ação. Como GitHub Actions executa o script dentro de um novo contêiner usando a mesma imagem base, o estado do runtime é diferente do contêiner principal `entrypoint` . Você pode acessar qualquer estado necessário tanto no workspace, `HOME`, quanto como uma variável `STATE_`. A ação `post-entrypoint:` sempre é executada por padrão, mas você pode substituir isso usando [`runs.post-if`](#runspost-if).

```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - 'bzz'
  entrypoint: 'main.sh'
  post-entrypoint: 'cleanup.sh'
```

### `runs.args`

**Opcional** Uma matriz de cadeias de caracteres que define as entradas de um contêiner do Docker. As entradas podem incluir strings com codificação rígida.               O GitHub passa o `args` para o `ENTRYPOINT` do contêiner quando o contêiner é iniciado.

Os `args` são usados no lugar da instrução `CMD` em um `Dockerfile`. Se você usar `CMD` no `Dockerfile`, use as diretrizes ordenadas por preferência:

1. Documente os argumentos necessários no README da ação e omita-os da instrução `CMD`.
2. Use padrões que permitam o uso da ação sem a especificação de `args`.
3. Se a ação expuser um sinalizador `--help` ou algo semelhante, use-o para tornar a ação autodocumentada.

Se você precisar passar variáveis de ambiente para uma ação, certifique-se de que sua ação executa um shell de comando para realizar a substituição de variáveis. Por exemplo, se o atributo `entrypoint` estiver definido como `"sh -c"`, `args` será executado em um shell de comando. Como alternativa, se o `Dockerfile` usar um `ENTRYPOINT` para executar o mesmo comando (`"sh -c"`), `args` será executado em um shell de comando.

Para obter mais informações sobre como usar a instrução `CMD` com GitHub Actions, consulte [Suporte do Dockerfile para GitHub Actions](dockerfile-support.md#cmd).

#### Exemplo: Definir argumentos para o contêiner do Docker

```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.greeting }}
    - 'foo'
    - 'bar'
```

## `branding`

**Opcional** Você pode usar uma cor e um ícone [Feather](https://feathericons.com/) para criar um distintivo para personalizar e distinguir sua ação. Os selos são mostrados ao lado do nome da ação em [GitHub Marketplace](https://github.com/marketplace?type=actions).

### Exemplo: Configurar a marca para uma ação

```yaml
branding:
  icon: 'award'
  color: 'green'
```

### `branding.color`

Cor de fundo do selo. Pode ser: `white`, `black`, `yellow`, `blue`, `green`, `orange`, `red`, `purple` ou `gray-dark`.

### `branding.icon`

O nome do ícone de [Pena](https://feathericons.com/) v4.28.0 a ser usado.

#### Ícones omitidos

Os ícones de marca, e todos os ícones a seguir, são omitidos.

- café
- colunas
- divide-circle
- divide-square
- dividir
- frown
- hexágono
- chave
- meh
- ponteiro do mouse
- sorriso
- ferramenta
- x-octagon

#### Lista completa de todos os ícones com suporte no momento

<!--
  This list should match the icon list in `app/models/repository_actions/icons.rb` in the internal github repo.
  To support a new icon, update `app/models/repository_actions/icons.rb` and add the svg to `/static/images/icons/feather` in the internal github repo.
-->

- atividade
- frequência de execução
- alerta-círculo
- alerta-octagon
- triângulo de alerta
- alinhar-centro
- alinhar-justificar
- alinhar-esquerda
- alinhar-direita
- âncora
- abertura
- arquivar
- círculo com flecha para baixo
- flecha-abaixo-esquerda
- flecha-abaixo-direita
- flecha-abaixo
- flecha-esquerda-círculo
- flecha-esquerda
- flecha-direita-círculo
- flecha-direita
- flecha-acima-círculo
- flecha-acima-esquerda
- flecha-acima-direita
- arrow-up
- arroba
- prêmio
- barra-quadro-2
- gráfico de barras
- carregamento da bateria
- bateria
- sino-desativado
- campainha
- bluetooth
- negrito
- livro-aberto
- livro
- indicador
- box
- pasta
- calendário
- câmera-desligada
- câmera
- conversão
- círculo de verificação
- marcar-quadrado
- verificação
- chevron-abaixo
- Chevron à esquerda
- chevron-direita
- chevron-acima
- chevrons-abaixo
- chevrons-esquerda
- chevrons-direita
- chevrons-acima
- círculo
- área de transferência
- relógio
- nuvem-chuvisco
- nuvem-relâmpago
- nuvem-desativada
- nuvem-chuva
- nuvem-neve
- nuvem
- codificar
- comando
- compass
- copiar
- canto-abaixo-esquerda
- canto-abaixo-direita
- canto-esquerda-abaixo
- canto-esquerda-acima
- canto-direita-abaixo
- canto-direita-acima
- canto-acima-esquerda
- canto-acima-direita
- cpu
- cartão-de-crédito
- cortar
- mira
- banco de dados
- excluir
- disco
- sinal de dólar
- download-nuvem
- baixar
- droplet
- editar-2
- editar-3
- edição
- link-externo
- olho-fechado
- olho
- avançar rapidamente
- pena
- arquivo-menos
- arquivo-plus
- arquivo-texto
- arquivo
- filme
- filtro
- sinalizador
- pasta-menos
- pasta-mais
- pasta
- presente
- git-branch
- git-commit
- git-merge
- git-pull-request (solicitação de pull do Git)
- globo
- grade
- disco-rígido
- hash
- fones-de-ouvido
- coração
- círculo de ajuda
- página inicial
- imagem
- caixa de entrada
- informações
- itálico
- camadas
- layout
- boia salva-vidas
- link-2
- link
- lista
- carregador
- bloquear
- log-in
- log-out
- email
- fixar-mapa
- mapa
- maximizar-2
- maximizar
- menu
- círculo de mensagens
- mensagem-quadrado
- microfone-desligado
- Microfone
- minimizar-2
- minimizar
- menos-círculo
- menos-quadrado
- negativo
- monitor
- lua
- mais horizontal
- mais-vertical
- move
- música
- navegação-2
- navegação
- octágono
- pacote
- clipe de papel
- ícone de pausa
- pausar
- por cento
- chamada-telefônica
- telefone-transferência
- telefone-entrada
- telefone-perdido
- telefone-desligado
- telefone-fora
- telefone
- gráfico-pizza
- reproduzir-círculo
- executar
- mais-círculo
- mais-quadrado
- mais
- bolso
- potência
- impressora
- rádio
- atualizar-ccw
- atualizar cw
- repetir
- retroceder
- girar-ccw
- girar-cw
- rss
- Salvar
- tesoura
- busca
- enviar
- servidor
- configurações
- compartilhar-2
- compartilhamento
- escudo-desabilitado
- escudo
- sacola-de-compras
- carrinho-de-compras
- shuffle
- barra lateral
- pular-atrás
- pular-frente
- slash
- controles deslizantes
- smartphone
- alto-falante
- square
- estrela
- círculo de parada
- sol
- nascer-do-sol
- pôr do sol
- tabela
- tablet
- marca
- destino
- terminal
- termômetro
- polegar-para-baixo
- polegar-para-cima
- alternar-esquerda
- alternar-direita
- lixeira-2
- jogar no lixo
- tendência de queda
- tendência de alta
- triângulo
- caminhão
- tv
- tipo
- guarda-chuva
- sublinhado
- desbloquear
- enviar para a nuvem
- carregamento
- usuário-marcar
- usuário-menos
- usuário premium
- usuário-x
- usuário
- usuários
- vídeo-desligado
- vídeo
- correio de voz
- volume-1
- volume-2
- volume-x
- volume
- inspeção
- wifi-desligado
- wifi
- vento
- x-círculo
- x-quadrado
- x
- zapear-desligado
- zap
- ampliar
- afastar

## Alterando o nome do arquivo de metadados

Embora o arquivo de metadados de ações seja compatível com ambos os formatos YAML, alterar o nome do arquivo de metadados (de `action.yml` para `action.yaml` ou vice-versa) entre versões afetará as versões anteriores da release que foram publicadas em GitHub Marketplace. Alterar o nome do arquivo ocultará todas as versões de lançamento associadas ao nome de arquivo anterior de GitHub Marketplace. As versões anteriores ainda estarão acessíveis para os usuários por meio do repositório de origem.

Ao lançar novas versões de ações, somente as versões lançadas após a alteração do nome do arquivo de metadados terão a tag GitHub Marketplace e serão exibidas em GitHub Marketplace
