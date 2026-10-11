---
title: Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller
description: Implante conjuntos de escalonadores com Actions Runner Controller, e use opções avançadas de configuração para adaptar Actions Runner Controller às suas necessidades.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets
captured: '2026-10-11'
section: How tos / Manage runners / Use actions runner controller
---

# Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller

_Implante conjuntos de escalonadores com Actions Runner Controller, e use opções avançadas de configuração para adaptar Actions Runner Controller às suas necessidades._

## Como implantar um conjunto de dimensionamento de executores

Para implantar um conjunto de dimensionamento de executores, você precisa ter o ARC em execução. Para obter mais informações, consulte [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md).

Você pode implantar conjuntos de dimensionamento de executores com os gráficos do Helm do ARC ou implantando os manifestos necessários. O uso de gráficos do Helm do ARC é o método preferencial, especialmente se você não tem experiência anterior no uso do ARC.

!!! note
    * Como uma melhor prática de segurança, crie os pods do executor em um namespace diferente do namespace que contém os pods do operador.
    * Como uma melhor prática de segurança, crie segredos do Kubernetes e passe as referências secretas. Passar seus segredos em texto sem formatação por meio da CLI pode representar um risco à segurança.
    * Recomendamos executar cargas de trabalho de produção isoladamente.
      GitHub Actions os fluxos de trabalho são projetados para executar código arbitrário e o uso de um cluster compartilhado do Kubernetes para cargas de trabalho de produção pode representar um risco à segurança.
    * Certifique-se de que implementou uma maneira de coletar e reter logs do controlador, dos ouvintes e dos executores efêmeros.

