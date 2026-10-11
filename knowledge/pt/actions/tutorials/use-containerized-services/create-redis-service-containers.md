---
title: Criando contêineres de serviço Redis
description: Você pode usar os contêineres de serviço para criar um cliente Redis no seu fluxo de trabalho. Este guia mostra exemplos de criação de serviço Redis para trabalhos executados em contêineres ou diretamente na máquina executora.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-containerized-services/create-redis-service-containers
captured: '2026-10-11'
section: Tutorials / Use containerized services
---

# Criando contêineres de serviço Redis

_Você pode usar os contêineres de serviço para criar um cliente Redis no seu fluxo de trabalho. Este guia mostra exemplos de criação de serviço Redis para trabalhos executados em contêineres ou diretamente na máquina executora._

## Introdução

Este guia mostra exemplos de fluxo de trabalho que configuram um contêiner de serviço usando a imagem Docker Hub `redis`. O fluxo de trabalho executa um script para criar um cliente Redis e preencher os dados do cliente. Para testar se o fluxo de trabalho cria e preenche o cliente Redis, o script imprime os dados do cliente no console.

!!! note
    Se os fluxos de trabalho usarem ações de contêiner do Docker, contêineres de trabalho ou contêineres de serviço, você precisará usar um executor do Linux:

    * Se você estiver usando executores hospedados em GitHub, você deverá usar um executor do Ubuntu.
    * Se você estiver usando executores auto-hospedados, você deve usar uma máquina Linux, pois seu executor e o Docker precisam ser instalados.

## Pré-requisitos

Você deve estar familiarizado com a forma como contêineres de serviço funcionam com GitHub Actions e as diferenças de rede entre trabalhos em execução diretamente no executor ou em um contêiner. Para saber mais, confira [Comunicar-se com os contêineres de serviço do Docker](use-docker-service-containers.md).

Você também pode achar útil ter uma compreensão básica do YAML, da sintaxe para GitHub Actionse do Redis. Para saber mais, veja:

