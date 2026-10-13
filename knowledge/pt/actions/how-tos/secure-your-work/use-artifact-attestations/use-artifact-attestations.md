---
title: Usar atestados de artefatos para estabelecer a procedência de compilações
description: Os atestados de artefatos permitem que você aumente a segurança da cadeia de fornecedores de suas compilações, estabelecendo onde e como seu software foi criado.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
captured: '2026-10-13'
section: How tos / Secure your work / Use artifact attestations
---

# Usar atestados de artefatos para estabelecer a procedência de compilações

_Os atestados de artefatos permitem que você aumente a segurança da cadeia de fornecedores de suas compilações, estabelecendo onde e como seu software foi criado._

## Pré-requisitos

Antes de começar a gerar atestados de artefato, você precisa entender o que eles são e quando você deve usá-los. Confira [Atestados de artefatos](../../../concepts/security/artifact-attestations.md).

## Gerar atestados de artefatos para seus builds.

Você pode usar GitHub Actions para gerar atestados de artefato que estabelecem a procedência de build para artefatos como binários e imagens de contêiner.

Para gerar um atestado de artefato, você deve fazer o seguinte:

* Verificar se as permissões apropriadas estão configuradas em seu fluxo de trabalho.
* Inclua uma etapa no seu fluxo de trabalho que utilize a ação [`attest`](https://github.com/actions/attest).

Quando você executar seus fluxos de trabalho atualizados, eles criarão seus artefatos e gerarão um atestado de artefato que estabelece a origem da compilação. Você pode exibir os atestados na guia **Ações** do repositório. Para obter mais informações, consulte o repositório [`attest`](https://github.com/actions/attest).

### Gerar origem de compilação para binários

1. No fluxo de trabalho que cria o binário que você deseja atestar, adicione as permissões a seguir.

            ```yaml
   permissions:
     id-token: write
     contents: read
     attestations: write
   ```

2. Após a etapa em que o binário foi criado, adicione a etapa a seguir.

            ```yaml
   - name: Generate artifact attestation
     uses: actions/attest@v4
     with:
       subject-path: 'PATH/TO/ARTIFACT'
   ```

   O valor do parâmetro `subject-path` deve ser definido como o caminho do binário que você deseja atestar.

### Gerar origem de compilação para imagens de contêiner

1. No fluxo de trabalho que cria a imagem do contêiner que você deseja atestar, adicione as permissões a seguir.

            ```yaml
   permissions:
     id-token: write
     contents: read
     attestations: write
     packages: write
   ```

2. Após a etapa em que a imagem foi criada, adicione a etapa a seguir.

            ```yaml
   - name: Generate artifact attestation
     uses: actions/attest@v4
     with:
       subject-name: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
       subject-digest: 'sha256:fedcba0...'
       push-to-registry: true
   ```

   O valor do parâmetro `subject-name` deve especificar o nome completo da imagem. Por exemplo, `ghcr.io/user/app` ou `acme.azurecr.io/user/app`. Não inclua uma etiqueta como parte do nome da imagem.

   O valor do parâmetro `subject-digest` deve ser definido como o resumo SHA256 do assunto para o atestado, no formato `sha256:HEX_DIGEST`. Se seu fluxo de trabalho usar `docker/build-push-action`, você poderá usar a saída [`digest`](https://github.com/docker/build-push-action?tab=readme-ov-file#outputs) dessa etapa para fornecer o valor. Para obter mais informações sobre como usar saídas, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs).

## Gerar um atestado para uma SBOM (Lista de Materiais de Software)

É possível gerar atestados de SBOM assinados para artefatos de fluxo de trabalho.

Para gerar uma comprovação para um SBOM, você deve:

* Verificar se as permissões apropriadas estão configuradas em seu fluxo de trabalho.
* Crie uma SBOM para seu artefato. Para obter mais informações, consulte [`anchore-sbom-action`](https://github.com/marketplace/actions/anchore-sbom-action) em GitHub Marketplace.
* Inclua uma etapa em seu fluxo de trabalho que utilize a ação [`attest`](https://github.com/actions/attest) com a entrada `sbom-path`.

Quando você executar seus fluxos de trabalho atualizados, eles criarão seus artefatos e gerarão um atestado de SBOM. Você pode exibir os atestados na guia **Ações** do repositório. Para obter mais informações, consulte o repositório [`attest`](https://github.com/actions/attest).

### Gerar um atestado de SBOM para binários

1. No fluxo de trabalho que cria o binário que você deseja atestar, adicione as permissões a seguir.

            ```yaml
   permissions:
     id-token: write
     contents: read
     attestations: write
   ```

2. Após a etapa em que o binário foi criado, adicione a etapa a seguir.

            ```yaml
   - name: Generate SBOM attestation
     uses: actions/attest@v4
     with:
       subject-path: 'PATH/TO/ARTIFACT'
       sbom-path: 'PATH/TO/SBOM'
   ```

   O valor do parâmetro `subject-path` deve ser definido como o caminho do binário descrito pela SBOM. O valor do parâmetro `sbom-path` deve ser definido como o caminho do arquivo de SBOM que você gerou.

### Gerar um atestado de SBOM para imagens de contêiner

1. No fluxo de trabalho que cria a imagem do contêiner que você deseja atestar, adicione as permissões a seguir.

            ```yaml
   permissions:
     id-token: write
     contents: read
     attestations: write
     packages: write
   ```

2. Após a etapa em que a imagem foi criada, adicione a etapa a seguir.

            ```yaml
   - name: Generate SBOM attestation
     uses: actions/attest@v4
     with:
       subject-name: ${{ env.REGISTRY }}/PATH/TO/IMAGE
       subject-digest: 'sha256:fedcba0...'
       sbom-path: 'sbom.json'
       push-to-registry: true
   ```

   O valor do parâmetro `subject-name` deve especificar o nome completo da imagem. Por exemplo, `ghcr.io/user/app` ou `acme.azurecr.io/user/app`. Não inclua uma etiqueta como parte do nome da imagem.

   O valor do parâmetro `subject-digest` deve ser definido como o resumo SHA256 do assunto para o atestado, no formato `sha256:HEX_DIGEST`. Se seu fluxo de trabalho usar `docker/build-push-action`, você poderá usar a saída [`digest`](https://github.com/docker/build-push-action?tab=readme-ov-file#outputs) dessa etapa para fornecer o valor. Para obter mais informações sobre como usar saídas, confira [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idoutputs).

   O valor do parâmetro `sbom-path` deve ser definido como o caminho para o arquivo de SBOM formatado em JSON que você deseja atestar.

## Enviando artefatos para o linked artifacts page

Recomendamos fazer upload de ativos com atestado para o(a) linked artifacts page
da sua organização. Esta página exibe o histórico de build, os registros de implantação e os detalhes do armazenamento dos artefatos. Você pode usar esses dados para priorizar alertas de segurança ou conectar rapidamente artefatos vulneráveis à equipe responsável, código-fonte e processo de build. Para saber mais, confira [Sobre artefatos vinculados](https://docs.github.com/pt/code-security/concepts/supply-chain-security/linked-artifacts).

A ação [attest](https://github.com/actions/attest) automaticamente cria registros de armazenamento no linked artifacts page se ambos os requisitos forem satisfeitos.

* A `push-to-registry` opção está definida como `true`
* O fluxo de trabalho que inclui a ação tem a `artifact-metadata: write` permissão

Para obter um exemplo de fluxo de trabalho, confira [Carregando dados de armazenamento e implantação no linked artifacts page](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/upload-linked-artifacts#generating-an-attestation).

## Verificando atestações de artefatos com o GitHub CLI

Você pode validar atestados de artefato para binários e imagens de contêiner e validar atestados SBOM usando o GitHub CLI. Para obter mais informações, consulte a [`attestation`](https://cli.github.com/manual/gh_attestation) seção do GitHub CLI manual.

> [!NOTE] Esses comandos presumem que você esteja em um ambiente online. Se você estiver em um ambiente offline ou desconectado, confira [Verificação de atestados offline](verify-attestations-offline.md).

### Verificando um atestado de artefato para binários

Para verificar atestados de artefatos para **binários**, use o seguinte comando GitHub CLI.

```bash copy
gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY -R ORGANIZATION_NAME/REPOSITORY_NAME
```

### Verificando um atestado de artefato para imagens de contêiner

Para verificar atestados de artefatos para **imagens de contêiner**, você deve fornecer o FQDN da imagem prefixado com `oci://` em vez do caminho para um binário. Você pode usar o comando a seguir GitHub CLI .

```bash copy
docker login ghcr.io

gh attestation verify oci://ghcr.io/ORGANIZATION_NAME/IMAGE_NAME:test -R ORGANIZATION_NAME/REPOSITORY_NAME
```

### Verificando uma certificação para SBOMs

Para verificar os atestados do SBOM, você precisa fornecer o sinalizador `--predicate-type` para fazer referência a um predicado não padrão. Para obter mais informações, confira [Predicados vetados](https://github.com/in-toto/attestation/tree/main/spec/predicates#vetted-predicates) no repositório `in-toto/attestation`.

Por exemplo, a ação [`attest`](https://github.com/actions/attest) atualmente dá suporte a predicados SPDX ou CycloneDX SBOM. Para verificar um atestado SBOM no formato SPDX, você pode usar o comando a seguir GitHub CLI .

```bash copy
gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY \
  -R ORGANIZATION_NAME/REPOSITORY_NAME \
  --predicate-type https://spdx.dev/Document/v2.3
```

Para exibir mais informações sobre o atestado, faça referência ao sinalizador `--format json`. Isso pode ser especialmente útil ao examinar atestados do SBOM.

```bash copy
gh attestation verify PATH/TO/YOUR/BUILD/ARTIFACT-BINARY \
  -R ORGANIZATION_NAME/REPOSITORY_NAME \
  --predicate-type https://spdx.dev/Document/v2.3 \
  --format json \
  --jq '.[].verificationResult.statement.predicate'
```

## Próximas etapas

Para manter seus atestados relevantes e gerenciáveis, exclua atestados que não são mais necessários. Confira [Como gerenciar o ciclo de vida dos atestados de artefato](manage-attestations.md).

Você também pode gerar atestados de versão para ajudar os consumidores a verificar a integridade e a origem de suas versões. Para saber mais, confira [Versões imutáveis](https://docs.github.com/pt/code-security/concepts/supply-chain-security/immutable-releases).
