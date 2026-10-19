---
title: Controlador de Ações Runner
description: Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus GitHub Actions fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/actions-runner-controller
captured: '2026-10-19'
section: Concepts / Runners
---

# Controlador de Ações Runner

_Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus GitHub Actions fluxos de trabalho._

## Sobre o Actions Runner Controller

Actions Runner Controller (ARC) é um operador de Kubernetes que orquestra e dimensiona executores auto-hospedados para GitHub Actions. Para obter mais informações, confira [Padrão do operador](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) da documentação do Kubernetes.

Com o ARC, você pode criar conjuntos de dimensionamento de executores que são dimensionados automaticamente com base no número de fluxos de trabalho em execução em seu repositório, organização ou empresa. Como os executores controlados podem ser efêmeros e baseados em contêineres, novas instâncias do executor podem expandir ou reduzir rapidamente e de forma limpa. Para obter mais informações sobre o dimensionamento automático, consulte [Referência de executores auto-hospedados](../../reference/runners/self-hosted-runners.md).

O diagrama a seguir ilustra a arquitetura do modo de conjunto de escalonamento automático do runner do ARC.

!!! note
    Para visualizar o diagrama a seguir em um tamanho maior, confira a documentação do [Modo de conjuntos de escalonamento do executor de escala automática](https://github.com/actions/actions-runner-controller/blob/master/docs/gha-runner-scale-set-controller/README.md#how-it-works) no repositório Actions Runner Controller.

![Diagrama mostrando o modo ScaleSet do Executor de Dimensionamento Automático do ARC.](https://docs.github.com/assets/images/help/actions/arc-diagram.png)

<!-- The numbers in the ordered list below correspond to numbers in the above diagram, which is why we use explicit numbering here. -->

1. Actions Runner Controller é instalado usando os gráficos do Helm fornecidos e o pod do gerenciador de controladores é implantado no namespace especificado. Um novo recurso AutoScalingRunnerSet é implantado por meio dos gráficos do Helm fornecidos ou de um arquivo de manifesto personalizado. O controlador do AutoScalingRunnerSet chama a API de GitHub para obter o ID do grupo de runners ao qual o conjunto de escalonamento de runners pertencerá.
2. O controlador AutoScalingRunnerSet faz mais uma chamada à API para buscar ou criar um runner scale set no serviço GitHub Actions antes de criar o recurso Listener do Runner ScaleSet.
3. Um pod Ouvinte ScaleSet do Executor é implantado pelo controlador AutoScalingListener. Neste pod, o aplicativo ouvinte se conecta ao GitHub Actions Serviço para autenticar e estabelecer uma conexão de pesquisa longa HTTPS. O ouvinte permanece ocioso até receber uma `Job Available` mensagem do GitHub Actions Serviço.
4. Quando uma execução de fluxo de trabalho é acionada de um repositório, o serviço GitHub Actions encaminha execuções individuais de trabalho para os executores ou conjuntos de dimensionamento de executores em que a chave `runs-on` corresponde ao nome de um conjunto de dimensionamento de executores ou aos rótulos de um conjunto de dimensionamento de executores ou de executores auto-hospedados.
5. Quando o ScaleSet Listener do Runner recebe a mensagem `Job Available`, verifica se pode escalar para cima até a contagem desejada. Se for possível, o Ouvinte ScaleSet do Executor reconhecerá a mensagem.
6. O Ouvinte ScaleSet do Executor usa uma Conta de Serviço e uma Função associada a essa conta para fazer uma chamada HTTPS por meio das APIs do Kubernetes para aplicar patch ao recurso RunnerSet Efêmero com o número de réplicas desejadas.
7. O RunnerSet Efêmero tenta criar executores e o Controlador EphemeralRunner solicita um token de configuração JIT (Just-In-Time) para registrar esses executores. O controlador tenta criar pods do executor. Se o status do pod for `failed`, o controlador tentará novamente até 5 vezes. Após 24 horas, o GitHub Actions Serviço cancelará a atribuição do trabalho se nenhum executor o aceitar.
8. Depois que o pod do executor é criado, o aplicativo do executor no pod usa o token de configuração JIT para se registrar no Serviço GitHub Actions. Em seguida, ele estabelece outra conexão de sondagem longa HTTPS para receber os detalhes do trabalho que precisa executar.
9. O Serviço GitHub Actions confirma o registro do executor e envia os detalhes da execução da tarefa.
10. Ao longo da execução do trabalho, o runner comunica continuamente os logs e o status da execução do trabalho para o GitHub Actions Serviço.
11. Quando o runner conclui seu trabalho com êxito, o Controlador de EphemeralRunner verifica com o serviço GitHub Actions se o runner pode ser excluído. Se puder, o RunnerSet Efêmero excluirá o executor.

## Componentes Actions Runner Controller

O ARC consiste em um conjunto de recursos, alguns dos quais criados especificamente para ele. A implantação do ARC aplica esses recursos a um cluster de Kubernetes. Uma vez aplicado, ele cria um conjunto de Pods que contêm os contêineres dos executores auto-hospedados. Com o ARC, GitHub pode tratar esses contêineres de executores como executores auto-hospedados e atribuir jobs a eles conforme necessário.

Cada recurso implantado pelo ARC recebe um nome formado por estes elementos:

* Um nome da instalação, que é o nome que você especifica ao instalar o Helm chart.
* Um sufixo de identificação do recurso, que é uma cadeia de caracteres que identifica o tipo de recurso. Este valor não é configurável.

!!! note
    Cada versão do Kubernetes têm limites de comprimento diferentes para os nomes dos recursos. O limite do comprimento do nome do recurso é calculado adicionando o comprimento do nome da instalação ao comprimento do sufixo de identificação do recurso. Se o nome do recurso for maior que o comprimento reservado, você receberá uma mensagem de erro.

### Recursos implementados por `gha-runner-scale-set-controller`

| Modelo | Tipo de recurso | Nome | Comprimento reservado | Descrição | Observações |
| --- | --- | --- | --- | --- | --- |
| `deployment.yaml` | Implantação | INSTALLATION_NAME-gha-rs-controller | 18 | O recurso que executa o gerenciador de controladores | Os pods criados por esse recurso têm os sufixos ReplicaSet e Pod. |
| `serviceaccount.yaml` | ServiceAccount | INSTALLATION_NAME-gha-rs-controller | 18 | Esse recurso será criado se `serviceAccount.create` em `values.yaml` estiver definido como verdadeiro. | O nome pode ser personalizado em `values.yaml` |
| `manager_cluster_role.yaml` | ClusterRole | INSTALLATION_NAME-gha-rs-controller | 18 | ClusterRole para o Controller Manager | Esse recurso será criado se o valor de `flags.watchSingleNamespace` estiver vazio. |
| `manager_cluster_role_binding.yaml` | ClusterRoleBinding | INSTALLATION_NAME-gha-rs-controller | 18 | ClusterRoleBinding do gerenciador do controlador | Esse recurso será criado se o valor de `flags.watchSingleNamespace` estiver vazio. |
| `manager_single_namespace_controller_role.yaml` | Função | INSTALLATION_NAME-gha-rs-controller-single-namespace | 35 | Função do gerenciador do controlador | Esse recurso será criado se for definido um valor para `flags.watchSingleNamespace`. |
| `manager_single_namespace_controller_role_binding.yaml` | RoleBinding | INSTALLATION_NAME-gha-rs-controller-single-namespace | 35 | RoleBinding do gerenciador do controlador | Esse recurso será criado se for definido um valor para `flags.watchSingleNamespace`. |
| `manager_single_namespace_watch_role.yaml` | Função | INSTALLATION_NAME-gha-rs-controller-single-namespace-watch | 41 | Função do gerenciador de controladores no namespace configurado | Esse recurso será criado se for definido um valor para `flags.watchSingleNamespace`. |
| `manager_single_namespace_watch_role_binding.yaml` | RoleBinding | INSTALLATION_NAME-gha-rs-controller-single-namespace-watch | 41 | RoleBinding do gerenciador do controlador no namespace configurado | Esse recurso será criado se for definido um valor para `flags.watchSingleNamespace`. |
| `manager_listener_role.yaml` | Função | INSTALLATION_NAME-gha-rs-controller-listener | 26 | Função do ouvinte | Esse recurso é sempre criado. |
| `manager_listener_role_binding.yaml ` | RoleBinding | INSTALLATION_NAME-gha-rs-controller-listener | 26 | RoleBinding para o ouvinte | Esse recurso é sempre criado e associa a função de ouvinte à conta de serviço, que é criada por `serviceaccount.yaml` ou configurada com `values.yaml`. |

### Recursos implementados por `gha-runner-scale-set`

| Modelo | Tipo de recurso | Nome | Comprimento reservado | Descrição | Observações |
| --- | --- | --- | --- | --- | --- |
| `autoscalingrunnerset.yaml` | AutoscalingRunnerSet | INSTALLATION_NAME | 0 | Recurso de nível superior ao se trabalhar com conjuntos de dimensionamento | O comprimento do nome está limitado a 45 caracteres. |
| `no_permission_service_account.yaml` | ServiceAccount | INSTALLATION_NAME-gha-rs-sem-permissão | 21 | Conta de serviço criada no contêiner do executor | Esse recurso será criado se o modo do contêiner não for "kubernetes" e `template.spec.serviceAccountName` não for especificado. |
| `githubsecret.yaml` | Segredo | INSTALLATION_NAME-gha-rs-github-secret | 20 | Segredo que contém valores necessários para autenticar na GitHub API | Esse recurso será criado se `githubConfigSecret` for um objeto. Se for fornecida uma cadeia de caracteres, o segredo não será criado. |
| `manager_role.yaml` | Função | INSTALLATION_NAME-gha-rs-manager | 15 | Função fornecida ao gerenciador para permitir a reconciliação de recursos no namespace do conjunto de executores de dimensionamento automático | Esse recurso é sempre criado. |
| `manager_role_binding.yaml` | RoleBinding | INSTALLATION_NAME-gha-rs-manager | 15 | Associa manager_role à conta de serviço do gerenciador. | Esse recurso é sempre criado. |
| `kube_mode_role.yaml` | Função | INSTALLATION_NAME-gha-rs-kube-modo | 17 | Função que fornece as permissões necessárias para o gancho | Esse recurso é criado quando o modo do contêiner é definido como "kubernetes" e `template.spec.serviceAccount` não é fornecido. |
| `kube_mode_serviceaccount.yaml` | ServiceAccount | INSTALLATION_NAME-gha-rs-kube-modo | 17 | Conta de serviço associada ao pod do executor. | Esse recurso é criado quando o modo do contêiner é definido como "kubernetes" e `template.spec.serviceAccount` não é fornecido. |

### Sobre recursos personalizados

O ARC consiste em várias CRDs (definições de recursos personalizados). Para obter mais informações sobre recursos personalizados, confira [Recursos personalizados](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) na documentação do Kubernetes. Você pode encontrar a lista de definições de recursos personalizados usadas para ARC nas definições de esquema de API a seguir.

* [actions.github.com/v1alpha1](https://pkg.go.dev/github.com/actions/actions-runner-controller/apis/actions.github.com/v1alpha1)
* [actions.summerwind.net/v1alpha1](https://pkg.go.dev/github.com/actions/actions-runner-controller/apis/actions.summerwind.net/v1alpha1)

Como os recursos personalizados são extensões da API do Kubernetes, eles não estarão disponíveis em uma instalação do Kubernetes padrão. Você precisará instalar esses recursos personalizados para usar o ARC. Para obter mais informações sobre como instalar recursos personalizados, confira [Comece a usar o Actions Runner Controller](../../tutorials/use-actions-runner-controller/get-started.md).

Depois que os recursos personalizados forem instalados, você poderá implantar o ARC no cluster do Kubernetes. Para saber mais sobre como implantar o ARC, confira [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).

### Sobre a imagem de contêiner do executor

GitHub mantém uma [imagem mínima de contêiner do runner](https://github.com/actions/runner/pkgs/container/actions-runner). Uma nova imagem será publicada com cada versão de binários do executor. A imagem mais recente terá a versão de binários do executor e `latest` como tags.

Essa imagem contém a menor quantidade de pacotes necessários para o tempo de execução do contêiner e os binários do executor. Para instalar software adicional, você pode criar sua própria imagem de runner. Você pode usar a imagem do executor do ARC como base ou usar as ações de configuração correspondentes. Por exemplo, `actions/setup-java` para Java ou `actions/setup-node` para Node.js.

Você pode encontrar a definição da imagem de executor do [ARC neste Dockerfile](https://github.com/actions/runner/blob/main/images/Dockerfile). Para exibir a imagem base atual, confira a linha `FROM` no Dockerfile da imagem do runner e pesquise essa tag no repositório [`dotnet/dotnet-docker`](https://github.com/dotnet/dotnet-docker/tree/main/src/runtime-deps).

Por exemplo, se a linha `FROM` no Dockerfile da imagem do executor for `mcr.microsoft.com/dotnet/runtime-deps:8.0-jammy AS build`, você poderá encontrar a imagem base em [`https://github.com/dotnet/dotnet-docker/blob/main/src/runtime-deps/8.0/jammy/amd64/Dockerfile`](https://github.com/dotnet/dotnet-docker/blob/main/src/runtime-deps/8.0/jammy/amd64/Dockerfile).

#### Criando sua própria imagem de runner

Você pode criar sua própria imagem do runner que atenda às suas necessidades. A imagem do executor deve atender às condições a seguir.

* Use uma imagem base que possa executar o aplicativo executor auto-hospedado. Confira [Como gerenciar executores auto-hospedados](../../how-tos/manage-runners/self-hosted-runners.md).

* O [binário do executor](https://github.com/actions/runner/releases) deve ser colocado em `/home/runner/` e iniciado usando `/home/runner/run.sh`.

* Se você usar o modo Kubernetes, os [ganchos de contêiner do executor](https://github.com/actions/runner-container-hooks/releases) deverão ser colocados em `/home/runner/k8s`.

Você pode usar o seguinte Dockerfile de exemplo para começar a criar sua própria imagem de runner.

```dockerfile copy
FROM mcr.microsoft.com/dotnet/runtime-deps:6.0 as build

```
# Replace value with the latest runner release version
# source: https://github.com/actions/runner/releases
# ex: 2.303.0
ARG RUNNER_VERSION=""
ARG RUNNER_ARCH="x64"
# Replace value with the latest runner-container-hooks release version
# source: https://github.com/actions/runner-container-hooks/releases
# ex: 0.3.1
ARG RUNNER_CONTAINER_HOOKS_VERSION=""

ENV DEBIAN_FRONTEND=noninteractive
ENV RUNNER_MANUALLY_TRAP_SIG=1
ENV ACTIONS_RUNNER_PRINT_LOG_TO_STDOUT=1

RUN apt update -y && apt install curl unzip -y

RUN adduser --disabled-password --gecos "" --uid 1001 runner \
    && groupadd docker --gid 123 \
    && usermod -aG sudo runner \
    && usermod -aG docker runner \
    && echo "%sudo ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers \
    && echo "Defaults env_keep += \"DEBIAN_FRONTEND\"" >> /etc/sudoers

WORKDIR /home/runner

RUN curl -f -L -o runner.tar.gz https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-${RUNNER_ARCH}-${RUNNER_VERSION}.tar.gz \
    && tar xzf ./runner.tar.gz \
    && rm runner.tar.gz

RUN curl -f -L -o runner-container-hooks.zip https://github.com/actions/runner-container-hooks/releases/download/v${RUNNER_CONTAINER_HOOKS_VERSION}/actions-runner-hooks-k8s-${RUNNER_CONTAINER_HOOKS_VERSION}.zip \
    && unzip ./runner-container-hooks.zip -d ./k8s \
    && rm runner-container-hooks.zip

USER runner
```

```
## Software instalado na imagem do ARC runner

A [imagem do executor](https://github.com/actions/runner/pkgs/container/actions-runner) ARC é agrupada com o seguinte software:

* [Binários do executor](https://github.com/actions/runner)
* [Ganchos de contêiner do executor](https://github.com/actions/runner-container-hooks)
* Docker (necessário para o modo Docker-in-Docker)

Para obter mais informações, confira [Dockerfile da imagem do executor do ARC](https://github.com/actions/runner/blob/main/images/Dockerfile) no repositório Ações.

## Ativos e lançamentos

O ARC é lançado como dois gráficos do Helm e uma imagem de contêiner. Os gráficos do Helm são publicados apenas como pacotes do Open Container Initiative (OCI). O ARC não fornece tarballs ou repositórios do Helm por meio de GitHub Pages.

Você pode encontrar as versões mais recentes dos gráficos helm da ARC e da imagem de contêiner em GitHub Packages:

* [Helm chart `gha-runner-scale-set-controller`](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set-controller).
* [Helm chart `gha-runner-scale-set`](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set).
* [Imagem do contêiner `gha-runner-scale-set-controller`](https://github.com/actions/actions-runner-controller/pkgs/container/gha-runner-scale-set-controller)

A imagem de runner com suporte é disponibilizada como uma imagem de contêiner separada, que você pode encontrar em [`actions-runner`](https://github.com/actions/runner/pkgs/container/actions-runner) no GitHub Packages.

## Aviso legal

Partes foram adaptadas do <https://github.com/actions/actions-runner-controller/> de acordo com a licença Apache-2.0:

```text
Copyright 2019 Moto Ishizawa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Próximas etapas

Se você for novo no ARC, consulte [Comece a usar o Actions Runner Controller](../../tutorials/use-actions-runner-controller/get-started.md) para experimentar as noções básicas.

Quando estiver pronto para usar o ARC para executar fluxos de trabalho, consulte [Usar executores do Controlador do Executor de Ações em um fluxo de trabalho](../../how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md).

Você pode usar o nome de instalação do conjunto de escalas do runner ou definir o valor do campo `runnerScaleSetName` no seu arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) como seu `runs-on` de destino. Você também pode atribuir vários rótulos a um conjunto de escalas para habilitar um roteamento de tarefas mais flexível. Para configurar rótulos para um conjunto de escalas de executor, defina o valor `runnerScaleSetLabels` no seu arquivo `values.yaml`. Consulte [Usar os executores auto-hospedados em um fluxo de trabalho](../../how-tos/manage-runners/self-hosted-runners/use-in-a-workflow.md).

Você pode dimensionar executores estaticamente ou dinamicamente, dependendo de suas necessidades. Confira [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).
