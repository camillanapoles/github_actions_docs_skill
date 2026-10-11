---
title: Configuring the self-hosted runner application as a service
description: You can configure the self-hosted runner application as a service to automatically start the runner application when the machine starts.
lang: en
plan: fpt
source: https://github.com/github/docs/blob/main/content/actions/how-tos/manage-runners/self-hosted-runners/configure-the-application.md
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Configuring the self-hosted runner application as a service

_You can configure the self-hosted runner application as a service to automatically start the runner application when the machine starts._

!!! note
    GitHub Enterprise Server users should use self-hosted runners. GitHub-hosted runners are **not** supported.

1. Stop the self-hosted runner application if it is currently running.
On the runner machine, open a shell in the directory where you installed the self-hosted runner application. Use the commands below to install and manage the self-hosted runner service.

!!! note
    You must add a runner to GitHub before you can configure the self-hosted runner application as a service.

For more information, see [Adding self-hosted runners](add-runners.md).

actions.runner.*

**Linux**

{{ service_nonwindows_intro }}

For Linux systems that use `systemd`, you can use the `svc.sh` script that is created after successfully adding the runner to install and manage using the application as a service.

{{ service_non_windows_intro_shell }}

**Windows**

!!! note
    Configuring the self-hosted runner application as a service on Windows is part of the application configuration process. If you have already configured the self-hosted runner application but did not choose to configure it as a service, you must remove the runner from GitHub and re-configure the application. When you re-configure the application, choose the option to configure the application as a service.

    For more information, see [Removing self-hosted runners](remove-runners.md) and [Adding self-hosted runners](add-runners.md).

You can manage the runner service in the Windows **Services** application, or you can use PowerShell to run the commands below.

**macOS**

{{ service_nonwindows_intro }}

{{ service_non_windows_intro_shell }}

**Linux**

## Installing the service

{{ service_first_step }}
1. Install the service with the following command:

            ```shell
   sudo ./svc.sh install
   ```

1. Alternatively, the command takes an optional `user` argument to install the service as a different user.

            ```shell
   ./svc.sh install USERNAME
   ```

**macOS**

## Installing the service { #installing-the-service-1 }

{{ service_first_step }}
1. Install the service with the following command:

            ```shell
   ./svc.sh install
   ```

## Starting the service

Start the service with the following command:

**Linux**

```shell
sudo ./svc.sh start
```

!!! note
    On Debian-based Linux systems (such as Debian or Ubuntu) with `needrestart` enabled, you can prevent `needrestart` from restarting the runner service during a workflow job by configuring it to ignore the runner service. Run the following command:

                ```bash
    echo '$nrconf{override_rc}{qr(^actions.runner..+.service$)} = 0;' | sudo tee /etc/needrestart/conf.d/actions_runner_services.conf
    ```

**Windows**

```shell
Start-Service "{{ service_win_name }}"
```

**macOS**

```shell
./svc.sh start
```

## Checking the status of the service

Check the status of the service with the following command:

**Linux**

```shell
sudo ./svc.sh status
```

**Windows**

```shell
Get-Service "{{ service_win_name }}"
```

**macOS**

```shell
./svc.sh status
```

 For more information on viewing the status of your self-hosted runner, see [Monitoring and troubleshooting self-hosted runners](monitor-and-troubleshoot.md).

## Stopping the service

Stop the service with the following command:

**Linux**

```shell
sudo ./svc.sh stop
```

**Windows**

```shell
Stop-Service "{{ service_win_name }}"
```

**macOS**

```shell
./svc.sh stop
```

## Uninstalling the service

1. Stop the service if it is currently running.
1. Uninstall the service with the following command:

**Linux**

```shell
    sudo ./svc.sh uninstall
    ```

**Windows**

```shell
    Remove-Service "{{ service_win_name }}"
    ```

**macOS**

```shell
    ./svc.sh uninstall
    ```

**Linux**

## Customizing the self-hosted runner service

If you don't want to use the above default `systemd` service configuration, you can create a customized service or use whichever service mechanism you prefer. Consider using the `serviced` template at `actions-runner/bin/actions.runner.service.template` as a reference. If you use a customized service, the self-hosted runner service must always be invoked using the `runsvc.sh` entry point.

**macOS**

## Customizing the self-hosted runner service { #customizing-the-self-hosted-runner-service-1 }

If you don't want to use the above default launchd service configuration, you can create a customized service or use whichever service mechanism you prefer. Consider using the `plist` template at `actions-runner/bin/actions.runner.plist.template` as a reference. If you use a customized service, the self-hosted runner service must always be invoked using the `runsvc.sh` entry point.
