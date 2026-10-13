---
title: Usando modelos de fluxo de trabalho
description: GitHub fornece modelos de fluxo de trabalho para uma variedade de linguagens e ferramentas.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/use-workflow-templates
captured: '2026-10-11'
section: How tos / Write workflows
---

# Usando modelos de fluxo de trabalho { #using-workflow-templates }

_GitHub fornece modelos de fluxo de trabalho para uma variedade de linguagens e ferramentas._

## Escolhendo e usando um modelo de fluxo de trabalho { #choosing-and-using-a-workflow-template }

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Se você já tiver um fluxo de trabalho no repositório, clique em **Novo fluxo de trabalho**.

4. A página "Escolher um fluxo de trabalho" mostra uma seleção de modelos de fluxo de trabalho recomendados. Localize o modelo de fluxo de trabalho que você deseja usar e clique em **Configurar**. Para ajudar a encontrar o modelo de fluxo de trabalho desejado, você pode pesquisar palavras-chave ou filtrar por categoria.

5. Se o modelo de fluxo de trabalho contiver comentários que detalham as etapas de instalação adicionais, siga-as.

   Há guias para acompanhar muitos dos modelos de fluxo de trabalho para criar e testar projetos. Para saber mais, confira [Criar e testar seu código](../../tutorials/build-and-test-code.md).

6. Alguns modelos de fluxo de trabalho usam segredos. Por exemplo, `${{ secrets.npm_token }}`. Se o modelo de fluxo de trabalho usar um segredo, armazene o valor descrito no nome do segredo como um segredo no repositório. Para saber mais, confira [Usar segredos em ações do GitHub](choose-what-workflows-do/use-secrets.md).

7. Opcionalmente, faça as alterações adicionais. Por exemplo, você pode querer alterar o valor de `on` quando o fluxo de trabalho for executado.

8. Clique em **Iniciar commit**.

9. Escreva uma mensagem de commit e decida se você deseja de fazer o commit diretamente para o branch padrão ou abrir um pull request.

## Leitura adicional { #further-reading }

* [Integração contínua](../../get-started/continuous-integration.md)
* [Gerenciar fluxos de trabalho](../manage-workflow-runs.md)
* [Monitorar fluxos de trabalho](../monitor-workflows.md)
* [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions)
