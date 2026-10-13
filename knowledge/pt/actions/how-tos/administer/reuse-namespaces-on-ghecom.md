---
title: Como disponibilizar namespaces desativados no GHE.com
description: Permita que as pessoas usem namespaces que correspondam às ações que você usou no GitHub.com.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: enterprise-cloud@latest
source: https://docs.github.com/pt/enterprise-cloud@latest/actions/how-tos/administer/reuse-namespaces-on-ghecom
captured: '2026-10-13'
section: How tos / Administer
---

# Como disponibilizar namespaces desativados no GHE.com

_Permita que as pessoas usem namespaces que correspondam às ações que você usou no GitHub.com._

## Visão geral

Se você usa o GitHub Enterprise Cloud com residência de dados, os membros da sua empresa podem criar fluxos de trabalho do GitHub Actions que usam ações diretamente do GitHub.com ou no [GitHub Marketplace](https://github.com/marketplace?type=actions).

GitHub Actions pesquisa sua empresa em GHE.com para cada ação antes de recorrer a GitHub.com. Isso garante que as versões personalizadas de ações da sua empresa sejam usadas em preferência aos equivalentes no GitHub.com.

Para garantir que os fluxos de trabalho usem as ações pretendidas e bloqueiem o potencial de abuso, assim que uma ação no GitHub.com é usada pela primeira vez, o namespace associado à ação é desativado na sua empresa. Isso impede que os usuários criem uma organização e um repositório na sua empresa que correspondam ao namespace da ação no GitHub.com.

## Como disponibilizar um namespace desativado

Após usar uma ação de GitHub.com, se você quiser criar uma ação em sua empresa com o mesmo nome, precisará disponibilizar o namespace dessa organização e repositório.

1. No canto superior direito do GitHub, clique em sua imagem de perfil e, em seguida, clique em **Enterprise**.
1. Na parte superior da página, clique (gear) em **Configurações**.
1. Em **(gear) Settings**, clique em **Retired namespaces**.
1. À direita do namespace que deseja usar na sua empresa, selecione **Cancelar desativação**.
1. Acesse a organização relevante e crie um novo repositório.

### Dicas para garantir que você possa criar um repositório

* Ao reativar um namespace, crie sempre o novo repositório com esse nome o mais rápido possível. Se um fluxo de trabalho chamar a ação associada em GitHub.com antes de criar o repositório local, o namespace será desativado novamente.
* Para ações usadas em fluxos de trabalho frequentemente, você pode considerar que um namespace foi desativado novamente antes de ter tempo para criar o repositório local. Neste caso, você pode desabilitar temporariamente os fluxos de trabalho relevantes até criar o novo repositório.
