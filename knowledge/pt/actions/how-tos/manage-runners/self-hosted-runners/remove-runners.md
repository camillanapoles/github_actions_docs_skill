---
title: Remover executores auto-hospedados
description: Você pode remover permanentemente um executor auto-hospedado de um repositório ou organização.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/remove-runners
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Remover executores auto-hospedados { #removing-self-hosted-runners }

_Você pode remover permanentemente um executor auto-hospedado de um repositório ou organização._

Você pode remover permanentemente um executor auto-hospedado de um repositório.

## Remover um executor de um repositório { #removing-a-runner-from-a-repository }

!!! note
    * Este procedimento remove permanentemente o executor auto-hospedado. Caso você deseje apenas impedir temporariamente que um executor seja atribuído a trabalhos, desligue o computador ou interrompa o aplicativo `run`. O executor permanecerá atribuído em um estado "Offline" e não executará nenhum trabalho até que você o reinicie usando o aplicativo `run`.
    * Um executor auto-hospedado é removido automaticamente do GitHub quando não se conecta ao GitHub Actions por mais de 14 dias. Um executor auto-hospedado efêmero é removido automaticamente do GitHub quando não se conecta ao GitHub Actions por mais de 1 dia.
    * Os executores JIT (Just-In-Time) só podem executar um único trabalho. Se os executores JIT nunca executarem um trabalho, eles serão removidos automaticamente. Para remover um executor JIT antes da remoção automática, você deve fazê-lo em GitHub.

Para remover um executor auto-hospedado de um repositório de usuário, você deve ser o proprietário do repositório. Os donos da organização podem remover um executor de um repositório na organização.

Recomendamos que você também tenha acesso à máquina do executor auto-hospedado.

Para obter informações sobre como remover um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

Como alternativa, se você não tiver acesso ao repositório ou organização no GitHub para remover um executor, mas quiser reutilizar o computador executor, poderá excluir o arquivo `.runner` no diretório do aplicativo executor auto-hospedado (ou seja, o diretório no qual você baixou e descompactou o software do executor). Isso permite que o runner seja registrado sem ter que baixar novamente o aplicativo do runner auto-hospedado.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de executores, clique no nome do executor que você deseja configurar.
5. Clique em **Remover**.
6. Você verá instruções para remover o executor auto-hospedado. Complete qualquer um dos seguintes passos para remover o executor, dependendo se ele ainda está acessível:

   * **Se você tiver acesso ao computador do executor:** siga as instruções na tela para que o sistema operacional do computador execute o comando de remoção. As instruções incluem a URL necessária e um token gerado automaticamente, limitado por tempo.

     O comando de remoção executa as seguintes tarefas:

     * Remove o executor do GitHub.
     * Remove todos os arquivos de configuração do aplicativo de executor auto-hospedado na máquina.
     * Remove todos os serviços configurados se não estiver em execução no modo interativo.

   * **Se você não tiver acesso ao computador:** clique em **Force remove this runner** para forçar o GitHub a remover o executor.

## Remover um executor de uma organização { #removing-a-runner-from-an-organization }

!!! note
    * Este procedimento remove permanentemente o executor auto-hospedado. Caso você deseje apenas impedir temporariamente que um executor seja atribuído a trabalhos, desligue o computador ou interrompa o aplicativo `run`. O executor permanecerá atribuído em um estado "Offline" e não executará nenhum trabalho até que você o reinicie usando o aplicativo `run`.
    * Um executor auto-hospedado é removido automaticamente do GitHub quando não se conecta ao GitHub Actions por mais de 14 dias. Um executor auto-hospedado efêmero é removido automaticamente do GitHub quando não se conecta ao GitHub Actions por mais de 1 dia.
    * Os executores JIT (Just-In-Time) só podem executar um único trabalho. Se os executores JIT nunca executarem um trabalho, eles serão removidos automaticamente. Para remover um executor JIT antes da remoção automática, você deve fazê-lo em GitHub.

Para remover um executor auto-hospedado de uma organização, você deve ser um proprietário. Recomendamos que você também tenha acesso à máquina do executor auto-hospedado. Para obter informações sobre como remover um executor auto-hospedado com a API REST, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).

Como alternativa, se você não tiver acesso ao repositório ou organização no GitHub para remover um executor, mas quiser reutilizar o computador executor, poderá excluir o arquivo `.runner` no diretório do aplicativo executor auto-hospedado (ou seja, o diretório no qual você baixou e descompactou o software do executor). Isso permite que o runner seja registrado sem ter que baixar novamente o aplicativo do runner auto-hospedado.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de executores, clique no nome do executor que você deseja configurar.
5. Clique em **Remover**.
6. Você verá instruções para remover o executor auto-hospedado. Complete qualquer um dos seguintes passos para remover o executor, dependendo se ele ainda está acessível:

   * **Se você tiver acesso ao computador do executor:** siga as instruções na tela para que o sistema operacional do computador execute o comando de remoção. As instruções incluem a URL necessária e um token gerado automaticamente, limitado por tempo.

     O comando de remoção executa as seguintes tarefas:

     * Remove o executor do GitHub.
     * Remove todos os arquivos de configuração do aplicativo de executor auto-hospedado na máquina.
     * Remove todos os serviços configurados se não estiver em execução no modo interativo.

   * **Se você não tiver acesso ao computador:** clique em **Force remove this runner** para forçar o GitHub a remover o executor.

## Remover um executor de uma empresa { #removing-a-runner-from-an-enterprise }

Se você usar GitHub Enterprise Cloud, também será possível remover executores de uma empresa. Para obter mais informações, consulte a [documentação do GitHub Enterprise Cloud](remove-runners.md#removing-a-runner-from-an-enterprise).
