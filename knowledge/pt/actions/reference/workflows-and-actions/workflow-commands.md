---
title: Comandos de fluxo de trabalho para o GitHub Actions
description: Você pode usar comandos do fluxo de trabalho ao executar comandos do shell em um fluxo de trabalho ou no código de uma ação.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/workflow-commands
captured: '2026-10-11'
section: Reference / Workflows and actions
---

# Comandos de fluxo de trabalho para o GitHub Actions { #workflow-commands-for-github-actions }

_Você pode usar comandos do fluxo de trabalho ao executar comandos do shell em um fluxo de trabalho ou no código de uma ação._

## Sobre os comandos do fluxo de trabalho { #about-workflow-commands }

As ações podem comunicar-se com a máquina do executor para definir as variáveis de ambiente, valores de saída usados por outras ações, adicionar mensagens de depuração aos registros de saída e outras tarefas.

A maioria dos comandos do fluxo de trabalho usa o comando `echo` em um formato específico, enquanto outros são chamados pela gravação em um arquivo. Para obter mais informações, confira [Arquivos de ambiente](#environment-files).

### Exemplo de um comando de fluxo de trabalho { #example-of-a-workflow-command }

```bash copy
echo "::workflow-command parameter1={data},parameter2={data}::{command value}"
```

```powershell copy
Write-Output "::workflow-command parameter1={data},parameter2={data}::{command value}"
```

!!! note
    Os nomes de comandos de fluxo de trabalho e de parâmetros não diferenciam maiúsculas e minúsculas.

    [!WARNING]
    Se estiver usando um prompt de comando, omita os caracteres de aspas duplas (`"`) ao usar comandos do fluxo de trabalho.

## Usar comandos do fluxo de trabalho para acessar funções do kit de ferramentas { #using-workflow-commands-to-access-toolkit-functions }

O [actions/toolkit](https://github.com/actions/toolkit) inclui várias funções que podem ser executadas como comandos do fluxo de trabalho. Use a sintaxe `::` para executar os comandos do fluxo de trabalho no arquivo YAML. Em seguida, esses comandos são enviados ao executor por meio do `stdout`.

Por exemplo, em vez de usar código para criar uma anotação de erro, como abaixo:

```javascript copy
core.error('Missing semicolon', {file: 'app.js', startLine: 1})
```

### Exemplo: como criar uma anotação de erro { #example-creating-an-annotation-for-an-error }

Use o comando `error` no fluxo de trabalho para criar a mesma anotação de erro:

```yaml copy
      - name: Create annotation for build error
        run: echo "::error file=app.js,line=1::Missing semicolon"
```

```yaml copy
      - name: Create annotation for build error
        run: Write-Output "::error file=app.js,line=1::Missing semicolon"
```

A tabela a seguir mostra quais funções do conjunto de ferramentas estão disponíveis dentro de um fluxo de trabalho:

| Função do kit de ferramentas | Comando equivalente do fluxo de trabalho                        |
|----------------------------|---------------------------------------------------------------|
| `core.addPath`               | Acessível por meio do arquivo de ambiente `GITHUB_PATH`         |
| `core.debug`                 | `debug`                                                         |
| `core.notice`                | `notice`                                                        |
| `core.error`                 | `error`                                                         |
| `core.endGroup`              | `endgroup`                                                      |
| `core.exportVariable`        | Acessível por meio do arquivo de ambiente `GITHUB_ENV`          |
| `core.getInput`              | Acessível por meio da variável de ambiente `INPUT_{NAME}`       |
| `core.getState`              | Acessível por meio da variável de ambiente `STATE_{NAME}`       |
| `core.isDebug`               | Acessível por meio da variável de ambiente `RUNNER_DEBUG`       |
| `core.summary`               | Acessível por meio do arquivo de ambiente `GITHUB_STEP_SUMMARY` |
| `core.saveState`             | Acessível por meio do arquivo de ambiente `GITHUB_STATE`        |
| `core.setCommandEcho`        | `echo`                                                          |
| `core.setFailed`             | Usado como atalho para `::error` e `exit 1`                     |
| `core.setOutput`             | Acessível por meio do arquivo de ambiente `GITHUB_OUTPUT`       |
| `core.setSecret`             | `add-mask`                                                      |
| `core.startGroup`            | `group`                                                         |
| `core.warning`               | `warning`                                                       |

## Definindo uma mensagem de depuração { #setting-a-debug-message }

Imprime uma mensagem de erro no log. Você precisa criar um segredo chamado `ACTIONS_STEP_DEBUG` com o valor `true` para ver as mensagens de depuração definidas por esse comando no log. Para saber mais, confira [Habilitando o log de depuração](../../how-tos/monitor-workflows/enable-debug-logging.md).

```text copy
::debug::{message}
```

### Exemplo: definição de uma mensagem de depuração { #example-setting-a-debug-message }

```bash copy
echo "::debug::Set the Octocat variable"
```

```powershell copy
Write-Output "::debug::Set the Octocat variable"
```

## Configurando uma mensagem de aviso { #setting-a-notice-message }

Cria uma mensagem de aviso e a imprime no registro. Esta mensagem criará uma anotação, que pode associar a mensagem a um arquivo em particular no repositório. Opcionalmente, sua mensagem pode especificar uma posição dentro do arquivo.

```text copy
::notice file={name},line={line},endLine={endLine},title={title}::{message}
```

| Parâmetro   | Valor                            | Obrigatório | Padrão    |
|:----------|:-------------------------------|:----------|:--------|
| `title`     | Título personalizado             | Não         | Nenhum    |
| `file`      | Nome de arquivo                  | Não         | `.github` |
| `col`       | Número da coluna, começando em 1 | Não         | Nenhum    |
| `endColumn` | Número final da coluna           | Não         | Nenhum    |
| `line`      | Número de linha, começando em 1  | Não         | `1`       |
| `endLine`   | Número final da linha            | Não         | `1`       |

### Exemplo: definição de uma mensagem de aviso { #example-setting-a-notice-message }

```bash copy
echo "::notice file=app.js,line=1,col=5,endColumn=7::Missing semicolon"
```

```powershell copy
Write-Output "::notice file=app.js,line=1,col=5,endColumn=7,title=YOUR-TITLE::Missing semicolon"
```

## Configurar uma mensagem de aviso { #setting-a-warning-message }

Cria uma mensagem de aviso e a imprime no log. Esta mensagem criará uma anotação, que pode associar a mensagem a um arquivo em particular no repositório. Opcionalmente, sua mensagem pode especificar uma posição dentro do arquivo.

```text copy
::warning file={name},line={line},endLine={endLine},title={title}::{message}
```

| Parâmetro   | Valor                            | Obrigatório | Padrão    |
|:----------|:-------------------------------|:----------|:--------|
| `title`     | Título personalizado             | Não         | Nenhum    |
| `file`      | Nome de arquivo                  | Não         | `.github` |
| `col`       | Número da coluna, começando em 1 | Não         | Nenhum    |
| `endColumn` | Número final da coluna           | Não         | Nenhum    |
| `line`      | Número de linha, começando em 1  | Não         | `1`       |
| `endLine`   | Número final da linha            | Não         | `1`       |

### Exemplo: definição de uma mensagem de aviso { #example-setting-a-warning-message }

```bash copy
echo "::warning file=app.js,line=1,col=5,endColumn=7,title=YOUR-TITLE::Missing semicolon"
```

```powershell copy
Write-Output "::warning file=app.js,line=1,col=5,endColumn=7,title=YOUR-TITLE::Missing semicolon"
```

## Configurar uma mensagem de erro { #setting-an-error-message }

Cria uma mensagem de erro e a imprime no log. Esta mensagem criará uma anotação, que pode associar a mensagem a um arquivo em particular no repositório. Opcionalmente, sua mensagem pode especificar uma posição dentro do arquivo.

```text copy
::error file={name},line={line},endLine={endLine},title={title}::{message}
```

| Parâmetro   | Valor                            | Obrigatório | Padrão    |
|:----------|:-------------------------------|:----------|:--------|
| `title`     | Título personalizado             | Não         | Nenhum    |
| `file`      | Nome de arquivo                  | Não         | `.github` |
| `col`       | Número da coluna, começando em 1 | Não         | Nenhum    |
| `endColumn` | Número final da coluna           | Não         | Nenhum    |
| `line`      | Número de linha, começando em 1  | Não         | `1`       |
| `endLine`   | Número final da linha            | Não         | `1`       |

### Exemplo: definição de uma mensagem de erro { #example-setting-an-error-message }

```bash copy
echo "::error file=app.js,line=1,col=5,endColumn=7,title=YOUR-TITLE::Missing semicolon"
```

```powershell copy
Write-Output "::error file=app.js,line=1,col=5,endColumn=7,title=YOUR-TITLE::Missing semicolon"
```

## Agrupar linhas de log { #grouping-log-lines }

Cria um grupo expansível no registro. Para criar um grupo, use o comando `group` e especifique um `title`. Qualquer coisa que você imprimir no log entre os comandos `group` e `endgroup` estará aninhada dentro de uma entrada expansível no log.

```text copy
::group::{title}
::endgroup::
```

### Exemplo: agrupamento de linhas de log { #example-grouping-log-lines }

```yaml copy
jobs:
  bash-example:
    runs-on: ubuntu-latest
    steps:
      - name: Group of log lines
        run: |
            echo "::group::My title"
            echo "Inside group"
            echo "::endgroup::"
```

```yaml copy
jobs:
  powershell-example:
    runs-on: windows-latest
    steps:
      - name: Group of log lines
        run: |
            Write-Output "::group::My title"
            Write-Output "Inside group"
            Write-Output "::endgroup::"
```

![Captura de tela do log da etapa de fluxo de trabalho. A segunda linha, "Meu título", é um grupo expandido. A próxima linha, "Dentro do grupo", está indentada abaixo.](/assets/images/help/actions/actions-log-group.png)

## Como mascarar um valor em um registro { #masking-a-value-in-a-log }

```text copy
::add-mask::{value}
```

Mascarar um valor evita que uma string ou variável seja impressa no log. Cada palavra mascarada separada por um espaço em branco é substituída pelo caractere `*`. Use uma variável de ambiente ou uma cadeia de caracteres para o `value` da máscara. Esse processo deve ser feito uma vez por valor por trabalho. Quando você mascara um valor, ele é tratado como um segredo e será redigido no executor. Por exemplo, depois de mascarar um valor, você não poderá definir esse valor como uma saída.

### Exemplo: mascaramento de uma cadeia de caracteres { #example-masking-a-string }

Ao imprimir `"Mona The Octocat"` no log, você verá `"***"`.

```bash copy
echo "::add-mask::Mona The Octocat"
```

```powershell copy
Write-Output "::add-mask::Mona The Octocat"
```

!!! warning
    Registre o segredo com ‘add-mask’ antes de enviá-lo aos logs de build ou usá-lo em comandos de outro fluxo de trabalho.

### Exemplo: mascaramento de uma variável de ambiente { #example-masking-an-environment-variable }

Ao imprimir a variável `MY_NAME` ou o valor `"Mona The Octocat"` no log, você verá `"***"` em vez de `"Mona The Octocat"`.

```yaml copy
jobs:
  bash-example:
    runs-on: ubuntu-latest
    env:
      MY_NAME: "Mona The Octocat"
    steps:
      - name: bash-version
        run: echo "::add-mask::$MY_NAME"
```

```yaml copy
jobs:
  powershell-example:
    runs-on: windows-latest
    env:
      MY_NAME: "Mona The Octocat"
    steps:
      - name: powershell-version
        run: Write-Output "::add-mask::$env:MY_NAME"
```

### Exemplo: mascarar uma saída gerada em um único trabalho { #example-masking-a-generated-output-within-a-single-job }

Se você não precisar passar seu segredo de um trabalho para outro, poderá:

1. Gerar o segredo (sem transmiti-lo).
2. Mascarar com `add-mask`.
3. Usar `GITHUB_OUTPUT` para disponibilizar o segredo para outras etapas dentro do trabalho.

```yaml copy
on: push
jobs:
  generate-a-secret-output:
    runs-on: ubuntu-latest
    steps:
      - id: sets-a-secret
        name: Generate, mask, and output a secret
        run: |
          the_secret=$((RANDOM))
          echo "::add-mask::$the_secret"
          echo "secret-number=$the_secret" >> "$GITHUB_OUTPUT"
      - name: Use that secret output (protected by a mask)
        run: |
          echo "the secret number is ${{ steps.sets-a-secret.outputs.secret-number }}"
```

```yaml copy
on: push
jobs:
  generate-a-secret-output:
    runs-on: ubuntu-latest
    steps:
      - id: sets-a-secret
        name: Generate, mask, and output a secret
        shell: pwsh
        run: |
          Set-Variable -Name TheSecret -Value (Get-Random)
          Write-Output "::add-mask::$TheSecret"
          "secret-number=$TheSecret" >> $env:GITHUB_OUTPUT
      - name: Use that secret output (protected by a mask)
        shell: pwsh
        run: |
          Write-Output "the secret number is ${{ steps.sets-a-secret.outputs.secret-number }}"
```

### Exemplo: mascarar e passar um segredo entre trabalhos ou fluxos de trabalho { #example-masking-and-passing-a-secret-between-jobs-or-workflows }

Se você quiser passar um segredo mascarado entre trabalhos ou fluxos de trabalho, deverá armazená-lo em um repositório e recuperá-lo no trabalho ou fluxo de trabalho subsequente.

#### Instalação { #setup }

1. Configure um repositório secreto para armazenar o segredo que você gerará durante o fluxo de trabalho. Por exemplo, Vault.
2. Gere uma chave para leitura e gravação nesse repositório secreto. Armazene a chave como um segredo do repositório. No fluxo de trabalho no exemplo a seguir, o nome do segredo é `SECRET_STORE_CREDENTIALS`. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md).

#### Workflow

!!! note
    Esse fluxo de trabalho usa um repositório de segredos imaginário, `secret-store`, que tem os comandos imaginários `store-secret` e `retrieve-secret`.
    `some/secret-store@ 27b31702a0e7fc50959f5ad993c78deac1bdfc29` é uma ação imaginária que instala o aplicativo `secret-store` e o configura para se conectar a um `instance` com `credentials`.

```yaml copy
on: push

jobs:
  secret-generator:
    runs-on: ubuntu-latest
    outputs:
      handle: ${{ steps.generate-secret.outputs.handle }}
    steps:
    - uses: some/secret-store@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        credentials: ${{ secrets.SECRET_STORE_CREDENTIALS }}
        instance: ${{ secrets.SECRET_STORE_INSTANCE }}
    - name: generate secret
      id: generate-secret
      shell: bash
      run: |
        GENERATED_SECRET=$((RANDOM))
        echo "::add-mask::$GENERATED_SECRET"
        SECRET_HANDLE=$(secret-store store-secret "$GENERATED_SECRET")
        echo "handle=$SECRET_HANDLE" >> "$GITHUB_OUTPUT"
  secret-consumer:
    runs-on: macos-latest
    needs: secret-generator
    steps:
    - uses: some/secret-store@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        credentials: ${{ secrets.SECRET_STORE_CREDENTIALS }}
        instance: ${{ secrets.SECRET_STORE_INSTANCE }}
    - name: use secret
      shell: bash
      run: |
        SECRET_HANDLE="${{ needs.secret-generator.outputs.handle }}"
        RETRIEVED_SECRET=$(secret-store retrieve-secret "$SECRET_HANDLE")
        echo "::add-mask::$RETRIEVED_SECRET"
        echo "We retrieved our masked secret: $RETRIEVED_SECRET"
```

```yaml copy
on: push

jobs:
  secret-generator:
    runs-on: ubuntu-latest
    steps:
    - uses: some/secret-store@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        credentials: ${{ secrets.SECRET_STORE_CREDENTIALS }}
        instance: ${{ secrets.SECRET_STORE_INSTANCE }}
    - name: generate secret
      shell: pwsh
      run: |
        Set-Variable -Name Generated_Secret -Value (Get-Random)
        Write-Output "::add-mask::$Generated_Secret"
        Set-Variable -Name Secret_Handle -Value (Store-Secret "$Generated_Secret")
        "handle=$Secret_Handle" >> $env:GITHUB_OUTPUT
  secret-consumer:
    runs-on: macos-latest
    needs: secret-generator
    steps:
    - uses: some/secret-store@27b31702a0e7fc50959f5ad993c78deac1bdfc29
      with:
        credentials: ${{ secrets.SECRET_STORE_CREDENTIALS }}
        instance: ${{ secrets.SECRET_STORE_INSTANCE }}
    - name: use secret
      shell: pwsh
      run: |
        Set-Variable -Name Secret_Handle -Value "${{ needs.secret-generator.outputs.handle }}"
        Set-Variable -Name Retrieved_Secret -Value (Retrieve-Secret "$Secret_Handle")
        echo "::add-mask::$Retrieved_Secret"
        echo "We retrieved our masked secret: $Retrieved_Secret"
```

## Parar e iniciar os comandos no fluxo de trabalho { #stopping-and-starting-workflow-commands }

Para de processar quaisquer comandos de fluxo de trabalho. Esse comando especial permite fazer o registro do que você desejar sem executar um comando do fluxo de trabalho acidentalmente. Por exemplo, é possível interromper o registro para exibir um script completo com comentários.

```text copy
::stop-commands::{endtoken}
```

Para interromper o processamento de comandos do fluxo de trabalho, transmita um token único para `stop-commands`. Para retomar os comandos do fluxo de trabalho, passe o mesmo token que você usou para parar os comandos do fluxo de trabalho.

!!! warning
    Verifique se o token que você está usando é gerado aleatoriamente e exclusivo para cada execução.

```text copy
::{endtoken}::
```

### Exemplo: interrupção e inicialização de comandos do fluxo de trabalho { #example-stopping-and-starting-workflow-commands }

```yaml copy
jobs:
  workflow-command-job:
    runs-on: ubuntu-latest
    steps:
      - name: Disable workflow commands
        run: |
          echo '::warning:: This is a warning message, to demonstrate that commands are being processed.'
          stopMarker=$(uuidgen)
          echo "::stop-commands::$stopMarker"
          echo '::warning:: This will NOT be rendered as a warning, because stop-commands has been invoked.'
          echo "::$stopMarker::"
          echo '::warning:: This is a warning again, because stop-commands has been turned off.'
```

```yaml copy
jobs:
  workflow-command-job:
    runs-on: windows-latest
    steps:
      - name: Disable workflow commands
        run: |
          Write-Output '::warning:: This is a warning message, to demonstrate that commands are being processed.'
          $stopMarker = New-Guid
          Write-Output "::stop-commands::$stopMarker"
          Write-Output '::warning:: This will NOT be rendered as a warning, because stop-commands has been invoked.'
          Write-Output "::$stopMarker::"
          Write-Output '::warning:: This is a warning again, because stop-commands has been turned off.'
```

## Enviar valores para as ações anterior e posterior { #sending-values-to-the-pre-and-post-actions }

Você pode criar variáveis de ambiente para compartilhamento com as ações `pre:` ou `post:` do fluxo de trabalho gravando no arquivo localizado em `GITHUB_STATE`. Por exemplo, você pode criar um arquivo com a ação `pre:`, transmitir a localização do arquivo para a ação `main:` e usar a ação `post:` para excluir o arquivo. Como alternativa, você pode criar um arquivo com a ação `main:`, transmitir a localização do arquivo para a ação `post:` e usar a ação `post:` para excluir o arquivo.

Se você tiver várias ações `pre:` ou `post:`, só poderá acessar o valor salvo na ação na qual ele foi gravado em `GITHUB_STATE`. Para obter mais informações sobre a ação `post:`, confira [Referência de sintaxe de metadados](metadata-syntax.md#runspost).

O arquivo `GITHUB_STATE` só está disponível dentro de uma ação. O valor salvo é armazenado como um valor de ambiente com o prefixo `STATE_`.

Este exemplo usa JavaScript para gravar no arquivo `GITHUB_STATE`. A variável de ambiente resultante é chamada `STATE_processID` com o valor de `12345`:

```javascript copy
import * as fs from 'fs'
import * as os from 'os'

fs.appendFileSync(process.env.GITHUB_STATE, `processID=12345${os.EOL}`, {
  encoding: 'utf8'
})
```

Em seguida, a variável `STATE_processID` fica disponível exclusivamente para o script de limpeza em execução na ação `main`. Este exemplo é executado em `main` e usa o JavaScript para exibir o valor atribuído à variável de ambiente `STATE_processID`:

```javascript copy
console.log("The running PID from the main action is: " + process.env.STATE_processID);
```

## Arquivos de ambiente { #environment-files }

Durante a execução de um fluxo de trabalho, o executor gera arquivos temporários que podem ser usados para executar certas ações. O caminho para esses arquivos pode ser acessado e editado usando as variáveis de ambiente padrão do GitHub. Confira [Referência de variáveis](variables.md#default-environment-variables). Você precisará usar a codificação UTF-8 ao escrever para esses arquivos para garantir o processamento adequado dos comandos. Vários comandos podem ser escritos no mesmo arquivo, separados por novas linhas.
Para usar variáveis de ambiente em uma GitHub Action, crie ou modifique arquivos `.env` usando comandos específicos do GitHub Actions.

Este é o procedimento:

```yaml copy
name: Example Workflow for Environment Files

on: push

jobs:
  set_and_use_env_vars:
    runs-on: ubuntu-latest
    steps:
      - name: Set environment variable
        run: echo "MY_ENV_VAR=myValue" >> $GITHUB_ENV

      - name: Use environment variable
        run: |
          echo "The value of MY_ENV_VAR is $MY_ENV_VAR"

```

Outro exemplo seria usá-las para armazenar metadados como carimbos de data/hora de build, SHAs de commit ou nomes de artefatos:

```yaml copy
steps:
  - name: Store build timestamp
    run: echo "BUILD_TIME=$(date +'%T')" >> $GITHUB_ENV

  - name: Deploy using stored timestamp
    run: echo "Deploying at $BUILD_TIME"
```

!!! note
    As versões 5.1 e inferior do PowerShell (`shell: powershell`) não usam o UTF-8 por padrão, ou seja, você precisa especificar a codificação UTF-8. Por exemplo:

                ```yaml copy
    jobs:
      legacy-powershell-example:
        runs-on: windows-latest
        steps:
          - shell: powershell
            run: |
              "mypath" | Out-File -FilePath $env:GITHUB_PATH -Encoding utf8 -Append
    ```

    As versões 6 e superior do PowerShell Core (`shell: pwsh`) usam UTF-8 por padrão. Por exemplo:

                ```yaml copy
    jobs:
      powershell-core-example:
        runs-on: windows-latest
        steps:
          - shell: pwsh
            run: |
              "mypath" >> $env:GITHUB_PATH
    ```

## Configurar uma variável de ambiente { #setting-an-environment-variable }

!!! note
    Para evitar problemas, é uma boa prática tratar as variáveis de ambiente como com diferenciação de maiúsculas e minúsculas, independentemente do comportamento do sistema operacional e do shell que você está usando.

```bash copy
echo "{environment_variable_name}={value}" >> "$GITHUB_ENV"
```

* Como usar o PowerShell versão 6 e superior:

        ```powershell copy
  "{environment_variable_name}={value}" >> $env:GITHUB_ENV
  ```

* Como usar o PowerShell versão 5.1 e inferior:

        ```powershell copy
  "{environment_variable_name}={value}" | Out-File -FilePath $env:GITHUB_ENV -Encoding utf8 -Append
  ```

Disponibilize uma variável de ambiente para todas as etapas posteriores em um trabalho de fluxo de trabalho definindo ou atualizando a variável de ambiente e gravando isso no arquivo de ambiente `GITHUB_ENV`. A etapa que cria ou atualiza a variável de ambiente não tem acesso ao novo valor, mas todos os passos subsequentes em um trabalho terão acesso.

Não é possível substituir o valor das variáveis de ambiente padrão chamadas `GITHUB_*` e `RUNNER_*`. Atualmente, você pode substituir o valor da variável `CI`. No entanto, não é garantido que isso sempre será possível. Para obter mais informações sobre as variáveis de ambiente padrão, consulte [Referência de variáveis](variables.md#default-environment-variables).

!!! note
    Devido a restrições de segurança, `GITHUB_ENV` não pode ser usado para definir a variável de ambiente `NODE_OPTIONS`.

### Exemplo de gravação de uma variável de ambiente em `GITHUB_ENV` { #example-of-writing-an-environment-variable-to-githubenv }

```yaml copy
steps:
  - name: Set the value
    id: step_one
    run: |
      echo "action_state=yellow" >> "$GITHUB_ENV"
  - name: Use the value
    id: step_two
    run: |
      printf '%s\n' "$action_state" # This will output 'yellow'
```

```yaml copy
steps:
  - name: Set the value
    id: step_one
    run: |
      "action_state=yellow" >> $env:GITHUB_ENV
  - name: Use the value
    id: step_two
    run: |
      Write-Output "$env:action_state" # This will output 'yellow'
```

### Strings de linha múltipla { #multiline-strings }

Para strings multilinha, você pode usar um delimitador com a seguinte sintaxe.

```text copy
{name}<<{delimiter}
{value}
{delimiter}
```

!!! warning
    Confira se o delimitador que você está usando não ocorre em uma linha separada dentro do valor. Se o valor for completamente arbitrário, você não deverá usar esse formato. Em vez disso, grave o valor em um arquivo.

#### Exemplo de uma cadeia de caracteres de várias linhas { #example-of-a-multiline-string }

Este exemplo usa `EOF` como delimitador e define a variável de ambiente `JSON_RESPONSE` como o valor da resposta `curl`.

```yaml copy
steps:
  - name: Set the value in bash
    id: step_one
    run: |
      {
        echo 'JSON_RESPONSE<<EOF'
        curl https://example.com
        echo EOF
      } >> "$GITHUB_ENV"
```

```yaml copy
steps:
  - name: Set the value in pwsh
    id: step_one
    run: |
      $EOF = (New-Guid).Guid
      "JSON_RESPONSE<<$EOF" >> $env:GITHUB_ENV
      (Invoke-WebRequest -Uri "https://example.com").Content >> $env:GITHUB_ENV
      "$EOF" >> $env:GITHUB_ENV
    shell: pwsh
```

## Definir um parâmetro de saída { #setting-an-output-parameter }

Define o parâmetro de saída de uma etapa. Observe que a etapa precisará de um `id` a ser definido para recuperar o valor de saída mais tarde. Você pode definir valores de saída de várias linhas com a mesma técnica usada na seção [Cadeias de caracteres de várias linhas](workflow-commands.md#multiline-strings) para definir variáveis de ambiente de várias linhas.

```bash copy
echo "{name}={value}" >> "$GITHUB_OUTPUT"
```

```powershell copy
"{name}=value" >> $env:GITHUB_OUTPUT
```

### Exemplo de definição de um parâmetro de saída { #example-of-setting-an-output-parameter }

Este exemplo demonstra como definir o parâmetro de saída `SELECTED_COLOR` e recuperá-lo mais tarde:

```yaml copy
      - name: Set color
        id: color-selector
        run: echo "SELECTED_COLOR=green" >> "$GITHUB_OUTPUT"
      - name: Get color
        env:
          SELECTED_COLOR: ${{ steps.color-selector.outputs.SELECTED_COLOR }}
        run: echo "The selected color is $SELECTED_COLOR"
```

Este exemplo demonstra como definir o parâmetro de saída `SELECTED_COLOR` e recuperá-lo mais tarde:

```yaml copy
      - name: Set color
        id: color-selector
        run: |
            "SELECTED_COLOR=green" >> $env:GITHUB_OUTPUT
      - name: Get color
        env:
          SELECTED_COLOR: ${{ steps.color-selector.outputs.SELECTED_COLOR }}
        run: Write-Output "The selected color is $env:SELECTED_COLOR"
```

## Adicionando um resumo de trabalho { #adding-a-job-summary }

```bash copy
echo "{markdown content}" >> $GITHUB_STEP_SUMMARY
```

```powershell copy
"{markdown content}" >> $env:GITHUB_STEP_SUMMARY
```

Você pode definir um Markdown personalizado para cada trabalho para que ele seja exibido na página de resumo de uma execução de fluxo de trabalho. Você pode usar resumos de trabalho para exibir e agrupar conteúdo exclusivo, como resumos de resultados de teste, para que alguém que exiba o resultado de uma execução de fluxo de trabalho não precise entrar nos logs para ver informações importantes relacionadas à execução, como falhas.

Os resumos de trabalho dão suporte ao [GitHub Flavored Markdown](https://github.github.com/gfm/), e você pode adicionar o conteúdo do Markdown para uma etapa ao arquivo do ambiente `GITHUB_STEP_SUMMARY`. O `GITHUB_STEP_SUMMARY` é exclusivo para cada etapa de um trabalho. Para mais informações sobre o arquivo por etapa que `GITHUB_STEP_SUMMARY` faz referência, confira [Arquivos de ambiente](#environment-files).

Quando um trabalho é concluído, os resumos de todas as etapas de um trabalho são agrupados em um único resumo de trabalho e são mostrados na página de resumo da execução do fluxo de trabalho. Se vários trabalhos gerarem resumos, os resumos do trabalho serão ordenados pelo tempo de conclusão do trabalho.

### Exemplo de adição de um resumo de trabalho { #example-of-adding-a-job-summary }

```bash copy
echo "### Hello world! :rocket:" >> $GITHUB_STEP_SUMMARY
```

```powershell copy
"### Hello world! :rocket:" >> $env:GITHUB_STEP_SUMMARY
```

![Captura de tela da página de resumo de uma execução de fluxo de trabalho. Em "resumo de exemplo", está "Olá, mundo!" e um emoji de foguete.](/assets/images/help/actions/actions-job-summary-simple-example.png)

### Conteúdo de Markdown de várias linhas { #multiline-markdown-content }

Para conteúdo de Markdown de várias linhas, você pode usar `>>` para acrescentar continuamente o conteúdo para a etapa atual. A cada operação de acréscimo, um caractere de nova linha é adicionado automaticamente.

#### Exemplo de conteúdo Markdown de várias linhas { #example-of-multiline-markdown-content }

```yaml
- name: Generate list using Markdown
  run: |
    echo "This is the lead in sentence for the list" >> $GITHUB_STEP_SUMMARY
    echo "" >> $GITHUB_STEP_SUMMARY # this is a blank line
    echo "- Lets add a bullet point" >> $GITHUB_STEP_SUMMARY
    echo "- Lets add a second bullet point" >> $GITHUB_STEP_SUMMARY
    echo "- How about a third one?" >> $GITHUB_STEP_SUMMARY
```

```yaml
- name: Generate list using Markdown
  run: |
    "This is the lead in sentence for the list" >> $env:GITHUB_STEP_SUMMARY
    "" >> $env:GITHUB_STEP_SUMMARY # this is a blank line
    "- Lets add a bullet point" >> $env:GITHUB_STEP_SUMMARY
    "- Lets add a second bullet point" >> $env:GITHUB_STEP_SUMMARY
    "- How about a third one?" >> $env:GITHUB_STEP_SUMMARY
```

### Substituir resumos de trabalho { #overwriting-job-summaries }

Para limpar todo o conteúdo da etapa atual, você pode usar `>` para substituir qualquer conteúdo adicionado anteriormente no Bash ou remover `-Append` no PowerShell

#### Exemplo de substituição de resumos de trabalho { #example-of-overwriting-job-summaries }

```yaml
- name: Overwrite Markdown
  run: |
    echo "Adding some Markdown content" >> $GITHUB_STEP_SUMMARY
    echo "There was an error, we need to clear the previous Markdown with some new content." > $GITHUB_STEP_SUMMARY
```

```yaml
- name: Overwrite Markdown
  run: |
    "Adding some Markdown content" >> $env:GITHUB_STEP_SUMMARY
    "There was an error, we need to clear the previous Markdown with some new content." >> $env:GITHUB_STEP_SUMMARY
```

### Removendo resumos de trabalho { #removing-job-summaries }

Para remover completamente um resumo da etapa atual, o arquivo que `GITHUB_STEP_SUMMARY` faz referência pode ser excluído.

#### Exemplo de remoção de resumos de trabalho { #example-of-removing-job-summaries }

```yaml
- name: Delete all summary content
  run: |
    echo "Adding Markdown content that we want to remove before the step ends" >> $GITHUB_STEP_SUMMARY
    rm $GITHUB_STEP_SUMMARY
```

```yaml
- name: Delete all summary content
  run: |
    "Adding Markdown content that we want to remove before the step ends" >> $env:GITHUB_STEP_SUMMARY
    Remove-Item $env:GITHUB_STEP_SUMMARY
```

Depois que uma etapa for concluída, os resumos de trabalho serão carregados e as etapas subsequentes não poderão modificar o conteúdo do Markdown carregado anteriormente. Os resumos mascaram automaticamente todos os segredos que podem ter sido adicionados acidentalmente. Se um resumo de trabalho contiver informações confidenciais que devem ser excluídas, você poderá excluir toda a execução do fluxo de trabalho para remover todos os resumos de trabalho. Para saber mais, confira [Excluir a execução de um fluxo de trabalho](../../how-tos/manage-workflow-runs/delete-a-workflow-run.md).

### Limites e isolamento de etapa { #step-isolation-and-limits }

Os resumos de trabalho são isolados entre as etapas e cada etapa é restrita a um tamanho máximo de 1MiB. O isolamento é imposto entre as etapas para que um Markdown potencialmente malformado de uma única etapa não possa interromper a renderização do Markdown para as etapas subsequentes. Se mais de 1MiB de conteúdo for adicionado a uma etapa, o upload da etapa falhará e uma anotação de erro será criada. Os problemas de upload de resumos de trabalho não afetam o status geral de uma etapa ou de um trabalho. No máximo 20 resumos de trabalho das etapas são exibidos por trabalho.

## Adicionar um caminho do sistema { #adding-a-system-path }

Insere um diretório antes da variável `PATH` do sistema e o disponibiliza automaticamente para todas as ações posteriores do trabalho atual. A ação atualmente em execução não pode acessar a variável de caminho atualizada. Para ver os caminhos atualmente definidos para seu trabalho, use `echo "$PATH"` em uma etapa ou uma ação.

### Exemplo de adição de um caminho do sistema { #example-of-adding-a-system-path }

Este exemplo demonstra como adicionar o diretório `$HOME/.local/bin` do usuário a `PATH`:

```bash copy
echo "$HOME/.local/bin" >> "$GITHUB_PATH"
```

Este exemplo demonstra como adicionar o diretório `$env:HOMEPATH/.local/bin` do usuário a `PATH`:

```powershell copy
"$env:HOMEPATH/.local/bin" | Out-File -FilePath "$env:GITHUB_PATH" -Append
```

## Declarando artefatos de fluxo de trabalho { #declaring-workflow-artifacts }

Declare arquivos ou referências de OCI como artefatos de fluxo de trabalho escrevendo uma declaração por linha no arquivo de `GITHUB_ARTIFACTS` ambiente. Cada etapa grava em um arquivo novo por etapa; o caminho é exclusivo para essa etapa.

Metadados sobre artefatos declarados são coletados em todas as etapas em um trabalho e expostos por meio do `GITHUB_ARTIFACTS_LIST` arquivo.

Cada linha deve ser um dos seguintes formatos. Linhas e linhas em branco começando com `#` são ignoradas.

* **Caminho do arquivo**: um caminho relativo ou absoluto para um arquivo, opcionalmente prefixado com `file://`. Caminhos relativos são resolvidos em relação `GITHUB_WORKSPACE`a . O caminho deve apontar para um arquivo regular existente (não um diretório). O executor registra o nome base do arquivo e seu resumo SHA-256.
* **Referência de OCI**: uma referência no formulário `REFERENCE@ALGORITHM:HEX`, opcionalmente prefixada com `oci://`.
  `REFERENCE` é o nome da imagem (incluindo a marca opcional) e `ALGORITHM` deve ser um de `sha256`, `sha384`ou `sha512`.
  `HEX` deve ser o resumo em minúsculas completo para o algoritmo: 64 caracteres hexadecimal para `sha256`, 96 para `sha384`, ou 128 para `sha512`.

Limites:

* O arquivo de comando por etapa é limitado a 1MiB.
* Um trabalho pode acumular até 500 artefatos de fluxo de trabalho em todas as etapas.
* Se o mesmo artefato for declarado mais de uma vez com nome e resumo idênticos, ele será duplicado. Declarações conflitantes (mesmo nome, resumo diferente) produzem um erro.

```bash copy
echo "dist/my-binary" >> "$GITHUB_ARTIFACTS"
```

Para declarar uma referência de OCI:

```bash copy
echo "oci://ghcr.io/octocat/myapp:1.0.0@sha256:914b38d45a65e4263a179d9c2b09cc04dcbcaa8257fa85100cf42f9a3b408cfb" >> "$GITHUB_ARTIFACTS"
```

```powershell copy
"dist/my-binary" >> $env:GITHUB_ARTIFACTS
```

Para declarar uma referência de OCI:

```powershell copy
"oci://ghcr.io/octocat/myapp:1.0.0@sha256:914b38d45a65e4263a179d9c2b09cc04dcbcaa8257fa85100cf42f9a3b408cfb" >> $env:GITHUB_ARTIFACTS
```

## Lendo artefatos de fluxo de trabalho { #reading-workflow-artifacts }

Leia os metadados de artefato de fluxo de trabalho agregado declarados por etapas anteriores no trabalho atual do `GITHUB_ARTIFACTS_LIST` arquivo de ambiente. Esse arquivo é somente leitura e é atualizado pelo executor após a conclusão de cada etapa. Ele contém um objeto JSON codificado em UTF-8 com a seguinte estrutura:

```json
{
  "version": 1,
  "subjects": [
    {
      "name": "my-binary",
      "digest": "sha256:abc123...",
      "kind": "file"
    },
    {
      "name": "ghcr.io/octocat/myapp:1.0.0",
      "digest": "sha256:a1b2c3d4...",
      "kind": "oci"
    }
  ]
}
```

Cada entrada na `subjects` matriz contém:

* `name`: o nome base do arquivo ou o nome de referência OCI (sem o resumo).
* `digest`: o `algorithm:hex` resumo do artefato.
* `kind`: `file` ou `oci`.

Artefatos são classificados em ordem alfabética por `name`.

```bash copy
cat "$GITHUB_ARTIFACTS_LIST"
```

```powershell copy
Get-Content $env:GITHUB_ARTIFACTS_LIST
```
