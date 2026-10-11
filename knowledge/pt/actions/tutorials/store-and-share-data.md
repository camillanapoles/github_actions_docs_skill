---
title: Armazenar e compartilhar dados com artefatos de fluxo de trabalho
description: Use artefatos para compartilhar dados entre trabalhos em um fluxo e armazene dados quando o fluxo de trabalho estiver concluído.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/store-and-share-data
captured: '2026-10-11'
section: GitHub Actions
---

# Armazenar e compartilhar dados com artefatos de fluxo de trabalho

_Use artefatos para compartilhar dados entre trabalhos em um fluxo e armazene dados quando o fluxo de trabalho estiver concluído._

## Pré-requisitos

Antes de realizar este tutorial, você precisa entender os artefatos do fluxo de trabalho. Confira [Artefatos do fluxo de trabalho](../concepts/workflows-and-actions/workflow-artifacts.md).

## Fazer upload da compilação e testar artefatos

A saída da compilação e teste de seu código muitas vezes produz arquivos que podem ser usados para depurar falhas em testes e códigos de produção que você pode implantar. Você pode configurar um workflow para compilar e testar o código enviado para o seu repositório e informar um status de sucesso ou falha. Você pode fazer upload da saída de compilação e teste para usar em implantações, para depurar falhas e testes com falhas e visualizar a cobertura do conjunto de teste.

