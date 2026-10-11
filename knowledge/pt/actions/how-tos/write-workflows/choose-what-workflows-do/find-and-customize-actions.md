---
title: Usando blocos de construção pré-gravados no seu fluxo de trabalho
description: Você pode usar e personalizar ações escritas previamente para alimentar o fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions
captured: '2026-10-11'
section: GitHub Actions
---

# Usando blocos de construção pré-gravados no seu fluxo de trabalho

_Você pode usar e personalizar ações escritas previamente para alimentar o fluxo de trabalho._

## Navegação nas ações do Marketplace no editor de fluxo de trabalho

Você pode pesquisar e navegar por ações diretamente no editor do fluxo de trabalho do seu repositório. Na barra lateral, você pode pesquisar uma ação específica, visualizar ações em destaque e pesquisar categorias em destaque. Você também pode exibir o número de estrelas que uma ação recebeu da GitHub comunidade.

1. No seu repositório, pesquise o arquivo do fluxo de trabalho que você deseja editar.
2. No canto superior direito da visualização do arquivo, para abrir o editor de fluxo de trabalho, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-pencil" aria-label="Edit file" role="img"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"></path></svg>.

![Captura de tela de um arquivo de fluxo de trabalho mostrando a seção de cabeçalho. O ícone de lápis para editar arquivos é destacado com um contorno laranja escuro.](/assets/images/help/repository/actions-edit-workflow-file.png)

1. À direita do editor, use a barra lateral GitHub Marketplace para navegar pelas ações. As ações com o selo <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-verified" aria-label="Creator verified by GitHub" role="img"><path d="m9.585.52.929.68c.153.112.331.186.518.215l1.138.175a2.678 2.678 0 0 1 2.24 2.24l.174 1.139c.029.187.103.365.215.518l.68.928a2.677 2.677 0 0 1 0 3.17l-.68.928a1.174 1.174 0 0 0-.215.518l-.175 1.138a2.678 2.678 0 0 1-2.241 2.241l-1.138.175a1.17 1.17 0 0 0-.518.215l-.928.68a2.677 2.677 0 0 1-3.17 0l-.928-.68a1.174 1.174 0 0 0-.518-.215L3.83 14.41a2.678 2.678 0 0 1-2.24-2.24l-.175-1.138a1.17 1.17 0 0 0-.215-.518l-.68-.928a2.677 2.677 0 0 1 0-3.17l.68-.928c.112-.153.186-.331.215-.518l.175-1.14a2.678 2.678 0 0 1 2.24-2.24l1.139-.175c.187-.029.365-.103.518-.215l.928-.68a2.677 2.677 0 0 1 3.17 0ZM7.303 1.728l-.927.68a2.67 2.67 0 0 1-1.18.489l-1.137.174a1.179 1.179 0 0 0-.987.987l-.174 1.136a2.677 2.677 0 0 1-.489 1.18l-.68.928a1.18 1.18 0 0 0 0 1.394l.68.927c.256.348.424.753.489 1.18l.174 1.137c.078.509.478.909.987.987l1.136.174a2.67 2.67 0 0 1 1.18.489l.928.68c.414.305.979.305 1.394 0l.927-.68a2.67 2.67 0 0 1 1.18-.489l1.137-.174a1.18 1.18 0 0 0 .987-.987l.174-1.136a2.67 2.67 0 0 1 .489-1.18l.68-.928a1.176 1.176 0 0 0 0-1.394l-.68-.927a2.686 2.686 0 0 1-.489-1.18l-.174-1.137a1.179 1.179 0 0 0-.987-.987l-1.136-.174a2.677 2.677 0 0 1-1.18-.489l-.928-.68a1.176 1.176 0 0 0-1.394 0ZM11.28 6.78l-3.75 3.75a.75.75 0 0 1-1.06 0L4.72 8.78a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L7 8.94l3.22-3.22a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg> indicam que GitHub verificou o criador da ação como uma organização parceira.

