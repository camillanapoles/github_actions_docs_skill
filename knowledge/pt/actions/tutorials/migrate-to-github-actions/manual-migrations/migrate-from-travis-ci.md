---
title: Migrando de Travis CI para GitHub Actions
description: GitHub Actions e Travis CI compartilham várias semelhanças, o que ajuda a tornar relativamente simples migrar para GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-actions/manual-migrations/migrate-from-travis-ci
captured: '2026-10-11'
section: GitHub Actions
---

# Migrando de Travis CI para GitHub Actions

_GitHub Actions e Travis CI compartilham várias semelhanças, o que ajuda a tornar relativamente simples migrar para GitHub Actions._

## Introdução

Este guia ajuda você a migrar de Travis CI para GitHub Actions. Ele compara os seus conceitos e sintaxe, descreve as semelhanças e demonstra as suas diferentes abordagens em relação às tarefas comuns.

## Antes de começar

Antes de iniciar sua migração para GitHub Actions, seria útil se familiarizar com a forma como ele funciona:

* Para obter um exemplo rápido que demonstra um trabalho do GitHub Actions, consulte [Guia Rápido do GitHub Actions](../../../get-started/quickstart.md).
* Para aprender os conceitos essenciais GitHub Actions , consulte [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../store-and-share-data.md#passing-data-between-jobs-in-a-workflow).

## Comparar a execução do trabalho

Para fornecer controle sobre quando as tarefas de CI são executadas, um GitHub Actions\_fluxo de trabalho\_ usa *trabalhos* executados em paralelo por padrão. Cada trabalho contém *etapas* que são executadas em uma sequência definida por você. Se você precisa executar ações de configuração e limpeza para um trabalho, pode definir etapas em cada trabalho para realizar essas ações.

## Principais semelhanças

GitHub Actions e Travis CI compartilham certas semelhanças, e compreendê-las antecipadamente pode ajudar a suavizar o processo de migração.

### Usar a sintaxe de YAML

Travis CI e GitHub Actions ambos usam YAML para criar trabalhos e fluxos de trabalho, e esses arquivos são armazenados no repositório do código. Para obter mais informações sobre como GitHub Actions usa o YAML, consulte [Criando um exemplo de fluxo de trabalho](../../create-an-example-workflow.md).

### Variáveis personalizadas

O Travis CI permite que você defina variáveis e as compartilhe entre fases. Da mesma forma, GitHub Actions permite definir variáveis para um fluxo de trabalho. Para saber mais, confira [Armazenar informações em variáveis](../../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

### Variáveis padrão

Travis CI e GitHub Actions ambos incluem variáveis de ambiente padrão que você pode usar em seus arquivos YAML. Para GitHub Actions, você pode vê-los listados em [Referência de variáveis](../../../reference/workflows-and-actions/variables.md#default-environment-variables).

### Processamento paralelo do trabalho

O Travis CI pode usar `stages` para executar trabalhos em paralelo. Da mesma forma, GitHub Actions é executado `jobs` em paralelo. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idneeds).

### Distintivos de status

Travis CI e GitHub Actions ambos oferecem suporte a emblemas de status, que permitem mostrar se uma compilação foi bem-sucedida ou falhou.
Para saber mais, confira [Adicionar um selo de status de fluxo de trabalho](../../../how-tos/monitor-workflows/add-a-status-badge.md).

### Usando uma matriz

Travis CI e GitHub Actions ambos dão suporte a uma matriz, permitindo que você execute testes usando combinações de sistemas operacionais e pacotes de software. Para saber mais, confira [Executando variações de tarefas em um workflow](../../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md).

Abaixo, há um exemplo de comparação da sintaxe para cada sistema.

#### Sintaxe de CI do Travis para uma matriz

```yaml
matrix:
  include:
    - rvm: '2.5'
    - rvm: '2.6.3'
```

#### GitHub Actions sintaxe para uma matriz

```yaml
jobs:
  build:
    strategy:
      matrix:
        ruby: ['2.5', '2.6.3']
```

### Apontar para ramificações específicas

Travis CI e GitHub Actions permitem que você configure sua CI para um ramo específico. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#onpushbranchestagsbranches-ignoretags-ignore).

Abaixo, há um exemplo da sintaxe para cada sistema.

#### Sintaxe de CI do Travis para direcionar ramificações específicas

```yaml
branches:
  only:
    - main
    - 'mona/octocat'
```

#### GitHub Actions sintaxe para direcionar ramificações específicas

```yaml
on:
  push:
    branches:
      - main
      - 'mona/octocat'
```

### Verificar submódulos

Travis CI e GitHub Actions ambos permitem que você controle se os submódulos estão incluídos no clone do repositório.

Abaixo, há um exemplo da sintaxe para cada sistema.

#### Sintaxe do Travis CI para verificação de submódulos

```yaml
git:
  submodules: false
```

#### GitHub Actions sintaxe para verificar submódulos

```yaml
- uses: actions/checkout@v6
  with:
    submodules: false
```

### Usando variáveis de ambiente em uma matriz

Travis CI e GitHub Actions pode adicionar variáveis personalizadas a uma matriz de teste, o que permite que você se refira à variável em uma etapa posterior.

Em GitHub Actions, você pode usar a `include` chave para adicionar variáveis de ambiente personalizadas a uma matriz. Neste exemplo, as entradas de matriz para `node-version` cada uma são configuradas para usar valores diferentes para as variáveis e `site` de `datacenter` ambiente. Em `Echo site details` seguida, a etapa usa `env: ${{ matrix.env }}` para se referir às variáveis personalizadas:

```yaml
name: Node.js CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
       include:
         - node-version: '14.x'
           site: "prod"
           datacenter: "site-a"
         - node-version: '16.x'
           site: "dev"
           datacenter: "site-b"
    steps:
      - name: Echo site details
        env:
          SITE: ${{ matrix.site }}
          DATACENTER: ${{ matrix.datacenter }}
        run: echo $SITE $DATACENTER
```

## Principais recursos em GitHub Actions

Ao migrar do Travis CI, considere os seguintes principais recursos em GitHub Actions:

### Armazenar segredos

GitHub Actions permite armazenar segredos e referenciá-los em seus trabalhos.
GitHub Actions as organizações podem limitar quais repositórios podem acessar segredos da organização. As regras de proteção de implantação podem exigir a aprovação manual de um fluxo de trabalho para acessar segredos de um ambiente. Para saber mais, confira [Segredos](../../../concepts/security/secrets.md).

### Compartilhar arquivos entre trabalhos e fluxos de trabalho

GitHub Actions inclui suporte integrado para armazenamento de artefatos, permitindo que você compartilhe arquivos entre trabalhos em um fluxo de trabalho. Você também pode salvar os arquivos resultantes e compartilhá-los com outros fluxos de trabalho. Para saber mais, confira [Noções básicas sobre GitHub Actions](../../../get-started/understand-github-actions.md).

### Hospedar seus próprios executores

Se seus trabalhos exigirem hardware ou software específico, GitHub Actions permitirá que você hospede seus próprios executores e envie seus trabalhos para eles para processamento.               O GitHub Actions também permite que você use políticas para controlar como esses executores podem ser acessados, concedendo acesso em nível de organização ou repositório. Para saber mais, confira [Como gerenciar executores auto-hospedados](../../../how-tos/manage-runners/self-hosted-runners.md).

### Trabalhos simultâneos e tempo de execução

Os trabalhos simultâneos e os tempos GitHub Actions de execução do fluxo de trabalho podem variar dependendo do seu GitHub plano. Para saber mais, confira [Cobrança e uso](../../../concepts/billing-and-usage.md).

### Usando idiomas diferentes em GitHub Actions

Ao trabalhar com diferentes linguagens no GitHub Actions, você pode criar uma etapa no trabalho para configurar as dependências de linguagem. Para obter mais informações sobre como trabalhar com uma linguagem em particular, confira [Criar e testar seu código](../../build-and-test-code.md).

## Execução de scripts

GitHub Actions pode usar `run` etapas para executar scripts ou comandos de shell. Para usar um shell específico, você pode especificar o tipo `shell` ao fornecer o caminho para o script. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsrun).

Por exemplo:

```yaml
steps:
  - name: Run build script
    run: ./.github/scripts/build.sh
    shell: bash
```

## Tratamento de erros em GitHub Actions

Ao migrar para GitHub Actions, há diferentes abordagens para tratamento de erros que talvez você precise estar ciente.

### Manipulação de erros de script

GitHub Actions interromperá um trabalho imediatamente se uma das etapas retornar um código de erro. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#exit-codes-and-error-action-preference).

### Manipulação de erro de trabalho

GitHub Actions
`if` usa condicionais para executar trabalhos ou etapas em determinadas situações. Por exemplo, você poderá executar uma etapa quando outra etapa resultar em uma `failure()`. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#example-using-status-check-functions). Use também [`continue-on-error`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idcontinue-on-error) para impedir que uma execução de fluxo de trabalho seja interrompida em caso de falha de um trabalho.

## Migrar a sintaxe para condicionais e expressões

Para executar trabalhos com base em expressões condicionais, Travis CI e GitHub Actions compartilham uma sintaxe de condição semelhante `if`.               O GitHub Actions permite que você use o condicional `if` para impedir que uma etapa ou trabalho sejam executados, a não ser que uma condição seja atendida. Para saber mais, confira [Avaliar expressões em fluxos de trabalho e ações](../../../reference/workflows-and-actions/expressions.md).

Este exemplo demonstra como um condicional `if` pode controlar o fato de uma etapa ser executada:

```yaml
jobs:
  conditional:
    runs-on: ubuntu-latest
    steps:
      - run: echo "This step runs with str equals 'ABC' and num equals 123"
        if: env.str == 'ABC' && env.num == 123
```

## Migrar fases para etapas

Onde o Travis CI usa *fases* para executar *etapas*, GitHub Actions tem *etapas* que executam *ações*. Você pode encontrar ações predefinidas no [GitHub Marketplace](https://github.com/marketplace?type=actions), ou você pode criar suas próprias ações. Para saber mais, confira [Reutilização de automações](../../../how-tos/reuse-automations.md).

Abaixo, há um exemplo da sintaxe para cada sistema.

### Sintaxe do Travis CI para fases e etapas

```yaml
language: python
python:
  - "3.7"

script:
  - python script.py
```

### GitHub Actions sintaxe para etapas e ações

```yaml
jobs:
  run_python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: '3.7'
          architecture: 'x64'
      - run: python script.py
```

## Memorizar dependências

Travis CI e GitHub Actions permitem que você armazene dependências manualmente em cache para reutilização posterior.

Esses exemplos demonstram a sintaxe de cache para cada sistema.

### Sintaxe do Travis CI para cacheamento

```yaml
language: node_js
cache: npm
```

### A sintaxe do GitHub Actions para cache

```yaml
- name: Cache node modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: v1-npm-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: v1-npm-deps-
```

## Exemplos de tarefas comuns

Esta seção compara como GitHub Actions e Travis CI executam tarefas comuns.

### Configurar variáveis de ambiente

Você pode criar variáveis de ambiente personalizadas em um job GitHub Actions.

#### Sintaxe de CI do Travis para uma variável de ambiente

```yaml
env:
  - MAVEN_PATH="/usr/local/maven"
```

#### GitHub Actions fluxo de trabalho com uma variável de ambiente

```yaml
jobs:
  maven-build:
    env:
      MAVEN_PATH: '/usr/local/maven'
```

### Criar com Node.js

#### Travis CI para construir com Node.js

```yaml
install:
  - npm install
script:
  - npm run build
  - npm test
```

#### GitHub Actions fluxo de trabalho para compilação com Node.js

```yaml
name: Node.js CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - name: Use Node.js
        uses: actions/setup-node@v7
        with:
          node-version: '16.x'
      - run: npm install
      - run: npm run build
      - run: npm test
```

## Próximas etapas

Para continuar aprendendo sobre os principais recursos de GitHub Actions, consulte [Escrevendo fluxos de trabalho](../../../how-tos/write-workflows.md).