1. Para configurar o conjunto de dimensionamento de executores, execute o comando a seguir no terminal usando valores da configuração do ARC.

   Ao executar o comando, tenha em mente as instruções a seguir.

   * Atualize o valor `INSTALLATION_NAME` com cuidado. Você pode usar o nome da instalação como o valor de [`runs-on`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idruns-on), em seus fluxos de trabalho.

   * Atualize o valor `NAMESPACE` para o local em que deseja criar os pods do executor.

   * Defina o valor `GITHUB_CONFIG_URL` como a URL do repositório, da organização ou da empresa. Essa é a entidade à qual os corredores pertencerão.

   * Este exemplo de comando instala a última versão do gráfico do Helm. Para instalar uma versão específica, transmita o argumento `--version` com a versão do gráfico que deseja instalar. Encontre a lista de versões no repositório [`actions-runner-controller`](https://github.com/actions/actions-runner-controller/pkgs/container/actions-runner-controller-charts%2Fgha-runner-scale-set).

!!! note

   > Este exemplo usa um personal access token para manter a configuração inicial curta. Se você estiver registrando corredores no repositório ou no nível da organização, recomendamos autenticar com um GitHub App em vez disso. Para obter mais informações, consulte [Autenticando o ARC na API de GitHub](authenticate-to-the-api.md). Os executores de nível empresarial exigem autenticação personal access token (classic).

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

   Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

2. Para verificar sua instalação, execute o comando a seguir no terminal.

            ```bash copy
   helm list -A
   ```

   Você deverá ver um resultado semelhante ao seguinte.

            ```bash
   NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                                       APP VERSION
   arc             arc-systems     1               2023-04-12 11:45:59.152090536 +0000 UTC deployed        gha-runner-scale-set-controller-0.4.0       0.4.0
   arc-runner-set  arc-systems     1               2023-04-12 11:46:13.451041354 +0000 UTC deployed        gha-runner-scale-set-0.4.0                  0.4.0
   ```

3. Para verificar o pod do gerenciador, execute o comando a seguir no terminal.

            ```bash copy
   kubectl get pods -n arc-systems
   ```

   Se a instalação tiver sido bem-sucedida, os pods mostrarão o status `Running`.

            ```bash
   NAME                                                   READY   STATUS    RESTARTS   AGE
   arc-gha-runner-scale-set-controller-594cdc976f-m7cjs   1/1     Running   0          64s
   arc-runner-set-754b578d-listener                       1/1     Running   0          12s
   ```

Se a instalação não tiver sido bem-sucedida, confira [Solução de problemas dos erros do Actions Runner Controller](../../../tutorials/use-actions-runner-controller/troubleshoot.md) para obter informações sobre solução de problemas.

## Como usar as opções de configuração avançada

O ARC oferece várias opções de configuração avançada.

### Como configurar o nome do conjunto de dimensionamento de executores

!!! note
    Os nomes do conjunto de dimensionamento do executor são exclusivos dentro do grupo de executores ao qual pertencem. Caso deseje implantar vários conjuntos de dimensionamento de executores com o mesmo nome, eles precisam pertencer a diferentes grupos de executores.

Para configurar o nome do conjunto de dimensionamento do executor, você pode definir um `INSTALLATION_NAME` ou definir o valor do `runnerScaleSetName` na sua cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

```yaml
## The name of the runner scale set to create, which defaults to the Helm release name
runnerScaleSetName: "my-runners"
```

Certifique-se de passar o arquivo `values.yaml` no comando `helm install`. Confira a documentação [instalação do Helm](https://helm.sh/docs/helm/helm_install/) para obter mais detalhes.

### Como escolher destinos do executor

Os conjuntos de dimensionamento de executores podem ser implantados nos níveis do repositório, da organização ou da empresa.

Para implantar conjuntos de dimensionamento de executores em um nível específico, defina o valor de `githubConfigUrl` na sua cópia do `values.yaml` como a URL do repositório, da organização ou da empresa.

O exemplo a seguir mostra como configurar o ARC para adicionar executores a `octo-org/octo-repo`.

```yaml
githubConfigUrl: "https://github.com/octo-ent/octo-org/octo-repo"
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Usando um GitHub App para autenticação

Se você não estiver usando executores de nível empresarial, poderá usar GitHub Apps para autenticar com a GitHub API. Para obter mais informações, consulte [Autenticando o ARC na API de GitHub](authenticate-to-the-api.md).

!!! note
    Considerando o risco de segurança associado à exposição da sua chave privada em texto sem formatação em um arquivo em disco, recomendamos criar um segredo do Kubernetes e transmitir a referência.

Você pode criar um segredo do Kubernetes ou especificar valores no arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

#### Opção 1: Criar um segredo do Kubernetes (recomendado)

Depois de criar seu GitHub App, crie um segredo do Kubernetes e passe a referência para esse segredo na cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

!!! note
    Crie o segredo no mesmo namespace onde o gráfico `gha-runner-scale-set` está instalado. Neste exemplo, o namespace é `arc-runners` para corresponder à documentação de início rápido. Para saber mais, confira [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md#configuring-a-runner-scale-set).

```bash
kubectl create secret generic pre-defined-secret \
  --namespace=arc-runners \
  --from-literal=github_app_id=123456 \
  --from-literal=github_app_installation_id=654321 \
  --from-file=github_app_private_key=private-key.pem
```

Na sua cópia do [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml), passe o nome do segredo como referência.

```yaml
githubConfigSecret: pre-defined-secret
```

#### Opção 2: Especificar valores no arquivo `values.yaml`

Como alternativa, você pode especificar os valores de `app_id`, `installation_id` e `private_key` na cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

```yaml
## githubConfigSecret is the Kubernetes secret to use when authenticating with GitHub API.
## You can choose to use a GitHub App or a personal access token (classic)
githubConfigSecret:
  ## GitHub Apps Configuration
  ## IDs must be strings, use quotes
  github_app_id: "123456"
  github_app_installation_id: "654321"
  github_app_private_key: |
    -----BEGIN RSA PRIVATE KEY-----
    ...
    HkVN9...
    ...
    -----END RSA PRIVATE KEY-----
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Gerenciamento de acesso com grupos de runners

Use grupos de executores para controlar quais organizações ou repositórios têm acesso aos conjuntos de dimensionamento de executores. Para obter mais informações sobre os grupos de executores, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](../self-hosted-runners/manage-access.md).

Para adicionar um conjunto de dimensionamento de executores a um grupo de executores, você já precisa ter criado um grupo de executores. Em seguida, defina a propriedade `runnerGroup` na sua cópia do arquivo `values.yaml`. O exemplo a seguir adiciona um conjunto de dimensionamento de executores ao grupo de executores Octo-Group.

```yaml
runnerGroup: "Octo-Group"
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como configurar um proxy de saída

Para forçar o tráfego HTTP para que o controlador e os executores passem pelo proxy de saída, defina as propriedades a seguir no gráfico do Helm.

```yaml
proxy:
  http:
    url: http://proxy.com:1234
    credentialSecretRef: proxy-auth # a Kubernetes secret with `username` and `password` keys
  https:
    url: http://proxy.com:1234
    credentialSecretRef: proxy-auth # a Kubernetes secret with `username` and `password` keys
  noProxy:
    - example.com
    - example.org
```

O ARC dá suporte ao uso de proxies anônimos ou autenticados. Se você usar proxies autenticados, precisará definir o valor `credentialSecretRef` para referenciar um segredo do Kubernetes. Você pode criar um segredo com suas credenciais de proxy com o comando a seguir.

!!! note
    Crie o segredo no mesmo namespace onde o gráfico `gha-runner-scale-set` está instalado. Neste exemplo, o namespace é `arc-runners` para corresponder à documentação de início rápido. Para saber mais, confira [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md#configuring-a-runner-scale-set).

```bash copy
  kubectl create secret generic proxy-auth \
    --namespace=arc-runners \
    --from-literal=username=proxyUsername \
    --from-literal=password=proxyPassword \
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como definir o número máximo e mínimo de executores

As propriedades `maxRunners` e `minRunners` fornecem uma variedade de opções para personalizar a configuração do ARC.

!!! note
    O ARC não dá suporte a configurações máxima e mínima agendadas. Use um cron job ou qualquer outra solução de agendamento para atualizar a configuração em um agendamento.

#### Exemplo: número ilimitado de corredores

Se você comentar as propriedades `maxRunners` e `minRunners`, o ARC aumentará para o número de trabalhos atribuídos ao conjunto de dimensionamento de executores e reduzirá para 0 se não houver trabalhos ativos.

```yaml
## maxRunners is the max number of runners the auto scaling runner set will scale up to.
# maxRunners: 0

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
# minRunners: 0
```

#### Exemplo: número mínimo de executores

Você pode definir a propriedade `minRunners` com qualquer número e o ARC garantirá que sempre haverá o número específico de executores ativos e disponíveis para realizar trabalhos atribuídos ao conjunto de dimensionamento de executores o tempo todo.

```yaml
## maxRunners is the max number of runners the auto scaling runner set will scale up to.
# maxRunners: 0

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
minRunners: 20
```

#### Exemplo: Defina o número máximo e mínimo de corredores

Nessa configuração, o Actions Runner Controller será dimensionado até um máximo de `30` executores e será reduzido para `20` executores quando os trabalhos terminarem.

!!! note
    O valor de `minRunners` nunca pode exceder o de `maxRunners`, a menos que `maxRunners` esteja comentado.

```yaml
## maxRunners is the max number of runners the auto scaling runner set will scale up to.
maxRunners: 30

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
minRunners: 20
```

#### Exemplo: esvaziamento da fila de trabalhos

Em alguns cenários, o ideal é esvaziar a fila de trabalhos para solucionar um problema ou para executar a manutenção do cluster. Se você definir ambas as propriedades para `0`, o Actions Runner Controller não criará novos pods de executor quando novos trabalhos estejam disponíveis e sejam atribuídos.

```yaml
## maxRunners is the max number of runners the auto scaling runner set will scale up to.
maxRunners: 0

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
minRunners: 0
```

### Certificados TLS personalizados

!!! note
    Se você estiver usando uma imagem de executor personalizada que não se baseie na distribuição do `Debian`, as instruções a seguir não funcionarão.

Alguns ambientes exigem certificados TLS assinados por uma AC (autoridade de certificação) personalizada. Como os certificados de autoridade de certificação personalizados não são agrupados com os contêineres do controlador ou do executor, você precisa injetá-los nos respectivos repositórios confiáveis.

```yaml
githubServerTLS:
  certificateFrom:
    configMapKeyRef:
      name: config-map-name
      key: ca.crt
  runnerMountPath: /usr/local/share/ca-certificates/
```

Ao fazer isso, verifique se você está usando o formato PEM (Privacy Enhanced Mail) e se a extensão do certificado é `.crt`. O restante será ignorado.

O controlador executa as ações a seguir.

* Cria um volume `github-server-tls-cert` que contém o certificado especificado em `certificateFrom`.
* Monta esse volume no caminho `runnerMountPath/<certificate name>`.
* Define a variável de ambiente `NODE_EXTRA_CA_CERTS` como esse mesmo caminho.
* Define a variável de ambiente `RUNNER_UPDATE_CA_CERTS` como `1` (a partir da versão `2.303.0`, isso instruirá o executor a recarregar os certificados no host).

O ARC observa os valores definidos no modelo de pod do executor e não os substitui.

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como usar um registro de contêiner privado

!!! warning
    Essa Actions Runner Controller opção de personalização pode estar fora do escopo do que Suporte do GitHub pode ajudar e pode causar um comportamento inesperado quando configurada incorretamente.

    Para obter mais informações sobre o que Suporte do GitHub pode ajudar, consulte [Suporte para o Controlador do Executor de Ações](../../../concepts/runners/support-for-arc.md).

Para usar um registro de contêiner privado, você pode copiar a imagem do controlador e a imagem do executor para o registro de contêiner privado. Em seguida, configure os links para essas imagens e defina os valores `imagePullPolicy` e `imagePullSecrets`.

#### Como configurar a imagem do controlador

Você pode atualizar sua cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) e definir as propriedades `image` conforme mostrado a seguir.

