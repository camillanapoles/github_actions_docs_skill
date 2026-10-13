---
title: Criando uma ação de contêiner do Docker
description: Neste tutorial, você aprenderá a criar uma ação de contêiner do Docker.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-containerized-services/create-a-docker-container-action
captured: '2026-10-13'
section: Tutorials / Use containerized services
---

# Criando uma ação de contêiner do Docker

_Neste tutorial, você aprenderá a criar uma ação de contêiner do Docker._

## Introdução

Neste guia, você aprenderá os componentes básicos necessários para criar e usar uma ação do contêiner Docker empacotado. Para manter o foco deste guia nos componentes necessários para empacotar a ação, a funcionalidade do código da ação é mínima. A ação imprime "Olá, mundo" nos registros ou "Olá, \[who-to-greet]", se você fornecer um nome personalizado.

Ao terminar esse projeto, você entenderá como criar sua própria ação de contêiner Docker e poderá testá-la em um fluxo de trabalho.

Executores auto-hospedados devem usar um sistema operacional Linux e ter o Docker instalado para executar as ações do contêiner Docker. Para obter mais informações sobre os requisitos dos executores autohospedados, consulte [Referência de executores auto-hospedados](../../reference/runners/self-hosted-runners.md#requirements-for-self-hosted-runner-machines).

!!! warning
    Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

## Pré-requisitos

* Você deve criar um repositório no GitHub e cloná-lo para sua estação de trabalho. Para saber mais, confira [Criar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/creating-a-new-repository) e [Clonar um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository).
* Se o repositório usar o Git LFS, você deverá incluir os objetos nos arquivos compactados do repositório. Para saber mais, confira [Gerenciando objetos LFS do Git em arquivos do seu repositório](https://docs.github.com/pt/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-git-lfs-objects-in-archives-of-your-repository).
* Talvez seja útil ter uma compreensão básica das variáveis de GitHub Actionsambiente e do sistema de arquivos de contêiner do Docker. Para saber mais, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md) e [Referência de executores hospedados pelo GitHub](../../reference/runners/github-hosted-runners.md#docker-container-filesystem).

## Criação de um Dockerfile

No diretório `hello-world-docker-action`, crie um arquivo `Dockerfile`. Verifique se o seu nome de arquivo está em maiúsculas corretamente (use um `D` maiúsculo, mas não um `f` maiúsculo) se estiver tendo problemas. Para saber mais, confira [Suporte do Dockerfile para GitHub Actions](../../reference/workflows-and-actions/dockerfile-support.md).

**Dockerfile**

```dockerfile copy
```
# Container image that runs your code
FROM alpine:3.10

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]
```

```
## Criar um arquivo de metadados de ação

Crie um arquivo `action.yml` no diretório `hello-world-docker-action` que você criou acima. Para saber mais, confira [Referência de sintaxe de metadados](../../reference/workflows-and-actions/metadata-syntax.md).

**action.yml**

```yaml copy
```
# action.yml
name: 'Hello World'
description: 'Greet someone and record the time'
inputs:
  who-to-greet:  # id of input
    description: 'Who to greet'
    required: true
    default: 'World'
outputs:
  time: # id of output
    description: 'The time we greeted you'
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.who-to-greet }}
```

Esses metadados definem um parâmetro de entrada `who-to-greet` e um de saída `time`. Para transmitir entradas para o contêiner do Docker, você deve declarar a entrada usando `inputs` e transmitir a entrada na palavra-chave `args`. Tudo o que você inclui em `args` é transmitido para o contêiner, mas para ter uma melhor capacidade de descoberta para os usuários da sua ação, recomendamos o uso de entradas.

GitHub criará uma imagem a partir do seu `Dockerfile` e executará comandos em um novo contêiner com essa imagem.

```
## Gravar um código de ação