![Captura de tela de um fluxo de trabalho no editor de arquivos. A barra lateral mostra ações do Marketplace. Um selo "Criador verificado por GitHub" é destacado em laranja.](/assets/images/help/repository/actions-marketplace-sidebar.png)

## Adicionar uma ação ao seu fluxo de trabalho

Você pode adicionar uma ação ao seu fluxo de trabalho fazendo referência à ação no arquivo do seu fluxo de trabalho. As ações que você usa no seu fluxo de trabalho podem ser definidas em:

* O mesmo repositório que o arquivo de fluxo de trabalho
* Qualquer repositório público
* Uma imagem de contêiner do Docker publicada no Docker Hub

Você pode exibir as ações referenciadas em seus GitHub Actions fluxos de trabalho como dependências no grafo de dependência do repositório que contém seus fluxos de trabalho. Para obter mais informações, confira "[Grafo de dependência](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependency-graph)".

> \[!NOTE]
> Para aprimorar a segurança, o GitHub Actions não dá suporte a redirecionamentos de ações nem a fluxos de trabalho reutilizáveis. Isso significa que quando o proprietário, o nome do repositório de uma ação ou o nome da ação é alterado, todos os fluxos de trabalho que usarem essa ação com o nome anterior falharão.

### Adicionando uma ação a partir de GitHub Marketplace

Uma página de listagem de ação inclui a versão da ação e a sintaxe do fluxo de trabalho necessária para usar a ação. Para manter seu fluxo de trabalho estável mesmo quando atualizações são feitas em uma ação, você pode fazer referência à versão da ação a ser usada especificando a tag do Git ou do Docker no arquivo de fluxo de trabalho.

1. Navegue para a ação que você deseja usar no seu fluxo de trabalho.
2. Clique para exibir a listagem completa do marketplace relacionada à ação.
3. Em "Instalação", clique <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-copy" aria-label="Copy to clipboard" role="img"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg> para copiar a sintaxe do fluxo de trabalho.

![Captura de tela da listagem de uma ação no marketplace. O ícone "Copiar para área de transferência" da ação está realçado com um contorno laranja escuro.](/assets/images/help/repository/actions-sidebar-detailed-view.png)

