---
title: Noções básicas sobre GitHub Actions
description: Aprenda os conceitos fundamentais e a terminologia essencial em GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/get-started/understand-github-actions
captured: '2026-10-11'
section: GitHub Actions
---

# Noções básicas sobre GitHub Actions

_Aprenda os conceitos fundamentais e a terminologia essencial em GitHub Actions._

## Visão geral

GitHub Actions é uma plataforma de integração contínua e entrega contínua (CI/CD) que permite automatizar a sua compilação, testar e pipeline de implantação. Você pode criar fluxos de trabalho que compilam e testam cada solicitação de pull para seu repositório ou implantam solicitações de pull mescladas em produção.

GitHub Actions vai além de apenas DevOps e permite executar fluxos de trabalho quando outros eventos acontecem em seu repositório. Por exemplo, você pode executar um fluxo de trabalho para adicionar automaticamente as etiquetas apropriadas sempre que alguém cria um novo problema no repositório.

GitHub fornece máquinas virtuais Linux, Windows e macOS para executar seus fluxos de trabalho ou você pode hospedar seus próprios executores auto-hospedados em seu próprio data center ou infraestrutura de nuvem.

## Os componentes de GitHub Actions

Você pode configurar um GitHub Actions**fluxo de trabalho** a ser disparado quando um **evento** ocorre em seu repositório, como uma solicitação de pull sendo aberta ou um problema que está sendo criado. Seu fluxo de trabalho contém um ou mais **trabalhos** que podem ser executados em ordem sequencial ou em paralelo. Cada trabalho será executado em um **executor** próprio de máquina virtual ou em um contêiner e tem uma ou mais **etapas** que executam um script definido por você ou uma **ação**, que é uma extensão reutilizável que pode simplificar o fluxo de trabalho.

![Diagrama de um evento que dispara o Executor 1 para executar o Trabalho 1, que dispara o Executor 2 para executar o Trabalho 2. Cada um dos trabalhos é dividido em várias etapas.](/assets/images/help/actions/overview-actions-simple.png)

### Fluxos de trabalho

Um **fluxo de trabalho** é um processo automatizado configurável que executará um ou mais trabalhos. Os fluxos de trabalho são definidos por um arquivo YAML verificado no seu repositório e será executado quando acionado por um evento no repositório, ou eles podem ser acionados manualmente ou de acordo com um cronograma definido.

Os fluxos de trabalho são definidos no diretório `.github/workflows` de um repositório. Um repositório pode ter vários fluxos de trabalho, cada um dos quais pode executar um conjunto diferente de tarefas, como:

* Como criar e testar pull requests
* Como implantar seu aplicativo sempre que uma versão for criada
* Como adicionar um rótulo sempre que um novo problema for aberto

Você pode referenciar um fluxo de trabalho dentro de outro fluxo de trabalho. Para saber mais, confira [Reutilizar fluxos de trabalho](../how-tos/reuse-automations/reuse-workflows.md).

Para saber mais, confira [Escrevendo fluxos de trabalho](../how-tos/write-workflows.md).

### Eventos

Um **evento** é uma atividade específica em um repositório que dispara a execução de um **fluxo de trabalho**. Por exemplo, uma atividade pode se originar de GitHub quando alguém cria uma solicitação de pull, abre um problema ou envia uma confirmação por push para um repositório. Além disso, é possível acionar um fluxo de trabalho para execução de acordo com um [agendamento](../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule) ao [postar em uma API REST](https://docs.github.com/pt/rest/repos/repos#create-a-repository-dispatch-event) ou de forma manual.

Para ver uma lista completa dos eventos que podem ser usados para disparar fluxos de trabalho, confira [Eventos que disparam fluxos de trabalho](../reference/workflows-and-actions/events-that-trigger-workflows.md).

### Trabalhos

Um **trabalho** é um conjunto de **etapas** em um fluxo de trabalho executadas no mesmo **executor**. Cada etapa é um script de shell que será executado ou uma **ação** que será executada. As etapas são executadas em ordem e dependem uma da outra. Uma vez que cada etapa é executada no mesmo executor, você pode compartilhar dados de um passo para outro. Por exemplo, você pode ter uma etapa que compila a sua aplicação seguida de uma etapa que testa ao aplicativo criado.

As etapas são executadas por padrão, mas você também pode executar etapas selecionadas simultaneamente quando o fluxo de trabalho se beneficia da execução paralela, como iniciar um serviço de execução longa enquanto as etapas posteriores continuam. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsbackground).

