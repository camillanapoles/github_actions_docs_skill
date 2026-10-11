---
title: Solução de problemas dos erros do Actions Runner Controller
description: Saiba como solucionar Actions Runner Controller erros.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/use-actions-runner-controller/troubleshoot
captured: '2026-10-11'
section: Tutorials / Use actions runner controller
---

# Solução de problemas dos erros do Actions Runner Controller

_Saiba como solucionar Actions Runner Controller erros._

## Registro

Os Actions Runner Controller recursos (ARC), que incluem o controlador, o ouvinte e os executores, gravam logs na saída padrão (`stdout`). Recomendamos que você implemente uma solução de logging para coletar e armazenar esses logs. Ter logs disponíveis pode ajudar você ou o suporte do GitHub com solução de problemas e depuração. Para obter mais informações, confira [Arquitetura de Registro em Log](https://kubernetes.io/docs/concepts/cluster-administration/logging/) na documentação do Kubernetes.

## Rótulos de recursos

Os rótulos são adicionados aos recursos criados por Actions Runner Controller, que incluem os pods controlador, ouvinte e executor. Você pode usar esses rótulos para filtrar recursos e ajudar na solução de problemas.

### Pod do controlador

Os seguintes rótulos são aplicados ao pod do controlador.

```yaml
app.kubernetes.io/component=controller-manager
app.kubernetes.io/instance=<controller installation name>
app.kubernetes.io/name=gha-runner-scale-set-controller
app.kubernetes.io/part-of=gha-runner-scale-set-controller
app.kubernetes.io/version=<chart version>
```

### Pod do ouvinte

Os rótulos a seguir são aplicados aos pods do ouvinte.

```yaml
actions.github.com/enterprise= # Will be populated if githubConfigUrl is an enterprise URL
actions.github.com/organization= # Will be populated if githubConfigUrl is an organization URL
actions.github.com/repository= # Will be populated if githubConfigUrl is a repository URL
actions.github.com/scale-set-name= # Runners scale set name
actions.github.com/scale-set-namespace= # Runners namespace
app.kubernetes.io/component=runner-scale-set-listener
app.kubernetes.io/part-of=gha-runner-scale-set
app.kubernetes.io/version= # Chart version
```

### Pod do executor

Os rótulos a seguir são aplicados aos runner pods.

```yaml
actions-ephemeral-runner= # True | False
actions.github.com/organization= # Will be populated if githubConfigUrl is an organization URL
actions.github.com/scale-set-name= # Runners scale set name
actions.github.com/scale-set-namespace= # Runners namespace
app.kubernetes.io/component=runner
app.kubernetes.io/part-of=gha-runner-scale-set
app.kubernetes.io/version= # Chart version
```

## Verificar os logs do ouvinte do conjunto de executores e controlador

Para verificar os logs do pod do controlador, você poderá usar o comando a seguir.

```bash copy
kubectl logs -n <CONTROLLER_NAMESPACE> -l app.kubernetes.io/name=gha-runner-scale-set-controller
```

Para verificar os logs do ouvinte do conjunto de executores, você poderá usar o comando a seguir.

```bash copy
kubectl logs -n <CONTROLLER_NAMESPACE> -l auto-scaling-runner-set-namespace=arc-systems -l auto-scaling-runner-set-name=arc-runner-set
```

## Usando os gráficos do branch `master`

Recomendamos que você use os gráficos da versão mais recente em vez do branch `master`. O branch `master` é altamente instável e não podemos garantir que os gráficos no branch `master` funcionarão em um determinado momento.

## Solução de problemas do pod do ouvinte

Se o pod do controlador estiver em execução, mas o pod do ouvinte não estiver, inspecione os logs do controlador primeiro e confira se há erros. Se não houver erros e o pod do ouvinte do conjunto de executores ainda não estiver em execução, verifique se o pod do controlador tem acesso ao servidor da API do Kubernetes em seu cluster.

Se você tiver um proxy configurado ou estiver usando um proxy sidecar injetado automaticamente, como o [Istio](https://istio.io/), verifique se ele está configurado para permitir o tráfego do contêiner de controle (gerenciador) para o servidor de API do Kubernetes.

Se você instalou o conjunto de executores de dimensionamento automático, mas o pod do ouvinte não foi criado, verifique se o `githubConfigSecret` fornecido está correto e se o `githubConfigUrl` fornecido é preciso. Confira [Autenticando o ARC na API de GitHub](../../how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md) e [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](../../how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md) para saber mais.

## Os pods do executor são recriados após uma execução de fluxo de trabalho cancelada

Depois que uma execução de fluxo de trabalho é cancelada, os eventos a seguir acontecem.

* O sinal de cancelamento é enviado diretamente aos executores.
* O aplicativo do executor é encerrado, o que também encerra os pods do executor.
* No próximo poll, o sinal de cancelamento é recebido pelo ouvinte.

Poderá haver um pequeno atraso entre quando os executores recebem o sinal e quando o ouvinte recebe o sinal. Quando os pods do executor começam a terminar, o ouvinte tenta trazer novos executores para corresponder ao número desejado de executores de acordo com o estado em que está. No entanto, quando o ouvinte receber o sinal de cancelamento, ele atuará para reduzir o número de executores. Eventualmente, o ouvinte reduzirá verticalmente para o número desejado de executores. Enquanto isso, você pode conferir executores adicionais.

## Erro: `Name must have up to n characters`

O ARC usa os nomes gerados de determinados recursos como rótulos para outros recursos. Devido a esse requisito, o ARC limita os nomes de recursos para 63 caracteres.

Como parte do nome do recurso é definida por você, o ARC impõe um limite no número de caracteres que você pode usar para o nome da instalação e o namespace.

```bash
Error: INSTALLATION FAILED: execution error at (gha-runner-scale-set/templates/autoscalingrunnerset.yaml:5:5): Name must have up to 45 characters

Error: INSTALLATION FAILED: execution error at (gha-runner-scale-set/templates/autoscalingrunnerset.yaml:8:5): Namespace must have up to 63 characters
```

## Erro: `Access to the path /home/runner/_work/_tool is denied`

Você poderá ver esse erro se estiver usando o modo Kubernetes com volumes persistentes. Este erro ocorre se o contêiner runner estiver em execução com um usuário não raiz e estiver causando uma incompatibilidade de permissões com o volume montado.

Para corrigir isso, utilize uma das opções a seguir.

* Use um tipo de volume que dê suporte a `securityContext.fsGroup`. Os volumes `hostPath` não dão suporte a essa propriedade, enquanto os volumes `local` e outros tipos de volumes a dão suporte. Atualize o `fsGroup` do pod do executor para corresponder ao GID do executor. Você pode fazer isso atualizando os valores do gráfico helm `gha-runner-scale-set` para incluir as informações abaixo. Substitua `VERSION` pela versão da imagem de contêiner `actions-runner` que você deseja usar.

        ```yaml copy
  template:
    spec:
      securityContext:
        fsGroup: 123
      containers:
        - name: runner
          image: ghcr.io/actions/actions-runner:latest
          command: ["/home/runner/run.sh"]
  ```

* Se atualizar o `securityContext` do pod do executor não for uma solução viável, você poderá resolver o problema usando `initContainers` para alterar a propriedade do volume montado, como indicado abaixo.

        ```yaml copy
  template:
    spec:
      initContainers:
        - name: kube-init
          image: ghcr.io/actions/actions-runner:latest
          command: ["sudo", "chown", "-R", "1001:123", "/home/runner/_work"]
      volumeMounts:
        - name: work
          mountPath: /home/runner/_work
      containers:
        - name: runner
          image: ghcr.io/actions/actions-runner:latest
          command: ["/home/runner/run.sh"]
  ```

## Erro: `failed to get access token for GitHub App auth: 401 Unauthorized`

Um `401 Unauthorized` erro ao tentar obter um token de acesso para um GitHub App pode ser resultado de um descompasso do Protocolo de Tempo de Rede (NTP). Verifique se o sistema Kubernetes está sincronizando com precisão com um servidor do NTP e se não há um descompasso de tempo significativo. Há mais margem de manobra se o tempo do sistema estiver atrasado GitHub, mas se o ambiente estiver mais de alguns segundos à frente, ocorrerão 401 erros ao usar GitHub App.

## Limites do grupo de executores

Você pode ter no máximo 10.000 executores auto-hospedados em um grupo de executores. Se esse limite for atingido, não será possível adicionar um novo executor.

## Atualizações do executor

> [!WARNING] Todas as atualizações lançadas para o software, incluindo versões principais, secundárias ou de patch, são consideradas como uma atualização disponível. Se você não executar uma atualização de software em 30 dias, o serviço do GitHub Actions não colocará trabalhos na fila para o seu executor. Além disso, se uma atualização crítica de segurança for necessária, o serviço de GitHub Actions não colocará os trabalhos na fila do seu executor até que ele seja atualizado.

Valide se a versão do software executor e/ou as imagens de executores personalizados em uso estão rodando a versão mais recente.

Para saber mais, confira [Referência de executores auto-hospedados](../../reference/runners/self-hosted-runners.md).

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
