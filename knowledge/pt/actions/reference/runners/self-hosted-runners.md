---
title: Referência de executores auto-hospedados
description: Encontre informações sobre como configurar e usar executores auto-hospedados.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/runners/self-hosted-runners
captured: '2026-10-11'
section: Reference / Runners
---

# Referência de executores auto-hospedados { #self-hosted-runners-reference }

_Encontre informações sobre como configurar e usar executores auto-hospedados._

## Requisitos para executores auto-hospedados { #requirements-for-self-hosted-runner-machines }

Você pode usar um computador como um executor auto-hospedado, desde que ele atenda a estes requisitos:

* Você pode instalar e executar o aplicativo do executor auto-hospedado na máquina. Confira [Sistemas operacionais com suporte](#supported-operating-systems) e [Arquiteturas de processador com suporte](#supported-processor-architectures).
* O computador pode se comunicar com GitHub Actions.
* A máquina tem recursos de hardware suficientes para o tipo de fluxos de trabalho que você planeja executar. O aplicativo de runner autogerenciado requer apenas recursos mínimos.
* Se você desejar executar fluxos de trabalho que usam ações do contêiner do Docker ou dos contêineres de serviço, você deverá usar uma máquina Linux e o Docker deve estar instalados.

### Sistemas operacionais compatíveis { #supported-operating-systems }

#### Linux

* Red Hat Enterprise Linux 8 ou posterior
* CentOS 8 ou posterior
* Oracle Linux 8 ou posterior
* Fedora 29 ou versão posterior
* Debian 10 ou versão posterior
* Ubuntu 20.04 ou posterior
* Linux Mint 20 ou posterior
* openSUSE 15.2 ou posterior
* SUSE Enterprise Linux (SLES) 15 SP2 ou posterior

#### Windows

* Windows 10 64 bits
* Windows 11 de 64 bits
* Windows Server 2016 de 64 bits
* Windows Server 2019 de 64 bits
* Windows Server 2022 de 64 bits

#### macOS

* macOS 11.0 (Big Sur) ou posterior

### Arquiteturas de processador com suporte { #supported-processor-architectures }

* `x64` – Linux, macOS e Windows.
* `ARM64` – Linux, macOS, Windows (atualmente em prévia pública).
* `ARM32` – Linux.

## Precedência de encaminhamento para executores auto-hospedados { #routing-precedence-for-self-hosted-runners }

Ao rotear um trabalho para um executor auto-hospedado, o GitHub procura um executor que corresponda aos rótulos e grupos `runs-on` do trabalho:

* Se o GitHub encontrar um executor online e ocioso que corresponda aos rótulos e grupos `runs-on` do trabalho, o trabalho será atribuído e enviado ao executor.
  * Se o executor não pegar a tarefa atribuída dentro de 60 segundos, a tarefa será enfileirada novamente para que um novo executor possa aceitá-la.
* Se o GitHub não encontrar um executor online e ocioso que corresponda aos rótulos e grupos `runs-on` do trabalho, o trabalho permanecerá na fila até que um executor fique online.
* Se o trabalho permanecer na fila por mais de 24 horas, o trabalho falhará.

## Dimensionamento automático { #autoscaling }

O dimensionamento automático permite ajustar dinamicamente o número de executores auto-hospedados com base na demanda. Isso ajuda a otimizar a utilização de recursos e garante capacidade de executor suficiente durante os horários de pico, reduzindo os custos durante períodos de baixa atividade. Há várias abordagens para implementar o dimensionamento automático para corredores auto-hospedados, cada uma com diferentes compensações em termos de complexidade, confiabilidade e capacidade de resposta.

### Actions Runner Controller

Os executores hospedados pelo GitHub inerentemente são dimensionados de forma automática com base em suas necessidades.               Os executores hospedados pelo GitHub podem ser uma alternativa econômica e de baixa manutenção para desenvolver ou implementar soluções de dimensionamento automático. Para saber mais, confira [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md).

O Actions Runner Controller (ARC) é a implementação de referência das APIs de conjuntos de dimensionamento do GitHub e a solução baseada em Kubernetes recomendada para executores auto-hospedados de dimensionamento automático. O ARC fornece uma solução completa de dimensionamento automático, pronta para produção, para equipes que executam GitHub Actions em ambientes Kubernetes.

GitHub recomenda o ARC para organizações com infraestrutura do Kubernetes e equipes com experiência no Kubernetes. O ARC gerencia todo o ciclo de vida dos executores em seu cluster, desde o provisionamento até a execução do trabalho, passando pela limpeza.

Para saber mais, confira [Controlador de Ações Runner](../../concepts/runners/actions-runner-controller.md) e [Suporte para o Controlador do Executor de Ações](../../concepts/runners/support-for-arc.md).

### GitHub Actions Cliente do Conjunto de Dimensionamento do Executor { #github-actions-runner-scale-set-client }

O cliente GitHub Actions Runner Scale Set é um módulo autônomo baseado em Go que capacita equipes de plataforma, integradores e provedores de infraestrutura a criar soluções personalizadas de dimensionamento automático para GitHub Actions executores em VMs, contêineres, infraestrutura local e serviços de nuvem, com suporte para plataformas Windows, Linux e macOS.

O cliente orquestra interações de API do GitHub para conjuntos de dimensionamento, deixando o provisionamento da infraestrutura para você. Você define como os executores são criados, dimensionados e destruídos e configura os executores com vários rótulos para roteamento e direcionamento de trabalho flexíveis. Isso oferece às organizações um controle mais detalhado sobre o gerenciamento do ciclo de vida dos runners e fornece telemetria em tempo real para a execução das tarefas.

O cliente foi projetado para trabalhar fora da caixa com configurações básicas, permitindo que as equipes implementem rapidamente o dimensionamento automático. No entanto, seu verdadeiro poder está em sua flexibilidade: o cliente é criado para ser estendido e personalizado para atender aos requisitos de infraestrutura, restrições de conformidade e fluxos de trabalho operacionais específicos de cada organização. Se você precisar de lógica de dimensionamento simples ou estratégias complexas de provisionamento de vários ambientes, o cliente se adaptará às suas necessidades.

O GitHub Actions Runner Scale Set Client é um projeto código aberto. O [repositório actions/scaleset](https://github.com/actions/scaleset) contém o código-fonte completo, documentação abrangente e exemplos práticos para ajudá-lo a começar. Você encontrará guias de implementação, configurações de exemplo para vários cenários de infraestrutura e arquiteturas de referência que demonstram como integrar o cliente a diferentes sistemas de provisionamento. O repositório também inclui diretrizes de contribuição para equipes interessadas em estender o cliente ou compartilhar seus padrões de dimensionamento automático com a comunidade.

> **Nota:** o Cliente do Conjunto de Dimensionamento do Executor não substitui o Actions Runner Controller (ARC), que continua sendo a implementação de referência das APIs de conjunto de dimensionamento e a solução recomendada do Kubernetes para executores de escalonamento automático. Em vez disso, o cliente é uma ferramenta complementar para interface com as mesmas APIs de conjunto de escalas para criar soluções de escalonamento automático personalizadas fora do Kubernetes.

### Executores efêmeros para dimensionamento automático { #ephemeral-runners-for-autoscaling }

O GitHub recomenda a implementação do escalonamento automático com executores auto-hospedados efêmeros; o escalonamento automático com executores auto-hospedados persistentes não é recomendado. Em determinados casos, GitHub não pode garantir que os trabalhos não sejam atribuídos a executores persistentes enquanto eles são desativados. Com executores efêmeros, isso pode ser garantido porque GitHub atribui apenas um trabalho a um executor.

Esta abordagem permite que você gerencie os seus executores como sistemas efêmeros, já que você pode usar automação para fornecer um ambiente limpo para cada trabalho. Isso ajuda a limitar a exposição de quaisquer recursos sensíveis de trabalhos anteriores e também ajuda a mitigar o risco de um runner comprometido receber novos trabalhos.

> [!WARNING]Os arquivos de log do aplicativo do executor para executores efêmeros devem ser encaminhados para uma solução de armazenamento de logs externo para fins de solução de problemas e diagnóstico. Embora não seja necessário implantar executores efêmeros, o GitHub recomenda que os logs dos executores sejam encaminhados e preservados externamente antes da implantação de uma solução de dimensionamento automático de executores efêmeros em um ambiente de produção. Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](../../how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot.md#reviewing-the-self-hosted-runner-application-log-files).

Para adicionar um executor efêmero ao seu ambiente, inclua o parâmetro `--ephemeral` ao registrar o executor usando `config.sh`. Por exemplo:

```shell
./config.sh --url https://github.com/octo-org --token example-token --ephemeral
```

O serviço GitHub Actions cancelará automaticamente o registro do executor depois que ele processar um trabalho. Em seguida, você poderá criar a sua própria automação que limpa o executor depois que ele tiver seu registro cancelado.

!!! note
    Se um trabalho estiver rotulado para certo tipo de executor, mas nenhuma correspondência desse tipo estiver disponível, o trabalho não falhará imediatamente no momento da colocação na fila. Em vez disso, o trabalho permanecerá na fila até que o período de tempo limite de 24 horas expire.

Como alternativa, você pode criar executores just-in-time efêmeros usando a API REST. Para saber mais, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

### Atualizações de software dos executores em executores auto-hospedados { #runner-software-updates-on-self-hosted-runners }

Por padrão, os executores auto-hospedados realizarão automaticamente uma atualização de software sempre que uma nova versão do executor estiver disponível. Se você usar executores efêmeros em contêineres, isso pode levar a atualizações de software repetidas quando uma nova versão do executor for lançada. A desabilitação das atualizações automáticas permite que você atualize a versão do executor na imagem do contêiner diretamente no seu próprio agendamento.

Para desativar as atualizações automáticas de software e instalar atualizações de software por conta própria, especifique o sinalizador `--disableupdate` ao registrar o executor usando `config.sh`. Por exemplo:

```shell
./config.sh --url https://github.com/YOUR-ORGANIZATION --token EXAMPLE-TOKEN --disableupdate
```

Se você desabilitar as atualizações automáticas, ainda deverá atualizar a versão do seu executor regularmente. Novas funcionalidades no GitHub Actions exigem alterações no serviço GitHub Actions_e\_ no software do executor. O executor pode não ser capaz de processar corretamente trabalhos que aproveitam os novos recursos GitHub Actions sem uma atualização de software.

Se você desabilitar as atualizações automáticas, será necessário atualizar a versão do seu executor no prazo de 30 dias a contar da nova versão disponível. Você pode querer se inscrever para receber notificações de lançamentos no [repositório `actions/runner`](https://github.com/actions/runner/releases). Para saber mais, confira [Configurar notificações](https://docs.github.com/pt/subscriptions-and-notifications/get-started/configuring-notifications#about-custom-notifications).

Para obter instruções sobre como instalar a última versão do executor, confira as instruções de instalação da [última versão](https://github.com/actions/runner/releases).

> [!WARNING] Todas as atualizações lançadas para o software, incluindo versões principais, secundárias ou de patch, são consideradas como uma atualização disponível. Se você não executar uma atualização de software em 30 dias, o serviço do GitHub Actions não colocará trabalhos na fila para o seu executor. Além disso, se uma atualização crítica de segurança for necessária, o serviço de GitHub Actions não colocará os trabalhos na fila do seu executor até que ele seja atualizado.

### Webhooks para dimensionamento automático { #webhooks-for-autoscaling }

Você pode criar seu ambiente de dimensionamento automático usando cargas recebidas do webhook [`workflow_job`](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_job). Esse webhook está disponível nos níveis de repositório, organização e empresa, e a carga útil desse evento contém uma chave `action` que corresponde às fases do ciclo de vida de uma tarefa de workflow; por exemplo, quando as tarefas são `queued`, `in_progress` e `completed`. Você deverá criar a sua própria automação de dimensionamento em resposta a estas cargas de webhook.

* Para saber mais sobre o webhook `workflow_job`, confira [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#workflow_job).
* Para saber como trabalhar com webhooks, confira [Documentação de Webhooks](https://docs.github.com/pt/webhooks).

> **Nota:** Essa abordagem depende da pontualidade da entrega de webhook para tomar decisões de dimensionamento, o que pode introduzir atrasos e preocupações de confiabilidade. Considere usar o Actions Controller ou o Scale Set Client para cenários de escalonamento automático de grande volume.

### Requisitos de autenticação { #authentication-requirements }

Você pode registrar e excluir os executores auto-hospedados do repositório e da organização usando [a API](https://docs.github.com/pt/rest/actions/self-hosted-runners). Para se autenticar na API, sua implementação de dimensionamento automático pode usar um token de acesso ou um GitHub aplicativo.

Seu token de acesso exigirá o seguinte escopo:

* Para repositórios privados, use um token de acesso com o escopo indicado por [`repo`](https://docs.github.com/pt/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).
* Para repositórios públicos, use um token de acesso com o [`public_repo` escopo](https://docs.github.com/pt/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).
* Para organizações, use um token de acesso que possua o escopo [`admin:org`](https://docs.github.com/pt/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps#available-scopes).

Para autenticar usando um GitHub aplicativo, ele deve receber as seguintes permissões:

* Para repositórios, atribua a permissão `administration`.
* Para organizações, atribua a permissão `organization_self_hosted_runners`.

Você pode registrar e excluir os executores auto-hospedados da empresa usando [a API](https://docs.github.com/pt/rest/actions/self-hosted-runners). Para efetuar a autenticação na API, sua implementação de dimensionamento automático pode usar um token de acesso.

Seu token de acesso exigirá o escopo `manage_runners:enterprise`.

## Comunicação { #communication }

Os executores auto-hospedados se conectam ao GitHub para receber atribuições de trabalhos e baixar novas versões do aplicativo do executor.

O aplicativo de executor do GitHub Actions tem código aberto. Você pode contribuir e apresentar problemas no repositório do [executor](https://github.com/actions/runner).
Quando uma nova versão é lançada, o aplicativo executor se atualiza automaticamente quando um trabalho é atribuído ao executor ou dentro de uma semana após o lançamento, se o executor não tiver recebido nenhum trabalho.

### Requisitos para comunicação com GitHub { #requirements-for-communication-with-your-github-enterprise-server-instance }

* O aplicativo do executor auto-hospedado deve estar em execução no computador host para aceitar e executar trabalhos GitHub Actions.
* O computador host deve ter acesso à rede apropriado com pelo menos 70 Kbps de velocidade de upload e download.
* O computador host deve ser capaz de fazer conexões HTTPS de saída pela porta 443.
* Dependendo da função dos fluxos de trabalho atribuídos ao seu executor auto-hospedado, o computador host deve ser capaz de se comunicar com os GitHub domínios listados abaixo.

### Domínios acessíveis por função { #communication-with-githubcom }

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

Além disso, seu fluxo de trabalho pode exigir acesso a outros recursos de rede.

Se você usar uma lista de permissões de endereços IP para a sua organização ou conta corporativa do GitHub, deverá adicionar o endereço IP do executor auto-hospedado à essa lista. Consulte [Gerenciamento de endereços IP permitidos para sua organização](https://docs.github.com/pt/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-allowed-ip-addresses-for-your-organization#using-github-actions-with-an-ip-allow-list) ou [Aplicando políticas para configurações de segurança na sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-security-settings-in-your-enterprise) na GitHub Enterprise Cloud documentação.