1. Cole a sintaxe como uma nova etapa no seu fluxo de trabalho. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idsteps).
2. Se a ação exigir que você forneça entradas, defina-as no seu fluxo de trabalho. Para obter informações sobre as entradas que uma ação pode exigir, confira [Usando blocos de construção pré-gravados no seu fluxo de trabalho](find-and-customize-actions.md#using-inputs-and-outputs-with-an-action).

Você também pode habilitar Dependabot version updates para as ações que adiciona ao fluxo de trabalho. Para saber mais, confira [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

### Adicionando uma ação do mesmo repositório

Se uma ação for definida no mesmo repositório em que o arquivo de fluxo de trabalho usa a ação, você poderá referenciar a ação com a `$/path/to/dir` referência de auto repositório ou com a `{owner}/{repo}@{ref}` sintaxe ou `./path/to/dir` no arquivo de fluxo de trabalho. A `$/` sintaxe não está disponível em GitHub Enterprise Server.

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

Recomendamos referenciar a ação com a `$/path/to/dir` referência de auto repositório. Isso é resolvido para o mesmo repositório na confirmação em execução, portanto, você não precisa fazer check-out do repositório primeiro. Para obter mais informações sobre como `$/` se compara `{owner}/{repo}@{ref}` a e `./`, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#example-using-an-action-in-the-same-repository-as-the-workflow-at-the-running-commit-recommended).

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

Você também pode referenciar a ação com a sintaxe relativa `./path/to/dir` , mas ela é mais propensa a erros. O caminho é relativo (`./`) ao diretório de trabalho padrão (`github.workspace`, portanto, `$GITHUB_WORKSPACE`requer uma etapa de check-out e, se a ação verificar o repositório para um local diferente do fluxo de trabalho, o caminho relativo deverá ser atualizado.

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

### Adicionando uma ação de um repositório diferente

Se uma ação for definida em um repositório diferente do arquivo de fluxo de trabalho, você poderá referenciar a ação com a sintaxe `{owner}/{repo}@{ref}` no arquivo de fluxo de trabalho.

A ação deve ser armazenada em um repositório.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: actions/setup-node@v7
```

### Referenciando um contêiner no Docker Hub

Se uma ação for definida em uma imagem de contêiner do Docker publicada no Docker Hub, você deverá referenciar a ação com a sintaxe `docker://{image}:{tag}` no arquivo de fluxo de trabalho. Para proteger seu código e dados, é altamente recomendável verificar a integridade da imagem de contêiner do Docker de Docker Hub antes de usá-la em seu fluxo de trabalho.

```yaml
jobs:
  my_first_job:
    steps:
      - name: My first step
        uses: docker://alpine:3.8
```

Para ver alguns exemplos de ações do Docker, confira o [fluxo de trabalho Docker-image.yml](https://github.com/actions/starter-workflows/blob/main/ci/docker-image.yml) e o [Criando uma ação de contêiner do Docker](../../../tutorials/use-containerized-services/create-a-docker-container-action.md).

### Fortalecimento de segurança no uso de ações em seus fluxos de trabalho

GitHub fornece recursos de segurança que você pode usar para aumentar a segurança de seus fluxos de trabalho. Você pode usar os recursos internos do GitHub para garantir que você seja notificado sobre vulnerabilidades nas ações que utiliza ou para automatizar o processo de manter atualizadas as ações em seus fluxos de trabalho. Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

## Usar o gerenciamento de versões para suas ações personalizadas

Os criadores de uma ação da comunidade têm a opção de usar tags, branches ou valores do SHA para gerenciar as versões da ação. Semelhante a qualquer dependência, você deve indicar a versão da ação que gostaria de usar, com base no seu conforto em aceitar automaticamente as atualizações da ação.

Você irá designar a versão da ação no seu arquivo de fluxo de trabalho. Verifique a documentação da ação para obter informações sobre suas abordagens de gerenciamento de release e para saber qual tag, branch ou valor de SHA usar.

> \[!NOTE]
> Recomendamos que você use um valor SHA ao usar ações de terceiros. No entanto, é importante observar que Dependabot só criará Dependabot alerts para GitHub Actions vulneráveis que usam versionamento semântico. Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md#using-third-party-actions) e [Alertas do Dependabot](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependabot-alerts).

### Usar etiquetas

As tags são úteis para permitir que você decida quando alternar entre versões maiores e menores, mas estas são mais efêmeras e podem ser movidas ou excluídas pelo mantenedor. Este exemplo demonstra como direcionar uma ação que foi marcada como `v1.0.1`:

```yaml
steps:
  - uses: actions/javascript-action@v1.0.1
```

### Usar SHAs

Se você precisar de uma versão mais confiável, você deverá usar o valor de SHA associado à versão da ação. Os SHAs são imutáveis e, portanto, mais confiáveis que tags ou branches. No entanto, esta abordagem significa que você não receberá automaticamente atualizações de uma ação, incluindo correções de bugs e atualizações de segurança importantes. Você deve usar o valor SHA completo de um commit e não um valor abreviado.
Ao selecionar um SHA, verifique se ele está no repositório da ação e não em uma bifurcação do repositório. Este exemplo tem como destino o SHA de uma ação:

```yaml
steps:
  - uses: actions/javascript-action@a824008085750b8e136effc585c3cd6082bd575f
```

### Usar branches

Especificar um branch de destino para a ação significa que ele sempre irá executar a versão atualmente nesse branch. Essa abordagem pode criar problemas se uma atualização do branch incluir mudanças significativas. Este exemplo é direcionado a um branch chamado `@main`:

```yaml
steps:
  - uses: actions/javascript-action@main
```

Para saber mais, confira [Como gerenciar ações personalizadas](../../create-and-publish-actions/manage-custom-actions.md#using-release-management-for-actions).

## Usar entradas e saídas com uma ação

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
