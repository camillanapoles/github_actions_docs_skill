---
title: Executores avançados
description: Organize e governe seus fluxos de trabalho com executores maiores hospedados em GitHub usando grupos de executores, políticas de concorrência e controles de acesso granulares.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/larger-runners
captured: '2026-10-26'
section: Concepts / Runners
---

# Executores avançados

_Organize e governe seus fluxos de trabalho com executores maiores hospedados em GitHub usando grupos de executores, políticas de concorrência e controles de acesso granulares._

## Sobre o executores avançados

Executor avançados são máquinas virtuais gerenciadas com mais recursos do que [executores padrão hospedados em GitHub](../../reference/runners/github-hosted-runners.md#supported-runners-and-hardware-resources). Eles oferecem os seguintes recursos avançados:

* Mais RAM, CPU e espaço em disco
* Endereços IP estáticos
* Azure rede privada
* A capacidade de agrupar executores
* Dimensionamento automático para oferecer suporte a fluxos de trabalho simultâneos
* Runners com GPU

Esses executores avançados são hospedados por GitHub e têm o aplicativo runner e outras ferramentas pré-instaladas.

## O que você pode fazer com corredores maiores

Todos os executores avançados oferecem os seguintes recursos:

* **Grupos de executores**: organize os executores e controle quais repositórios podem usá-los
* **Dimensionamento automático**: aumente ou reduza o número de executores com base na demanda da carga de trabalho
* **Controles de simultaneidade**: limitar quantos trabalhos podem ser executados ao mesmo tempo

Os seguintes recursos estão disponíveis apenas nos executores Linux e Windows:

* **Endereços IP estáticos**: atribua endereços IP estáticos de um intervalo específico a executores, permitindo que você configure listas de permissões de firewall.
* **Imagens personalizadas**: use imagens personalizadas do runner para pré-instalar dependências e reduzir o tempo de configuração.
* **Rede privada do Azure**: Conecte seus runners a redes privadas do Azure.

## Sobre executores avançados para a configuração padrão code scanning

Considere configurar executores avançados para a configuração padrão de code scanning se:

* Suas verificações com executores padrão hospedados em GitHub estão demorando muito.
* Suas varreduras com executores padrão hospedados em GitHub estão retornando erros de memória ou de disco.
* Você deseja personalizar aspectos do seu executor code scanning, como o tamanho do executor, a imagem do executor e a concorrência do trabalho, sem usar executores auto-hospedados.

Para obter mais informações sobre como configurar executores avançados para a configuração padrão de code scanning, consulte [Configurando executores maiores para configuração padrão](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/configure-larger-runners).

## Faturamento

!!! note
    Executor avançados não são elegíveis para o uso de minutos incluídos em repositórios privados. Para repositórios privados e públicos, quando executores avançados forem utilizados, eles sempre serão cobrados à taxa por minuto.

Em comparação com os executores hospedados GitHub padrão, executores avançados são cobrados de forma diferente.
Executor avançado são cobrados somente pela taxa por minuto do tempo em que os fluxos de trabalho são executados neles. Não há nenhum custo associado à criação de um executor avançado que não está sendo usado pelo fluxo de trabalho. Para obter mais informações, consulte [Precificação do executor de ações](https://docs.github.com/pt/billing/reference/actions-runner-pricing).

## Próximas etapas

Para começar a usar executores maiores, consulte [Gerenciar executores maiores](../../how-tos/manage-runners/larger-runners/manage-larger-runners.md).

Para encontrar informações de referência sobre como usar executores avançados, consulte [Referência de executores avançados](../../reference/runners/larger-runners.md).
