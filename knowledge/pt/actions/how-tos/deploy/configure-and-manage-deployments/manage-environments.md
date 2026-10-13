---
title: Gerenciar ambientes para implantação
description: Você pode criar ambientes e proteger esses ambientes com regras de proteção de implantação. Um trabalho que faz referência a um ambiente deve seguir quaisquer regras de proteção para o ambiente antes de executar ou acessar os segredos do ambiente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments
captured: '2026-10-13'
section: How tos / Deploy / Configure and manage deployments
---

# Gerenciar ambientes para implantação { #managing-environments-for-deployment }

_Você pode criar ambientes e proteger esses ambientes com regras de proteção de implantação. Um trabalho que faz referência a um ambiente deve seguir quaisquer regras de proteção para o ambiente antes de executar ou acessar os segredos do ambiente._

## Pré-requisitos { #prerequisites }

!!! note
    Os usuários com GitHub Free planos só podem configurar ambientes para repositórios públicos. Se você converter um repositório de público em privado, todas as regras de proteção ou segredos de ambiente configurados serão ignorados, e você não conseguirá configurar nenhum ambiente. Se você converter seu repositório de volta para público, você terá acesso a todas as regras de proteção e segredos de ambiente previamente configurados.

    Organizações com GitHub Team e usuários com GitHub Pro podem configurar ambientes para repositórios privados. Para saber mais, confira [Planos do GitHub](https://docs.github.com/pt/get-started/learning-about-github/githubs-plans).

* Para obter informações gerais sobre ambientes, confira [Implantando com GitHub Actions](control-deployments.md#using-environments).
* Para obter informações sobre as regras disponíveis, confira [Implantações e ambientes](../../../reference/workflows-and-actions/deployments-and-environments.md).

## Criando um ambiente { #creating-an-environment }

Para configurar um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para configurar um ambiente em um repositório da organização, você precisa ter acesso de `admin`.

!!! note
    * A criação de um ambiente em um repositório privado está disponível para organizações com GitHub Team e para usuários com GitHub Pro.
    * Alguns recursos para ambientes não estão disponíveis ou têm disponibilidade limitada para repositórios privados. Se você não conseguir acessar um recurso descrito nas instruções abaixo, confira a documentação vinculada na etapa relacionada para obter as informações de disponibilidade.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](https://docs.github.com/assets/images/help/repository/repo-actions-settings.png)
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

    3. No menu suspenso "Tipo de referência", dependendo da regra que deseja aplicar, clique em **(git-branch)Ramificação** ou **(tag) Marcação**.

    4. Insira o padrão de nome do branch ou tag que você deseja permitir.

!!! note

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

## Excluir um ambiente { #deleting-an-environment }

Para configurar um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para configurar um ambiente em um repositório da organização, você precisa ter acesso de `admin`.

A exclusão de um ambiente apagará todos os segredos e regras de proteção associados ao ambiente. Todos os trabalhos que estejam atualmente em espera devido às regras de proteção do ambiente eliminado falharão automaticamente.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](https://docs.github.com/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Ao lado do ambiente que você deseja excluir, clique em (Delete environment).
5. Clique em **Entendi. Excluir este ambiente**.

Também é possível excluir ambientes por meio da API REST. Para saber mais, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#environments).

## Como os ambientes relacionam-se com as implantações { #how-environments-relate-to-deployments }

Quando um trabalho de fluxo de trabalho que referencia um ambiente é executado, ele cria um objeto de implantação com a propriedade `environment` definida como o nome do ambiente. À medida que o fluxo de trabalho progride, ele também cria objetos de status de implantação com a propriedade `environment` definida como o nome do ambiente, a propriedade `environment_url` definida como a URL para o ambiente (se especificado no fluxo de trabalho) e a propriedade `state` definida como o status do trabalho.

Você pode acessar esses objetos por meio da API REST ou API do GraphQL. Você também pode se inscrever nesses eventos de webhook. Para obter mais informações, confira [Pontos de extremidade da API REST para repositórios](https://docs.github.com/pt/rest/repos#deployments), [Deployments](https://docs.github.com/pt/graphql/reference/deployments#object-deployment) (API do GraphQL) ou [Eventos e cargas de webhook](https://docs.github.com/pt/webhooks/webhook-events-and-payloads#deployment).

## Próximas etapas { #next-steps }

GitHub Actions fornece vários recursos para gerenciar suas implantações. Para saber mais, confira [Implantando com GitHub Actions](control-deployments.md).
