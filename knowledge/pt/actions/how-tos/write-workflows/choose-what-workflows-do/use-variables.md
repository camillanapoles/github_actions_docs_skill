---
title: Armazenar informações em variáveis
description: GitHub define variáveis padrão para cada GitHub Actions execução de fluxo de trabalho. Você também pode definir variáveis personalizadas para uso em um ou vários fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables
captured: '2026-10-11'
section: GitHub Actions
---

# Armazenar informações em variáveis

_GitHub define variáveis padrão para cada GitHub Actions execução de fluxo de trabalho. Você também pode definir variáveis personalizadas para uso em um ou vários fluxos de trabalho._

## Definir variáveis de ambiente para um único fluxo de trabalho

Para definir uma variável de ambiente personalizada para uso em um único fluxo de trabalho, é possível usar a chave `env` no arquivo do fluxo de trabalho. O escopo de uma variável personalizada definida por este método fica limitado ao elemento em que ele está definido. Você pode definir variáveis cujos escopos são definidos como:

* Todo o fluxo de trabalho, usando [`env`](../../../reference/workflows-and-actions/workflow-syntax.md#env) no nível superior do arquivo de fluxo de trabalho.
* O conteúdo de um trabalho em um fluxo de trabalho, usando [`jobs.<job_id>.env`](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idenv).
* Uma etapa específica em um trabalho, usando [`jobs.<job_id>.steps[*].env`](/pt/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsenv).

```yaml copy
name: Greeting on variable day

on:
  workflow_dispatch

env:
  DAY_OF_WEEK: Monday

jobs:
  greeting_job:
    runs-on: ubuntu-latest
    env:
      Greeting: Hello
    steps:
      - name: "Say Hello Mona it's Monday"
        run: echo "$Greeting $First_Name. Today is $DAY_OF_WEEK!"
        env:
          First_Name: Mona
```

Você pode acessar `env` valores de variáveis usando as variáveis de ambiente do executor ou usando contextos. O exemplo acima mostra três variáveis personalizadas usadas como variáveis de ambiente de executor em um comando `echo`: `$DAY_OF_WEEK`, `$Greeting` e `$First_Name`. Os valores e os escopos dessas variáveis são definidos no nível do fluxo de trabalho, do trabalho e da etapa, respectivamente. A interpolação dessas variáveis acontece no executor.

Os comandos nas etapas `run` de um fluxo de trabalho, ou uma ação referenciada, são processados pelo shell que você está usando no executor. As instruções em outras partes de um fluxo de trabalho são processadas por GitHub Actions e não são enviadas ao runner. Você pode usar variáveis de ambiente do executor ou contextos nas etapas `run`, mas, nas partes de um fluxo de trabalho que não são enviadas ao executor, você deve usar contextos para acessar valores de variáveis. Para obter mais informações, consulte [Usar contextos para acessar valores de variáveis](#using-contexts-to-access-variable-values).

Como a interpolação de variável de ambiente do executor é feita depois que um trabalho do fluxo de trabalho é enviado para uma máquina do executor, você deve usar a sintaxe apropriada para o shell usado no executor. Neste exemplo, o fluxo de trabalho especifica `ubuntu-latest`. Por padrão, os executores do Linux usam o shell do Bash. Portanto, você precisa usar a sintaxe `$NAME`. Por padrão, os executores do Windows usam o PowerShell, então, você usaria a sintaxe `$env:NAME`. Para saber mais sobre shells, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsshell).

## Como definir variáveis de configuração para vários fluxos de trabalho

Você pode criar variáveis de configuração para uso em vários fluxos de trabalho e pode defini-las no nível da [organização](#creating-configuration-variables-for-an-organization), do [repositório](#creating-configuration-variables-for-a-repository) ou do [ambiente](#creating-configuration-variables-for-an-environment).

Por exemplo, você pode usar variáveis de configuração para definir valores padrão a parâmetros passados para criar ferramentas no nível da organização, mas permitir que os proprietários de repositório substituam esses parâmetros caso a caso.

Quando você define variáveis de configuração, elas ficam automaticamente disponíveis no contexto `vars`. Para obter mais informações, confira [Como usar o `vars`contexto para acessar valores de variáveis de configuração](#using-the-vars-context-to-access-configuration-variable-values).

### Criando variáveis de configuração para um repositório

Para criar segredos ou variáveis em GitHub para um repositório de organização, você deve ter `write` acesso. Para um repositório de conta pessoal, você deve ser um colaborador do repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na seção "Security" da barra lateral, selecione **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-key-asterisk" aria-label="key-asterisk" role="img"><path d="M0 2.75A2.75 2.75 0 0 1 2.75 0h10.5A2.75 2.75 0 0 1 16 2.75v10.5A2.75 2.75 0 0 1 13.25 16H2.75A2.75 2.75 0 0 1 0 13.25ZM2.75 1.5c-.69 0-1.25.56-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25Z"></path><path d="M8 4a.75.75 0 0 1 .75.75V6.7l1.69-.975a.75.75 0 0 1 .75 1.3L9.5 8l1.69.976a.75.75 0 0 1-.75 1.298L8.75 9.3v1.951a.75.75 0 0 1-1.5 0V9.299l-1.69.976a.75.75 0 0 1-.75-1.3L6.5 8l-1.69-.975a.75.75 0 0 1 .75-1.3l1.69.976V4.75A.75.75 0 0 1 8 4Z"></path></svg> Secrets and variables** e clique em **Actions**.
4. Clique na guia **Variáveis**.

![Captura de tela da página "Segredos e variáveis das ações". A aba "Variáveis" está contornada em laranja escuro.](/assets/images/help/repository/actions-variables-tab.png)

1. Clique em **Nova variável de repositório**.
2. No campo **Nome**, insira um nome para sua variável.
3. No campo **Valor**, insira o valor da variável.
4. Clique em **Adicionar variável**.

### Como criar variáveis de configuração para um ambiente

Para criar segredos ou variáveis para um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para criar segredos ou variáveis para um ambiente em um repositório de uma organização, é necessário ter acesso `admin`. Para saber mais sobre os ambientes, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Clique no ambiente ao qual deseja adicionar uma variável.
5. Em **Variáveis de ambiente**, clique em **Adicionar variável**.
6. No campo **Nome**, insira um nome para sua variável.
7. No campo **Valor**, insira o valor da variável.
8. Clique em **Adicionar variável**.

### Como criar variáveis de configuração para uma organização

> \[!NOTE]
> Os segredos e variáveis no nível da organização não são acessíveis por repositórios privados para GitHub Free. Para obter mais informações sobre como atualizar sua GitHub assinatura, consulte [Atualizando o plano da sua conta](https://docs.github.com/pt/billing/how-tos/manage-plan-and-licenses/upgrade-plan).

Ao criar um segredo ou uma variável em uma organização, você poderá usar uma política para limitar o acesso por repositório. Por exemplo, você pode conceder acesso a todos os repositórios ou limitar o acesso a apenas repositórios privados ou a uma lista específica de repositórios.

Os proprietários "Gerenciar variáveis de ações da organização" ou "Gerenciar segredos de ações da organização" podem criar segredos ou variáveis no nível da organização.

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na seção "Security" da barra lateral, selecione **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-key-asterisk" aria-label="key-asterisk" role="img"><path d="M0 2.75A2.75 2.75 0 0 1 2.75 0h10.5A2.75 2.75 0 0 1 16 2.75v10.5A2.75 2.75 0 0 1 13.25 16H2.75A2.75 2.75 0 0 1 0 13.25ZM2.75 1.5c-.69 0-1.25.56-1.25 1.25v10.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25V2.75c0-.69-.56-1.25-1.25-1.25Z"></path><path d="M8 4a.75.75 0 0 1 .75.75V6.7l1.69-.975a.75.75 0 0 1 .75 1.3L9.5 8l1.69.976a.75.75 0 0 1-.75 1.298L8.75 9.3v1.951a.75.75 0 0 1-1.5 0V9.299l-1.69.976a.75.75 0 0 1-.75-1.3L6.5 8l-1.69-.975a.75.75 0 0 1 .75-1.3l1.69.976V4.75A.75.75 0 0 1 8 4Z"></path></svg> Secrets and variables** e clique em **Actions**.

4. Clique na guia **Variáveis**.

   ![Captura de tela da página "Ações: segredos e variáveis". A aba "Variáveis" está contornada em laranja escuro.](/assets/images/help/repository/actions-variables-tab.png)

5. Clique em **Nova variável de organização**.

6. No campo **Nome**, insira um nome para sua variável.

7. No campo **Valor**, insira o valor da variável.

8. Na lista de menu suspenso **Acesso do repositório**, escolha uma política de acesso.

9. Clique em **Adicionar variável**.

## Como usar contextos para acessar valores de variáveis

Os contextos são uma forma de acessar informações sobre execuções de fluxo de trabalho, variáveis, ambientes dos executores, trabalhos e etapas. Para obter mais informações, consulte [Referência de contextos](../../../reference/workflows-and-actions/contexts.md). Há muitos outros contextos que você pode usar para uma série de finalidades nos seus fluxos de trabalho. Para obter detalhes sobre quando usar contextos específicos em um fluxo de trabalho, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#context-availability).

Você pode acessar valores de variáveis de ambiente usando o contexto `env` e valores de variáveis de configuração usando o contexto `vars`.

### Como usar o contexto `env` para acessar valores de variáveis de ambiente

Além das variáveis de ambiente do runner, GitHub Actions permite definir e ler os valores de chave de `env` por meio de contextos. As variáveis e os contextos do ambiente são destinados a serem usados em diferentes pontos do fluxo de trabalho.

As etapas `run` em um fluxo de trabalho ou em uma ação referenciada são processadas por um executor. Como resultado, você pode usar variáveis de ambiente de executor aqui, usando a sintaxe apropriada para o shell que você está usando no executor; por exemplo, `$NAME` para o shell bash em um executor do Linux ou `$env:NAME` para o PowerShell em um executor do Windows. Na maioria dos casos, você também pode usar contextos, com a sintaxe `${{ CONTEXT.PROPERTY }}`, para acessar o mesmo valor. A diferença é que o contexto será interpolado e substituído por uma cadeia de caracteres antes que o trabalho seja enviado a um executor.

No entanto, você não pode usar variáveis de ambiente do executor em partes de um fluxo de trabalho que são processadas por GitHub Actions e não são enviadas ao executor. Em vez disso, você deve usar contextos. Por exemplo, uma `if` condicional, que determina se uma tarefa ou etapa será enviada ao executor, é sempre processada por GitHub Actions. Portanto, você deve usar um contexto em uma instrução `if` condicional para acessar o valor de uma variável.

```yaml copy
name: Conditional env variable

on: workflow_dispatch

env:
  DAY_OF_WEEK: Monday

jobs:
  greeting_job:
    runs-on: ubuntu-latest
    env:
      Greeting: Hello
    steps:
      - name: "Say Hello Mona it's Monday"
        if: ${{ env.DAY_OF_WEEK == 'Monday' }}
        run: echo "$Greeting $First_Name. Today is $DAY_OF_WEEK!"
        env:
          First_Name: Mona
```

Nessa modificação do exemplo anterior, introduzimos um `if` condicional. A etapa de fluxo de trabalho agora só será executada se `DAY_OF_WEEK` estiver definido como "Segunda-feira". Acessamos esse valor por meio da instrução condicional `if` usando o [ contexto `env`](../../../reference/workflows-and-actions/contexts.md#env-context). O contexto `env` não é necessário para as variáveis referenciadas no comando `run`. Elas são referenciadas como variáveis de ambiente do executor e são interpoladas depois que o trabalho é recebido pelo executor. No entanto, poderíamos ter optado por interpolar essas variáveis antes de enviar o trabalho ao executor, usando contextos. A saída resultante seria a mesma.

```yaml
run: echo "${{ env.Greeting }} ${{ env.First_Name }}. Today is ${{ env.DAY_OF_WEEK }}!"
```

> \[!NOTE]
> Os contextos geralmente são indicados pelo sinal de cifrão e chaves, como `${{ context.property }}`. Em uma condicional `if`, `${{` e `}}` são opcionais, mas, se você usá-los, eles devem envolver toda a expressão de comparação, conforme mostrado acima.

> \[!WARNING]
> Ao criar fluxos de trabalho e ações, sempre considere se o código poderá executar entradas não confiáveis de possíveis invasores. Certos contextos devem ser tratados como entradas não confiáveis, uma vez que um invasor pode inserir seu próprio conteúdo malicioso. Para saber mais, confira [Referência de uso seguro](../../../reference/security/secure-use.md#good-practices-for-mitigating-script-injection-attacks).

### Como usar o contexto `vars` para acessar valores de variáveis de configuração

As variáveis de configuração podem ser acessadas em todo o fluxo de trabalho usando o contexto `vars`. Para saber mais, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#vars-context).

Se uma variável de configuração não tiver sido definida, o valor retornado de um contexto referenciando a variável será uma cadeia de caracteres vazia.

O exemplo a seguir mostra o uso de variáveis de configuração com o contexto `vars` em um fluxo de trabalho. Cada uma das variáveis de configuração a seguir foram definidas no nível do repositório, da organização ou do ambiente.

```yaml copy
on:
  workflow_dispatch:
env:
  # Setting an environment variable with the value of a configuration variable
  env_var: ${{ vars.ENV_CONTEXT_VAR }}

jobs:
  display-variables:
    name: ${{ vars.JOB_NAME }}
    # You can use configuration variables with the `vars` context for dynamic jobs
    if: ${{ vars.USE_VARIABLES == 'true' }}
    runs-on: ${{ vars.RUNNER }}
    environment: ${{ vars.ENVIRONMENT_STAGE }}
    steps:
    - name: Use variables
      run: |
        echo "repository variable : $REPOSITORY_VAR"
        echo "organization variable : $ORGANIZATION_VAR"
        echo "overridden variable : $OVERRIDE_VAR"
        echo "variable from shell environment : $env_var"
      env:
        REPOSITORY_VAR: ${{ vars.REPOSITORY_VAR }}
        ORGANIZATION_VAR: ${{ vars.ORGANIZATION_VAR }}
        OVERRIDE_VAR: ${{ vars.OVERRIDE_VAR }}

    - name: ${{ vars.HELLO_WORLD_STEP }}
      if: ${{ vars.HELLO_WORLD_ENABLED == 'true' }}
      uses: actions/hello-world-javascript-action@main
      with:
        who-to-greet: ${{ vars.GREET_NAME }}
```

## Detectando o sistema operacional

Você pode escrever um único arquivo de fluxo de trabalho que pode ser usado para sistemas operacionais diferentes usando a `RUNNER_OS` variável de ambiente padrão e a propriedade <span style="white-space: nowrap;">`${{ runner.os }}`</span>de contexto correspondente. Por exemplo, o fluxo de trabalho a seguir poderá ser executado com sucesso se você alterar o sistema operacional de `macos-latest` para `windows-latest` sem precisar alterar a sintaxe das variáveis de ambiente, que varia conforme o shell que está sendo usado pelo executor.

```yaml copy
on: workflow_dispatch

jobs:
  if-Windows-else:
    runs-on: macos-latest
    steps:
      - name: condition 1
        if: runner.os == 'Windows'
        run: echo "The operating system on the runner is $env:RUNNER_OS."
      - name: condition 2
        if: runner.os != 'Windows'
        run: echo "The operating system on the runner is not Windows, it's $RUNNER_OS."
```

Neste exemplo, as duas instruções `if` verificam a propriedade `os` do contexto `runner` para determinar o sistema operacional do executor.
`if` as condicionais são processadas por GitHub Actions, e apenas as etapas em que a verificação é resolvida conforme `true` são enviadas para o executor. Aqui, uma das verificações sempre será `true` e a outra `false`. Portanto, apenas uma dessas etapas será enviada ao executor. Assim que o trabalho for enviado ao executor, a etapa será executada e a variável de ambiente no comando `echo` será interpolada com a sintaxe apropriada (`$env:NAME` para o PowerShell no Windows e `$NAME` para o Bash e o sh no Linux e no macOS). Neste exemplo, a instrução `runs-on: macos-latest` significa que a segunda etapa será executada.

## Passando valores entre etapas e trabalhos em um fluxo de trabalho

Se você gerar um valor em uma etapa de um trabalho, poderá usar o valor em etapas posteriores do mesmo trabalho atribuindo o valor a uma variável de ambiente nova ou existente e gravando isso no arquivo de ambiente `GITHUB_ENV`. O arquivo de ambiente pode ser usado diretamente por uma ação ou em um comando do shell no arquivo de fluxo de trabalho usando a palavra-chave `run`. Para saber mais, confira [Comandos de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-commands.md#setting-an-environment-variable).

Se você deseja passar um valor de uma etapa de um trabalho em um fluxo de trabalho para uma etapa de outro trabalho no fluxo de trabalho, você poderá definir o valor como uma saída de trabalho. Em seguida, você poderá fazer referência a saída desse trabalho a partir de uma etapa em outro trabalho. Para saber mais, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs).

## Próximas etapas

Para obter informações de referência, confira [Referência de variáveis](../../../reference/workflows-and-actions/variables.md).
