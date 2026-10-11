---
title: Criar uma ação composta
description: Neste tutorial, você aprenderá a criar uma ação composta.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/create-actions/create-a-composite-action
captured: '2026-10-11'
section: Tutorials / Create actions
---

# Criar uma ação composta

_Neste tutorial, você aprenderá a criar uma ação composta._

## Introdução

Neste guia, você aprenderá os componentes básicos necessários para criar e usar uma ação composta empacotada. Para manter o foco deste guia nos componentes necessários para empacotar a ação, a funcionalidade do código da ação é mínima. A ação imprime "Olá, Mundo" e depois "Adeus", ou se você fornecer um nome personalizado, ela imprime "Olá \[quem cumprimentar]" e, em seguida, "Adeus". A ação também mapeia um número aleatório para a variável de saída `random-number` e executa um script chamado `goodbye.sh`.

Ao concluir este projeto, você entenderá como criar a sua própria ação composta e testá-la em um fluxo de trabalho.

!!! warning
    Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

### Ações compostas e fluxos de trabalho reutilizáveis

As ações compostas permitem coletar uma série de etapas de tarefas de fluxo de trabalho em uma única ação que você pode executar como uma única etapa de trabalho em vários fluxos de trabalho. Os fluxos de trabalho reutilizáveis fornecem outra maneira de evitar a duplicação, permitindo que você execute um fluxo de trabalho completo de dentro de outros fluxos de trabalho. Para saber mais, confira [Reutilizando configurações de fluxo de trabalho](../../concepts/workflows-and-actions/reusing-workflow-configurations.md).

## Pré-requisitos

!!! note
    Este exemplo explica como criar uma ação composta em um repositório separado. No entanto, é possível criar uma ação composta no mesmo repositório. Para saber mais, confira [Criar uma ação composta](create-a-composite-action.md#creating-a-composite-action-within-the-same-repository).

Antes de começar, você criará um repositório em GitHub.

1. Crie um novo repositório público em GitHub. Você pode escolher qualquer nome de repositório ou usar o exemplo de `hello-world-composite-action` a seguir. Você pode adicionar esses arquivos depois que seu projeto tiver sido enviado por push para GitHub. Para saber mais, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository).

2. Clone o repositório para seu computador. Para saber mais, confira [Clonar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository).

3. No seu terminal, mude os diretórios para seu novo repositório.

            ```shell copy
   cd hello-world-composite-action
   ```

4. No repositório `hello-world-composite-action`, crie um arquivo chamado `goodbye.sh` com o código de exemplo:

            ```shell copy
   echo "echo Goodbye" > goodbye.sh
   ```

5. A partir do terminal, torne o comando `goodbye.sh` executável.

            ```shell copy
   chmod +x goodbye.sh
   ```

            ```shell copy
   chmod +x goodbye.sh
   ```

            ```shell copy
   git add --chmod=+x -- goodbye.sh
   ```

6. Ainda no terminal, faça check-in do arquivo `goodbye.sh`.

            ```shell copy
   git add goodbye.sh
   git commit -m "Add goodbye script"
   git push
   ```

            ```shell copy
   git add goodbye.sh
   git commit -m "Add goodbye script"
   git push
   ```

            ```shell copy
   git commit -m "Add goodbye script"
   git push
   ```

## Criar um arquivo de metadados de ação

