---
title: Exibir o histórico de implantações
description: Veja as implantações atuais e anteriores para o seu repositório.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history
captured: '2026-10-26'
section: How tos / Deploy / Configure and manage deployments
---

# Exibir o histórico de implantações

_Veja as implantações atuais e anteriores para o seu repositório._

## Visualizar o histórico de implantações do seu repositório

Na página de implantações do seu repositório, você pode visualizar os seguintes aspectos das suas implantações.

* Implantações ativas no momento em vários ambientes
* Implantações filtradas por ambiente
* O histórico completo de implantação do seu repositório
* Commits associados que dispararam a implantação
* Registros conectados de fluxo de trabalho GitHub Actions
* A URL de implantação (se existir)
* A solicitação de pull de origem e o branch relacionados a cada implantação
* Status da implantação. Para obter mais informações sobre os status da implantação, confira [Pontos de extremidade da API REST para implantações](https://docs.github.com/pt/rest/deployments/deployments#about-deployments).

Por padrão, a página de implantações mostra as implantações atualmente ativas dos ambientes selecionados e uma linha do tempo das últimas implantações para todos os ambientes.

1. Na barra lateral direita da página inicial do repositório, clique em **Implantações**.
2. Quando estiver na página "Implantações", você poderá exibir as seguintes informações sobre seu histórico de implantação.
   * **Para exibir implantações recentes para um ambiente específico**, na seção "Environments" da barra lateral esquerda, clique em um ambiente.
   * **Para fixar um ambiente na parte superior da lista de histórico de implantação**, os administradores do repositório podem clicar (Pin environment) à direita do ambiente. Você pode fixar até dez ambientes.
   * **Para exibir a confirmação que disparou uma implantação**, na lista histórico de implantação, clique na mensagem de confirmação da implantação que você deseja exibir.
     > [!NOTE]As implantações com confirmações vindas de um fork fora do repositório não mostram links para a ramificação e solicitação de pull da origem relacionada a cada implantação. Para obter mais informações sobre forks, confira [Garfos](https://docs.github.com/pt/pull-requests/reference/forks).
   * **Para exibir a URL de uma implantação**, à direita da mensagem de commit na lista de histórico de implantação, clique (Navigate to deployment URL).
   * **Para navegar até os logs de execução de fluxo de trabalho associados a uma implantação**, à direita da mensagem de confirmação na lista de histórico de implantação, clique (View logs)e clique em **Exibir logs**.
3. Outra opção, para filtrar a lista de histórico de implantação, é criar um filtro.
   1. Clique no **(filter) botão Filtrar** .
   2. Clique **(plus) Adicionar um filtro**.
   3. Escolha um qualificador pelo qual você gostaria de filtrar o histórico de implantação.
   4. Dependendo do qualificador escolhido, preencha as informações nas colunas "Operador" e "Valor".
   5. Opcionalmente, clique em **(plus) Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
