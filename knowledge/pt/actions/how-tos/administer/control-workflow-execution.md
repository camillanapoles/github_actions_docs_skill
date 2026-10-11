---
title: Controlando quem pode executar GitHub Actions fluxos de trabalho
description: Controle quem pode disparar fluxos de trabalho GitHub Actions e quais eventos podem executá-los em toda a empresa, organização e repositório.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/administer/control-workflow-execution
captured: '2026-10-11'
section: GitHub Actions
---

# Controlando quem pode executar GitHub Actions fluxos de trabalho

_Controle quem pode disparar fluxos de trabalho GitHub Actions e quais eventos podem executá-los em toda a empresa, organização e repositório._

Com as proteções de execução de fluxo de trabalho, você pode definir uma lista de permissões que controla quem pode disparar GitHub Actions fluxos de trabalho e quais eventos têm permissão para executá-los. Para obter mais informações, consulte [Sobre as políticas do Actions](../../concepts/about-actions-policies.md).

<!-- expires 2026-11-02 -->

> \[!NOTE] GitHub adicionou uma política padrão que bloqueará o `pull_request_target` evento em repositórios públicos. Essa política será imposta em 2 de novembro de 2026. Consulte [Uso seguro de pull\_request\_target](../../reference/security/securely-using-pull_request_target.md#default-policy-for-pull_request_target).

<!-- end expires 2026-11-02 -->

## Preparando-se para adicionar proteções

Assim como os conjuntos de regras, as proteções de execução de fluxos de trabalho se sobrepõem a outras proteções no mesmo repositório, organização ou empresa.

Em vez de criar uma política grande por conta, recomendamos criar várias políticas claramente definidas e proteções em camadas entre níveis de conta. Os proprietários corporativos podem criar proteções no nível empresarial para políticas amplas e não negociáveis. Os proprietários da organização e os administradores do repositório podem adicionar a essas restrições.

Para cada política que você definir, pense em:

1. **Quais organizações ou repositórios** sua proteção terá como destino. Por exemplo, código aberto repositórios podem precisar de restrições mais rígidas sobre quem pode disparar fluxos de trabalho. Você pode direcionar repositórios por fatores como visibilidade, status de implantação ou propriedade personalizada.

   * O status de implantação é obtido do linked artifacts page de uma organização. Se isso for um fator importante, verifique se você está enviando registros de implantação sempre que um artefato for implantado. Consulte [Sobre artefatos vinculados](https://docs.github.com/pt/code-security/concepts/supply-chain-security/linked-artifacts).
   * Para criar e atribuir propriedades personalizadas, consulte [Como gerenciar propriedades personalizadas para repositórios na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization).

2. **Quais fluxos de trabalho** serão protegidos. Por exemplo, fluxos de trabalho que implantam código de produção podem precisar de um determinado nível de proteção, mas automações menos confidenciais podem não precisar do mesmo nível de proteção. Você pode definir o escopo de políticas para caminhos de fluxo de trabalho específicos ou fluxos de trabalho necessários.

3. **Quem deve ser capaz de executar esses fluxos de trabalho** nos repositórios que você está direcionando. Podem ser usuários com determinada função, contas de bot selecionadas ou uma equipe específica. Considere agrupar esses usuários em uma organização ou equipe empresarial para que eles possam ser facilmente contatados e referenciados em vários conjuntos de regras. Confira [Como criar uma equipe da organização](https://docs.github.com/pt/organizations/organizing-members-into-teams/creating-a-team) ou [Como criar equipes corporativas](https://docs.github.com/pt/enterprise-cloud@latest/admin/managing-accounts-and-repositories/managing-users-in-your-enterprise/create-enterprise-teams).

## Criando uma política de execução de fluxo de trabalho

Primeiro, crie uma nova política de Ações para o nível de conta em que você está trabalhando.

Em um repositório ou organização:

1. Clique na guia **Configurações**.
2. Na barra lateral esquerda, em **Ações**, clique em **Políticas**.

Em uma empresa:

1. Clique na guia **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-law" aria-label="law" role="img"><path d="M8.75.75V2h.985c.304 0 .603.08.867.231l1.29.736c.038.022.08.033.124.033h2.234a.75.75 0 0 1 0 1.5h-.427l2.111 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.006.005-.01.01-.045.04c-.21.176-.441.327-.686.45C14.556 10.78 13.88 11 13 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L12.178 4.5h-.162c-.305 0-.604-.079-.868-.231l-1.29-.736a.245.245 0 0 0-.124-.033H8.75V13h2.5a.75.75 0 0 1 0 1.5h-6.5a.75.75 0 0 1 0-1.5h2.5V3.5h-.984a.245.245 0 0 0-.124.033l-1.289.737c-.265.15-.564.23-.869.23h-.162l2.112 4.692a.75.75 0 0 1-.154.838l-.53-.53.529.531-.001.002-.002.002-.006.006-.016.015-.045.04c-.21.176-.441.327-.686.45C4.556 10.78 3.88 11 3 11a4.498 4.498 0 0 1-2.023-.454 3.544 3.544 0 0 1-.686-.45l-.045-.04-.016-.015-.006-.006-.004-.004v-.001a.75.75 0 0 1-.154-.838L2.178 4.5H1.75a.75.75 0 0 1 0-1.5h2.234a.249.249 0 0 0 .125-.033l1.288-.737c.265-.15.564-.23.869-.23h.984V.75a.75.75 0 0 1 1.5 0Zm2.945 8.477c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L13 6.327Zm-10 0c.285.135.718.273 1.305.273s1.02-.138 1.305-.273L3 6.327Z"></path></svg> Políticas** .
2. Na barra lateral esquerda, clique em **Ações** e em **Políticas**.

> \[!TIP] Para gerenciar políticas programaticamente, consulte [Pontos de extremidade da API REST para políticas de GitHub Actions](https://docs.github.com/pt/rest/actions/policies).

### Configurando a política

Em seguida, crie uma nova política.

1. Escolha um nome para a política.
2. Escolha um status de aplicação. Se você selecionar **Avaliar** (GitHub Enterprise Cloud somente), poderá monitorar quando os usuários atingirem a restrição nos insights de política.
3. Direcione seus fluxos de trabalho, organizações ou repositórios desejados.
4. Configure as seguintes proteções de execução de fluxo de trabalho.

### Restringir atores

Por padrão, cada usuário com acesso de gravação a um repositório pode disparar fluxos de trabalho. As regras para atores permitem separar quem contribui com código de quem executa sua integração contínua (CI), para que você possa conceder a um colaborador permissão de escrita sem conceder a ele a permissão de executar fluxos de trabalho.

Somente os atores permitidos poderão executar os fluxos de trabalho especificados no repositório de destino. Se você também restringir eventos, esses usuários só poderão disparar fluxos de trabalho com os eventos permitidos. Os atores não permitidos não poderão executar os fluxos de trabalho especificados.

GitHub os recursos estão isentos dessas restrições para os processos integrados nos quais são executados GitHub Actions. No entanto, se você criou fluxos de trabalho que precisam ser executados pela identidade associada a um GitHub recurso, como `dependabot[bot]`, então, essa identidade deve ser adicionada como um ator permitido.

### Restringir eventos

As regras de evento controlam quais eventos são permitidos, como`push`, , `pull_request`e `workflow_dispatch``pull_request_target`.

## Avaliando políticas

Você pode exibir insights de política para ver as execuções de fluxo de trabalho que foram bloqueadas (para políticas ativas) ou que teriam sido bloqueadas (para políticas de "avaliação"). Essa é uma boa maneira de verificar se as políticas estão funcionando conforme o esperado e não causando atritos desnecessários.

Para exibir insights, clique na página **Insights de política** . Você encontrará isso logo abaixo da página de políticas de GitHub Actions na barra lateral do seu repositório, organização ou empresa.
