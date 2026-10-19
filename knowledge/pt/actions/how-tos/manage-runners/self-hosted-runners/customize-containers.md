---
title: Como personalizar os contêineres usados por trabalhos
description: Você pode personalizar como o executor auto-hospedado invoca um contêiner para um trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/customize-containers
captured: '2026-10-19'
section: How tos / Manage runners / Self hosted runners
---

# Como personalizar os contêineres usados por trabalhos

_Você pode personalizar como o executor auto-hospedado invoca um contêiner para um trabalho._

!!! note
    Esse recurso está atualmente dentro prévia pública e está sujeito a alterações.

## Sobre a personalização de contêiner

GitHub Actions permite que você execute um trabalho em um contêiner, usando a `container:` instrução em seu arquivo de fluxo de trabalho. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md). Para processar trabalhos baseados em contêiner, o executor auto-hospedado cria um contêiner para cada trabalho.

GitHub Actions dá suporte a comandos que permitem personalizar a maneira como os contêineres são criados pelo executor auto-hospedado. Por exemplo, você pode usar esses comandos para gerenciar os contêineres por meio do Kubernetes ou do Podman e também pode personalizar os comandos `docker run` ou `docker create`usados para invocar o contêiner. Os comandos de personalização são executados por um script, que é disparado automaticamente quando uma variável de ambiente específica é definida no executor. Para obter mais informações, confira [Como disparar o script de personalização](#triggering-the-customization-script) abaixo.

Essa personalização só está disponível para executores auto-hospedados baseados em Linux e o acesso de usuário raiz não é necessário.

## Comandos de personalização de contêiner

GitHub Actions inclui os seguintes comandos para personalização de contêiner:

* [
  `prepare_job`
  ](customize-containers.md#prepare_job): É chamado quando um trabalho é iniciado.
* [
  `cleanup_job`
  ](customize-containers.md#cleanup_job): chamado no final de uma tarefa.
* [
  `run_container_step`
  ](customize-containers.md#run_container_step): Chamado uma vez para cada ação de contêiner no trabalho.
* [
  `run_script_step`
  ](customize-containers.md#run_script_step): executa qualquer etapa que não seja uma ação de contêiner.

Cada um desses comandos de personalização precisa ser definido no próprio arquivo JSON. O nome do arquivo precisa corresponder ao nome do comando, com a extensão `.json`. Por exemplo, o comando `prepare_job` é definido em `prepare_job.json`. Esses arquivos JSON serão executados juntos no executor auto-hospedado, como parte do script `index.js` principal. Esse processo é descrito em mais detalhes em [Como gerar o script de personalização](#generating-the-customization-script).

Esses comandos também incluem argumentos de configuração, explicados abaixo em mais detalhes.

### `prepare_job`

O comando `prepare_job` é chamado quando um trabalho é iniciado.
GitHub Actions passa em qualquer trabalho ou contêineres de serviço que o trabalho tem. Esse comando será chamado se você tiver algum contêiner de trabalho ou de serviço no trabalho.

GitHub Actions pressupõe que você realizará as seguintes tarefas no `prepare_job` comando:

* Remover tudo dos trabalhos anteriores, se necessário.
* Criar uma rede, se necessário.
* Efetuar pull dos contêineres de serviço e de trabalho.
* Iniciar o contêiner de trabalho.
* Iniciar os contêineres de serviço.
* Escreva no arquivo de resposta todas as informações que GitHub Actions precisarão:
  * Obrigatório: informar se o contêiner é um contêiner `alpine` do Linux (usando o `isAlpine` booliano).
  * Opcional: todos os campos de contexto que você deseja definir no contexto do trabalho, caso contrário, eles não estarão disponíveis para os usuários usarem. Para saber mais, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#job-context).
* Retornar `0` quando as verificações de integridade forem bem-sucedidas e os contêineres de trabalho/serviço forem iniciados.

#### Argumentos para `prepare_job`

* `jobContainer`: **opcional**. Um objeto que contém informações sobre o contêiner de trabalho especificado.
  * `image`: **obrigatório**. Uma cadeia de caracteres que contém a imagem do Docker.
  * `workingDirectory`: **obrigatório**. Uma cadeia de caracteres que contém o caminho absoluto do diretório de trabalho.
  * `createOptions`: **opcional**. As opções opcionais de *create* especificadas no YAML. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md#example-running-a-job-within-a-container).
  * `environmentVariables`: **opcional**. Define um mapa das principais variáveis de ambiente.
  * `userMountVolumes`: **opcional**. Uma matriz de volumes de montagem do usuário definida no YAML. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md#example-running-a-job-within-a-container).
    * `sourceVolumePath`: **obrigatório**. O caminho de origem para o volume que será montado no contêiner do Docker.
    * `targetVolumePath`: **obrigatório**. O caminho de destino do volume que será montado no contêiner do Docker.
    * `readOnly`: **obrigatório**. Determina se a montagem deve ser somente leitura ou não.
  * `systemMountVolumes`: **obrigatório**. Uma matriz de montagens a serem montadas no contêiner, usando os mesmos campos que acima.
    * `sourceVolumePath`: **obrigatório**. O caminho de origem para o volume que será montado no contêiner do Docker.
    * `targetVolumePath`: **obrigatório**. O caminho de destino do volume que será montado no contêiner do Docker.
    * `readOnly`: **obrigatório**. Determina se a montagem deve ser somente leitura ou não.
  * `registry`
    **opcional**. As credenciais do registro do Docker para um registro de contêiner privado.
    * `username`: **opcional**. O nome de usuário da conta do registro.
    * `password`: **opcional**. A senha da conta do registro.
    * `serverUrl`: **opcional**. A URL do registro.
  * `portMappings`: **opcional**. Um hash de valor de chave das portas *source:target* a serem mapeadas para o contêiner.
* `services`: **opcional**. Uma matriz de contêineres de serviço a ser ativada.
  * `contextName`: **obrigatório**. O nome do serviço no contexto do trabalho.
  * `image`: **obrigatório**. Uma cadeia de caracteres que contém a imagem do Docker.
  * `createOptions`: **opcional**. As opções opcionais de *create* especificadas no YAML. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md#example-running-a-job-within-a-container).
  * `environmentVariables`: **opcional**. Define um mapa das principais variáveis de ambiente.
  * `userMountVolumes`: **opcional**. Uma matriz de montagens a serem montadas no contêiner, usando os mesmos campos que acima.
    * `sourceVolumePath`: **obrigatório**. O caminho de origem para o volume que será montado no contêiner do Docker.
    * `targetVolumePath`: **obrigatório**. O caminho de destino do volume que será montado no contêiner do Docker.
    * `readOnly`: **obrigatório**. Determina se a montagem deve ser somente leitura ou não.
  * `registry`
    **opcional**. As credenciais do registro do Docker para o registro de contêiner privado.
    * `username`: **opcional**. O nome de usuário da conta do registro.
    * `password`: **opcional**. A senha da conta do registro.
    * `serverUrl`: **opcional**. A URL do registro.
  * `portMappings`: **opcional**. Um hash de valor de chave das portas *source:target* a serem mapeadas para o contêiner.

#### Exemplo de entrada para `prepare_job`

```json copy
{
  "command": "prepare_job",
  "responseFile": "/users/octocat/runner/_work/{guid}.json",
  "state": {},
  "args": {
    "jobContainer": {
      "image": "node:18",
      "workingDirectory": "/__w/octocat-test2/octocat-test2",
      "createOptions": "--cpus 1",
      "environmentVariables": {
        "NODE_ENV": "development"
      },
      "userMountVolumes": [
        {
          "sourceVolumePath": "my_docker_volume",
          "targetVolumePath": "/volume_mount",
          "readOnly": false
        }
      ],
      "systemMountVolumes": [
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work",
          "targetVolumePath": "/__w",
          "readOnly": false
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/externals",
          "targetVolumePath": "/__e",
          "readOnly": true
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp",
          "targetVolumePath": "/__w/_temp",
          "readOnly": false
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_actions",
          "targetVolumePath": "/__w/_actions",
          "readOnly": false
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_tool",
          "targetVolumePath": "/__w/_tool",
          "readOnly": false
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_home",
          "targetVolumePath": "/github/home",
          "readOnly": false
        },
        {
          "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_workflow",
          "targetVolumePath": "/github/workflow",
          "readOnly": false
        }
      ],
      "registry": {
        "username": "octocat",
        "password": "examplePassword",
        "serverUrl": "https://index.docker.io/v1"
      },
      "portMappings": { "80": "801" }
    },
    "services": [
      {
        "contextName": "redis",
        "image": "redis",
        "createOptions": "--cpus 1",
        "environmentVariables": {},
        "userMountVolumes": [],
        "portMappings": { "80": "801" },
        "registry": {
          "username": "octocat",
          "password": "examplePassword",
          "serverUrl": "https://index.docker.io/v1"
        }
      }
    ]
  }
}
```

#### Exemplo de saída para `prepare_job`

Este exemplo de saída é o conteúdo do `responseFile` definido na entrada acima.

```json copy
{
  "state": {
    "network": "example_network_53269bd575972817b43f7733536b200c",
    "jobContainer": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
    "serviceContainers": {
      "redis": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105"
    }
  },
  "context": {
    "container": {
      "id": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
      "network": "example_network_53269bd575972817b43f7733536b200c"
    },
    "services": {
      "redis": {
        "id": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105",
        "ports": {
          "8080": "8080"
        },
        "network": "example_network_53269bd575972817b43f7733536b200c"
      }
    },
    "isAlpine": true
  }
}
```

### `cleanup_job`

O comando `cleanup_job` é chamado no final de um trabalho.
GitHub Actions pressupõe que você realizará as seguintes tarefas no `cleanup_job` comando:

* Pare todos os contêineres de trabalho ou de serviço em execução (ou o pod equivalente).
* Pare a rede (se existir).
* Exclua todos os contêineres de trabalho ou de serviço (ou o pod equivalente).
* Exclua a rede (se existir).
* Limpe todos os outros itens que foram criados para o trabalho.

#### Argumentos para `cleanup_job`

Nenhum argumento é fornecido para `cleanup_job`.

#### Exemplo de entrada para `cleanup_job`

```json copy
{
  "command": "cleanup_job",
  "responseFile": null,
  "state": {
    "network": "example_network_53269bd575972817b43f7733536b200c",
    "jobContainer": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
    "serviceContainers": {
      "redis": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105"
    }
  },
  "args": {}
}
```

#### Exemplo de saída para `cleanup_job`

Nenhuma saída é esperada para `cleanup_job`.

### `run_container_step`

O comando `run_container_step` é chamado uma vez para cada ação de contêiner no trabalho.
GitHub Actions pressupõe que você realizará as seguintes tarefas no `run_container_step` comando:

* Efetuar pull ou criar o contêiner necessário (ou falhar, se não for possível).
* Executar a ação do contêiner e retornar o código de saída do contêiner.
* Transmitir as saídas de logs de etapa para stdout e stderr.
* Limpar o contêiner depois que ele for executado.

#### Argumentos para `run_container_step`

* `image`: **opcional**. Uma cadeia de caracteres que contém a imagem do Docker. Caso contrário, um dockerfile precisará ser fornecido.
* `dockerfile`: **opcional**. Uma cadeia de caracteres que contém o caminho para o dockerfile, caso contrário, uma imagem precisará ser fornecida.
* `entryPointArgs`: **opcional**. Uma lista que contém os argumentos de ponto de entrada.
* `entryPoint`: **opcional**. O ponto de entrada do contêiner a ser usado se o ponto de entrada de imagem padrão precisar ser substituído.
* `workingDirectory`: **obrigatório**. Uma cadeia de caracteres que contém o caminho absoluto do diretório de trabalho.
* `createOptions`: **opcional**. As opções opcionais de *create* especificadas no YAML. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md#example-running-a-job-within-a-container).
* `environmentVariables`: **opcional**. Define um mapa das principais variáveis de ambiente.
* `prependPath`: **opcional**. Uma matriz de caminhos adicionais a serem acrescentados à variável `$PATH`.
* `userMountVolumes`: **opcional**. uma matriz de volumes de montagem do usuário definida no YAML. Para saber mais, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md#example-running-a-job-within-a-container).
  * `sourceVolumePath`: **obrigatório**. O caminho de origem para o volume que será montado no contêiner do Docker.
  * `targetVolumePath`: **obrigatório**. O caminho de destino do volume que será montado no contêiner do Docker.
  * `readOnly`: **obrigatório**. Determina se a montagem deve ser somente leitura ou não.
* `systemMountVolumes`: **obrigatório**. Uma matriz de montagens a serem montadas no contêiner, usando os mesmos campos que acima.
  * `sourceVolumePath`: **obrigatório**. O caminho de origem para o volume que será montado no contêiner do Docker.
  * `targetVolumePath`: **obrigatório**. O caminho de destino do volume que será montado no contêiner do Docker.
  * `readOnly`: **obrigatório**. Determina se a montagem deve ser somente leitura ou não.
* `registry`
  **opcional**. As credenciais do registro do Docker para um registro de contêiner privado.
  * `username`: **opcional**. O nome de usuário da conta do registro.
  * `password`: **opcional**. A senha da conta do registro.
  * `serverUrl`: **opcional**. A URL do registro.
* `portMappings`: **opcional**. Um hash de valor de chave das portas *source:target* a serem mapeadas para o contêiner.

#### Exemplo de entrada de imagem

Se você estiver usando uma imagem do Docker, especifique o nome da imagem no parâmetro `"image":`.

```json copy
{
  "command": "run_container_step",
  "responseFile": null,
  "state": {
    "network": "example_network_53269bd575972817b43f7733536b200c",
    "jobContainer": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
    "serviceContainers": {
      "redis": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105"
    }
  },
  "args": {
    "image": "node:18",
    "dockerfile": null,
    "entryPointArgs": ["-f", "/dev/null"],
    "entryPoint": "tail",
    "workingDirectory": "/__w/octocat-test2/octocat-test2",
    "createOptions": "--cpus 1",
    "environmentVariables": {
      "NODE_ENV": "development"
    },
    "prependPath": ["/foo/bar", "bar/foo"],
    "userMountVolumes": [
      {
        "sourceVolumePath": "my_docker_volume",
        "targetVolumePath": "/volume_mount",
        "readOnly": false
      }
    ],
    "systemMountVolumes": [
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work",
        "targetVolumePath": "/__w",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/externals",
        "targetVolumePath": "/__e",
        "readOnly": true
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp",
        "targetVolumePath": "/__w/_temp",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_actions",
        "targetVolumePath": "/__w/_actions",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_tool",
        "targetVolumePath": "/__w/_tool",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_home",
        "targetVolumePath": "/github/home",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_workflow",
        "targetVolumePath": "/github/workflow",
        "readOnly": false
      }
    ],
    "registry": null,
    "portMappings": { "80": "801" }
  }
}
```

#### Entrada de exemplo de Dockerfile

Para um contêiner definido por um Dockerfile, este exemplo demonstra como especificar o caminho para um `Dockerfile` na entrada usando o parâmetro `"dockerfile":`.

```json copy
{
  "command": "run_container_step",
  "responseFile": null,
  "state": {
    "network": "example_network_53269bd575972817b43f7733536b200c",
    "jobContainer": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
    "services": {
      "redis": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105"
    }
  },
  "args": {
    "image": null,
    "dockerfile": "/__w/_actions/foo/dockerfile",
    "entryPointArgs": ["hello world"],
    "entryPoint": "echo",
    "workingDirectory": "/__w/octocat-test2/octocat-test2",
    "createOptions": "--cpus 1",
    "environmentVariables": {
      "NODE_ENV": "development"
    },
    "prependPath": ["/foo/bar", "bar/foo"],
    "userMountVolumes": [
      {
        "sourceVolumePath": "my_docker_volume",
        "targetVolumePath": "/volume_mount",
        "readOnly": false
      }
    ],
    "systemMountVolumes": [
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work",
        "targetVolumePath": "/__w",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/externals",
        "targetVolumePath": "/__e",
        "readOnly": true
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp",
        "targetVolumePath": "/__w/_temp",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_actions",
        "targetVolumePath": "/__w/_actions",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_tool",
        "targetVolumePath": "/__w/_tool",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_home",
        "targetVolumePath": "/github/home",
        "readOnly": false
      },
      {
        "sourceVolumePath": "/home/octocat/git/runner/_layout/_work/_temp/_github_workflow",
        "targetVolumePath": "/github/workflow",
        "readOnly": false
      }
    ],
    "registry": null,
    "portMappings": { "80": "801" }
  }
}
```

#### Exemplo de saída para `run_container_step`

Nenhuma saída é esperada para `run_container_step`.

### `run_script_step`

GitHub Actions pressupõe que você realizará as seguintes tarefas:

* Invocar o script fornecido dentro do contêiner de trabalho e retornar o código de saída.
* Transmitir as saídas de logs de etapa para stdout e stderr.

#### Argumentos para `run_script_step`

* `entryPointArgs`: **opcional**. Uma lista que contém os argumentos de ponto de entrada.
* `entryPoint`: **opcional**. O ponto de entrada do contêiner a ser usado se o ponto de entrada de imagem padrão precisar ser substituído.
* `prependPath`: **opcional**. Uma matriz de caminhos adicionais a serem acrescentados à variável `$PATH`.
* `workingDirectory`: **obrigatório**. Uma cadeia de caracteres que contém o caminho absoluto do diretório de trabalho.
* `environmentVariables`: **opcional**. Define um mapa das principais variáveis de ambiente.

#### Exemplo de entrada para `run_script_step`

```json copy
{
  "command": "run_script_step",
  "responseFile": null,
  "state": {
    "network": "example_network_53269bd575972817b43f7733536b200c",
    "jobContainer": "82e8219701fe096a35941d869cf3d71af1d943b5d8bdd718857fb87ac3042480",
    "serviceContainers": {
      "redis": "60972d9aa486605e66b0dad4abb678dc3d9116f536579e418176eedb8abb9105"
    }
  },
  "args": {
    "entryPointArgs": ["-e", "/runner/temp/example.sh"],
    "entryPoint": "bash",
    "environmentVariables": {
      "NODE_ENV": "development"
    },
    "prependPath": ["/foo/bar", "bar/foo"],
    "workingDirectory": "/__w/octocat-test2/octocat-test2"
  }
}
```

#### Exemplo de saída para `run_script_step`

Nenhuma saída é esperada para `run_script_step`.

## Como gerar o script de personalização

GitHub criou um repositório de exemplo que demonstra como gerar scripts de personalização para Docker e Kubernetes.

!!! note
    Os scripts resultantes estão disponíveis para fins de teste e você precisará determinar se eles são apropriados para seus requisitos.

1. Clone o repositório [actions/runner-container-hooks](https://github.com/actions/runner-container-hooks) para seu executor auto-hospedado.

2. O diretório `examples/` contém alguns comandos de personalização existentes, cada um com o próprio arquivo JSON. Você pode examinar esses exemplos e usá-los como um ponto de partida para seus comandos de personalização.

   * `prepare_job.json`
   * `run_script_step.json`
   * `run_container_step.json`

3. Crie os pacotes npm. Esses comandos geram os arquivos `index.js` dentro de `packages/docker/dist` e `packages/k8s/dist`.

            ```shell
   npm install && npm run bootstrap && npm run build-all
   ```

Quando o(a) `index.js` resultante for acionado(a) por GitHub Actions, ele executará os comandos de personalização definidos nos arquivos JSON. Para disparar o `index.js`, você precisa adicioná-la à variável de ambiente `ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER`, como está descrito na próxima seção.

## Como disparar o script de personalização

Os scripts personalizados precisam estar localizados no executor, mas não precisam ser armazenados no diretório do aplicativo executor auto-hospedado (ou seja, o diretório no qual você baixou e descompactou o software executor). Os scripts são executados no contexto de segurança da conta de serviço que executa o serviço de executor.

!!! note
    O script disparado é processado de maneira síncrona, ou seja, ele bloqueará a execução do trabalho enquanto estiver em execução.

Os scripts são executados automaticamente quando o executor tem a seguinte variável de ambiente que contêm um caminho absoluto para o script:

* `ACTIONS_RUNNER_CONTAINER_HOOKS`: o script definido nessa variável de ambiente é disparado quando um trabalho é atribuído a um executor, mas antes do trabalho começar a ser executado.

Para definir essa variável de ambiente, você pode adicioná-la ao sistema operacional ou a um arquivo chamado `.env` no diretório do aplicativo executor auto-hospedado. Por exemplo, a seguinte entrada `.env` fará com que o executor execute o script em `/Users/octocat/runner/index.js` automaticamente antes da execução de cada trabalho de contêiner:

```bash
ACTIONS_RUNNER_CONTAINER_HOOKS=/Users/octocat/runner/index.js
```

Se você quiser garantir que o trabalho sempre seja executado dentro de um contêiner e, portanto, sempre aplique as personalizações de contêiner, defina a variável `ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER` no executor auto-hospedado como `true`. Isso falhará trabalhos que não especificam um contêiner de trabalho.

## Solução de problemas

### Sem configuração de tempo limite

No momento, não há nenhuma configuração de tempo limite disponível para o script executado por `ACTIONS_RUNNER_CONTAINER_HOOKS`. Como resultado, você pode considerar a adição de tratamento do tempo limite ao script.

### Examinar o log de execução do fluxo de trabalho

Para confirmar se os scripts estão em execução, você pode revisar os logs desse trabalho. Para obter mais informações sobre como verificar os logs, confira [Usando registros de execução de fluxo de trabalho](../../monitor-workflows/use-workflow-run-logs.md#viewing-logs-to-diagnose-failures).