Você pode escolher qualquer imagem Docker de base e, portanto, qualquer linguagem para sua ação. O exemplo de script de shell a seguir usa a variável de entrada `who-to-greet` para imprimir "Olá, \[quem cumprimentar]" no arquivo de log.

Na sequência, o script obtém a hora atual e a configura como uma variável de saída que pode ser usada pelas ações executadas posteriormente em um trabalho. Para GitHub reconhecer variáveis de saída, você deve gravá-las no arquivo de `$GITHUB_OUTPUT` ambiente: `echo "<output name>=<value>" >> $GITHUB_OUTPUT`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-commands.md#setting-an-output-parameter).

1. Crie um arquivo `entrypoint.sh` no diretório `hello-world-docker-action`.

2. Adicione o código a seguir ao arquivo `entrypoint.sh`.

**entrypoint.sh**

```shell copy
#!/bin/sh -l

echo "Hello $1"
time=$(date)
echo "time=$time" >> $GITHUB_OUTPUT

```

Se `entrypoint.sh` for executado sem erros, o status da ação será definido como `success`. Você também pode definir explicitamente códigos de saída no código de ação para fornecer o status de uma ação. Para saber mais, confira [Definindo códigos de saída para ações](../../how-tos/create-and-publish-actions/set-exit-codes.md).

1. Torne o arquivo `entrypoint.sh` executável. O Git fornece uma maneira de alterar explicitamente o modo de permissão de um arquivo para que ele não seja redefinido toda vez que houver um clone/fork.

            ```shell copy
   git add entrypoint.sh
   git update-index --chmod=+x entrypoint.sh
   ```

2. Opcionalmente, para verificar o modo de permissão do arquivo no índice Git, execute o comando a seguir.

            ```shell copy
   git ls-files --stage entrypoint.sh
   ```

   Uma saída como `100755 e69de29bb2d1d6434b8b29ae775ad8c2e48c5391 0       entrypoint.sh` significa que o arquivo tem a permissão executável. Neste exemplo, `755` denota a permissão executável.

## Criando um README

Para que as pessoas saibam como usar sua ação, você pode criar um arquivo README. Um arquivo README é útil quando você planeja compartilhar publicamente sua ação, mas também é uma ótima maneira de lembrá-lo ou sua equipe sobre como usar a ação.

No diretório `hello-world-docker-action`, crie um arquivo `README.md` que especifica as seguintes informações:

* Uma descrição detalhada do que a ação faz.
* Argumentos de entrada e saída obrigatórios.
* Argumentos de entrada e saída opcionais.
* Segredos que a ação usa.
* Variáveis de ambiente que a ação usa.
* Um exemplo de como usar sua ação em um fluxo de trabalho.

**LEIAME.md**

```markdown copy
```
# Hello world docker action

This action prints "Hello World" or "Hello" + the name of a person to greet to the log.

## Inputs

## `who-to-greet`

**Required** The name of the person to greet. Default `"World"`.

## Outputs

## `time`

The time we greeted you.

## Example usage

uses: actions/hello-world-docker-action@v2
with:
  who-to-greet: 'Mona the Octocat'
```

```
## Faça commit, tag e push da sua ação

Pelo terminal, faça commit dos arquivos `action.yml`, `entrypoint.sh`, `Dockerfile` e `README.md`.

Adicionar uma tag da versão para versões da sua ação é considerada uma prática recomendada. Para obter mais informações sobre o controle de versão da ação, confira [Como gerenciar ações personalizadas](../../how-tos/create-and-publish-actions/manage-custom-actions.md#using-release-management-for-actions).

```shell copy
git add action.yml entrypoint.sh Dockerfile README.md
git commit -m "My first action is ready"
git tag -a -m "My first action release" v1
git push --follow-tags
```

## Testar sua ação em um fluxo de trabalho

Agora você está pronto para testar sua ação em um fluxo de trabalho.

* Quando uma ação está em um repositório privado, é possível controlar quem tem acesso a ela. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-access-to-components-in-a-private-repository).
* Quando uma ação está em um repositório interno, a ação só pode ser usada em fluxos de trabalho no mesmo repositório.
* As ações públicas podem ser usadas por fluxos de trabalho em qualquer repositório.

