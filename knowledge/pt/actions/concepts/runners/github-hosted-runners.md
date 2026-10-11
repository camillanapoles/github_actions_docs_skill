---
title: Executores hospedados no GitHub
description: GitHub oferece máquinas virtuais hospedadas para executar fluxos de trabalho. A máquina virtual contém um ambiente de ferramentas, pacotes e configurações disponíveis para GitHub Actions usar.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/github-hosted-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Executores hospedados no GitHub

_GitHub oferece máquinas virtuais hospedadas para executar fluxos de trabalho. A máquina virtual contém um ambiente de ferramentas, pacotes e configurações disponíveis para GitHub Actions usar._

## Visão geral dos executores hospedados em GitHub

Os runners são as máquinas responsáveis por executar trabalhos em um GitHub Actions fluxo de trabalho. Por exemplo, um executor pode clonar seu repositório localmente, instalar software de teste e executar comandos que avaliam seu código.

GitHub fornece corredores que você pode usar para executar seus trabalhos ou pode [hospedar seus próprios corredores](self-hosted-runners.md). Com exceção dos executores de CPU única, cada executor hospedado por GitHub é uma nova máquina virtual (VM) hospedada por GitHub. Processos de CPU única são hospedados em um contêiner em uma VM compartilhada—consulte [Referência de executores hospedados pelo GitHub](../../reference/runners/github-hosted-runners.md#single-cpu-runners).

Cada runner vem com o aplicativo runner e outras ferramentas pré-instaladas.               Os executores hospedados em GitHub estão disponíveis com Ubuntu Linux, Windows ou macOS. Quando você utiliza um executor hospedado em GitHub, a manutenção e as atualizações do computador ficam a cargo do sistema.

Você pode escolher uma das opções de executor hospedado padrão GitHub ou, se estiver no plano GitHub Team ou GitHub Enterprise Cloud, pode provisionar um executor com mais núcleos, ou um executor alimentado por um processador GPU. Esses computadores são chamados de "executor avançado". Para obter mais informações, consulte [Executores avançados](larger-runners.md).

Executores avançados também dá suporte a imagens personalizadas, que permitem criar e gerenciar suas próprias imagens de VM pré-configuradas. Para obter mais informações, consulte [Imagens personalizadas](#custom-images).

O uso de executores hospedados em GitHub requer acesso à rede com pelo menos 70 quilobits por segundo de carregamento e velocidades de download.

## Imagens do executor

GitHub mantém nosso próprio conjunto de imagens de VM para nossos executores hospedados padrão. A lista de imagens e suas ferramentas incluídas são gerenciadas no repositório [`actions/runner-images`](https://github.com/actions/runner-images).

### Software pré-instalado para imagens de propriedade do GitHub

As ferramentas de software incluídas em nossas imagens de propriedade do GitHub são atualizadas semanalmente. O processo de atualização leva vários dias, e a lista de programas de software pré-instalados no branch `main` é atualizada após o término de toda a implantação.

Os registros de fluxo de trabalho incluem um link para as ferramentas pré-instaladas no executor exato. Para encontrar essas informações no log de fluxo de trabalho, expanda a seção `Set up job`. Nessa seção, expanda a seção `Runner Image`. O link depois de `Included Software` descreverá as ferramentas pré-instaladas no executor que executou o fluxo de trabalho.

Para saber mais, confira [Visualizar o histórico de execução do fluxo de trabalho](../../how-tos/monitor-workflows/view-workflow-run-history.md).

Os executores hospedados em GitHub incluem as ferramentas padrão internas do sistema operacional, além dos pacotes listados nas referências mencionadas acima. Por exemplo, os executores do Ubuntu e do macOS incluem `grep`, `find` e `which`, entre outras ferramentas padrão.

Você também pode exibir uma SBOM (lista de materiais de software) para cada build das imagens de executor do Windows e do Ubuntu. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#reviewing-the-supply-chain-for-github-hosted-runners).

Recomendamos usar ações para interagir com o software instalado nos executores. Essa abordagem tem vários benefícios:

* Normalmente, as ações fornecem funcionalidades mais flexíveis, como seleção de versões, capacidade de passar argumentos e parâmetros
* Ela garante que as versões da ferramenta usadas no seu fluxo de trabalho permaneçam as mesmas independentemente das atualizações do software

Se houver uma ferramenta que você deseja solicitar, abra um problema em [actions/runner-images](https://github.com/actions/runner-images). Este repositório também contém anúncios sobre todas as principais atualizações de software nos executores.

> \[!NOTE]
>
> * Você também pode instalar software adicional em executores hospedados em GitHub. Confira [Personalizando executores hospedados no GitHub](../../how-tos/manage-runners/github-hosted-runners/customize-runners.md).
> * Embora a virtualização aninhada seja tecnicamente possível ao usar runners, ela não é oficialmente compatível. Qualquer uso de VMs aninhadas é experimental e feito por sua conta e risco, não oferecemos garantias sobre estabilidade, desempenho ou compatibilidade.

### Imagens personalizadas

As imagens personalizadas permitem que você comece com uma GitHubimagem base fornecida e crie sua própria imagem de VM personalizada de acordo com suas necessidades de fluxo de trabalho. Com imagens personalizadas, você pode:

* Crie imagens de VM personalizadas usando a sintaxe YAML do fluxo de trabalho existente.
* Pré-configurar ambientes com ferramentas, patches de segurança e dependências aprovados antes do início dos fluxos de trabalho.
* Crie ambientes base consistentes e validados em todos os builds.

As imagens personalizadas podem incluir código de repositório, imagens de contêiner, binários, certificados e outras dependências para criar um ambiente de build consistente entre fluxos de trabalho. Isso ajuda você a obter controle sobre sua cadeia de suprimentos. Eles ajudam a reduzir o tempo de instalação, melhorar o desempenho do build e fortalecer a segurança reduzindo o vetor de ataque de superfície em suas imagens. Os administradores também podem aplicar políticas para gerenciar versões de imagem, retenção e idade para atender aos requisitos de conformidade e segurança organizacional.

As imagens personalizadas só podem ser usadas com executores avançados. Os trabalhos que utilizam imagens personalizadas são cobrados pelas mesmas tarifas por minuto que esses executores. O armazenamento de imagens personalizadas é tarifado e medido através do armazenamento de GitHub Actions. Para saber mais, confira [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions#custom-image-storage).

Para começar a usar imagens personalizadas, consulte [Usando imagens personalizadas](../../how-tos/manage-runners/larger-runners/use-custom-images.md).

## Hosts de nuvem usados por executores hospedados em GitHub

GitHub hospeda executores Linux e Windows em máquinas virtuais em Microsoft Azure com o aplicativo de executor do GitHub Actions instalado. O aplicativo de executor hospedado em GitHub é uma ramificação do Agente do Azure Pipelines. Os pacotes ICMP de entrada estão bloqueados para todas as máquinas virtuais do Azure. Portanto, é possível que os comandos ping ou traceroute não funcionem.
GitHub hospeda corredores macOS em data centers Azure.

## Continuidade do fluxo de trabalho

Se os serviços de GitHub Actions estiverem temporariamente indisponíveis, a execução do fluxo de trabalho será descartada se não tiver sido enfileirada em 30 minutos após ser acionada. Por exemplo, se um fluxo de trabalho for acionado e os serviços de GitHub Actions não estiverem disponíveis por 31 minutos ou mais, a execução do fluxo de trabalho não será processada.

Além disso, se a execução do fluxo de trabalho entrar na fila com sucesso, mas não foi processado por um executor hospedado em GitHub dentro de 45 minutos, a execução do fluxo de trabalho na fila será descartada.

## O arquivo `etc/hosts`

Os executores hospedados pelo GitHub são provisionados com um arquivo `etc/hosts` que bloqueia o acesso à rede a vários pools de mineração de criptomoedas e sites mal-intencionados. Hosts como MiningMadness.com e cpu-pool.com são redirecionados para localhost para que não apresentem um risco de segurança significativo.
