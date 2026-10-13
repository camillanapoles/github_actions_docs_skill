---
title: Criando uma ação de JavaScript
description: Neste tutorial, você aprenderá como criar uma ação JavaScript usando o conjunto de ferramentas de ações.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/create-actions/create-a-javascript-action
captured: '2026-10-13'
section: Tutorials / Create actions
---

# Criando uma ação de JavaScript

_Neste tutorial, você aprenderá como criar uma ação JavaScript usando o conjunto de ferramentas de ações._

## Introdução

Neste guia, você aprenderá os componentes básicos necessários para criar e usar uma ação JavaScript empacotada. Para manter o foco deste guia nos componentes necessários para empacotar a ação, a funcionalidade do código da ação é mínima. A ação imprime "Olá, mundo" nos registros ou "Olá, \[who-to-greet]", se você fornecer um nome personalizado.

Este guia usa o GitHub Actions módulo Node.js do Kit de Ferramentas para acelerar o desenvolvimento. Para obter mais informações, confira o repositório [actions/toolkit](https://github.com/actions/toolkit).

Ao terminar esse projeto, você entenderá como criar sua própria ação JavaScript e poderá testá-la em um fluxo de trabalho.

Para garantir que suas ações de JavaScript sejam compatíveis com todos os executores hospedados no GitHub (Ubuntu, Windows e macOS), o código JavaScript empacotado que você escreve deve ser JavaScript puro e não depender de outros binários. As ações JavaScript são executadas diretamente no executor e usam binários que já existem na imagem do executor.

!!! warning
    Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

## Pré-requisitos

Antes de começar, você precisará baixar Node.js e criar um repositório público GitHub .

1. Baixe e instale Node.js 24.x, que inclui npm.

   <https://nodejs.org/en/download/>

2. Crie um novo repositório GitHub público e chame-o de "hello-world-javascript-action". Para saber mais, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

3. Clone o repositório para seu computador. Para saber mais, confira [Clonar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository).

4. No seu terminal, mude os diretórios para seu novo repositório.

            ```shell copy
   cd hello-world-javascript-action
   ```

5. No terminal, inicialize o diretório com o npm para gerar um arquivo `package.json`.

            ```shell copy
   npm init -y
   ```

## Criar um arquivo de metadados de ação

Crie um arquivo chamado `action.yml` no diretório `hello-world-javascript-action` com o código de exemplo a seguir. Para saber mais, confira [Referência de sintaxe de metadados](../../reference/workflows-and-actions/metadata-syntax.md).

```yaml copy
name: Hello World
description: Greet someone and record the time

inputs:
  who-to-greet: # id of input
    description: Who to greet
    required: true
    default: World

outputs:
  time: # id of output
    description: The time we greeted you

runs:
  using: node24
  main: dist/index.js
```

Esse arquivo define a entrada `who-to-greet` e a saída `time`. O arquivo também diz ao executor da ação como começar a executar essa ação JavaScript.

## Adicionar pacotes de ferramentas de ações

O conjunto de ferramentas de ações é uma coleção de pacotes Node.js que permite a rápida criação de ações JavaScript com mais consistência.

O pacote [`@actions/core`](https://github.com/actions/toolkit/tree/main/packages/core) do kit de ferramentas fornece uma interface para os comandos de fluxo de trabalho, variáveis de entrada e saída, status de saída e mensagens de depuração.

O kit de ferramentas também oferece um pacote [`@actions/github`](https://github.com/actions/toolkit/tree/main/packages/github) que retorna um cliente REST Octokit autenticado e acesso a contextos de GitHub Actions.

O kit de ferramentas oferece mais do que os pacotes `core` e `github`. Para obter mais informações, confira o repositório [actions/toolkit](https://github.com/actions/toolkit).

No terminal, instale os pacotes `core` e `github` do kit de ferramentas de ações.

```shell copy
npm install @actions/core @actions/github
```

Agora você deve ver um diretório `node_modules` e um arquivo `package-lock.json` que acompanham as dependências instaladas e suas versões. Você não deve confirmar o diretório `node_modules` em seu repositório.

## Gravar um código de ação

Essa ação usa o kit de ferramentas para obter a variável de entrada `who-to-greet` obrigatória no arquivo de metadados da ação e imprime "Olá, \[quem deve ser saudado]" em uma mensagem de depuração no log. Na sequência, o script obtém a hora atual e a configura como uma variável de saída que pode ser usada pelas ações executadas posteriormente em um trabalho.

GitHub Actions fornece informações de contexto sobre o evento de webhook, as referências do Git, o workflow, a ação e a pessoa que acionou o workflow. Para acessar as informações de contexto, use o pacote `github`. A ação que você vai escrever imprimirá a carga do evento webhook no log.

Adicione um novo arquivo chamado `src/index.js` com o código a seguir.

```javascript copy
import * as core from "@actions/core";
import * as github from "@actions/github";

try {
  // `who-to-greet` input defined in action metadata file
  const nameToGreet = core.getInput("who-to-greet");
  core.info(`Hello ${nameToGreet}!`);

  // Get the current time and set it as an output variable
  const time = new Date().toTimeString();
  core.setOutput("time", time);

  // Get the JSON webhook payload for the event that triggered the workflow
  const payload = JSON.stringify(github.context.payload, undefined, 2);
  core.info(`The event payload: ${payload}`);
} catch (error) {
  core.setFailed(error.message);
}
```

Se um erro for gerado no exemplo `index.js` acima, `core.setFailed(error.message);` usa o pacote [`@actions/core`](https://github.com/actions/toolkit/tree/main/packages/core) do kit de ferramentas de ações para registrar uma mensagem e definir um código de saída falho. Para saber mais, confira [Definindo códigos de saída para ações](../../how-tos/create-and-publish-actions/set-exit-codes.md).

## Criando um README

Para que as pessoas saibam como usar sua ação, você pode criar um arquivo README. Um arquivo README é útil quando você planeja compartilhar publicamente sua ação, mas também é uma ótima maneira de lembrá-lo ou sua equipe sobre como usar a ação.

No diretório `hello-world-javascript-action`, crie um arquivo `README.md` que especifica as seguintes informações:

* Uma descrição detalhada do que a ação faz.
* Argumentos de entrada e saída obrigatórios.
* Argumentos de entrada e saída opcionais.
* Segredos que a ação usa.
* Variáveis de ambiente que a ação usa.
* Um exemplo de como usar sua ação em um fluxo de trabalho.

````markdown copy
````
# Hello world JavaScript action

This action prints "Hello World" or "Hello" + the name of a person to greet to the log.

## Inputs

### `who-to-greet`

**Required** The name of the person to greet. Default `"World"`.

## Outputs

### `time`

The time we greeted you.

## Example usage

```yaml
uses: actions/hello-world-javascript-action@e76147da8e5c81eaf017dede5645551d4b94427b
with:
  who-to-greet: Mona the Octocat
```
````

````
## Faça commit, tag e push da sua ação

GitHub baixa cada ação executada em um fluxo de trabalho durante o runtime e executa-a como um pacote completo de código antes que você possa usar comandos de fluxo de trabalho como `run` interagir com o computador executor. Isso significa que você deve incluir quaisquer dependências de pacotes necessárias para executar o código JavaScript. Por exemplo, essa ação usa pacotes `@actions/core` e `@actions/github`.

Realizar o check-in do diretório `node_modules` pode causar problemas. Como alternativa, você pode usar ferramentas como [`rollup.js`](https://github.com/rollup/rollup) ou [`@vercel/ncc`](https://github.com/vercel/ncc) para combinar seu código e dependências em um arquivo para distribuição.

1. Instale `rollup` e seus plug-ins executando esse comando em seu terminal.

   `npm install --save-dev rollup @rollup/plugin-commonjs @rollup/plugin-node-resolve`

2. Crie um arquivo chamado `rollup.config.js` na raiz do repositório com o código a seguir.

            ```javascript copy
   import commonjs from "@rollup/plugin-commonjs";
   import { nodeResolve } from "@rollup/plugin-node-resolve";

   const config = {
     input: "src/index.js",
     output: {
       esModule: true,
       file: "dist/index.js",
       format: "es",
       sourcemap: true,
     },
     plugins: [commonjs(), nodeResolve({ preferBuiltins: true })],
   };

   export default config;
   ```

3. Compile o arquivo `dist/index.js`.

   `rollup --config rollup.config.js`

   Você verá um novo arquivo `dist/index.js` com seu código e todas as dependências.

4. No terminal, confirme as atualizações.

            ```shell copy
   git add src/index.js dist/index.js rollup.config.js package.json package-lock.json README.md action.yml
   git commit -m "Initial commit of my first action"
   git tag -a -m "My first action release" v1.1
   git push --follow-tags
   ```

Quando você confirma e envia o código por push, o repositório atualizado deve ter esta aparência:

```text
hello-world-javascript-action/
├── action.yml
├── dist/
│   └── index.js
├── package.json
├── package-lock.json
├── README.md
├── rollup.config.js
└── src/
    └── index.js
```

## Testar sua ação em um fluxo de trabalho

Agora você está pronto para testar sua ação em um fluxo de trabalho.

As ações públicas podem ser usadas por fluxos de trabalho em qualquer repositório. Quando uma ação está em um repositório privado, as configurações do repositório determinam se a ação está disponível somente dentro do mesmo repositório ou também para outros repositórios pertencentes à mesma  corporativa. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

### Exemplo usando uma ação pública

Este exemplo demonstra como sua nova ação pública pode ser executada dentro de um repositório externo.

Copie o YAML a seguir em um novo arquivo em `.github/workflows/main.yml` e atualize a linha `uses: octocat/hello-world-javascript-action@1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b` com seu nome de usuário e o nome do repositório público criado acima. Você também pode substituir a entrada `who-to-greet` pelo seu nome.

```yaml copy
on:
  push:
    branches:
      - main

jobs:
  hello_world_job:
    name: A job to say hello
    runs-on: ubuntu-latest

    steps:
      - name: Hello world action step
        id: hello
        uses: octocat/hello-world-javascript-action@1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b
        with:
          who-to-greet: Mona the Octocat

      # Use the output from the `hello` step
      - name: Get the output time
        run: echo "The time was ${{ steps.hello.outputs.time }}"
```

Quando esse fluxo de trabalho for disparado, o executor baixará a ação `hello-world-javascript-action` do repositório público e a executará.

### Exemplo usando uma ação privada

Copie o código de fluxo de trabalho em um arquivo `.github/workflows/main.yml` no repositório da ação. Você também pode substituir a entrada `who-to-greet` pelo seu nome.

```yaml copy
on:
  push:
    branches:
      - main

jobs:
  hello_world_job:
    name: A job to say hello
    runs-on: ubuntu-latest

    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v6

      - name: Hello world action step
        uses: ./ # Uses an action in the root directory
        id: hello
        with:
          who-to-greet: Mona the Octocat

      # Use the output from the `hello` step
      - name: Get the output time
        run: echo "The time was ${{ steps.hello.outputs.time }}"
```

No repositório, clique na guia **Ações** e selecione a execução mais recente do fluxo de trabalho. Em **Trabalhos** ou no grafo de visualização, clique em **Um trabalho para dizer olá**.

Clique em **Etapa da ação Olá, mundo** e você verá "Olá, Mona, o Octocat" ou o nome usado para a entrada `who-to-greet` impresso no log. Para ver o carimbo de data/hora, clique em **Obter a hora da saída**.

## Repositórios de modelos para criar ações javaScript

GitHub fornece repositórios de modelo para criar ações JavaScript e TypeScript. Você pode usar esses modelos para começar rapidamente a criar uma nova ação que inclui testes, lint e outras práticas recomendadas.

* [
  `javascript-action` repositório de modelo](https://github.com/actions/javascript-action)
* [
  `typescript-action` repositório de modelo](https://github.com/actions/typescript-action)

## Exemplo de ações javaScript em GitHub.com

Você pode encontrar muitos exemplos de ações JavaScript em GitHub.com.

* [DevExpress/testcafe-action](https://github.com/DevExpress/testcafe-action)
* [duckduckgo/privacy-configuration](https://github.com/duckduckgo/privacy-configuration)
