---
title: Publicar ações no GitHub Marketplace
description: Você pode publicar ações em GitHub Marketplace e compartilhar as ações que você criou com a comunidade GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/publish-in-github-marketplace
captured: '2026-10-11'
section: GitHub Actions
---

# Publicar ações no GitHub Marketplace

_Você pode publicar ações em GitHub Marketplace e compartilhar as ações que você criou com a comunidade GitHub._

## Pré-requisitos

> \[!NOTE]
> Você deve aceitar os termos de serviço para publicar ações em GitHub Marketplace.

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

   > \[!NOTE]
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
3. Ao lado da versão que você deseja editar, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-pencil" aria-label="Edit" role="img"><path d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"></path></svg>.

   ![Captura de tela de uma versão na lista de versões. Um ícone de lápis é realçado com um contorno laranja.](/assets/images/help/releases/edit-release-pencil.png)
4. Selecione **Publicar esta ação para a GitHub Marketplace** para remover a marca da caixa.
5. Clique em **Atualizar versão** na parte inferior da página.

## Transferência de um repositório de ações

É possível transferir um repositório de ações para outro usuário ou organização. Para saber mais, confira [Transferir um repositório](https://docs.github.com/pt/repositories/creating-and-managing-repositories/transferring-a-repository).

Quando um administrador do repositório transfere um repositório de ações, GitHub cria automaticamente um redirecionamento da URL anterior para a nova URL, o que significa que os fluxos de trabalho que usam a ação afetada não precisam ser atualizados.

As ações publicadas em GitHub Marketplace são vinculadas a um repositório pelo seu identificador exclusivo `name`, o que significa que você pode publicar novas versões de uma ação a partir do repositório transferido na mesma listagem em GitHub Marketplace. Se um repositório de ações for excluído, a GitHub Marketplace listagem também será excluída e o identificador exclusivo `name` ficará disponível.

> \[!NOTE]
> O selo "Verificado" visto no perfil de GitHub uma organização é diferente do selo do criador verificado em GitHub Marketplace. Se você transferir um repositório de ações, a GitHub Marketplace listagem perderá o selo do criador verificado, a menos que o novo proprietário também seja um criador verificado.

## Sobre emblemas em GitHub Marketplace

Ações com o <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-verified" aria-label="The verified badge" role="img"><path d="m9.585.52.929.68c.153.112.331.186.518.215l1.138.175a2.678 2.678 0 0 1 2.24 2.24l.174 1.139c.029.187.103.365.215.518l.68.928a2.677 2.677 0 0 1 0 3.17l-.68.928a1.174 1.174 0 0 0-.215.518l-.175 1.138a2.678 2.678 0 0 1-2.241 2.241l-1.138.175a1.17 1.17 0 0 0-.518.215l-.928.68a2.677 2.677 0 0 1-3.17 0l-.928-.68a1.174 1.174 0 0 0-.518-.215L3.83 14.41a2.678 2.678 0 0 1-2.24-2.24l-.175-1.138a1.17 1.17 0 0 0-.215-.518l-.68-.928a2.677 2.677 0 0 1 0-3.17l.68-.928c.112-.153.186-.331.215-.518l.175-1.14a2.678 2.678 0 0 1 2.24-2.24l1.139-.175c.187-.029.365-.103.518-.215l.928-.68a2.677 2.677 0 0 1 3.17 0ZM7.303 1.728l-.927.68a2.67 2.67 0 0 1-1.18.489l-1.137.174a1.179 1.179 0 0 0-.987.987l-.174 1.136a2.677 2.677 0 0 1-.489 1.18l-.68.928a1.18 1.18 0 0 0 0 1.394l.68.927c.256.348.424.753.489 1.18l.174 1.137c.078.509.478.909.987.987l1.136.174a2.67 2.67 0 0 1 1.18.489l.928.68c.414.305.979.305 1.394 0l.927-.68a2.67 2.67 0 0 1 1.18-.489l1.137-.174a1.18 1.18 0 0 0 .987-.987l.174-1.136a2.67 2.67 0 0 1 .489-1.18l.68-.928a1.176 1.176 0 0 0 0-1.394l-.68-.927a2.686 2.686 0 0 1-.489-1.18l-.174-1.137a1.179 1.179 0 0 0-.987-.987l-1.136-.174a2.677 2.677 0 0 1-1.18-.489l-.928-.68a1.176 1.176 0 0 0-1.394 0ZM11.28 6.78l-3.75 3.75a.75.75 0 0 1-1.06 0L4.72 8.78a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L7 8.94l3.22-3.22a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg>, ou selo de criador verificado, indicam que GitHub verificou o criador da ação como uma organização parceira. Os parceiros podem enviar um email para <a href="mailto:partnerships@github.com"><partnerships@github.com></a> a fim de solicitar o selo de criador verificado.

![Captura de tela do GitHub Actions com o selo de criador verificado.](/assets/images/marketplace/verified-creator-badge-for-actions.png)
