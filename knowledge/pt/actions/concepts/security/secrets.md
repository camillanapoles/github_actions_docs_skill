---
title: Segredos
description: Saiba mais sobre segredos e como são usados em fluxos de trabalho GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/secrets
captured: '2026-10-13'
section: Concepts / Security
---

# Segredos

_Saiba mais sobre segredos e como são usados em fluxos de trabalho GitHub Actions._

## Sobre segredos

Os segredos permitem que você armazene informações confidenciais na organização, repositório ou em ambientes de repositório. Segredos são variáveis que você cria para usar em GitHub Actions fluxos de trabalho em uma organização, repositório ou ambiente de repositório.

GitHub Actions só poderá ler um segredo se você incluir explicitamente o segredo em um fluxo de trabalho.

## Como os segredos funcionam

Os segredos usam [caixas lacradas do Libsodium](https://libsodium.gitbook.io/doc/public-key_cryptography/sealed_boxes), para que sejam criptografadas antes de atingir GitHub. Isso ocorre quando o segredo é enviado [pela interface do usuário](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository) ou pela [API REST](https://docs.github.com/pt/rest/actions/secrets). Esta criptografia do lado do cliente ajuda a minimizar os riscos relacionados ao registro acidental (por exemplo, registros de exceções e de solicitação, entre outros) dentro da infraestrutura do GitHub. Depois que o segredo é carregado, GitHub é capaz de descriptografá-lo para que ele possa ser injetado no runtime do fluxo de trabalho.

## Segredos no nível da organização

Segredos no nível da organização permitem que você compartilhe segredos entre vários repositórios, o que reduz a necessidade de criar segredos duplicados. A atualização de um segredo de organização em um único local também garante que a alteração tenha efeito em todos os fluxos de trabalho do repositório que usam esse segredo.

Ao criar um segredo para uma organização, você poderá usar uma política para limitar o acesso por repositório. Por exemplo, você pode conceder acesso a todos os repositórios ou limitar o acesso a apenas repositórios privados ou a uma lista específica de repositórios.

Para segredos de ambiente, você pode habilitar os revisores necessários para controlar o acesso aos segredos. Uma tarefa de fluxo de trabalho não pode acessar segredos do ambiente até que a aprovação seja concedida pelos aprovadores exigidos.

Para disponibilizar um segredo para uma ação, você deve configurá-lo como uma entrada ou variável de ambiente no arquivo do fluxo de trabalho. Revise o arquivo README da ação para saber quais entradas e variáveis de ambientes a ação exige. Confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsenv).

## Limitar permissões de credenciais

Ao gerar credenciais, recomendamos que você conceda as permissões mínimas possíveis. Por exemplo, em vez de usar credenciais pessoais, use [chaves de implantação](https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/managing-deploy-keys#deploy-keys) ou uma conta de serviço. Considere conceder permissões de somente leitura se isso for tudo o que é necessário e limite o acesso na medida do possível.

Ao gerar um personal access token (classic), selecione o menor número de escopos necessários. Ao gerar um fine-grained personal access token, selecione as permissões mínimas e o acesso ao repositório necessários.

Em vez de usar um personal access token, considere usar um GitHub App, que usa permissões refinadas e tokens de curta duração, semelhante a um fine-grained personal access token. Ao contrário de um personal access token, um GitHub App não está vinculado a um usuário, portanto, o fluxo de trabalho continuará funcionando mesmo se o usuário que instalou o aplicativo sair da sua organização. Para saber mais, confira [Fazer solicitações de API autenticadas com um aplicativo GitHub em um fluxo de trabalho GitHub Actions](https://docs.github.com/pt/apps/creating-github-apps/authenticating-with-a-github-app/making-authenticated-api-requests-with-a-github-app-in-a-github-actions-workflow).

## Segredos ocultados automaticamente

GitHub Actions redige automaticamente o conteúdo de todos os segredos do GitHub que são impressos em logs de fluxo de trabalho.

GitHub Actions também redigi informações que são reconhecidas como confidenciais, mas não são armazenadas como um segredo. Para obter uma lista de segredos redigidos automaticamente, confira [Referência de segredos](../../reference/security/secrets.md#automatically-redacted-secrets).

Como há várias maneiras de transformar um valor secreto, essa redação não é garantida. Além disso, o executor só pode editar segredos usados no trabalho atual. Como resultado, existem certas etapas proativas de segurança que você deve seguir para ajudar a garantir que os segredos sejam redigidos, e para limitar outros riscos associados aos segredos. Para obter uma lista de referência das práticas recomendadas de segurança com segredos, consulte [Referência de uso seguro](../../reference/security/secure-use.md#use-secrets-for-sensitive-information).

## Leitura adicional

* [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)
* [Pontos de extremidade da API REST para segredos do GitHub Actions](https://docs.github.com/pt/rest/actions/secrets)
