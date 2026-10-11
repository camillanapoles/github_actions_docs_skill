---
title: Como gerenciar ações personalizadas
description: Saiba como criar e gerenciar suas próprias ações e personalizar ações compartilhadas pela GitHub comunidade.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/manage-custom-actions
captured: '2026-10-11'
section: GitHub Actions
---

# Como gerenciar ações personalizadas

_Saiba como criar e gerenciar suas próprias ações e personalizar ações compartilhadas pela GitHub comunidade._

## Definir o local da ação

Se você estiver desenvolvendo uma ação a ser usada por outras pessoas, recomendamos manter a ação no próprio repositório em vez de criar um pacote dela com outro código de aplicativo. Assim, você poderá controlar as versões e monitorar a ação como qualquer outro software.

Armazenar uma ação em seu próprio repositório torna mais fácil para a GitHub comunidade descobrir a ação, restringe o escopo da base de códigos para desenvolvedores corrigirem problemas e estenderem a ação e desacoplar o controle de versão da ação do controle de versão de outro código do aplicativo.

Se você estiver criando uma ação que não planeja disponibilizar para outras pessoas, poderá  armazenar os arquivos da ação em qualquer local em seu repositório. Se você pretende combinar a ação, o fluxo de trabalho e o código do aplicativo em um só repositório, recomendamos armazenar a ação no diretório `.github`. Por exemplo, `.github/actions/action-a` e `.github/actions/action-b`.

## Garantir a compatibilidade com outras plataformas

Muitas pessoas acessam GitHub em um domínio diferente GitHub.comde , como GHE.com ou um domínio personalizado para GitHub Enterprise Server.

Para garantir que a sua ação seja compatível com outras plataformas, não use referências embutidas em código para URLs de API, como `https://api.github.com`. Em vez disso, você pode:

* Usar variáveis de ambiente (consulte [Referência de variáveis](../../reference/workflows-and-actions/variables.md#default-environment-variables)):

  * Para a API REST, use a variável de ambiente `GITHUB_API_URL`.
  * Para o GraphQL, use a variável de ambiente `GITHUB_GRAPHQL_URL`.

* Usar um kit de ferramentas, como [`@actions/github`](https://github.com/actions/toolkit/tree/main/packages/github), que possa definir automaticamente as URLs corretas.

## Usando gerenciamento de versão em ações

Se você estiver desenvolvendo uma ação para outras pessoas usarem, recomendamos que você use o gerenciamento de versão para controlar como você distribui as atualizações. Os usuários podem esperar que a versão de patch de uma ação inclua os pachtes de segurança e as correções críticas necessárias, mas permaneça compatível com os fluxos de trabalho existentes. Você deve considerar lançar uma nova versão principal sempre que as suas alterações afetarem a compatibilidade.

Nessa abordagem de gerenciamento de versão, os usuários não devem fazer referência ao branch-padrão da ação, uma vez que é provável que contenha o último código e, consequentemente, pode ser instável. Em vez disso, você pode recomendar que os usuários especifiquem uma versão principal ao usar a sua ação e direcioná-los para uma versão mais específica somente se encontrarem problemas.

Para usar uma versão de ação específica, os usuários podem configurar seu GitHub Actions fluxo de trabalho para direcionar uma marca, um SHA de confirmação ou um branch nomeado para uma versão.

### Usar tags para o gerenciamento de versão

> \[!NOTE] Se você habilitou versões imutáveis para ajudar a evitar ataques de cadeia de fornecedores e alterações acidentais em suas versões, consulte [Como usar versões e marcas imutáveis para gerenciar as versões da sua ação](using-immutable-releases-and-tags-to-manage-your-actions-releases.md).

Recomendamos o uso de tags para gerenciamento da versão de ações. Ao usar essa abordagem, os seus usuários poderão distinguir facilmente as versões principais e não principais:

1. Desenvolver e validar uma versão em um branch de lançamento (por exemplo, `release/v1`).
2. Criar uma versão com uma tag de versão usando controle de versão semântico (por exemplo, `v1.0.1`). Para saber mais, confira [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository).
3. Mover a marcação de versão principal (como `v1`) a fim de apontar para a referência do Git da versão atual. Para saber mais, confira [Noções básicas do Git – Marcação](https://git-scm.com/book/en/v2/Git-Basics-Tagging).
4. Introduza uma nova tag de versão principal (por exemplo, `v2`) para alterações que interromperão fluxos de trabalho existentes, como alterar as entradas de uma ação.

#### Sintaxe para referenciar tags

Este exemplo demonstra como um usuário pode fazer referência a uma tag da versão principal:

```yaml
steps:
    - uses: actions/javascript-action@v1
```

Este exemplo demonstra como um usuário pode fazer referência a uma tag da versão do patch:

```yaml
steps:
    - uses: actions/javascript-action@v1.0.1
```

### Usar branches para gerenciamento de versão

Se você preferir usar nomes de branch para gerenciamento de versão, este exemplo irá demonstrar como fazer referência a um branch nomeado:

```yaml
steps:
    - uses: actions/javascript-action@v1-beta
```

### Usar um SHA do commit para o gerenciamento de versão

Cada commit do Git recebe um valor SHA calculado, que é único e imutável. Os usuários da sua ação podem preferir depender de um valor SHA do commit, uma vez que esta abordagem pode ser mais confiável do que especificar uma tag, que pode ser excluída ou movida. No entanto, isso significa que os usuários não receberão mais atualizações realizadas na ação. Você deve usar o valor SHA completo de um commit e não um valor abreviado.

```yaml
steps:
    - uses: actions/javascript-action@a824008085750b8e136effc585c3cd6082bd575f
```

## Criar um arquivo README para a ação

Se você planeja compartilhar sua ação publicamente, é recomendável criar um arquivo README para ajudar as pessoas a saberem como usar a ação. Você pode incluir estas informações no `README.md`:

* Descrição detalhada do que a ação faz;
* Argumentos obrigatórios de entrada e saída;
* Argumentos opcionais de entrada e saída;
* Segredos usados pela ação;
* Variáveis de ambiente usadas pela ação;
* Um exemplo de uso da ação no fluxo de trabalho.
