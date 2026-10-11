---
title: Sobre ações personalizadas
description: As ações são tarefas individuais que podem ser combinadas para criar trabalhos e personalizar seu fluxo de trabalho. Você pode criar suas próprias ações ou usar e personalizar ações compartilhadas pela GitHub comunidade.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/custom-actions
captured: '2026-10-11'
section: GitHub Actions
---

# Sobre ações personalizadas

_As ações são tarefas individuais que podem ser combinadas para criar trabalhos e personalizar seu fluxo de trabalho. Você pode criar suas próprias ações ou usar e personalizar ações compartilhadas pela GitHub comunidade._

## Sobre ações personalizadas

Você pode criar ações escrevendo código personalizado que interage com seu repositório da maneira que desejar, incluindo a integração com GitHubAPIs e qualquer API de terceiros publicamente disponível. Por exemplo, uma ação pode publicar módulos npm, enviar alertas de SMS quando problemas urgentes surgirem ou implantar o código pronto para produção.

Você pode escrever suas próprias ações para usar em seu fluxo de trabalho ou compartilhar as ações que cria com a GitHub comunidade. Para compartilhar as ações que você criou com todas as pessoas, seu repositório deve ser público.

As ações podem ser executadas diretamente em uma máquina ou em um contêiner Docker. É possível definir as entradas, saídas e variáveis do ambiente de uma ação.

## Tipos de ações

> \[!NOTE]
> Você pode criar um contêiner do Docker, JavaScript e ações compostas. As ações exigem um arquivo de metadados para definir a configuração de entradas, saídas e execuções para sua ação. Os arquivos de metadados de ação usam a sintaxe YAML e o nome do arquivo de metadados deve ser `action.yml` ou `action.yaml`. O formato preferencial é `action.yml`.

<div class="ghd-tool rowheaders">

| Tipo                | Linux                                                                                                                                                                                                                                                                                                                    | macOS                                                                                                                                                                                                                                                                                                                                                                                                                               | Windows                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| contêiner do Docker | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg> | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-x" aria-label="Not supported" role="img"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path></svg> | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-x" aria-label="Not supported" role="img"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z"></path></svg> |
| JavaScript          | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg> | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>                                                                                                            | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>                                                                                                            |
| Ações compostas     | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg> | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>                                                                                                            | <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-check" aria-label="Supported" role="img"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>                                                                                                            |

</div>

### Ações de contêiner do Docker

Os contêineres do Docker empacotam o ambiente com o GitHub Actions código. Esse procedimento cria uma unidade de trabalho mais consistente e confiável, pois o consumidor da ação não precisa se preocupar com ferramentas ou dependências.

Um contêiner Docker permite usar versões específicas de um sistema operacional, bem como as dependências, as ferramentas e o código. Para ações a serem executadas em uma configuração específica de ambiente, o Docker é a opção ideal porque permite personalizar o sistema operacional e as ferramentas. Por causa da latência para compilar e recuperar o contêiner, as ações de contêiner Docker são mais lentas que as ações JavaScripts.

As ações do contêiner Docker podem apenas ser executadas em executores com o sistema operacional Linux. Executores auto-hospedados devem usar um sistema operacional Linux e ter o Docker instalado para executar as ações do contêiner Docker. Para obter mais informações sobre os requisitos dos executores autohospedados, consulte [Referência de executores auto-hospedados](../../reference/runners/self-hosted-runners.md#requirements-for-self-hosted-runner-machines).

### Ações de JavaScript

As ações do JavaScript podem ser executadas diretamente em uma máquina executora e separar o código de ação do ambiente usado para executar o código. Usar ações JavaScript simplifica o código da ação e é um processo mais rápido se comparado à opção do contêiner Docker.

Para garantir que suas ações de JavaScript sejam compatíveis com todos os executores hospedados no GitHub (Ubuntu, Windows e macOS), o código JavaScript empacotado que você escreve deve ser JavaScript puro e não depender de outros binários. As ações JavaScript são executadas diretamente no executor e usam binários que já existem na imagem do executor.

Se você estiver desenvolvendo um projeto Node.js, o GitHub Actions Kit de Ferramentas fornecerá pacotes que você pode usar em seu projeto para acelerar o desenvolvimento. Para obter mais informações, confira o repositório [actions/toolkit](https://github.com/actions/toolkit).

### Ações compostas

Uma ação *composta* permite combinar várias etapas de fluxo de trabalho em uma ação. Por exemplo, você pode usar esse recurso para juntar vários comandos executando em uma ação e, em seguida, ter um fluxo de trabalho que executa os comandos empacotados como uma única etapa usando essa ação. Para ver um exemplo, confira [Criar uma ação composta](../../tutorials/create-actions/create-a-composite-action.md).

## Próximas etapas

Para saber mais sobre como gerenciar suas ações personalizadas, consulte [Como gerenciar ações personalizadas](../../how-tos/create-and-publish-actions/manage-custom-actions.md).
