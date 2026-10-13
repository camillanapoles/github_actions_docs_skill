---
title: Comece a usar o Actions Runner Controller
description: Neste tutorial, você experimentará as noções básicas de Actions Runner Controller.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-actions-runner-controller/get-started
captured: '2026-10-11'
section: Tutorials / Use actions runner controller
---

# Comece a usar o Actions Runner Controller { #get-started-with-actions-runner-controller }

_Neste tutorial, você experimentará as noções básicas de Actions Runner Controller._

## Pré-requisitos { #prerequisites }

Para usar o ARC, verifique se você tem os itens a seguir.

* Um cluster do Kubernetes
  * Para um ambiente de nuvem gerenciado, você pode usar o AKS. Para obter mais informações, consulte [Serviço de Kubernetes do Azure](https://azure.microsoft.com/en-us/products/kubernetes-service) na documentação do Azure.
  * Para uma configuração local, você pode usar o minikube ou o kind. Para obter mais informações, confira [minikube start](https://minikube.sigs.k8s.io/docs/start/) na documentação do minikube e [kind](https://kind.sigs.k8s.io/) na documentação do kind.

* Helm 3
  * Para obter mais informações, confira [Como instalar o Helm](https://helm.sh/docs/intro/install/) na documentação do Helm.

* Embora não seja necessário implantar o ARC, é recomendável garantir que você tenha uma maneira de coletar e reter logs do controlador, dos ouvintes e dos executores efêmeros antes de implantar o ARC em fluxos de trabalho da produção.

## Como instalar o Actions Runner Controller { #installing-actions-runner-controller }

1. Para instalar o operador e as CRDs (definições de recursos personalizados) no cluster, execute as etapas a seguir.

   1. No gráfico do Helm, atualize o valor `NAMESPACE` para o local em que deseja criar os pods do operador. Esse namespace precisa permitir o acesso ao servidor de API do Kubernetes.
   2. Instale o gráfico do Helm.

   O exemplo a seguir instala a última versão do gráfico. Para instalar uma versão específica, transmita o argumento `--version` com a versão do gráfico que deseja instalar. Você pode encontrar a lista de versões no Registro de Contêiner [GitHub](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set-controller).

            ```bash copy
   NAMESPACE="arc-systems"
   helm install arc \
       --namespace "${NAMESPACE}" \
       --create-namespace \
       oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
            ```

   Para ver mais opções de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) na documentação do ARC.

2. Para permitir que o ARC se autentique em GitHub, escolha um método de autenticação para o conjunto de dimensionamento de executores. Se você estiver registrando corredores no repositório ou no nível da organização, recomendamos autenticar com um GitHub App. Os conjuntos de escala de executores registrados no nível empresarial exigem autenticação personal access token (classic). Para obter mais informações, consulte [Autenticando o ARC na API de GitHub](../../how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md).

## Como configurar um conjunto de dimensionamento de executores { #configuring-a-runner-scale-set }

1. Para configurar o conjunto de dimensionamento de executores, execute o comando a seguir no terminal usando valores da configuração do ARC.

   Ao executar o comando, tenha em mente as instruções a seguir.

   * Atualize o valor `INSTALLATION_NAME` com cuidado. Você usará o nome da instalação como o valor de `runs-on` nos seus fluxos de trabalho. Para obter mais informações, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on).

   * Atualize o valor `NAMESPACE` para o local em que deseja criar os pods do executor.

   * Defina `GITHUB_CONFIG_URL` como a URL do repositório, da organização ou da empresa. Essa é a entidade à qual os corredores pertencerão.

   * Este exemplo usa um personal access token (classic) para manter a configuração inicial curta. Para conjuntos de escalonamento de executores de repositório ou organização, use um GitHub App em ambientes de produção, quando possível.

   * Defina `GITHUB_PAT` como um GitHubpersonal access token (classic) com os escopos `repo` e `admin:org` para executores de repositório e de organização.

   * Este exemplo de comando instala a última versão do gráfico do Helm. Para instalar uma versão específica, transmita o argumento `--version` com a versão do gráfico que deseja instalar. Você pode encontrar a lista de versões no Registro de Contêiner [GitHub](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set).

!!! note

     >
     > * Como uma melhor prática de segurança, crie os pods do executor em um namespace diferente do namespace que contém os pods do operador.
     > *

Como uma melhor prática de segurança, crie segredos do Kubernetes e passe as referências secretas. Passar seus segredos em texto sem formatação por meio da CLI pode representar um risco à segurança. Para obter mais informações, consulte [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).

````
                ```bash copy
    INSTALLATION_NAME="arc-runner-set"
    NAMESPACE="arc-runners"
    GITHUB_CONFIG_URL="https://github.com/<your_enterprise/org/repo>"
    GITHUB_PAT="<PAT>"
    helm install "${INSTALLATION_NAME}" \
        --namespace "${NAMESPACE}" \
        --create-namespace \
        --set githubConfigUrl="${GITHUB_CONFIG_URL}" \
        --set githubConfigSecret.github_token="${GITHUB_PAT}" \
        oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
    ```

    Para ver mais opções de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) na documentação do ARC.
