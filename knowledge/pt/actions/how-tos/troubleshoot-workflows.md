---
title: Solução de problemas de fluxos de trabalho
description: Você pode usar as ferramentas GitHub Actions para depurar seus fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/troubleshoot-workflows
captured: '2026-10-11'
section: How tos
---

# Solução de problemas de fluxos de trabalho { #troubleshooting-workflows }

_Você pode usar as ferramentas GitHub Actions para depurar seus fluxos de trabalho._

## Sugestões iniciais de solução de problemas { #initial-troubleshooting-suggestions }

Há várias maneiras de solucionar problemas de execuções de fluxo de trabalho com falha.

> [!NOTE] Se você estiver em uma GitHub Copilot Free assinatura, isso contará para o limite mensal de mensagens de chat.

### Usando GitHub Copilot { #using-github-copilot }

Para iniciar um chat com GitHub Copilot sobre uma execução com falha de um fluxo de trabalho, você pode:

* Ao lado da verificação com falha na caixa de mesclagem, clique **(kebab-horizontal)** e clique **(copilot) em Explicar erro**.
* Na caixa de mesclagem, clique na verificação com falha. Na parte superior da página de resumo da execução do fluxo de trabalho, clique em **(copilot)Explicar erro**.

Isso abre uma janela de chat com GitHub Copilot, em que fornecerá instruções para resolver o problema.

### Usando logs de execução de fluxo de trabalho { #using-workflow-run-logs }

A execução de cada fluxo de trabalho gera registros de atividade que você pode visualizar, pesquisar e baixar. Para saber mais, confira [Usando registros de execução de fluxo de trabalho](monitor-workflows/use-workflow-run-logs.md).

### Habilitando o log de depuração { #enabling-debug-logging }

Se os logs do fluxo de trabalho não fornecerem detalhes suficientes para diagnosticar o motivo pelo qual um fluxo de trabalho, um trabalho ou uma etapa não está funcionando como esperado, habilite o log de depuração adicional. Para saber mais, confira [Habilitando o log de depuração](monitor-workflows/enable-debug-logging.md).

Se o fluxo de trabalho usar ferramentas ou ações específicas, habilitar suas opções de depuração ou log detalhado poderá ajudar a gerar uma saída mais detalhada para a solução de problemas.
Por exemplo, você pode usar `npm install --verbose` para npm ou `GIT_TRACE=1 GIT_CURL_VERBOSE=1 git ...` para git.

## Como revisar de erros de cobrança { #reviewing-billing-errors }

O uso de ações inclui minutos de executor e armazenamento para [artefatos de fluxo de trabalho](../tutorials/store-and-share-data.md). Para saber mais, confira [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions).

### Como definir um orçamento { #setting-a-budget }

