---
title: Configurando OpenID Connect em provedores da nuvem
description: Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com provedores de nuvem.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
captured: '2026-10-13'
section: How tos / Secure your work / Security harden deployments
---

# Configurando OpenID Connect em provedores da nuvem

_Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com provedores de nuvem._

## Visão geral

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho acessem recursos em seu provedor de nuvem, sem precisar armazenar credenciais como segredos de GitHub longa duração.

Para usar o OIDC, primeiro você precisará configurar seu provedor de nuvem para confiar no GitHubOIDC como uma identidade federada e, em seguida, deve atualizar seus fluxos de trabalho para autenticar usando tokens.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

## Atualizando seu GitHub Actions fluxo de trabalho

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação oficial do seu provedor de nuvem para trocar o token OIDC (JWT) por um token de acesso em nuvem.

Se seu provedor de nuvem ainda não oferece uma ação oficial, você pode atualizar seus fluxos de trabalho para executar essas etapas manualmente.

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

### Adicionando configurações de permissões

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> [!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

### Usando ações oficiais

Se o provedor de nuvem tiver criado uma ação oficial para usar o OIDC, GitHub Actionsele permitirá que você troque facilmente o token OIDC por um token de acesso. Em seguida, você pode atualizar seus fluxos de trabalho para usar este token ao acessar recursos da nuvem.

Por exemplo, Alibaba Cloud criou [`aliyun/configure-aliyun-credentials-action`](https://github.com/aliyun/configure-aliyun-credentials-action) para integrar-se usando OIDC com GitHub.

## Usando ações personalizadas

Se o provedor de nuvem não tiver uma ação oficial ou se você preferir criar scripts personalizados, poderá solicitar manualmente o JWT (Token Web JSON) do GitHubprovedor OIDC.

Se você não estiver usando uma ação oficial, GitHub recomenda que você use o kit de ferramentas principal do Actions. Como alternativa, você pode usar as seguintes variáveis de ambiente para recuperar o token: `ACTIONS_ID_TOKEN_REQUEST_TOKEN` e `ACTIONS_ID_TOKEN_REQUEST_URL`.

Para atualizar seus fluxos de trabalho usando esta abordagem, você deverá fazer três alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Adicione o código que solicita o token OIDC do provedor OIDC de GitHub.
3. Adicione um código que troque o token OIDC com seu provedor de nuvem por um token de acesso.

### Solicitando o JWT usando o kit de ferramentas principal do Actions

O exemplo a seguir demonstra como usar `actions/github-script` com o kit de ferramentas `core` para solicitar o JWT do provedor OIDC de GitHub. Para saber mais, confira [Criando uma ação de JavaScript](../../../tutorials/create-actions/create-a-javascript-action.md#adding-actions-toolkit-packages).

```yaml
jobs:
  job:
    environment: Production
    runs-on: ubuntu-latest
    steps:
    - name: Install OIDC Client from Core Package
      run: npm install @actions/core@1.6.0 @actions/http-client
    - name: Get Id Token
      uses: actions/github-script@v8
      id: idtoken
      with:
        script: |
          let id_token = await core.getIDToken()
          core.setOutput('id_token', id_token)
```

### Solicitando o JWT usando variáveis de ambiente

O exemplo a seguir demonstra como usar variáveis de ambiente para solicitar um Token Web JSON.

Para seu trabalho de implantação, você precisará definir as configurações de token usando `actions/github-script` com o kit de ferramentas `core`. Para saber mais, confira [Criando uma ação de JavaScript](../../../tutorials/create-actions/create-a-javascript-action.md#adding-actions-toolkit-packages).

Por exemplo:

```yaml
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/github-script@v8
      id: script
      timeout-minutes: 10
      with:
        debug: true
        script: |
          const token = process.env['ACTIONS_ID_TOKEN_REQUEST_TOKEN']
          const runtimeUrl = process.env['ACTIONS_ID_TOKEN_REQUEST_URL']
          core.setOutput('TOKEN', token.trim())
          core.setOutput('IDTOKENURL', runtimeUrl.trim())
```

Em seguida, você pode usar `curl` para recuperar um JWT do provedor OIDC GitHub . Por exemplo:

```yaml
    - run: |
        IDTOKEN=$(curl -H "Authorization: Bearer ${{steps.script.outputs.TOKEN}}" ${{steps.script.outputs.IDTOKENURL}}  -H "Accept: application/json; api-version=2.0" -H "Content-Type: application/json" -d "{}" | jq -r '.value')
        echo $IDTOKEN
        jwtd() {
            if [[ -x $(command -v jq) ]]; then
                jq -R 'split(".") | .[0],.[1] | @base64d | fromjson' <<< "${1}"
                echo "Signature: $(echo "${1}" | awk -F'.' '{print $3}')"
            fi
        }
        jwtd $IDTOKEN
        echo "idToken=${IDTOKEN}" >> $GITHUB_OUTPUT
      id: tokenid
```

### Obtendo o token de acesso do provedor da nuvem

Você precisará apresentar o token web JSON do OIDC para seu provedor de nuvem a fim de obter um token de acesso.

Para cada implantação, seus fluxos de trabalho devem usar ações de login em nuvem (ou scripts personalizados) que buscam o token do OIDC e o apresentam ao seu provedor de nuvem. O provedor da nuvem valida as reivindicações no token; se for bem sucedido, ele fornece um token de acesso à nuvem que está disponível apenas para a execução do trabalho. O token de acesso fornecido pode ser usado por ações subsequentes no trabalho para conectar-se à nuvem e fazer a implantação nos seus recursos.

As etapas para trocar o token do OIDC por um token de acesso irão variar para cada provedor de nuvem.

### Acessando recursos no seu provedor da nuvem

Depois de obter o token de acesso, você pode usar as ações específicas da nuvem ou scripts para efetuar a autenticação no provedor da nuvem e fazer a implantação nos seus recursos. Essas etapas podem ser diferentes para cada provedor da nuvem.

Por exemplo, o Alibaba Cloud mantém suas próprias instruções para autenticação OIDC. Para obter mais informações, consulte [Visão geral do SSO baseado em OIDC](https://www.alibabacloud.com/help/en/ram/user-guide/overview-of-oidc-based-sso) na documentação do Alibaba Cloud.

Além disso, o tempo de expiração padrão desse token de acesso pode variar entre as nuvens e pode ser configurável no lado do provedor de nuvem.

## Leitura adicional

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
