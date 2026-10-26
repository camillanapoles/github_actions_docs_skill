---
title: OpenID Connect
description: O OpenID Connect permite que seus fluxos de trabalho troquem tokens de curta duração diretamente do seu provedor da nuvem.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/openid-connect
captured: '2026-10-26'
section: Concepts / Security
---

# OpenID Connect

_O OpenID Connect permite que seus fluxos de trabalho troquem tokens de curta duração diretamente do seu provedor da nuvem._

## Visão geral do OIDC (OpenID Connect)

GitHub Actions Os fluxos de trabalho geralmente são projetados para acessar um provedor de nuvem (como AWS, Azure, GCP, HashiCorp Vault e outros) para implantar software ou usar os serviços da nuvem. Antes que o fluxo de trabalho possa acessar esses recursos, ele fornecerá credenciais para o provedor da nuvem, como uma senha ou token. Essas credenciais geralmente são armazenadas como um segredo GitHube o fluxo de trabalho apresenta esse segredo para o provedor de nuvem sempre que ele é executado.

No entanto, o uso de segredos codificados requer que você crie credenciais no provedor de nuvem e depois duplicá-las como um segredo em GitHub.

Depois de estabelecer uma conexão de confiança com um provedor de nuvem que dá suporte ao OIDC, você pode configurar seu fluxo de trabalho para solicitar um token de acesso de curta duração diretamente do provedor de nuvem.

## Benefícios de usar o OIDC

Ao atualizar seus fluxos de trabalho para usar tokens do OIDC, você pode adotar as seguintes práticas recomendadas de segurança:

* **Nenhum segredo de nuvem:** Você não precisará duplicar suas credenciais de nuvem como segredos de GitHub longa duração. Em vez disso, você pode configurar a confiança do OIDC no seu provedor de nuvem, e, em seguida, atualizar seus fluxos de trabalho para solicitar um token de acesso curto do provedor de nuvem por meio do OIDC.
* **Gerenciamento de autenticação e autorização:** você tem um controle mais granular sobre como os fluxos de trabalho podem usar credenciais, usando as ferramentas de autenticação (authN) e autorização (authZ) do seu provedor de nuvem para controlar o acesso aos recursos da nuvem.
* **Credenciais rotativas:** com o OIDC, seu provedor de nuvem emite um token de acesso de curta duração, válido apenas para uma única tarefa, e que expira automaticamente em seguida.

## Como o OIDC se integra ao GitHub Actions

O diagrama a seguir fornece uma visão geral de como GitHubo provedor OIDC se integra aos fluxos de trabalho e ao provedor de nuvem:

