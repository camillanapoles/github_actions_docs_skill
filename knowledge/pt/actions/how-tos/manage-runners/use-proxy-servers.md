---
title: Utilizando servidores proxy com um executor
description: Você pode configurar executores em ambientes isolados para usar um servidor proxy para comunicação segura com GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/use-proxy-servers
captured: '2026-10-11'
section: How tos / Manage runners
---

# Utilizando servidores proxy com um executor

_Você pode configurar executores em ambientes isolados para usar um servidor proxy para comunicação segura com GitHub._

## Configurando um proxy para executores do Linux e do Windows

Se o executor precisar se comunicar por meio de um servidor proxy, você poderá definir configurações de proxy usando variáveis de ambiente ou configurações no nível do sistema.

| Variable | Description | Example |
| --- | --- | --- |
| `https_proxy` | URL de proxy para tráfego HTTPS. Você pode incluir a autenticação básica, se necessário. | `http://proxy.local`<br>`http://192.168.1.1:8080`<br>`http://username:password@proxy.local` |
| `http_proxy` | URL de proxy para tráfego HTTP. Você pode incluir a autenticação básica, se necessário. | `http://proxy.local`<br>`http://192.168.1.1:8080`<br>`http://username:password@proxy.local` |
| `no_proxy` | Uma lista separada por vírgulas de hosts ou endereços IP que devem ignorar o proxy. Alguns clientes só respeitam endereços IP quando as conexões são feitas diretamente com o IP em vez de um nome de host. | `example.com`<br>`example.com,myserver.local:443,example.org` |

As variáveis de ambiente de proxy são lidas quando o aplicativo executor é iniciado, portanto, você deve definir as variáveis de ambiente antes de configurar ou iniciar o aplicativo executor. Se a configuração do proxy for alterada, você deverá reiniciar o aplicativo executor.

Em computadores Windows, os nomes das variáveis de ambiente proxy não diferenciam maiúsculas de minúsculas. Nos sistemas Linux e macOS, recomendamos que você use variáveis de ambiente em minúscula. Caso tenha uma variável de ambiente em letras minúsculas e maiúsculas no Linux ou macOS (por exemplo, `https_proxy` e `HTTPS_PROXY`), o aplicativo executor auto-hospedado usará a variável de ambiente em minúsculas.

A conexão entre executores auto-hospedados e GitHub ocorre em HTTPS (porta 443).

!!! warning
    Os executores auto-hospedados não oferecem suporte ao uso de endereços IP e intervalos CIDR na variável de ambiente `no_proxy`. Se sua instância de GitHub Enterprise Server usar um endereço IP e você configurar o `no_proxy` para contornar o proxy desse endereço, o runner ainda assim falhará ao tentar se conectar.
    Se sua instância GitHub Enterprise Server for acessada usando um endereço IP, e a conexão precisar ignorar o proxy, o executor não conseguirá se conectar, mesmo que esse endereço IP esteja listado em `no_proxy`.

### Configurações de exemplo

!!! note
    Para evitar problemas, é uma boa prática tratar as variáveis de ambiente como com diferenciação de maiúsculas e minúsculas, independentemente do comportamento do sistema operacional e do shell que você está usando.

#### Linux e macOS

Defina variáveis de ambiente de proxy para o executor.

```shell copy
export https_proxy=http://proxy.local:8080
export http_proxy=http://proxy.local:8080
export no_proxy=example.com,localhost,127.0.0.1
```

#### Windows

No Windows, você pode definir configurações de proxy definindo variáveis de ambiente ou usando o [comando netsh](https://learn.microsoft.com/en-us/windows/win32/winhttp/netsh-exe-commands#set-advproxy).
A abordagem netsh se aplica a aplicativos e serviços que dependem da API WinHTTP.

A definição de variáveis de ambiente ainda é necessária para corredores que usam rede privada. Se você também precisa configurar o netsh depende dos aplicativos usados em seus fluxos de trabalho.

```shell copy
netsh winhttp set advproxy setting-scope=machine settings={\"Proxy\":\"proxy.local:8080\",\"ProxyBypass\":\"168.63.129.16;169.254.169.254\",\"AutoconfigUrl\":\"\",\"AutoDetect\":false}
```

Ao configurar isso durante a geração de imagem personalizada, use `setting-scope=machine` para garantir que as configurações de proxy persistam após reinicializações e durante a geração de imagens de VM.

### Tornando as configurações de proxy persistentes

Ao definir essas variáveis de ambiente durante a geração de imagem personalizada, verifique se a configuração persiste entre reinicializações ou recompilações de imagem.

#### Linux e macOS

Escreva as variáveis em `/etc/environment`.

```shell
 echo 'http_proxy=http://proxy.local' >> /etc/environment
```

#### Windows

Defina as variáveis de ambiente em todo o sistema.

```shell copy
[Environment]::SetEnvironmentVariable("http_proxy", "http://proxy.local", "Machine")
```

## Configurando um proxy para executores do Azure

Se o executor estiver hospedado no Azure, seja como um executor auto-hospedado ou um executor maior hospedado no GitHub implantado com rede privada, talvez seja necessário configurar um proxy para permitir a conectividade de saída com os serviços do GitHub, mantendo o isolamento de rede.

Você deve adicionar os IPs de gerenciamento e metadados do Azure à sua `no_proxy` lista para garantir que o executor possa acessar os serviços necessários do Azure. Esses pontos de extremidade permitem que as VMs do Azure recuperem as informações de configuração e identidade necessárias para a operação adequada.

Os dois IPs do Azure são:
* 168.63.129.16 (confira [a visão geral do endereço IP do Azure 168.63.129.16](https://learn.microsoft.com/en-us/azure/virtual-network/what-is-ip-address-168-63-129-16?tabs=linux))
* 169.254.169.254 (consulte o [Serviço de Metadados de Instância do Azure](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service?tabs=linux))

## Usar um arquivo .env para definir a configuração de proxy

!!! note
    O uso de um `.env` arquivo para definir a configuração de proxy não pode ser feito em um executor hospedado pelo GitHub.

Em executores auto-hospedados, você pode definir as configurações de proxy adicionando as variáveis a um `.env` arquivo no diretório do aplicativo executor auto-hospedado (o diretório em que você baixou e desempacotou o software executor). Essa abordagem é útil quando o executor está configurado para ser executado como um serviço em uma conta do sistema. Quando o runner inicia, ele lê as variáveis definidas em `.env` para a configuração do proxy.

### Exemplo de configuração de proxy `.env`

```shell copy
https_proxy=http://proxy.local:8080
no_proxy=example.com,myserver.local:443
```

## Definir configuração de proxy para contêineres Docker

Se você usar ações do contêiner Dock ou contêineres de serviço nos seus fluxos de trabalho, você também deverá configurar o Docker para usar o seu servidor proxy além de definir as variáveis do ambiente acima.

Para obter informações sobre a configuração necessária do Docker, confira [Configurar o Docker para usar um servidor proxy](https://docs.docker.com/network/proxy/) na documentação do Docker.
