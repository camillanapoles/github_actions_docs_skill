---
title: Referência de executores hospedados pelo GitHub
description: Encontre informações sobre executores hospedados em GitHub, incluindo suas especificações e opções de personalização.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/runners/github-hosted-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Referência de executores hospedados pelo GitHub

_Encontre informações sobre executores hospedados em GitHub, incluindo suas especificações e opções de personalização._

## Executores e recursos de hardware suportados

Tipos de executores hospedados em GitHub estão disponíveis para uso em repositórios públicos e privados.

Veja as listas de agentes disponíveis:

* [Executores padrão para repositórios **públicos**](#standard-github-hosted-runners-for-public-repositories)
* [Executores padrão para repositórios **privados**](#standard-github-hosted-runners-for--private-repositories)

GitHubOs executores do Linux hospedados dão suporte à aceleração de hardware para ferramentas do SDK do Android, o que torna a execução de testes do Android muito mais rápida e consome menos minutos. Para obter mais informações sobre a aceleração de hardware do Android, confira [Configurar a aceleração de hardware para o Android Emulator](https://developer.android.com/studio/run/emulator-acceleration) na documentação Desenvolvedores do Android.

> \[!NOTE]
> As imagens do executor `-latest` são as imagens estáveis mais recentes fornecidas pelo GitHub, e podem não ser a versão mais recente do sistema operacional disponível junto ao fornecedor do sistema operacional.

> \[!WARNING]
> As imagens beta e preteridas são fornecidas “no estado em que se encontram”, “com todas as falhas” e “conforme disponível” e são excluídas do contrato de nível de serviço e da garantia. As imagens beta podem não ser cobertas pelo atendimento ao cliente.

### Executores padrão hospedados GitHubpara repositórios públicos

Para repositórios públicos, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados com as especificações associadas.
Com exceção dos executores de CPU única, cada executor hospedado por GitHub é uma nova máquina virtual (VM) hospedada por GitHub. Processos de CPU única são hospedados em um contêiner em uma VM compartilhada—consulte [Referência de executores hospedados pelo GitHub](github-hosted-runners.md#single-cpu-runners). O uso dos executores hospedados padrão GitHubé gratuito e ilimitado em repositórios públicos.

<table style="width:100%">
  <thead>
    <tr>
      <th scope="col">
<b>Máquina virtual/contêiner</b></th>
      <th scope="col">
<b>Processador (CPU)</b></th>
      <th scope="col">
<b>Memória (RAM)</b></th>
      <th scope="col">
<b>Armazenamento (SSD)</b></th>
      <th scope="col">
<b>Arquitetura</b></th>
      <th scope="col">
<b>Rótulo do fluxo de trabalho</b></th>
    </tr>
  </thead>
  <tbody>
    <tr>
          <td>Linux</td>
          <td>1</td>
          <td>5 GB</td>
          <td>14 GB</td>
          <td> x64 </td>
          <td>
            <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md">ubuntu-slim</a></code>
          </td>
        </tr>
    <tr>
      <td>Linux</td>
      <td>4</td>
      <td>16 GB</td>
      <td>14 GB</td>
      <td> x64 </td>
      <td>

```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-VS2026-Readme.md">windows-2025-vs2026</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>4</td>
  <td>16 GB</td>
  <td>14 GB</td>
  <td>arm64</td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-VS2026-Arm64-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

  </tbody>

</table>

### Executores hospedados padrão GitHubpara  privados

Para  privados, os trabalhos que usam os rótulos de fluxo de trabalho mostrados na tabela abaixo serão executados em máquinas virtuais com as especificações associadas. Esses executores usam a alocação de minutos gratuitos da sua GitHub conta e, posteriormente, são cobrados a taxas por minuto de uso. Confira [Precificação do executor de ações](https://docs.github.com/pt/billing/reference/actions-runner-pricing).

<table style="width:100%">
  <thead>
    <tr>
      <th scope="col">
<b>Máquina virtual</b></th>
      <th scope="col">
<b>Processador (CPU)</b></th>
      <th scope="col">
<b>Memória (RAM)</b></th>
      <th scope="col">
<b>Armazenamento (SSD)</b></th>
      <th scope="col">
<b>Arquitetura</b></th>
      <th scope="col">
<b>Rótulo do fluxo de trabalho</b></th>
    </tr>
  </thead>
  <tbody>
    <tr>
          <td>Linux</td>
          <td>1</td>
          <td>5 GB</td>
          <td>14 GB</td>
          <td> x64 </td>
          <td>
            <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md">ubuntu-slim</a></code>
          </td>
        </tr>
    <tr>
      <td>Linux</td>
      <td>2</td>
      <td>8 GB</td>
      <td>14 GB</td>
      <td> x64 </td>
      <td>

```
    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Readme.md">ubuntu-24.04</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Readme.md">ubuntu-22.04</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Readme.md">ubuntu-26.04</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> x64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-latest</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md">windows-2025</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows2022-Readme.md">windows-2022</a></code></td>
</tr>
<tr>
  <td>Linux</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2404-Arm64-Readme.md">ubuntu-24.04-arm</a></code>, , <code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2204-Arm64-Readme.md">ubuntu-22.04-arm</a></code><code><a href="https://github.com/actions/runner-images/blob/main/images/ubuntu/Ubuntu2604-Arm64-Readme.md">ubuntu-26.04-arm</a></code></td>
</tr>
<tr>
  <td>Windows</td>
  <td>2</td>
  <td>8 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-Readme.md">windows-11-arm</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/windows/Windows11-Arm64-VS2026-Readme.md">windows-11-vs2026-arm</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>4</td>
  <td>14 GB</td>
  <td>14 GB</td>
  <td> Intel </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-Readme.md">macos-15-intel</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-Readme.md">macos-26-intel</a></code></td>
</tr>
<tr>
  <td>macOS</td>
  <td>3 (M1)</td>
  <td>7 GB</td>
  <td>14 GB</td>
  <td> arm64 </td>
  <td>

    <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-latest</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-14-arm64-Readme.md">macos-14</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-15-arm64-Readme.md">macos-15</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md">macos-26</a></code>, <code><a href="https://github.com/actions/runner-images/blob/main/images/macos/xcode-27-arm64-Readme.md">xcode-27</a></code> (Versão preliminar pública) </td>
</tr>
```

  </tbody>
</table>

Os registros do fluxo de trabalho listam o executor usado para rodar uma tarefa. Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).

### Limitações dos executores macOS arm64

* Todas as ações fornecidas pelo GitHub são compatíveis com executores arm64 hospedados pelo GitHub. No entanto, as ações da comunidade podem não ser compatíveis com o arm64 e precisam ser instaladas manualmente em tempo de execução.
* Não há suporte para virtualização aninhada devido à limitação da Estrutura de Virtualização da Apple.
* Os recursos de rede, como a rede privada do Azure e a atribuição de IPs estáticos, não estão disponíveis atualmente para corredores maiores do macOS.
* Os executores macOS arm64 não têm um UUID/UDID estático atribuído a eles porque a Apple não suporta esse recurso. No entanto, os executores Intel MacOS recebem um UDID estático, especificamente `4203018E-580F-C1B5-9525-B745CECA79EB`. Caso esteja criando e assinando no mesmo host no qual planeja testar a compilação, você poderá assinar com um [perfil de provisionamento de desenvolvimento](https://developer.apple.com/help/account/provisioning-profiles/create-a-development-provisioning-profile/). Caso precise de um DID estático, você poderá usar os executores Intel e adicionar seu UDID à sua conta de desenvolvedor da Apple.

### Agentes de single-CPU

Executores de CPU única hospedados em GitHub estão disponíveis em ambos os repositórios públicos e privados. Esses executores, especificados usando o rótulo de fluxo de trabalho `ubuntu-slim`, oferecem uma opção de menor custo para executar operações leves. Esse tipo de agente é otimizado para tarefas de automação, operações de problemas e tarefas de curta duração. Eles não são adequados para builds típicos de CI/CD pesados.

`ubuntu-slim` os executores executam fluxos de trabalho do Actions no Ubuntu Linux, dentro de um contêiner, em vez de uma instância de VM completa. Quando o trabalho começa, GitHub provisiona automaticamente um novo contêiner para esse trabalho. Todas as etapas no trabalho são executadas no contêiner, permitindo que as etapas nesse trabalho compartilhem informações usando o sistema de arquivos do runner. Quando o trabalho for concluído, o contêiner será desativado automaticamente. Cada contêiner fornece isolamento de nível 2 do hipervisor.

> \[!NOTE]
> O contêiner para agentes `ubuntu-slim` funciona no modo sem privilégios. Isso significa que não há suporte para algumas operações que exigem privilégios elevados, como montar sistemas de arquivos, usar o Docker-in-Docker ou acessar recursos de kernel de baixo nível.

Um conjunto mínimo de ferramentas é instalado na imagem do agente `ubuntu-slim`, apropriado para tarefas leves. Para obter detalhes sobre qual software está instalado na `ubuntu-slim` imagem, consulte o [arquivo README](https://github.com/actions/runner-images/blob/main/images/ubuntu-slim/ubuntu-slim-Readme.md) no `actions/runner-images` repositório.

#### Limites de uso

Executores de CPU única seguem o mesmo modelo de concorrência que outros executores padrão hospedados em GitHub. Confira [Limites do Actions](../limits.md#job-concurrency-limits-for-github-hosted-runners). A concorrência dos agentes é determinada pelo seu plano.

O tempo limite do trabalho para agentes single-CPU é de 15 minutos. Se um trabalho atingir esse limite, ele será terminado e falhará.

### Executor avançados

Executor avançados estão disponíveis para organizações e empresas nos planos GitHub Team e GitHub Enterprise Cloud.

Executor avançados são máquinas virtuais gerenciadas com mais recursos do que [executores padrão hospedados em GitHub](github-hosted-runners.md#supported-runners-and-hardware-resources). Eles oferecem os seguintes recursos avançados:

* Mais RAM, CPU e espaço em disco
* Endereços IP estáticos
* Azure rede privada
* A capacidade de agrupar executores
* Dimensionamento automático para oferecer suporte a fluxos de trabalho simultâneos
* Runners com GPU

Esses executores avançados são hospedados por GitHub e têm o aplicativo runner e outras ferramentas pré-instaladas.

Para saber mais, confira [Usando executores maiores](../../how-tos/manage-runners/larger-runners.md).

## Privilégios administrativos

As máquinas virtuais do Linux e do macOS são executadas sem senha por meio do `sudo`. Quando precisar executar comandos ou instalar ferramentas que exigem mais privilégios do que o usuário atual, use o `sudo` sem precisar fornecer uma senha. Para obter mais informações, confira o [Manual do sudo](https://www.sudo.ws/man/1.8.27/sudo.man.html).

As máquinas virtuais do Windows estão configuradas para ser executadas como administradores com Controle de Conta de Usuário (UAC) desativado. Para obter mais informações, confira [Como funciona o Controle de Conta de Usuário](https://docs.microsoft.com/windows/security/identity-protection/user-account-control/how-user-account-control-works) na documentação do Windows.

## Endereços IP

Para obter uma lista de intervalos de endereços IP que GitHub Actions usa para executores hospedados em GitHub, você pode usar a API REST GitHub. Para obter mais informações, confira a chave `actions` na resposta do endpoint `GET /meta`. Para saber mais, confira [Pontos de extremidade da API REST para metadados](https://docs.github.com/pt/rest/meta/meta#get-github-meta-information).

Os executores do Windows e Ubuntu são hospedados no Azure e, consequentemente, têm as mesmas faixas de endereços IP que os centros de dados do Azure. Os executores do macOS são hospedados na GitHubprópria nuvem do macOS.

Como há muitas faixas de endereços IP para os executores hospedados em GitHub, não recomendamos que você as use como lista de permissões para seus recursos internos. Em vez disso, recomendamos que você use executor avançados com um intervalo de endereços IP estático ou executores auto-hospedados. Para obter mais informações, confira [Usando executores maiores](../../how-tos/manage-runners/larger-runners.md) ou [Executores auto-hospedados](../../concepts/runners/self-hosted-runners.md).

A lista de GitHub Actions endereços IP retornados pela API é atualizada uma vez por semana.

## Requisitos de comunicação para executores hospedados em GitHub

Um executor hospedado em GitHub deve estabelecer conexões com pontos de extremidade pertencentes a GitHub para executar operações essenciais de comunicação. Além disso, seu executor pode exigir acesso a redes adicionais que você especificar ou utilizar dentro de uma ação.

Para garantir a comunicação adequada dos executores hospedados GitHub entre as redes na sua configuração, certifique-se de que as comunicações a seguir sejam permitidas.

> \[!NOTE]
> Alguns dos domínios listados são configurados por meio de registros `CNAME`. Alguns firewalls podem exigir que você adicione regras de maneira recursiva para todos os registros `CNAME`. Observe que os registros `CNAME` poderão mudar no futuro e que apenas os domínios listados permanecerão constantes.

**Necessário para operações essenciais:**

```shell copy
github.com
api.github.com
*.actions.githubusercontent.com
```

**Necessário para baixar as ações:**

```shell copy
codeload.github.com
```

**Necessário para upload e download de resumos de trabalhos, logs, artefatos de fluxo de trabalho e caches:**

```shell copy
results-receiver.actions.githubusercontent.com
*.blob.core.windows.net
```

**Necessário para atualizações de versão do runner:**

```shell copy
objects.githubusercontent.com
objects-origin.githubusercontent.com
github-releases.githubusercontent.com
github-registry-files.githubusercontent.com
```

**Necessário para recuperar tokens OIDC:**

```shell copy
*.actions.githubusercontent.com
```

**Necessário para baixar ou publicar pacotes ou contêineres no GitHub Packages:**

```shell copy
*.pkg.github.com
pkg-containers.githubusercontent.com
ghcr.io
```

**Necessário para Armazenamento de Arquivos Grandes do Git**

```shell copy
github-cloud.githubusercontent.com
github-cloud.s3.amazonaws.com
```

**Necessário para os trabalhos de Dependabot updates**

```shell copy
dependabot-actions.githubapp.com
```

**Necessário para baixar os arquivos da versão:**

```shell copy
release-assets.githubusercontent.com
```

**Necessário para a VNet:**

```shell copy
api.snapcraft.io
*.core.windows.net
```

## Sistemas de arquivos

GitHub executa ações e comandos de shell em diretórios específicos na máquina virtual. Os caminhos dos arquivos nas máquinas virtuais não são estáticos. Use as variáveis de ambiente fornecidas GitHub para construir caminhos de arquivo para os `home`diretórios e `workspace` os `workflow`diretórios.

| Diretório                                                                                            | Variável de ambiente | Descrição                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------- | -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `home`                                                                                               | `HOME`               | Contém dados relacionados ao usuário. Por exemplo, esse diretório pode conter credenciais de uma tentativa de login.                                             |
| `workspace`                                                                                          | `GITHUB_WORKSPACE`   | A execução de ações e comandos do shell acontece neste diretório. Uma ação pode modificar o conteúdo desse diretório, que fica acessível nas ações subsequentes. |
| `workflow/event.json`                                                                                | `GITHUB_EVENT_PATH`  | A carga `POST` do evento de webhook que disparou o fluxo de trabalho.                                                                                            |
| GitHub reescreve isso sempre que uma ação é executada para isolar o conteúdo do arquivo entre ações. |                      |                                                                                                                                                                  |

Para obter uma lista das variáveis de ambiente criadas GitHub para cada fluxo de trabalho, consulte [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

### Sistema de arquivos do contêiner Docker

As ações executadas em contêineres do Docker têm diretórios estáticos no caminho `/github`. No entanto, é altamente recomendável usar as variáveis de ambiente padrão para elaborar caminhos de arquivos em contêineres do Docker.

GitHub reserva o prefixo de caminho `/github` e cria três diretórios para as ações.

* `/github/home`
* `/github/workspace` - **Observação:** o GitHub Actions precisa ser executado pelo usuário padrão do Docker (raiz). Verifique se o Dockerfile não define a instrução `USER`, caso contrário, você não poderá acessar o `GITHUB_WORKSPACE`.
* `/github/workflow`