````

1. No terminal, execute o comando a seguir para verificar sua instalação.

            ```bash copy
   helm list -A
            ```

   Você deverá ver um resultado semelhante ao seguinte.

            ```bash
   NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                                       APP VERSION
   arc             arc-systems     1               2023-04-12 11:45:59.152090536 +0000 UTC deployed        gha-runner-scale-set-controller-0.4.0       0.4.0
   arc-runner-set  arc-runners     1               2023-04-12 11:46:13.451041354 +0000 UTC deployed        gha-runner-scale-set-0.4.0                  0.4.0
            ```

2. Para verificar o pod do gerenciador, execute o comando a seguir no terminal.

            ```bash copy
   kubectl get pods -n arc-systems
            ```

   Se tudo tiver sido instalado com sucesso, a status dos pods será exibido como **Em execução**.

            ```bash
   NAME                                                   READY   STATUS    RESTARTS   AGE
   arc-gha-runner-scale-set-controller-594cdc976f-m7cjs   1/1     Running   0          64s
   arc-runner-set-754b578d-listener                       1/1     Running   0          12s
            ```

Se a instalação não tiver sido bem-sucedida, confira [Solução de problemas dos erros do Actions Runner Controller](troubleshoot.md) para obter informações sobre solução de problemas.

## Como usar conjuntos de dimensionamento de executores { #using-runner-scale-sets }

Agora você criará e executará um fluxo de trabalho de teste simples que usa os executores do conjunto de dimensionamento de executores.

1. Em um repositório, crie um fluxo de trabalho semelhante ao exemplo a seguir. O valor `runs-on` deve corresponder ao nome de instalação do Helm usado quando você instalou o conjunto de executores de dimensionamento automático.

   Para obter mais informações sobre como adicionar fluxos de trabalho a um repositório, confira [Guia Rápido do GitHub Actions](../../get-started/quickstart.md#creating-your-first-workflow).

            ```yaml copy
   name: Actions Runner Controller Demo
   on:
     workflow_dispatch:

   jobs:
     Explore-GitHub-Actions:
       # You need to use the INSTALLATION_NAME from the previous step
       runs-on: arc-runner-set
       steps:
       - run: echo "🎉 This job uses runner scale set runners!"
            ```

2. Depois de adicionar o fluxo de trabalho ao repositório, dispare manualmente o fluxo de trabalho. Para obter mais informações, consulte [Executar um fluxo de trabalho manualmente](../../how-tos/manage-workflow-runs/manually-run-a-workflow.md).

3. Para ver os pods do executor que estão sendo criados enquanto o fluxo de trabalho está em execução, execute o comando a seguir no terminal.

            ```bash copy
   kubectl get pods -n arc-runners -w
            ```

   Um resultado bem-sucedido será semelhante ao seguinte.

            ```bash
   NAMESPACE     NAME                                                  READY   STATUS    RESTARTS      AGE
   arc-runners   arc-runner-set-rmrgw-runner-p9p5n                     1/1     Running   0             21s
            ```

## Próximas Etapas { #next-steps }

O Actions Runner Controller pode ajudá-lo a gerenciar os executores do GitHub Actions com eficiência. Pronto para começar? Confira alguns recursos úteis para dar seus próximos passos com o ARC:

* Para obter informações detalhadas sobre autenticação, confira [Autenticando o ARC na API de GitHub](../../how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md).
* Para obter ajuda no uso de executores do ARC nos fluxos de trabalho, confira [Usar executores do Controlador do Executor de Ações em um fluxo de trabalho](../../how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md).
* Para obter informações sobre a implantação, consulte [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md).

## Aviso legal { #legal-notice }

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
