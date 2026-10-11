---
title: Implantando com GitHub Actions
description: GitHub Actions fornece controle detalhado sobre implantações com ambientes, grupos de concorrência e regras de proteção.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments
captured: '2026-10-11'
section: GitHub Actions
---

# Implantando com GitHub Actions

_GitHub Actions fornece controle detalhado sobre implantações com ambientes, grupos de concorrência e regras de proteção._

## Pré-requisitos

Você deve estar familiarizado com a sintaxe para GitHub Actions. Para saber mais, confira [Escrevendo fluxos de trabalho](../../write-workflows.md).

## Acionando a sua implantação

Você pode usar uma série de eventos para acionar seu fluxo de trabalho de implantação. Algumas das opções mais comuns são: `pull_request`, `push` e `workflow_dispatch`.

Por exemplo, um fluxo de trabalho com os seguintes gatilhos é executado sempre que:

* Há um push para o branch `main`.
* Uma solicitação de pull direcionada ao branch `main` é aberta, sincronizada ou reaberta.
* Alguém aciona ela manualmente.

```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
  workflow_dispatch:
```

Para saber mais, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md).

## Usar ambientes

Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](manage-environments.md).

Você pode configurar ambientes com regras de proteção e segredos. Quando um trabalho de fluxo de trabalho faz referência a um ambiente, o trabalho não será iniciado até que todas as regras de proteção do ambiente sejam aprovadas. Um trabalho também não pode acessar segredos definidos em um ambiente até que todas as regras de proteção da implantação tenham êxito. Para saber mais, consulte [Usando regras de proteção de implantação personalizadas](#using-custom-deployment-protection-rules) neste artigo.

## Usando concorrência

A concorrência garante que apenas um único trabalho ou fluxo de trabalho que utilize o mesmo grupo de concorrência seja executado por vez. Você pode usar a simultaneidade para que um ambiente tenha no máximo uma implantação em andamento por vez. Para obter mais informações sobre a simultaneidade, confira [Controlar a simultaneidade de fluxos de trabalho e tarefas](../../write-workflows/choose-when-workflows-run/control-workflow-concurrency.md).

## Usando ambientes sem implantações

Por padrão, quando um trabalho de fluxo de trabalho faz referência a um ambiente, GitHub cria um objeto de implantação para acompanhar a implantação. Você pode optar por não criar a implantação definindo `deployment` como `false` na configuração do ambiente. Os valores válidos são `true` (padrão) e `false`. Você também pode usar uma expressão, por exemplo `deployment: ${{ github.ref_name == 'main' }}`.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    environment:
      name: staging
      deployment: false
    steps:
      - name: run tests
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: echo "Running tests with staging secrets"
```

Quando `deployment` é definido como `false`:

* O trabalho possui acesso completo a segredos e variáveis do ambiente.
* Nenhum GitHub objeto de implantação é criado– o histórico de implantação do ambiente não é atualizado.
* As regras de proteção do temporizador de espera ainda se aplicam, o trabalho aguarda a duração configurada.
* Avaliadores obrigatórios ainda se aplicam, os avaliadores ainda devem aprovar antes que o trabalho seja executado.

Isso é útil quando você deseja usar ambientes para:

* **Organizar segredos** — agrupar segredos relacionados em um nome de ambiente sem criar registros de implantação.
* **Controle de acesso** — restrinja quais ramificações podem usar determinados segredos por meio de políticas de ambientes para ramificações, sem a necessidade de rastreamento de implantações.
* **Trabalhos de CI e teste:** referenciar um ambiente para sua configuração sem adicionar ruído ao histórico de implantação.

### Interação com regras de proteção

A propriedade `deployment` controla quais regras de proteção são aplicáveis:

\| Regra de proteção |
`deployment: true` (padrão) | `deployment: false` |
\|----------------|------------------------------|---------------------|
\| **Nenhum** | Implantação criada, trabalho em execução | Sem implantação, execuções de trabalhos |
\| **Temporizador de espera** | Temporizador de espera imposto | Temporizador de espera ainda imposto |
\| **Revisores necessários** | Os revisores devem aprovar | Os revisores devem aprovar |
\| **Aplicativo de regras de proteção de implantação personalizadas** | Webhook do aplicativo foi enviado, precisa ser aprovado | **Tarefa falhou com erro** |

As regras de proteção de implantação personalizada (GitHub Apps) exigem que um objeto de implantação funcione. Se você definir `deployment: false` em um ambiente que tenha regras de proteção de implantação personalizadas, o trabalho falhará imediatamente com uma anotação ou mensagem de erro explicando que as regras de proteção do ambiente são incompatíveis com `deployment: false`. Ou remova `deployment: false` do fluxo de trabalho ou remova as regras de proteção de implantação personalizadas do ambiente.

Observe que `concurrency` e `environment` não estão conectados. O valor da simultaneidade pode ser qualquer cadeia de caracteres; não precisa ser o nome de um ambiente. Além disso, se outro fluxo de trabalho usar o mesmo ambiente, mas não especificar a equivalência, esse fluxo de trabalho não estará sujeito a nenhuma regra de simultaneidade.

Por exemplo, quando o fluxo de trabalho a seguir for executado, ele será colocado em pausa com o status `pending` se qualquer trabalho ou fluxo de trabalho que usa o grupo de simultaneidade `production` estiver em andamento. Ele também cancelará qualquer trabalho ou fluxo de trabalho que use o grupo de simultaneidade `production` e que tenha o status `pending`. Isso significa que haverá, no máximo, um trabalho ou um fluxo de trabalho em execução e um pendente que usa o grupo de simultaneidade `production`.

```yaml
name: Deployment

concurrency: production

on:
  push:
    branches:
      - main

jobs:
  deployment:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: deploy
        # ...deployment-specific steps
```

Você também pode especificar a concorrência no nível do trabalho. Isso permitirá que outros trabalhos no fluxo de trabalho continuem mesmo que o trabalho simultâneo esteja `pending`.

```yaml
name: Deployment

on:
  push:
    branches:
      - main

jobs:
  deployment:
    runs-on: ubuntu-latest
    environment: production
    concurrency: production
    steps:
      - name: deploy
        # ...deployment-specific steps
```

Você pode também usar `cancel-in-progress` para cancelar qualquer trabalho ou fluxo de trabalho em execução no mesmo grupo de concorrência.

```yaml
name: Deployment

concurrency:
  group: production
  cancel-in-progress: true

on:
  push:
    branches:
      - main

jobs:
  deployment:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: deploy
        # ...deployment-specific steps
```

Para obter diretrizes sobre como escrever etapas específicas à implantação, confira [Como encontrar exemplos de implantação](#finding-deployment-examples).

## Exibir o histórico de implantações

Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Para saber mais sobre como exibir implantações em ambientes, confira [Exibir o histórico de implantações](view-deployment-history.md).

Sua organização pode coletar registros de implantação para todos os seus builds em um único lugar carregando dados no linked artifacts page. Confira [Sobre artefatos vinculados](https://docs.github.com/pt/code-security/concepts/supply-chain-security/linked-artifacts).

## Monitoramento de fluxo de trabalho

Cada execução de fluxo de trabalho gera um gráfico em tempo real que ilustra o progresso da execução. Você pode usar este gráfico para monitorar e depurar implantações. Para saber mais, confira [Usar o gráfico de visualização](../../monitor-workflows/use-the-visualization-graph.md).

Você também pode visualizar os registros de cada execução do fluxo de trabalho e o histórico de execuções do fluxo de trabalho. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../monitor-workflows/view-workflow-run-history.md).

## Usando revisões necessárias nos fluxos de trabalho

Os trabalhos que fazem referência a um ambiente configurado com os revisores necessários irão aguardar a aprovação antes de serem iniciados. Enquanto um trabalho está aguardando aprovação, ele tem um status de "Aguardando". Se um trabalho não for aprovado em até 30 dias, falhará automaticamente.

Para obter mais informações sobre ambientes e aprovações necessárias, confira [Gerenciar ambientes para implantação](manage-environments.md). Para obter informações de como examinar implantações com a API REST, confira [Endpoints da API REST para execuções de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs).

## Usando regras de proteção de implantação personalizadas

> \[!NOTE]
> Regras de proteção de implementação personalizada estão em prévia pública e estão sujeitas a alterações.

Você pode habilitar suas próprias regras de proteção personalizadas para bloquear implantações com serviços de terceiros. Por exemplo, você pode usar serviços como Datadog, Honeycomb e ServiceNow para fornecer aprovações automatizadas para implantações no GitHub.

As regras de proteção de implantação personalizada são impulsionadas por GitHub Apps e executadas com base em webhooks e retornos de chamada. A aprovação ou rejeição de um trabalho de fluxo de trabalho baseia-se no consumo do webhook `deployment_protection_rule`. Para saber mais, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment_protection_rule) e [Aprovação ou rejeição de implantações](create-custom-protection-rules.md#approving-or-rejecting-deployments).

Depois de criar uma regra de proteção de implementação personalizada e instalá-la em seu repositório, a regra de proteção de implementação personalizada estará automaticamente disponível para todos os ambientes no repositório.

As implantações em um ambiente podem ser aprovadas ou rejeitadas com base nas condições definidas em qualquer serviço externo, como um tíquete aprovado em um sistema de gerenciamento de serviços de TI (ITSM), resultado de verificação de vulnerabilidades em dependências ou métricas de integridade estáveis de um recurso de nuvem. A decisão de aprovar ou rejeitar implantações fica a critério do aplicativo integrador de terceiros e das condições de gating que você define neles. Confira a seguir alguns casos de uso para os quais você pode criar uma regra de proteção de implantação.

* ITSM & Operações de Segurança: você pode verificar a prontidão do serviço validando processos de qualidade, segurança e conformidade que verificam a prontidão da implantação.
* Sistemas de observabilidade: você pode consultar sistemas de monitoramento ou observabilidade (Sistemas de gerenciamento de desempenho de ativos e agregadores de registro, sistemas de verificação de integridade de recursos em nuvem, etc.) para verificar a prontidão de segurança e implantação.
* Ferramentas de teste e qualidade de código: você pode verificar testes automatizados em compilações de CI que precisam ser implantados em um ambiente.

Como alternativa, você pode escrever suas próprias regras de proteção para qualquer um dos casos de uso acima ou pode definir qualquer lógica personalizada para aprovar ou rejeitar implantações com segurança desde a pré-produção até os ambientes de produção.

## Rastreando implantações por meio de aplicativos

Se sua conta pessoal ou organização no GitHub estiver integrada ao Microsoft Teams ou ao Slack, você poderá acompanhar implantações que usam ambientes por meio de Microsoft Teams ou Slack. Por exemplo, você pode receber notificações por meio do aplicativo quando uma implantação estiver pendente de aprovação, quando uma implantação for aprovada, ou quando o status de implantação for alterado. Para obter mais informações sobre como integrar Microsoft Teams ou Slack, consulte [Integrações de GitHub em destaque](https://docs.github.com/pt/integrations/concepts/featured-github-integrations#team-communication-tools).

Você também pode criar um aplicativo que usa webhooks de status de implantação e implantação para rastrear implantações.
Quando um trabalho de fluxo de trabalho que referencia um ambiente é executado, ele cria um objeto de implantação com a propriedade `environment` definida como o nome do ambiente. À medida que o fluxo de trabalho progride, ele também cria objetos de status de implantação com a propriedade `environment` definida como o nome do ambiente, a propriedade `environment_url` definida como a URL para o ambiente (se especificado no fluxo de trabalho) e a propriedade `state` definida como o status do trabalho. Para obter mais informações, consulte [Documentação do GitHub Apps](https://docs.github.com/pt/apps) e [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment).

## Escolher um executor

Você pode executar seu fluxo de trabalho de implantação em executores hospedados em GitHub ou em executores auto-hospedados. O tráfego de executores hospedados em GitHub pode vir de uma [ampla gama de endereços de rede](https://docs.github.com/pt/rest/meta/meta#get-github-meta-information). Se você estiver implantando em um ambiente interno e sua empresa restringir o tráfego externo em redes privadas, fluxos de trabalho GitHub Actions em execução em executores hospedados em GitHub podem não conseguir se comunicar com seus serviços ou recursos internos. Para superar isso, você pode hospedar seus próprios executores. Para saber mais, confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md) e [Executores hospedados no GitHub](../../../concepts/runners/github-hosted-runners.md).

## Exibindo um selo de status

Você pode usar um selo de status para exibir o status do seu fluxo de trabalho de implantação. Um selo de status mostra se um fluxo de trabalho está falhando ou passando. Um local comum para adicionar uma notificação de status é no arquivo `README.md` do repositório, mas você pode adicioná-lo a qualquer página da Web desejada. Por padrão, os selos exibem o status do seu branch-padrão. Se não houver execuções de fluxo de trabalho em seu branch padrão, ele exibirá o status da execução mais recente em todos os branches. Você pode exibir o status de uma execução de fluxo de trabalho para um branch ou um evento específico usando os parâmetros de consulta `branch` e `event` na URL.

![Captura de tela de um selo de status de fluxo de trabalho. Da direita para a esquerda, são mostrados: o logotipo do GitHub, o nome do fluxo de trabalho ("GitHub Actions Demo") e o status ("passing").](/assets/images/help/repository/actions-workflow-status-badge.png)

Para saber mais, confira [Adicionar um selo de status de fluxo de trabalho](../../monitor-workflows/add-a-status-badge.md).

## Procurando exemplos de implantação

Este artigo demonstrou recursos do GitHub Actions que você pode adicionar aos workflows de implantação.

GitHuboferece modelos de fluxo de trabalho de implantação para vários serviços populares, como Azure Aplicativo Web. Para saber como começar a usar um modelo de fluxo de trabalho, confira [Usando modelos de fluxo de trabalho](../../write-workflows/use-workflow-templates.md) ou [navegue pela lista completa de modelos de fluxo de trabalho de implantação](https://github.com/actions/starter-workflows/tree/main/deployments). Confira também nossos guias mais detalhados de fluxos de trabalho de implantação específicos, como [Implantando Node.js em Azure App Service](../deploy-to-third-party-platforms/nodejs-to-azure-app-service.md).

Muitos provedores de serviços também oferecem ações no GitHub Marketplace para implantar em seus serviços. Para obter a lista completa, consulte [GitHub Marketplace](https://github.com/marketplace?category=deployment\&type=actions).
