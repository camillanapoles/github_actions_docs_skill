---
title: Usar rótulos com os executores auto-hospedados
description: Você pode usar etiquetas para organizar os seus executores auto-hospedados com base em suas características.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/self-hosted-runners/apply-labels
captured: '2026-10-11'
section: How tos / Manage runners / Self hosted runners
---

# Usar rótulos com os executores auto-hospedados { #using-labels-with-self-hosted-runners }

_Você pode usar etiquetas para organizar os seus executores auto-hospedados com base em suas características._

Para obter informações sobre como usar rótulos para direcionar trabalhos para tipos específicos de executores auto-hospedados, consulte [Usar os executores auto-hospedados em um fluxo de trabalho](use-in-a-workflow.md). Você também pode direcionar trabalhos para executores em um grupo específico. Para saber mais, confira [Escolhendo o executor para um trabalho](../../write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md#choosing-runners-in-a-group).

Um executor auto-hospedado pode estar localizado no repositório, na organização ou nas configurações de conta corporativa do GitHub. Para gerenciar um executor auto-hospedado, você deve ter as seguintes permissões, dependendo de onde o executor auto-hospedado foi adicionado:

* **Repositório do usuário**: você precisa ser o proprietário do repositório.
* **Organização**: você precisa ser um proprietário da organização.
* **Repositório da organização**: você precisa ser um proprietário da organização ou ter acesso de administrador no repositório.

## Criar etiquetas personalizadas { #creating-a-custom-label }

Você pode criar rótulos personalizados para executores nos níveis de repositório e organização.

* [Criar um rótulo personalizado para um executor de repositório](#creating-a-custom-label-for-a-repository-runner)
* [Criar um rótulo personalizado para um executor de organização](#creating-a-custom-label-for-an-organization-runner)

!!! note
    Os rótulos são insensíveis a maiúsculas e minúsculas.

### Criar um rótulo personalizado para um executor de repositório { #creating-a-custom-label-for-an-organization-runner }

1. Acesse a página principal do repositório onde o grupo de executor auto-hospedado está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de executores, clique no nome do executor que você deseja configurar.
5. Na seção "Etiquetas", clique em (The Gear icon).
6. No campo "Localizar ou criar um rótulo", digite o nome do novo rótulo e clique em **Criar rótulo**. O rótulo personalizado é criado e atribuído ao executor auto-hospedado. É possível remover as etiquetas personalizadas dos executores auto-hospedados, mas não é possível excluí-las manualmente. Quaisquer etiquetas não utilizadas que não forem atribuídas a um executor serão automaticamente excluídas dentro de 24 horas.

### Criar um rótulo personalizado para um executor de organização { #creating-a-custom-label-for-an-enterprise-runner }

1. Navegue até a página principal da organização onde seu grupo de executores auto-hospedados está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na lista de executores, clique no nome do executor que você deseja configurar.
5. Na seção "Etiquetas", clique em (The Gear icon).
6. No campo "Localizar ou criar um rótulo", digite o nome do novo rótulo e clique em **Criar rótulo**. O rótulo personalizado é criado e atribuído ao executor auto-hospedado. É possível remover as etiquetas personalizadas dos executores auto-hospedados, mas não é possível excluí-las manualmente. Quaisquer etiquetas não utilizadas que não forem atribuídas a um executor serão automaticamente excluídas dentro de 24 horas.

## Atribuir uma etiqueta a um executor auto-hospedado { #assigning-a-label-to-a-self-hosted-runner }

Você pode atribuir rótulos a executores auto-hospedados nos níveis de repositório e organização.

* [Atribuir um rótulo a um executor de repositório](#assigning-a-label-to-a-repository-runner)
* [Atribuir um rótulo a um executor de organização](#assigning-a-label-to-an-organization-runner)

### Atribuir um rótulo a um executor de repositório { #assigning-a-label-to-a-repository-runner }

1. Acesse a página principal do repositório onde o grupo de executor auto-hospedado está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na seção "Etiquetas", clique em (The Gear icon).
5. Para atribuir uma etiqueta ao executor auto-hospedado, no campo "Localizar ou criar uma etiqueta", clique na etiqueta.

### Atribuir um rótulo a um executor de organização { #assigning-a-label-to-an-organization-runner }

1. Navegue até a página principal da organização onde seu grupo de executores auto-hospedados está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na seção "Etiquetas", clique em (The Gear icon).
5. Para atribuir uma etiqueta ao executor auto-hospedado, no campo "Localizar ou criar uma etiqueta", clique na etiqueta.

## Remover uma etiqueta personalizada de um executor auto-hospedado { #removing-a-custom-label-from-a-self-hosted-runner }

Você pode remover rótulos personalizados de executores auto-hospedados nos níveis de repositório e organização.

* [Remover um rótulo personalizado de um executor de repositório](#removing-a-custom-label-from-a-repository-runner)
* [Remover um rótulo personalizado de um executor de organização](#removing-a-custom-label-from-an-organization-runner)

### Remover um rótulo personalizado de um executor de repositório { #removing-a-custom-label-from-a-repository-runner }

1. Acesse a página principal do repositório onde o grupo de executor auto-hospedado está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na seção "Etiquetas", clique em (The Gear icon).
5. No campo "Localizar ou criar um rótulo", os rótulos atribuídos são marcados com o ícone (The Check icon). Clique em uma etiqueta marcada para cancelar a atribuição do seu executor auto-hospedado.

### Remover um rótulo personalizado de um executor de organização { #removing-a-custom-label-from-an-organization-runner }

1. Navegue até a página principal da organização onde seu grupo de executores auto-hospedados está registrado.
2. Clique em **(gear) Settings**.
3. Na barra lateral esquerda, clique em **(play) Actions** e clique em **Runners**.
4. Na seção "Etiquetas", clique em (The Gear icon).
5. No campo "Localizar ou criar um rótulo", os rótulos atribuídos são marcados com o ícone (The Check icon). Clique em uma etiqueta marcada para cancelar a atribuição do seu executor auto-hospedado.

## Atribuir rótulos programaticamente { #programmatically-assign-labels }

É possível atribuir rótulos programaticamente a um executor auto-hospedado após a criação dele ou durante sua configuração inicial.

* Para atribuir rótulos programaticamente a um executor auto-hospedado existente, você deve usar a API REST. Para saber mais, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners).
* Para atribuir rótulos programaticamente a um executor auto-hospedado durante a configuração inicial dele, transmita nomes de rótulo ao script `config` usando o parâmetro `labels`.

!!! note

  > Não é possível usar o script `config` para atribuir rótulos a um executor auto-hospedado existente.

  Por exemplo, o seguinte comando atribui um rótulo `gpu` durante a configuração de um novo executor auto-hospedado:

        ```shell
  ./config.sh --url <REPOSITORY_URL> --token <REGISTRATION_TOKEN> --labels gpu
        ```

  Caso não exista, a etiqueta será criada. Use também essa abordagem para atribuir os rótulos padrão aos executores, como `x64` ou `linux`. Quando os rótulos padrão são atribuídos usando o script de configuração, GitHub Actions aceita-os conforme determinado e não valida que o executor está realmente usando esse sistema operacional ou arquitetura.

  Você pode usar a separação por vírgula para atribuir múltiplas etiquetas. Por exemplo:

        ```shell
  ./config.sh --url <REPOSITORY_URL> --token <REGISTRATION_TOKEN> --labels gpu,x64,linux
        ```

!!! note

  > Se você substituir um executor existente, deverá reatribuir todos os rótulos personalizados.
