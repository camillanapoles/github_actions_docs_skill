---
title: Usar executores do Controlador do Executor de Ações em um fluxo de trabalho
description: Usar executores Actions Runner Controller em um arquivo de fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow
captured: '2026-10-11'
section: How tos / Manage runners / Use actions runner controller
---

# Usar executores do Controlador do Executor de Ações em um fluxo de trabalho { #using-actions-runner-controller-runners-in-a-workflow }

_Usar executores Actions Runner Controller em um arquivo de fluxo de trabalho._

## Usar executores do ARC em um arquivo de fluxo de trabalho { #using-arc-runners-in-a-workflow-file }

Para atribuir trabalhos a serem executados em um conjunto de dimensionamento de executores, você poderá especificar o nome do conjunto de dimensionamento como o valor da chave `runs-on` no arquivo de fluxo de trabalho do GitHub Actions.

Por exemplo, a configuração a seguir para um conjunto de escalonamento de executores tem o valor `INSTALLATION_NAME` definido como `arc-runner-set`.

```bash
# Using a Personal Access Token (PAT)
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

Para usar essa configuração em um fluxo de trabalho, defina o valor da chave `runs-on` em seu fluxo de trabalho como `arc-runner-set`, semelhante ao exemplo a seguir.

```yaml
jobs:
  job_name:
    runs-on: arc-runner-set
```

## Usar nomes do conjunto de dimensionamento de executores { #using-runner-scale-set-names }

Os nomes do conjunto de dimensionamento do executor são exclusivos dentro do grupo de executores ao qual pertencem. Para implantar vários conjuntos de dimensionamento de executores com o mesmo nome, eles deverão pertencer a diferentes grupos de executores. Para obter mais informações sobre como especificar nomes do conjunto de dimensionamento de executores, confira [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](deploy-runner-scale-sets.md).

Você pode usar o nome de instalação do conjunto de escalas do runner ou definir o valor do campo `runnerScaleSetName` no seu arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) como seu `runs-on` de destino. Você também pode atribuir vários rótulos a um conjunto de escalas para habilitar um roteamento de tarefas mais flexível. Para configurar rótulos para um conjunto de escalas de executor, defina o valor `runnerScaleSetLabels` no seu arquivo `values.yaml`. Para obter mais informações, consulte [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](deploy-runner-scale-sets.md).

## Usando rótulos para definir conjuntos de dimensionamento do executor de destino { #using-labels-to-target-runner-scale-sets }

Você também pode atribuir vários rótulos a um conjunto de dimensionamento de executores e usá-los para direcionar corredores em seu fluxo de trabalho. Para configurar rótulos para um conjunto de instâncias de execução, defina os valores `runnerScaleSetLabels` em seu arquivo `values.yaml`.

```yaml
runnerScaleSetLabels:
  - linux
  - gpu
  - private-network
```

Para direcionar um conjunto de dimensionamento de executores com rótulos específicos, especifique os rótulos como uma matriz na chave `runs-on` do fluxo de trabalho.

```yaml
jobs:
  job_name:
    runs-on: [linux, gpu, private-network]
```

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