1. No repositório `hello-world-composite-action`, crie um arquivo chamado `action.yml` e adicione o código de exemplo a seguir. Para obter mais informações sobre essa sintaxe, confira [Referência de sintaxe de metadados](../../reference/workflows-and-actions/metadata-syntax.md#runs-for-composite-actions).

            ```yaml copy
   name: 'Hello World'
   description: 'Greet someone'
   inputs:
     who-to-greet:  # id of input
       description: 'Who to greet'
       required: true
       default: 'World'
   outputs:
     random-number:
       description: "Random number"
       value: ${{ steps.random-number-generator.outputs.random-number }}
   runs:
     using: "composite"
     steps:
       - name: Set Greeting
         run: echo "Hello $INPUT_WHO_TO_GREET."
         shell: bash
         env:
           INPUT_WHO_TO_GREET: ${{ inputs.who-to-greet }}

       - name: Random Number Generator
         id: random-number-generator
         run: echo "random-number=$(echo $RANDOM)" >> $GITHUB_OUTPUT
         shell: bash

       - name: Set GitHub Path
         run: echo "$GITHUB_ACTION_PATH" >> $GITHUB_PATH
         shell: bash
         env:
           GITHUB_ACTION_PATH: ${{ github.action_path }}

       - name: Run goodbye.sh
         run: goodbye.sh
         shell: bash

   ```

   Esse arquivo define a entrada de`who-to-greet`, mapeia o número gerado aleatoriamente para a variável de saída`random-number`, adiciona o caminho da ação ao caminho do sistema executor (para localizar o script`goodbye.sh` durante a execução) e executa o script`goodbye.sh`.

   Para obter mais informações sobre como gerenciar saídas, confira [Referência de sintaxe de metadados](../../reference/workflows-and-actions/metadata-syntax.md#outputs-for-composite-actions).

   Para obter mais informações sobre como usar o `github.action_path`, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md#github-context).

2. Ainda no terminal, faça check-in do arquivo `action.yml`.

            ```shell copy
   git add action.yml
   git commit -m "Add action"
   git push
   ```

3. No seu terminal, adicione uma tag. Este exemplo usa uma tag chamada `v1`. Para saber mais, confira [Como gerenciar ações personalizadas](../../how-tos/create-and-publish-actions/manage-custom-actions.md#using-release-management-for-actions).

            ```shell copy
   git tag -a -m "Description of this release" v1
   git push --follow-tags
   ```

## Testar sua ação em um fluxo de trabalho

O código de fluxo de trabalho a seguir usa a ação concluída "olá, mundo" que você criou em [Criar uma ação composta](create-a-composite-action.md#creating-an-action-metadata-file).

Copie o código do fluxo de trabalho em um arquivo `.github/workflows/main.yml` em outro repositório, substituindo `OWNER` e `SHA` pelo proprietário do repositório e o SHA do commit que deseja usar, respectivamente. Você também pode substituir a entrada `who-to-greet` pelo seu nome.

```yaml copy
on: [push]

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      - uses: actions/checkout@v6
      - id: foo
        uses: OWNER/hello-world-composite-action@SHA
        with:
          who-to-greet: 'Mona the Octocat'
      - run: echo random-number "$RANDOM_NUMBER"
        shell: bash
        env:
          RANDOM_NUMBER: ${{ steps.foo.outputs.random-number }}
```

No repositório, clique na guia **Ações** e selecione a execução mais recente do fluxo de trabalho. A saída deve incluir: "Hello Mona the Octocat", o resultado do script "Goodbye" e um número aleatório.

## Criando uma ação composta no mesmo repositório

1. Crie uma subpasta chamada `hello-world-composite-action`, que pode ser colocada em qualquer subpasta dentro do repositório. No entanto, é recomendável que seja colocada na subpasta `.github/actions` para facilitar a organização.

2. Na pasta `hello-world-composite-action`, execute as mesmas etapas para criar o script `goodbye.sh`

            ```shell copy
   echo "echo Goodbye" > goodbye.sh
   ```

            ```shell copy
   chmod +x goodbye.sh
   ```

            ```shell copy
   chmod +x goodbye.sh
   ```

            ```shell copy
   git add --chmod=+x -- goodbye.sh
   ```

            ```shell copy
   git add goodbye.sh
   git commit -m "Add goodbye script"
   git push
   ```

            ```shell copy
   git add goodbye.sh
   git commit -m "Add goodbye script"
   git push
   ```

            ```shell copy
   git commit -m "Add goodbye script"
   git push
   ```

3. Na pasta `hello-world-composite-action`, crie o arquivo `action.yml` com base nas etapas em [Criar uma ação composta](create-a-composite-action.md#creating-an-action-metadata-file).

4. Ao usar a ação, use o caminho relativo para a pasta em que o arquivo `action.yml` da ação composta está localizado na chave `uses`. O exemplo a seguir pressupõe que ele esteja na pasta `.github/actions/hello-world-composite-action`.

```yaml copy
on: [push]

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      - uses: actions/checkout@v6
      - id: foo
        uses: ./.github/actions/hello-world-composite-action
        with:
          who-to-greet: 'Mona the Octocat'
      - run: echo random-number "$RANDOM_NUMBER"
        shell: bash
        env:
          RANDOM_NUMBER: ${{ steps.foo.outputs.random-number }}
```
