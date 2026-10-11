---
title: Migrando de executores auto-hospedados para executores hospedados no GitHub
description: Saiba como avaliar sua infraestrutura atual de CI e migrar fluxos de trabalho de executores auto-hospedados para executores GitHubhospedados.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/tutorials/migrate-to-github-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Migrando de executores auto-hospedados para executores hospedados no GitHub

_Saiba como avaliar sua infraestrutura atual de CI e migrar fluxos de trabalho de executores auto-hospedados para executores GitHubhospedados._

Você pode executar fluxos de trabalho em GitHubexecutores hospedados ou auto-hospedados, ou usar uma combinação de tipos de executores.

Este tutorial mostra como avaliar o uso atual dos executores e, em seguida, migrar os fluxos de trabalho de executores auto-hospedados para executores GitHubhospedados de maneira eficiente.

## 1. Avaliar sua infraestrutura de CI atual

A migração de executores auto-hospedados para GitHubexecutores maiores hospedados começa com uma avaliação minuciosa da sua infraestrutura atual de CI. Ao dedicar tempo para corresponder cuidadosamente às especificações e ambientes, você minimizará o tempo gasto corrigindo problemas ao começar a executar fluxos de trabalho em diferentes executores.

1. Crie um inventário de cada especificação de computador usada para executar fluxos de trabalho, incluindo núcleos de CPU, RAM, armazenamento, arquitetura de chip e sistema operacional.
2. Observe se algum executor faz parte de um grupo de executores ou possui um rótulo. Você pode usar essas informações para simplificar a migração de fluxos de trabalho para novos executores.
3. Documente quaisquer imagens personalizadas e dependências pré-instaladas nas quais os fluxos de trabalho dependem, pois elas influenciarão sua estratégia de migração.
4. Identifique quais workflows atualmente têm como alvo executores auto-hospedados e por quê. Por exemplo, nas GitHub Actions métricas de uso, use a guia **Trabalhos** e filtre por rótulo de executor (como `self-hosted` ou um rótulo personalizado) para ver quais repositórios e trabalhos estão usando esse rótulo. Se você precisar validar arquivos de fluxo de trabalho específicos, também poderá usar a pesquisa de código para encontrar arquivos de fluxo de trabalho que fazem referência `runs-on: self-hosted` ou outros rótulos auto-hospedados.
5. Identifique fluxos de trabalho que acessam recursos de rede privada (por exemplo, registros de pacotes internos, APIs privadas, bancos de dados ou serviços locais), pois eles podem exigir configuração de rede adicional.

## 2. Mapeie seus requisitos de processamento para tipos de runner hospedados em GitHub

GitHub oferece runners gerenciados em vários sistemas operacionais, Linux, Windows e macOS, com opções de máquinas com GPU. Confira [Referência de executores avançados](../reference/runners/larger-runners.md).

1. Mapeie cada especificação distinta de computador em seu inventário para uma especificação de executor GitHubhospedado adequada.
2. Anote todos os executores auto-hospedados para os quais não haja um executor GitHubhospedado adequado.
3. Exclua todos os fluxos de trabalho que devem continuar a ser executados em executores auto-hospedados de seus planos de migração.

## 3. Estimar os requisitos de capacidade

Antes de provisionar runners hospedados em GitHub, estime quanta capacidade de computação seus fluxos de trabalho precisarão. A revisão do uso atual do executor auto-hospedado ajuda você a escolher tamanhos de executor apropriados, definir limites de simultaneidade e prever possíveis alterações de custo.

1. No canto superior direito de GitHub, clique na foto de perfil e clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-organization" aria-label="organization" role="img"><path d="M1.75 16A1.75 1.75 0 0 1 0 14.25V1.75C0 .784.784 0 1.75 0h8.5C11.216 0 12 .784 12 1.75v12.5c0 .085-.006.168-.018.25h2.268a.25.25 0 0 0 .25-.25V8.285a.25.25 0 0 0-.111-.208l-1.055-.703a.749.749 0 1 1 .832-1.248l1.055.703c.487.325.779.871.779 1.456v5.965A1.75 1.75 0 0 1 14.25 16h-3.5a.766.766 0 0 1-.197-.026c-.099.017-.2.026-.303.026h-3a.75.75 0 0 1-.75-.75V14h-1v1.25a.75.75 0 0 1-.75.75Zm-.25-1.75c0 .138.112.25.25.25H4v-1.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 .75.75v1.25h2.25a.25.25 0 0 0 .25-.25V1.75a.25.25 0 0 0-.25-.25h-8.5a.25.25 0 0 0-.25.25ZM3.75 6h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 3.75A.75.75 0 0 1 3.75 3h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 3.75Zm4 3A.75.75 0 0 1 7.75 6h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 7 6.75ZM7.75 3h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5ZM3 9.75A.75.75 0 0 1 3.75 9h.5a.75.75 0 0 1 0 1.5h-.5A.75.75 0 0 1 3 9.75ZM7.75 9h.5a.75.75 0 0 1 0 1.5h-.5a.75.75 0 0 1 0-1.5Z"></path></svg> Your organizations**.

