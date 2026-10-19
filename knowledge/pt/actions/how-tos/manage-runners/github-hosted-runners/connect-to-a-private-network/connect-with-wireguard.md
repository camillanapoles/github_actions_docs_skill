---
title: Usar o WireGuard para criar uma sobreposição de rede
description: Você pode criar uma rede de sobreposição entre seu executor e um serviço em sua rede privada.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard
captured: '2026-10-19'
section: How tos / Manage runners / Github hosted runners / Connect to a private network
---

# Usar o WireGuard para criar uma sobreposição de rede

_Você pode criar uma rede de sobreposição entre seu executor e um serviço em sua rede privada._

## Usar o WireGuard para criar uma sobreposição de rede

Se você não quiser manter uma infraestrutura separada para um Gateway de API, poderá criar uma rede de sobreposição entre o executor e um serviço em sua rede privada, executando o WireGuard em ambos os locais.

Há várias desvantagens nessa abordagem:

* Para acessar o WireGuard em execução em seu serviço privado, você precisará de um endereço IP conhecido e uma porta que seu fluxo de trabalho possa referenciar: isso pode ser um endereço IP público e uma porta, um mapeamento de porta em um gateway de rede ou um serviço que atualiza dinamicamente o DNS.
* O WireGuard não suporta a passagem NAT por padrão, então você precisará identificar uma maneira de fornecer esse serviço.
* Essa conexão é um para um. Por isso, se você precisar de alta disponibilidade ou alta taxa de transferência, precisará compilar isso em cima do WireGuard.
* Você precisará gerar e armazenar chaves com segurança para o executor e seu serviço privado. O WireGuard usa UDP. Portanto, sua rede deve dar suporte ao tráfego UDP.

Há algumas vantagens também, pois você pode executar o WireGuard em um servidor existente, assim não precisa manter uma infraestrutura separada, e ele tem bom suporte em executores hospedados em GitHub.

## Exemplo: configurar o WireGuard

Este exemplo do fluxo de trabalho configura o WireGuard para se conectar a um serviço privado.

Para este exemplo, a instância do WireGuard em execução na rede privada tem essa configuração:

* Sobreposição de endereço IP de rede do `192.168.1.1`
* Endereço IP público e porta do `1.2.3.4:56789`
* Chave pública `examplepubkey1234...`

A instância do WireGuard no GitHub Actions executor tem esta configuração:

* Sobreposição de endereço IP de rede do `192.168.1.2`
* Armazena a chave privada como um segredo GitHub Actions em `WIREGUARD_PRIVATE_KEY`

```yaml
name: WireGuard example

on:
  workflow_dispatch:

jobs:
  wireguard_example:
    runs-on: ubuntu-latest
    steps:
      - run: sudo apt install wireguard

      - run: echo "${{ secrets.WIREGUARD_PRIVATE_KEY }}" > privatekey

      - run: sudo ip link add dev wg0 type wireguard

      - run: sudo ip address add dev wg0 192.168.1.2 peer 192.168.1.1

      - run: sudo wg set wg0 listen-port 48123 private-key privatekey peer examplepubkey1234... allowed-ips 0.0.0.0/0 endpoint 1.2.3.4:56789

      - run: sudo ip link set up dev wg0

      - run: curl -vvv http://192.168.1.1
```

Para obter mais informações, confira [Início Rápido do WireGuard](https://www.wireguard.com/quickstart/), bem como [Usar segredos em ações do GitHub](../../../write-workflows/choose-what-workflows-do/use-secrets.md) para saber como armazenar chaves com segurança.

### Usar o Tailscale para criar uma sobreposição de rede

Tailscale é um produto comercial criado sobre o WireGuard. Essa opção é muito semelhante ao WireGuard, exceto que o Tailscale é mais uma experiência completa do produto em vez de um componente código aberto.

As desvantagens dele são semelhantes às do WireGuard: a conexão é de um para um. Portanto, talvez seja necessário fazer um trabalho adicional para obter alta disponibilidade ou alta taxa de transferência. Você ainda precisa gerar e armazenar chaves com segurança. O protocolo ainda é UDP. Portanto, sua rede deve dar suporte ao tráfego UDP.

No entanto, há algumas vantagens sobre o WireGuard: a passagem NAT é interna. Por isso, você não precisa expor uma porta à Internet pública. É de longe a mais rápida dessas opções para começar a funcionar, já que o Tailscale fornece um fluxo de trabalho do GitHub Actions com uma única etapa para se conectar à rede de sobreposição.

Para obter mais informações, consulte [Tailscale GitHub Action](https://github.com/tailscale/github-action), bem como [Usar segredos em ações do GitHub](../../../write-workflows/choose-what-workflows-do/use-secrets.md) para saber como armazenar chaves com segurança.
