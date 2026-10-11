---
title: Compartilhando ações e fluxos de trabalho com sua empresa
description: É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua empresa sem publicar a ação ou fluxo de trabalho publicamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: enterprise-cloud@latest
source: https://docs.github.com/pt/enterprise-cloud@latest/actions/how-tos/reuse-automations/share-with-your-enterprise
captured: '2026-10-11'
section: How tos / Reuse automations
---

# Compartilhando ações e fluxos de trabalho com sua empresa

_É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua empresa sem publicar a ação ou fluxo de trabalho publicamente._

## Visão geral

Se sua organização pertencer a uma conta corporativa, você poderá compartilhar ações e fluxos de trabalho reutilizáveis em sua empresa, sem publicá-los publicamente, permitindo GitHub Actions que os fluxos de trabalho acessem um repositório interno ou privado que contenha a ação ou o fluxo de trabalho reutilizável.

Quaisquer ações ou fluxos de trabalho reutilizáveis armazenados no repositório privado ou interno podem ser usados em fluxos de trabalho definidos em outros repositórios internos ou privados pertencentes à mesma organização ou por qualquer organização pertencente à empresa. Ações e fluxos de trabalho reutilizáveis armazenados em repositórios internos não podem ser usados em repositórios públicos e ações e fluxos de trabalho reutilizáveis armazenados em repositórios privados não podem ser usados em repositórios públicos ou internos.

!!! warning
    * Para tornar um repositório privado acessível aos fluxos de trabalho do GitHub Actions em outros repositórios, os colaboradores externos nos outros repositórios podem acessar indiretamente o repositório privado, mesmo que não tenham acesso direto a esses repositórios. Os colaboradores externos podem exibir os logs das execuções do fluxo de trabalho quando ações ou fluxos de trabalho do repositório privado são usados.
    * Para permitir que os executores baixem essas ações, o GitHub transmite um token de instalação com escopo para o executor. Esse token tem acesso de leitura no repositório e expira automaticamente após uma hora.

## Compartilhando ações e fluxos de trabalho com sua empresa

1. Armazene a ação ou o fluxo de trabalho reutilizável em um repositório privado ou interno. Para saber mais, confira [Sobre repositórios](https://docs.github.com/pt/enterprise-cloud@latest/repositories/creating-and-managing-repositories/about-repositories).
2. Configure o repositório para permitir o acesso a fluxos de trabalho em outros repositórios privados ou internos. Para saber mais, confira [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-access-to-components-in-a-private-repository) e [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/enterprise-cloud@latest/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#allowing-access-to-components-in-an-internal-repository).

## Leitura adicional

* [Contas empresariais](https://docs.github.com/pt/enterprise-cloud@latest/admin/concepts/enterprise-fundamentals/enterprise-accounts)
* [Reutilizar fluxos de trabalho](reuse-workflows.md)
