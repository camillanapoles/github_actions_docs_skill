---
title: Exibir o histórico de implantações
description: Veja as implantações atuais e anteriores para o seu repositório.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history
captured: '2026-10-11'
section: GitHub Actions
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
   * **Para fixar um ambiente na parte superior da lista de histórico de implantação**, os administradores do repositório podem clicar <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-pin" aria-label="Pin environment" role="img"><path d="m11.294.984 3.722 3.722a1.75 1.75 0 0 1-.504 2.826l-1.327.613a3.089 3.089 0 0 0-1.707 2.084l-.584 2.454c-.317 1.332-1.972 1.8-2.94.832L5.75 11.311 1.78 15.28a.749.749 0 1 1-1.06-1.06l3.969-3.97-2.204-2.204c-.968-.968-.5-2.623.832-2.94l2.454-.584a3.08 3.08 0 0 0 2.084-1.707l.613-1.327a1.75 1.75 0 0 1 2.826-.504ZM6.283 9.723l2.732 2.731a.25.25 0 0 0 .42-.119l.584-2.454a4.586 4.586 0 0 1 2.537-3.098l1.328-.613a.25.25 0 0 0 .072-.404l-3.722-3.722a.25.25 0 0 0-.404.072l-.613 1.328a4.584 4.584 0 0 1-3.098 2.537l-2.454.584a.25.25 0 0 0-.119.42l2.731 2.732Z"></path></svg> à direita do ambiente. Você pode fixar até dez ambientes.
   * **Para exibir a confirmação que disparou uma implantação**, na lista histórico de implantação, clique na mensagem de confirmação da implantação que você deseja exibir.
     > \[!NOTE]As implantações com confirmações vindas de um fork fora do repositório não mostram links para a ramificação e solicitação de pull da origem relacionada a cada implantação. Para obter mais informações sobre forks, confira [Garfos](https://docs.github.com/pt/pull-requests/reference/forks).
   * **Para exibir a URL de uma implantação**, à direita da mensagem de commit na lista de histórico de implantação, clique <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-link-external" aria-label="Navigate to deployment URL" role="img"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg>.
   * **Para navegar até os logs de execução de fluxo de trabalho associados a uma implantação**, à direita da mensagem de confirmação na lista de histórico de implantação, clique <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="View logs" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>e clique em **Exibir logs**.
3. Outra opção, para filtrar a lista de histórico de implantação, é criar um filtro.
   1. Clique no **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-filter" aria-label="filter" role="img"><path d="M.75 3h14.5a.75.75 0 0 1 0 1.5H.75a.75.75 0 0 1 0-1.5ZM3 7.75A.75.75 0 0 1 3.75 7h8.5a.75.75 0 0 1 0 1.5h-8.5A.75.75 0 0 1 3 7.75Zm3 4a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg> botão Filtrar** .
   2. Clique **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro**.
   3. Escolha um qualificador pelo qual você gostaria de filtrar o histórico de implantação.
   4. Dependendo do qualificador escolhido, preencha as informações nas colunas "Operador" e "Valor".
   5. Opcionalmente, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-plus" aria-label="plus" role="img"><path d="M7.75 2a.75.75 0 0 1 .75.75V7h4.25a.75.75 0 0 1 0 1.5H8.5v4.25a.75.75 0 0 1-1.5 0V8.5H2.75a.75.75 0 0 1 0-1.5H7V2.75A.75.75 0 0 1 7.75 2Z"></path></svg> Adicionar um filtro** para adicionar outro filtro.
   6. Clique em **Aplicar**.
