---
title: Como controlar o acesso a executores maiores
description: Você pode usar políticas para limitar o acesso a executor avançados que foram adicionados a uma organização ou empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/larger-runners/control-access
captured: '2026-10-13'
section: How tos / Manage runners / Larger runners
---

# Como controlar o acesso a executores maiores

_Você pode usar políticas para limitar o acesso a executor avançados que foram adicionados a uma organização ou empresa._

## Controlar o acesso a executores avançados

!!! note
    Antes que seus fluxos de trabalho possam enviar trabalhos para executor avançados, primeiro você deve configurar permissões para o grupo de executores. Confira as seções a seguir para obter mais informações.

Os grupos de executores são usados para controlar quais repositórios podem executar trabalhos em seus executor avançados. Você deve gerenciar o acesso ao grupo em cada nível da hierarquia de gerenciamento, dependendo de onde você definiu o executor avançado:

* \*\*Corredores no nível da empresa:\*\*Por padrão, os repositórios na organização não têm acesso a grupos de executores de nível empresarial. Para fornecer aos repositórios acesso aos grupos de executores corporativos, os proprietários da organização devem configurar cada grupo de executores corporativos e escolher quais repositórios têm acesso.
* \*\*Corredores no nível da organização:\*\*Por padrão, todos os repositórios em uma organização recebem acesso aos grupos de executores no nível da organização. Para restringir quais repositórios têm acesso, os proprietários da organização configurar grupos de executores da organização e escolher quais repositórios têm acesso.

Por exemplo, o diagrama a seguir tem um grupo de executores chamado `grp-ubuntu-24.04-16core` no nível da empresa. Para que o repositório chamado `octo-repo` possa usar os executores do grupo, você deve primeiro configurar o grupo no nível da empresa para permitir o acesso à organização `octo-org`. Em seguida, você precisará configurar o grupo no nível da organização para permitir o acesso ao `octo-repo`.

![Diagrama mostrando um grupo de executores definido no nível corporativo com uma configuração de organização que permite acesso a dois repositórios.](https://docs.github.com/assets/images/help/actions/hosted-runner-mgmt.png)

## Como criar um grupo de executores para uma organização

!!! warning
    Se você estiver usando um intervalo de IP fixo, a recomendação será usar apenas executor avançado com repositórios particulares. Bifurcações do seu repositório podem executar códigos perigosos em seu executor avançado criando uma solicitação de pull que executa o código em um fluxo de trabalho.

    [!NOTE]
    Ao criar um grupo de executores, você deve escolher uma política que defina quais repositórios de trabalho têm acesso ao grupo de executores. Para alterar quais repositórios e fluxos de trabalho podem acessar o grupo de executores, os proprietários "Gerenciar corredores e grupos de executores" podem definir uma política para a organização. Para saber mais, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](../self-hosted-runners/manage-access.md#changing-which-repositories-can-access-a-runner-group).

Todas as organizações têm um único grupo de runners padrão.
Os proprietários da organização que usam o plano GitHub Team podem criar grupos de executores adicionais no nível da organização.

Se nenhum grupo for especificado durante o processo de registro, os executores serão adicionados automaticamente ao grupo padrão. Mais tarde, você pode mover o runner do grupo padrão para um grupo personalizado.

Para obter informações sobre como criar um grupo de executores com a API REST, confira [Endpoints da API REST para Ações do GitHub](https://docs.github.com/pt/rest/actions#self-hosted-runner-groups).

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.

4. Na seção "Grupos de executores", clique em **Novo grupo de executores**.

5. Digite um nome para o grupo do seu executor.

6. Atribua uma política para acesso ao repositório.

   Você pode configurar um grupo de executores para ser acessível a uma lista específica de repositórios ou a todos os repositórios na organização. Por padrão, somente repositórios privados podem acessar executores em um grupo de executores, mas você pode substituir isso. Essa configuração não poderá ser substituída se você configurar um grupo de executores da organização que tenha sido compartilhado por uma empresa.

7. Clique em **Criar grupo** para criar o grupo e aplicar a política.

## Como alterar quais repositórios podem acessar um grupo de executores

!!! warning
    Se você estiver usando um intervalo de IP fixo, a recomendação será usar apenas executor avançado com repositórios particulares. Bifurcações do seu repositório podem executar códigos perigosos em seu executor avançado criando uma solicitação de pull que executa o código em um fluxo de trabalho.

Para grupos de executores em uma organização, você pode alterar quais repositórios na organização podem acessar um grupo de executores.

1. Acesse a página principal da organização em que os grupos de executores estão localizados.

2. Clique em **(gear) Settings**.

3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.

4. Na lista de grupos, clique no grupo de executores que deseja configurar.

5. Em “Acesso ao repositório”, use o menu suspenso para clicar em **Repositórios selecionados**.
   1. À direita do menu suspenso, clique em (The Gear icon).
   2. Na janela pop-up, use as caixas de seleção para selecionar os repositórios que podem acessar esse grupo de executores.

6. Clique em **Salvar grupo**.

## Configurar o acesso à rede privada para executores maiores

Você pode usar executores hospedados no GitHub em uma VNET do Azure. Isso permite usar a infraestrutura gerenciada pela GitHub para CI/CD e, ao mesmo tempo, fornece controle total sobre as políticas de rede dos seus executores. Para obter mais informações sobre VNETs do Azure, consulte [O que é uma Rede Virtual do Azure?](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview), na documentação do Azure.

Se você configurou sua organização para se conectar a uma VNET Azure, poderá conceder aos grupos executores acesso à rede virtual. Para saber mais, confira [Rede privada com executores hospedados pelo GitHub](../../../concepts/runners/private-networking.md#using-an-azure-virtual-network-vnet).

Não é possível atribuir macOS executor avançadoa um grupo de executores que tenha uma configuração de rede. Da mesma forma, você não pode adicionar uma configuração de rede a um grupo de executores que contenha macOS executor avançados.

## Alterando o nome de um grupo de runners

1. Acesse a página principal da organização em que os grupos de executores estão localizados.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.
4. Na lista de grupos, clique no grupo de executores que deseja configurar.
5. Insira o novo nome do grupo de executores no campo de texto em "Nome do grupo".
6. Clique em **Save** (Salvar).

## Como mover um executor para um grupo

Se você não especificar o grupo de um executor durante o processo de registro, seus novos executores são automaticamente atribuídos ao grupo padrão e poderão ser transferidos para outro grupo.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de "Executores", clique no executor que você deseja configurar.
5. Selecione o menu suspenso **Grupo de executores**.
6. Em "Transferir executor para o grupo", escolha um grupo de destino para o executor.

## Como remover um grupo de executores

Para remover um grupo de executores, primeiro você deve mover ou remover todos os executores do grupo.

1. Acesse a página principal da organização em que os grupos de executores estão localizados.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.
4. Na lista de grupos, à direita do grupo que você deseja excluir, clique em (The horizontal kebab icon).
5. Para remover o grupo, clique em **Remover grupo**.
6. Revise as solicitações de confirmação e clique em **Remover este grupo de executores**.