```yaml
image:
  repository: "custom-registry.io/gha-runner-scale-set-controller"
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "0.4.0"

imagePullSecrets:
  - name: <registry-secret-name>
```

O contêiner do ouvinte herda a `imagePullPolicy` definida para o controlador.

#### Configurando a imagem do runner

Você pode atualizar sua cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) e definir as propriedades de `template.spec` para configurar o pod do executor para seu caso de uso específico.

!!! note
    O contêiner do executor deve ser nomeado `runner`. Caso contrário, ele não será configurado corretamente para se conectar a GitHub.

Veja a seguir um exemplo de configuração:

```yaml
template:
  spec:
    containers:
      - name: runner
        image: "custom-registry.io/actions-runner:latest"
        imagePullPolicy: Always
        command: ["/home/runner/run.sh"]
    imagePullSecrets:
      - name: <registry-secret-name>
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como atualizar a especificação de pod para o pod do executor

!!! warning
    Essa Actions Runner Controller opção de personalização pode estar fora do escopo do que Suporte do GitHub pode ajudar e pode causar um comportamento inesperado quando configurada incorretamente.

    Para obter mais informações sobre o que Suporte do GitHub pode ajudar, consulte [Suporte para o Controlador do Executor de Ações](../../../concepts/runners/support-for-arc.md).

Você pode personalizar totalmente a PodSpec do pod do executor e o controlador aplicará a configuração especificada. A seguir, um exemplo de especificação de um pod.

```yaml
template:
  spec:
    containers:
      - name: runner
        image: ghcr.io/actions/actions-runner:latest
        command: ["/home/runner/run.sh"]
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
        securityContext:
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
          capabilities:
            add:
              - NET_ADMIN
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como atualizar a especificação de pod para o pod do ouvinte

!!! warning
    Essa Actions Runner Controller opção de personalização pode estar fora do escopo do que Suporte do GitHub pode ajudar e pode causar um comportamento inesperado quando configurada incorretamente.

    Para obter mais informações sobre o que Suporte do GitHub pode ajudar, consulte [Suporte para o Controlador do Executor de Ações](../../../concepts/runners/support-for-arc.md).

Você pode personalizar o PodSpec do pod do ouvinte e o controlador aplicará a configuração especificada. A seguir, um exemplo de especificação de um pod.

!!! note
    É importante não alterar o valor `listenerTemplate.spec.containers.name` do contêiner listener. Caso contrário, a configuração especificada será aplicada a um novo contêiner sidecar.

