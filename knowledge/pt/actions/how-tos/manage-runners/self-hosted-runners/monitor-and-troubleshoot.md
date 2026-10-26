---
title: Monitorar e solucionar problemas de executores auto-hospedados
description: Você pode monitorar seus executores auto-hospedados para visualizar sua atividade e diagnosticar problemas comuns.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot
captured: '2026-10-26'
section: How tos / Manage runners / Self hosted runners
---

# Monitorar e solucionar problemas de executores auto-hospedados

_Você pode monitorar seus executores auto-hospedados para visualizar sua atividade e diagnosticar problemas comuns._

## Como verificar os níveis de acesso

Talvez você não consiga criar um executor auto-hospedado para um repositório de propriedade da organização.

organização podem escolher quais repositórios têm permissão para criar executores auto-hospedados em nível de repositório.

Para obter mais informações, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners).

## Como verificar o status de um executor auto-hospedado

Um executor auto-hospedado pode estar localizado no repositório, na organização ou nas configurações de conta corporativa do GitHub. Para gerenciar um executor auto-hospedado, você deve ter as seguintes permissões, dependendo de onde o executor auto-hospedado foi adicionado:

* **Repositório do usuário**: você precisa ser o proprietário do repositório.
* **Organização**: você precisa ser um proprietário da organização.
* **Repositório da organização**: você precisa ser um proprietário da organização ou ter acesso de administrador no repositório.

1. Na organização ou no repositório, navegue até a página principal e clique em **(gear) Settings**.

2. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.

3. Em "Executores", você pode ver uma lista de executores registrados, incluindo o nome, etiqueta e status do executor.

   O status pode ser um dos seguintes:

   * **Ocioso:** o executor está conectado a GitHub e está pronto para executar trabalhos.
   * **Ativo:** O executor está executando uma tarefa no momento.
   * **Offline:** O executor não está conectado a GitHub. Isso pode ocorrer porque o computador está offline, o aplicativo executor auto-hospedado não está em execução no computador ou o aplicativo executor auto-hospedado não pode se comunicar.GitHub

## Solução de problemas da conectividade de rede

### Verificação da conectividade de rede do executor hospedado localmente

Você pode usar o script `config` do aplicativo de executor auto-hospedado com o parâmetro `--check` para verificar se um executor auto-hospedado pode acessar todos os serviços de rede necessários em GitHub.

Além de `--check`, você precisa fornecer dois argumentos para o script:

