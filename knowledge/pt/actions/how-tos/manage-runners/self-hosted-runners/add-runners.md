---
title: Adicionar executores auto-hospedados
description: Você pode adicionar um runner autogerenciado a um repositório, a uma organização ou a uma empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/add-runners
captured: '2026-10-13'
section: How tos / Manage runners / Self hosted runners
---

# Adicionar executores auto-hospedados { #adding-self-hosted-runners }

_Você pode adicionar um runner autogerenciado a um repositório, a uma organização ou a uma empresa._

!!! warning
    Recomendamos que você use apenas executores auto-hospedados com repositórios privados. Isso acontece porque as bifurcações do seu repositório público podem executar código perigoso em seu computador de executor auto-hospedado criando uma solicitação de pull que executa o código em um fluxo de trabalho.

    Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

## Pré-requisitos { #prerequisites }

Antes de adicionar um executor auto-hospedado, entenda o que eles são e como funcionam. Confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md).

Além disso, você deve atender aos seguintes requisitos:

* Você precisa ter acesso à máquina que você usará como runner auto-hospedado no seu ambiente.

## Adicionar um executor auto-hospedado a um repositório { #adding-a-self-hosted-runner-to-a-repository }

Você pode adicionar executores auto-hospedados a um único repositório. Para adicionar um executor auto-hospedado a um repositório de usuário, você deve ser o proprietário do repositório. Para um repositório da organização, você deve ser proprietário da organização ou ter acesso de administrador ao repositório.

Para obter informações sobre como adicionar um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

!!! note
    organização podem escolher quais repositórios têm permissão para criar executores auto-hospedados em nível de repositório.

    Para obter mais informações, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners).

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](https://docs.github.com/assets/images/help/repository/repo-actions-settings.png)

3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.

4. Clique em **Novo executor auto-hospedado**.

5. Selecione a imagem e a arquitetura do sistema operacional do computador do executor auto-hospedado.

   ![Captura de tela da escolha do sistema operacional e da arquitetura. Essas opções são realçadas com um contorno laranja escuro.](https://docs.github.com/assets/images/help/actions/creating-selfhosted-runner.png)

6. Você verá instruções mostrando como baixar o executor e instalá-lo em sua máquina de executor auto-hospedada.

   Abra um shell em sua máquina de executor auto-hospedado e execute cada comando shell na ordem mostrada.

!!! note

   > No Windows, se você quiser instalar o aplicativo do runner auto-hospedado como um serviço, é necessário abrir um terminal com privilégios de administrador. Também recomendamos que você use `C:\actions-runner` como diretório para o aplicativo do executor auto-hospedado para que as contas do sistema do Windows possam acessar o diretório do executor.

   As instruções te ajudam a completar estas tarefas:

   * Transferindo e extraindo o aplicativo do executor auto-hospedado.
   * Executar o script `config` para configurar o aplicativo executor auto-hospedado e registrá-lo com GitHub Actions. O script `config` exige a URL de destino e um token de tempo limitado gerado automaticamente para autenticar a solicitação. O token expira após uma hora.
     * No Windows, o script `config` também pergunta se você deseja instalar o aplicativo do executor auto-hospedado como um serviço. Para Linux e macOS, você pode instalar um serviço depois de terminar de adicionar o executor. Para saber mais, confira [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md).
   * Executar o aplicativo executor auto-hospedado para conectar o computador a GitHub Actions.

### Verificando se o seu executor auto-hospedado foi adicionado com sucesso { #checking-that-your-self-hosted-runner-was-successfully-added }

Após concluir as etapas para adicionar um executor auto-hospedado, o executor e seu status agora estão listados em "Executores".

A aplicação dos executores auto-hospedados deve estar activa para que o executor aceite os trabalhos. Quando o aplicativo do executor estiver conectado ao GitHub e pronto para receber trabalhos, você verá a seguinte mensagem no terminal do computador.

```shell
√ Connected to GitHub

2019-10-24 05:45:56Z: Listening for Jobs
```

Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](monitor-and-troubleshoot.md).

## Adicionar um executor auto-hospedado a uma organização { #adding-a-self-hosted-runner-to-an-organization }

Você pode adicionar executores auto-hospedados no nível da organização, onde podem ser usados para processar trabalhos para múltiplos repositórios em uma organização. Para adicionar um executor auto-hospedado a uma organização, você deve ser um proprietário. Para obter informações sobre como adicionar um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](https://docs.github.com/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.

4. Clique em **Novo executor**, e clique em **Novo executor auto-hospedado**.

5. Selecione a imagem e a arquitetura do sistema operacional do computador do executor auto-hospedado.

   ![Captura de tela da escolha do sistema operacional e da arquitetura. Essas opções são realçadas com um contorno laranja escuro.](https://docs.github.com/assets/images/help/actions/creating-selfhosted-runner.png)

6. Você verá instruções mostrando como baixar o executor e instalá-lo em sua máquina de executor auto-hospedada.

   Abra um shell em sua máquina de executor auto-hospedado e execute cada comando shell na ordem mostrada.

!!! note

   > No Windows, se você quiser instalar o aplicativo do runner auto-hospedado como um serviço, é necessário abrir um terminal com privilégios de administrador. Também recomendamos que você use `C:\actions-runner` como diretório para o aplicativo do executor auto-hospedado para que as contas do sistema do Windows possam acessar o diretório do executor.

   As instruções te ajudam a completar estas tarefas:

   * Transferindo e extraindo o aplicativo do executor auto-hospedado.
   * Executar o script `config` para configurar o aplicativo executor auto-hospedado e registrá-lo com GitHub Actions. O script `config` exige a URL de destino e um token de tempo limitado gerado automaticamente para autenticar a solicitação. O token expira após uma hora.
     * No Windows, o script `config` também pergunta se você deseja instalar o aplicativo do executor auto-hospedado como um serviço. Para Linux e macOS, você pode instalar um serviço depois de terminar de adicionar o executor. Para saber mais, confira [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md).
   * Executar o aplicativo executor auto-hospedado para conectar o computador a GitHub Actions.

### Verificando se o seu executor auto-hospedado foi adicionado com sucesso { #checking-that-your-self-hosted-runner-was-successfully-added-1 }

Após concluir as etapas para adicionar um executor auto-hospedado, o executor e seu status agora estão listados em "Executores".

A aplicação dos executores auto-hospedados deve estar activa para que o executor aceite os trabalhos. Quando o aplicativo do executor estiver conectado ao GitHub e pronto para receber trabalhos, você verá a seguinte mensagem no terminal do computador.

```shell
√ Connected to GitHub

2019-10-24 05:45:56Z: Listening for Jobs
```

Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](monitor-and-troubleshoot.md).

!!! note
    Por motivos de segurança, repositórios públicos não podem usar executores em um grupo de executores por padrão, mas você pode alterar isso nas configurações do grupo de executores. Para saber mais, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](manage-access.md#changing-which-repositories-can-access-a-runner-group).

## Adicionar um executor auto-hospedado a uma empresa { #adding-a-self-hosted-runner-to-an-enterprise }

Se você usar GitHub Enterprise Cloud, poderá adicionar executores auto-hospedados a uma empresa, onde eles podem ser atribuídos a várias organizações. O proprietário da organização pode controlar quais repositórios podem usá-lo.
Para obter mais informações, consulte a [GitHub Enterprise Cloud documentação](add-runners.md#adding-a-self-hosted-runner-to-an-enterprise).

## Próximas etapas { #next-steps }

Você pode configurar a automação para dimensionar o número de executores auto-hospedados. Para saber mais, confira [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md#autoscaling).
