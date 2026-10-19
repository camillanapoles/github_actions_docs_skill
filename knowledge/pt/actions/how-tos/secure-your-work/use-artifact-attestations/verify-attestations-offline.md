---
title: Verificação de atestados offline
description: Os atestados de artefato podem ser verificados sem uma conexão de Internet.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline
captured: '2026-10-19'
section: How tos / Secure your work / Use artifact attestations
---

# Verificação de atestados offline

_Os atestados de artefato podem ser verificados sem uma conexão de Internet._

## Pré-requisitos

Antes de iniciar este guia, você deve gerar atestados de artefato para seus builds. Confira [Usar atestados de artefatos para estabelecer a procedência de compilações](use-artifact-attestations.md).

## Etapa 1: baixar o pacote de atestados

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

## Etapa 2: Baixar raízes confiáveis

Depois, obtenha o material chave das raízes confiáveis.

Os atestados de artefatos usam a instância pública do Sigstore na rede pública para repositórios públicos e a instância do Sigstore do GitHub para repositórios privados. É possível usar um comando para obter as duas raízes confiáveis:

```bash copy
gh attestation trusted-root > trusted_root.jsonl
```

### Atualização de informações da raiz confiável em um ambiente offline

É uma prática recomendada gerar um novo arquivo de `trusted_root.jsonl` sempre que você importar um novo material assinado para seu ambiente off-line.

O material chave em `trusted_root.jsonl` não tem uma data de expiração embutida, portanto, qualquer coisa assinada antes da geração do arquivo de raiz confiável continuará a ser verificada com sucesso. Qualquer coisa assinada após a geração do arquivo será verificada até que a instância do Sigstore gire o respectivo material de chaves, o que geralmente acontece algumas vezes por ano. Você não saberá se o material de chave foi revogado desde a última vez que gerou o arquivo de raiz confiável.

## Etapa 3: fazer verificação offline

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

### Confirmando o repositório em um ambiente offline

Quando você verifica offline, `gh attestation verify` compara o `-R` valor somente com o repositório e os nomes de proprietário registrados no certificado de assinatura do atestado. Estes são os nomes que o repositório e o proprietário tinham quando o atestado de procedência foi criado. O comando não pode detectar se o repositório ou proprietário foi renomeado ou se um repositório ou proprietário diferente agora usa esse nome.

Para garantir que uma attestation venha do repositório que atualmente tem o nome, baixe seu bundle da API de attestation, conforme descrito na Etapa 1. A API de atestado retorna apenas atestados desse repositório.

O certificado de assinatura também registra a ID do repositório. Um repositório mantém sua ID quando é renomeado e um novo repositório que usa o nome antigo obtém uma ID diferente. Se você verificar um bundle de outra fonte, como um bundle publicado junto com o artefato, compare essa ID com a ID do repositório esperado.

1. Em um computador online, obtenha a ID do repositório do qual você espera que o artefato venha.

            ```bash copy
   gh api repos/ORGANIZATION_NAME/REPOSITORY_NAME --jq .id
   ```

2. Em seu ambiente offline, adicione os sinalizadores `--jq` e `--format json` ao comando de verificação para imprimir a ID do repositório de cada atestado verificado.

   Para `-R`, substitua `ORGANIZATION_NAME/REPOSITORY_NAME` pelos nomes de proprietário e repositório registrados no certificado de assinatura. Se o repositório ou proprietário tiver sido renomeado, eles serão diferentes dos nomes atuais usados para a pesquisa de API.

            ```bash copy
   gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY \
     -R ORGANIZATION_NAME/REPOSITORY_NAME \
     --bundle PATH/TO/YOUR/BUNDLE.jsonl \
     --custom-trusted-root trusted_root.jsonl \
     --format json \
     --jq '.[].verificationResult.signature.certificate.sourceRepositoryIdentifier'
   ```

3. Verifique se cada ID na saída corresponde à ID da primeira etapa. Não confie em um atestado de procedência cuja ID não corresponde, porque outro repositório que usou o mesmo nome o criou.
