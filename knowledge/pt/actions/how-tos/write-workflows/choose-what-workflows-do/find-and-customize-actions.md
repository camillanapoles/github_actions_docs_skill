---
title: Usando blocos de construção pré-gravados no seu fluxo de trabalho
description: Você pode usar e personalizar ações escritas previamente para alimentar o fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions
captured: '2026-10-13'
section: How tos / Write workflows / Choose what workflows do
---

# Usando blocos de construção pré-gravados no seu fluxo de trabalho { #using-pre-written-building-blocks-in-your-workflow }

_Você pode usar e personalizar ações escritas previamente para alimentar o fluxo de trabalho._

## Navegação nas ações do Marketplace no editor de fluxo de trabalho { #browsing-marketplace-actions-in-the-workflow-editor }

Você pode pesquisar e navegar por ações diretamente no editor do fluxo de trabalho do seu repositório. Na barra lateral, você pode pesquisar uma ação específica, visualizar ações em destaque e pesquisar categorias em destaque. Você também pode exibir o número de estrelas que uma ação recebeu da GitHub comunidade.

1. No seu repositório, pesquise o arquivo do fluxo de trabalho que você deseja editar.
2. No canto superior direito da visualização do arquivo, para abrir o editor de fluxo de trabalho, clique em (Edit file).

