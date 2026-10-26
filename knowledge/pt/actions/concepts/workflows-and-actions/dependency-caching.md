---
title: Cache de dependência
description: Saiba mais sobre o cache de dependência para velocidade e eficiência do fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/dependency-caching
captured: '2026-10-26'
section: Concepts / Workflows and actions
---

# Cache de dependência

_Saiba mais sobre o cache de dependência para velocidade e eficiência do fluxo de trabalho._

## Sobre o cacheamento de dependências em fluxos de trabalho

As execuções do fluxo de trabalho geralmente reutilizam as mesmas saídas ou dependências baixadas de uma execução para outra. Por exemplo, as ferramentas de gerenciamento de pacotes e de dependência, como, por exemplo, Maven, Gradle, npm e Yarn mantêm uma cache local de dependências baixadas.

Os trabalhos em GitHubexecutores hospedados começam em uma imagem de executor limpo e devem baixar dependências sempre, causando maior utilização de rede, tempo de execução mais longo e aumento do custo.
Para ajudar a acelerar o tempo necessário para recriar arquivos como dependências, GitHub você pode armazenar em cache arquivos usados com frequência em fluxos de trabalho.

!!! note
    Ao usar executores auto-hospedados, os caches de execuções de fluxo de trabalho são armazenados no armazenamento em GitHubnuvem de propriedade. Uma solução de armazenamento de propriedade do cliente só está disponível com GitHub Enterprise Server.

## Artefatos versus armazenamento em cache de dependência

Artefatos e caches são semelhantes porque permitem armazenar arquivos em GitHub, mas cada recurso oferece casos de uso distintos e eles não podem ser usados de maneira intercambiável.

* Use o cache quando quiser reutilizar arquivos que não são alterados com frequência entre execuções de fluxo de trabalho, como dependências baixadas por um sistema de gerenciamento de pacotes, saídas de build intermediárias ou outros arquivos que são caros para regenerar. Armazenar esses arquivos em cache pode acelerar suas execuções de fluxo de trabalho, embora um trabalho sempre seja capaz de baixar novamente ou regenerar esses arquivos se um cache não estiver disponível.
* Use artefatos quando quiser salvar arquivos produzidos por uma tarefa para usar ou visualizar após o término da execução de um fluxo de trabalho, como binários compilados ou logs de compilação, ou quando quiser transferir arquivos entre tarefas em um fluxo de trabalho.

Para obter mais informações sobre artefatos de execução de fluxo de trabalho, confira [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](../../tutorials/store-and-share-data.md).

## Segurança do cache

Os caches são compartilhados com base na branch ou na tag usada por uma execução de workflow, não na identidade do workflow ou do job. Consulte [Eventos que disparam fluxos de trabalho](../../reference/workflows-and-actions/events-that-trigger-workflows.md) e a ramificação `GITHUB_REF` usada para vários acionadores de fluxo de trabalho. Qualquer execução que possa ler um cache restaura seu conteúdo as-is, portanto, você deve tratar arquivos restaurados como entrada não confiável e nunca armazenar segredos ou outros dados confidenciais em um cache.

Fluxos de trabalho não confiáveis podem ler conteúdo sensível do cache, como quando uma execução `pull_request` de um fork restaura o cache. Caches envenenados podem levar à execução de código em fluxos de trabalho confiáveis. Para limitar o risco de envenenamento de cache, GitHub concede aos fluxos de trabalho executados em resposta a gatilhos pouco confiáveis acesso somente para leitura aos caches no escopo do branch padrão. Um fluxo de trabalho ou job pode substituir essa restrição de somente leitura ao declarar explicitamente um token `cache-mode`com permissão de gravação, o que reintroduz o risco de envenenamento de cache para esse fluxo de trabalho.

Para ver o detalhamento dos gatilhos confiáveis versus os de baixa confiança e o comportamento padrão do cache, consulte [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md#cache-access-for-low-trust-workflow-triggers). Para obter diretrizes de segurança específicas do cache, consulte [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md#best-practices-for-using-caches-securely).

## Próximas etapas

Para implementar o cache de dependência em seus fluxos de trabalho, consulte [Referência do cache de dependência](../../reference/workflows-and-actions/dependency-caching.md).
