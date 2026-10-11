---
title: Gerenciar ambientes para implantação
description: Você pode criar ambientes e proteger esses ambientes com regras de proteção de implantação. Um trabalho que faz referência a um ambiente deve seguir quaisquer regras de proteção para o ambiente antes de executar ou acessar os segredos do ambiente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
captured: '2026-10-11'
section: GitHub Actions
---

# Gerenciar ambientes para implantação

_Você pode criar ambientes e proteger esses ambientes com regras de proteção de implantação. Um trabalho que faz referência a um ambiente deve seguir quaisquer regras de proteção para o ambiente antes de executar ou acessar os segredos do ambiente._

## Pré-requisitos

> \[!NOTE]
> Os usuários com GitHub Free planos só podem configurar ambientes para repositórios públicos. Se você converter um repositório de público em privado, todas as regras de proteção ou segredos de ambiente configurados serão ignorados, e você não conseguirá configurar nenhum ambiente. Se você converter seu repositório de volta para público, você terá acesso a todas as regras de proteção e segredos de ambiente previamente configurados.
>
> Organizações com GitHub Team e usuários com GitHub Pro podem configurar ambientes para repositórios privados. Para saber mais, confira [Planos do GitHub](https://docs.github.com/pt/get-started/learning-about-github/githubs-plans).

* Para obter informações gerais sobre ambientes, confira [Implantando com GitHub Actions](control-deployments.md#using-environments).
* Para obter informações sobre as regras disponíveis, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md).

## Criando um ambiente

Para configurar um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para configurar um ambiente em um repositório da organização, você precisa ter acesso de `admin`.

> \[!NOTE]
>
> * A criação de um ambiente em um repositório privado está disponível para organizações com GitHub Team e para usuários com GitHub Pro.
> * Alguns recursos para ambientes não estão disponíveis ou têm disponibilidade limitada para repositórios privados. Se você não conseguir acessar um recurso descrito nas instruções abaixo, confira a documentação vinculada na etapa relacionada para obter as informações de disponibilidade.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Clique em **Novo ambiente**.
5. Insira um nome para o ambiente e clique em **Configurar ambiente**. Os nomes de ambiente não diferenciam maiúsculas de minúsculas. Um nome de ambiente não pode exceder 255 caracteres e deve ser único dentro do repositório.
6. Opcionalmente, especifique as pessoas ou equipes que devem aprovar os trabalhos do fluxo de trabalho que usam esse ambiente. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#required-reviewers).
   1. Selecione **Revisores necessários**.
   2. Insira até até 6 pessoas ou equipes. Apenas um dos revisores precisam aprovar o trabalho para que prossiga.
   3. Opcionalmente, para impedir que os usuários aprovem as execuções de fluxos de trabalho que eles dispararam, selecione **Impedir a auto-revisão**.
   4. Clique em **Salvar regras de proteção**.
7. Opcionalmente, especifique o tempo a esperar antes de permitir que os trabalhos do fluxo de trabalho que usam esse ambiente prossigam. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#wait-timer).
   1. Selecione **Temporizador de espera**.
   2. Insira o número de minutos para esperar.
   3. Clique em **Salvar regras de proteção**.
8. Opcionalmente, impedir a ignorância das regras de proteção configuradas. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#allow-administrators-to-bypass-configured-protection-rules).
   1. Desmarque **Permitir que os administradores ignorem as regras de proteção configuradas**.
   2. Clique em **Salvar regras de proteção**.
9. Opcionalmente, habilite todas as regras de proteção de implantação personalizadas que foram criadas com GitHub Apps. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#custom-deployment-protection-rules).
   1. Selecione a regra de proteção personalizada que você deseja habilitar.
   2. Clique em **Salvar regras de proteção**.
10. Opcionalmente, especifique quais branches e tags podem ser implantados neste ambiente. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#deployment-branches-and-tags).
    1. Selecione a opção desejada no menu suspenso **Branches de implantação**.

    2. Se você escolheu **Ramos e etiquetas selecionados**, para adicionar uma nova regra, clique em **Adicionar regra de implantação de ramo ou etiqueta**

    3. No menu suspenso "Tipo de referência", dependendo da regra que deseja aplicar, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-git-branch" aria-label="git-branch" role="img"><path d="M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"></path></svg>Ramificação** ou **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-tag" aria-label="tag" role="img"><path d="M1 7.775V2.75C1 1.784 1.784 1 2.75 1h5.025c.464 0 .91.184 1.238.513l6.25 6.25a1.75 1.75 0 0 1 0 2.474l-5.026 5.026a1.75 1.75 0 0 1-2.474 0l-6.25-6.25A1.752 1.752 0 0 1 1 7.775Zm1.5 0c0 .066.026.13.073.177l6.25 6.25a.25.25 0 0 0 .354 0l5.025-5.025a.25.25 0 0 0 0-.354l-6.25-6.25a.25.25 0 0 0-.177-.073H2.75a.25.25 0 0 0-.25.25ZM6 5a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z"></path></svg> Marcação**.

    4. Insira o padrão de nome do branch ou tag que você deseja permitir.

       > \[!NOTE]
       > Os padrões de nomes devem ser configurados individualmente para branches ou rótulos.

    5. Clique em **Adicionar regra**.
11. Opcionalmente, adicione segredos de ambiente. Esses segredos só estão disponíveis para trabalhos de fluxo de trabalho que usam o ambiente. Além disso, os trabalhos do fluxo de trabalho que usam este ambiente só podem acessar esses segredos após qualquer regra configurada (por exemplo, revisores obrigatórios) ser aprovada. Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#environment-secrets).
    1. Em **Segredos do ambiente**, clique em **Adicionar Segredo**.
    2. Insira o nome do segredo.
    3. Insira o valor do segredo.
    4. Clique em **Adicionar segredo**.
12. Opcionalmente, adicione variáveis de ambiente. Essas variáveis só ficam disponíveis para trabalhos de fluxo de trabalho que usam o ambiente e só podem ser acessadas usando o contexto [`vars`](../../../reference/workflows-and-actions/contexts.md#vars-context). Para saber mais, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md#environment-variables).
    1. Em **Variáveis de ambiente**, clique em **Adicionar Variável**.
    2. Informe o nome da variável.
    3. Informe o valor da variável.
    4. Clique em **Adicionar variável**.

Também é possível criar e configurar ambientes por meio da API REST. Para saber mais, confira [Endpoints da API REST para contextos de implantação](https://docs.github.com/pt/rest/deployments/environments), [Pontos de extremidade da API REST para segredos do GitHub Actions](https://docs.github.com/pt/rest/actions/secrets), [Pontos de extremidade da API REST para variáveis de GitHub Actions](https://docs.github.com/pt/rest/actions/variables) e [Pontos de extremidade da API REST para políticas de branch de implantação](https://docs.github.com/pt/rest/deployments/branch-policies).

Executar um fluxo de trabalho que faz referência a um ambiente que não existe criará um ambiente com o nome referenciado. Se o ambiente for criado a partir da execução de builds de página implícitos (por exemplo, a partir de uma ramificação ou pasta de origem), a ramificação de origem será adicionada como uma regra de proteção ao ambiente. Caso contrário, o novo ambiente criado não terá nenhuma regra de proteção ou segredo configurado. Qualquer pessoa que possa editar fluxos de trabalho no repositório pode criar ambientes por meio de um arquivo de fluxo de trabalho, mas apenas os administradores do repositório podem configurar o ambiente.

## Excluir um ambiente

Para configurar um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para configurar um ambiente em um repositório da organização, você precisa ter acesso de `admin`.

A exclusão de um ambiente apagará todos os segredos e regras de proteção associados ao ambiente. Todos os trabalhos que estejam atualmente em espera devido às regras de proteção do ambiente eliminado falharão automaticamente.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Ao lado do ambiente que você deseja excluir, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-trash" aria-label="Delete environment" role="img"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"></path></svg>.
5. Clique em **Entendi. Excluir este ambiente**.

Também é possível excluir ambientes por meio da API REST. Para saber mais, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#environments).

## Como os ambientes relacionam-se com as implantações

Quando um trabalho de fluxo de trabalho que referencia um ambiente é executado, ele cria um objeto de implantação com a propriedade `environment` definida como o nome do ambiente. À medida que o fluxo de trabalho progride, ele também cria objetos de status de implantação com a propriedade `environment` definida como o nome do ambiente, a propriedade `environment_url` definida como a URL para o ambiente (se especificado no fluxo de trabalho) e a propriedade `state` definida como o status do trabalho.

Você pode acessar esses objetos por meio da API REST ou API do GraphQL. Você também pode se inscrever nesses eventos de webhook. Para obter mais informações, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#deployments), [Deployments](https://docs.github.com/pt/graphql/reference/deployments#object-deployment) (API do GraphQL) ou [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment).

## Próximas etapas

GitHub Actions fornece vários recursos para gerenciar suas implantações. Para saber mais, confira [Implantando com GitHub Actions](control-deployments.md).
