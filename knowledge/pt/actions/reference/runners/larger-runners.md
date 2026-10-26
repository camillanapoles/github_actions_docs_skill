---
title: Referência de executores avançados
description: Encontre informações sobre corredores maiores, incluindo suas especificações e opções de personalização.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/runners/larger-runners
captured: '2026-10-26'
section: Reference / Runners
---

# Referência de executores avançados

_Encontre informações sobre corredores maiores, incluindo suas especificações e opções de personalização._

## Tamanhos de máquina para executores avançados

Você pode escolher entre várias especificações para executores avançados.

### Especificações para geral executores avançados

| CPU | Memória (RAM) | Armazenamento (SSD) | Arquitetura | OS (sistema operacional) |
|---|-------------|-------------------|-----------|------------------------|
| 5   | 14 GB         | 14 GB               | arm64 (M2)  | macOS                    |
| 12  | 30 GB         | 14 GB               | x64 (Intel) | macOS                    |
| 2   | 8 GB          | 75 GB               | X64, ARM64  | Ubuntu                   |
| 4   | 16 GB         | 150 GB              | X64, ARM64  | Ubuntu, Windows          |
| 8   | 32 GB         | 300 GB              | X64, ARM64  | Ubuntu, Windows          |
| 16  | 64 GB         | 600 GB              | X64, ARM64  | Ubuntu, Windows          |
| 32  | 128 GB        | 1.200 GB            | X64, ARM64  | Ubuntu, Windows          |
| 64  | 208 GB        | 2.040 GB            | arm64       | Ubuntu, Windows          |
| 64  | 256 GB        | 2.040 GB            | x64         | Ubuntu, Windows          |
| 96  | 384 GB        | 2.040 GB            | x64         | Ubuntu, Windows          |

> [!NOTE] O executor de 4 vCPUs do Windows só funciona com a imagem base da área de trabalho do Windows 11 ou do Windows Server 2025.

### Especificações para GPU executores avançados

| CPU | GPU | Placa de GPU | Memória (RAM) | Memória da GPU (VRAM) | Armazenamento (SSD) | OS (sistema operacional) |
|---|---|------------|-------------|---------------------|-------------------|------------------------|
| 4   | 1   | Tesla T4     | 28 GB         | 16 GB                 | 176 GB              | Ubuntu, Windows          |

## Imagens do executor

Executor avançadoé executado em VMs (máquinas virtuais) e GitHub instala um VHD (disco rígido virtual) nesta máquina durante o processo de criação da VM. Você pode escolher entre diferentes imagens de VM para instalar em seus executores.

