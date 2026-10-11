---
title: Adicionar executores auto-hospedados
description: Você pode adicionar um runner autogerenciado a um repositório, a uma organização ou a uma empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/add-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Adicionar executores auto-hospedados

_Você pode adicionar um runner autogerenciado a um repositório, a uma organização ou a uma empresa._

> \[!WARNING]
> Recomendamos que você use apenas executores auto-hospedados com repositórios privados. Isso acontece porque as bifurcações do seu repositório público podem executar código perigoso em seu computador de executor auto-hospedado criando uma solicitação de pull que executa o código em um fluxo de trabalho.
>
> Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md).

## Pré-requisitos

Antes de adicionar um executor auto-hospedado, entenda o que eles são e como funcionam. Confira [Executores auto-hospedados](../../../concepts/runners/self-hosted-runners.md).

Além disso, você deve atender aos seguintes requisitos:

* Você precisa ter acesso à máquina que você usará como runner auto-hospedado no seu ambiente.

## Adicionar um executor auto-hospedado a um repositório

Você pode adicionar executores auto-hospedados a um único repositório. Para adicionar um executor auto-hospedado a um repositório de usuário, você deve ser o proprietário do repositório. Para um repositório da organização, você deve ser proprietário da organização ou ter acesso de administrador ao repositório.

Para obter informações sobre como adicionar um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

> \[!NOTE]
> organização podem escolher quais repositórios têm permissão para criar executores auto-hospedados em nível de repositório.
>
> Para obter mais informações, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners).

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)

3. Na barra lateral esquerda, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions** e clique em **Runners**.

4. Clique em **Novo executor auto-hospedado**.

5. Selecione a imagem e a arquitetura do sistema operacional do computador do executor auto-hospedado.

   ![Captura de tela da escolha do sistema operacional e da arquitetura. Essas opções são realçadas com um contorno laranja escuro.](/assets/images/help/actions/creating-selfhosted-runner.png)

6. Você verá instruções mostrando como baixar o executor e instalá-lo em sua máquina de executor auto-hospedada.

   Abra um shell em sua máquina de executor auto-hospedado e execute cada comando shell na ordem mostrada.

   > \[!NOTE]
   > No Windows, se você quiser instalar o aplicativo do runner auto-hospedado como um serviço, é necessário abrir um terminal com privilégios de administrador. Também recomendamos que você use `C:\actions-runner` como diretório para o aplicativo do executor auto-hospedado para que as contas do sistema do Windows possam acessar o diretório do executor.

   As instruções te ajudam a completar estas tarefas:

   * Transferindo e extraindo o aplicativo do executor auto-hospedado.
   * Executar o script `config` para configurar o aplicativo executor auto-hospedado e registrá-lo com GitHub Actions. O script `config` exige a URL de destino e um token de tempo limitado gerado automaticamente para autenticar a solicitação. O token expira após uma hora.
     * No Windows, o script `config` também pergunta se você deseja instalar o aplicativo do executor auto-hospedado como um serviço. Para Linux e macOS, você pode instalar um serviço depois de terminar de adicionar o executor. Para saber mais, confira [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md).
   * Executar o aplicativo executor auto-hospedado para conectar o computador a GitHub Actions.

### Verificando se o seu executor auto-hospedado foi adicionado com sucesso

Após concluir as etapas para adicionar um executor auto-hospedado, o executor e seu status agora estão listados em "Executores".

A aplicação dos executores auto-hospedados deve estar activa para que o executor aceite os trabalhos. Quando o aplicativo do executor estiver conectado ao GitHub e pronto para receber trabalhos, você verá a seguinte mensagem no terminal do computador.

```shell
√ Connected to GitHub

2019-10-24 05:45:56Z: Listening for Jobs
```

Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](monitor-and-troubleshoot.md).

## Adicionar um executor auto-hospedado a uma organização

Você pode adicionar executores auto-hospedados no nível da organização, onde podem ser usados para processar trabalhos para múltiplos repositórios em uma organização. Para adicionar um executor auto-hospedado a uma organização, você deve ser um proprietário. Para obter informações sobre como adicionar um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na barra lateral esquerda, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions** e clique em **Runners**.

4. Clique em **Novo executor**, e clique em **Novo executor auto-hospedado**.

5. Selecione a imagem e a arquitetura do sistema operacional do computador do executor auto-hospedado.

   ![Captura de tela da escolha do sistema operacional e da arquitetura. Essas opções são realçadas com um contorno laranja escuro.](/assets/images/help/actions/creating-selfhosted-runner.png)

6. Você verá instruções mostrando como baixar o executor e instalá-lo em sua máquina de executor auto-hospedada.

   Abra um shell em sua máquina de executor auto-hospedado e execute cada comando shell na ordem mostrada.

   > \[!NOTE]
   > No Windows, se você quiser instalar o aplicativo do runner auto-hospedado como um serviço, é necessário abrir um terminal com privilégios de administrador. Também recomendamos que você use `C:\actions-runner` como diretório para o aplicativo do executor auto-hospedado para que as contas do sistema do Windows possam acessar o diretório do executor.

   As instruções te ajudam a completar estas tarefas:

   * Transferindo e extraindo o aplicativo do executor auto-hospedado.
   * Executar o script `config` para configurar o aplicativo executor auto-hospedado e registrá-lo com GitHub Actions. O script `config` exige a URL de destino e um token de tempo limitado gerado automaticamente para autenticar a solicitação. O token expira após uma hora.
     * No Windows, o script `config` também pergunta se você deseja instalar o aplicativo do executor auto-hospedado como um serviço. Para Linux e macOS, você pode instalar um serviço depois de terminar de adicionar o executor. Para saber mais, confira [Configurar o aplicativo do executor auto-hospedado como um serviço](configure-the-application.md).
   * Executar o aplicativo executor auto-hospedado para conectar o computador a GitHub Actions.

### Verificando se o seu executor auto-hospedado foi adicionado com sucesso

Após concluir as etapas para adicionar um executor auto-hospedado, o executor e seu status agora estão listados em "Executores".

A aplicação dos executores auto-hospedados deve estar activa para que o executor aceite os trabalhos. Quando o aplicativo do executor estiver conectado ao GitHub e pronto para receber trabalhos, você verá a seguinte mensagem no terminal do computador.

```shell
√ Connected to GitHub

2019-10-24 05:45:56Z: Listening for Jobs
```

Para saber mais, confira [Monitorar e solucionar problemas de executores auto-hospedados](monitor-and-troubleshoot.md).

> \[!NOTE]
> Por motivos de segurança, repositórios públicos não podem usar executores em um grupo de executores por padrão, mas você pode alterar isso nas configurações do grupo de executores. Para saber mais, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](manage-access.md#changing-which-repositories-can-access-a-runner-group).

## Adicionar um executor auto-hospedado a uma empresa

Se você usar GitHub Enterprise Cloud, poderá adicionar executores auto-hospedados a uma empresa, onde eles podem ser atribuídos a várias organizações. O proprietário da organização pode controlar quais repositórios podem usá-lo.
Para obter mais informações, consulte a [GitHub Enterprise Cloud documentação](add-runners.md#adding-a-self-hosted-runner-to-an-enterprise).

## Próximas etapas

Você pode configurar a automação para dimensionar o número de executores auto-hospedados. Para saber mais, confira [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md#autoscaling).