```yaml
listenerTemplate:
  spec:
    containers:
    # If you change the name of the container, the configuration will not be applied to the listener,
    # and it will be treated as a sidecar container.
    - name: listener
      securityContext:
        runAsUser: 1000
      resources:
        limits:
          cpu: "1"
          memory: 1Gi
        requests:
          cpu: "1"
          memory: 1Gi
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

## Como usar o modo Docker-in-Docker ou Kubernetes para contêineres

!!! warning
    Essa Actions Runner Controller opção de personalização pode estar fora do escopo do que Suporte do GitHub pode ajudar e pode causar um comportamento inesperado quando configurada incorretamente.

    Para obter mais informações sobre o que Suporte do GitHub pode ajudar, consulte [Suporte para o Controlador do Executor de Ações](../../../concepts/runners/support-for-arc.md).

Se você estiver usando trabalhos de contêiner e serviços ou ações de contêiner, você precisará definir o valor `containerMode` como `dind` ou `kubernetes`. Para usar um modo de contêiner personalizado, comente ou remova `containerMode` e adicione a configuração desejada à seção `template`. Confira [Como personalizar modos de contêiner](deploy-runner-scale-sets.md#customizing-container-modes).

* Para obter mais informações sobre os trabalhos e os serviços de contêiner, confira [Executar trabalhos em um contêiner](../../write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md).
* Para obter mais informações sobre as ações de contêiner, confira [Criando uma ação de contêiner do Docker](../../../tutorials/use-containerized-services/create-a-docker-container-action.md).

### Como usar o modo Docker-in-Docker

!!! note
    O contêiner Docker-in-Docker exige o modo privilegiado. Para obter mais informações, confira [Configurar um contexto de segurança para um pod ou um contêiner](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/) na documentação do Kubernetes.

    Por padrão, o contêiner `dind` usa a imagem `docker:dind`, que executa o daemon do Docker como raiz. Você pode substituir essa imagem por `docker:dind-rootless` desde que esteja ciente das [limitações conhecidas](https://docs.docker.com/engine/security/rootless/#known-limitations) e executar os pods com o modo `--privileged`. Para saber como personalizar a configuração do Docker-in-Docker, consulte [Personalizando modos de contêiner](deploy-runner-scale-sets.md#customizing-container-modes).

O modo Docker-in-Docker é uma configuração que permite executar o Docker dentro de um contêiner do Docker. Nessa configuração, para cada pod de runner criado, o ARC cria os contêineres a seguir.

* Um contêiner `init`
* Um contêiner `runner`
* Um contêiner `dind`

Para habilitar o modo Docker-in-Docker, defina o `containerMode.type` como `dind` conforme mostrado a seguir.

```yaml
containerMode:
  type: "dind"
```

O `template.spec` será atualizado com a configuração padrão a seguir.

Para versões do Kubernetes `>= v1.29`, o contêiner sidecar será usado para executar o daemon do Docker.

```yaml
template:
  spec:
    initContainers:
      - name: init-dind-externals
        image: ghcr.io/actions/actions-runner:latest
        command: ["cp", "-r", "/home/runner/externals/.", "/home/runner/tmpDir/"]
        volumeMounts:
          - name: dind-externals
            mountPath: /home/runner/tmpDir
      - name: dind
        image: docker:dind
        args:
          - dockerd
          - --host=unix:///var/run/docker.sock
          - --group=$(DOCKER_GROUP_GID)
        env:
          - name: DOCKER_GROUP_GID
            value: "123"
        securityContext:
          privileged: true
        restartPolicy: Always
        startupProbe:
          exec:
            command:
              - docker
              - info
          initialDelaySeconds: 0
          failureThreshold: 24
          periodSeconds: 5
        volumeMounts:
          - name: work
            mountPath: /home/runner/_work
          - name: dind-sock
            mountPath: /var/run
          - name: dind-externals
            mountPath: /home/runner/externals
    containers:
      - name: runner
        image: ghcr.io/actions/actions-runner:latest
        command: ["/home/runner/run.sh"]
        env:
          - name: DOCKER_HOST
            value: unix:///var/run/docker.sock
          - name: RUNNER_WAIT_FOR_DOCKER_IN_SECONDS
            value: "120"
        volumeMounts:
          - name: work
            mountPath: /home/runner/_work
          - name: dind-sock
            mountPath: /var/run
    volumes:
      - name: work
        emptyDir: {}
      - name: dind-sock
        emptyDir: {}
      - name: dind-externals
        emptyDir: {}
```

Para versões do Kubernetes `< v1.29`, a seguinte configuração será aplicada:

```yaml
template:
  spec:
    initContainers:
      - name: init-dind-externals
        image: ghcr.io/actions/actions-runner:latest
        command:
          ["cp", "-r", "/home/runner/externals/.", "/home/runner/tmpDir/"]
        volumeMounts:
          - name: dind-externals
            mountPath: /home/runner/tmpDir
    containers:
      - name: runner
        image: ghcr.io/actions/actions-runner:latest
        command: ["/home/runner/run.sh"]
        env:
          - name: DOCKER_HOST
            value: unix:///var/run/docker.sock
        volumeMounts:
          - name: work
            mountPath: /home/runner/_work
          - name: dind-sock
            mountPath: /var/run
      - name: dind
        image: docker:dind
        args:
          - dockerd
          - --host=unix:///var/run/docker.sock
          - --group=$(DOCKER_GROUP_GID)
        env:
          - name: DOCKER_GROUP_GID
            value: "123"
        securityContext:
          privileged: true
        volumeMounts:
          - name: work
            mountPath: /home/runner/_work
          - name: dind-sock
            mountPath: /var/run
          - name: dind-externals
            mountPath: /home/runner/externals
    volumes:
      - name: work
        emptyDir: {}
      - name: dind-sock
        emptyDir: {}
      - name: dind-externals
        emptyDir: {}
