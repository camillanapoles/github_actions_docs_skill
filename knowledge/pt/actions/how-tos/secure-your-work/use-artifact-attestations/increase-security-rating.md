---
title: Usando atestados de artefatos e fluxos de trabalho reutilizáveis para alcançar o SLSA v1 Build Level 3
description: A criação de software com fluxos de trabalho reutilizáveis e atestados de artefatos pode simplificar a segurança da sua cadeia de fornecedores e ajudar você a alcançar o SLSA v1.0 Build Level 3.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/increase-security-rating
captured: '2026-10-13'
section: How tos / Secure your work / Use artifact attestations
---

# Usando atestados de artefatos e fluxos de trabalho reutilizáveis para alcançar o SLSA v1 Build Level 3 { #using-artifact-attestations-and-reusable-workflows-to-achieve-slsa-v1-build-level-3 }

_A criação de software com fluxos de trabalho reutilizáveis e atestados de artefatos pode simplificar a segurança da sua cadeia de fornecedores e ajudar você a alcançar o SLSA v1.0 Build Level 3._

## Pré-requisitos { #prerequisites }

Antes de começar este guia, você deve ter familiaridade com:

* Os benefícios de uso e segurança dos atestados de artefato. Confira [Atestados de artefatos](../../../concepts/security/artifact-attestations.md).
* Gerando atestados de artefatos Confira [Usar atestados de artefatos para estabelecer a procedência de compilações](use-artifact-attestations.md).
* Escrever e usar fluxos de trabalho reutilizáveis. Confira [Reutilizar fluxos de trabalho](../../reuse-automations/reuse-workflows.md).

## Etapa 1: Configurando suas compilações { #step-1-configuring-your-builds }

Primeiro, precisamos compilar com atestados de artefatos e um fluxo de trabalho reutilizável.

### Construir com um fluxo de trabalho reutilizável { #building-with-a-reusable-workflow }

Se você ainda não estiver usando fluxos de trabalho reutilizáveis para compilar seu software, precisará executar suas etapas de build e movê-las para um fluxo de trabalho reutilizável.

### Compilar com atestados de artefatos. { #building-with-artifact-attestations }

O fluxo de trabalho reutilizável que você usa para criar seu software também deve gerar atestados de artefato para estabelecer a procedência do build.

Quando você usa um fluxo de trabalho reutilizável para gerar atestados de artefatos, o fluxo de trabalho de chamada e o fluxo de trabalho reutilizável precisam ter as permissões a seguir.

```yaml copy
permissions:
  attestations: write
  contents: read
  id-token: write
```

Se você estiver compilando imagens de contêiner, também precisará incluir a permissão `packages: write`.

## Etapa 2: Verificar atestados de artefato compilados com um fluxo de trabalho reutilizável { #step-2-verifying-artifact-attestations-built-with-a-reusable-workflow }

Para verificar as certificações de artefatos geradas com suas compilações, você pode usar [`gh attestation verify`](https://cli.github.com/manual/gh_attestation_verify) a partir da CLI do GitHub.

O comando `gh attestation verify` exige o uso de um sinalizador `--owner` ou `--repo`. Esses sinalizadores fazem duas coisas.

* Eles informam a `gh attestation verify` o local em que o atestado deve ser buscado. Isso será sempre o seu fluxo de trabalho de chamador.
* Eles informam a `gh attestation verify` o local de origem do fluxo de trabalho que fez a assinatura. Esse sempre será o fluxo de trabalho que usa a [ação`attest`](https://github.com/actions/attest), que pode ser um fluxo de trabalho reutilizável.

Você pode usar sinalizadores opcionais com o comando `gh attestation verify`.

* Se o fluxo de trabalho reutilizável não estiver no mesmo repositório que o fluxo de trabalho do chamador, use o sinalizador `--signer-repo` para especificar o repositório que contém o fluxo de trabalho reutilizável.
* Se você quiser exigir que um fluxo de trabalho específico assine um atestado de artefato, use o sinalizador `--signer-workflow` para indicar o arquivo de fluxo de trabalho que deve ser usado.

Por exemplo, se o fluxo de trabalho de chamada for `ORGANIZATION_NAME/REPOSITORY_NAME/.github/workflows/calling.yml` e usar `REUSABLE_ORGANIZATION_NAME/REUSABLE_REPOSITORY_NAME/.github/workflows/reusable.yml`, poderá fazer o seguinte:

```bash copy
gh attestation verify -o ORGANIZATION_NAME --signer-repo REUSABLE_ORGANIZATION_NAME/REUSABLE_REPOSITORY_NAME PATH/TO/YOUR/BUILD/ARTIFACT-BINARY
```

Se você quiser especificar o fluxo de trabalho exato:

```bash copy
gh attestation verify -o ORGANIZATION_NAME --signer-workflow REUSABLE_ORGANIZATION_NAME/REUSABLE_REPOSITORY_NAME/.github/workflows/reusable.yml PATH/TO/YOUR/BUILD/ARTIFACT-BINARY
```