2. Clique no nome da sua organização.

3. No nome da organização, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-graph" aria-label="graph" role="img"><path d="M1.5 1.75V13.5h13.75a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1-.75-.75V1.75a.75.75 0 0 1 1.5 0Zm14.28 2.53-5.25 5.25a.75.75 0 0 1-1.06 0L7 7.06 4.28 9.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.25-3.25a.75.75 0 0 1 1.06 0L10 7.94l4.72-4.72a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg> Insights**.

   ![Captura de tela da barra de navegação horizontal para uma organização. Uma guia, rotulada com um ícone de grafo e "Insights" tem um contorno laranja escuro.](/assets/images/help/organizations/org-nav-insights-tab.png)

4. No menu de navegação "Insights", clique em **Métricas de Uso de Ações**.

5. Selecione a guia que contém as métricas que deseja ver. Confira [Sobre as métricas do GitHub Actions](../concepts/metrics.md).

6. Revise os seguintes pontos de dados para estimar a capacidade do executor hospedado:

   * **Total de minutos consumidos**: ajuda você a estimar a demanda de computação de linha de base.
   * **Número de execuções de fluxo de trabalho**: identifica os horários de pico de atividade que podem exigir mais simultaneidade.
   * **Distribuição de trabalho entre tipos de sistema** operacional: garante que você provisione a combinação certa de executores linux, Windows e macOS.
   * **Rótulos de executor (guia Trabalhos)**: filtre por um rótulo de executor para entender onde um rótulo é usado.

7. Converta suas descobertas em um plano de capacidade:

   * Ajuste fluxos de trabalho de alto uso a executores de tamanhos maiores, quando apropriado.
   * Identifique fluxos de trabalho que podem se beneficiar de imagens pré-criadas ou personalizadas para reduzir o runtime.
   * Estimar simultaneidade determinando quantos trabalhos normalmente são executados simultaneamente.

8. Anote todas as lacunas:

   * Fluxos de trabalho com dependências críticas que suas imagens atuais de executores hospedados não suportam.
   * Trabalhos com tempos de execução extraordinariamente longos ou necessidades de ambiente sob medida. (Talvez você precise de imagens personalizadas para elas.)

Seu plano de capacidade orientará quantos executores provisionar, quais tipos de computador usar e como configurar grupos de executores e políticas nas próximas etapas.

## 4. Configurar grupos de executores e políticas

Depois de estimar suas necessidades de capacidade, configure os grupos de executores e as políticas de acesso para que seus executores GitHubhospedados estejam disponíveis para as organizações e fluxos de trabalho corretos.

Configurar grupos de executores antes de provisionar executores ajuda a garantir que a migração não abra acidentalmente o acesso muito amplamente ou crie aumentos de custos inesperados.