Definir um orçamento do Actions pode ajudar a desbloquear imediatamente os fluxos de trabalho com falha devido a erros de cobrança ou armazenamento. Isso permitirá a cobrança de mais minutos e uso do armazenamento até o valor do orçamento definido. Para saber mais, confira [Definir orçamentos para controlar gastos com produtos limitados](https://docs.github.com/pt/billing/how-tos/set-up-budgets).

## Analisando a atividade com métricas { #reviewing-github-actions-activity-with-metrics }

Para analisar a eficiência e a confiabilidade dos seus fluxos de trabalho usando métricas, confira [Como ver as métricas do GitHub Actions](administer/view-metrics.md).

## Solução de problemas de gatilhos de fluxo de trabalho { #troubleshooting-workflow-triggers }

Primeiro, verifique se o fluxo de trabalho não foi desabilitado manualmente, consulte [Desabilitar e habilitar um fluxo de trabalho](manage-workflow-runs/disable-and-enable-workflows.md). Um fluxo de trabalho desabilitado não responde aos gatilhos.

Você pode examinar o campo `on:` do fluxo de trabalho para entender o que é esperado que dispare o fluxo de trabalho. Para saber mais, confira [Acionando um fluxo de trabalho](write-workflows/choose-when-workflows-run/trigger-a-workflow.md).

Para obter uma lista completa de eventos disponíveis, confira [Eventos que disparam fluxos de trabalho](../reference/workflows-and-actions/events-that-trigger-workflows.md).

### Condições de evento de gatilho { #triggering-event-conditions }

Alguns eventos de gatilho só são executados no branch padrão (ou seja, `issues`, `schedule`). As versões de arquivo de fluxo de trabalho que existem fora do branch padrão não serão disparadas s nesses eventos.

Os fluxos de trabalho não serão executados na atividade `pull_request` se a solicitação de pull tiver um conflito de mesclagem.

Fluxos de trabalho que de outra forma seriam disparados na atividade de `push` ou `pull_request` serão ignorados se a mensagem do commit contiver uma anotação de ignorar. Para saber mais, confira [Ignorar execuções de fluxo de trabalho](manage-workflow-runs/skip-workflow-runs.md).

### Fluxos de trabalho agendados em execução em horários inesperados { #scheduled-workflows-running-at-unexpected-times }

Eventos agendados podem sofrer atrasos durante períodos de alta carga de execuções de GitHub Actions workflow.

Os tempos de carregamento altos incluem o início de cada hora. Se a carga for suficientemente alta o suficiente, alguns trabalhos enfileirados talvez sejam descartados. Para diminuir a probabilidade de atraso, agende o fluxo de trabalho para ser executado em uma parte diferente da hora. Para saber mais, confira [Eventos que disparam fluxos de trabalho](../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).

### Fluxo de trabalho agendado parou de ser executado { #scheduled-workflow-stopped-running }

Um fluxo de trabalho agendado (`cron`) pode parar de ser executado mesmo que ainda esteja habilitado e as execuções manuais ou `workflow_dispatch` ainda funcionam.

Isso pode acontecer quando a conta `actor` associada do fluxo de trabalho é suspensa, excluída ou desprovisionada. Para reiniciá-lo, um usuário com `write` acesso ao repositório pode fazer commit de uma alteração no `cron` agendamento. Consulte [Eventos que disparam fluxos de trabalho](../reference/workflows-and-actions/events-that-trigger-workflows.md#actor-for-scheduled-workflows).

### Filtragem e limites de comparação { #filtering-and-diff-limits }

Eventos específicos permitem filtrar por branch, marca e/ou caminhos que você pode personalizar. A criação da execução do fluxo de trabalho será ignorada se as condições de filtro se aplicarem para filtrar o fluxo de trabalho.

Você pode usar caracteres especiais com filtros. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#filter-pattern-cheat-sheet).

Para filtragem de caminho, a avaliação de diferenças é limitada aos primeiros 3.000 arquivos. Se houver arquivos alterados que não são correspondidos nos primeiros 3.000 arquivos retornados pelo filtro, o fluxo de trabalho não será executado. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../reference/workflows-and-actions/workflow-syntax.md#git-diff-comparisons).

## Solucionar problemas de execução do fluxo de trabalho { #troubleshoot-workflow-execution }

A execução do fluxo de trabalho envolve todos os problemas vistos depois que o fluxo de trabalho foi disparado e uma execução de fluxo de trabalho foi criada.

### Depurando condições de trabalho { #debugging-job-conditions }

Se um trabalho foi ignorado inesperadamente ou executado quando esperava-se que ele fosse ignorado, você poderá exibir a avaliação da expressão para entender o porquê:

1. Clique no trabalho na execução do fluxo de trabalho.
2. Baixe o arquivo de log no menu da tarefa.
3. Abra o arquivo `JOB-NAME/system.txt` .
4. Procure pelas linhas `Evaluating`, `Expanded` e `Result`.

A linha `Expanded` mostra os valores reais de tempo de execução que foram substituídos em sua condição `if`, deixando claro por que a expressão foi avaliada como `true` ou `false`.

Para saber mais, confira [Exibindo logs de expressão de condição de tarefa](monitor-workflows/view-job-condition-logs.md).

### Como cancelar fluxos de trabalho { #canceling-workflows }

Se o cancelamento padrão por meio da [UI](../reference/workflows-and-actions/workflow-cancellation.md) ou da [API](https://docs.github.com/pt/rest/actions/workflow-runs#cancel-a-workflow-run) não for processado conforme o esperado, talvez uma instrução condicional configurada para seus trabalhos de fluxo de trabalho em execução esteja impedindo o cancelamento.

Nesses casos, você pode aproveitar a API para forçar o cancelamento da execução. Para saber mais, confira [Endpoints da API REST para execuções de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#force-cancel-a-workflow-run).

Uma causa comum pode ser usar a `always()`[função de verificação de status](../reference/workflows-and-actions/expressions.md#status-check-functions) que retorna `true`, mesmo em caso de cancelamento. Uma alternativa é usar o inverso da função `cancelled()`, `${{ !cancelled() }}`.

Para saber mais, confira [Usando condições para controlar a execução do trabalho](write-workflows/choose-when-workflows-run/control-jobs-with-conditions.md) e [Cancelar a execução do fluxo de trabalho](manage-workflow-runs/cancel-a-workflow-run.md).

## Como solucionar problemas de executores { #troubleshooting-runners }

### Como definir rótulos de executor { #defining-runner-labels }

Os executores hospedados em GitHub aproveitam [os rótulos predefinidos](../reference/runners/github-hosted-runners.md#standard-github-hosted-runners-for-public-repositories) mantidos por meio do repositório [`actions/runner-images`](https://github.com/actions/runner-images?tab=readme-ov-file#available-images).

É recomendável usar nomes de rótulo exclusivos para executores maiores e auto-hospedados. Se um rótulo corresponder a qualquer um dos rótulos predefinidos, poderá haver problemas de atribuição de executor em que não há garantia em qual opção de executor correspondente o trabalho será executado.

### Executores auto-hospedados { #self-hosted-runners }

Se você usar executores auto-hospedados, você poderá ver a atividade deles e diagnosticar problemas comuns.

Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](manage-runners/self-hosted-runners/monitor-and-troubleshoot.md).

### Endereços IP do executor marcados por scanners de segurança { #runner-ip-addresses-flagged-by-security-scanners }

Os executores hospedados por GitHub usam endereços IP atribuídos dinamicamente pela infraestrutura compartilhada. Esses endereços IP são publicados por meio da API da Meta (por exemplo, as chaves `actions` e `actions_macos`). Para obter mais informações, consulte [Pontos de extremidade da API REST para metadados](https://docs.github.com/pt/rest/meta/meta#get-github-meta-information).

Serviços de inteligência contra ameaças de terceiros, scanners de reputação ip ou fornecedores de firewall podem sinalizar esses endereços IP como "mal-intencionados" ou "suspeitos". Como a infraestrutura subjacente é compartilhada, a atividade de outros usuários da mesma infraestrutura pode influenciar as pontuações de reputação atribuídas a esses endereços.

GitHub não controla listas de reputação de IP de terceiros e não pode comentar sua precisão ou frequência de atualização. Para verificar se um endereço IP pertence a runners hospedados em GitHub, verifique os intervalos de IP retornados pela API Meta.

Se você tiver uma preocupação de segurança com um endereço IP de propriedade Microsoft, denuncie-o ao [Microsoft Security Response Center (MSRC)](https://msrc.microsoft.com/report/).

## Sugestões de solução de problemas de rede { #networking-troubleshooting-suggestions }

Nosso suporte é limitado a problemas de rede que envolvem:

* Suas redes
* Redes externas
* Sistemas de terceiros
* Conectividade com a Internet geral

Para ver o status da plataforma em tempo real de GitHub, consulte [GitHub Status](https://githubstatus.com/).

Para outros problemas relacionados à rede, examine as configurações de rede da sua organização e verifique o status dos serviços de terceiros que você está acessando. Se os problemas persistirem, considere entrar em contato com os administradores de rede para obter mais assistência.

Se você não tiver certeza sobre o problema, entre em contato com Suporte do GitHub. Para obter detalhes sobre como entrar em contato com o suporte, confira [Entrando em contato com o suporte do GitHub](https://docs.github.com/pt/support/contacting-github-support).

### DNS

Os problemas podem ocorrer devido a erros de configuração, resolução ou resolvedor do DNS (Sistema de Nomes de Domínio). Recomendamos examinar os logs disponíveis, a documentação do fornecedor ou consultar os administradores para obter mais assistência.

### Firewalls

As atividades podem ser bloqueadas por firewalls. Se isso ocorrer, pode ser útil examinar os logs disponíveis, a documentação do fornecedor ou consultar os administradores para obter mais assistência.

### Proxies

As atividades podem falhar ao usar um proxy para comunicações. É uma boa prática examinar os logs disponíveis, a documentação do fornecedor ou consultar os administradores para obter assistência adicional.

Confira [Utilizando servidores proxy com um executor](manage-runners/use-proxy-servers.md) para obter informações sobre como configurar o aplicativo executor para utilizar um proxy.

### Sub-redes { #subnets }

É possível encontrar problemas com sub-redes em uso ou sobreposições com uma rede existente, como no provedor de nuvem virtual ou em redes do Docker. Nesses casos, recomendamos examinar sua topologia de rede e sub-redes em uso.

### Certificados { #certificates }

Podem ocorrer problemas de cadeias de certificados autoassinados ou personalizados e repositórios de certificados. Você pode verificar se um certificado em uso não expirou e é confiável no momento. Os certificados podem ser inspecionados com `curl` ou ferramentas semelhantes. Você também pode examinar os logs disponíveis, a documentação do fornecedor ou consultar os administradores para obter assistência adicional.

### Listas de IP { #ip-lists }

Listas de permissão ou negação de IP podem interromper as comunicações esperadas. Se houver um problema, examine os logs disponíveis, a documentação do fornecedor ou consulte os administradores para obter assistência adicional.

Para obter informações sobre os endereços IP de GitHub, como os usados por executores hospedados em GitHub, consulte [Sobre os endereços IP do GitHub](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/about-githubs-ip-addresses).

Endereços IP estáticos estão disponíveis para uso com executores maiores hospedados em GitHub. Confira [Gerenciar executores maiores](manage-runners/larger-runners/manage-larger-runners.md) para obter mais informações.

### Sistemas operacionais e aplicativos de software { #operating-systems-and-software-applications }

Além de firewalls ou proxies, personalizações feitas nos executores hospedados em GitHub, como a instalação de pacotes de software adicionais, podem causar interrupções na comunicação. Para obter informações sobre as opções de personalização disponíveis, confira [Personalizando executores hospedados no GitHub](manage-runners/github-hosted-runners/customize-runners.md).

* Para executores auto-hospedados, saiba mais sobre os pontos de extremidade necessários em [Referência de executores auto-hospedados](../reference/runners/self-hosted-runners.md).

* Para obter ajuda sobre como configurar o WireGuard, confira [Usar o WireGuard para criar uma sobreposição de rede](manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard.md).

* Para obter detalhes sobre como configurar o OpenID Connect (OIDC), confira [Usando um gateway de API com o OIDC](manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md).

### A rede privada do Azure para executores hospedados em GitHub { #azure-private-networking-for-github-hosted-runners }

Podem surgir problemas com o uso de executores hospedados em GitHub nas configurações das Redes Virtuais do Azure (VNETs) que você configurou.

Para obter conselhos de solução de problemas, consulte [Resolução de problemas nas configurações de rede privada do Azure para runners hospedados pelo GitHub em sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/troubleshooting-azure-private-network-configurations-for-github-hosted-runners-in-your-organization) ou [Solução de problemas nas configurações de rede privada do Azure para runners hospedados no GitHub em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/troubleshooting-azure-private-network-configurations-for-github-hosted-runners-in-your-enterprise) nos GitHub Enterprise Cloud documentos.
