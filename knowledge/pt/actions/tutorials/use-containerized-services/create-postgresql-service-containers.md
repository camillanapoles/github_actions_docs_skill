---
title: Criar contêineres de serviço PostgreSQL
description: Você pode criar um contêiner de serviço PostgreSQL para usar no seu fluxo de trabalho. Este guia mostra exemplos para criar um serviço PostgreSQL para trabalhos executados em contêineres ou diretamente na máquina executora.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-containerized-services/create-postgresql-service-containers
captured: '2026-10-26'
section: Tutorials / Use containerized services
---

# Criar contêineres de serviço PostgreSQL

_Você pode criar um contêiner de serviço PostgreSQL para usar no seu fluxo de trabalho. Este guia mostra exemplos para criar um serviço PostgreSQL para trabalhos executados em contêineres ou diretamente na máquina executora._

## Introdução

Este guia mostra exemplos de fluxo de trabalho que configuram um contêiner de serviço usando a imagem Docker Hub `postgres`. O fluxo de trabalho executa um script que se conecta ao serviço do PostgreSQL, cria uma tabela e, em seguida, preenche-a com dados. Para testar se o fluxo de trabalho cria e preenche a tabela do PostgreSQL, o script imprime os dados da tabela para o console.

!!! note
    Se os fluxos de trabalho usarem ações de contêiner do Docker, contêineres de trabalho ou contêineres de serviço, você precisará usar um executor do Linux:

    * Se você estiver usando executores hospedados em GitHub, você deverá usar um executor do Ubuntu.
    * Se você estiver usando executores auto-hospedados, você deve usar uma máquina Linux, pois seu executor e o Docker precisam ser instalados.

## Pré-requisitos

Você deve estar familiarizado com a forma como contêineres de serviço funcionam com GitHub Actions e as diferenças de rede entre trabalhos em execução diretamente no executor ou em um contêiner. Para saber mais, confira [Comunicar-se com os contêineres de serviço do Docker](use-docker-service-containers.md).

Você também pode achar útil ter um conhecimento básico de YAML, da sintaxe para GitHub Actions e de PostgreSQL. Para saber mais, veja:

