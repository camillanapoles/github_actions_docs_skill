---
title: Autenticando o ARC na API de GitHub
description: Autenticar Actions Runner Controller na API GitHub.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api
captured: '2026-10-13'
section: How tos / Manage runners / Use actions runner controller
---

# Autenticando o ARC na API de GitHub

_Autenticar Actions Runner Controller na API GitHub._

Você pode autenticar Actions Runner Controller (ARC) na GitHub API usando um GitHub App ou usando um personal access token (classic).

!!! note
    Você não pode autenticar usando um GitHub App para executores no nível corporativo. Para obter mais informações, consulte [Gerenciar o acesso a executores auto-hospedados usando grupos](../self-hosted-runners/manage-access.md).

## Autenticando ARC com um GitHub App

1. Crie um GitHub App que pertence a uma organização. Para obter mais informações, consulte [Registrando um aplicativo GitHub](https://docs.github.com/pt/apps/creating-github-apps/registering-a-github-app/registering-a-github-app). Configure GitHub App da seguinte forma.

   1. Em "URL da Home Page", insira `https://github.com/actions/actions-runner-controller`.

   2. Em "Permissões", clique em **Permissões do repositório**. Em seguida, use os menus suspensos para selecionar as permissões de acesso a seguir.
      * **Administração**: leitura e gravação

!!! note

`Administration: Read and write` só é necessário ao configurar Actions Runner Controller para registrar no escopo do repositório. Não é necessário fazer registro no escopo da organização.

```
  * **Metadados**: somente leitura
```

1. Em "Permissões", clique em **Permissões da organização**. Em seguida, use os menus suspensos para selecionar as permissões de acesso a seguir.
   * **Executores auto-hospedados**: leitura e gravação

2. Depois de criar os dados do GitHub App, na página do GitHub App, observe o valor de "ID do aplicativo". Você usará esse valor mais tarde.

3. Em "Chaves privadas", clique em **Gerar uma chave privada** e salve o arquivo `.pem`. Você usará esta chave mais tarde.

4. No menu no canto superior esquerdo da página, clique em **Instalar aplicativo** e, ao lado da sua organização, clique em **Instalar** para instalar o aplicativo na sua organização.

5. Depois de confirmar as permissões de instalação na sua organização, anote a ID de instalação do aplicativo. Você o usará mais tarde. Encontre a ID de instalação do aplicativo na página de instalação do aplicativo, que tem o seguinte formato de URL:

   `https://github.com/organizations/ORGANIZATION/settings/installations/INSTALLATION_ID`

6. Registre a ID do aplicativo, a ID de instalação e o arquivo de chave privada `.pem` baixado das etapas anteriores para o Kubernetes como um segredo.

   Para criar um segredo do Kubernetes com os valores de seus dados do GitHub App, execute o comando a seguir.

!!! note

   > Crie o segredo no mesmo namespace onde o gráfico `gha-runner-scale-set` está instalado. Neste exemplo, o namespace é `arc-runners` para corresponder à documentação de início rápido. Para saber mais, confira [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md#configuring-a-runner-scale-set).

            ```bash copy
   kubectl create secret generic pre-defined-secret \
      --namespace=arc-runners \
      --from-literal=github_app_id=123456 \
      --from-literal=github_app_installation_id=654321 \
      --from-literal=github_app_private_key='-----BEGIN RSA PRIVATE KEY-----********'
   ```

   Usando a propriedade `githubConfigSecret` em sua cópia do arquivo [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml), passe o nome do segredo como uma referência.

            ```yaml
   githubConfigSecret: pre-defined-secret
   ```

Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

## Autenticando ARC com um personal access token (classic)

O ARC pode usar personal access tokens (classic) para registrar executores auto-hospedados.

1. Crie um personal access token (classic) com os escopos necessários. Os escopos necessários são diferentes dependendo se você está registrando executores no nível de repositório, ou nível de organização. Para obter mais informações sobre como criar um personal access token (classic), consulte [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic).

   Veja a seguir a lista de escopos personal access token necessários para executores ARC.

   * Executores do repositório: `repo`
   * Corredores da organização: `admin:org`

2. Para criar um segredo do Kubernetes com o valor do seu personal access token (classic), use o comando a seguir.

!!! note

   > Crie o segredo no mesmo namespace onde o gráfico `gha-runner-scale-set` está instalado. Neste exemplo, o namespace é `arc-runners` para corresponder à documentação de início rápido. Para saber mais, confira [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md#configuring-a-runner-scale-set).

            ```bash copy
   kubectl create secret generic pre-defined-secret \
      --namespace=arc-runners \
      --from-literal=github_token='YOUR-PAT'
   ```

3. Na sua cópia do [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) arquivo , transmita o nome do segredo como uma referência.

            ```yaml
   githubConfigSecret: pre-defined-secret
   ```

   Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

## Autenticando ARC com um fine-grained personal access token

O ARC pode usar fine-grained personal access tokens para registrar executores auto-hospedados.

1. Crie um fine-grained personal access token com os escopos necessários. Os escopos necessários são diferentes dependendo se você está registrando executores no nível do repositório ou da organização. Para obter mais informações sobre como criar um fine-grained personal access token, consulte [Gerenciar seus tokens de acesso pessoal](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token).

   Veja a seguir a lista de escopos personal access token necessários para executores ARC.

   * Executores do repositório:
     * **Administração**: leitura e gravação

   * Executores da organização:
     * **Administração:** Leitura
     * **Executores auto-hospedados**: leitura e gravação

2. Para criar um segredo do Kubernetes com o valor do seu fine-grained personal access token, use o comando a seguir.

!!! note

   > Crie o segredo no mesmo namespace onde o gráfico `gha-runner-scale-set` está instalado. Neste exemplo, o namespace é `arc-runners` para corresponder à documentação de início rápido. Para saber mais, confira [Comece a usar o Actions Runner Controller](../../../tutorials/use-actions-runner-controller/get-started.md#configuring-a-runner-scale-set).

            ```bash copy
   kubectl create secret generic pre-defined-secret \
      --namespace=arc-runners \
      --from-literal=github_token='YOUR-PAT'
   ```

3. Na sua cópia do [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) arquivo , transmita o nome do segredo como uma referência.

            ```yaml
   githubConfigSecret: pre-defined-secret
   ```

   Para obter opções adicionais de configuração do Helm, confira [`values.yaml`](https://github.com/actions/actions-runner-controller/blob/master/charts/gha-runner-scale-set/values.yaml) no repositório ARC.

## Autenticar ARC com segredos do cofre

!!! note
    No momento, a integração com o Vault está disponível em versão prévia pública com suporte para o Azure Key Vault.

A partir da versão 0.12.0 do gha-runner-scale-set, o ARC dá suporte à recuperação de credenciais do GitHub de um cofre externo. A integração do cofre é configurada por conjunto de dimensionamento de executores. Isso significa que você pode executar alguns conjuntos de escalonamento usando segredos do Kubernetes, enquanto outros utilizam segredos armazenados em cofres, dependendo de seus requisitos de segurança e operacionais.

### Habilitar a integração do Vault

Para habilitar a integração do cofre de chaves em um conjunto de escalonamento de executores:

1. **Defina o campo `githubConfigSecret`** no arquivo `values.yaml` como o nome da chave secreta armazenada em seu cofre. Esse valor precisa ser uma cadeia de caracteres.
2. **Remova os comentários e configure a `keyVault` seção** no arquivo `values.yaml` com o provedor apropriado e os detalhes de acesso.
3. \*\*Forneça o certificado \*\* necessário (`.pfx`) ao controlador e ao ouvinte. Para fazer isso: \*Recriar a imagem do controlador com o certificado incluído ou \*Monte o certificado como um volume no controlador e no ouvinte usando os campos `listenerTemplate` e `controllerManager`.

### Formato Secreto

O segredo armazenado em Azure Key Vault deve estar no formato JSON. A estrutura depende do tipo de autenticação que você está usando:

#### Exemplo: token de GitHub

```json
{
  "github_token": "TOKEN"
}
```

#### Exemplo: aplicativo GitHub

```json
{
  "github_app_id": "APP_ID_OR_CLIENT_ID",
  "github_app_installation_id": "INSTALLATION_ID",
  "github_app_private_key": "PRIVATE_KEY"
}
```

### Configurar `values.yaml` para a integração do Cofre

O certificado é armazenado como um arquivo .pfx e montado no contêiner em /akv/cert.pfx. Veja abaixo um exemplo de como configurar a seção keyVault para usar este certificado para autenticação:

```yaml
keyVault:
  type: "azure_key_vault"
  proxy:
    https:
      url: "PROXY_URL"
      credentialSecretRef: "PROXY_CREDENTIALS_SECRET_NAME"
    http: {}
    noProxy: []
  azureKeyVault:
    clientId: <AZURE_CLIENT_ID>
    tenantId: <AZURE_TENANT_ID>
    url: <AZURE_VAULT_URL>
    certificatePath: "/akv/cert.pfx"
```

### Fornecendo o certificado para o controlador e o ouvinte

O ARC requer um certificado `.pfx` para autenticar no cofre. Esse certificado deve ser disponibilizado para os componentes do controlador e do ouvinte durante a instalação do controlador.
Você pode fazer isso montando o certificado como um volume usando os campos `controllerManager` e `listenerTemplate` no arquivo `values.yaml`:

```yaml
volumes:
  - name: cert-volume
    secret:
      secretName: my-cert-secret
volumeMounts:
  - mountPath: /akv
    name: cert-volume
    readOnly: true

listenerTemplate:
  volumeMounts:
    - name: cert-volume
      mountPath: /akv/certs
      readOnly: true
  volumes:
    - name: cert-volume
      secret:
        secretName: my-cert-secret
```

O código abaixo é um exemplo de um arquivo de conjunto de dimensionamento `values.yml`.

```yaml
listenerTemplate:
  spec:
    containers:
      - name: listener
        volumeMounts:
          - name: cert-volume
            mountPath: /akv
            readOnly: true
    volumes:
      - name: cert-volume
        secret:
          secretName: my-cert-secret
```

## Aviso legal

Partes foram adaptadas do <https://github.com/actions/actions-runner-controller/> de acordo com a licença Apache-2.0:

```text
Copyright 2019 Moto Ishizawa

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