* `--url` com a URL do seu GitHub repositório, organização ou empresa. Por exemplo, `--url https://github.com/octo-org/octo-repo`.
* `--pat` com o valor de um personal access token (classic), que deve ter o escopo `workflow`, ou um fine-grained personal access token com acesso de leitura e gravação a fluxos de trabalho. Por exemplo, `--pat ghp_abcd1234`. Para saber mais, confira [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

Por exemplo:

```shell
./config.sh --check --url URL --pat ghp_abcd1234
```

```shell
./config.sh --check --url URL --pat ghp_abcd1234
```

```powershell
config.cmd --check --url https://github.com/YOUR-ORG/YOUR-REPO --pat GHP_ABCD1234
```

O script testa cada serviço e gera um `PASS` ou um `FAIL` para cada um. Se você tiver alguma verificação com falha, pode ver mais detalhes sobre o problema no arquivo de log da verificação. Os arquivos de log estão localizados no diretório `_diag` em que você instalou o aplicativo do executor, e o caminho do arquivo de log para cada verificação é mostrado na saída do console do script.

Se você tiver alguma verificação com falha, você deve também verificar se a sua máquina de executores auto-hospedada cumpre todos os requisitos de comunicação. Para saber mais, confira [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md).

### Desabilitando verificação de certificado TLS

Por padrão, o aplicativo executor auto-hospedado verifica o certificado TLS para GitHub. Se você encontrar problemas de rede, você deverá desabilitar a verificação de certificado TLS para fins de teste.

Para desabilitar a verificação de certificação TLS no aplicativo do executor auto-hospedado, defina a variável de ambiente `GITHUB_ACTIONS_RUNNER_TLS_NO_VERIFY` como `1` antes de configurar e executar o aplicativo do executor auto-hospedado.

```shell
export GITHUB_ACTIONS_RUNNER_TLS_NO_VERIFY=1
./config.sh --url https://github.com/YOUR-ORG/YOUR-REPO --token
./run.sh
```

```shell
export GITHUB_ACTIONS_RUNNER_TLS_NO_VERIFY=1
./config.sh --url https://github.com/YOUR-ORG/YOUR-REPO --token
./run.sh
```

```powershell
[Environment]::SetEnvironmentVariable('GITHUB_ACTIONS_RUNNER_TLS_NO_VERIFY', '1')
./config.cmd --url https://github.com/YOUR-ORG/YOUR-REPO --token
./run.cmd
```

!!! warning
    Não é recomendável desabilitar a verificação do TLS, pois o TLS fornece privacidade e integridade de dados entre o aplicativo executor auto-hospedado e GitHub. Recomendamos que você instale o certificado GitHub no armazenamento de certificados do sistema operacional do seu executor auto-hospedado. Para obter diretrizes sobre como instalar o certificado, verifique com o GitHub fornecedor do sistema operacional.

    [!NOTE]
    Para Executores maiores hospedados no GitHub usar Azure rede privada, consulte os requisitos de interceptação do TLS no [Configurando rede privada para executores hospedados no GitHub na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/configuring-private-networking-for-github-hosted-runners-in-your-organization#prerequisites).

## Revisar os arquivos de registro do aplicativo do executor auto-hospedado

Você pode monitorar o status do aplicativo do executor auto-hospedado e suas atividades. Os arquivos de log são mantidos no diretório `_diag` em que você instalou o aplicativo do executor, e um novo log é gerado sempre que o aplicativo é iniciado. O nome do arquivo começa com `Runner_` e é seguido de um carimbo de data/hora UTC de quando o aplicativo é iniciado.

!!! warning
    Os arquivos de log do aplicativo do executor para executores efêmeros devem ser encaminhados e preservados externamente para fins de solução de problemas e diagnóstico. Para obter mais informações sobre executores efêmeros e dimensionamento automático de executores auto-hospedados, consulte [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md#ephemeral-runners-for-autoscaling).

Para obter logs detalhados sobre as execuções de tarefa de fluxo de trabalho, confira a próxima seção que descreve os arquivos `Worker_`.

## Revisar o arquivo de registro de um trabalho

O aplicativo do executor auto-hospedado cria um arquivo de registro detalhado para cada trabalho que processa. Esses arquivos são armazenados no diretório `_diag` em que você instalou o aplicativo do executor, e o nome do arquivo começa com `Worker_`.

## Usar journalctl para verificar o serviço do aplicativo do executor auto-hospedado

Para executores auto-hospedados baseados em Linux que executam o aplicativo usando um serviço, use `journalctl` para monitorar sua atividade em tempo real. O serviço padrão baseado em sistema usa a seguinte convenção de nomenclatura: `actions.runner.<org>-<repo>.<runnerName>.service`. Esse nome será truncado se exceder 80 caracteres, ou seja, a maneira preferencial de localizar o nome do serviço é verificando o arquivo *.service*. Por exemplo:

```shell
$ cat ~/actions-runner/.service
actions.runner.octo-org-octo-repo.runner01.service
```

Se isso falhar devido ao serviço que está sendo instalado em outro lugar, você poderá encontrar o nome do serviço na lista de serviços em execução. Por exemplo, na maioria dos sistemas Linux, você pode usar o comando `systemctl`:

```shell
$ systemctl --type=service | grep actions.runner
actions.runner.octo-org-octo-repo.hostname.service loaded active running GitHub Actions Runner (octo-org-octo-repo.hostname)
```

Use `journalctl` para monitorar a atividade em tempo real do executor auto-hospedado:

```shell
sudo journalctl -u actions.runner.octo-org-octo-repo.runner01.service -f
```

Neste exemplo de saída, você pode ver `runner01` ser iniciado, receber um trabalho chamado `testAction` e exibir o status resultante:

```shell
Feb 11 14:57:07 runner01 runsvc.sh[962]: Starting Runner listener with startup type: service
Feb 11 14:57:07 runner01 runsvc.sh[962]: Started listener process
Feb 11 14:57:07 runner01 runsvc.sh[962]: Started running service
Feb 11 14:57:16 runner01 runsvc.sh[962]: √ Connected to GitHub
Feb 11 14:57:17 runner01 runsvc.sh[962]: 2020-02-11 14:57:17Z: Listening for Jobs
Feb 11 16:06:54 runner01 runsvc.sh[962]: 2020-02-11 16:06:54Z: Running job: testAction
Feb 11 16:07:10 runner01 runsvc.sh[962]: 2020-02-11 16:07:10Z: Job testAction completed with result: Succeeded
```

Para ver a configuração `systemd`, localize o arquivo de serviço aqui: `/etc/systemd/system/actions.runner.<org>-<repo>.<runnerName>.service`.
Se você desejar personalizar o serviço de aplicação do executor auto-hospedado, não modifique esse arquivo diretamente. Siga as instruções descritas em [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md#customizing-the-self-hosted-runner-service).

## Como usar `launchd` para verificar o serviço de aplicativo do executor auto-hospedado

Para executores auto-hospedados baseados em macOS que executam o aplicativo como um serviço, use `launchctl` para monitorar sua atividade em tempo real. O serviço padrão baseado em launchd utiliza a seguinte convenção de nomenclatura: `actions.runner.<org>-<repo>.<runnerName>`. Esse nome será truncado se exceder 80 caracteres, ou seja, a maneira preferencial de localizar o nome do serviço é verificando o arquivo *.service* no diretório do executor:

```shell
% cat ~/actions-runner/.service
/Users/exampleUsername/Library/LaunchAgents/actions.runner.octo-org-octo-repo.runner01.plist
```

O script `svc.sh` usa `launchctl` para verificar se o aplicativo está em execução. Por exemplo:

```shell
$ ./svc.sh status
status actions.runner.example.runner01:
/Users/exampleUsername/Library/LaunchAgents/actions.runner.example.runner01.plist
Started:
379 0 actions.runner.example.runner01
```

A saída resultante inclui a ID do processo e o nome do serviço `launchd` do aplicativo.

Para ver a configuração `launchd`, localize o arquivo de serviço aqui: `/Users/exampleUsername/Library/LaunchAgents/actions.runner.<repoName>.<runnerName>.service`.
Se você desejar personalizar o serviço de aplicação do executor auto-hospedado, não modifique esse arquivo diretamente. Siga as instruções descritas em [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md#customizing-the-self-hosted-runner-service).

## Usar PowerShell para verificar o serviço do aplicativo do executor auto-hospedado

Para executores auto-hospedados baseados no Windows que executam o aplicativo como um serviço, você pode usar o PowerShell para monitorar suas atividades em tempo real. O serviço usa a convenção de nomenclatura `GitHub Actions Runner (<org>-<repo>.<runnerName>)`. Você também pode encontrar o nome do serviço verificando o arquivo *.service* no diretório do executor:

```powershell
PS C:\actions-runner> Get-Content .service
actions.runner.octo-org-octo-repo.runner01.service
```

Veja o status do executor no aplicativo *Serviços* do Windows (`services.msc`). Você também pode usar o PowerShell para verificar se o serviço está sendo executado:

```powershell
PS C:\actions-runner> Get-Service "actions.runner.octo-org-octo-repo.runner01.service" | Select-Object Name, Status
Name                                                  Status
----                                                  ------
actions.runner.octo-org-octo-repo.runner01.service    Running
```

Você pode usar o PowerShell para verificar a atividade recente do executor auto-hospedado. Neste exemplo de saída, você pode ver o aplicativo ser iniciado, receber um trabalho chamado `testAction` e exibir o status resultante:

```powershell
PS C:\actions-runner> Get-EventLog -LogName Application -Source ActionsRunnerService

   Index Time          EntryType   Source                 InstanceID Message
   ----- ----          ---------   ------                 ---------- -------
     136 Mar 17 13:45  Information ActionsRunnerService          100 2020-03-17 13:45:48Z: Job Greeting completed with result: Succeeded
     135 Mar 17 13:45  Information ActionsRunnerService          100 2020-03-17 13:45:34Z: Running job: testAction
     134 Mar 17 13:41  Information ActionsRunnerService          100 2020-03-17 13:41:54Z: Listening for Jobs
     133 Mar 17 13:41  Information ActionsRunnerService          100 û Connected to GitHub
     132 Mar 17 13:41  Information ActionsRunnerService            0 Service started successfully.
     131 Mar 17 13:41  Information ActionsRunnerService          100 Starting Actions Runner listener
     130 Mar 17 13:41  Information ActionsRunnerService          100 Starting Actions Runner Service
     129 Mar 17 13:41  Information ActionsRunnerService          100 create event log trace source for actions-runner service
```

## Monitorar o processo de atualização automática

Recomendamos que você verifique regularmente o processo de atualização automática, uma vez que o executor auto-hospedado não será capaz de processar os trabalhos se estiver abaixo de um determinado limite de versão. O aplicativo do executor auto-hospedado atualiza-se automaticamente, mas observe que este processo não inclui atualizações do sistema operacional ou de outro software; você precisará gerenciar essas atualizações separadamente.

Você pode ver as atividades de atualização nos arquivos de log `Runner_`. Por exemplo:

```shell
[Feb 12 12:37:07 INFO SelfUpdater] An update is available.
```

Além disso, você pode encontrar mais informações nos arquivos de log *SelfUpdate* localizados no diretório `_diag` em que você instalou o aplicativo runner.

## Resolução de problemas de contêineres em executores auto-hospedados

### Verificar se o Docker está instalado

Se seus trabalhos exigirem contêineres, o executor auto-hospedado deverá ser baseado no Linux e deverá ter o Docker instalado. Verifique se o seu executor auto-hospedado tem o Docker instalado e se o serviço está em execução.

Use `systemctl` para verificar o status do serviço:

```shell
$ sudo systemctl is-active docker.service
active
```

Se o Docker não estiver instalado, ações dependentes irão falhar com as seguintes mensagens de erro:

```shell
[2020-02-13 16:56:10Z INFO DockerCommandManager] Which: 'docker'
[2020-02-13 16:56:10Z INFO DockerCommandManager] Not found.
[2020-02-13 16:56:10Z ERR  StepsRunner] Caught exception from step: System.IO.FileNotFoundException: File not found: 'docker'
```

### Verificar as permissões do Docker

Se seu trabalho falhar com o seguinte erro:

```shell
dial unix /var/run/docker.sock: connect: permission denied
```

Verifique se a conta de serviço do executor auto-hospedado tem permissão para usar o serviço do Docker. Identifique essa conta verificando a configuração do executor auto-hospedado em `systemd`. Por exemplo:

```shell
$ sudo systemctl show -p User actions.runner.octo-org-octo-repo.runner01.service
User=runner-user
```

### Verificando qual motor do Docker está instalado no executor

Caso seu build falhe com o seguinte erro:

```shell
Error: Input required and not supplied: java-version
```

Verifique qual mecanismo do Docker está instalado no executor auto-hospedado. Para passar as entradas de uma ação para o contêiner do Docker, o executor usa variáveis de ambiente cujos nomes podem conter traços. A ação talvez não consiga obter as entradas se o mecanismo do Docker não for um executável binário, mas, em vez disso, for um wrapper de shell ou um link (por exemplo, um mecanismo do Docker instalado no Linux usando `snap`). Para resolver esse erro, configure seu executor auto-hospedado para usar um mecanismo diferente do Docker.

Para verificar se o mecanismo do Docker foi instalado usando o `snap`, use o comando `which`. No seguinte exemplo, o mecanismo do Docker foi instalado usando o `snap`:

```shell
$ which docker
/snap/bin/docker
```