1. Crie grupos de executores no nível da empresa para definir quem pode usar seus executores hospedados. Confira [Como controlar o acesso a executores maiores](../how-tos/manage-runners/larger-runners/control-access.md#creating-a-runner-group-for-an-enterprise).

   Use grupos de executores para definir o escopo do acesso por organização, repositório ou fluxo de trabalho. Se você estiver migrando de executores auto-hospedados, reutilize nomes ou etiquetas de grupos de executores existentes sempre que possível. Isso permite que os fluxos de trabalho continuem funcionando sem alterações quando você muda para runners hospedados em GitHub.

2. Adicione novos executores GitHubhospedados ao grupo apropriado e defina limites de simultaneidade com base nos padrões de uso identificados na etapa 3. Para obter detalhes sobre o dimensionamento automático, consulte [Gerenciar executores maiores](../how-tos/manage-runners/larger-runners/manage-larger-runners.md#configuring-autoscaling-for-larger-runners).

3. Examine as configurações de política para garantir que os executores sejam usados apenas pelos fluxos de trabalho pretendidos. Por exemplo, restringir o uso a repositórios específicos ou impedir que fluxos de trabalho não confiáveis acessem tipos de computador mais poderosos.

## 5. Configurar executores GitHubhospedados

Em seguida, configure seus executores GitHubhospedados com base nos tipos de computador e na capacidade que você identificou anteriormente.

1. Escolha o tamanho do computador e o sistema operacional que correspondem aos seus requisitos de fluxo de trabalho. Para obter imagens e especificações disponíveis, consulte [Referência de executores avançados](../reference/runners/larger-runners.md#runner-images).

2. Atribua cada executor a um grupo de executores e configure limites de simultaneidade para controlar quantos trabalhos podem ser executados ao mesmo tempo.

3. Selecione um tipo de imagem:

   * Use imagens gerenciadas por GitHub para um ambiente mantido e atualizado com frequência.
   * Use imagens personalizadas quando precisar de dependências pré-instaladas para reduzir o tempo de instalação. Confira [Usando imagens personalizadas](../how-tos/manage-runners/larger-runners/use-custom-images.md).

4. Aplique as personalizações necessárias, como variáveis de ambiente, instalação de software ou scripts de inicialização. Para obter mais exemplos, consulte [Personalizando executores hospedados no GitHub](../how-tos/manage-runners/github-hosted-runners/customize-runners.md).

5. Opcionalmente, configure a rede privada se os executores precisarem acessar recursos internos. Confira [Rede privada com executores hospedados pelo GitHub](../concepts/runners/private-networking.md).

### Configurar opções de conectividade privada

Se os fluxos de trabalho precisarem de acesso a recursos privados (por exemplo, registros de pacote internos, APIs privadas, bancos de dados ou serviços locais), escolha uma abordagem que atenda aos requisitos de rede e segurança.

#### Configurar a Rede Privada do Azure

Execute executores GitHubhospedados dentro de uma Rede Virtual do Azure (VNET) para obter acesso seguro aos recursos internos.

1. Crie uma Rede Virtual do Azure (VNET) e configure sub-redes e grupos de segurança de rede para os seus executores.
2. Habilite a rede privada do Azure para o seu grupo de runners. Confira [Configurando a rede privada para executores hospedados por GitHub em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/configuring-private-networking-for-github-hosted-runners-in-your-enterprise#1-add-a-new-network-configuration-for-your-enterprise)
3. Aplique a configuração de rede, como NSGs e regras de firewall, para controlar o tráfego de entrada e saída.
4. Atualize o direcionamento do fluxo de trabalho para usar o grupo de executores configurado para rede privada.

Para obter instruções detalhadas, consulte:

* [Configurando rede privada para executores hospedados no GitHub na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/configuring-private-networking-for-github-hosted-runners-in-your-organization)
* [Configurando a rede privada para executores hospedados por GitHub em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/configuring-settings/configuring-private-networking-for-hosted-compute-products/configuring-private-networking-for-github-hosted-runners-in-your-enterprise)

#### Conectar usando uma rede de sobreposição WireGuard

Se a rede privada do Azure não for aplicável (por exemplo, como sua rede de destino é local ou em outra nuvem), você pode usar uma sobreposição VPN, como o WireGuard, para fornecer acesso em nível de rede a recursos privados.

Para obter instruções e exemplos detalhados, consulte [Usar o WireGuard para criar uma sobreposição de rede](../how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard.md).

#### Usar o OIDC com um gateway de API para acesso confiável a recursos privados

Se você não precisar que o runner entre na sua rede privada, poderá usar o OIDC para estabelecer acesso confiável e temporário a um serviço exposto por meio de um gateway de API. Essa abordagem pode reduzir a necessidade de segredos de longa duração e limita o acesso à rede aos pontos de extremidade específicos que seu fluxo de trabalho precisa.

Para obter instruções e exemplos detalhados, consulte [Usando um gateway de API com o OIDC](../how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md).

## 6. Atualizar fluxos de trabalho para usar os novos executores

Depois que seus executores GitHubhospedados estiverem configurados, atualize seus arquivos de fluxo de trabalho para direcioná-los a esses executores.

1. Reutilize rótulos existentes se você atribuiu seus novos executores aos mesmos nomes de grupo de executores usados por seus executores auto-hospedados. Nesse caso, os fluxos de trabalho usarão automaticamente os novos executores sem alterações.

2. Se você criou novos grupos de executores ou rótulos, atualize o campo de execuções em seus arquivos YAML de fluxo de trabalho. Por exemplo:

            ```yaml
   jobs:
     build:
       runs-on: [github-larger-runner, linux-x64]
       steps:
         - name: Checkout code
           uses: actions/checkout@v6
         - name: Build project
           run: make build
   ```

3. Verifique se há referências fixas a rótulos auto-hospedados (como `self-hosted`, `linux-x64`, ou rótulos personalizados) e substitua-as pelos rótulos de executor GitHubhospedados apropriados.

4. Teste cada fluxo de trabalho atualizado para garantir que ele seja executado corretamente nos novos executores. Monitore quaisquer problemas relacionados a diferenças de ambiente ou dependências ausentes.

## 7. Remover executores auto-hospedados não utilizados

Depois que seus fluxos de trabalho tiverem sido atualizados e testados em executores hospedados em GitHub, remova os executores auto-hospedados que não forem mais necessários. Isso impede que os trabalhos sejam acidentalmente direcionados para a infraestrutura desatualizada. Confira [Remover executores auto-hospedados](../how-tos/manage-runners/self-hosted-runners/remove-runners.md).

Antes de remover os executores auto-hospedados, verifique se você concluiu a migração:

* Nas métricas de uso GitHub Actions, acesse a guia **Tarefas** e filtre por rótulo do executor (por exemplo, `self-hosted` ou seus rótulos personalizados) para confirmar se nenhum repositório ou tarefa ainda está usando executores auto-hospedados.
