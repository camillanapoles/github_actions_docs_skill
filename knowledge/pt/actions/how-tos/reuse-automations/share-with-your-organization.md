---
title: Compartilhamento de ações e fluxos de trabalho com sua organização
description: É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua organização sem publicá-lo publicamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/reuse-automations/share-with-your-organization
captured: '2026-10-19'
section: How tos / Reuse automations
---

# Compartilhamento de ações e fluxos de trabalho com sua organização

_É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua organização sem publicá-lo publicamente._

!!! warning
    * Para tornar um repositório privado acessível aos fluxos de trabalho do GitHub Actions em outros repositórios, os colaboradores externos nos outros repositórios podem acessar indiretamente o repositório privado, mesmo que não tenham acesso direto a esses repositórios. Os colaboradores externos podem exibir os logs das execuções do fluxo de trabalho quando ações ou fluxos de trabalho do repositório privado são usados.
    * Para permitir que os executores baixem essas ações, o GitHub transmite um token de instalação com escopo para o executor. Esse token tem acesso de leitura no repositório e expira automaticamente após uma hora.

## Compartilhamento de ações e fluxos de trabalho com sua organização

1. Armazene a ação ou o fluxo de trabalho reutilizável em um repositório privado. Para saber mais, confira [Sobre repositórios](https://docs.github.com/pt/repositories/creating-and-managing-repositories/about-repositories#about-repository-visibility).
2. No GitHub, navegue até a página principal do repositório privado.
3. No nome do repositório, clique em **(gear) Configurações**.
4. Na barra lateral esquerda, clique em **(play) Actions** e clique em **General**.
5. Para conceder acesso a outros repositórios privados na organização, na seção **Access** na parte inferior da página, selecione **Accessible from repositories in the 'ORGANIZATION-NAME' organization**.
6. Clique em **Salvar** para aplicar as configurações.

## Próximas etapas

Para saber como reutilizar os fluxos de trabalho compartilhados, consulte [Reutilizar fluxos de trabalho](reuse-workflows.md).