* [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md)
* [Tutorial do PostgreSQL](https://www.postgresqltutorial.com/) na documentação do PostgreSQL

## Executar trabalhos em contêineres

A configuração de tarefas a serem executadas em um contêiner simplifica as configurações de rede entre o trabalho e os contêineres do serviço. Docker contêineres na mesma rede de ponte definida pelo usuário expõe todas as portas umas para as outras, então você não precisa mapear nenhuma das portas de contêiner de serviço para o host Docker. Você pode acessar o contêiner de serviço do contêiner de trabalho usando a etiqueta que você configurar no fluxo de trabalho.

Você pode copiar esse arquivo de fluxo de trabalho para o diretório `.github/workflows` do repositório e modificá-lo conforme necessário.

```yaml copy
name: PostgreSQL service example
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
      postgres:
        # Docker Hub image
        image: postgres
        # Provide the password for postgres
        env:
          POSTGRES_PASSWORD: postgres
        # Set health checks to wait until postgres has started
        options: >-
          --health-cmd pg_isready
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

      - name: Connect to PostgreSQL
        # Runs a script that creates a PostgreSQL table, populates
        # the table with data, and then retrieves the data.
        run: node client.js
        # Environment variables used by the `client.js` script to create a new PostgreSQL table.
        env:
          # The hostname used to communicate with the PostgreSQL service container
          POSTGRES_HOST: postgres
          # The default PostgreSQL port
          POSTGRES_PORT: 5432
```

### Com configurar o trabalho do executor para trabalhos em contêineres

Este fluxo de trabalho configura uma tarefa que é executada no contêiner `node:20-bookworm-slim` e usa o executor do `ubuntu-latest`  hospedado no GitHub como host do Docker para o contêiner. Para obter mais informações sobre o contêiner `node:20-bookworm-slim`, confira a [imagem do nó](https://hub.docker.com/_/node) no Docker Hub.

O fluxo de trabalho configura um contêiner de serviço com o rótulo `postgres`. Todos os serviços precisam ser executados em um contêiner, ou seja, cada serviço exige que você especifique o contêiner `image`. Este exemplo usa a imagem de contêiner `postgres`, fornece a senha padrão do PostgreSQL e inclui opções de verificação de integridade para verificar se o serviço está em execução. Para obter mais informações, confira a [imagem do Postgres](https://hub.docker.com/_/postgres) no Docker Hub.

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
      postgres:
        # Docker Hub image
        image: postgres
        # Provide the password for postgres
        env:
          POSTGRES_PASSWORD: postgres
        # Set health checks to wait until postgres has started
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
```

### Configurar as etapas para trabalhos em contêineres

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

  - name: Connect to PostgreSQL
    # Runs a script that creates a PostgreSQL table, populates
    # the table with data, and then retrieves the data.
    run: node client.js
    # Environment variable used by the `client.js` script to create
    # a new PostgreSQL client.
    env:
      # The hostname used to communicate with the PostgreSQL service container
      POSTGRES_HOST: postgres
      # The default PostgreSQL port
      POSTGRES_PORT: 5432
```

O script *client.js* procura as variáveis de ambiente `POSTGRES_HOST` e `POSTGRES_PORT` para criar o cliente. O fluxo de trabalho define essas duas variáveis de ambiente como parte da etapa "Conectar-se ao PostgreSQL" para disponibilizá-las ao script *client.js*. Para obter mais informações sobre o script, confira [Como testar o contêiner do serviço do PostgreSQL](#testing-the-postgresql-service-container).

O nome do host do serviço PostgreSQL é o rótulo configurado no fluxo de trabalho, nesse caso, `postgres`. Uma vez que os contêineres do Docker na mesma rede da ponte definida pelo usuário abrem todas as portas por padrão, você poderá acessar o contêiner de serviço na porta-padrão 5432 do PostgreSQL.

## Executar trabalhos diretamente na máquina executora

Ao executar um trabalho diretamente na máquina executora, você deverá mapear as portas no contêiner de serviço às portas do host Docker. Você pode acessar os contêineres de serviço do host do Docker usando o `localhost` e o número da porta do host do Docker.

Você pode copiar esse arquivo de fluxo de trabalho para o diretório `.github/workflows` do repositório e modificá-lo conforme necessário.

```yaml copy
name: PostgreSQL Service Example
on: push

jobs:
  # Label of the runner job
  runner-job:
    # You must use a Linux environment when using service containers or container jobs
    runs-on: ubuntu-latest

    # Service containers to run with `runner-job`
    services:
      # Label used to access the service container
      postgres:
        # Docker Hub image
        image: postgres
        # Provide the password for postgres
        env:
          POSTGRES_PASSWORD: postgres
        # Set health checks to wait until postgres has started
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          # Maps tcp port 5432 on service container to the host
          - 5432:5432

    steps:
      # Downloads a copy of the code in your repository before running CI tests
      - name: Check out repository code
        uses: actions/checkout@v6

      # Performs a clean installation of all dependencies in the `package.json` file
      # For more information, see https://docs.npmjs.com/cli/ci.html
      - name: Install dependencies
        run: npm ci

      - name: Connect to PostgreSQL
        # Runs a script that creates a PostgreSQL table, populates
        # the table with data, and then retrieves the data
        run: node client.js
        # Environment variables used by the `client.js` script to create
        # a new PostgreSQL table.
        env:
          # The hostname used to communicate with the PostgreSQL service container
          POSTGRES_HOST: localhost
          # The default PostgreSQL port
          POSTGRES_PORT: 5432
```

### Configurar o trabalho do executor para trabalhos diretamente no computador do executor

O exemplo usa o executor hospedado no `ubuntu-latest`  GitHub como o host do Docker.

O fluxo de trabalho configura um contêiner de serviço com o rótulo `postgres`. Todos os serviços precisam ser executados em um contêiner, ou seja, cada serviço exige que você especifique o contêiner `image`. Este exemplo usa a imagem de contêiner `postgres`, fornece a senha padrão do PostgreSQL e inclui opções de verificação de integridade para verificar se o serviço está em execução. Para obter mais informações, confira a [imagem do Postgres](https://hub.docker.com/_/postgres) no Docker Hub.

O fluxo de trabalho mapeia a porta 5432 no contêiner de serviço do PostgreSQL para o host do Docker. Para saber mais sobre a palavra-chave `ports`, confira [Comunicar-se com os contêineres de serviço do Docker](use-docker-service-containers.md#mapping-docker-host-and-service-container-ports).

```yaml copy
jobs:
  # Label of the runner job
  runner-job:
    # You must use a Linux environment when using service containers or container jobs
    runs-on: ubuntu-latest

    # Service containers to run with `runner-job`
    services:
      # Label used to access the service container
      postgres:
        # Docker Hub image
        image: postgres
        # Provide the password for postgres
        env:
          POSTGRES_PASSWORD: postgres
        # Set health checks to wait until postgres has started
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          # Maps tcp port 5432 on service container to the host
          - 5432:5432
```

### Configurar as etapas para trabalhos diretamente no computador executor

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

  - name: Connect to PostgreSQL
    # Runs a script that creates a PostgreSQL table, populates
    # the table with data, and then retrieves the data
    run: node client.js
    # Environment variables used by the `client.js` script to create
    # a new PostgreSQL table.
    env:
      # The hostname used to communicate with the PostgreSQL service container
      POSTGRES_HOST: localhost
      # The default PostgreSQL port
      POSTGRES_PORT: 5432
```

O script *client.js* procura as variáveis de ambiente `POSTGRES_HOST` e `POSTGRES_PORT` para criar o cliente. O fluxo de trabalho define essas duas variáveis de ambiente como parte da etapa "Conectar-se ao PostgreSQL" para disponibilizá-las ao script *client.js*. Para obter mais informações sobre o script, confira [Como testar o contêiner do serviço do PostgreSQL](#testing-the-postgresql-service-container).

O nome do host é `localhost` ou `127.0.0.1`.

## Testar o contêiner de serviço do PostgreSQL

Você pode testar o seu fluxo de trabalho usando o seguinte script, que se conecta ao serviço do PostgreSQL e adiciona uma nova tabela com alguns dados de espaço reservado. Em seguida, o script imprime os valores armazenados na tabela do PostgreSQL no terminal. Seu script pode usar qualquer idioma desejado, mas este exemplo usa o Node.js e o módulo npm `pg`. Para obter mais informações, confira o [módulo npm pg](https://www.npmjs.com/package/pg).

Você pode modificar o *client.js* para incluir todas as operações do PostgreSQL necessárias para o fluxo de trabalho. Neste exemplo, o script se conecta ao serviço PostgreSQL, adiciona uma tabela ao banco de dados `postgres`, insere alguns dados de espaço reservado e recupera os dados.

Adicione um novo arquivo chamado *client.js* ao seu repositório com o seguinte código.

```javascript copy
const { Client } = require('pg');

const pgclient = new Client({
    host: process.env.POSTGRES_HOST,
    port: process.env.POSTGRES_PORT,
    user: 'postgres',
    password: 'postgres',
    database: 'postgres'
});

pgclient.connect();

const table = 'CREATE TABLE student(id SERIAL PRIMARY KEY, firstName VARCHAR(40) NOT NULL, lastName VARCHAR(40) NOT NULL, age INT, address VARCHAR(80), email VARCHAR(40))'
const text = 'INSERT INTO student(firstname, lastname, age, address, email) VALUES($1, $2, $3, $4, $5) RETURNING *'
const values = ['Mona the', 'Octocat', 9, '88 Colin P Kelly Jr St, San Francisco, CA 94107, United States', 'octocat@github.com']

pgclient.query(table, (err, res) => {
    if (err) throw err
});

pgclient.query(text, values, (err, res) => {
    if (err) throw err
});

pgclient.query('SELECT * FROM student', (err, res) => {
    if (err) throw err
    console.log(err, res.rows) // Print the data in student table
    pgclient.end()
});
```

O script cria uma conexão com o serviço PostgreSQL e usa as variáveis de ambiente `POSTGRES_HOST` e `POSTGRES_PORT` para especificar a porta ou o endereço IP do serviço PostgreSQL. Se `host` e `port` não estiverem definidos, o host padrão será `localhost` e a porta padrão será 5432.

O script cria uma tabela e preenche com dados de espaço reservado. Para testar se o banco de dados `postgres` contém os dados, o script imprime o conteúdo da tabela no log do console.

Ao executar este fluxo de trabalho, você verá a seguinte saída na etapa "Conectar ao PostgreSQL", que confirma que você criou com sucesso a tabela do PostgreSQL e adicionou dados:

```text
null [ { id: 1,
    firstname: 'Mona the',
    lastname: 'Octocat',
    age: 9,
    address:
     '88 Colin P Kelly Jr St, San Francisco, CA 94107, United States',
    email: 'octocat@github.com' } ]
```
