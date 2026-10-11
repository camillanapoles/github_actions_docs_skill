---
title: Gerenciar executores maiores
description: Você pode configurar executor avançados para sua organização ou empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/larger-runners/manage-larger-runners
captured: '2026-10-11'
section: How tos / Manage runners / Larger runners
---

# Gerenciar executores maiores

_Você pode configurar executor avançados para sua organização ou empresa._

## Adicionando um executor avançado a uma organização

Os proprietários da organização podem adicionar um executor avançado a uma organização e controlar quais repositórios podem usá-lo. Quando você cria um novo executor para uma organização, por padrão, todos os repositórios na organização têm acesso ao executor. Para limitar quais repositórios podem usar o executor, atribua-o a um grupo de executores com acesso a repositórios específicos. Para obter mais informações, consulte [Como permitir que repositórios acessem executores avançados](#allowing-repositories-to-access-larger-runners).

Você pode escolher um sistema operacional e uma configuração de hardware na lista de opções disponíveis. Quando novas instâncias desse executor forem implantadas por meio do dimensionamento automático, elas usarão o mesmo sistema operacional e a mesma configuração de hardware que você definiu aqui.

Novos executores são atribuídos automaticamente ao grupo padrão, ou você pode escolher em qual grupo os executores devem ingressar durante o processo de criação dos executores. Além disso, você pode modificar a associação ao grupo do executor depois de registrá-lo. Para saber mais, confira [Como controlar o acesso a executores maiores](control-access.md).

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.

4. Clique em **New runner** e clique em **(mark-github) New GitHub-hosted runner**.

5. Preencha os detalhes obrigatórios para configurar seu novo executor:

   * **Nome:** insira um nome para seu novo executor. Para facilitar a identificação, esse campo deve indicar o hardware e configuração operacional, como `ubuntu-24.04-16core`.

   * **Plataforma:** escolha uma plataforma entre as opções disponíveis. Depois de selecionar uma plataforma, você poderá escolher uma imagem específica.

     Se você estiver criando uma imagem personalizada, a plataforma selecionada para o executor deve ser compatível com a plataforma da imagem que você deseja criar. A plataforma do executor pode ser uma das seguintes:

     * Linux x64
     * Linux ARM64
     * Windows x64

   * **Imagem:** escolha uma imagem entre as opções disponíveis. Depois de selecionar uma imagem, você poderá escolher um tamanho específico.
     * **Propriedade do GitHub:** para imagens gerenciadas pelo GitHub, selecione uma imagem nesta guia.
     * **Parceiro:** para imagens gerenciadas por um parceiro, selecione uma imagem nesta guia. Por exemplo: as imagens de Windows 11 para desktop, otimizadas para GPU e arm64 estão localizadas nessa guia.
     * **Personalizado:** Para imagens criadas por sua organização ou empresa, selecione uma imagem nesta aba. As imagens personalizadas são criadas executando um fluxo de trabalho em um executor de criação de imagens que você, sua organização ou sua empresa configurou. Para obter mais informações, consulte [Instalando imagens personalizadas](use-custom-images.md#installing-custom-images).

   * **Tamanho:** escolha uma configuração de hardware na lista de opções disponíveis. Os tamanhos disponíveis dependem da imagem selecionada em uma etapa anterior. Para executores de GPU, selecione um tamanho na guia **baseados em GPU**.

   * **Simultaneidade máxima:** escolha o número máximo de trabalhos que podem estar ativos a qualquer momento.

   * **Grupo de executores:** escolha o grupo do qual seu executor será membro. Esse grupo hospedará várias instâncias do seu executor, à medida que elas escalarem verticalmente para atender à demanda.

!!! note

   > Os nomes de executores avançados podem determinar sua funcionalidade. Por exemplo, para usar uma executor avançado para a instalação padrão de code scanning, o executor deve ser chamado `code-scanning`. Para obter mais informações sobre code scanning com executores avançados, consulte [Configurando executores maiores para configuração padrão](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/configure-larger-runners).

6. Clique em **Criar executor**.

7. Para permitir que os repositórios acessem seus executor avançados, adicione-os à lista de repositórios que podem usá-lo. Para obter mais informações, consulte [Permitir que repositórios acessem executor avançados](#allowing-repositories-to-access-larger-runners).

## Permitir que repositórios acessem executor avançados

Os repositórios recebem acesso aos executor avançadopor meio de grupos de executores. Os administradores da empresa podem escolher quais organizações recebem acesso a grupos de executores em nível empresarial, e os proprietários da organização controlam o acesso em nível de repositório a todos os executor avançado.

Os proprietários da organização podem usar e configurar grupos de executores de nível empresarial para os repositórios em sua organização ou podem criar grupos de executores no nível da organização para controlar o acesso.

* \*\*Para grupos de runners de nível empresarial:\*\*Por padrão, os repositórios na organização não têm acesso a grupos de executores de nível empresarial. Para fornecer aos repositórios acesso aos grupos de executores corporativos, os proprietários da organização devem configurar cada grupo de executores corporativos e escolher quais repositórios têm acesso.
* \*\*Para grupos de executores no nível da organização:\*\*Por padrão, todos os repositórios em uma organização recebem acesso aos grupos de executores no nível da organização. Para restringir quais repositórios têm acesso, os proprietários da organização configurar grupos de executores da organização e escolher quais repositórios têm acesso.

Depois que um repositório tiver acesso a executor avançados, os executor avançados poderão ser adicionados aos arquivos de fluxo de trabalho. Para saber mais, confira [Como executar trabalhos em executores maiores](use-larger-runners.md).

1. Acesse a página principal da organização em que os grupos de executores estão localizados.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.
4. Selecione um grupo de executores de qualquer lista na página. Os grupos de executores no nível da organização são listados na parte superior da página e os grupos de executores no nível da empresa são listados em "Compartilhados pela empresa".
5. Na página do grupo de executores, em "Acesso ao repositório", selecione **Todos os repositórios** ou **Repositórios selecionados**. Se você optar por conceder acesso a repositórios específicos, clique (The Settings gear)e selecione os repositórios aos quais deseja conceder acesso na lista.

!!! warning
    Se você estiver usando um intervalo de IP fixo, a recomendação será usar apenas executor avançado com repositórios particulares. Bifurcações do seu repositório podem executar códigos perigosos em seu executor avançado criando uma solicitação de pull que executa o código em um fluxo de trabalho.
    Para saber mais, confira [Como controlar o acesso a executores maiores](control-access.md).

Se você quiser exigir que os fluxos de trabalho sejam direcionados a executores somente por meio de grupos de executores, você pode desativar os executores padrão hospedados em GitHubno nível da organização ou da empresa. Confira [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization) e [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise).

## Alterando o nome de um executor avançado

!!! note
    Os nomes de executores avançados podem determinar sua funcionalidade. Por exemplo, para usar uma executor avançado para a instalação padrão de code scanning, o executor deve ser chamado `code-scanning`. Para obter mais informações sobre code scanning com executores avançados, consulte [Configurando executores maiores para configuração padrão](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/configure-larger-runners).

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista correspondente, selecione o executor que você deseja editar.
5. Insira um nome para o executor no campo de texto "Nome".
6. Clique em **Save** (Salvar).

## Alterando o tamanho de um executor avançado

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista correspondente, selecione o executor que você deseja editar.
5. Escolha um novo tamanho para o executor na lista de opções disponíveis em “Size”. Os tamanhos disponíveis dependem da imagem instalada no executor.
6. Clique em **Save** (Salvar).

## Alterando a imagem de um executor avançado

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista correspondente, selecione o executor que você deseja editar.
5. Escolha uma nova imagem para o executor na lista de opções disponíveis em "Imagem". As imagens disponíveis são limitadas às de propriedade do GitHub.
6. Clique em **Save** (Salvar).

## Configurando o dimensionamento automático para executor avançados

Você pode controlar o número máximo de trabalhos permitidos para execução simultânea para conjuntos de executores específicos. Definir esse campo como um valor mais alto pode ajudar a impedir que os fluxos de trabalho sejam bloqueados devido ao paralelismo.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista correspondente, selecione o executor que você deseja editar.
5. Na seção "Capacidade", em "Simultaneidade máxima", insira o número máximo de trabalhos que você deseja permitir que executem ao mesmo tempo.
6. Clique em **Salvar**.

## Criando endereços IP estáticos para executor avançados

!!! note
    * Para usar endereços IP estáticos, sua organização deve usar GitHub Enterprise Cloud. Para obter mais informações sobre como você pode experimentar o GitHub Enterprise Cloud gratuitamente, confira [Como configurar uma avaliação do GitHub Enterprise Cloud](https://docs.github.com/pt/enterprise-cloud@latest/admin/overview/setting-up-a-trial-of-github-enterprise-cloud).
    * Os macOS executor avançadonão dão suporte a endereços IP estáticos.

Você pode habilitar endereços IP estáticos para executor avançados. Quando você faz isso, os executor avançados recebem intervalos de endereços IP estáticos. Todos os endereços IP no intervalo atribuído são utilizáveis. Por padrão, você pode configurar até 10 executor avançado pools com intervalos de endereços IP estáticos para sua conta. Se você quiser usar mais de 10 pools de executores maiores com intervalos de endereços IP estáticos, entre em contato com nos por meio do portal .

Cada executor avançado que você cria não é uma única máquina. É um pool de executores que é dimensionado automaticamente para lidar com trabalhos simultâneos, até a simultaneidade máxima definida ao criar o executor. Todos os trabalhos no pool compartilham o mesmo intervalo de endereços IP estáticos. Isso significa que um único executor avançado com um intervalo de IP estático pode lidar com muitos trabalhos em execução ao mesmo tempo sem exigir corredores adicionais.

O número de endereços IP disponíveis nos intervalos atribuídos não restringe o número de trabalhos simultâneos. Dentro de um pool de executores, há um balanceador de carga que permite a reutilização alta dos endereços IP nos intervalos atribuídos. Isso garante que seus fluxos de trabalho possam ser executados simultaneamente em escala enquanto cada computador recebe um endereço IP estático.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista correspondente, selecione o executor que você deseja editar.
5. Para atribuir endereços IP estáticos ao executor, em "Rede", marque **Atribuir intervalos de endereços IP público estáticos e exclusivo para esse executor**.
6. Clique em **Save** (Salvar).

## Armazenamento do Azure considerações de firewall

### Máquinas virtuais e contas de armazenamento na mesma região

Se você usar Armazenamento do Azure contas protegidas por regras de rede, lembre-se de que o tráfego de VMs para contas de executor avançadoarmazenamento na mesma região Azure usará endereços IP de Azure privados em vez do executor avançadointervalo de IP público.

Como resultado, Armazenamento do Azure regras de firewall que dependem apenas de listas de permissões de IP público do executor podem não funcionar conforme o esperado. Isso pode causar falhas de conectividade que aparecem como respostas 403 (AuthorizationFailure), com uma mensagem de erro semelhante a:

```text
The request may be blocked by network rules of storage account. Please check network rule set using 'az storage account show -n accountname --query networkRuleSet'.
  If you want to change the default action to apply when no rule matches, please use 'az storage account update'.
```

Para obter mais informações, consulte a documentação Microsoft para [diretrizes e limitações para o firewall de Armazenamento do Azure](https://learn.microsoft.com/en-us/azure/storage/common/storage-network-security-limitations) e configurar a [preferência de roteamento de rede para Armazenamento do Azure](https://learn.microsoft.com/en-us/azure/storage/common/configure-network-routing-preference?tabs=azure-portal\&source=docs).

!!! note
    Não recomendamos configurar Armazenamento do Azure regras de rede de firewall para executor avançados, a menos que você use um ou um `static public IP ranges``Azure VNet`.
    Os intervalos de IP públicos podem ser dinâmicos, portanto, as regras baseadas em lista de permissões podem quebrar e causar falhas de conectividade intermitentes.
    Confira [Referência de executores avançados](../../../reference/runners/larger-runners.md#networking-for-larger-runners)

### Usar intervalos de IP estáticos e pontos de extremidade de serviço

Uma opção para habilitar com segurança as regras de rede da Conta de Armazenamento é usar executores com IPs estáticos e solicitar suporte para configurar Armazenamento do Azure pontos de extremidade de serviço para a rede virtual que hospeda esses IPs estáticos. Consulte [Azure pontos de extremidade de serviço de rede virtual](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-service-endpoints-overview) para obter mais informações.

Entre em contato com GitHub Suporte para configurar essa configuração por meio do [portal de suporte do GitHub](https://support.github.com/).

### Configurar Azure VNET

Outra opção para se conectar com segurança a contas Armazenamento do Azure é habilitar Azure VNET com GitHubexecutores hospedados.

* [Sobre a rede privada do Azure para executores hospedados por GitHub em sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/about-azure-private-networking-for-github-hosted-runners-in-your-organization)
