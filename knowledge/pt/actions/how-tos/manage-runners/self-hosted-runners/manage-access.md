---
title: Gerenciar o acesso a executores auto-hospedados usando grupos
description: Você pode usar políticas para limitar o acesso a runners auto-hospedados que foram adicionados a uma conta corporativa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/manage-access
captured: '2026-10-13'
section: How tos / Manage runners / Self hosted runners
---

# Gerenciar o acesso a executores auto-hospedados usando grupos { #managing-access-to-self-hosted-runners-using-groups }

_Você pode usar políticas para limitar o acesso a runners auto-hospedados que foram adicionados a uma conta corporativa._

## Criar um grupo de executor auto-hospedado para uma organização { #creating-a-self-hosted-runner-group-for-an-organization }

!!! warning
    Recomendamos que você use apenas executores auto-hospedados com repositórios privados. Isso acontece porque as bifurcações do seu repositório público podem executar código perigoso em seu computador de executor auto-hospedado criando uma solicitação de pull que executa o código em um fluxo de trabalho.

    Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

    [!NOTE]
    Ao criar um grupo de executores, você deve escolher uma política que defina quais repositórios de trabalho têm acesso ao grupo de executores. Para alterar quais repositórios e fluxos de trabalho podem acessar o grupo de executores, os proprietários "Gerenciar corredores e grupos de executores" podem definir uma política para a organização. Para saber mais, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](manage-access.md#changing-which-repositories-can-access-a-runner-group).

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

## Como alterar quais repositórios podem acessar um grupo de executores { #creating-a-self-hosted-runner-group-for-an-enterprise }

!!! warning
    Recomendamos que você use apenas executores auto-hospedados com repositórios privados. Isso acontece porque as bifurcações do seu repositório público podem executar código perigoso em seu computador de executor auto-hospedado criando uma solicitação de pull que executa o código em um fluxo de trabalho.

    Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

Para grupos de executores em uma organização, você pode alterar quais repositórios na organização podem acessar um grupo de executores.

1. Acesse a página principal da organização em que os grupos de executores estão localizados.

2. Clique em **(gear) Settings**.

3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.

4. Na lista de grupos, clique no grupo de executores que deseja configurar.

5. Em “Acesso ao repositório”, use o menu suspenso para clicar em **Repositórios selecionados**.
   1. À direita do menu suspenso, clique em (The Gear icon).
   2. Na janela pop-up, use as caixas de seleção para selecionar os repositórios que podem acessar esse grupo de executores.

6. Clique em **Salvar grupo**.

## Alterando o nome de um grupo de runners { #changing-which-organizations-can-access-a-runner-group }

1. Acesse a página principal da organização em que os grupos de executores estão localizados.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.
4. Na lista de grupos, clique no grupo de executores que deseja configurar.
5. Insira o novo nome do grupo de executores no campo de texto em "Nome do grupo".
6. Clique em **Save** (Salvar).

## Adicionando um executor auto-hospedado a um grupo automaticamente { #changing-which-repositories-can-access-a-runner-group }

Você pode usar o script de configuração para adicionar automaticamente um novo executor a um grupo. Por exemplo, esse comando registra um novo executor e usa o parâmetro `--runnergroup` para adicioná-lo a um grupo chamado `rg-runnergroup`.

```shell
./config.sh --url $org_or_enterprise_url --token $token --runnergroup rg-runnergroup
```

O comando irá falhar se o grupo do executor não existir:

```shell
Could not find any self-hosted runner group named "rg-runnergroup".
```

## Mover um executor auto-hospedado para um grupo { #changing-which-workflows-can-access-a-runner-group }

Se você não especificar o grupo de um executor durante o processo de registro, seus novos executores são automaticamente atribuídos ao grupo padrão e poderão ser transferidos para outro grupo.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de "Executores", clique no executor que você deseja configurar.
5. Selecione o menu suspenso **Grupo de executores**.
6. Em "Transferir executor para o grupo", escolha um grupo de destino para o executor.

## Remover um grupo de executor auto-hospedado { #changing-the-name-of-a-runner-group }

Para remover um grupo de executores, primeiro você deve mover ou remover todos os executores do grupo.

1. Acesse a página principal da organização em que os grupos de executores estão localizados.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e escolha **Runner groups**.
4. Na lista de grupos, à direita do grupo que você deseja excluir, clique em (The horizontal kebab icon).
5. Para remover o grupo, clique em **Remover grupo**.
6. Revise as solicitações de confirmação e clique em **Remover este grupo de executores**.
