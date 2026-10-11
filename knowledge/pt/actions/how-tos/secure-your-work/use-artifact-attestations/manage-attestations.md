---
title: Como gerenciar o ciclo de vida dos atestados de artefato
description: Pesquise e exclua atestados de que você não precisa mais.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/manage-attestations
captured: '2026-10-11'
section: GitHub Actions
---

# Como gerenciar o ciclo de vida dos atestados de artefato

_Pesquise e exclua atestados de que você não precisa mais._

Os atestados só são relevantes quando estão vinculados a artefatos que as pessoas consomem. Para manter seus atestados relevantes e gerenciáveis, exclua atestados que não são mais necessários, como:

* Atestados criados por engano
* Atestados vinculados a artefatos que não existem mais
* Atestados vinculados a artefatos em que os consumidores não devem mais confiar

Quando os consumidores têm um processo de verificação em vigor, a exclusão de um atestado pode impedir o uso do artefato associado. Considere configurar automações para garantir que os atestados sejam excluídos quando o artefato associado for removido de um serviço externo (por exemplo, uma imagem é excluída de um registro de contêiner).

## Como localizar atestados

1. Navegue até o repositório em que o atestado foi produzido.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, em "Gerenciamento", clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-verified" aria-label="verified" role="img"><path d="m9.585.52.929.68c.153.112.331.186.518.215l1.138.175a2.678 2.678 0 0 1 2.24 2.24l.174 1.139c.029.187.103.365.215.518l.68.928a2.677 2.677 0 0 1 0 3.17l-.68.928a1.174 1.174 0 0 0-.215.518l-.175 1.138a2.678 2.678 0 0 1-2.241 2.241l-1.138.175a1.17 1.17 0 0 0-.518.215l-.928.68a2.677 2.677 0 0 1-3.17 0l-.928-.68a1.174 1.174 0 0 0-.518-.215L3.83 14.41a2.678 2.678 0 0 1-2.24-2.24l-.175-1.138a1.17 1.17 0 0 0-.215-.518l-.68-.928a2.677 2.677 0 0 1 0-3.17l.68-.928c.112-.153.186-.331.215-.518l.175-1.14a2.678 2.678 0 0 1 2.24-2.24l1.139-.175c.187-.029.365-.103.518-.215l.928-.68a2.677 2.677 0 0 1 3.17 0ZM7.303 1.728l-.927.68a2.67 2.67 0 0 1-1.18.489l-1.137.174a1.179 1.179 0 0 0-.987.987l-.174 1.136a2.677 2.677 0 0 1-.489 1.18l-.68.928a1.18 1.18 0 0 0 0 1.394l.68.927c.256.348.424.753.489 1.18l.174 1.137c.078.509.478.909.987.987l1.136.174a2.67 2.67 0 0 1 1.18.489l.928.68c.414.305.979.305 1.394 0l.927-.68a2.67 2.67 0 0 1 1.18-.489l1.137-.174a1.18 1.18 0 0 0 .987-.987l.174-1.136a2.67 2.67 0 0 1 .489-1.18l.68-.928a1.176 1.176 0 0 0 0-1.394l-.68-.927a2.686 2.686 0 0 1-.489-1.18l-.174-1.137a1.179 1.179 0 0 0-.987-.987l-1.136-.174a2.677 2.677 0 0 1-1.18-.489l-.928-.68a1.176 1.176 0 0 0-1.394 0ZM11.28 6.78l-3.75 3.75a.75.75 0 0 1-1.06 0L4.72 8.78a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L7 8.94l3.22-3.22a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042Z"></path></svg> Atestações**.
4. As atestações são ordenadas pela data de criação, da mais recente para a mais antiga. Use a barra "Search or filter" para pesquisar um atestado ou filtrar os resultados.

### Pesquisando e filtrando

Insira **texto livre** para pesquisar pelo nome da entidade. Retorna todas as atestações com nomes de assunto que correspondem parcialmente ao termo de pesquisa. Vários atestados podem ter o mesmo nome de assunto.

Use o filtro `created` para filtrar por data de criação. Para inserir um intervalo de datas personalizado, clique na data de hoje e edite a consulta padrão.

* Por exemplo: `created:<2025-04-03`.
* Operadores com suporte: `> <`.

Use o filtro `predicate` para filtrar pelo tipo de atestado. Um predicado é o tipo de declaração que um atestado faz sobre um artefato, como "este artefato foi criado durante uma execução de fluxo de trabalho específica e se origina desse repositório".

* Atestados de procedência foram criados com a ação `attest`.
* As declarações SBOM foram criadas com a ação `attest` usando a entrada `sbom-path`.
* **Não** há suporte para padrões de tipo de predicado personalizado no campo de pesquisa, mas são compatíveis com a API.

## Como excluir atestados

Antes de excluir um atestado, recomendamos baixar uma cópia dele. Depois que o atestado for excluído, os consumidores com um processo de verificação em vigor **não poderão mais usar o artefato**associado, e você não poderá mais localizar o atestado em GitHub.

1. Na lista de atestados, marque a caixa de seleção ao lado dos atestados que você quer excluir. Você pode selecionar vários atestados de cada vez.
2. Clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-trash" aria-label="trash" role="img"><path d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"></path></svg> Delete**.
3. Leia a mensagem e confirme clicando em **Delete attestations**.

## Como gerenciar atestados com a API

Para gerenciar atestados em massa com a API REST, confira [Pontos de extremidade de API REST para atestados de artefatos](https://docs.github.com/pt/rest/users/attestations).
