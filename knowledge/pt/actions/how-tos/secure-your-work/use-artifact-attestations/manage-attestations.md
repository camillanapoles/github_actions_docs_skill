---
title: Como gerenciar o ciclo de vida dos atestados de artefato
description: Pesquise e exclua atestados de que você não precisa mais.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/manage-attestations
captured: '2026-10-13'
section: How tos / Secure your work / Use artifact attestations
---

# Como gerenciar o ciclo de vida dos atestados de artefato { #managing-the-lifecycle-of-artifact-attestations }

_Pesquise e exclua atestados de que você não precisa mais._

Os atestados só são relevantes quando estão vinculados a artefatos que as pessoas consomem. Para manter seus atestados relevantes e gerenciáveis, exclua atestados que não são mais necessários, como:

* Atestados criados por engano
* Atestados vinculados a artefatos que não existem mais
* Atestados vinculados a artefatos em que os consumidores não devem mais confiar

Quando os consumidores têm um processo de verificação em vigor, a exclusão de um atestado pode impedir o uso do artefato associado. Considere configurar automações para garantir que os atestados sejam excluídos quando o artefato associado for removido de um serviço externo (por exemplo, uma imagem é excluída de um registro de contêiner).

## Como localizar atestados { #finding-attestations }

1. Navegue até o repositório em que o atestado foi produzido.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, em "Gerenciamento", clique em **(verified) Atestações**.
4. As atestações são ordenadas pela data de criação, da mais recente para a mais antiga. Use a barra "Search or filter" para pesquisar um atestado ou filtrar os resultados.

### Pesquisando e filtrando { #searching-and-filtering }

Insira **texto livre** para pesquisar pelo nome da entidade. Retorna todas as atestações com nomes de assunto que correspondem parcialmente ao termo de pesquisa. Vários atestados podem ter o mesmo nome de assunto.

Use o filtro `created` para filtrar por data de criação. Para inserir um intervalo de datas personalizado, clique na data de hoje e edite a consulta padrão.

* Por exemplo: `created:<2025-04-03`.
* Operadores com suporte: `> <`.

Use o filtro `predicate` para filtrar pelo tipo de atestado. Um predicado é o tipo de declaração que um atestado faz sobre um artefato, como "este artefato foi criado durante uma execução de fluxo de trabalho específica e se origina desse repositório".

* Atestados de procedência foram criados com a ação `attest`.
* As declarações SBOM foram criadas com a ação `attest` usando a entrada `sbom-path`.
* **Não** há suporte para padrões de tipo de predicado personalizado no campo de pesquisa, mas são compatíveis com a API.

## Como excluir atestados { #deleting-attestations }

Antes de excluir um atestado, recomendamos baixar uma cópia dele. Depois que o atestado for excluído, os consumidores com um processo de verificação em vigor **não poderão mais usar o artefato**associado, e você não poderá mais localizar o atestado em GitHub.

1. Na lista de atestados, marque a caixa de seleção ao lado dos atestados que você quer excluir. Você pode selecionar vários atestados de cada vez.
2. Clique em **(trash) Delete**.
3. Leia a mensagem e confirme clicando em **Delete attestations**.

## Como gerenciar atestados com a API { #managing-attestations-with-the-api }

Para gerenciar atestados em massa com a API REST, confira [Pontos de extremidade de API REST para atestados de artefatos](https://docs.github.com/pt/rest/users/attestations).
