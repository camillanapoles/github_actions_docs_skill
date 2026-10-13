---
title: Verificação de atestados offline
description: Os atestados de artefato podem ser verificados sem uma conexão de Internet.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline
captured: '2026-10-11'
section: How tos / Secure your work / Use artifact attestations
---

# Verificação de atestados offline { #verifying-attestations-offline }

_Os atestados de artefato podem ser verificados sem uma conexão de Internet._

## Pré-requisitos { #prerequisites }

Antes de iniciar este guia, você deve gerar atestados de artefato para seus builds. Confira [Usar atestados de artefatos para estabelecer a procedência de compilações](use-artifact-attestations.md).

## Etapa 1: baixar o pacote de atestados { #step-1-download-attestation-bundle }

Primeiro, obtenha o pacote de comprovação da API de atestado.

Você pode fazer isso com o seguinte comando em uma máquina que está online:

```bash copy
gh attestation download PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME
```

Este é um exemplo de saída desse comando:

```bash
Wrote attestations to file sha256:ae57936def59bc4c75edd3a837d89bcefc6d3a5e31d55a6fa7a71624f92c3c3b.jsonl.
Any previous content has been overwritten

The trusted metadata is now available at sha256:ae57936def59bc4c75edd3a837d89bcefc6d3a5e31d55a6fa7a71624f92c3c3b.jsonl
```

## Etapa 2: Baixar raízes confiáveis { #step-2-download-trusted-roots }

Depois, obtenha o material chave das raízes confiáveis.

Os atestados de artefatos usam a instância pública do Sigstore na rede pública para repositórios públicos e a instância do Sigstore do GitHub para repositórios privados. É possível usar um comando para obter as duas raízes confiáveis:

```bash copy
gh attestation trusted-root > trusted_root.jsonl
```

### Atualização de informações da raiz confiável em um ambiente offline { #updating-trusted-root-information-in-an-offline-environment }

É uma prática recomendada gerar um novo arquivo de `trusted_root.jsonl` sempre que você importar um novo material assinado para seu ambiente off-line.

O material chave em `trusted_root.jsonl` não tem uma data de expiração embutida, portanto, qualquer coisa assinada antes da geração do arquivo de raiz confiável continuará a ser verificada com sucesso. Qualquer coisa assinada após a geração do arquivo será verificada até que a instância do Sigstore gire o respectivo material de chaves, o que geralmente acontece algumas vezes por ano. Você não saberá se o material de chave foi revogado desde a última vez que gerou o arquivo de raiz confiável.

## Etapa 3: fazer verificação offline { #step-3-perform-offline-verification }

Agora, você está pronto para verificar o artefato offline.

Você deve importar para seu ambiente offline:

* GitHub CLI
* Seu artefato
* O arquivo do pacote
* O arquivo de raiz confiável

Depois, você pode fazer a verificação offline com o seguinte comando:

```bash copy
gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME --bundle sha256:ae57936def59bc4c75edd3a837d89bcefc6d3a5e31d55a6fa7a71624f92c3c3b.jsonl --custom-trusted-root trusted_root.jsonl
```
