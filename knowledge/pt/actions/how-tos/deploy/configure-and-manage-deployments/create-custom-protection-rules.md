---
title: Criar regras de proteção de implantação personalizadas
description: Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules
captured: '2026-10-11'
section: How tos / Deploy / Configure and manage deployments
---

# Criar regras de proteção de implantação personalizadas

_Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros._

## Pré-requisitos

!!! note
    Regras de proteção de implementação personalizada estão em prévia pública e estão sujeitas a alterações.

Para obter informações gerais sobre as regras de proteção à implantação, confira [Implantando com GitHub Actions](control-deployments.md#using-custom-deployment-protection-rules).

## Criando uma regra de proteção de implantação personalizada com GitHub Apps

1. Criar um GitHub App. Para saber mais, confira [Registrando um aplicativo GitHub](https://docs.github.com/pt/apps/creating-github-apps/registering-a-github-app/registering-a-github-app). Configure GitHub App da seguinte forma.
   1. Opcionalmente, no campo de texto **URL de Retorno de Chamada** em "Identificar e autorizar usuários", insira a URL de retorno de chamada. Para saber mais, confira [Sobre a URL de retorno de chamada de autorização do usuário](https://docs.github.com/pt/apps/creating-github-apps/registering-a-github-app/about-the-user-authorization-callback-url).
   2. Em "Permissões", selecione **Permissões de repositório**.
   3. À direita de "Ações", clique no menu suspenso e selecione **Acesso: somente leitura**.

![Screenshot da seção "Permissões de repositório" para um novo aplicativo GitHub. A permissão "Ações" aparece como "Somente leitura" e está destacada em laranja.](/assets/images/help/actions/actions-repo-permissions-read-only.png)

1. À direita de "Implantações", clique no menu suspenso e selecione **Acesso: Leitura e gravação**.

![Screenshot da seção "Permissões de repositório" para um novo aplicativo GitHub. A permissão de Implantações mostra "Leitura e gravação" e está destacada em laranja.](/assets/images/help/actions/actions-deployments-repo-permissions-read-and-write.png)

1. Em "Inscrever-se em eventos", selecione **Regra de proteção de implantação**.

![Captura de tela da seção "Inscrever-se em eventos" para um novo aplicativo GitHub. A caixa de seleção da regra de proteção de implantação está destacada em laranja.](/assets/images/help/actions/actions-subscribe-to-events-deployment-protection-rules.png)

1. Instale a regra de proteção de implantação personalizada em seus repositórios e habilite-a para uso. Para saber mais, confira [Configurar regras de proteção de implantação personalizadas](configure-custom-protection-rules.md).

## Aprovar ou rejeitar implantações

Depois que um fluxo de trabalho atinge um trabalho que faz referência a um ambiente com a regra de proteção de implantação personalizada habilitada, GitHub envia uma solicitação `POST` para um URL que você configura contendo a payload `deployment_protection_rule`. Você pode escrever sua regra de proteção de implantação para enviar automaticamente solicitações de API REST que aprovem ou rejeitem a implantação com base na carga `deployment_protection_rule`. Configure suas solicitações de API REST da seguinte maneira.

As regras de proteção de implantação personalizadas não são compatíveis quando o ambiente de um trabalho de fluxo de trabalho é definido como `deployment: false`. Para saber mais, confira [Implantando com GitHub Actions](control-deployments.md#interaction-with-protection-rules).

1. Valide a solicitação de `POST` recebida. Para saber mais, confira [Validação de entregas de webhooks](https://docs.github.com/pt/webhooks/using-webhooks/validating-webhook-deliveries#validating-webhook-deliveries).

2. Use um JSON Web Token para se autenticar como GitHub App. Para saber mais, confira [Autenticando como aplicativo GitHub](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app#about-authentication-as-a-github-app).

3. Usando o ID de instalação do payload do webhook `deployment_protection_rule`, gere um token de instalação. Para saber mais, confira [Sobre a autenticação com um aplicativo GitHub](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app#authentication-as-a-github-app).

            ```shell
   curl --request POST \
   --url "https://api.github.com/app/installations/INSTALLATION_ID/ACCESS_TOKENS" \
   --header "Accept: application/vnd.github+json" \
   --header "Authorization: Bearer {jwt}" \
   --header "Content-Type: application/json" \
   --data \
   '{ \
      "repository_ids": [321], \
      "permissions": { \
         "deployments": "write" \
      } \
   }'
   ```

4. Opcionalmente, para adicionar um relatório de status a GitHub sem realizar nenhuma outra ação, envie uma solicitação `POST` para `/repos/OWNER/REPO/actions/runs/RUN_ID/deployment_protection_rule`. No corpo da solicitação, omita o `state`. Para saber mais, confira [Endpoints da API REST para execuções de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#review-custom-deployment-protection-rules-for-a-workflow-run). Você pode postar um relatório status na mesma implantação até 10 vezes. Os relatórios de status dão suporte à formatação Markdown e podem ter até 1.024 caracteres.

5. Para aprovar ou rejeitar uma solicitação, envie uma solicitação `POST` para `/repos/OWNER/REPO/actions/runs/RUN_ID/deployment_protection_rule`. No corpo da solicitação, defina a propriedade `state` como `approved` ou `rejected`. Para saber mais, confira [Endpoints da API REST para execuções de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#review-custom-deployment-protection-rules-for-a-workflow-run).

6. Opcionalmente, solicite o status de uma aprovação para um fluxo de trabalho executado enviando uma solicitação `GET` para `/repos/OWNER/REPOSITORY_ID/actions/runs/RUN_ID/approvals`. Para saber mais, confira [Endpoints da API REST para execuções de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#get-the-review-history-for-a-workflow-run).

7. Opcionalmente, revise a implantação em GitHub. Para saber mais, confira [Revisar implantações](review-deployments.md).

## Publicando regras de proteção de implantação personalizadas no GitHub Marketplace

Você pode publicar o GitHub App no GitHub Marketplace para permitir que os desenvolvedores encontrem regras de proteção adequadas e as instalem em seus repositórios GitHub. Ou você pode navegar pelas regras de proteção de implantação personalizadas existentes para atender às suas necessidades. Para saber mais, confira [Sobre GitHub Marketplace para aplicativos](https://docs.github.com/pt/apps/github-marketplace/github-marketplace-overview/about-github-marketplace-for-apps) e [Listando um aplicativo no GitHub Marketplace](https://docs.github.com/pt/apps/github-marketplace/listing-an-app-on-github-marketplace).