```

Os valores em `template.spec` são injetados automaticamente e não podem ser substituídos. Se você quiser personalizar essa configuração, terá que remover a definição de `containerMode.type`, copiar essa configuração e aplicá-la diretamente em sua cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

### Como usar o modo Kubernetes

No modo Kubernetes, o ARC usa ganchos de contêiner do executor para criar um pod no mesmo namespace para executar o serviço, o trabalho de contêiner ou a ação.

#### Pré-requisitos

O modo Kubernetes oferece suporte a duas abordagens para compartilhar dados de trabalhos entre o pod do executor e o pod de trabalho do contêiner. Você pode usar volumes persistentes, que continuam sendo a opção recomendada para cenários que exigem acesso de gravação simultâneo ou pode usar hooks de ciclo de vida de contêiner para restaurar e exportar sistemas de arquivos de trabalhos entre pods sem depender de volumes RWX. A abordagem do gancho de ciclo de vida melhora a portabilidade e o desempenho aproveitando o armazenamento local e é ideal para clusters sem armazenamento compartilhado.

#### Configurando o modo Kubernetes com volumes persistentes

Para usar o modo Kubernetes, você deve criar volumes persistentes que os pods dos executores possam reivindicar e usar uma solução que automaticamente provisione esses volumes sob demanda. Para o teste, você pode usar uma solução como o [OpenEBS](https://github.com/openebs/openebs).

Para habilitar o modo Kubernetes, defina o `containerMode.type` como `kubernetes` no arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml).

```yaml
containerMode:
  type: "kubernetes"
  kubernetesModeWorkVolumeClaim:
    accessModes: ["ReadWriteOnce"]
    storageClassName: "dynamic-blob-storage"
    resources:
      requests:
        storage: 1Gi
```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

#### Configurar o modo Kubernetes com hooks de ciclo de vida de contêiner

Para habilitar o modo Kubernetes usando ganchos de ciclo de vida de contêiner, defina o `containerMode.type` para `kubernetes-novolume` no seu arquivo `values.yaml`.

```yaml
containerMode:
  type: "kubernetes-novolume"
```

#### Solução de problemas do modo kubernetes

Quando o modo Kubernetes estiver habilitado, ocorrerá uma falha nos fluxos de trabalho que não estiverem configurados com um trabalho de contêiner com um erro semelhante a:

```bash
Jobs without a job container are forbidden on this runner, please add a 'container:' to your job or contact your self-hosted runner administrator.
```

Para permitir que trabalhos sem um contêiner de trabalho sejam executados, configure `ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER` para `false` no contêiner runner. Isso instrui o corredor a desabilitar essa verificação.

!!! warning
    Permitir que trabalhos sejam executados sem um contêiner no modo `kubernetes` ou `kubernetes-novolume` pode fornecer privilégios elevados ao pod do executor com o servidor de API do Kubernetes, incluindo a capacidade de criar pods e acessar segredos. Antes de alterar esse padrão, recomendamos examinar cuidadosamente as possíveis implicações de segurança.

```yaml
  template:
    spec:
      containers:
        - name: runner
          image: ghcr.io/actions/actions-runner:latest
          command: ["/home/runner/run.sh"]
          env:
            - name: ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER
              value: "false"
```

### Como personalizar modos de contêiner

Ao definir o `containerMode` no arquivo `values.yaml` para o gráfico Helm [`gha-runner-scale-set`](https://github.com/actions/actions-runner-controller/blob/5347e2c2c80fbc45be7390eab117e861d30776d1/charts/gha-runner-scale-set/values.yaml#L77), você pode usar um dos seguintes valores:

* `dind` ou
* `kubernetes`

Dependendo do valor definido para o `containerMode`, uma configuração será automaticamente injetada na seção `template` do arquivo `values.yaml` para o  gráfico helm `gha-runner-scale-set`.

* Consulte a [`dind` configuração](https://github.com/actions/actions-runner-controller/blob/5347e2c2c80fbc45be7390eab117e861d30776d1/charts/gha-runner-scale-set/values.yaml#L110).
* Consulte a [`kubernetes` configuração](https://github.com/actions/actions-runner-controller/blob/5347e2c2c80fbc45be7390eab117e861d30776d1/charts/gha-runner-scale-set/values.yaml#L160).

Para personalizar a especificação, comente ou remova `containerMode` e acrescente a configuração desejada na seção `template`.

#### Por exemplo: executar `dind-rootless`

Antes de decidir executar `dind-rootless`, esteja ciente das [limitações conhecidas](https://docs.docker.com/engine/security/rootless/#known-limitations).

Para versões do Kubernetes >= v1.29, o contêiner sidecar será usado para executar o daemon do Docker.

```yaml
## githubConfigUrl is the GitHub url for where you want to configure runners
## ex: https://github.com/myorg/myrepo or https://github.com/myorg
githubConfigUrl: "https://github.com/actions/actions-runner-controller"

## githubConfigSecret is the k8s secrets to use when auth with GitHub API.
## You can choose to use GitHub App or a PAT token
githubConfigSecret: my-super-safe-secret

## maxRunners is the max number of runners the autoscaling runner set will scale up to.
maxRunners: 5

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
minRunners: 0

runnerGroup: "my-custom-runner-group"

## name of the runner scale set to create. Defaults to the helm release name
runnerScaleSetName: "my-awesome-scale-set"