* [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md)
* [Introdução ao Redis](https://redis.io/learn/howtos/quick-start) na documentação do Redis

## Executar trabalhos em contêineres

A configuração de tarefas a serem executadas em um contêiner simplifica as configurações de rede entre o trabalho e os contêineres do serviço. Docker contêineres na mesma rede de ponte definida pelo usuário expõe todas as portas umas para as outras, então você não precisa mapear nenhuma das portas de contêiner de serviço para o host Docker. Você pode acessar o contêiner de serviço do contêiner de trabalho usando a etiqueta que você configurar no fluxo de trabalho.

Você pode copiar esse arquivo de fluxo de trabalho para o diretório `.github/workflows` do repositório e modificá-lo conforme necessário.

```yaml copy
name: Redis container example
on: push

jobs:
  # Label of the container job
  container-job:
    # Containers must run in Linux based operating systems
    runs-on: ubuntu-latest
    # Docker Hub image that `container-job` executes in
    container: node:20-bookworm-slim

    # Service containers to run with `container-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
        # Set health checks to wait until redis has started
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      # Downloads a copy of the code in your repository before running CI tests
      - name: Check out repository code
        uses: actions/checkout@v6

      # Performs a clean installation of all dependencies in the `package.json` file
      # For more information, see https://docs.npmjs.com/cli/ci.html
      - name: Install dependencies
        run: npm ci

      - name: Connect to Redis
        # Runs a script that creates a Redis client, populates
        # the client with data, and retrieves data
        run: node client.js
        # Environment variable used by the `client.js` script to create a new Redis client.
        env:
          # The hostname used to communicate with the Redis service container
          REDIS_HOST: redis
          # The default Redis port
          REDIS_PORT: 6379
```

### Configuração da tarefa do contêiner

Este fluxo de trabalho configura uma tarefa que é executada no contêiner `node:20-bookworm-slim` e usa o executor do `ubuntu-latest`  hospedado no GitHub como host do Docker para o contêiner. Para obter mais informações sobre o contêiner `node:20-bookworm-slim`, confira a [imagem do nó](https://hub.docker.com/_/node) no Docker Hub.

O fluxo de trabalho configura um contêiner de serviço com o rótulo `redis`. Todos os serviços precisam ser executados em um contêiner, ou seja, cada serviço exige que você especifique o contêiner `image`. Este exemplo usa a imagem de contêiner `redis` e inclui opções de verificação de integridade para verificar se o serviço está funcionando. Acrescente uma marca ao nome da imagem para especificar uma versão, por exemplo `redis:6`. Para obter mais informações, confira a [imagem redis](https://hub.docker.com/_/redis) no Docker Hub.

```yaml copy
jobs:
  # Label of the container job
  container-job:
    # Containers must run in Linux based operating systems
    runs-on: ubuntu-latest
    # Docker Hub image that `container-job` executes in
    container: node:20-bookworm-slim

    # Service containers to run with `container-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
        # Set health checks to wait until redis has started
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
```

### Configurando as etapas para o trabalho de contêiner

O fluxo de trabalho executa as seguintes etapas:

1. Verifica o repositório no executor
2. Instala dependências
3. Executa um script para criar um cliente

```yaml copy
steps:
  # Downloads a copy of the code in your repository before running CI tests
  - name: Check out repository code
    uses: actions/checkout@v6

  # Performs a clean installation of all dependencies in the `package.json` file
  # For more information, see https://docs.npmjs.com/cli/ci.html
  - name: Install dependencies
    run: npm ci

  - name: Connect to Redis
    # Runs a script that creates a Redis client, populates
    # the client with data, and retrieves data
    run: node client.js
    # Environment variable used by the `client.js` script to create a new Redis client.
    env:
      # The hostname used to communicate with the Redis service container
      REDIS_HOST: redis
      # The default Redis port
      REDIS_PORT: 6379
```

O script *client.js* procura as variáveis de ambiente `REDIS_HOST` e `REDIS_PORT` para criar o cliente. O fluxo de trabalho define essas duas variáveis de ambiente como parte da etapa "Conectar-se ao Redis" para disponibilizá-las ao script *client.js*. Para obter mais informações sobre o script, confira [Como testar o contêiner do serviço do Redis](#testing-the-redis-service-container).

O hostname do serviço Redis é o rótulo que você configurou no seu fluxo de trabalho, neste caso, `redis`. Uma vez que os contêineres do Docker na mesma rede da ponte definida pelo usuário abrem todas as portas por padrão, você poderá acessar o contêiner de serviço na porta-padrão 6379 do Redis.

## Executar trabalhos diretamente na máquina executora

Ao executar um trabalho diretamente na máquina executora, você deverá mapear as portas no contêiner de serviço às portas do host Docker. Você pode acessar os contêineres de serviço do host do Docker usando o `localhost` e o número da porta do host do Docker.

Você pode copiar esse arquivo de fluxo de trabalho para o diretório `.github/workflows` do repositório e modificá-lo conforme necessário.

```yaml copy
name: Redis runner example
on: push

jobs:
  # Label of the runner job
  runner-job:
    # You must use a Linux environment when using service containers or container jobs
    runs-on: ubuntu-latest

    # Service containers to run with `runner-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
        # Set health checks to wait until redis has started
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          # Maps port 6379 on service container to the host
          - 6379:6379

    steps:
      # Downloads a copy of the code in your repository before running CI tests
      - name: Check out repository code
        uses: actions/checkout@v6

      # Performs a clean installation of all dependencies in the `package.json` file
      # For more information, see https://docs.npmjs.com/cli/ci.html
      - name: Install dependencies
        run: npm ci

      - name: Connect to Redis
        # Runs a script that creates a Redis client, populates
        # the client with data, and retrieves data
        run: node client.js
        # Environment variable used by the `client.js` script to create
        # a new Redis client.
        env:
          # The hostname used to communicate with the Redis service container
          REDIS_HOST: localhost
          # The default Redis port
          REDIS_PORT: 6379
```

### Configurar o trabalho executor

O exemplo usa o executor hospedado no `ubuntu-latest`  GitHub como o host do Docker.

O fluxo de trabalho configura um contêiner de serviço com o rótulo `redis`. Todos os serviços precisam ser executados em um contêiner, ou seja, cada serviço exige que você especifique o contêiner `image`. Este exemplo usa a imagem de contêiner `redis` e inclui opções de verificação de integridade para verificar se o serviço está funcionando. Acrescente uma marca ao nome da imagem para especificar uma versão, por exemplo `redis:6`. Para obter mais informações, confira a [imagem redis](https://hub.docker.com/_/redis) no Docker Hub.

O fluxo de trabalho mapeia a porta 6379 no contêiner de serviço do Redis para o host do Docker. Para saber mais sobre a palavra-chave `ports`, confira [Comunicar-se com os contêineres de serviço do Docker](use-docker-service-containers.md#mapping-docker-host-and-service-container-ports).

```yaml copy
jobs:
  # Label of the runner job
  runner-job:
    # You must use a Linux environment when using service containers or container jobs
    runs-on: ubuntu-latest

    # Service containers to run with `runner-job`
    services:
      # Label used to access the service container
      redis:
        # Docker Hub image
        image: redis
        # Set health checks to wait until redis has started
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          # Maps port 6379 on service container to the host
          - 6379:6379
```

### Configurando as etapas para o trabalho do executor

O fluxo de trabalho executa as seguintes etapas:

1. Verifica o repositório no executor
2. Instala dependências
3. Executa um script para criar um cliente

```yaml copy
steps:
  # Downloads a copy of the code in your repository before running CI tests
  - name: Check out repository code
    uses: actions/checkout@v6

  # Performs a clean installation of all dependencies in the `package.json` file
  # For more information, see https://docs.npmjs.com/cli/ci.html
  - name: Install dependencies
    run: npm ci

  - name: Connect to Redis
    # Runs a script that creates a Redis client, populates
    # the client with data, and retrieves data
    run: node client.js
    # Environment variable used by the `client.js` script to create
    # a new Redis client.
    env:
      # The hostname used to communicate with the Redis service container
      REDIS_HOST: localhost
      # The default Redis port
      REDIS_PORT: 6379
```

O script *client.js* procura as variáveis de ambiente `REDIS_HOST` e `REDIS_PORT` para criar o cliente. O fluxo de trabalho define essas duas variáveis de ambiente como parte da etapa "Conectar-se ao Redis" para disponibilizá-las ao script *client.js*. Para obter mais informações sobre o script, confira [Como testar o contêiner do serviço do Redis](#testing-the-redis-service-container).

O nome do host é `localhost` ou `127.0.0.1`.

## Testar o contêiner de serviço Redis

Você pode testar o seu pipeline usando o script a seguir, que cria um cliente Redis e preenche o cliente com alguns dados de exemplo. Em seguida, o script imprime no terminal os valores armazenados no cliente Redis. Seu script pode usar qualquer idioma desejado, mas este exemplo usa o Node.js e o módulo npm `redis`. Para obter mais informações, confira o [módulo npm redis](https://www.npmjs.com/package/redis).

Você pode modificar o *client.js* para incluir todas as operações do Redis necessárias para o fluxo de trabalho. Neste exemplo, o script cria a instância do cliente Redis, adiciona dados temporários e, em seguida, recupera os dados.

Adicione um novo arquivo chamado *client.js* ao seu repositório com o seguinte código.

```javascript copy
const redis = require("redis");

// Creates a new Redis client
// If REDIS_HOST is not set, the default host is localhost
// If REDIS_PORT is not set, the default port is 6379
const redisClient = redis.createClient({
  url: `redis://${process.env.REDIS_HOST}:${process.env.REDIS_PORT}`
});

redisClient.on("error", (err) => console.log("Error", err));

(async () => {
  await redisClient.connect();

  // Sets the key "octocat" to a value of "Mona the octocat"
  const setKeyReply = await redisClient.set("octocat", "Mona the Octocat");
  console.log("Reply: " + setKeyReply);
  // Sets a key to "species", field to "octocat", and "value" to "Cat and Octopus"
  const SetFieldOctocatReply = await redisClient.hSet("species", "octocat", "Cat and Octopus");
  console.log("Reply: " + SetFieldOctocatReply);
  // Sets a key to "species", field to "dinotocat", and "value" to "Dinosaur and Octopus"
  const SetFieldDinotocatReply = await redisClient.hSet("species", "dinotocat", "Dinosaur and Octopus");
  console.log("Reply: " + SetFieldDinotocatReply);
  // Sets a key to "species", field to "robotocat", and "value" to "Cat and Robot"
  const SetFieldRobotocatReply = await redisClient.hSet("species", "robotocat", "Cat and Robot");
  console.log("Reply: " + SetFieldRobotocatReply);

  try {
    // Gets all fields in "species" key
    const replies = await redisClient.hKeys("species");
    console.log(replies.length + " replies:");
    replies.forEach((reply, i) => {
        console.log("    " + i + ": " + reply);
    });
    await redisClient.quit();
  }
  catch (err) {
    // statements to handle any exceptions
  }
})();
```

O script cria um cliente do Redis usando o método `createClient`, que aceita um parâmetro `host` e `port`. O script usa as variáveis de ambiente `REDIS_HOST` e `REDIS_PORT` para definir o endereço IP e a porta do cliente. Se `host` e `port` não estiverem definidos, o host padrão será `localhost` e a porta padrão será 6379.

O script usa os métodos `set` e `hset` para preencher o banco de dados com algumas chaves, campos e valores. Para confirmar se o cliente Redis contém os dados, o script imprime o conteúdo do banco de dados no registro do console.

Ao executar este fluxo de trabalho, você deve ver a saída a seguir na etapa "Conectar-se ao Redis", confirmando que você criou o cliente Redis e adicionou os dados:

```shell
Reply: OK
Reply: 1
Reply: 1
Reply: 1
3 replies:
    0: octocat
    1: dinotocat
    2: robotocat
```
