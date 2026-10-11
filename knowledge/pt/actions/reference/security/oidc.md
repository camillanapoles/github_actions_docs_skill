---
title: Referência do OpenID Connect
description: Encontre informações sobre como usar o OpenID Connect (OIDC) para autenticar GitHub Actions fluxos de trabalho com provedores de nuvem.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/security/oidc
captured: '2026-10-11'
section: Reference / Security
---

# Referência do OpenID Connect

_Encontre informações sobre como usar o OpenID Connect (OIDC) para autenticar GitHub Actions fluxos de trabalho com provedores de nuvem._

## Declarações de token OIDC

Para ver todas as declarações com suporte pelo provedor OIDC do GitHub, verifique as entradas `claims_supported` em <https://token.actions.githubusercontent.com/.well-known/openid-configuration>.

O token OIDC inclui as declarações a seguir.

### Declarações de audiência, emissor e entidade padrão

| Declaração | Tipo de declaração | Descrição |
| --- | --- | --- |
| `aud` | Público | Por padrão, esta é a URL do proprietário do repositório, como a organização proprietária do repositório. Defina um público-alvo personalizado com um comando de kit de ferramentas: [`core.getIDToken(audience)`](https://www.npmjs.com/package/@actions/core/v/1.6.0) |
| `iss` | Emissor | O emissor do token OIDC: `https://token.actions.githubusercontent.com` |
| `sub` | Assunto | Define a declaração do sujeito que deve ser validada pelo provedor de nuvem. Esta configuração é essencial para garantir que os tokens de acesso sejam apenas alocados de forma previsível. Para repositórios que usam declarações de assunto imutáveis, o formato `sub` inclui IDs de proprietário e de repositório imutáveis (não disponíveis no GitHub Enterprise Server). |

### Parâmetros e declarações de cabeçalho JOSE padrão adicionais

| Parâmetro de cabeçalho | Tipo de parâmetro      | Descrição                                                    |
|----------------------|----------------------|------------------------------------------------------------|
| `alg`                  | Algoritmo              | O algoritmo usado pelo provedor OIDC.                        |
| `kid`                  | Identificador da chave | Chave exclusiva do token OIDC.                               |
| `typ`                  | Tipo                   | Descreve o tipo de token. Este é um token web do JSON (JWT). |

| Declaração | Tipo de declaração         | Descrição                                        |
|----------|--------------------------|------------------------------------------------|
| `exp`      | Expira em                  | Identifica o tempo de validade do JWT.           |
| `iat`      | Emitido em                 | A hora em que o JWT foi emitido.                 |
| `jti`      | Identificador do token JWT | Identificador exclusivo do token OIDC.           |
| `nbf`      | Não antes de               | O JWT não é válido para uso antes deste horário. |

### Declarações personalizadas fornecidas por GitHub

| Declaração | Descrição |
| --- | --- |
| `actor` | A conta pessoal que iniciou a execução do fluxo de trabalho. |
| `actor_id` | A ID da conta pessoal que iniciou a execução do fluxo de trabalho. |
| `base_ref` | O branch de destino do pull request na execução de um fluxo de trabalho. |
| `check_run_id` | A ID de verificação de execução do trabalho atual. |
| `environment` | O nome do ambiente usado pelo trabalho. Se a declaração `environment` for incluída (também via `include_claim_keys`), um ambiente será necessário e deverá ser fornecido. |
| `event_name` | O nome do evento que disparou a execução do fluxo de trabalho. Os tokens OIDC solicitados para Dependabot trabalhos de atualização usam `dynamic` como o valor. |
| `head_ref` | O branch de origem do pull request na execução de um fluxo de trabalho. |
| `job_workflow_ref` | Para trabalhos que usam um fluxo de trabalho reutilizável, o caminho de ref para o fluxo de trabalho reutilizável. Para saber mais, confira [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](../../how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows.md). |
| `job_workflow_sha` | Para trabalhos que usam um fluxo de trabalho reutilizável, o SHA de commit do arquivo de fluxo de trabalho reutilizável. |
| `ref` |  |
| *(Referência)* A referência do Git que disparou a execução de fluxo de trabalho. |  |
| `ref_type` | O tipo de `ref`, por exemplo: "branch". |
| `repository_visibility` | A visibilidade do repositório em que o fluxo de trabalho está sendo executado. Aceita os seguintes valores: `internal`, `private`, ou `public`. |
| `repository` | O repositório de onde o fluxo de trabalho está sendo executado. |
| `repository_id` | A ID do repositório do qual o fluxo de trabalho está sendo executado. |
| `repository_owner` | O nome da organização na qual o `repository` é armazenado. |
| `repository_owner_id` | A ID da organização na qual o `repository` é armazenado. |
| `repo_property_*` | Propriedades personalizadas definidas no nível da organização ou da empresa incluídas como declarações no token OIDC, prefixadas com `repo_property_`. Para obter mais informações, consulte [Incluir propriedades personalizadas do repositório em tokens OIDC](#including-repository-custom-properties-in-oidc-tokens). |
| `run_id` | O ID da execução que acionou o fluxo de trabalho. |
| `run_number` | O número de vezes que este fluxo de trabalho foi executado. |
| `run_attempt` | O número de vezes que este fluxo de trabalho foi reexecutado. |
| `runner_environment` | O tipo de executor usado pelo trabalho. Aceita os seguintes valores: `github-hosted` ou `self-hosted`. |
| `workflow` | Nome do fluxo de trabalho. |
| `workflow_ref` | O caminho de referência para o fluxo de trabalho. Por exemplo, `octocat/hello-world/.github/workflows/my-workflow.yml@refs/heads/my_branch`. |
| `workflow_sha` | O SHA de commit para o arquivo de fluxo de trabalho. |

## Declarações OIDC usadas para definir condições de confiança em funções de nuvem

As declarações de público-alvo e assunto são normalmente usadas em combinação, ao definir as condições da função/recursos em nuvem para definir o escopo do seu acesso aos fluxos de trabalho do GitHub.

* **Público-alvo**: por padrão, esse valor usa a URL do proprietário da organização ou do repositório. Isto pode ser usado para definir uma condição para que apenas os fluxos de trabalho na organização específica possam acessar a função da nuvem.
* **Assunto:** Por padrão, tem um formato predefinido e é uma concatenação de alguns dos principais metadados sobre o fluxo de trabalho, como a organização, o GitHub repositório, o branch ou o ambiente associado [`job`](../workflows-and-actions/workflow-syntax.md#jobsjob_idenvironment) . Confira [Exemplos de declarações de entidade](#example-subject-claims) para ver como a declaração de entidade é montada com base em metadados concatenados.

Se precisar de condições de confiança mais granulares, você poderá personalizar as declarações do do assunto (`sub`) que estão  incluídas no JWT. Para obter mais informações, confira [Personalizando as declarações de token](#customizing-the-token-claims).

Há também muitas reivindicações adicionais compatíveis com o token do OIDC que podem ser usadas para definir essas condições. Além disso, seu provedor de nuvem poderia permitir que você atribuísse uma função aos tokens de acesso, permitindo que você especifique ainda mais permissões granulares.

Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho.

!!! note
    Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem.

## Exemplos de reivindicações

Os exemplos a seguir demonstram como usar "Assunto" como condição e explicam como o "Assunto" é montado a partir de metadados concatenados. A [entidade](https://openid.net/specs/openid-connect-core-1_0.html#StandardClaims) usa as informações do [`job` contexto](../workflows-and-actions/contexts.md#job-context), e instrui seu provedor de nuvem a conceder tokens de acesso apenas para fluxos de trabalho em execução em ramificações e ambientes específicos. As seguintes secções descrevem alguns assuntos comuns que você pode usar.

### Filtragem para um ambiente específico

A reivindicação de assunto inclui o nome do ambiente quando o trabalho fizer referência a um ambiente.

Você pode configurar um assunto que filtra um nome de [ambiente](../../how-tos/deploy/configure-and-manage-deployments/manage-environments.md) específico. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado de um trabalho que tenha um ambiente chamado `Production`, em um repositório chamado `octo-repo` que pertence à organização `octo-org`:

* Sintaxe: `repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME`
* Exemplo: `repo:octo-org/octo-repo:environment:Production`

### Filtragem de eventos `pull_request`

A declaração de entidade inclui a cadeia de caracteres `pull_request` quando o fluxo de trabalho é disparado por um evento de solicitação de pull, mas apenas se o trabalho não referencia um ambiente.

Você pode configurar um tópico que filtra o evento [`pull_request`](../workflows-and-actions/events-that-trigger-workflows.md#pull_request). Neste exemplo, a execução de fluxo de trabalho precisa ter sido disparada por um evento `pull_request` em um repositório chamado `octo-repo` que pertence à organização `octo-org`:

* Sintaxe: `repo:ORG-NAME/REPO-NAME:pull_request`
* Exemplo: `repo:octo-org/octo-repo:pull_request`

### Filtrando um branch específico

A reivindicação de assunto inclui o nome do branch do fluxo de trabalho, mas somente se o trabalho não fizer referência a um ambiente e se o fluxo de trabalho não for acionado por um evento de pull request.

Você pode configurar um assunto que filtra para um nome de branch específico. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado de um branch chamado `demo-branch`, em um repositório chamado `octo-repo` que pertence à organização `octo-org`:

* Sintaxe: `repo:ORG-NAME/REPO-NAME:ref:refs/heads/BRANCH-NAME`
* Exemplo: `repo:octo-org/octo-repo:ref:refs/heads/demo-branch`

### Filtrando uma tag específica

A reivindicação de assunto inclui o nome da tag do fluxo de trabalho, mas somente se o trabalho não fizer referência a um ambiente e se o fluxo de trabalho não for acionado por um evento de pull request.

Você pode criar um assunto que filtra uma tag específica. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado com uma marca chamada `demo-tag`, em um repositório chamado `octo-repo` que pertence à organização `octo-org`:

* Sintaxe: `repo:ORG-NAME/REPO-NAME:ref:refs/tags/TAG-NAME`
* Exemplo: `repo:octo-org/octo-repo:ref:refs/tags/demo-tag`

### Filtragem de metadados que contêm `:`

Qualquer `:` presente nos valores de metadados será substituído por `%3A` na declaração de assunto.

Você pode configurar um tópico que inclui metadados contendo dois-pontos. Neste exemplo, a execução de fluxo de trabalho precisa ter se originado de um trabalho que tenha um ambiente chamado `Production:V1`, em um repositório chamado `octo-repo` que pertence à organização `octo-org`:

* Sintaxe: `repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME`
* Exemplo: `repo:octo-org/octo-repo:environment:Production%3AV1`

## Reivindicações de sujeito imutáveis

A especificação OIDC (OpenID Connect) requer que as declarações de assunto (`sub`) sejam exclusivas localmente e nunca reatribuídas. Anteriormente, o formato padrão `sub` usava apenas nomes de organização e repositório. Se um namespace foi reciclado, um proprietário diferente poderia criar o mesmo valor de assunto.

Para ajudar a evitar esse cenário, os repositórios criados após 15 de julho de 2026 agora usam um formato de assunto padrão imutável que inclui a ID do proprietário e a ID do repositório. Essa distribuição não inclui GitHub Enterprise Server.

* Sintaxe: `repo:OWNER@OWNER-ID/REPO@REPO-ID:ref:refs/heads/BRANCH`
* Exemplo de formato anterior: `repo:octo-org/octo-repo:ref:refs/heads/main`
* Exemplo de formato imutável: `repo:octo-org@123456/octo-repo@456789:ref:refs/heads/main`

O `@` separador é usado entre nomes e IDs porque `@` não pode aparecer em GitHub nomes de usuário ou de repositório.

Repositórios criados antes de 15 de julho de 2026 mantêm o formato anterior, a menos que você opte por declarações de assunto imutáveis. Você pode optar por aderir no nível da organização ou do repositório usando as configurações do OIDC na interface do usuário ou na API REST.

Renomeações e transferências de repositórios após 15 de julho de 2026 também passam a usar o formato de assunto imutável.

## Configurando o assunto no seu provedor de nuvem

Para configurar o assunto no relacionamento de confiança do seu provedor de nuvem, você deve adicionar a cadeia de caracteres do assunto à sua configuração de confiança. Os seguintes exemplos demonstram como vários provedores de nuvem podem aceitar a mesma entidade `repo:octo-org/octo-repo:ref:refs/heads/demo-branch` de diferentes maneiras:

| Provedor de nuvem | Exemplo |
| --- | --- |
| Amazon Web Services | `"token.actions.githubusercontent.com:sub": "repo:octo-org/octo-repo:ref:refs/heads/demo-branch"` |
| Azure | `repo:octo-org/octo-repo:ref:refs/heads/demo-branch` |
| Google Cloud Platform | `(assertion.sub=='repo:octo-org/octo-repo:ref:refs/heads/demo-branch')` |
| HashiCorp Vault | `bound_subject="repo:octo-org/octo-repo:ref:refs/heads/demo-branch"` |

Para repositórios criados após 15 de julho de 2026 ou que optaram por declarações de entidade imutáveis, a `sub` declaração inclui `owner_id` e `repo_id` conforme mostrado nos exemplos imutáveis. Atualize suas políticas de confiança para corresponder ao formato usado pelo repositório. As declarações de assunto imutáveis não estão disponíveis em GitHub Enterprise Server.

| Provedor de nuvem | Exemplo de formato imutável |
| --- | --- |
| Amazon Web Services | `"token.actions.githubusercontent.com:sub": "repo:octo-org@123456/octo-repo@456789:ref:refs/heads/demo-branch"` |
| Azure | `repo:octo-org@123456/octo-repo@456789:ref:refs/heads/demo-branch` |
| Google Cloud Platform | `(assertion.sub=='repo:octo-org@123456/octo-repo@456789:ref:refs/heads/demo-branch')` |
| HashiCorp Vault | `bound_subject="repo:octo-org@123456/octo-repo@456789:ref:refs/heads/demo-branch"` |

Para obter mais informações sobre como configurar provedores de nuvem específicos, confira os guias listados em [Reforço de segurança em suas implementações](../../how-tos/secure-your-work/security-harden-deployments.md).

## Personalizando as declarações de token

Você pode proteger a segurança da configuração do OIDC personalizando as declarações incluídas no JWT. Essas personalizações permitem definir condições de confiança mais granulares em suas funções de nuvem ao permitir que seus fluxos de trabalho acessem recursos hospedados na nuvem:

* Você pode personalizar valores para `audience` declarações. Consulte [Personalizando o valor de `audience`](#customizing-the-audience-value).

* Você pode personalizar o formato de sua configuração OIDC definindo condições na declaração de assunto (`sub`) que exigem que os tokens JWT sejam originados de um repositório específico, fluxo de trabalho reutilizável ou outra fonte.

* Você pode definir políticas OIDC granulares usando declarações de token OIDC adicionais, como `repository_id` e `repository_visibility`. Confira [OpenID Connect](../../concepts/security/openid-connect.md#understanding-the-oidc-token).

* Você pode incluir propriedades personalizadas do repositório como declarações em tokens OIDC, habilitando políticas de controle de acesso baseadas em atributo. Confira [Como incluir propriedades personalizadas do repositório em tokens OIDC](#including-repository-custom-properties-in-oidc-tokens).

### Como personalizar o valor de `audience`

Quando você usa ações personalizadas em seus fluxos de trabalho, essas ações podem usar o GitHub Actions Kit de Ferramentas para permitir que você forneça um valor personalizado para a `audience` declaração. Alguns provedores de nuvem também usam isso em suas ações oficiais de logon a fim de impor um valor padrão para a declaração `audience`. Por exemplo, a [GitHub Action for Azure Login](https://github.com/Azure/login/blob/master/action.yml) fornece um valor padrão `aud` de `api://AzureADTokenExchange` ou permite que você defina um valor `aud` personalizado em seus fluxos de trabalho. Para obter mais informações sobre o GitHub Actions Toolkit, consulte a seção [OIDC token](https://github.com/actions/toolkit/tree/main/packages/core#oidc-token) na documentação.

Se você não quiser usar o valor padrão `aud` oferecido por uma ação, você pode fornecer um valor personalizado para a reivindicação `audience`. Isso permite que você defina uma condição de que apenas fluxos de trabalho em um repositório ou organização específica possam acessar a função de nuvem. Se a ação que você está usando suporta isso, você pode usar a palavra-chave `with` no seu fluxo de trabalho para passar um valor personalizado `aud` para a ação. Para saber mais, confira [Referência de sintaxe de metadados](../workflows-and-actions/metadata-syntax.md#inputs).

### Incluindo propriedades personalizadas do repositório nos tokens OIDC

Os administradores da organização e da empresa podem selecionar propriedades personalizadas do repositório para incluir como declarações nos tokens OIDC do GitHub Actions. Depois que uma propriedade personalizada é adicionada à configuração do OIDC, cada repositório na organização ou na empresa que tem um valor definido para essa propriedade irá incluí-la automaticamente em seus tokens OIDC. O nome da propriedade aparece no token prefixado com `repo_property_`.

Isso permite que você crie políticas de ABAC (controle de acesso baseado em atributo) em seu provedor de nuvem que se associam diretamente aos metadados do repositório, reduzindo o descompasso de configuração e eliminando a necessidade de gerenciar a configuração de acesso separada para cada repositório.

#### Formato de declaração

Cada propriedade personalizada habilitada aparece como uma declaração separada no token OIDC. O nome da declaração é o nome da propriedade prefixado com `repo_property_`.

| Nome da propriedade personalizada | Nome da declaração no token OIDC    |
|---------------------------------|-----------------------------------|
| `business_unit`                   | `repo_property_business_unit`       |
| `workspace_id`                    | `repo_property_workspace_id`        |
| `data_classification`             | `repo_property_data_classification` |

#### Tipos de propriedade com suporte

Os seguintes tipos de propriedade personalizada têm suporte como declarações OIDC. A representação de valor no token depende do tipo de propriedade.

| Tipo de propriedade | Valor de exemplo no token OIDC | Observações |
| --- | --- | --- |
| String | `"repo_property_team": "platform-eng"` | O valor aparece como uma cadeia de caracteres sem formatação. |
| Seleção única | `"repo_property_env_tier": "production"` | A opção selecionada aparece como uma cadeia de caracteres sem formatação. |
| Seleção múltipla | `"repo_property_regions": "us-east-1,eu-west-1"` | Vários valores selecionados são unidos em uma única cadeia de caracteres separada por vírgulas. |
| Verdadeiro/Falso | `"repo_property_pci_compliant": "true"` | Os valores boolianos aparecem como a cadeia de caracteres `"true"` ou `"false"`. |

#### Representação de valor de seleção múltipla

Quando um repositório tem uma propriedade personalizada de várias seleções com vários valores selecionados, os valores são unidos em uma única cadeia de caracteres separada por vírgula no token OIDC. Por exemplo, se um repositório tiver uma propriedade `regions` com os valores `us-east-1` e `eu-west-1`, a declaração aparece como:

```json
{
  "repo_property_regions": "us-east-1,eu-west-1"
}
```

Ao configurar políticas de confiança em seu provedor de nuvem, use a correspondência de cadeia de caracteres ou contenha verificações para avaliar declarações de seleção múltipla.

#### Pré-requisitos para incluir propriedades personalizadas

* As propriedades personalizadas já devem ser definidas no nível da organização ou da empresa. Para saber mais, confira [Como gerenciar propriedades personalizadas para repositórios na sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization).
* Você deve ser um administrador da organização ou administrador corporativo.
* Depois de adicionar uma propriedade personalizada à configuração do OIDC, todos os repositórios na organização ou na empresa que têm um valor definido para essa propriedade a incluirão automaticamente em seus tokens OIDC.

#### Adicionando uma propriedade personalizada a declarações de token OIDC

Você pode gerenciar quais propriedades personalizadas estão incluídas em tokens OIDC usando a interface do usuário de configurações ou a API REST.

* **Usando a interface de configurações:**

  Navegue até as configurações de Ações OIDC da sua organização ou empresa para visualizar e configurar quais propriedades personalizadas estão incluídas em tokens de OIDC.

* **Uso da API REST:**

  Para adicionar uma propriedade personalizada às declarações de token OIDC da sua organização, envie uma solicitação `POST` para o endpoint de inclusão de propriedade personalizada OIDC apropriado. Por exemplo:

  * Para uma organização: `POST /orgs/{org}/actions/oidc/customization/properties/repo`
  * Para uma empresa: `POST /enterprises/{enterprise}/actions/oidc/customization/properties/repo` para obter parâmetros de solicitação e detalhes completos, consulte a documentação da API REST para gerenciar propriedades personalizadas do OIDC: [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc).

#### Token de exemplo com propriedades personalizadas

Depois que uma propriedade personalizada for adicionada à configuração do OIDC, os repositórios com um valor definido para essa propriedade a incluirão em seus tokens. No exemplo a seguir, duas propriedades personalizadas (`business_unit` e `workspace_id`) são incluídas no token:

```json
{
  "sub": "repo:my-org/my-repo:ref:refs/heads/main",
  "aud": "https://github.com/my-org",
  "repository": "my-org/my-repo",
  "repo_property_business_unit": "payments",
  "repo_property_workspace_id": "ws-abc123"
}
```

Você pode usar essas `repo_property_*` declarações como condições na política de confiança do provedor de nuvem. Para obter um exemplo, consulte [Exemplo: filtragem em uma propriedade personalizada do repositório](#example-filtering-on-a-repository-custom-property).

### Personalizando as afirmações de assunto para uma organização ou repositório

Para ajudar a melhorar a segurança, a conformidade e a padronização, você pode personalizar as declarações padrão para atender às condições de acesso necessárias. Se o provedor de nuvem der suporte a condições em declarações de assunto, você poderá criar uma condição que verifique se o valor `sub` corresponde ao caminho do fluxo de trabalho reutilizável, como `"job_workflow_ref:octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main"`. O formato exato variará dependendo da configuração do OIDC do provedor de nuvem. Para configurar a condição GitHubcorrespondente, você pode usar a API REST para exigir que a `sub` declaração sempre inclua uma declaração personalizada específica, como `job_workflow_ref`. Você pode usar a API REST para aplicar um modelo de personalização à declaração de entidade do OIDC; por exemplo, você pode exigir que a declaração `sub` dentro do token do OIDC sempre inclua uma declaração personalizada específica, como `job_workflow_ref`. Para saber mais, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc).

!!! note
    Quando o modelo da organização é aplicado, ele não afeta nenhum fluxo de trabalho que já esteja usando o OIDC, a menos que o repositório tenha aceito os modelos personalizados da organização. Para todos os repositórios, existentes e novos, o proprietário do repositório precisará usar a API REST no nível do repositório para aceitar o recebimento dessa configuração, definindo `use_default` como `false`. Como alternativa, o proprietário do repositório pode usar a API REST para aplicar uma configuração diferente específica ao repositório. Para saber mais, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

Personalizar as declarações resulta em um novo formato para toda a declaração `sub`, que substitui o formato predefinido padrão `sub` no token descrito em "[Declarações de entidade de exemplo](#example-subject-claims)".

!!! note
    A declaração `sub` usa a forma abreviada `repo` (por exemplo, `repo:ORG-NAME/REPO-NAME`) em vez de `repository` para referenciar o repositório. Qualquer um `:` dentro do valor de contexto será substituído por `%3A`.
    Para repositórios que usam declarações de assunto imutáveis (não disponíveis em GitHub Enterprise Server), `owner_id` e `repo_id` sempre são incluídos no segmento `repo` da declaração `sub`, mesmo quando você personaliza declarações com `include_claim_keys`. Não é possível remover essas IDs do formato imutável.

Os modelos de exemplo a seguir demonstram várias maneiras de personalizar a declaração de assunto. Para definir essas configurações no GitHub, os administradores usam a API REST para especificar uma lista de declarações que devem ser incluídas na declaração de assunto (`sub`).

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

Para personalizar suas declarações de assunto, primeiro você deve criar uma condição correspondente na configuração OIDC do provedor de nuvem, antes de personalizar a configuração usando a API REST. Depois que a configuração for concluída, cada vez que um novo trabalho for executado, o token OIDC gerado durante esse trabalho seguirá o novo modelo de personalização. Se a condição correspondente não existir na configuração OIDC do provedor de nuvem antes da execução do trabalho, o token gerado poderá não ser aceito pelo provedor de nuvem, pois as condições de nuvem podem não ser sincronizadas.

#### Exemplo: permitir repositório com base na visibilidade e no proprietário

Este modelo de exemplo permite que a declaração `sub` tenha um novo formato, usando `repository_owner` e `repository_visibility`:

```json
{
   "include_claim_keys": [
       "repository_owner",
       "repository_visibility"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a `sub` condição para exigir que as declarações incluam valores específicos para `repository_owner` e `repository_visibility`. Por exemplo: `"sub": "repository_owner:monalisa:repository_visibility:private"`. A abordagem permite restringir o acesso de função de nuvem a apenas repositórios privados em uma organização ou empresa.

#### Exemplo: permitindo acesso a todos os repositórios com um proprietário específico

Este modelo de exemplo permite que a declaração `sub` tenha um novo formato apenas com o valor de `repository_owner`.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "include_claim_keys": [
       "repository_owner"
   ]
}

```

Na configuração do OIDC do provedor de nuvem, configure a condição `sub` para exigir que as declarações incluam um valor específico para `repository_owner`. Por exemplo: `"sub": "repository_owner:monalisa"`

#### Exemplo: exigir um fluxo de trabalho reutilizável

Este modelo de exemplo permite que a declaração `sub` tenha um novo formato que contenha o valor da `job_workflow_ref` declaração. Isso permite que uma empresa use fluxos de trabalho reutilizáveis para impor implantações consistentes em nas organizações e nos repositórios dela.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
  {
     "include_claim_keys": [
         "job_workflow_ref"
     ]
  }
```

Na configuração do OIDC do provedor de nuvem, configure a condição `sub` para exigir que as declarações incluam um valor específico para `job_workflow_ref`. Por exemplo: `"sub": "job_workflow_ref:octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main"`.

#### Exemplo: exigir um fluxo de trabalho reutilizável e outras declarações

O modelo de exemplo a seguir combina o requisito de um fluxo de trabalho reutilizável específico com declarações adicionais.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

Este exemplo também demonstra como usar `"context"` para definir suas condições. Essa é a parte que segue o repositório no formato `sub` padrão. Por exemplo, quando o trabalho faz referência a um ambiente, o contexto traz: `environment:ENVIRONMENT-NAME`.

```json
{
   "include_claim_keys": [
       "repo",
       "context",
       "job_workflow_ref"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a condição `sub` para exigir que as declarações incluam valores específicos para `repo`, `context` e `job_workflow_ref`.

Este modelo de personalização exige que `sub` adote o seguinte formato: `repo:ORG-NAME/REPO-NAME:environment:ENVIRONMENT-NAME:job_workflow_ref:REUSABLE-WORKFLOW-PATH`.
Por exemplo: `"sub": "repo:octo-org/octo-repo:environment:prod:job_workflow_ref:octo-org/octo-automation/.github/workflows/oidc.yml@refs/heads/main"`

#### Exemplo: conceder acesso a um repositório específico

Este modelo de exemplo permite conceder acesso à nuvem a todos os fluxos de trabalho em um repositório específico, em todos os branches/marcas e ambientes.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "include_claim_keys": [
       "repo"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a `sub` condição para exigir uma `repo` declaração que corresponda ao valor necessário.

#### Exemplo: usando GUIDs gerados pelo sistema

Este modelo de exemplo permite declarações OIDC previsíveis com GUIDs gerados pelo sistema que não mudam entre renomeações de entidades (como renomear um repositório).

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
  {
     "include_claim_keys": [
         "repository_id"
     ]
  }
```

Na configuração do OIDC do provedor de nuvem, configure a `sub` condição para exigir uma `repository_id` declaração que corresponda ao valor necessário.

ou:

```json
{
   "include_claim_keys": [
       "repository_owner_id"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a `sub` condição para exigir uma `repository_owner_id` declaração que corresponda ao valor necessário.

#### Exemplo: valor de contexto com `:`

Este exemplo demonstra como lidar com o valor de contexto com `:`. Por exemplo, quando o trabalho faz referência a um ambiente chamado `production:eastus`.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "include_claim_keys": [
       "environment",
       "repository_owner"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a condição `sub` para exigir que as declarações incluam um valor específico para `environment` e `repository_owner`. Por exemplo: `"sub": "environment:production%3Aeastus:repository_owner:octo-org"`.

#### Exemplo: realizar filtragem em uma propriedade personalizada de um repositório

Este modelo de exemplo permite que a declaração `sub` inclua uma declaração de propriedade personalizada do repositório. As propriedades personalizadas incluídas em tokens OIDC aparecem com o prefixo `repo_property_` no token, mas o valor de `include_claim_keys` usa o nome de declaração completo como ele aparece no token.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "include_claim_keys": [
       "repo_property_workspace_id"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a condição `sub` para exigir que as declarações incluam um valor específico para `repo_property_workspace_id`. Por exemplo: `"sub": "repo_property_workspace_id:ws-abc123"`.

#### Redefinir as personalizações do modelo da organização

Este modelo de exemplo redefine as declarações de assunto para o formato padrão. Esse template efetivamente exclui-se de qualquer política de customização no nível da organização.

Para aplicar essa configuração, envie uma solicitação ao ponto de extremidade da API e inclua a configuração necessária no corpo da solicitação. Para organizações, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-an-organization) e para repositórios, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "include_claim_keys": [
       "repo",
       "context"
   ]
}
```

Na configuração do OIDC do provedor de nuvem, configure a `sub` condição para exigir que as declarações incluam valores específicos para `repo` e `context`.

#### Redefinir as personalizações do modelo do repositório

Todos os repositórios de uma organização têm a capacidade de aceitar ou recusar os modelos personalizados de declaração `sub` (no nível da organização e do repositório).

Para desvincular um repositório e restaurar o formato de declaração `sub` padrão, um administrador de repositório deve usar o endpoint da API REST em [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

Para configurar repositórios para que usem o formato de declaração padrão `sub`, use o endpoint `PUT /repos/{owner}/{repo}/actions/oidc/customization/sub` da API REST com o seguinte corpo da solicitação:

```json
{
   "use_default": true
}
```

#### Exemplo: configurar um repositório para usar um modelo de organização

Depois que uma organização criou um modelo de declaração `sub` personalizado, a API REST pode ser usada para aplicar o modelo programaticamente aos repositórios dentro da organização. Um administrador pode configurar seu repositório para usar o modelo criado pelo administrador de sua organização.

Para configurar o repositório de modo que ele use o modelo da organização, um administrador de repositório deve usar o ponto de extremidade `PUT /repos/{owner}/{repo}/actions/oidc/customization/sub` da API REST com o seguinte corpo da solicitação: Para saber mais, confira [Pontos de extremidade da API REST para OIDC do GitHub Actions](https://docs.github.com/pt/rest/actions/oidc#set-the-customization-template-for-an-oidc-subject-claim-for-a-repository).

```json
{
   "use_default": false
}
```

## Depurar as declarações do OIDC

Você pode usar a ação [`github/actions-oidc-debugger`](https://github.com/github/actions-oidc-debugger) para visualizar as declarações que serão enviadas, antes de integrar com um provedor de nuvem. Essa ação solicita um JWT e imprime as declarações incluídas no JWT que foram recebidas de GitHub Actions.

## Permissões de fluxo de trabalho para a solicitação do token OIDC

### Permissão necessária

* O trabalho ou fluxo de trabalho deve conceder permissão de [`id-token: write`](../workflows-and-actions/workflow-syntax.md#permissions) para que o provedor OIDC do GitHub possa criar um JWT (Token Web JSON):

        ```yaml
  permissions:
    id-token: write
  ```

* Sem `id-token: write`, o token de ID JWT do OIDC não pode ser solicitado. Essa configuração habilita apenas a busca e a configuração do token OIDC; ela não concede acesso de gravação a outros recursos.

### Como configurar as permissões

* Para buscar um token OIDC para um fluxo de trabalho, defina a permissão no nível do fluxo de trabalho:

        ```yaml
  permissions:
    id-token: write # This is required for requesting the JWT
    contents: read # This is required for actions/checkout
  ```

* Para buscar um token OIDC para um só trabalho, defina a permissão dentro desse trabalho:

        ```yaml
  permissions:
    id-token: write # This is required for requesting the JWT
  ```

* Podem ser necessárias permissões adicionais dependendo das necessidades do fluxo de trabalho.

### Fluxos de trabalho reutilizáveis

* Para fluxos de trabalho reutilizáveis pertencentes ao mesmo usuário, organização ou empresa que o chamador, o token OIDC gerado no fluxo de trabalho reutilizável está acessível pelo contexto do chamador.
* Para fluxos de trabalho reutilizáveis fora de sua empresa ou organização, defina explicitamente a configuração `permissions` para `id-token` como `write` no fluxo de trabalho ou no nível de trabalho do chamador. Isso garante que o token OIDC só esteja disponível para fluxos de trabalho destinados ao chamador.

## Métodos para solicitar o token OIDC

Ações personalizadas podem solicitar o token OIDC usando:

* O método `getIDToken()` do kit de ferramentas do Actions. Para obter mais informações, confira [OIDC Token](https://www.npmjs.com/package/@actions/core/v/1.6.0#oidc-token) na documentação do pacote npm.
* As variáveis de ambiente a seguir no executor.

| Variável                         | Descrição                                                  |
|--------------------------------|----------------------------------------------------------|
| `ACTIONS_ID_TOKEN_REQUEST_URL`   | A URL do provedor OIDC do GitHub.                          |
| `ACTIONS_ID_TOKEN_REQUEST_TOKEN` | Token portador para a solicitação para o provedor do OIDC. |

  Por exemplo:

        ```shell copy
  curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=api://AzureADTokenExchange"
  ```