Use a ação `upload-artifact` para carregar artefatos. Ao fazer o upload de um artefato, você pode especificar um arquivo ou diretório único, ou vários arquivos ou diretórios. Você também pode excluir certos arquivos ou diretórios e usar padrões coringa. Recomendamos que você forneça um nome para um artefato, mas se nenhum nome for fornecido, `artifact` será usado como o nome padrão. Para obter mais informações sobre a sintaxe, consulte a ação [actions/upload-artifact](https://github.com/actions/upload-artifact).

### Exemplo

Por exemplo, o seu repositório ou um aplicativo web pode conter arquivos SASS e TypeScript que você deve converter para CSS e JavaScript. Pressupondo que a sua configuração de build gere os arquivos compilados no diretório `dist`, você implantará os arquivos no diretório `dist` no seu servidor de aplicativos Web se todos os testes forem concluídos com sucesso.

```text
|-- hello-world (repository)
|   └── dist
|   └── tests
|   └── src
|       └── sass/app.scss
|       └── app.ts
|   └── output
|       └── test
|
```

Este exemplo mostra como criar um fluxo de trabalho para um projeto do Node.js que compila o código no diretório `src` e executa os testes no diretório `tests`. Você pode pressupor que a execução `npm test` produza um relatório de cobertura de código chamado `code-coverage.html` armazenado no diretório `output/test/`.

O fluxo de trabalho carrega os artefatos de produção no diretório `dist`, mas exclui os arquivos markdown. Ele também carrega o relatório `code-coverage.html` como outro artefato.

```yaml copy
name: Node CI

on: [push]

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: npm install, build, and test
        run: |
          npm install
          npm run build --if-present
          npm test
      - name: Archive production artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist-without-markdown
          path: |
            dist
            !dist/**/*.md
      - name: Archive code coverage results
        uses: actions/upload-artifact@v4
        with:
          name: code-coverage-report
          path: output/test/code-coverage.html
```

> \[!TIP]
> Para exibir os resultados da cobertura de código diretamente em pull requests, em vez de baixar artefatos, você pode enviar um relatório Cobertura XML para Code Quality. Confira [Configurando a cobertura de código para seu repositório](https://docs.github.com/pt/code-security/how-tos/maintain-quality-code/set-up-code-coverage).

## Configurar um período de retenção do artefato personalizado

Você pode definir um período de retenção personalizado para artefatos individuais criados por um fluxo de trabalho. Ao usar um fluxo de trabalho para criar um artefato, você pode usar `retention-days` com a ação `upload-artifact`. Este exemplo demonstra como definir um período de retenção personalizado de cinco dias para o artefato chamado `my-artifact`:

```yaml copy
  - name: 'Upload Artifact'
    uses: actions/upload-artifact@v4
    with:
      name: my-artifact
      path: my_file.txt
      retention-days: 5
```

O valor `retention-days` não pode exceder o limite de retenção definido pelo repositório, pela organização ou pela empresa.

## Fazer o download dos artefatos durante a execução de um fluxo de trabalho

Use a ação [`actions/download-artifact`](https://github.com/actions/download-artifact) para baixar artefatos já carregados durante uma execução de fluxo de trabalho.

> \[!NOTE]
> Se você quiser baixar artefatos de um fluxo de trabalho ou uma execução de fluxo de trabalho diferente, será necessário fornecer um token e executar o identificador. Confira [Baixar artefatos de outras execuções de fluxo de trabalho ou repositórios](https://github.com/actions/download-artifact?tab=readme-ov-file#download-artifacts-from-other-workflow-runs-or-repositories) na documentação da ação `download-artifact`.

Especifique o nome de um artefato para fazer o download de um artefato individual. Se você carregar um artefato sem especificar um nome, o nome padrão será `artifact`.

```yaml
- name: Download a single artifact
  uses: actions/download-artifact@v5
  with:
    name: my-artifact
```

Você também pode baixar todos os artefatos em uma execução de fluxo de trabalho sem especificar um nome. Isso pode ser útil se você estiver trabalhando com muitos artefatos.

```yaml
- name: Download all workflow run artifacts
  uses: actions/download-artifact@v5
```

Se você fizer o download de todos os artefatos da execução de um fluxo de trabalho, será criado um diretório para cada artefato usando seu nome.

Para obter mais informações sobre a sintaxe, consulte a ação [actions/download-artifact](https://github.com/actions/download-artifact).

## Passando dados entre trabalhos em um fluxo de trabalho

Use as ações `upload-artifact` e `download-artifact` para compartilhar dados entre trabalhos em um fluxo de trabalho. Este exemplo de fluxo de trabalho ilustra como transmitir dados entre trabalhos em um mesmo fluxo. Para obter mais informações, consulte as ações [actions/upload-artifact](https://github.com/actions/upload-artifact) e [download-artifact](https://github.com/actions/download-artifact).

Os trabalhos que são dependentes de artefatos de um trabalho anterior devem aguardar a finalização bem-sucedida do trabalho anterior. Esse fluxo de trabalho usa a palavra-chave `needs` para garantir que `job_1`, `job_2` e `job_3` sejam executados sequencialmente. Por exemplo, `job_2` exige o `job_1` usando a sintaxe `needs: job_1`.

O Job 1 (Trabalho 1) executa estas etapas:

* Faz um cálculo matemático e salva o resultado em um arquivo de texto chamado `math-homework.txt`.
* Usa a ação `upload-artifact` para carregar o `math-homework.txt` arquivo com o nome`homework_pre` do artefato.

O Job 2 (Trabalho 2) usa o resultado do trabalho anterior:

* Faz o download do artefato `homework_pre` enviado no trabalho anterior. Por padrão, a ação `download-artifact` baixa artefatos no diretório do workspace no qual a etapa está sendo executada. Use o parâmetro de entrada `path` para especificar outro diretório de download.
* Lê o valor do arquivo `math-homework.txt`, faz um cálculo matemático e salva o resultado em `math-homework.txt` novamente, substituindo o conteúdo.
* Carrega o arquivo `math-homework.txt`.
  Como os artefatos são considerados imutáveis em `v4`, é fornecida ao artefato uma entrada diferente, `homework_final`, como nome.

O Job 3 (Trabalho 3) mostra o resultado carregado no trabalho anterior:

* Baixe o artefato `homework_final` de Job 2.
* Imprime o resultado da equação matemática no log.

A operação matemática completa feita nesse exemplo de fluxo de trabalho é `(3 + 7) x 9 = 90`.

```yaml copy
name: Share data between jobs

on: [push]

jobs:
  job_1:
    name: Add 3 and 7
    runs-on: ubuntu-latest
    steps:
      - shell: bash
        run: |
          expr 3 + 7 > math-homework.txt
      - name: Upload math result for job 1
        uses: actions/upload-artifact@v4
        with:
          name: homework_pre
          path: math-homework.txt

  job_2:
    name: Multiply by 9
    needs: job_1
    runs-on: windows-latest
    steps:
      - name: Download math result for job 1
        uses: actions/download-artifact@v5
        with:
          name: homework_pre
      - shell: bash
        run: |
          value=`cat math-homework.txt`
          expr $value \* 9 > math-homework.txt
      - name: Upload math result for job 2
        uses: actions/upload-artifact@v4
        with:
          name: homework_final
          path: math-homework.txt

  job_3:
    name: Display results
    needs: job_2
    runs-on: macOS-latest
    steps:
      - name: Download math result for job 2
        uses: actions/download-artifact@v5
        with:
          name: homework_final
      - name: Print the final result
        shell: bash
        run: |
          value=`cat math-homework.txt`
          echo The result is $value
```

A execução do fluxo de trabalho arquivará quaisquer artefatos gerados por ele. Para obter mais informações sobre como baixar os artefatos arquivados, confira [Baixar artefatos do fluxo de trabalho](../how-tos/manage-workflow-runs/download-workflow-artifacts.md).

## Validando artefatos

Sempre que a ação upload-artifact é usada, ela retorna uma saída chamada `digest`. Este é um resumo em SHA256 do Artefato que você carregou durante uma execução de fluxo de trabalho.

Quando a ação download-artifact é usada para baixar esse artefato, ela calcula automaticamente o resumo desse artefato baixado e valida que ele corresponde à saída da etapa upload-artifact.

Se o resumo não corresponder, a execução exibirá um aviso na interface do usuário e nos logs de trabalho.

Para exibir o código hash SHA256, abra os logs do trabalho upload-artifact ou faça check-in da saída do Artefato que aparece na interface do usuário da execução do fluxo de trabalho.
