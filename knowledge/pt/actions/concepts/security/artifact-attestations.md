---
title: Atestados de artefatos
description: Entenda os benefícios de uso e segurança dos atestados de artefato.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/artifact-attestations
captured: '2026-10-13'
section: Concepts / Security
---

# Atestados de artefatos { #artifact-attestations }

_Entenda os benefícios de uso e segurança dos atestados de artefato._

## Visão geral { #overview }

Os atestados de artefatos permitem que você crie garantias de procedência e integridade infalsificáveis para o software que você cria. Por sua vez, as pessoas que consomem seu software podem verificar onde e como seu software foi criado.

Ao gerar atestados de artefato com seu software, você cria declarações assinadas criptograficamente que estabelecem a procedência do build e incluem as seguintes informações:

* Um link para o fluxo de trabalho associado ao artefato
* O repositório, a organização, o ambiente, o SHA de commit e o evento de gatilho do artefato
* Outras informações do token OIDC usado para estabelecer a procedência. Para saber mais, confira [OpenID Connect](openid-connect.md).

Você também pode gerar atestados de artefato que incluam uma SBOM (lista de materiais de software) associada. Associar suas compilações a uma lista de dependências de código aberto usadas nelas fornece transparência e permite que os consumidores cumpram os padrões de proteção de dados.

## Níveis de SLSA para atestados de artefatos { #slsa-levels-for-artifact-attestations }

A estrutura SLSA é um padrão do setor usado para avaliar a segurança da cadeia de fornecedores. Está organizada em níveis. Cada nível representa um grau crescente de segurança e confiabilidade para uma cadeia de fornecedores de software. Os atestados de artefato em si fornecem SLSA v1.0 Build Level 2.

Isso fornece um link entre seu artefato e suas instruções de build, mas você pode dar um passo adiante exigindo que os builds usem instruções de build conhecidas e verificadas. Uma ótima maneira de fazer isso é fazer com que seu build ocorra em um fluxo de trabalho reutilizável que muitos repositórios em sua organização compartilhem. Os fluxos de trabalho reutilizáveis podem fornecer isolamento entre o processo de build e o fluxo de trabalho de chamada, para atender ao SLSA v1.0 Build Level 3. Para saber mais, confira [Usando atestados de artefatos e fluxos de trabalho reutilizáveis para alcançar o SLSA v1 Build Level 3](../../how-tos/secure-your-work/use-artifact-attestations/increase-security-rating.md).

Para obter mais informações sobre os níveis de SLSA, consulte [Níveis de segurança do SLSA](https://slsa.dev/spec/v1.0/levels).

## Como GitHub gera atestações de artefatos { #how-github-generates-artifact-attestations }

Para gerar atestados de artefato, GitHub usa o Sigstore, que é um projeto código aberto que oferece uma solução abrangente para assinar e verificar artefatos de software por meio de atestados.

**Repositórios públicos** que geram atestados de artefatos usam a [Instância de Bem Público do Sigstore](https://openssf.org/blog/2023/10/03/running-sigstore-as-a-managed-service-a-tour-of-sigstores-public-good-instance/). Uma cópia do pacote Sigstore gerado é armazenada com GitHub e também é gravada em um log de transparência imutável que é publicamente legível na Internet.

**Repositórios privados** que geram atestados de artefato usam a instância Sigstore do GitHub. A instância do Sigstore do GitHub usa a mesma base de código que a instância pública do Sigstore, mas não tem um log de transparência e apenas federa com GitHub Actions.

## Quando gerar atestados { #when-to-generate-attestations }

A geração de atestados por si só não traz nenhum benefício de segurança, é preciso verificar os atestados para aproveitar os benefícios. Aqui estão algumas diretrizes de como pensar sobre o que assinar e com que frequência:

Você deverá assinar:

* Software que você está liberando em que você espera que as pessoas executem `gh attestation verify ...`.
* Binários que as pessoas executarão, pacotes dos quais as pessoas farão download ou manifestos que incluem hashes de conteúdo detalhado.

Você não **deveria** assinar:

* Compilações frequentes que são apenas para testes automatizados.
* Arquivos individuais, como código-fonte, arquivos de documentação ou imagens incorporadas.

## Verificação de atestados de artefatos { #verifying-artifact-attestations }

Se você consumir software que publica atestados de artefato, poderá usar o GitHub CLI para verificar esses atestados. Como os atestados fornecem informações sobre onde e como o software foi desenvolvido, você pode usar essas informações para criar e aplicar políticas de segurança que elevem a segurança de sua cadeia de fornecedores.

> [!WARNING] É importante lembrar que os atestados de artefatos *não* são uma garantia de que um artefato seja seguro. Em vez disso, os atestados de artefatos vinculam você a itens como o código-fonte e as instruções de compilação que os produziram. Cabe a você definir os critérios de sua política, avaliá-la avaliando o conteúdo e tomar uma decisão embasada sobre riscos ao consumir software.

## Próximas etapas { #next-steps }

Para começar a gerar e verificar atestados de artefato para seus builds, consulte [Usar atestados de artefatos para estabelecer a procedência de compilações](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md).
