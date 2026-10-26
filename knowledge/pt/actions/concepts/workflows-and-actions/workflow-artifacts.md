---
title: Artefatos do fluxo de trabalho
description: Saiba mais sobre como armazenar e compartilhar dados como artefatos de fluxos de GitHub Actions trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/workflow-artifacts
captured: '2026-10-26'
section: Concepts / Workflows and actions
---

# Artefatos do fluxo de trabalho

_Saiba mais sobre como armazenar e compartilhar dados como artefatos de fluxos de GitHub Actions trabalho._

## Sobre artefatos de fluxos de trabalho

Um artefato é um arquivo ou uma coleção de arquivos produzidos durante a execução de um fluxo de trabalho. Os artefatos permitem que você preserve os dados após a conclusão de um trabalho e compartilhe-os com outro trabalho no mesmo fluxo de trabalho. Por exemplo, você pode usar artefatos para salvar o build e os resultados dos testes após o término da execução do fluxo de trabalho.

GitHub fornece duas ações que você pode usar para carregar e baixar artefatos de build, [carregar artefato](https://github.com/actions/upload-artifact) e [baixar artefato](https://github.com/actions/download-artifact).

Os artefatos comuns incluem:

* Arquivos de log e arquivos de despejo de núcleo
* Resultados de testes, falhas e capturas de tela;
* Arquivos binários ou comprimidos
* Resultados de desempenho do teste de estresse e de cobertura do código.

## Artefatos versus armazenamento em cache de dependência

Artefatos e caches são semelhantes porque permitem armazenar arquivos em GitHub, mas cada recurso oferece casos de uso distintos e eles não podem ser usados de maneira intercambiável.

* Use o cache quando quiser reutilizar arquivos que não são alterados com frequência entre execuções de fluxo de trabalho, como dependências baixadas por um sistema de gerenciamento de pacotes, saídas de build intermediárias ou outros arquivos que são caros para regenerar. Armazenar esses arquivos em cache pode acelerar suas execuções de fluxo de trabalho, embora um trabalho sempre seja capaz de baixar novamente ou regenerar esses arquivos se um cache não estiver disponível.
* Use artefatos quando quiser salvar arquivos produzidos por uma tarefa para usar ou visualizar após o término da execução de um fluxo de trabalho, como binários compilados ou logs de compilação, ou quando quiser transferir arquivos entre tarefas em um fluxo de trabalho.

Para obter mais informações sobre o cache de dependência, confira [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).

## Gerar atestados de artefato para compilações

Os atestados de artefatos permitem que você crie garantias de procedência e integridade infalsificáveis para o software que você cria. Por sua vez, as pessoas que consomem seu software podem verificar onde e como seu software foi criado.

Ao gerar atestados de artefato com seu software, você cria declarações assinadas criptograficamente que estabelecem a procedência do build e incluem as seguintes informações:

* Um link para o fluxo de trabalho associado ao artefato
* O repositório, a organização, o ambiente, o SHA de commit e o evento de gatilho do artefato
* Outras informações do token OIDC usado para estabelecer a procedência. Para saber mais, confira [OpenID Connect](../security/openid-connect.md).

Você também pode gerar atestados de artefato que incluam uma SBOM (lista de materiais de software) associada. Associar suas compilações a uma lista de dependências de código aberto usadas nelas fornece transparência e permite que os consumidores cumpram os padrões de proteção de dados.

Você pode acessar atestados após a execução de uma compilação, abaixo da lista de artefatos que a compilação produziu.

Para saber mais, confira [Usar atestados de artefatos para estabelecer a procedência de compilações](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md).

## Artefatos de execuções de fluxo de trabalho excluídas

Quando uma execução de fluxo de trabalho é excluída, todos os artefatos associados a ela também são excluídos do armazenamento. Você pode excluir uma execução de fluxo de trabalho usando a interface do usuário do GitHub Actions, a API REST ou a CLI do GitHub, confira: [Excluir a execução de um fluxo de trabalho](../../how-tos/manage-workflow-runs/delete-a-workflow-run.md), [Excluir uma execução de fluxo de trabalho](https://docs.github.com/pt/rest/actions/workflow-runs#delete-a-workflow-run) ou [gh run delete](https://cli.github.com/manual/gh_run_delete).
