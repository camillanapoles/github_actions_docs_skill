---
title: Configurando o OpenID Connect no PyPI
description: Use o OpenID Connect em seus fluxos de trabalho para se autenticar no PyPI.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-pypi
captured: '2026-10-11'
section: How tos / Secure your work / Security harden deployments
---

# Configurando o OpenID Connect no PyPI

_Use o OpenID Connect em seus fluxos de trabalho para se autenticar no PyPI._

## Visão geral

O OIDC (OpenID Connect) permite que seus fluxos de trabalho GitHub Actions se autentiquem com [PyPI](https://pypi.org) para publicar pacotes Python.

Este guia oferece uma visão geral de como configurar o PyPI para confiar no OIDC do GitHub como uma identidade federada e demonstra como usar essa configuração na ação [`pypa/gh-action-pypi-publish`](https://github.com/marketplace/actions/pypi-publish) para publicar pacotes no PyPI (ou em outros repositórios de pacotes Python) sem qualquer necessidade de gerenciamento manual de tokens de API.

## Pré-requisitos

* Para saber os conceitos básicos de como GitHub usa o OpenID Connect (OIDC) e sua arquitetura e benefícios, consulte [OpenID Connect](../../../concepts/security/openid-connect.md).

* Antes de prosseguir, você deve planejar sua estratégia de segurança para garantir que os tokens de acesso sejam atribuídos apenas de forma previsível. Para controlar como o provedor de nuvem emite os tokens de acesso, você **precisa** definir, pelo menos, uma condição, para que os repositórios não confiáveis não possam solicitar tokens de acesso aos seus recursos de nuvem. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

* Os tokens OIDC solicitados para Dependabot trabalhos de atualização têm uma declaração `event_name` de `dynamic`. Se sua política de confiança se destina a autorizar apenas GitHub Actions fluxos de trabalho e seu provedor de nuvem dá suporte a condições `event_name`, permita apenas os nomes de eventos esperados por seus fluxos de trabalho. Para obter mais informações, consulte [Referência do OpenID Connect](../../../reference/security/oidc.md#oidc-claims-used-to-define-trust-conditions-on-cloud-roles).

## Adicionando o provedor de identidade ao PyPI

Para usar o OIDC com o PyPI, adicione uma configuração de confiança que vincule cada projeto no PyPI a cada repositório e combinação de fluxo de trabalho que tenha permissão para publicar para ele.

1. Faça login no PyPI e navegue até as configurações de publicação confiáveis do projeto que você deseja configurar. Para um projeto chamado `myproject`, isso será feito em `https://pypi.org/manage/project/myproject/settings/publishing/`.

2. Configure uma relação de confiança entre o projeto PyPI e um repositório do GitHub (e o fluxo de trabalho dentro desse repositório). Por exemplo, se o seu repositório do GitHub estiver em `myorg/myproject` e o seu fluxo de trabalho de lançamento estiver definido em `release.yml` com um ambiente de `release`, você deverá usar as seguintes configurações para o seu editor confiável no PyPI.

!!! note

   > Insira esses valores com cuidado. Dar ao usuário, repositório ou fluxo de trabalho incorreto a capacidade de publicar no seu projeto PyPI é equivalente a compartilhar um token de API.

   * Proprietário: `myorg`
   * Nome do repositório: `myproject`
   * Nome do fluxo de trabalho: `release.yml`
   * (Opcionalmente) um nome de ambiente do GitHub Actions: `release`

## Atualizar o seu fluxo de trabalho de GitHub Actions

Depois que seu editor confiável estiver registrado no PyPI, você poderá atualizar seu fluxo de trabalho de lançamento para usar a publicação confiável.

!!! note
    Quando os ambientes são usados em fluxos de trabalho ou em políticas OIDC, recomendamos adicionar regras de proteção ao ambiente para segurança adicional. Por exemplo, você pode configurar regras de implantação em um ambiente para restringir quais ramificações e tags podem ser implantadas no ambiente ou acessar segredos de ambiente. Para saber mais, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

A ação [`pypa/gh-action-pypi-publish`](https://github.com/marketplace/actions/pypi-publish) tem suporte integrado para publicação confiável, que pode ser ativada dando à sua tarefa contida a permissão `id-token: write` e omitindo `username` e `password`.

O exemplo a seguir usa a ação `pypa/gh-action-pypi-publish` para trocar um token OIDC por um token da API do PyPI, que é então usado para carregar as distribuições de lançamento de um pacote no PyPI.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.
jobs:
  release-build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: build release distributions
        run: |
          # NOTE: put your own distribution build steps here.
          python -m pip install build
          python -m build

      - name: upload windows dists
        uses: actions/upload-artifact@v4
        with:
          name: release-dists
          path: dist/

  pypi-publish:
    runs-on: ubuntu-latest
    needs:
      - release-build
    permissions:
      id-token: write

    steps:
      - name: Retrieve release distributions
        uses: actions/download-artifact@v5
        with:
          name: release-dists
          path: dist/

      - name: Publish release distributions to PyPI
        uses: pypa/gh-action-pypi-publish@3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f
```