Você pode configurar as dependências de um trabalho com outros trabalhos; por padrão, os trabalhos não têm dependências e são executados em paralelo. Quando um trabalho depende de outro, ele aguarda a conclusão do trabalho dependente antes de ser executado.

Você também pode usar uma **matriz** para executar o mesmo trabalho várias vezes, cada uma com uma combinação diferente de variáveis, como sistemas operacionais ou versões de linguagem.

Por exemplo, você pode configurar vários trabalhos de build para diferentes arquiteturas sem quaisquer dependências de trabalho e um trabalho de empacotamento que dependa desses builds. Os trabalhos de build são executados em paralelo e, quando concluídos com êxito, o trabalho de empacotamento é executado.

Para saber mais, confira [Escolhendo o que seu fluxo de trabalho faz](../how-tos/write-workflows/choose-what-workflows-do.md).

### Ações

Uma **ação** é um conjunto de trabalhos ou código reutilizável predefinido que executa tarefas específicas em um **fluxo de trabalho**, reduzindo a quantidade de código repetitivo que você escreve em seus arquivos de fluxo de trabalho. As ações podem executar tarefas como:

* Extraindo o seu repositório Git de GitHub
* Configurar a cadeia de ferramentas correta para seu ambiente de build
* Configurar a autenticação para seu provedor de nuvem

Você pode escrever suas próprias ações ou encontrar ações para usar em seus fluxos de trabalho no GitHub Marketplace.

Para obter mais informações sobre ações, consulte [Reutilização de automações](../how-tos/reuse-automations.md).

### Executores

Um **runner** é um servidor que executa seus fluxos de trabalho quando eles são disparados. Cada executor pode executar um único **trabalho** por vez.

GitHub fornece executores do Ubuntu Linux, Microsoft Windows e macOS para a execução de seus **fluxos de trabalho**. Cada execução de fluxo de trabalho é executada em uma máquina virtual nova e recém-provisionada.

GitHub também oferece executor avançados, que estão disponíveis em configurações maiores. Para saber mais, confira [Usando executores maiores](../how-tos/manage-runners/larger-runners.md).

Se você precisar de um sistema operacional diferente ou exigir uma configuração de hardware específica, poderá hospedar seus próprios executores.

Para obter mais informações sobre os executores auto-hospedados, confira [Como gerenciar executores auto-hospedados](../how-tos/manage-runners/self-hosted-runners.md).

## Próximas etapas

GitHub Actions pode ajudá-lo a automatizar quase todos os aspectos dos processos de desenvolvimento de aplicativos. Pronto para começar? Aqui estão alguns recursos úteis para executar suas próximas etapas com GitHub Actions:

* Para criar um GitHub Actions fluxo de trabalho, consulte [Usando modelos de fluxo de trabalho](../how-tos/write-workflows/use-workflow-templates.md).
* Para fluxos de trabalho de CI (integração contínua), confira [Criar e testar seu código](../tutorials/build-and-test-code.md).
* Para compilar e publicar pacotes, confira [Publicando pacotes](../tutorials/publish-packages.md).
* Para implantar projetos, confira [Implantação em plataformas de terceiros](../how-tos/deploy/deploy-to-third-party-platforms.md).
* Para automatizar tarefas e processos em GitHub, consulte [Gerenciando seu trabalho com o GitHub Actions](../tutorials/manage-your-work.md).
* Para ver exemplos que demonstram recursos mais complexos de GitHub Actions, consulte [Escolhendo o que seu fluxo de trabalho faz](../how-tos/write-workflows/choose-what-workflows-do.md). Estes exemplos detalhados explicam como testar seu código em um executor, acessar a GitHub CLI e usar recursos avançados, como simultaneidade e matrizes de teste.
* Para certificar sua proficiência em automatizar fluxos de trabalho e acelerar o desenvolvimento com GitHub Actions, obtenha um certificado GitHub Actions com GitHub Certifications. Para obter mais informações, consulte [Sobre GitHub Certifications](https://docs.github.com/pt/get-started/showcase-your-expertise-with-github-certifications/about-github-certifications).

> \[!NOTE]
> Para automações que exigem julgamento contextual sobre o conteúdo do repositório, você também pode criar agentic workflows em linguagem natural em vez de um fluxo de trabalho tradicional GitHub Actions . Para obter mais informações, consulte [Seu primeiro fluxo de trabalho agente](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/quickstart) e [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).
