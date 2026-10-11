---
title: Publicar ações no GitHub Marketplace
description: Você pode publicar ações em GitHub Marketplace e compartilhar as ações que você criou com a comunidade GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace
captured: '2026-10-11'
section: How tos / Create and publish actions
---

# Publicar ações no GitHub Marketplace

_Você pode publicar ações em GitHub Marketplace e compartilhar as ações que você criou com a comunidade GitHub._

## Pré-requisitos

!!! note
    Você deve aceitar os termos de serviço para publicar ações em GitHub Marketplace.

Antes de poder publicar uma ação, você deverá criar uma ação no seu repositório. Para saber mais, confira [Reutilização de automações](../reuse-automations.md).

Ao planejar publicar sua ação em GitHub Marketplace, você precisará garantir que o repositório inclua apenas o arquivo de metadados, o código e os arquivos necessários para a ação. Criar um repositório único para a ação permite que você identifique, lance e empacote o código em uma única unidade.
GitHub também usa os metadados da ação na sua página GitHub Marketplace.

As ações são publicadas em GitHub Marketplace imediatamente e não são revisadas por GitHub, desde que atendam a estes requisitos:

* A ação precisa estar em um repositório público.
* Cada repositório precisa conter um só arquivo de metadados de ação (`action.yml` ou `action.yaml`) na raiz.
  * Os repositórios podem incluir outros arquivos de metadados de ações em subpastas, mas eles não serão listados automaticamente no marketplace.
* O `name` no arquivo de metadados da ação precisa ser único.
  * O `name` não pode ter o mesmo nome de uma ação existente publicada em GitHub Marketplace.
  * O `name` não pode corresponder a um usuário ou a uma organização em GitHub, a menos que o usuário ou o proprietário da organização esteja publicando a ação. Por exemplo, somente a GitHub organização pode publicar uma ação chamada `github`.
  * Não é possível que `name` corresponda a uma categoria GitHub Marketplace existente.
  * GitHub reserva os nomes dos GitHub recursos.

## Publicação de uma ação

Você pode adicionar a ação criada ao GitHub Marketplace marcando-a como uma nova versão e, em seguida, publicando-a.

Para criar uma nova versão e publicar a ação em GitHub Marketplace, siga estas instruções:

1. Em GitHub, acesse a página principal do repositório.

2. Navegue até o arquivo de metadados da ação em seu repositório (`action.yml`), e você verá um banner para publicar a ação no GitHub Marketplace. Clique em **Criar rascunho de uma versão**.

3. Em "Ação de Liberação", selecione **Publicar esta ação no GitHub Marketplace**.

!!! note

   > A caixa de seleção "Publicar" será desabilitada se a conta que possui o repositório ainda não tiver aceitado o Contrato de GitHub Marketplace Desenvolvedor. Se você tiver o repositório ou for um proprietário da organização, clique no link para "aceitar o Contrato de Desenvolvedor do GitHub Marketplace" e aceite o contrato. Se não houver nenhum link, envie ao proprietário da organização um link para esta página de "Ação de Liberação" e solicite que ele aceite o contrato.

4. Se os rótulos de seu arquivo de metadados tiverem algum problema, você receberá uma mensagem de erro ou uma mensagem de aviso. Resolva-os atualizando o arquivo de metadados. Após a conclusão, você verá a mensagem "Está tudo certo!" mensagem.

5. Selecione o menu suspenso **Categoria Primária** e clique em uma categoria que ajudará as pessoas a encontrar sua ação em GitHub Marketplace.

6. Opcionalmente, selecione o menu suspenso **Outra Categoria** e clique em uma categoria secundária.

7. No campo de tag, digite uma versão para a ação. Isso ajuda as pessoas a saber quais alterações ou recursos estão incluídos na versão. As pessoas verão a versão na página dedicada da ação GitHub Marketplace.

8. No campo de título, digite um título de versão.

9. Preencha todos os outros campos e clique em **Publicar versão**. A publicação exige a utilização de uma autenticação de dois fatores. Para saber mais, confira [Configurar a autenticação de dois fatores](https://docs.github.com/pt/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).

## Removendo uma ação de GitHub Marketplace

Para remover uma ação publicada de GitHub Marketplace, você precisará atualizar cada release publicada. Siga as etapas a seguir para cada versão da ação que você publicou em GitHub Marketplace.

1. Em GitHub, acesse a página principal do repositório.
2. À direita da lista de arquivos, clique em **Versões**.

   ![Captura de tela da página principal de um repositório. Um link, rotulado como "Versões", é realçado com um contorno laranja.](/assets/images/help/releases/release-link.png)
3. Ao lado da versão que você deseja editar, clique em (Edit).

   ![Captura de tela de uma versão na lista de versões. Um ícone de lápis é realçado com um contorno laranja.](/assets/images/help/releases/edit-release-pencil.png)
4. Selecione **Publicar esta ação para a GitHub Marketplace** para remover a marca da caixa.
5. Clique em **Atualizar versão** na parte inferior da página.

## Transferência de um repositório de ações

É possível transferir um repositório de ações para outro usuário ou organização. Para saber mais, confira [Transferir um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/transferring-a-repository).

Quando um administrador do repositório transfere um repositório de ações, GitHub cria automaticamente um redirecionamento da URL anterior para a nova URL, o que significa que os fluxos de trabalho que usam a ação afetada não precisam ser atualizados.

As ações publicadas em GitHub Marketplace são vinculadas a um repositório pelo seu identificador exclusivo `name`, o que significa que você pode publicar novas versões de uma ação a partir do repositório transferido na mesma listagem em GitHub Marketplace. Se um repositório de ações for excluído, a GitHub Marketplace listagem também será excluída e o identificador exclusivo `name` ficará disponível.

!!! note
    O selo "Verificado" visto no perfil de GitHub uma organização é diferente do selo do criador verificado em GitHub Marketplace. Se você transferir um repositório de ações, a GitHub Marketplace listagem perderá o selo do criador verificado, a menos que o novo proprietário também seja um criador verificado.

## Sobre emblemas em GitHub Marketplace

Ações com o (The verified badge), ou selo de criador verificado, indicam que GitHub verificou o criador da ação como uma organização parceira. Os parceiros podem enviar um email para [<partnerships@github.com>](mailto:partnerships@github.com) a fim de solicitar o selo de criador verificado.

![Captura de tela do GitHub Actions com o selo de criador verificado.](/assets/images/marketplace/verified-creator-badge-for-actions.png)