## template is the PodSpec for each runner Pod
## For reference: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec
template:
  spec:
    initContainers:
    - name: init-dind-externals
      image: ghcr.io/actions/actions-runner:latest
      command: ["cp", "-r", "/home/runner/externals/.", "/home/runner/tmpDir/"]
      volumeMounts:
        - name: dind-externals
          mountPath: /home/runner/tmpDir
    - name: init-dind-rootless
      image: docker:dind-rootless
      command:
        - sh
        - -c
        - |
          set -x
          cp -a /etc/. /dind-etc/
          echo 'runner:x:1001:1001:runner:/home/runner:/bin/ash' >> /dind-etc/passwd
          echo 'runner:x:1001:' >> /dind-etc/group
          echo 'runner:100000:65536' >> /dind-etc/subgid
          echo 'runner:100000:65536' >> /dind-etc/subuid
          chmod 755 /dind-etc;
          chmod u=rwx,g=rx+s,o=rx /dind-home
          chown 1001:1001 /dind-home
      securityContext:
        runAsUser: 0
      volumeMounts:
        - mountPath: /dind-etc
          name: dind-etc
        - mountPath: /dind-home
          name: dind-home
    - name: dind
      image: docker:dind-rootless
      args:
        - dockerd
        - --host=unix:///run/user/1001/docker.sock
      securityContext:
        privileged: true
        runAsUser: 1001
        runAsGroup: 1001
      restartPolicy: Always
      startupProbe:
        exec:
          command:
            - docker
            - info
        initialDelaySeconds: 0
        failureThreshold: 24
        periodSeconds: 5
      volumeMounts:
        - name: work
          mountPath: /home/runner/_work
        - name: dind-sock
          mountPath: /run/user/1001
        - name: dind-externals
          mountPath: /home/runner/externals
        - name: dind-etc
          mountPath: /etc
        - name: dind-home
          mountPath: /home/runner
    containers:
    - name: runner
      image: ghcr.io/actions/actions-runner:latest
      command: ["/home/runner/run.sh"]
      env:
        - name: DOCKER_HOST
          value: unix:///run/user/1001/docker.sock
      securityContext:
        privileged: true
        runAsUser: 1001
        runAsGroup: 1001
      volumeMounts:
        - name: work
          mountPath: /home/runner/_work
        - name: dind-sock
          mountPath: /run/user/1001
    volumes:
    - name: work
      emptyDir: {}
    - name: dind-externals
      emptyDir: {}
    - name: dind-sock
      emptyDir: {}
    - name: dind-etc
      emptyDir: {}
    - name: dind-home
      emptyDir: {}
```

Para versões do Kubernetes `< v1.29`, a seguinte configuração será aplicada:

```yaml
## githubConfigUrl is the GitHub url for where you want to configure runners
## ex: https://github.com/myorg/myrepo or https://github.com/myorg
githubConfigUrl: "https://github.com/actions/actions-runner-controller"

## githubConfigSecret is the k8s secrets to use when auth with GitHub API.
## You can choose to use GitHub App or a PAT token
githubConfigSecret: my-super-safe-secret

## maxRunners is the max number of runners the autoscaling runner set will scale up to.
maxRunners: 5

## minRunners is the min number of idle runners. The target number of runners created will be
## calculated as a sum of minRunners and the number of jobs assigned to the scale set.
minRunners: 0

runnerGroup: "my-custom-runner-group"

## name of the runner scale set to create. Defaults to the helm release name
runnerScaleSetName: "my-awesome-scale-set"

## template is the PodSpec for each runner Pod
## For reference: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec
template:
  spec:
    initContainers:
    - name: init-dind-externals
      image: ghcr.io/actions/actions-runner:latest
      command: ["cp", "-r", "/home/runner/externals/.", "/home/runner/tmpDir/"]
      volumeMounts:
        - name: dind-externals
          mountPath: /home/runner/tmpDir
    - name: init-dind-rootless
      image: docker:dind-rootless
      command:
        - sh
        - -c
        - |
          set -x
          cp -a /etc/. /dind-etc/
          echo 'runner:x:1001:1001:runner:/home/runner:/bin/ash' >> /dind-etc/passwd
          echo 'runner:x:1001:' >> /dind-etc/group
          echo 'runner:100000:65536' >> /dind-etc/subgid
          echo 'runner:100000:65536' >> /dind-etc/subuid
          chmod 755 /dind-etc;
          chmod u=rwx,g=rx+s,o=rx /dind-home
          chown 1001:1001 /dind-home
      securityContext:
        runAsUser: 0
      volumeMounts:
        - mountPath: /dind-etc
          name: dind-etc
        - mountPath: /dind-home
          name: dind-home
    containers:
    - name: runner
      image: ghcr.io/actions/actions-runner:latest
      command: ["/home/runner/run.sh"]
      env:
        - name: DOCKER_HOST
          value: unix:///run/user/1001/docker.sock
      securityContext:
        privileged: true
        runAsUser: 1001
        runAsGroup: 1001
      volumeMounts:
        - name: work
          mountPath: /home/runner/_work
        - name: dind-sock
          mountPath: /run/user/1001
    - name: dind
      image: docker:dind-rootless
      args:
        - dockerd
        - --host=unix:///run/user/1001/docker.sock
      securityContext:
        privileged: true
        runAsUser: 1001
        runAsGroup: 1001
      volumeMounts:
        - name: work
          mountPath: /home/runner/_work
        - name: dind-sock
          mountPath: /run/user/1001
        - name: dind-externals
          mountPath: /home/runner/externals
        - name: dind-etc
          mountPath: /etc
        - name: dind-home
          mountPath: /home/runner
    volumes:
    - name: work
      emptyDir: {}
    - name: dind-externals
      emptyDir: {}
    - name: dind-sock
      emptyDir: {}
    - name: dind-etc
      emptyDir: {}
    - name: dind-home
      emptyDir: {}
