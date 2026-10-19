---
title: Compilar e testar Python
description: Saiba como criar um fluxo de trabalho de CI (integração contínua) para criar e testar seu projeto de Python.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/build-and-test-code/python
captured: '2026-10-19'
section: Tutorials / Build and test code
---

# Compilar e testar Python

_Saiba como criar um fluxo de trabalho de CI (integração contínua) para criar e testar seu projeto de Python._

## Introdução

Este guia mostra como criar, testar e publicar um pacote Python.

GitHub-hosted runners têm um cache de ferramentas com software pré-instalado, que inclui Python e PyPy. Você não precisa instalar nada! Para obter uma lista completa do software atualizado e das versões pré-instaladas do Python e do PyPy, consulte [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md#preinstalled-software-for-github-owned-images).

## Pré-requisitos

Você deve estar familiarizado com YAML e a sintaxe para GitHub Actions. Para saber mais, confira [Escrevendo fluxos de trabalho](../../how-tos/write-workflows.md).

Recomendamos que você tenha uma compreensão básica de Python e pip. Para saber mais, veja:

* [Começando com Python](https://www.python.org/about/gettingstarted/)
* [Gerenciador de pacotes Pip](https://pypi.org/project/pip/)

## Usando um modelo de fluxo de trabalho Python

Para uma introdução rápida, adicione um modelo de fluxo de trabalho ao diretório `.github/workflows` do repositório.

GitHub fornece um modelo de fluxo de trabalho para Python que deve funcionar se o repositório já contiver pelo menos um arquivo `.py`. As seções subsequentes deste guia fornecem exemplos de como você pode personalizar esse modelo de fluxo de trabalho.

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Pesquise "Python aplicação".

5. No fluxo de trabalho "aplicativo Python", clique em **Configure**.

6. Edite o fluxo de trabalho conforme necessário. Por exemplo, altere a versão Python.

7. Clique em **Confirmar alterações**.

   O `python-app.yml` arquivo de fluxo de trabalho é adicionado ao `.github/workflows` diretório do repositório.

## Especificando uma versão Python

Para usar uma versão pré-instalada do Python ou PyPy em um executor hospedado em GitHub, use a ação `setup-python`. Essa ação localiza uma versão específica de Python ou PyPy do cache de ferramentas em cada executor e adiciona os binários necessários a `PATH`, que persiste para o restante do trabalho. Se uma versão específica do Python não estiver pré-instalada no cache de ferramentas, a ação `setup-python` baixará e configurará a versão apropriada do repositório [`python-versions`](https://github.com/actions/python-versions).

Usar a ação `setup-python` é a forma recomendada de usar Python com GitHub Actions, porque isso garante um comportamento consistente em diferentes executores e versões do Python. Se você estiver usando um executor auto-hospedado, deverá instalar Python e adicioná-lo a `PATH`. Para obter mais informações, confira a [Ação `setup-python`](https://github.com/marketplace/actions/setup-python).

A tabela abaixo descreve a localização do cache de ferramentas em cada runner hospedado em GitHub.

|                                      | Ubuntu                          | Mac                                      | Windows                               |
|------------------------------------|-------------------------------|----------------------------------------|-------------------------------------|
| **Diretório de cache da ferramenta** | `/opt/hostedtoolcache/*`        | `/Users/runner/hostedtoolcache/*`        | `C:\hostedtoolcache\windows\*`        |
| **Cache de Ferramentas do Python**   | `/opt/hostedtoolcache/Python/*` | `/Users/runner/hostedtoolcache/Python/*` | `C:\hostedtoolcache\windows\Python\*` |
| **Cache da ferramenta do PyPy**      | `/opt/hostedtoolcache/PyPy/*`   | `/Users/runner/hostedtoolcache/PyPy/*`   | `C:\hostedtoolcache\windows\PyPy\*`   |

Se você estiver usando um executor auto-hospedado, poderá configurar o executor para usar a ação `setup-python` a fim de gerenciar suas dependências. Para obter mais informações, confira [Como usar o setup-python com um executor auto-hospedado](https://github.com/actions/setup-python#using-setup-python-with-a-self-hosted-runner) no README de `setup-python`.

GitHub dá suporte à sintaxe semântica de controle de versão. Para obter mais informações, confira [Como usar o controle de versão semântico](https://docs.npmjs.com/about-semantic-versioning#using-semantic-versioning-to-specify-update-types-your-package-can-accept) e [Especificação de controle de versão semântico](https://semver.org/).

### Usando várias versões de Python

O exemplo a seguir usa uma matriz para o trabalho para configurar várias versões Python. Para saber mais, confira [Executando variações de tarefas em um workflow](../../how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md).

```yaml copy
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["pypy3.10", "3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v6
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # You can test your matrix by printing the current Python version
      - name: Display Python version
        run: python -c "import sys; print(sys.version)"
```

### Usando uma versão de Python específica

Você pode configurar uma versão específica do Python. Por exemplo, 3.12. Como alternativa, você pode usar a sintaxe da versão semântica para obter a última versão secundária. Este exemplo usa a versão secundária mais recente do Python 3.

```yaml copy
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6
      - name: Set up Python
        # This is the version of the action for setting up Python, not the Python version.
        uses: actions/setup-python@v5
        with:
          # Semantic version range syntax or exact version of a Python version
          python-version: '3.x'
          # Optional - x64 or x86 architecture, defaults to x64
          architecture: 'x64'
      # You can test your matrix by printing the current Python version
      - name: Display Python version
        run: python -c "import sys; print(sys.version)"
```

### Excluir uma versão

Se você especificar uma versão de Python que não está disponível, `setup-python` falhará com um erro como: `##[error]Version 3.7 with arch x64 not found`. A mensagem de erro inclui as versões disponíveis.

Você também pode usar a palavra-chave `exclude` em seu fluxo de trabalho se houver uma configuração de Python que você não deseja executar. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstrategy).

```yaml copy
name: Python package

on: [push]

jobs:
  build:

    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.9", "3.11", "3.13", "pypy3.10"]
        exclude:
          - os: macos-latest
            python-version: "3.11"
          - os: windows-latest
            python-version: "3.11"
```

### Usando a versão de Python padrão

É recomendável usar `setup-python` para configurar a versão de Python usada em seus fluxos de trabalho, pois ajuda a tornar suas dependências explícitas. Se você não usar `setup-python`, a versão padrão de Python definida em `PATH` será usada em qualquer shell quando você chamar `python`. A versão padrão do Python varia entre os executores hospedados em GitHub, o que pode causar alterações inesperadas ou fazer com que seja usada uma versão mais antiga do que a esperada.

| Executor hospedado emGitHub | Descrição |
| --- | --- |
| Ubuntu | Os executores do Ubuntu têm várias versões do sistema Python instaladas em `/usr/bin/python` e `/usr/bin/python3`. As versões Python que vêm empacotadas com o Ubuntu são além das versões que GitHub instala no cache de ferramentas. |
| Windows | Excluindo as versões de Python que estão no cache das ferramentas, o Windows não vem com uma versão equivalente do Python do sistema. Para manter um comportamento consistente com outros executores e permitir que o Python seja usado imediatamente, sem a ação `setup-python`, GitHub adiciona algumas versões do cache de ferramentas a `PATH`. |
| macOS | Os executores do macOS têm mais de uma versão do sistema Python instalada, além das versões que fazem parte do cache de ferramentas. As versões Python do sistema estão localizadas no diretório `/usr/local/Cellar/python/*`. |

## Instalar dependências

Os executores hospedados em GitHub têm o gerenciador de pacotes pip instalado. Você pode usar o pip para instalar dependências do registro de pacotes do PyPI antes de criar e testar o seu código. Por exemplo, o YAML abaixo instala ou atualiza o instalador de pacote `pip` e os pacotes `setuptools` e `wheel`.

Você também pode armazenar dependências em cache para acelerar seu fluxo de trabalho. Para saber mais, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- name: Install dependencies
  run: python -m pip install --upgrade pip setuptools wheel
```

### Arquivo de requisitos

Depois que você atualizar `pip`, uma próxima etapa típica será instalar dependências de `requirements.txt`. Para obter mais informações, confira [pip](https://pip.pypa.io/en/stable/cli/pip_install/#example-requirements-file).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

### Memorizar dependências

Você pode armazenar em cache e restaurar as dependências com a ação [`setup-python`](https://github.com/actions/setup-python).

O exemplo a seguir armazena dependências para pip.

```yaml copy
steps:
- uses: actions/checkout@v6
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
- run: pip install -r requirements.txt
- run: pip test
```

Por padrão, a ação `setup-python` pesquisa o arquivo de dependência (`requirements.txt` para pip, `Pipfile.lock` para pipenv, ou `poetry.lock` para poetry) em todo o repositório. Para obter mais informações, confira [Como armazenar dependências de pacotes em cache](https://github.com/actions/setup-python#caching-packages-dependencies) no README `setup-python`.

Se houver uma necessidade específica ou precisar de controles mais precisos de cache, use a [ação `cache`](https://github.com/marketplace/actions/cache). O Pip armazena dependências em diferentes locais, dependendo do sistema operacional do executor. O caminho que você precisa efetuar o armazenamento em cache pode ser diferente do exemplo do Ubuntu acima, dependendo do sistema operacional que você usa. Para obter mais informações, consulte [exemplos de cache do Python](https://github.com/actions/cache/blob/main/examples.md#python---pip) no repositório de ações `cache`.

## Testar seu código

Você pode usar os mesmos comandos usados localmente para criar e testar seu código.

### Testando com pytest e pytest-cov

Este exemplo instala ou atualiza `pytest` e `pytest-cov`. Em seguida, os testes são executados e retornados no formato JUnit enquanto os resultados da cobertura do código são emitidos em Cobertura. Para obter mais informações, confira [JUnit](https://junit.org/junit5/) e [Cobertura](https://cobertura.github.io/cobertura/).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
- name: Test with pytest
  run: |
    pip install pytest pytest-cov
    pytest tests.py --doctest-modules --junitxml=junit/test-results.xml --cov=com --cov-report=xml --cov-report=html
```

!!! tip
    Este exemplo já produz um relatório de cobertura XML de Cobertura (`--cov-report=xml`). Para exibir os resultados de cobertura diretamente nas pull requests, faça o upload do relatório usando a ação `actions/upload-code-coverage`. Consulte [Configurando a cobertura de código para seu repositório](https://docs.github.com/pt/code-security/how-tos/maintain-quality-code/set-up-code-coverage).

### Usando o Ruff para fazer lint e/ou formatar código

O exemplo a seguir instala ou atualiza o `ruff` e o usa para fazer lint de todos os arquivos. Para obter mais informações, confira [Ruff](https://docs.astral.sh/ruff).

```yaml copy
steps:
- uses: actions/checkout@v6
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- name: Install the code linting and formatting tool Ruff
  run: pipx install ruff
- name: Lint code with Ruff
  run: ruff check --output-format=github --target-version=py39
- name: Check code formatting with Ruff
  run: ruff format --diff --target-version=py39
  continue-on-error: true
```

A etapa de formatação tem o parâmetro `continue-on-error: true` definido. Isso impedirá que o fluxo de trabalho falhe se a etapa de formatação não for bem-sucedida. Após corrigir todos os erros de formatação, você poderá remover essa opção para que o fluxo de trabalho capture novos problemas.

### Executar testes com tox

Com GitHub Actions, você pode executar testes com tox e distribuir o trabalho entre várias tarefas. Você precisará invocar o tox usando a opção `-e py` para escolher a versão do Python em seu `PATH`, em vez de especificar uma versão específica. Para obter mais informações, confira [Tox](https://tox.readthedocs.io/en/latest/).

```yaml copy
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.9", "3.11", "3.13"]

    steps:
      - uses: actions/checkout@v6
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - name: Install tox and any other packages
        run: pip install tox
      - name: Run tox
        # Run tox using the version of Python in `PATH`
        run: tox -e py
```

## Empacotar dados do fluxo de trabalho como artefatos

Você pode fazer o upload de artefatos para visualização após a conclusão de um fluxo de trabalho. Por exemplo, é possível que você precise salvar os arquivos de registro, os despejos de núcleo, os resultados de teste ou capturas de tela. Para saber mais, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../store-and-share-data.md).

O exemplo a seguir demonstra como usar a ação `upload-artifact` para arquivar os resultados do teste da execução de `pytest`. Para obter mais informações, confira a [Ação `upload-artifact`](https://github.com/actions/upload-artifact).

```yaml copy
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v6
      - name: Setup Python # Set Python version
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      # Install pip and pytest
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest
      - name: Test with pytest
        run: pytest tests.py --doctest-modules --junitxml=junit/test-results-${{ matrix.python-version }}.xml
      - name: Upload pytest test results
        uses: actions/upload-artifact@v4
        with:
          name: pytest-results-${{ matrix.python-version }}
          path: junit/test-results-${{ matrix.python-version }}.xml
        # Use always() to always run this step to publish test results when there are test failures
        if: ${{ always() }}
```

## Publicando no PyPI

Você pode configurar seu fluxo de trabalho para publicar seu pacote de Python no PyPI depois que os testes de CI forem aprovados. Esta seção demonstra como você pode usar GitHub Actions para carregar seu pacote no PyPI sempre que publicar uma versão. Para saber mais, confira [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

O fluxo de trabalho de exemplo abaixo usa a [Publicação Confiável](https://docs.pypi.org/trusted-publishers/) para autenticar com o PyPI, eliminando a necessidade de um token de API configurado manualmente.

```yaml copy
```
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Upload Python Package

on:
  release:
    types: [published]

permissions:
  contents: read

jobs:
  release-build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Build release distributions
        run: |
          # NOTE: put your own distribution build steps here.
          python -m pip install build
          python -m build

      - name: Upload distributions
        uses: actions/upload-artifact@v4
        with:
          name: release-dists
          path: dist/

  pypi-publish:
    runs-on: ubuntu-latest

    needs:
      - release-build

    permissions:
      # IMPORTANT: this permission is mandatory for trusted publishing
      id-token: write

    # Dedicated environments with protections for publishing are strongly recommended.
    environment:
      name: pypi
      # OPTIONAL: uncomment and update to include your PyPI project URL in the deployment status:
      # url: https://pypi.org/p/YOURPROJECT

    steps:
      - name: Retrieve release distributions
        uses: actions/download-artifact@v5
        with:
          name: release-dists
          path: dist/

      - name: Publish release distributions to PyPI
        uses: pypa/gh-action-pypi-publish@6f7e8d9c0b1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d
```

Para obter mais informações sobre esse fluxo de trabalho, incluindo as configurações do PyPI necessárias, consulte [Configurando o OpenID Connect no PyPI](../../how-tos/secure-your-work/security-harden-deployments/oidc-in-pypi.md).
```
