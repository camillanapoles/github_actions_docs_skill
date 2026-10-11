---
title: Configurar o aplicativo do executor auto-hospedado como um serviço
description: Você pode configurar o aplicativo do executor auto-hospedado como um serviço para que inicie o aplicativo do executor automaticamente quando a máquina for iniciada.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application
captured: '2026-10-11'
section: GitHub Actions
---

# Configurar o aplicativo do executor auto-hospedado como um serviço

_Você pode configurar o aplicativo do executor auto-hospedado como um serviço para que inicie o aplicativo do executor automaticamente quando a máquina for iniciada._

<div class="ghd-tool linux">

> \[!NOTE]
> Você deve adicionar um executor a GitHub antes de poder configurar o aplicativo do executor auto-hospedado como um serviço.
> Para saber mais, confira [Adicionar executores auto-hospedados](add-runners.md).

Para sistemas Linux que usam `systemd`, você pode usar o script `svc.sh` que é criado após incluir com êxito o executor a fim de instalar e gerenciar usando o aplicativo como um serviço.

No computador executor, abra um shell no diretório em que você instalou o aplicativo executor auto-hospedado. Use os comandos abaixo para instalar e gerenciar o serviço de executor auto-hospedado.

</div>

<div class="ghd-tool windows">

> \[!NOTE]
> Configurar o aplicativo executor auto-hospedado como um serviço no Windows faz parte do processo de configuração do aplicativo. Se você já configurou o aplicativo de executor auto-hospedado, mas não escolheu configurá-lo como um serviço, você deve remover o executor do GitHub e reconfigurar o aplicativo. Ao reconfigurar o aplicativo, selecione a opção para configurar o aplicativo como um serviço.
>
> Para saber mais, confira [Remover executores auto-hospedados](remove-runners.md) e [Adicionar executores auto-hospedados](add-runners.md).

Você pode gerenciar o serviço de executor no aplicativo **Serviços** Windows ou usar o PowerShell para executar os comandos abaixo.

</div>

<div class="ghd-tool mac">

> \[!NOTE]
> Você deve adicionar um executor a GitHub antes de poder configurar o aplicativo do executor auto-hospedado como um serviço.
> Para saber mais, confira [Adicionar executores auto-hospedados](add-runners.md).

No computador executor, abra um shell no diretório em que você instalou o aplicativo executor auto-hospedado. Use os comandos abaixo para instalar e gerenciar o serviço de executor auto-hospedado.

</div>

<div class="ghd-tool linux">

## Instalar o serviço

1. Pare o aplicativo de executor auto-hospedado se ele estiver em execução no momento.

2. Instale o serviço com o comando a seguir:

            ```shell
   sudo ./svc.sh install
   ```

3. Como alternativa, o comando usa um argumento `user` opcional para instalar o serviço como outro usuário.

            ```shell
   ./svc.sh install USERNAME
   ```

</div>

<div class="ghd-tool mac">

## Instalar o serviço

1. Pare o aplicativo de executor auto-hospedado se ele estiver em execução no momento.
2. Instale o serviço com o comando a seguir:

            ```shell
   ./svc.sh install
   ```

</div>

## Iniciar o serviço

Inicie o serviço com o seguinte comando:

<div class="ghd-tool linux">

```shell
sudo ./svc.sh start
```

> \[!NOTE]
> Em sistemas Linux baseados em Debian (como Debian ou Ubuntu) com `needrestart` habilitado, `needrestart` você pode impedir a reinicialização do serviço executor durante um trabalho de fluxo de trabalho configurando-o para ignorar o serviço executor. Execute o comando a seguir:
>
> ```bash
> echo '$nrconf{override_rc}{qr(^actions\.runner\..+\.service$)} = 0;' | sudo tee /etc/needrestart/conf.d/actions_runner_services.conf
> ```

</div>

<div class="ghd-tool windows">

```shell
Start-Service "actions.runner.*"
```

</div>

<div class="ghd-tool mac">

```shell
./svc.sh start
```

</div>

## Verificando o status do serviço

Verifique o status do serviço com o comando a seguir:

<div class="ghd-tool linux">

```shell
sudo ./svc.sh status
```

</div>

<div class="ghd-tool windows">

```shell
Get-Service "actions.runner.*"
```

</div>

<div class="ghd-tool mac">

```shell
./svc.sh status
```

</div>

Para obter mais informações sobre como visualizar o status do seu executor auto-hospedado, consulte [Monitorar e solucionar problemas de executores auto-hospedados](monitor-and-troubleshoot.md).

## Interromper o serviço

Interrompa o serviço com o comando a seguir:

<div class="ghd-tool linux">

```shell
sudo ./svc.sh stop
```

</div>

<div class="ghd-tool windows">

```shell
Stop-Service "actions.runner.*"
```

</div>

<div class="ghd-tool mac">

```shell
./svc.sh stop
```

</div>

## Desinstalando o serviço

1. Interrompa o serviço se estiver em execução.
2. Desinstale o serviço com o comando a seguir:

    <div class="ghd-tool linux">

            ```shell
   sudo ./svc.sh uninstall
   ```

    </div>

    <div class="ghd-tool windows">

            ```shell
   Remove-Service "actions.runner.*"
   ```

    </div>

    <div class="ghd-tool mac">

            ```shell
   ./svc.sh uninstall
   ```

    </div>

<div class="ghd-tool linux">

## Personalizar o serviço do executor auto-hospedado

Caso não deseje usar a configuração padrão do serviço `systemd` acima, crie um serviço personalizado ou use o mecanismo de serviço que preferir. Considere o uso do modelo `serviced` localizado em `actions-runner/bin/actions.runner.service.template` como uma referência. Se você usa um serviço personalizado, o serviço do executor auto-hospedado precisa sempre ser acessado por meio do ponto de entrada `runsvc.sh`.

</div>

<div class="ghd-tool mac">

## Personalizar o serviço do executor auto-hospedado

Se você não desejar usar a configuração-padrão do serviço do launchd acima, você poderá criar um serviço personalizado ou usar o mecanismo de serviço que preferir. Considere o uso do modelo `plist` localizado em `actions-runner/bin/actions.runner.plist.template` como uma referência. Se você usa um serviço personalizado, o serviço do executor auto-hospedado precisa sempre ser acessado por meio do ponto de entrada `runsvc.sh`.

</div>
