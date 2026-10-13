---
title: Adicionar scripts ao seu fluxo de trabalho
description: Você pode usar GitHub Actions fluxos de trabalho para executar scripts.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/add-scripts
captured: '2026-10-13'
section: How tos / Write workflows / Choose what workflows do
---

# Adicionar scripts ao seu fluxo de trabalho

_Você pode usar GitHub Actions fluxos de trabalho para executar scripts._

Você pode usar um GitHub Actions fluxo de trabalho para executar scripts e comandos de shell, que são executados no executor atribuído. Este exemplo demonstra como usar a palavra-chave `run` para executar o comando `npm install -g bats` no executor.

```yaml
jobs:
  example-job:
    runs-on: ubuntu-latest
    steps:
      - run: npm install -g bats
```

Para usar um fluxo de trabalho para executar um script armazenado em seu repositório, primeiro você deve fazer check-out do repositório para o executor. Feito isso, você pode usar a palavra-chave `run` para executar o script no executor. O exemplo a seguir executa dois scripts, cada um em uma etapa de trabalho separada. O local dos scripts no executor é especificado definindo um diretório de trabalho padrão para comandos de execução. Para saber mais, confira [Definindo um shell padrão e diretório de trabalho](set-default-values-for-jobs.md).

```yaml
jobs:
  example-job:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./scripts
    steps:
      - name: Check out the repository to the runner
        uses: actions/checkout@v6
      - name: Run a script
        run: ./my-script.sh
      - name: Run another script
        run: ./my-other-script.sh
```

Todos os scripts que você deseja que um trabalho de fluxo de trabalho execute devem ser executáveis. Você pode fazer isso no fluxo de trabalho, passando o script como um argumento para o interpretador que executará o script, por exemplo, `run: bash script.sh`, ou tornando o próprio arquivo executável. Você pode dar ao arquivo a permissão de execução usando o comando `git update-index --chmod=+x PATH/TO/YOUR/script.sh` localmente e, em seguida, confirmando e enviando o arquivo por push para o repositório. Como alternativa, para fluxos de trabalho executados em executores Linux e Mac, você pode adicionar um comando para dar ao arquivo a permissão de execução no trabalho de fluxo de trabalho, antes de executar o script:

```yaml
jobs:
  example-job:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ./scripts
    steps:
      - name: Check out the repository to the runner
        uses: actions/checkout@v6
      - name: Make the script files executable
        run: chmod +x my-script.sh my-other-script.sh
      - name: Run the scripts
        run: |
          ./my-script.sh
          ./my-other-script.sh
```

Para saber mais sobre a palavra-chave `run`, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsrun).