\*\*
GitHubImagens próprias:\*\* essas imagens são mantidas por GitHub e estão disponíveis para executáveis do Linux (x64 e arm64), Windows (x64 e arm64) e macOS (x64 e arm64). Para obter mais informações sobre essas imagens e uma lista completa das ferramentas incluídas para cada sistema operacional do executável, consulte o repositório de [GitHub Actions imagens executáveis](https://github.com/actions/runner-images).

**Partner Images:** As imagens do Parceiro não são gerenciadas por GitHub e são extraídas do Azure Marketplace. Veja abaixo onde encontrar mais informações e relatar problemas sobre imagens de parceiros.

* [Imagem base da área de trabalho do Windows 11](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoftwindowsdesktop.windows-11?tab=Overview).
* [VMI otimizada para GPU NVIDIA](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/nvidia.ngc_azure_17_11)
* [Máquina Virtual de Ciência de Dados – Windows 2019](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/microsoft-dsvm.dsvm-win-2019?tab=overview).

## Disponível para macOS executores avançados e rótulos

Os computadores a seguir estão disponíveis para macOS executores avançados. Quando você cria um macOS executor avançado, o nome do executor também está disponível como um rótulo de fluxo de trabalho que você pode usar com `runs-on`.

| Tamanho do executor | Arquitetura | Processador (CPU) | Memória (RAM) | Armazenamento (SSD) | Etiqueta de fluxo de trabalho |
| --- | --- | --- | --- | --- | --- |
| Grande | Intel | 12 | 30 GB | 14 GB |  |
| `macos-latest-large`, `macos-14-large`( `macos-15-large` mais recente), `macos-26-large` |  |  |  |  |  |
| XLarge | arm64 (M2) | 5 (+ 8 aceleração de hardware GPU) | 14 GB | 14 GB |  |
| `macos-latest-xlarge`, `macos-14-xlarge`( `macos-15-xlarge` mais recente), `macos-26-xlarge`, `xcode-27-xlarge` |  |  |  |  |  |

## Limitações para macOS executores avançados

* Todas as ações fornecidas pelo GitHub são compatíveis com executores arm64 hospedados pelo GitHub. No entanto, as ações da comunidade podem não ser compatíveis com o arm64 e precisam ser instaladas manualmente em tempo de execução.
* Não há suporte para virtualização aninhada devido à limitação da Estrutura de Virtualização da Apple.
* Os recursos de rede, como a rede privada do Azure e a atribuição de IPs estáticos, não estão disponíveis atualmente para corredores maiores do macOS.
* Os executores macOS arm64 não têm um UUID/UDID estático atribuído a eles porque a Apple não suporta esse recurso. No entanto, os executores Intel MacOS recebem um UDID estático, especificamente `4203018E-580F-C1B5-9525-B745CECA79EB`. Caso esteja criando e assinando no mesmo host no qual planeja testar a compilação, você poderá assinar com um [perfil de provisionamento de desenvolvimento](https://developer.apple.com/help/account/provisioning-profiles/create-a-development-provisioning-profile/). Caso precise de um DID estático, você poderá usar os executores Intel e adicionar seu UDID à sua conta de desenvolvedor da Apple.

## Solução de problemas executores avançados

Se você perceber que as tarefas direcionados ao seu sistema executor avançados estão atrasadas ou não estão sendo executadas, há vários fatores que podem estar causando isso.

* **Configurações de simultaneidade**: talvez você tenha atingido o limite máximo de simultaneidade. Para permitir que mais trabalhos sejam executados em paralelo, atualize as configurações de dimensionamento automático para um número maior. Consulte [Gerenciar executores maiores](../../how-tos/manage-runners/larger-runners/manage-larger-runners.md#configuring-autoscaling-for-larger-runners).
* **Permissões de repositório:** Verifique se você tem as permissões de repositório apropriadas habilitadas para seus executor avançados. Por padrão, os executores corporativos não estão disponíveis no nível do repositório e devem ser habilitados manualmente por um administrador da organização. Consulte [Gerenciar executores maiores](../../how-tos/manage-runners/larger-runners/manage-larger-runners.md#allowing-repositories-to-access-larger-runners).
* **Informações de cobrança:** Você deve ter um cartão de crédito válido cadastrado para usar executor avançados. Depois de adicionar um cartão de crédito à sua conta, pode levar até 10 minutos para que o uso de seus executor avançados seja ativado. Consulte [Gerenciar suas informações de pagamento e cobrança](https://docs.github.com/pt/billing/how-tos/set-up-payment/manage-payment-info).
* **Limite de gastos:** Seu GitHub Actions limite de gastos deve ser definido como um valor maior que zero. Consulte [Definir orçamentos para controlar gastos com produtos limitados](https://docs.github.com/pt/billing/how-tos/set-up-budgets).
* \*\*Política de uso justo:\*\*GitHub tem uma política de uso justo que começa a restringir os trabalhos com base em vários fatores, como quantos trabalhos você está executando ou quantos trabalhos estão sendo executados em toda a GitHub Actions.
* **Tempo de atribuição na fila de trabalhos:** O tempo de atribuição na fila de trabalhos refere-se ao intervalo entre uma solicitação de trabalho e GitHub a atribuição de uma VM para executar o trabalho. Executores padrão hospedados em GitHub que utilizam rótulos de fluxo de trabalho em YAML predefinidos (como `ubuntu-latest`) estão sempre em um "estado de prontidão". Com executores avançados, é possível que uma VM quente não esteja pronta para assumir um trabalho na primeira solicitação, pois os pools para essas máquinas são menores. Como resultado, GitHub talvez seja necessário criar uma nova VM, o que aumenta a fila para atribuir tempo. Quando um executor está em uso, as VMs ficam prontas para execuções de fluxo de trabalho subsequentes em 5 minutos. Se não for usado novamente nesse período, um subconjunto dessas máquinas permanecerá quente, reduzindo a fila para atribuir tempo para execuções de fluxo de trabalho futuras nas próximas 24 horas. Quanto maior o volume de trabalhos executados, mais VMs permanecerão no pool quente.

## Rede para executores avançados

Por padrão, executores avançados receba um endereço IP dinâmico que é alterado para cada execução de trabalho. Opcionalmente, os clientes GitHub Enterprise Cloud podem configurar seu executores avançados para receber endereços IP estáticos do pool de endereços IP do GitHub. Para saber mais, confira [Sobre os endereços IP do GitHub](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses).

Quando ativado, as instâncias do executor avançado receberão endereços IP de faixas específicas exclusivas do executor, permitindo que você use essas faixas para configurar uma lista de permissões no firewall. Cada executor avançado é um pool que é escalado automaticamente até sua concorrência máxima configurada, e todos os trabalhos nesse pool compartilham o mesmo intervalo de endereços IP estáticos. Isso significa que você não precisa criar corredores adicionais para executar trabalhos mais simultâneos.
Você pode usar até 10 executor avançado pools com intervalos de endereços IP estáticos no total em todos os seus executores avançados. Para saber mais, confira [Gerenciar executores maiores](../../how-tos/manage-runners/larger-runners/manage-larger-runners.md).

Se você quiser usar mais de 10 pools de executores maiores com intervalos de endereços IP estáticos, entre em contato com nos por meio do portal .

!!! note
    Se os executores não forem usados por mais de 90 dias, os respectivos intervalos de endereços IP serão removidos automaticamente e não poderão ser recuperados.

## Requisitos de comunicação para executor avançados

Um(a) executor avançado deve estabelecer conexões com endpoints de propriedade de GitHub para executar operações essenciais de comunicação. Além disso, seu executor pode exigir acesso a redes adicionais que você especificar ou utilizar dentro de uma ação.

Para garantir a comunicação adequada para executor avançados entre redes dentro de sua configuração, verifique se as comunicações a seguir são permitidas.

!!! note
    Alguns dos domínios listados são configurados por meio de registros `CNAME`. Alguns firewalls podem exigir que você adicione regras de maneira recursiva para todos os registros `CNAME`. Observe que os registros `CNAME` poderão mudar no futuro e que apenas os domínios listados permanecerão constantes.

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
