---
title: Configurando o OpenID Connect no Amazon Web Services
description: Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com Amazon Web Services.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
captured: '2026-10-13'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no Amazon Web Services

_Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com Amazon Web Services._

## Visão geral

O OIDC (OpenID Connect) permite que seus GitHub Actions fluxos de trabalho acessem recursos no AWS (Amazon Web Services), sem a necessidade de armazenar as credenciais do AWS como segredos de GitHub longa duração.

Este guia explica como configurar o AWS para confiar no GitHubOIDC como uma identidade federada e inclui um exemplo de fluxo de trabalho para o [`aws-actions/configure-aws-credentials`](https://github.com/aws-actions/configure-aws-credentials) que usa tokens para autenticar no AWS e acessar recursos.

!!! note
    O suporte para declarações personalizadas de OIDC não está disponível na AWS.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

## Adicionando o provedor de identidade ao AWS

Para adicionar o GitHub provedor OIDC ao IAM, consulte a [documentação do AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).

* Para a URL do provedor: Usar `https://token.actions.githubusercontent.com`
* Em "Público-alvo": use `sts.amazonaws.com` se você estiver usando a [ação oficial](https://github.com/aws-actions/configure-aws-credentials).

### Configurando a função e a política de confiança

Para configurar a função e a política de confiança no IAM, consulte a documentação da AWS [Configurar credenciais da AWS para ações do GitHub](https://github.com/aws-actions/configure-aws-credentials#configure-aws-credentials-for-github-actions) e [Configurando uma função para o provedor de identidade OIDC do GitHub](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html#idp_oidc_Create_GitHub).

!!! note
    O IAM (Gerenciamento de Identidade e Acesso) da AWS recomenda que os usuários avaliem a chave de condição do IAM, `token.actions.githubusercontent.com:sub`, na política de confiança de qualquer função que confie no provedor de identidade (IdP) OIDC do GitHub. A avaliação dessa chave de condição na política de confiança de função limita as ações GitHub que podem assumir a função.

Edite a política de confiança, adicionando o campo `sub` às condições de validação. Por exemplo:

```json copy
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:ref:refs/heads/octo-branch"
  }
}
```

Para repositórios criados após 15 de julho de 2026 ou que optaram por declarações de entidade imutáveis, a declaração `sub` inclui IDs de proprietário e repositório imutáveis (não disponíveis no GitHub Enterprise Server). Verifique se a política de confiança corresponde ao formato usado pelo repositório. Para saber mais, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#immutable-subject-claims).

```json copy
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:octo-org@123456/octo-repo@456789:ref:refs/heads/octo-branch"
  }
}
```

Se você usar um fluxo de trabalho com um ambiente, o campo `sub` deverá fazer referência ao nome do ambiente: `repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME`. Para saber mais, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#filtering-for-a-specific-environment).

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

```json copy
"Condition": {
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:environment:prod"
  }
}
```

No exemplo a seguir, `StringLike` é usado com um operador curinga (`*`) para permitir que qualquer branch, branch de mesclagem de solicitação de pull ou ambiente da organização `octo-org/octo-repo` e do repositório assuma uma função na AWS.

```json copy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Federated": "arn:aws:iam::123456123456:oidc-provider/token.actions.githubusercontent.com"
            },
            "Action": "sts:AssumeRoleWithWebIdentity",
            "Condition": {
                "StringLike": {
                    "token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:*"
                },
                "StringEquals": {
                    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
                }
            }
        }
    ]
}
```

## Atualizando seu GitHub Actions fluxo de trabalho

Para atualizar seus fluxos de trabalho para o OIDC, você deverá fazer duas alterações no seu YAML:

1. Adicionar configurações de permissões para o token.
2. Use a ação [`aws-actions/configure-aws-credentials`](https://github.com/aws-actions/configure-aws-credentials) para trocar o token OIDC (JWT) por um token de acesso à nuvem.

### Adicionando configurações de permissões

A execução do trabalho ou do fluxo de trabalho requer uma configuração `permissions` com [`id-token: write`](../../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token) para permitir que o provedor OIDC de GitHub crie um token JWT para cada execução.

> [!NOTE] A configuração de `id-token: write` nas permissões do fluxo de trabalho não concede ao fluxo de trabalho permissão para modificar ou gravar em qualquer recurso. Em vez disso, só permite que o fluxo de trabalho solicite (busque) e use (defina) um token OIDC para uma ação ou etapa. Esse token é então utilizado para autenticar com serviços externos, utilizando um token de acesso de curta duração.

Para obter informações detalhadas sobre permissões necessárias, exemplos de configuração e cenários avançados, confira [Referência do OpenID Connect](../../../reference/security/oidc.md#workflow-permissions-for-the-requesting-the-oidc-token).

### Solicitando o token de acesso

A `aws-actions/configure-aws-credentials` ação recebe um JWT do provedor OIDC GitHub e solicita um token de acesso da AWS. Para obter mais informações, confira a [documentação](https://github.com/aws-actions/configure-aws-credentials) da AWS.

* `BUCKET-NAME`: substitua isso pelo nome do bucket de S3.
* `AWS-REGION`: substitua pelo nome da sua região da AWS.
* `ROLE-TO-ASSUME`: substitua isso por sua função da AWS. Por exemplo, `arn:aws:iam::1234567890:role/example-role`

```yaml copy
```
# Sample workflow to access AWS resources when workflow is tied to branch
# The workflow creates a static website using Amazon S3
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
name: AWS example workflow
on:
  push
env:
  BUCKET_NAME : "BUCKET-NAME"
  AWS_REGION : "AWS-REGION"
# permission can be added at job level or workflow level
permissions:
  id-token: write   # This is required for requesting the JWT
  contents: read    # This is required for actions/checkout
jobs:
  S3PackageUpload:
    runs-on: ubuntu-latest
    steps:
      - name: Git clone the repository
        uses: actions/checkout@v6
      - name: configure aws credentials
        uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          role-to-assume: ROLE-TO-ASSUME
          role-session-name: samplerolesession
          aws-region: ${{ env.AWS_REGION }}
      # Upload a file to AWS s3
      - name: Copy index.html to s3
        run: |
          aws s3 cp ./index.html s3://${{ env.BUCKET_NAME }}/
```

```
## Leitura adicional

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](oidc-with-reusable-workflows.md)
* [Referência de executores auto-hospedados](../../../reference/runners/self-hosted-runners.md)