![Captura de tela de um arquivo de fluxo de trabalho mostrando a seção de cabeçalho. O ícone de lápis para editar arquivos é destacado com um contorno laranja escuro.](https://docs.github.com/assets/images/help/repository/actions-edit-workflow-file.png)

1. À direita do editor, use a barra lateral GitHub Marketplace para navegar pelas ações. As ações com o selo (Creator verified by GitHub) indicam que GitHub verificou o criador da ação como uma organização parceira.

![Captura de tela de um fluxo de trabalho no editor de arquivos. A barra lateral mostra ações do Marketplace. Um selo "Criador verificado por GitHub" é destacado em laranja.](https://docs.github.com/assets/images/help/repository/actions-marketplace-sidebar.png)

## Adicionar uma ação ao seu fluxo de trabalho { #adding-an-action-to-your-workflow }

Você pode adicionar uma ação ao seu fluxo de trabalho fazendo referência à ação no arquivo do seu fluxo de trabalho. As ações que você usa no seu fluxo de trabalho podem ser definidas em:

* O mesmo repositório que o arquivo de fluxo de trabalho
* Qualquer repositório público
* Uma imagem de contêiner do Docker publicada no Docker Hub

Você pode exibir as ações referenciadas em seus GitHub Actions fluxos de trabalho como dependências no grafo de dependência do repositório que contém seus fluxos de trabalho. Para obter mais informações, confira "[Grafo de dependência](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependency-graph)".

!!! note
    Para aprimorar a segurança, o GitHub Actions não dá suporte a redirecionamentos de ações nem a fluxos de trabalho reutilizáveis. Isso significa que quando o proprietário, o nome do repositório de uma ação ou o nome da ação é alterado, todos os fluxos de trabalho que usarem essa ação com o nome anterior falharão.

### Adicionando uma ação a partir de GitHub Marketplace { #adding-an-action-from-github-marketplace }

Uma página de listagem de ação inclui a versão da ação e a sintaxe do fluxo de trabalho necessária para usar a ação. Para manter seu fluxo de trabalho estável mesmo quando atualizações são feitas em uma ação, você pode fazer referência à versão da ação a ser usada especificando a tag do Git ou do Docker no arquivo de fluxo de trabalho.

1. Navegue para a ação que você deseja usar no seu fluxo de trabalho.
2. Clique para exibir a listagem completa do marketplace relacionada à ação.
3. Em "Instalação", clique (Copy to clipboard) para copiar a sintaxe do fluxo de trabalho.

![Captura de tela da listagem de uma ação no marketplace. O ícone "Copiar para área de transferência" da ação está realçado com um contorno laranja escuro.](https://docs.github.com/assets/images/help/repository/actions-sidebar-detailed-view.png)

1. Cole a sintaxe como uma nova etapa no seu fluxo de trabalho. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps).
2. Se a ação exigir que você forneça entradas, defina-as no seu fluxo de trabalho. Para obter informações sobre as entradas que uma ação pode exigir, confira [Usando blocos de construção pré-gravados no seu fluxo de trabalho](find-and-customize-actions.md#using-inputs-and-outputs-with-an-action).

Você também pode habilitar Dependabot version updates para as ações que adiciona ao fluxo de trabalho. Para saber mais, confira [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

### Adicionando uma ação do mesmo repositório { #adding-an-action-from-the-same-repository }

Se uma ação for definida no mesmo repositório em que o arquivo de fluxo de trabalho usa a ação, você poderá referenciar a ação com a referência de auto repositório `$/path/to/dir` ou com a sintaxe `{owner}/{repo}@{ref}` ou `./path/to/dir` no arquivo de fluxo de trabalho. A sintaxe `$/` não está disponível em GitHub Enterprise Server.

Exemplo de estrutura de arquivo de repositório:

```shell
|-- hello-world (repository)
|   |__ .github
|       └── workflows
|           └── my-first-workflow.yml
|       └── actions
|           |__ hello-world-action
|               └── action.yml
```

Recomendamos referenciar a ação com a `$/path/to/dir` referência ao repositório self. Isso é resolvido para o mesmo repositório no commit atual, portanto, você não precisa fazer check-out do repositório primeiro. Para obter mais informações sobre como `$/` se compara a `{owner}/{repo}@{ref}` e `./`, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#example-using-an-action-in-the-same-repository-as-the-workflow-at-the-running-commit-recommended).

Exemplo de arquivo de fluxo de trabalho usando `$/`:

```yaml
jobs:
  my_first_job:
    runs-on: ubuntu-latest
    steps:
      # This step references an action in the same repository at the
      # running commit. No repository checkout is required.
      - name: Use hello-world-action
        uses: $/.github/actions/hello-world-action
```

Você também pode referenciar a ação com a sintaxe relativa `./path/to/dir` , mas ela é mais propensa a erros. O caminho é relativo (`./`) ao diretório de trabalho padrão (`github.workspace`, `$GITHUB_WORKSPACE`), portanto, requer uma etapa de check-out e, se a ação fizer check-out do repositório em um local diferente do fluxo de trabalho, o caminho relativo deverá ser atualizado.

Exemplo de arquivo de fluxo de trabalho usando `./`:

```yaml
jobs:
  my_first_job:
    runs-on: ubuntu-latest
    steps:
      # This step checks out a copy of your repository.
      - name: My first step - check out repository
        uses: actions/checkout@v6
      # This step references the directory that contains the action.
      - name: Use local hello-world-action
        uses: ./.github/actions/hello-world-action
```

O arquivo `action.yml` é usado para fornecer metadados para a ação. Saiba mais sobre o conteúdo deste arquivo em [Referência de sintaxe de metadados](../../../reference/workflows-and-actions/metadata-syntax.md).

### Adicionando uma ação de um repositório diferente { #adding-an-action-from-a-different-repository }

Se uma ação for definida em um repositório diferente do arquivo de fluxo de trabalho, você poderá referenciar a ação com a sintaxe `{owner}/{repo}@{ref}` no arquivo de fluxo de trabalho.

A ação deve ser armazenada em um repositório.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: actions/setup-node@v7
```

### Referenciando um contêiner no Docker Hub { #referencing-a-container-on-docker-hub }

Se uma ação for definida em uma imagem de contêiner do Docker publicada no Docker Hub, você deverá referenciar a ação com a sintaxe `docker://{image}:{tag}` no arquivo de fluxo de trabalho. Para proteger seu código e dados, é altamente recomendável verificar a integridade da imagem de contêiner do Docker de Docker Hub antes de usá-la em seu fluxo de trabalho.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: docker://alpine:3.8
```

Para ver alguns exemplos de ações do Docker, confira o [fluxo de trabalho Docker-image.yml](https://github.com/actions/starter-workflows/blob/main/ci/docker-image.yml) e o [Criando uma ação de contêiner do Docker](../../../tutorials/use-containerized-services/create-a-docker-container-action.md).

### Fortalecimento de segurança no uso de ações em seus fluxos de trabalho { #security-hardening-for-using-actions-in-your-workflows }

GitHub fornece recursos de segurança que você pode usar para aumentar a segurança de seus fluxos de trabalho. Você pode usar os recursos internos do GitHub para garantir que você seja notificado sobre vulnerabilidades nas ações que utiliza ou para automatizar o processo de manter atualizadas as ações em seus fluxos de trabalho. Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

## Usar o gerenciamento de versões para suas ações personalizadas { #using-release-management-for-your-custom-actions }

Os criadores de uma ação da comunidade têm a opção de usar tags, branches ou valores do SHA para gerenciar as versões da ação. Semelhante a qualquer dependência, você deve indicar a versão da ação que gostaria de usar, com base no seu conforto em aceitar automaticamente as atualizações da ação.

Você irá designar a versão da ação no seu arquivo de fluxo de trabalho. Verifique a documentação da ação para obter informações sobre suas abordagens de gerenciamento de release e para saber qual tag, branch ou valor de SHA usar.

!!! note
    Recomendamos que você use um valor SHA ao usar ações de terceiros. No entanto, é importante observar que Dependabot só criará Dependabot alerts para GitHub Actions vulneráveis que usam versionamento semântico. Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md#using-third-party-actions) e [Alertas do Dependabot](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependabot-alerts).

### Usar etiquetas { #using-tags }

As tags são úteis para permitir que você decida quando alternar entre versões maiores e menores, mas estas são mais efêmeras e podem ser movidas ou excluídas pelo mantenedor. Este exemplo demonstra como direcionar uma ação que foi marcada como `v1.0.1`:

```yaml
steps:
  - uses: actions/javascript-action@v1.0.1
```

### Usar SHAs { #using-shas }

Se você precisar de uma versão mais confiável, você deverá usar o valor de SHA associado à versão da ação. Os SHAs são imutáveis e, portanto, mais confiáveis que tags ou branches. No entanto, esta abordagem significa que você não receberá automaticamente atualizações de uma ação, incluindo correções de bugs e atualizações de segurança importantes. Você deve usar o valor SHA completo de um commit e não um valor abreviado.
Ao selecionar um SHA, verifique se ele está no repositório da ação e não em uma bifurcação do repositório. Este exemplo tem como destino o SHA de uma ação:

```yaml
steps:
  - uses: actions/javascript-action@a824008085750b8e136effc585c3cd6082bd575f
```

> [!TIP] Um arquivo de bloqueio de dependências do fluxo de trabalho fixa suas ações em commits verificados sem colocar SHAs em seus arquivos de fluxo de trabalho, de modo que suas referências `uses` permaneçam legíveis. Ele também abrange dependências transitivas, o que a fixação SHA não faz. Consulte [Arquivos de bloqueio de dependências do fluxo de trabalho](../../../concepts/security/workflow-dependency-lockfiles.md).

### Usar branches { #using-branches }

Especificar um branch de destino para a ação significa que ele sempre irá executar a versão atualmente nesse branch. Essa abordagem pode criar problemas se uma atualização do branch incluir mudanças significativas. Este exemplo é direcionado a um branch chamado `@main`:

```yaml
steps:
  - uses: actions/javascript-action@main
```

Para saber mais, confira [Como gerenciar ações personalizadas](../../create-and-publish-actions/manage-custom-actions.md#using-release-management-for-actions).

## Usar entradas e saídas com uma ação { #using-inputs-and-outputs-with-an-action }

Uma ação geralmente aceita ou exige entradas e gera saídas que você pode usar. Por exemplo, uma ação pode exigir que você especifique um caminho para um arquivo, o nome de uma etiqueta ou outros dados que usará como parte do processamento da ação.

Para ver as entradas e as saídas de uma ação, verifique o `action.yml` no diretório raiz do repositório.

Neste exemplo de `action.yml`, a palavra-chave `inputs` define uma entrada obrigatória chamada `file-path` e inclui um valor padrão que será usado se nenhum for especificado. A palavra-chave `outputs` define uma saída chamada `results-file`, que informa o local em que os resultados se encontram.

```yaml
name: "Example"
description: "Receives file and generates output"
inputs:
  file-path: # id of input
    description: "Path to test script"
    required: true
    default: "test-file.js"
outputs:
  results-file: # id of output
    description: "Path to results file"
```
