---
title: Guia Rápido do GitHub Actions
description: Experimente os principais recursos em GitHub Actions minutos.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/get-started/quickstart
captured: '2026-10-11'
section: Get started
---

# Guia Rápido do GitHub Actions

_Experimente os principais recursos em GitHub Actions minutos._

## Introdução

GitHub Actions é uma plataforma de integração contínua e entrega contínua (CI/CD) que permite automatizar a sua compilação, testar e pipeline de implantação. Você pode criar fluxos de trabalho que executam testes sempre que você envia uma alteração por push para o repositório ou que implantam solicitações de pull mescladas para produção.

Este guia de início rápido mostra como usar a interface do usuário para adicionar um fluxo de GitHub trabalho que demonstra alguns dos recursos essenciais de GitHub Actions.

Para começar a usar fluxos de trabalho pré-configurados, navegue pela lista de modelos no repositório [actions/starter-workflows](https://github.com/actions/starter-workflows). Para saber mais, confira [Usando modelos de fluxo de trabalho](../how-tos/write-workflows/use-workflow-templates.md).

Para obter uma visão geral dos fluxos de GitHub Actions trabalho, consulte [Fluxos de trabalho](../concepts/workflows-and-actions/workflows.md). Se você quiser saber mais sobre os vários componentes que compõem GitHub Actions, consulte [Noções básicas sobre GitHub Actions](understand-github-actions.md).

## Usando modelos de fluxo de trabalho

O GitHub fornece modelos de fluxo de trabalho pré-configurados que você pode usar no estado em que se encontram ou personalizar para criar seu fluxo de trabalho. O GitHub analisa seu código e mostra os modelos de fluxo de trabalho que podem ser úteis para seu repositório. Por exemplo, se o seu repositório contiver o código Node.js, você verá sugestões para projetos Node.js.

Esses modelos de fluxo de trabalho são projetados para ajudar a entrar em funcionamento rapidamente, oferecendo uma variedade de configurações, como:

* CI: [fluxos de trabalho de integração contínua](https://github.com/actions/starter-workflows/tree/main/ci)
* Implantações: [fluxos de trabalho de implantação](https://github.com/actions/starter-workflows/tree/main/deployments)
* Automação: [fluxos de trabalho de automação](https://github.com/actions/starter-workflows/tree/main/automation)
* Varredura de código: [fluxos de trabalho de varredura de código](https://github.com/actions/starter-workflows/tree/main/code-scanning)
* Páginas: [fluxos de trabalho de páginas](https://github.com/actions/starter-workflows/tree/main/pages)

Use esses fluxos de trabalho como ponto de partida para criar seu fluxo de trabalho personalizado ou usá-los no estado em que se encontram. É possível navegar pela lista completa de modelos de fluxo de trabalho no repositório [actions/starter-workflows](https://github.com/actions/starter-workflows).

## Pré-requisitos

Este guia supõe que:

* Você tem pelo menos um conhecimento básico de como usar GitHub. Se você não fizer isso, achará útil ler alguns dos artigos na documentação sobre repositórios e pull requests primeiro. Para ver exemplos, confira [Guia de início rápido para repositórios](https://docs.github.com/pt/repositories/creating-and-managing-repositories/quickstart-for-repositories), [Branches](https://docs.github.com/pt/pull-requests/reference/branches) e [Solicitações de pull](https://docs.github.com/pt/pull-requests/reference/pull-requests).
* Você tem um repositório no GitHub qual pode adicionar arquivos.
* Você tem acesso a GitHub Actions.

  > [!NOTE] Se a guia **(play) Ações** não for exibida com o nome do repositório ativado GitHub, pode ser porque As ações estão desabilitadas para o repositório. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository).

## Criar o seu primeiro fluxo de trabalho

1. Em seu repositório, GitHubcrie um arquivo de fluxo de trabalho chamado `github-actions-demo.yml` no `.github/workflows` diretório. Para fazer isso:
   * Se o `.github/workflows` diretório já existir, navegue até esse diretório, clique em GitHub**Adicionar arquivo** e, em seguida, clique em **Criar novo arquivo** e nomeie o arquivo`github-actions-demo.yml`.

   * Se o repositório não tiver um `.github/workflows` diretório, vá para a página principal do repositório, clique em GitHub e, em seguida, clique em \*\*\*\***Criar novo arquivo** e nomeie o arquivo`.github/workflows/github-actions-demo.yml`. Isso criará os diretórios `.github` e `workflows` e o arquivo `github-actions-demo.yml` em uma única etapa.
!!! note

   > Para GitHub descobrir todos os GitHub Actions fluxos de trabalho em seu repositório, você deve salvar os arquivos de fluxo de trabalho em um diretório chamado `.github/workflows`.
   >
   > É possível dar ao arquivo de fluxo de trabalho qualquer nome que desejar, mas você deverá usar `.yml` ou `.yaml` como a extensão de nome de arquivo. YAML é uma linguagem de marcação comumente usada para arquivos de configuração.

2. Copie o seguinte conteúdo YAML para o arquivo `github-actions-demo.yml`:

            ```yaml copy
   name: GitHub Actions Demo
   run-name: ${{ github.actor }} is testing out GitHub Actions 🚀
   on: [push]
   jobs:
     Explore-GitHub-Actions:
       runs-on: ubuntu-latest
       steps:
         - run: echo "🎉 The job was automatically triggered by a ${{ github.event_name }} event."
         - run: echo "🐧 This job is now running on a ${{ runner.os }} server hosted by GitHub!"
         - run: echo "🔎 The name of your branch is ${{ github.ref }} and your repository is ${{ github.repository }}."
         - name: Check out repository code
           uses: actions/checkout@v6
         - run: echo "💡 The ${{ github.repository }} repository has been cloned to the runner."
         - run: echo "🖥️ The workflow is now ready to test your code on the runner."
         - name: List files in the repository
           run: |
             ls ${{ github.workspace }}
         - run: echo "🍏 This job's status is ${{ job.status }}."
   ```

   Neste estágio, você não precisa entender os detalhes desse fluxo de trabalho. Por enquanto, só é possível copiar e colar o conteúdo no arquivo. Depois de concluir este guia de início rápido, você pode aprender sobre a sintaxe de arquivos de fluxo de trabalho em [Fluxos de trabalho](../concepts/workflows-and-actions/workflows.md) e para obter uma explicação de GitHub Actions contextos, como `${{ github.actor }}` e `${{ github.event_name }}`, consulte [Referência de contextos](../reference/workflows-and-actions/contexts.md).

3. Clique em **Confirmar alterações**.

4. Na caixa de diálogo "Propor alterações", selecione a opção para confirmar o branch padrão ou a opção para criar um novo branch e iniciar uma solicitação de pull. Em seguida, clique em **Confirmar alterações** ou em **Propor alterações**.

   ![Captura de tela da caixa de diálogo "Propor alterações" com as áreas mencionadas destacadas com um contorno laranja.](/assets/images/help/repository/actions-quickstart-commit-new-file.png)

O commit do arquivo de fluxo de trabalho em um branch no repositório dispara o evento `push` e executa o fluxo de trabalho.

Se você optar por iniciar uma solicitação de pull, poderá continuar e criar a solicitação de pull, mas isso não será necessário para os fins deste início rápido, pois a confirmação ainda foi feita em um branch e acionará o novo fluxo de trabalho.

## Visualizar os resultados do seu fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que você deseja exibir, neste exemplo "Demonstração GitHub Actions".

   ![Captura de tela da página "Ações". O nome do fluxo de trabalho de exemplo, "GitHub Actions Demo", é realçado por um contorno laranja escuro.](/assets/images/help/repository/actions-quickstart-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução que você deseja ver, neste exemplo "USERNAME está testando GitHub Actions".

5. Na barra lateral esquerda da página de execução do fluxo de trabalho, em **Jobs**, clique no trabalho **Explore-GitHub-Actions**.

   ![Captura de tela da página "Execução do fluxo de trabalho". Na barra lateral esquerda, a tarefa "Explore-GitHub-Actions" é realçada com um contorno laranja escuro.](/assets/images/help/repository/actions-quickstart-job.png)

6. O registro mostra como cada uma das etapas foi processada. Expanda qualquer um dos passos para ver seus detalhes.

   ![Captura de tela das etapas executadas pelo fluxo de trabalho.](/assets/images/help/repository/actions-quickstart-logs.png)

   Por exemplo, é possível ver a lista de arquivos no repositório:

   ![Captura de tela da etapa "Listar arquivos no repositório" expandida para mostrar a saída do log. A saída da etapa é realçada com um contorno laranja.](/assets/images/help/repository/actions-quickstart-log-detail.png)

O fluxo de trabalho de exemplo que você acabou de adicionar é disparado sempre que o código é enviado por push para o branch e mostra como GitHub Actions você pode trabalhar com o conteúdo do repositório. Para obter um tutorial detalhado, confira [Noções básicas sobre GitHub Actions](understand-github-actions.md).

## Próximas etapas

GitHub Actions pode ajudá-lo a automatizar quase todos os aspectos dos processos de desenvolvimento de aplicativos. Pronto para começar? Aqui estão alguns recursos úteis para executar suas próximas etapas com GitHub Actions:

* Para criar um GitHub Actions fluxo de trabalho, consulte [Usando modelos de fluxo de trabalho](../how-tos/write-workflows/use-workflow-templates.md).
* Para fluxos de trabalho de CI (integração contínua), confira [Criar e testar seu código](../tutorials/build-and-test-code.md).
* Para compilar e publicar pacotes, confira [Publicando pacotes](../tutorials/publish-packages.md).
* Para implantar projetos, confira [Implantação em plataformas de terceiros](../how-tos/deploy/deploy-to-third-party-platforms.md).
* Para automatizar tarefas e processos em GitHub, consulte [Gerenciando seu trabalho com o GitHub Actions](../tutorials/manage-your-work.md).
* Para ver exemplos que demonstram recursos mais complexos de GitHub Actions, consulte [Escolhendo o que seu fluxo de trabalho faz](../how-tos/write-workflows/choose-what-workflows-do.md). Estes exemplos detalhados explicam como testar seu código em um executor, acessar a GitHub CLI e usar recursos avançados, como simultaneidade e matrizes de teste.
* Para certificar sua proficiência em automatizar fluxos de trabalho e acelerar o desenvolvimento com GitHub Actions, obtenha um certificado GitHub Actions com GitHub Certifications. Para obter mais informações, consulte [Sobre GitHub Certifications](https://docs.github.com/pt/get-started/showcase-your-expertise-with-github-certifications/about-github-certifications).
