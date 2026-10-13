---
title: Referência de segredos
description: Encontre informações técnicas sobre segredos em GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/security/secrets
captured: '2026-10-13'
section: Reference / Security
---

# Referência de segredos

_Encontre informações técnicas sobre segredos em GitHub Actions._

## Nomear os seus segredos

!!! tip
    Para ajudar a garantir que GitHub os segredos sejam redigidos nos logs corretamente, evite usar dados estruturados como os valores dos segredos.

As regras a seguir aplicam-se aos nomes dos segredos:

* Só pode conter caracteres alfanuméricos (`[a-z]`, `[A-Z]`, `[0-9]`) ou sublinhados (`_`). Espaços não são permitidos.
* Não precisa começar com o prefixo `GITHUB_`.
* Não precisa começar com um número.
* Não diferenciam maiúsculas de minúsculas quando referenciados. GitHub armazena nomes secretos como maiúsculas, independentemente de como eles são inseridos.
* Deve ser exclusivo para o repositório, a organização ou a empresa em que são criados.

Se houver um segredo com o mesmo nome em vários níveis, o segredo no nível mais baixo terá precedência. Por exemplo, se um segredo a nível de organização tiver o mesmo nome que um segredo a nível de repositório, o segredo a nível de repositório terá prioridade. Da mesma forma, se uma organização, repositório e ambiente tiverem um segredo com o mesmo nome, o segredo no nível do ambiente terá precedência.

## Limites para segredos

Você pode armazenar até 1.000 segredos da organização, 100 segredos de repositório e 100 segredos de ambiente.

Um fluxo de trabalho criado em um repositório pode acessar o seguinte número de segredos:

* Todos os 100 segredos do repositório.
* Se o repositório tiver acesso a mais de 100 segredos da organização, o fluxo de trabalho só poderá usar os primeiros 100 segredos da organização (ordem alfabética por nome de segredo).
* Todos os 100 segredos de ambiente.

Os segredos são limitados a 48 KB. Para armazenar segredos maiores, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md#storing-large-secrets).

## Quando GitHub Actions lê segredos

Os segredos da organização e do repositório são lidos quando uma execução de fluxo de trabalho é enfileirada e os segredos de ambiente são lidos quando um trabalho que faz referência ao ambiente é iniciado.

## Segredos ocultados automaticamente

GitHub oculta automaticamente as seguintes informações confidenciais dos logs do fluxo de trabalho.

> [!NOTE] Caso deseje que outros tipos de informações confidenciais sejam ocultados automaticamente, entre em contato conosco em nossas [discussões da comunidade](https://github.com/orgs/community/discussions?discussions_q=is%3Aopen+label%3AActions).

* Chaves do Azure de 32 e 64 bytes
* Senhas de aplicativos cliente do Azure AD
* Chaves do Cache do Azure
* Chaves do Registro de Contêiner do Azure
* Chaves de hospedagem do Azure Functions
* Chaves do Azure Search
* Cadeias de conexão de banco de dados
* Cabeçalhos de token de portador HTTP
* JWTs
* Tokens de autor do NPM
* Chaves de API do NuGet
* Tokens de instalação do GitHub v1
* Tokens de instalação do GitHub v2 (`ghp`, `gho`, `ghu`, `ghs`, `ghr`)
* PATs do GitHub v2

## Segurança

Para conhecer as práticas recomendadas de segurança para usar segredos, consulte [Referência de uso seguro](secure-use.md#use-secrets-for-sensitive-information).
