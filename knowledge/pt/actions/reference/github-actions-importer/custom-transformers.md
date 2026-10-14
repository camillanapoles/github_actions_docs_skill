---
title: Estendendo o Importador do GitHub Actions com transformadores personalizados
description: GitHub Actions Importer oferece a capacidade de estender seu mapeamento interno.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/github-actions-importer/custom-transformers
captured: '2026-10-11'
section: Reference / Github actions importer
---

# Estendendo o Importador do GitHub Actions com transformadores personalizados { #extending-github-actions-importer-with-custom-transformers }

_GitHub Actions Importer oferece a capacidade de estender seu mapeamento interno._

## Sobre transformadores personalizados { #about-custom-transformers }

GitHub Actions Importer oferece a capacidade de estender seu mapeamento interno criando transformadores personalizados. Os transformadores personalizados podem ser usados para:

* Converta itens que GitHub Actions Importer não converte automaticamente ou modifique como os itens são convertidos. Para obter mais informações, confira [Como criar transformadores personalizados para itens](#creating-custom-transformers-for-items).
* Converta referências em executores para usar rótulos de executores diferentes. Para mais informações, consulte [Como criar transformadores personalizados para executores](#creating-custom-transformers-for-runners).
* Converta os valores das variáveis de ambiente dos seus pipelines existentes para fluxos de trabalho GitHub Actions. Para obter mais informações, confira [Como criar transformadores personalizados para variáveis de ambiente](#creating-custom-transformers-for-environment-variables).

## Usando transformadores personalizados com GitHub Actions Importer { #using-custom-transformers-with-github-actions-importer }

Um transformador personalizado contém a lógica de mapeamento que GitHub Actions Importer pode usar para transformar seus plug-ins, tarefas, rótulos de executores ou variáveis de ambiente para funcionarem com GitHub Actions. Os transformadores personalizados são gravados com uma DSL (linguagem específica de domínio) criada com base no Ruby e são definidos em um arquivo com a extensão de arquivo `.rb`.

Você pode usar a opção da CLI `--custom-transformers` para especificar quais arquivos de transformador personalizados usar com os comandos `audit`, `dry-run` e `migrate`.

Por exemplo, se os transformadores personalizados forem definidos em um arquivo nomeado `transformers.rb`, você poderá usar o seguinte comando para usá-los com GitHub Actions Importer:

```shell
gh actions-importer ... --custom-transformers transformers.rb
```

Como alternativa, você pode usar a sintaxe de padrão glob para especificar vários arquivos de transformador personalizados. Por exemplo, se vários arquivos personalizados de transformador estiverem em um diretório chamado `transformers`, você pode fornecê-los todos ao GitHub Actions Importer com o seguinte comando:

```shell
gh actions-importer ... --custom-transformers transformers/*.rb
```

!!! note
    Quando você usa transformadores personalizados, os arquivos de transformador personalizados precisam residir no mesmo diretório ou em subdiretórios, no local em que o comando `gh actions-importer` é executado.

## Criar transformadores personalizados para itens { #creating-custom-transformers-for-items }

Você pode criar transformadores personalizados que GitHub Actions Importer usará ao converter etapas de build existentes ou gatilhos em seus equivalentes no GitHub Actions. Isso é especialmente útil quando:

* GitHub Actions Importer não converte automaticamente um item.
* Você deseja alterar a forma como um item é convertido por GitHub Actions Importer.
* Seus pipelines existentes usam extensões personalizadas ou proprietárias, como bibliotecas compartilhadas no Jenkins, e você precisa definir como essas etapas devem funcionar.GitHub Actions

GitHub Actions Importer usa transformadores personalizados que são definidos usando uma DSL criada sobre Ruby. Para criar transformadores personalizados para etapas de compilação e gatilhos:

* Cada arquivo de transformador personalizado deve conter pelo menos um método `transform`.
* Cada método `transform` deve retornar um `Hash`, uma matriz de `Hash` ou `nil`. Esse valor retornado corresponderá a uma ação definida no YAML. Para obter mais informações sobre ações, confira [Noções básicas sobre GitHub Actions](../../get-started/understand-github-actions.md).

### Exemplo de transformador personalizado para uma etapa de compilação { #example-custom-transformer-for-a-build-step }

O seguinte exemplo converte uma etapa de compilação que usa o identificador "buildJavaScriptApp" para executar vários comandos `npm`:

```ruby copy
transform "buildJavaScriptApp" do |item|
  command = ["build", "package", "deploy"].map do |script|
    "npm run #{script}"
  end

  {
    name: "build javascript app",
    run: command.join("\n")
  }
end
```

O exemplo acima resulta na seguinte etapa do fluxo de trabalho GitHub Actions. Ele é composto por etapas de compilação convertidas que tinham um identificador `buildJavaScriptApp`:

```yaml
- name: build javascript app
  run: |
    npm run build
    npm run package
    npm run deploy
```

O método `transform` usa o identificador da etapa de compilação da instância de CI/CD de origem em um argumento. Neste exemplo, o identificador é `buildJavaScriptLibrary`. Você também pode usar valores separados por vírgulas para passar vários identificadores para o método `transform`. Por exemplo, `transform "buildJavaScriptApp", "buildTypeScriptApp" { |item| ... }`.

!!! note
    A estrutura de dados de `item` será diferente dependendo da plataforma de CI/CD e do tipo de item que está sendo convertido.

## Criando transformadores customizados para runners { #creating-custom-transformers-for-runners }

Você pode personalizar o mapeamento entre os executores na instância de CI/CD de origem e seus executores GitHub Actions equivalentes.

GitHub Actions Importer usa transformadores personalizados que são definidos usando uma DSL criada sobre Ruby. Para criar transformadores personalizados para executores:

* O arquivo de transformador personalizado deve ter pelo menos um método `runner`.
* O método `runner` aceita dois parâmetros. O primeiro parâmetro é o rótulo de executor da instância de CI/CD de origem e o segundo parâmetro é o rótulo de executor correspondente GitHub Actions . Para obter mais informações sobre os executores GitHub Actions, consulte [Referência de executores hospedados pelo GitHub](../runners/github-hosted-runners.md#supported-runners-and-hardware-resources).

### Exemplo de transformadores personalizados para runners { #example-custom-transformers-for-runners }

O exemplo a seguir mostra um método `runner` que converte um rótulo de executor em um rótulo de executor GitHub Actions no fluxo de trabalho resultante.

```ruby copy
runner "linux", "ubuntu-latest"
```

Você também pode usar o método `runner` para converter um rótulo de executor em vários rótulos de executor GitHub Actions no fluxo de trabalho gerado.

```ruby copy
runner "big-agent", ["self-hosted", "xl", "linux"]
```

GitHub Actions Importer tenta mapear o rótulo do executor da melhor forma possível. Nos casos em que ele não pode fazer isso, o rótulo do executor `ubuntu-latest` é usado como padrão. Você pode usar uma palavra-chave especial com o método `runner` para controlar esse valor padrão. Por exemplo, o seguinte transformador personalizado instrui GitHub Actions Importer a usar `macos-latest` como o executor padrão em vez de `ubuntu-latest`.

```ruby copy
runner :default, "macos-latest"
```

## Criar transformadores personalizados para variáveis de ambiente { #creating-custom-transformers-for-environment-variables }

Você pode personalizar o mapeamento entre as variáveis de ambiente dos seus pipelines de CI/CD de origem e seus respectivos valores em GitHub Actions.

GitHub Actions Importer usa transformadores personalizados que são definidos usando uma DSL criada sobre Ruby. Para criar transformadores personalizados para variáveis de ambiente:

* O arquivo de transformador personalizado deve ter pelo menos um método `env`.
* O método `env` aceita dois parâmetros. O primeiro parâmetro é o nome da variável de ambiente no pipeline original e o segundo parâmetro é o valor atualizado da variável de ambiente para GitHub Actions. Para obter mais informações sobre GitHub Actions variáveis de ambiente, consulte [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

### Exemplo de transformadores personalizados para variáveis de ambiente { #example-custom-transformers-for-environment-variables }

Há várias maneiras de configurar os transformadores personalizados para mapear suas variáveis de ambiente.

* O exemplo a seguir define o valor de qualquer variável de ambiente existente chamada `OCTO`, como `CAT` ao transformar um pipeline.

        ```ruby copy
  env "OCTO", "CAT"
        ```

  Você também pode remover todas as instâncias de uma variável de ambiente específica para que elas não sejam transformadas em um GitHub Actions fluxo de trabalho. O exemplo a seguir remove todas as variáveis de ambiente com o nome `MONA_LISA`.

        ```ruby copy
  env "MONA_LISA", nil
        ```

* Você também pode mapear suas variáveis de ambiente existentes para segredos. Por exemplo, o método `env` a seguir mapeia uma variável de ambiente chamada `MONALISA` para um segredo chamado `OCTOCAT`.

        ```ruby copy
  env "MONALISA", secret("OCTOCAT")
        ```

  Isso configurará uma referência a um segredo chamado `OCTOCAT` no fluxo de trabalho transformado. Para que o segredo funcione, você precisará criar o segredo em seu repositório GitHub. Para saber mais, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository).

* Você também pode usar expressões regulares para atualizar os valores de diversas variáveis de ambiente ao mesmo tempo. Por exemplo, o seguinte transformador personalizado remove todas as variáveis de ambiente do fluxo de trabalho convertido:

        ```ruby copy
  env /.*/, nil
        ```

  O exemplo a seguir usa um grupo de correspondência de expressão regular para transformar os valores de variáveis de ambiente em segredos gerados dinamicamente.

        ```ruby copy
  env /^(.+)_SSH_KEY/, secret("%s_SSH_KEY)
        ```

!!! note

  > A ordem na qual os métodos `env` são definidos importa ao usar expressões regulares. O primeiro transformador `env` que corresponde a um nome de variável de ambiente tem precedência sobre métodos `env` subsequentes. Você deve definir primeiro os transformadores de variáveis de ambiente mais específicos.

## Aviso legal { #legal-notice }

Partes foram adaptadas do <https://github.com/github/gh-actions-importer/> de acordo com a licença MIT:

```text
MIT License

Copyright (c) 2022 GitHub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
