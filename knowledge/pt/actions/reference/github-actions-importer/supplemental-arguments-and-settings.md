---
title: Argumentos e configurações complementares
description: GitHub Actions Importer tem vários argumentos e configurações complementares para adaptar o processo de migração às suas necessidades.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/github-actions-importer/supplemental-arguments-and-settings
captured: '2026-10-13'
section: Reference / Github actions importer
---

# Argumentos e configurações complementares { #supplemental-arguments-and-settings }

_GitHub Actions Importer tem vários argumentos e configurações complementares para adaptar o processo de migração às suas necessidades._

Este artigo fornece informações gerais para configurar GitHub Actions Importerargumentos e configurações complementares, como parâmetros opcionais, argumentos de caminho e configurações de rede.

## Parâmetros opcionais { #optional-parameters }

GitHub Actions Importer tem vários parâmetros opcionais que você pode usar para personalizar o processo de migração.

### Como limitar ações permitidas { #limiting-allowed-actions }

As opções a seguir podem ser usadas para limitar quais ações são permitidas em fluxos de trabalho convertidos. Quando usadas em combinação, essas opções expandem a lista de ações permitidas. Se nenhuma dessas opções for fornecida, todas as ações serão permitidas.

* `--allowed-actions` especifica uma lista de ações que serão permitidas em fluxos de trabalho convertidos. Os caracteres curinga têm suporte. Quaisquer outras ações diferentes das fornecidas não serão permitidas.

  Por exemplo:

        ```shell
  --allowed-actions actions/checkout@v6 actions/upload-artifact@* my-org/*
        ```

  Você pode fornecer uma lista vazia a fim de bloquear qualquer ação. Por exemplo, `--allowed-actions=`.

* `--allow-verified-actions` especifica que todas as ações de criadores verificados são permitidas.

* `--allow-github-created-actions` especifica que as ações publicadas das organizações `github`ou `actions` são permitidas.

  Por exemplo, essas ações incluem `github/super-linter` e `actions/checkout`.

  Essa opção é equivalente a `--allowed-actions actions/* github/*`.

### Usando um arquivo de credenciais de autenticação { #using-a-credentials-file-for-authentication }

O `--credentials-file` parâmetro especifica o caminho para um arquivo que contém credenciais para servidores diferentes que GitHub Actions Importer podem se autenticar. Isso é útil quando scripts de build (como `.travis.yml` ou `jenkinsfile`) são armazenados em várias GitHub Enterprise Server instâncias.

Um arquivo de credenciais deve ser um YAML e conter uma lista de combinações de servidor e token de acesso.
GitHub Actions Importer usa as credenciais para a URL que corresponde mais de perto à solicitação de rede que está sendo feita.

Por exemplo:

```yaml
- url: https://github.com
  access_token: ghp_mygeneraltoken
- url: https://github.com/specific_org/
  access_token: ghp_myorgspecifictoken
- url: https://jenkins.org
  access_token: abc123
  username: marty_mcfly
```

Para o arquivo de credenciais acima, GitHub Actions Importer usa o token `ghp_mygeneraltoken` de acesso para autenticar todas as solicitações `https://github.com`de rede, _a menos que_ a solicitação de rede seja para um repositório na `specific_org` organização. Nesse caso, o token `ghp_myorgspecifictoken` é usado para autenticar.

#### Provedores alternativos de código-fonte { #alternative-source-code-providers }

GitHub Actions Importer pode buscar automaticamente o código-fonteGitHub de não repositórios. Um arquivo de credenciais pode especificar o `provider`, a URL do provedor e as credenciais necessárias para recuperar o código-fonte.

Por exemplo:

```yaml
- url: https://gitlab.com
  access_token: super_secret_token
  provider: gitlab
```

Para o exemplo acima, GitHub Actions Importer usa o token `super_secret_token` para recuperar qualquer código-fonte hospedado.`https://gitlab.com`

Os valores com suporte para `provider` são:

* `github` (padrão)
* `gitlab`
* `bitbucket_server`
* `azure_devops`

### Como controlar recursos opcionais { #controlling-optional-features }

Você pode usar a opção `--features` para limitar os recursos usados em fluxos de trabalho que GitHub Actions Importer criam. Isso é útil para excluir a sintaxe mais GitHub Actions recente dos fluxos de trabalho ao migrar para uma instância mais antiga GitHub Enterprise Server . Ao usar a opção `--features` , você deve especificar a versão para GitHub Enterprise Server a qual está migrando.

Por exemplo:

```shell
gh actions-importer dry-run ... --features ghes-3.3
```

Os valores com suporte para `--features` são:

* `all` (valor padrão)
* `ghes-latest`
* `ghes-<number>`, onde `<number>` está a versão de GitHub Enterprise Server, `3.0` ou posterior. Por exemplo, `ghes-3.3`.

Você pode exibir a lista de sinalizadores GitHub Actions Importer de recursos disponíveis executando o `list-features` comando. Por exemplo:

```shell copy
gh actions-importer list-features
```

Você deverá ver um resultado semelhante ao seguinte.

<!-- markdownlint-disable search-replace -->

```shell
Available feature flags:

actions/cache (disabled):
        Control usage of actions/cache inside of workflows. Outputs a comment if not enabled.
        GitHub Enterprise Server >= ghes-3.5 required.

composite-actions (enabled):
        Minimizes resulting workflow complexity through the use of composite actions. See https://docs.github.com/en/actions/creating-actions/creating-a-composite-action for more information.
        GitHub Enterprise Server >= ghes-3.4 required.

reusable-workflows (disabled):
        Avoid duplication by re-using existing workflows. See https://docs.github.com/en/actions/using-workflows/reusing-workflows for more information.
        GitHub Enterprise Server >= ghes-3.4 required.

workflow-concurrency-option-allowed (enabled):
        Allows the use of the `concurrency` option in workflows. See https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#concurrency for more information.
        GitHub Enterprise Server >= ghes-3.2 required.

Enable features by passing --enable-features feature-1 feature-2
Disable features by passing --disable-features feature-1 feature-2
```

<!-- markdownlint-enable search-replace -->

Para alternar sinalizadores de recursos, use um dos seguintes métodos:
* Use as opções `--enable-features` e `--disable-features` ao executar um comando `gh actions-importer`.
* Use uma variável de ambiente para cada sinalizador de recurso.

Use as opções `--enable-features` e `--disable-features` para selecionar recursos específicos para habilitá-los ou desabilitá-los pelo tempo de duração do comando.
Por exemplo, o seguinte comando desabilita o uso de `actions/cache` e `composite-actions`:

```shell
gh actions-importer dry-run ... --disable-features=composite-actions actions/cache
```

Use o comando `configure --features` para configurar de maneira interativa os sinalizadores de recursos e gravá-los automaticamente no seu ambiente:

```shell
$ gh actions-importer configure --features

✔ Which features would you like to configure?: actions/cache, reusable-workflows
✔ actions/cache (disabled): Enable
? reusable-workflows (disabled):
› Enable
  Disable
```

### Como desabilitar o cache de resposta de rede { #disabling-network-response-caching }

Por padrão, GitHub Actions Importer armazena em cache respostas de solicitações de rede para reduzir a carga de rede e reduzir o tempo de execução. Você pode usar a opção `--no-http-cache` para desabilitar o cache de rede. Por exemplo:

```shell
gh actions-importer forecast ... --no-http-cache
```

## Argumentos de caminho { #path-arguments }

Ao executar GitHub Actions Importer, os argumentos de caminho são relativos ao disco do contêiner, portanto, não há suporte para caminhos absolutos relativos ao computador host do contêiner. Quando GitHub Actions Importer é executado, o diretório do `/data` contêiner é montado no diretório onde GitHub Actions Importer é executado.

Por exemplo, o seguinte comando, quando usado no `/Users/mona` diretório, gera o resumo da GitHub Actions Importer auditoria para o `/Users/mona/out` diretório:

```shell
gh actions-importer audit --output-dir /data/out
```

## Como usar um proxy { #using-a-proxy }

Para acessar servidores configurados com um proxy HTTP, você deve definir as seguintes variáveis de ambiente com a URL do proxy:

* `OCTOKIT_PROXY`: para qualquer GitHub servidor.
* `HTTP_PROXY` (ou `HTTPS_PROXY`): para qualquer outro servidor.

Por exemplo:

```shell
export OCTOKIT_PROXY=https://proxy.example.com:8443
export HTTPS_PROXY=$OCTOKIT_PROXY
```

Se o proxy exigir autenticação, nome de usuário e senha, estes deverão ser incluídos na URL do proxy. Por exemplo, `https://username:password@proxy.url:port`.

## Como desabilitar a verificação de certificado TLS { #disabling-ssl-certificate-verification }

Por padrão, GitHub Actions Importer verifica os certificados SSL ao fazer solicitações de rede. Você pode desabilitar a verificação de certificado SSL com a opção `--no-ssl-verify`. Por exemplo:

```shell
gh actions-importer audit --output-dir ./output --no-ssl-verify
```

## Aviso legal { #legal-notice }

Partes foram adaptadas do https://github.com/github/gh-actions-importer/ de acordo com a licença MIT:

```text
MIT License

Copyright (c) 2022 GitHub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