![Diagrama de como um provedor de nuvem se integra ao GitHub Actions por meio de tokens de acesso e IDs de função de nuvem do token Web JSON.](https://docs.github.com/assets/images/help/actions/oidc-architecture.png)

1. Você estabelece uma relação de confiança OIDC no provedor de nuvem, permitindo que fluxos de trabalho específicos GitHub solicitem tokens de acesso à nuvem em nome de uma função de nuvem definida.
2. Sempre que seu trabalho é executado, o provedor OIDC do GitHub gera automaticamente um token OIDC. Esse token contém várias reivindicações para estabelecer uma identidade de segurança reforçada e verificável sobre o fluxo de trabalho específico que está tentando autenticar.
3. Uma etapa ou ação na tarefa do fluxo de trabalho pode solicitar um token do provedor OIDC de GitHub, que pode ser apresentado ao provedor de nuvem como prova da identidade do fluxo de trabalho.
4. Uma vez que o provedor de nuvem valida as reivindicações apresentadas no token, ele irá fornecer, posteriormente, um token de acesso à nuvem de curta duração que está disponível apenas para a duração do trabalho.

## Entendendo o token do OIDC

Cada trabalho solicita um token do OIDC do provedor OIDC de GitHub, que responde com um token web do JSON (JWT)gerado automaticamente que é único para cada trabalho de fluxo de trabalho em que é gerado. Quando o trabalho é executado, o token de OIDC é apresentado ao provedor de nuvem. Para validar o token, o provedor de nuvem verifica se o assunto do token do OIDC e outras reivindicações correspondem às condições que foram pré-configuradas na definição de confiança do OIDC da função da nuvem.

O exemplo de token OIDC a seguir usa uma entidade (`sub`) que referencia um ambiente de trabalho chamado `prod` no repositório `octo-org/octo-repo`.

```yaml
{
  "typ": "JWT",
  "alg": "RS256",
  "x5t": "example-thumbprint",
  "kid": "example-key-id"
}
{
  "jti": "example-id",
  "sub": "repo:octo-org/octo-repo:environment:prod",
  "environment": "prod",
  "aud": "https://github.com/octo-org",
  "ref": "refs/heads/main",
  "sha": "example-sha",
  "repository": "octo-org/octo-repo",
  "repository_owner": "octo-org",
  "actor_id": "12",
  "repository_visibility": "private",
  "repository_id": "74",
  "repository_owner_id": "65",
  "run_id": "example-run-id",
  "run_number": "10",
  "run_attempt": "2",
  "runner_environment": "github-hosted",
  "actor": "octocat",
  "workflow": "example-workflow",
  "head_ref": "",
  "base_ref": "",
  "event_name": "workflow_dispatch",
  "repo_property_workspace_id": "ws-abc123",
  "ref_type": "branch",
  "job_workflow_ref": "octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main",
  "iss": "https://token.actions.githubusercontent.com",
  "nbf": 1632492967,
  "exp": 1632493867,
  "iat": 1632493567
}
```

!!! note
    A `sub` declaração neste exemplo usa o formato anterior. Os repositórios criados após 15 de julho de 2026 usam um formato de assunto padrão imutável que inclui IDs do proprietário e do repositório (não disponível em GitHub Enterprise Server). Para saber mais, confira [Referência do OpenID Connect](../../reference/security/oidc.md#immutable-subject-claims).

## Autenticar ações personalizadas usando o OIDC

As ações personalizadas usam o método `getIDToken()` do kit de ferramentas do Ações ou de um comando `curl` para autenticar usando o OIDC.

Para saber mais, confira [Referência do OpenID Connect](../../reference/security/oidc.md#methods-for-requesting-the-oidc-token).

## Atualizando seus fluxos de trabalho para o OIDC

GitHub Actions os fluxos de trabalho podem usar tokens OIDC em vez de segredos para autenticar com provedores de nuvem. Muitos provedores de nuvem populares oferecem ações de logon oficiais que simplificam o processo de uso do OIDC em seus fluxos de trabalho. Para obter mais informações sobre como atualizar seus fluxos de trabalho com provedores de nuvem específicos, consulte [Reforço de segurança em suas implementações](../../how-tos/secure-your-work/security-harden-deployments.md).

## Usando propriedades personalizadas do repositório como declarações OIDC

Administradores corporativos e organizacionais podem incluir propriedades personalizadas do repositório como declarações em tokens OIDC. Isso permite políticas de ABAC (controle de acesso baseado em atributo) em seu provedor de nuvem, registro de artefato ou gerenciador de segredos que são orientados por metadados do repositório em vez de listas de permissões codificadas.

### Como funcionam as declarações de propriedade personalizadas

O fluxo de ponta a ponta para usar propriedades personalizadas como declarações OIDC é o seguinte:

1. **Definir propriedades personalizadas.** Uma organização ou administrador corporativo cria propriedades personalizadas (por exemplo, `business_unit`, `data_classification`ou `environment_tier`) e atribui valores a repositórios. Para obter mais informações, consulte [Como gerenciar propriedades personalizadas para repositórios na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization) e [Referência do OpenID Connect](../../reference/security/oidc.md#including-repository-custom-properties-in-oidc-tokens).
2. **Habilitar propriedades em tokens OIDC.** Uma organização ou administrador corporativo seleciona quais propriedades personalizadas devem ser incluídas em tokens OIDC, usando a interface do usuário de configurações ou a API REST.
3. **Reivindicações são exibidas automaticamente.** Cada execução de fluxo de trabalho em um repositório que tem um valor definido para uma propriedade habilitada incluirá esse valor em seu token OIDC, prefixado com `repo_property_`. Nenhuma alteração de configuração no nível do fluxo de trabalho é necessária.
4. **Atualize as políticas de confiança na nuvem.** Atualize as condições de confiança do provedor de nuvem para avaliar as novas reivindicações `repo_property_*`, permitindo decisões de acesso refinadas e baseadas em atributos.

Como isso se baseia no modelo de credencial de curta duração OIDC existente do GitHub, nenhum segredo de longa duração é necessário e cada token tem seu escopo definido, é auditável e é rotacionado automaticamente por execução de fluxo de trabalho.

### Pré-requisitos

* As propriedades personalizadas já devem ser definidas no nível da organização ou da empresa. Para saber mais, confira [Como gerenciar propriedades personalizadas para repositórios na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization).
* Você deve ser um administrador da organização ou administrador corporativo.

### Adicionando uma propriedade personalizada a declarações de token OIDC

Para incluir uma propriedade personalizada em tokens OIDC, use a API REST ou a interface de configurações da sua organização ou empresa.

* **Usando a interface de usuário das configurações:** Navegue até a página de configurações de ações OIDC de sua organização ou empresa para exibir e gerenciar quais propriedades personalizadas estão incluídas em tokens OIDC.

* **Usando a API REST:** Envie uma `POST` solicitação ao `/orgs/{org}/actions/oidc/customization/properties/repo` ponto de extremidade para adicionar uma propriedade personalizada às declarações de token OIDC para sua organização. Para obter parâmetros de solicitação e detalhes completos, consulte a documentação da API REST para gerenciar propriedades personalizadas do OIDC: [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc).

### Exemplo de token OIDC com propriedades personalizadas

O exemplo a seguir mostra um token OIDC que inclui duas propriedades personalizadas: uma propriedade de seleção `business_unit` única e uma propriedade de cadeia de caracteres `workspace_id`. Cada propriedade personalizada aparece no token com o prefixo `repo_property_`.

```json
{
  "sub": "repo:my-org/my-repo:ref:refs/heads/main",
  "aud": "https://github.com/my-org",
  "repository": "my-org/my-repo",
  "repository_owner": "my-org",
  "ref": "refs/heads/main",
  "repo_property_business_unit": "payments",
  "repo_property_workspace_id": "ws-abc123"
}
```

Você pode usar as `repo_property_*` declarações nas condições de confiança do provedor de nuvem para criar políticas flexíveis de controle de acesso baseadas em atributo. Para obter mais informações sobre o formato de declaração, os tipos de propriedade com suporte e os limites, consulte [Referência do OpenID Connect](../../reference/security/oidc.md#including-repository-custom-properties-in-oidc-tokens).

## Suporte do OIDC para Dependabot

Dependabot pode usar o OIDC para autenticar com registros privados, eliminando a necessidade de armazenar credenciais de longa duração como segredos do repositório. Com a autenticação baseada em OIDC, os trabalhos de atualização Dependabot podem obter dinamicamente credenciais de curta duração do seu provedor de identidade de nuvem.

Dependabot dá suporte à autenticação OIDC para qualquer tipo de registro que usa `username` e `password` autenticação, quando o registro é hospedado no AWS CodeArtifact, Azure DevOps Artifacts ou JFrog Artifactory.

Os benefícios da autenticação OIDC para Dependabot são:

* **Segurança aprimorada:** Elimina credenciais estáticas e de longa duração de seus repositórios.
* **Gerenciamento mais simples:** Habilita o acesso seguro e compatível com a política a registros privados.
* **Evite limitar a taxa:** As credenciais dinâmicas ajudam você a evitar atingir os limites de taxa associados a tokens estáticos.

Para saber mais, confira [Configurando o acesso a registros privados para Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-access-to-private-registries#using-oidc-for-authentication).

## Próximas etapas

Para saber mais sobre como configurar OIDC, confira [Reforço de segurança em suas implementações](../../how-tos/secure-your-work/security-harden-deployments.md).

Para obter informações de referência sobre o OIDC, consulte [Referência do OpenID Connect](../../reference/security/oidc.md).