```

#### Como reconhecer os ganchos do contêiner do executor

Quando o executor detecta uma execução de workflow que usa um trabalho de contêiner, contêiner de serviço ou ação do Docker, ele chama ganchos do contêiner do executor para criar um novo pod. O executor depende de ganchos do contêiner do executor para chamar as APIs do Kubernetes e criar um novo pod no mesmo namespace que o do pod do executor. Esse pod recém-criado é usado para executar o trabalho de contêiner, o contêiner de serviço ou a ação do Docker. Para obter mais informações, confira o repositório [`runner-container-hooks`](https://github.com/actions/runner-container-hooks).

#### Configuração de extensões de gancho

A partir da versão 0.4.0 do ARC, os ganchos do contêiner do executor suportam extensões de gancho. Você pode usá-los para configurar o pod criado pelo runner-container-hooks. Por exemplo, você pode usar uma extensão de gancho para definir um contexto de segurança no pod. As extensões de gancho permitem especificar um arquivo YAML que é usado para atualizar o [PodSpec](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#podspec-v1-core) do pod criado por ganchos do contêiner do executor.

Há duas opções para configurar extensões de gancho.

* Armazene em sua **imagem de executor personalizada**. Você pode armazenar o PodSpec em um arquivo YAML em qualquer lugar da sua imagem de executor personalizada. Para obter mais informações, consulte [Controlador de Ações Runner](../../../concepts/runners/actions-runner-controller.md#creating-your-own-runner-image).
* Armazene em um **ConfigMap**. Você pode criar um mapa de configurações com o PodSpec e montar esse mapa de configurações no contêiner do executor. Para obter mais informações, consulte [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) na documentação do Kubernetes.

!!! note
    Com as duas opções, é preciso definir a variável de ambiente `ACTIONS_RUNNER_CONTAINER_HOOK_TEMPLATE` na especificação do contêiner do executor para apontá-la para o caminho do arquivo YAML montado no contêiner do executor.

##### Exemplo: o uso do mapa de configurações para definir securityContext

Crie um mapa de configurações no mesmo namespace que os pods do executor. Por exemplo:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: hook-extension
  namespace: arc-runners
data:
  content: |
    metadata:
      annotations:
        example: "extension"
    spec:
      containers:
        - name: "$job" # Target the job container
          securityContext:
            runAsUser: 1000
```

* Os campos `.metadata.labels` e `metadata.annotations` serão acrescentados no estado em que se encontram, a menos que suas chaves sejam reservadas. Não é possível substituir os campos `.metadata.name` e `metadata.namespace`.
* A maioria dos campos PodSpec é aplicada com base no modelo especificado e substitui os valores passados do arquivo `values.yaml` do gráfico Helm.
* Se você especificar volumes adicionais, eles serão acrescentados aos volumes padrão especificados pelo executor.
* Os `spec.containers` são mesclados com base nos nomes atribuídos a eles.
  * Se o nome do contêiner for `$job`:
    * Os campos `spec.containers.name` e `spec.containers.image` são ignorados.
    * Os campos `spec.containers.env`, `spec.containers.volumeMounts` e `spec.containers.ports` são acrescentados à especificação de contêiner padrão criada pelo gancho.
    * O restante dos campos é aplicado da maneira fornecida.
  * Se o nome do contêiner não for `$job`, os campos serão adicionados à definição do pod como estão.

## Habilitar métricas

!!! note
    As métricas do ARC estão disponíveis a partir da versão gha-runner-scale-set-0.5.0.

O ARC pode emitir métricas para os executores, os trabalhos e o tempo gasto na execução dos fluxos de trabalho. As métricas podem ser usadas para identificar congestionamentos, monitorar a integridade da implantação do ARC, visualizar tendências de uso, otimizar o consumo de recursos, além de muitos outros casos de uso. As métricas são emitidas pelos pods controller-manager e listener no formato Prometheus. Para obter mais informações, consulte [Formatos de exposição](https://prometheus.io/docs/instrumenting/exposition_formats/) na documentação do Prometheus.

Para habilitar métricas no ARC, configure a propriedade `metrics` no arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) do gráfico `gha-runner-scale-set-controller`.

A seguir, há um exemplo de configuração.

```yaml
metrics:
  controllerManagerAddr: ":8080"
  listenerAddr: ":8080"
  listenerEndpoint: "/metrics"
```

!!! note
    Se o objeto `metrics:` não for fornecido ou for comentado, estes sinalizadores serão aplicados aos pods do gerenciador do controlador e do ouvinte com valores vazios: `--metrics-addr`, `--listener-metrics-addr` e `--listener-metrics-endpoint`. Quando isso acontece, as métricas são desabilitadas no ARC.

Depois que essas propriedades são configuradas, os pods controller-manager e listener emitem métricas por meio do listenerEndpoint associado às portas especificadas no arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml). No exemplo acima, o ponto de extremidade é `/metrics` e a porta é `:8080`. Você pode usar esse ponto de extremidade para extrair métricas dos pods controller-manager e listener.

Para desligar as métricas, atualize o arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) removendo ou comentando o objeto `metrics:` e suas propriedades.

### Métricas disponíveis no ARC

As métricas emitidas pelos pods controlador-gerente e ouvinte são exibidas na tabela a seguir.

!!! note
    As métricas que o gerenciador de controladores emite pertencem ao runtime do controlador e não pertencem a GitHub.

| Proprietário | Métrica | Tipo | Descrição |
| --- | --- | --- | --- |
| gerenciador-controlador | gha_controller_pending_ephemeral_runners | medidor | Número de executores efêmeros em estado pendente |
| gerenciador-controlador | gha_controller_running_ephemeral_runners | medidor | Número de executores efêmeros em estado de execução |
| gerenciador-controlador | gha_controller_failed_ephemeral_runners | medidor | Número de executores efêmeros em estado de falha |
| gerenciador-controlador | gha_controller_running_listeners | medidor | Número de ouvintes em um estado de execução |
| ouvinte | gha_assigned_jobs | medidor | Número de trabalhos atribuídos ao conjunto de dimensionamento de executores |
| ouvinte | gha_running_jobs | medidor | Número de trabalhos em execução ou na fila para execução |
| ouvinte | gha_registered_runners | medidor | Número de executores registrados pelo conjunto de dimensionamento de executores |
| ouvinte | gha_busy_runners | medidor | Número de corredores registrados atualmente executando um trabalho |
| ouvinte | gha_min_runners | medidor | Número mínimo de executores configurados para o conjunto de dimensionamento de executores |
| ouvinte | gha_max_runners | medidor | Número máximo de executores configurados para o conjunto de dimensionamento de executores |
| ouvinte | gha_desired_runners | medidor | Número de executores desejados (meta de escala/redução vertical) pelo conjunto de dimensionamento de executores |
| ouvinte | gha_idle_runners | medidor | Número de executores registrados que não estão executando um trabalho |
| ouvinte | gha_started_jobs_total | contador | Número total de trabalhos iniciados desde que o listener ficou pronto \[1] |
| ouvinte | gha_completed_jobs_total | contador | Número total de trabalhos concluídos desde que o listener ficou pronto \[1] |
| ouvinte | gha_job_startup_duration_seconds | histograma | Número de segundos gastos aguardando a tarefa do fluxo de trabalho para iniciar no executor de propriedade do conjunto de dimensionamento do executor |
| ouvinte | gha_job_execution_duration_seconds | histograma | Número de segundos gastos executando tarefas do fluxo de trabalho pelo conjunto de dimensionamento do executor |

