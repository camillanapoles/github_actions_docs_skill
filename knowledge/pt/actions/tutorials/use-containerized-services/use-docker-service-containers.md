---
title: Comunicar-se com os contêineres de serviço do Docker
description: Saiba como usar contêineres de serviço do Docker para conectar bancos de dados, serviços web, memória cache e outras ferramentas ao seu fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-containerized-services/use-docker-service-containers
captured: '2026-10-13'
section: Tutorials / Use containerized services
---

# Comunicar-se com os contêineres de serviço do Docker { #communicating-with-docker-service-containers }

_Saiba como usar contêineres de serviço do Docker para conectar bancos de dados, serviços web, memória cache e outras ferramentas ao seu fluxo de trabalho._

## Comunicar-se com os contêineres de serviço do Docker { #communicating-with-docker-service-containers-1 }

Os contêineres de serviço são contêineres Docker que oferecem uma maneira simples e portátil de hospedar serviços que você pode precisar testar ou executar sua aplicação em um fluxo de trabalho. Por exemplo, o seu fluxo de trabalho pode precisar executar testes de integração que necessitem de acesso a um banco de dados e a uma memória cache.

Você pode configurar os contêineres de serviço para cada trabalho em um fluxo de trabalho.
GitHub cria um novo contêiner do Docker para cada serviço configurado no fluxo de trabalho e destrói o contêiner de serviço quando o trabalho é concluído. As etapas em um trabalho podem comunicar-se com todos os contêineres de serviço que fazem parte do mesmo trabalho. No entanto, não é possível criar nem usar contêineres de serviço em uma ação composta.

!!! note
    Se os fluxos de trabalho usarem ações de contêiner do Docker, contêineres de trabalho ou contêineres de serviço, você precisará usar um executor do Linux:

    * Se você estiver usando executores hospedados em GitHub, você deverá usar um executor do Ubuntu.
    * Se você estiver usando executores auto-hospedados, você deve usar uma máquina Linux, pois seu executor e o Docker precisam ser instalados.

Você pode configurar trabalhos em um fluxo de trabalho para ser executados diretamente em uma máquina executora ou em um contêiner Docker. A comunicação entre o trabalho e seus contêineres de serviço é diferente, dependendo se um trabalho é executado diretamente na máquina executora ou em um contêiner.

### Executar trabalhos em um contêiner { #running-jobs-in-a-container }