### Exemplo usando uma ação pública

O código de fluxo de trabalho a seguir usa a ação *hello world* concluída no repositório público [`actions/hello-world-docker-action`](https://github.com/actions/hello-world-docker-action). Copie o código de exemplo de fluxo de trabalho a seguir em um arquivo `.github/workflows/main.yml`, mas substitua o `actions/hello-world-docker-action` pelo nome do repositório e da ação. Você também pode substituir a entrada `who-to-greet` pelo seu nome.
Ações públicas podem ser usadas mesmo que não sejam publicadas em GitHub Marketplace. Para saber mais, confira [Publicar ações no GitHub Marketplace](../../how-tos/create-and-publish-actions/publish-in-github-marketplace.md#publishing-an-action).

**.github/workflows/main.yml**

```yaml copy
on: [push]

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      - name: Hello world action step
        id: hello
        uses: actions/hello-world-docker-action@v2
        with:
          who-to-greet: 'Mona the Octocat'
      # Use the output from the `hello` step
      - name: Get the output time
        run: echo "The time was ${{ steps.hello.outputs.time }}"
```

### Exemplo usando uma ação privada

Copie o código de exemplo de fluxo de trabalho a seguir para um arquivo `.github/workflows/main.yml` no repositório da ação. Você também pode substituir a entrada `who-to-greet` pelo seu nome.
Essa ação privada não pode ser publicada em GitHub Marketplace e só pode ser usada neste repositório.

**.github/workflows/main.yml**

```yaml copy
on: [push]

jobs:
  hello_world_job:
    runs-on: ubuntu-latest
    name: A job to say hello
    steps:
      # To use this repository's private action,
      # you must check out the repository
      - name: Checkout
        uses: actions/checkout@v6
      - name: Hello world action step
        uses: ./ # Uses an action in the root directory
        id: hello
        with:
          who-to-greet: 'Mona the Octocat'
      # Use the output from the `hello` step
      - name: Get the output time
        run: echo "The time was ${{ steps.hello.outputs.time }}"
```

No repositório, clique na guia **Ações** e selecione a execução mais recente do fluxo de trabalho. Em **Trabalhos** ou no grafo de visualização, clique em **Um trabalho para dizer olá**.

Clique em **Etapa da ação Olá, mundo** e você verá "Olá, Mona, o Octocat" ou o nome usado para a entrada `who-to-greet` impresso no log. Para ver o carimbo de data/hora, clique em **Obter a hora da saída**.

## Acessar arquivos criados por uma ação de contêiner

Quando uma ação de contêiner é executada, ela mapeia automaticamente o diretório de trabalho padrão (`GITHUB_WORKSPACE`) no executor com o diretório `/github/workspace` no contêiner. Todos os arquivos adicionados a esse diretório no contêiner estarão disponíveis para todas as etapas subsequentes no mesmo trabalho. Por exemplo, se você tiver uma ação de contêiner que compila seu projeto e quiser carregar a saída da compilação como um artefato, poderá usar as etapas a seguir.

**workflow\.yml**

```yaml copy
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      # Output build artifacts to /github/workspace on the container.
      - name: Containerized Build
        uses: ./.github/actions/my-container-action

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: workspace_artifacts
          path: ${{ github.workspace }}
```

Para obter mais informações sobre como carregar a saída de compilação como um artefato, consulte [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

## Exemplo de ações de contêiner do Docker em GitHub.com

Você pode encontrar muitos exemplos de ações de contêiner do Docker em GitHub.com.

* [github/issue-metrics](https://github.com/github/issue-metrics)
* [microsoft/infersharpaction](https://github.com/microsoft/infersharpaction)
* [microsoft/ps-docs](https://github.com/microsoft/ps-docs)