\[1]: Listener metrics that have the counter type are reset when the listener pod restarts.

## Como atualizar o ARC

Como não há suporte para atualizar ou excluir CRDs com o Helm, não é possível usar o Helm para atualizar o ARC. Para obter mais informações, consulte [Custom Resource Definitions](https://helm.sh/docs/chart_best_practices/custom_resource_definitions/#some-caveats-and-explanations) na documentação do Helm. Para atualizar o ARC para uma versão mais recente, você deve concluir as etapas a seguir.

1. Desinstale todas as instalações do `gha-runner-scale-set`.
2. Aguarde a limpeza dos recursos.
3. Desinstale o ARC.
4. Se houver uma alteração nos CRDs da versão que está instalada no momento para a versão atualizada, remova todos os CRDs associados ao grupo de APIs do `actions.github.com`.
5. Reinstale o ARC novamente.

Para obter mais informações, consulte [Como implantar um conjunto de dimensionamento de executores](deploy-runner-scale-sets.md#deploying-a-runner-scale-set).

Se você quiser atualizar o ARC, mas estiver preocupado com o tempo de inatividade, poderá implantar o ARC em uma configuração de alta disponibilidade para garantir que os executores estejam sempre disponíveis. Para obter mais informações, consulte [Alta disponibilidade e failover automático](deploy-runner-scale-sets.md#high-availability-and-automatic-failover).

!!! note
    A transição da versão do ARC compatível com a comunidade para a versão com suporte do GitHub é uma alteração arquitetônica substancial. A versão GitHub com suporte envolve uma reformulação de muitos componentes do ARC. Não é um pequeno upgrade de software. Por esses motivos, recomendamos testar as novas versões em um ambiente de preparo que corresponda primeiro ao seu ambiente de produção. Isso garantirá a estabilidade e a confiabilidade da configuração antes da implantação em produção.

### Como implantar uma imagem canário

Você pode testar os recursos antes que eles sejam liberados usando versões canário da imagem de contêiner controller-manager. As imagens canário são publicadas no formato de tag `canary-SHORT_SHA`. Para obter mais informações, consulte [`gha-runner-scale-set-controller`](https://github.com/actions/actions-runner-controller/pkgs/container/gha-runner-scale-set-controller) no Container registry.

!!! note
    * Você deve usar gráficos Helm em seu sistema de arquivos local.
    * Você não pode usar os gráficos Helm liberados.

1. Atualize o `tag` no arquivo [gha-runner-scale-set-controller `values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set-controller/values.yaml) para: `canary-SHORT_SHA`
2. Atualize o campo `appVersion` no arquivo [`Chart.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/Chart.yaml) de `gha-runner-scale-set` para: `canary-SHORT_SHA`
3. Reinstale o ARC usando o gráfico e os arquivos `values.yaml` atualizados do Helm.

## Alta disponibilidade e failover automático

O ARC pode ser implantado em uma configuração de alta disponibilidade (ativo-ativo). Se você tiver dois clusters Kubernetes distintos implantados em regiões separadas, poderá implantar o ARC em ambos os clusters e configurar conjuntos de dimensionamento de executor para usar o mesmo `runnerScaleSetName`. Para fazer isso, cada conjunto de dimensionamento de executores deve ser atribuído a um grupo de executores distinto. Por exemplo, você pode ter dois conjuntos de dimensionamento de executores, cada um nomeado `arc-runner-set`, desde que um conjunto de dimensionamento de executores pertença a `runner-group-A` e o outro pertença a `runner-group-B`. Para obter informações sobre como atribuir conjuntos de dimensionamento de executores a grupos de executores, consulte [Gerenciar o acesso a executores auto-hospedados usando grupos](../self-hosted-runners/manage-access.md).

Se os dois conjuntos de dimensionamento de executores estiverem online, os trabalhos atribuídos a eles serão distribuídos arbitrariamente (corrida de atribuição). Não é possível configurar o algoritmo de atribuição de trabalho. Se um dos clusters ficar inativo, o conjunto de dimensionamento de executores no outro cluster continuará a adquirir trabalhos normalmente sem qualquer intervenção ou alteração de configuração.

## Como usar o ARC entre organizações

Uma única instalação de Actions Runner Controller permite que você configure um ou mais conjuntos de dimensionamento de executores. Esses conjuntos de dimensionamento de executores podem ser registrados em um repositório, uma organização ou uma empresa. Use também grupos de executores para controlar os limites de permissões desses conjuntos de dimensionamento de executores.

Como melhor prática, crie um namespace exclusivo para cada organização. Você também pode criar um namespace para cada grupo de executores ou cada conjunto de dimensionamento de executores. Você pode instalar quantos conjuntos de dimensionamento de executores forem necessários em cada namespace. Isso vai fornecer os níveis mais altos de isolamento e aprimorar sua segurança. Você pode usar GitHub Apps para autenticação e definir permissões granulares para cada conjunto de executores.

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