Quando você executa trabalhos em um contêiner, GitHub conecta contêineres de serviço ao trabalho usando redes de ponte definidas pelo usuário do Docker. Para obter mais informações, confira [Driver de rede de ponte](https://docs.docker.com/engine/network/drivers/bridge/) na documentação do Docker.

Executar o trabalho e os serviços em um contêiner simplifica o acesso à rede. Você pode acessar um contêiner de serviço usando a etiqueta que você configurar no fluxo de trabalho. O nome de host do contêiner do serviço é mapeado automaticamente de acordo com o nome da etiqueta. Por exemplo, se você criar um contêiner de serviço com o rótulo `redis`, o nome do host do contêiner de serviço será `redis`.

Você não precisa configurar nenhuma porta para os contêineres de serviço. Por padrão, todos os contêineres que fazem parte da mesma rede do Docker expõem todas as portas entre si e nenhuma porta é exposta fora da rede do Docker.

### Executar trabalhos na máquina executora { #running-jobs-on-the-runner-machine }

Ao executar trabalhos diretamente na máquina do runner, você pode acessar os contêineres de serviço usando `localhost:<port>` ou `127.0.0.1:<port>`.
GitHub configura a rede de contêiner para habilitar a comunicação do contêiner de serviço para o host do Docker.

Quando um trabalho é executado diretamente em uma máquina executora, o serviço executado no contêiner do Docker não expõe suas portas ao trabalho no executor por padrão. Você deve mapear as portas do contêiner de serviço para o host do Docker. Para saber mais, confira [Comunicar-se com os contêineres de serviço do Docker](use-docker-service-containers.md#mapping-docker-host-and-service-container-ports).

## Criar contêineres de serviço { #creating-service-containers }

Use a palavra-chave `services` para criar contêineres de serviço que fazem parte de um trabalho no fluxo de trabalho. Para obter mais informações, confira [`jobs.<job_id>.services`](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idservices).

Este exemplo cria um serviço chamado `redis` em um trabalho chamado `container-job`. O host do Docker neste exemplo é o contêiner `node:16-bullseye`.

```yaml copy
name: Redis container example
on: push

jobs:
  # Label of the container job
  container-job:
    # Containers must run in Linux based operating systems
    runs-on: ubuntu-latest
    # Docker Hub image that `container-job` executes in
    container: node:16-bullseye

    # Service containers to run with `container-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
```

## Mapear o host do Docker e as portas do contêiner de serviço { #mapping-docker-host-and-service-container-ports }

Se o seu trabalho for executado em um contêiner do Docker, você não precisará mapear as portas no host ou no contêiner de serviço. Se o seu trabalho for executado diretamente na máquina executora, você precisará mapear todas as portas do contêiner de serviço necessárias com as portas na máquina executora do host.

Você pode mapear portas de contêineres de serviço para o host do Docker usando a palavra-chave `ports`. Para obter mais informações, confira [`jobs.<job_id>.services`](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idservices).

| Valor de `ports` | Descrição |
| --- | --- |
| `8080:80` | Mapeia a porta 80 TCP no contêiner com a porta 8080 no host do Docker. |
| `8080:80/udp` | Mapeia a porta 80 UDP no contêiner com a porta 8080 no host do Docker. |
| `8080/udp` | Mapeia uma porta aleatória no host do Docker para a porta UDP 8080 no contêiner. |

Quando você mapeia portas usando a `ports` palavra-chave, GitHub usa o `--publish` comando para publicar as portas do contêiner no host do Docker. Para obter mais informações, confira [Rede de contêineres do Docker](https://docs.docker.com/config/containers/container-networking/) na documentação do Docker.

Ao especificar a porta do contêiner mas não a porta do Docker, a porta do contêiner será atribuída aleatoriamente a uma porta livre.
GitHub define a porta de contêiner atribuída no contexto do contêiner de serviço. Por exemplo, para um contêiner de serviço `redis`, se você tiver configurado a porta de host do Docker 5432, poderá acessar a porta de contêiner correspondente usando o contexto `job.services.redis.ports[5432]`. Para saber mais, confira [Referência de contextos](../../reference/workflows-and-actions/contexts.md#job-context).

### Exemplo de mapeamento de portas Redis { #example-mapping-redis-ports }

Este exemplo mapeia a porta `redis` do contêiner de serviço 6379 para a porta 6379 do host do Docker.

```yaml copy
name: Redis Service Example
on: push

jobs:
  # Label of the container job
  runner-job:
    # You must use a Linux environment when using service containers or container jobs
    runs-on: ubuntu-latest

    # Service containers to run with `runner-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
        #
        ports:
          # Opens tcp port 6379 on the host and service container
          - 6379:6379
```

## Autenticando com registros de imagem { #authenticating-with-image-registries }

Você poderá especificar credenciais para os contêineres de serviço se precisar fazer autenticação com um registro de imagem. Isso permite a você usar imagens de registros privados ou [aumentar o limite de taxa do DockerHub](https://www.docker.com/increase-rate-limits/).

Aqui está um exemplo de autenticação com o Docker Hub e GitHubContainer registry:

```yaml copy
jobs:
  build:
    services:
      redis:
        # Docker Hub image
        image: redis
        ports:
          - 6379:6379
        credentials:
          username: ${{ secrets.dockerhub_username }}
          password: ${{ secrets.dockerhub_password }}
      db:
        # Private registry image
        image: ghcr.io/octocat/testdb:latest
        credentials:
          username: ${{ github.repository_owner }}
          password: ${{ secrets.ghcr_password }}
```

## Personalizando os pontos de entrada e os comandos do contêiner de serviço { #customizing-service-container-entrypoints-and-commands }

Por padrão, os contêineres de serviço são executados com o ponto de entrada e o comando definidos na imagem do Docker. Você pode substituí-los usando as teclas `entrypoint` e `command`. Isso é útil quando você precisa passar sinalizadores para um serviço (como um banco de dados) ou trocar totalmente o ponto de entrada da imagem, sem criar uma imagem de wrapper personalizada.

A `command` chave substitui o comando padrão da imagem (`CMD`). A maioria dos cenários só precisa `command` — a imagem já tem o ponto de entrada certo, você só precisa passar sinalizadores:

```yaml copy
services:
  mysql:
    image: mysql:8
    command: --sql_mode=STRICT_TRANS_TABLES --max_allowed_packet=512M
    env:
      MYSQL_ROOT_PASSWORD: test
    ports:
      - 3306:3306
```

A `entrypoint` chave substitui o `ENTRYPOINT` da imagem. Você pode combiná-lo com `command` para passar argumentos ao ponto de entrada personalizado.

```yaml copy
services:
  etcd:
    image: quay.io/coreos/etcd:v3.5.17
    entrypoint: etcd
    command: >-
      --listen-client-urls http://0.0.0.0:2379
      --advertise-client-urls http://0.0.0.0:2379
    ports:
      - 2379:2379
```

A nomenclatura e o comportamento correspondem ao Docker Compose. Para obter mais informações, consulte [`jobs.<job_id>.services.<service_id>.command`](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idservicesservice_idcommand) e [`jobs.<job_id>.services.<service_id>.entrypoint`](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idservicesservice_identrypoint).

## Leitura adicional { #further-reading }

* [Criando contêineres de serviço Redis](create-redis-service-containers.md)
* [Criar contêineres de serviço PostgreSQL](create-postgresql-service-containers.md)
