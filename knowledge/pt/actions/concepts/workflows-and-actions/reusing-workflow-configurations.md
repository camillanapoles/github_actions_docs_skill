---
title: Reutilizando configurações de fluxo de trabalho
description: Aprenda a evitar a duplicação ao criar um fluxo de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/workflows-and-actions/reusing-workflow-configurations
captured: '2026-10-11'
section: Concepts / Workflows and actions
---

# Reutilizando configurações de fluxo de trabalho { #reusing-workflow-configurations }

_Aprenda a evitar a duplicação ao criar um fluxo de trabalho._

## Fluxos de trabalho reutilizáveis { #reusable-workflows }

Em vez de copiar e colar de um fluxo de trabalho para outro, você pode tornar os fluxos de trabalho reutilizáveis. Você e qualquer pessoa com acesso ao fluxo de trabalho reutilizável pode chamar o fluxo de trabalho reutilizável a partir de outro fluxo de trabalho.

Fluxos de trabalho reutilizáveis também complementam agentic workflows: um fluxo de trabalho com agente pode chamar fluxos de trabalho reutilizáveis aprovados e determinísticos em vez de duplicar a lógica. Para saber mais, confira [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

A reutilização dosfluxos de trabalho evita duplicação. Isso torna os fluxos de trabalho mais fáceis de manter e permite que você crie novos fluxos de trabalho mais rapidamente, aproveitando o trabalho dos outros, assim como você faz com ações. A reutilização do fluxo de trabalho também promove práticas recomendadas, ajudando você a usar os fluxos de trabalho bem projetados, já testados e com a eficiência comprovada. Sua organização pode criar uma biblioteca de fluxos de trabalho reutilizáveis que pode ser mantida centralmente.

O diagrama abaixo mostra uma execução de fluxo de trabalho em andamento que usa um fluxo de trabalho reutilizável.

* Depois que cada um dos três trabalhos de build à esquerda do diagrama for concluído com êxito, um trabalho dependente chamado "Implantar" será executado.
* O trabalho "Implantar" chama um fluxo de trabalho reutilizável que contém três trabalhos: "Treinamento", "Revisão" e "Produção".
* A tarefa de implantação "Produção" só é executada após a tarefa de "Treinamento" ter sido concluída com sucesso.
* Quando um trabalho é direcionado a um ambiente, a execução do fluxo de trabalho exibe uma barra de progresso que mostra o número de etapas no trabalho. No diagrama abaixo, o trabalho "Produção" contém 8 etapas, com a etapa 6 sendo processada no momento.
* O uso um fluxo de trabalho reutilizável para executar trabalhos de implantação permite que você execute esses trabalhos para cada compilação sem duplicar o código nos fluxos de trabalho.

![Diagrama de um fluxo de trabalho chamando um fluxo de trabalho reutilizável.](https://docs.github.com/assets/images/help/actions/reusable-workflows-ci-cd.png)

Um fluxo de trabalho que usa outro fluxo de trabalho é referido como um fluxo de trabalho "de chamada". O fluxo de trabalho reutilizável é um fluxo de trabalho invocado. Um fluxo de trabalho de chamada pode usar vários fluxos de trabalho chamados. Cada fluxo de trabalho chamado é referenciado em uma única linha. O resultado é que o arquivo de fluxo de trabalho de chamadas pode conter apenas algumas linhas de YAML mas pode executar um grande número de tarefas quando for executado. Quando um fluxo de trabalho é reutilizado, todo o fluxo de trabalho chamado é usado, como se fosse parte do fluxo de trabalho de chamada.

Se você reutilizar um fluxo de trabalho de um repositório diferente, todas as ações no fluxo de trabalho chamado executam-se como se fossem parte do fluxo de trabalho que chama. Por exemplo, se o fluxo de trabalho chamado usar `actions/checkout`, a ação fará check-out do conteúdo do repositório que hospeda o fluxo de trabalho do chamador, não o fluxo de trabalho chamado.

Você pode exibir os fluxos de trabalho reutilizados referenciados em seus GitHub Actions fluxos de trabalho como dependências no grafo de dependência do repositório que contém seus fluxos de trabalho. Para obter mais informações, confira “[Sobre o grafo de dependência](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependency-graph)”.

### Fluxos de trabalho reutilizáveis versus ações compostas { #reusable-workflows-versus-composite-actions }

Fluxos de trabalho reutilizáveis e ações compostas ajudam a evitar a duplicação do conteúdo do fluxo de trabalho. Enquanto os fluxos de trabalho reutilizáveis permitem reutilizar um fluxo de trabalho inteiro, com vários cargos e etapas, as ações compostas combinam várias etapas que podem ser executadas em uma etapa de trabalho, assim como qualquer outra ação.

Vamos comparar alguns aspectos de cada solução:

* **Trabalhos do fluxo de trabalho** – As ações compostas contêm uma série de etapas que são executadas como uma única etapa dentro do fluxo de trabalho chamador. Ao contrário dos fluxos de trabalho reutilizáveis, elas não podem conter tarefas.
* **Log** - Quando uma ação composta é executada, o log exibirá apenas a etapa do fluxo de trabalho chamador que acionou a execução da ação composta, e não as etapas individuais dentro da ação composta. Com fluxos de trabalho reutilizáveis, cada tarefa e cada etapa é registrada separadamente.
* **Especificando executores** - Os fluxos de trabalho reutilizáveis contêm uma ou mais tarefas. Como acontece com todas as tarefas do fluxo de trabalho, as tarefas em um fluxo de trabalho reutilizável especificam o tipo de máquina na qual será executada. Portanto, se for preciso executar as etapas em um tipo de máquina que talvez seja diferente da máquina escolhida para a tarefa do fluxo de trabalho chamador, você deverá usar um fluxo de trabalho reutilizável, não uma ação composta.
* **Passando a saída para etapas** - Uma ação composta é executada como uma etapa dentro de uma tarefa do fluxo de trabalho e você pode ter várias etapas antes ou depois da etapa que executa a ação composta. Fluxos de trabalho reutilizáveis são chamados diretamente dentro de um trabalho, e não de dentro de uma etapa de trabalho. Você não pode adicionar etapas a um trabalho depois de chamar um fluxo de trabalho reutilizável, mas os fluxos de trabalho reutilizáveis agora dão suporte a saídas que podem ser referenciadas em trabalhos subsequentes no fluxo de trabalho do chamador.

### Principais diferenças entre fluxos de trabalho reutilizáveis e ações compostas { #key-differences-between-reusable-workflows-and-composite-actions }

| Fluxos de trabalho reutilizáveis | Ações compostas |
| --- | --- |
| Um arquivo YAML, muito semelhante a qualquer arquivo de fluxo de trabalho padrão | Uma ação que contém um pacote de etapas do fluxo de trabalho |
| Cada fluxo de trabalho reutilizável é um único arquivo no diretório `.github/workflows` de um repositório | Cada ação composta é um repositório, ou um diretório, separado contendo um arquivo `action.yml` e, opcionalmente, outros arquivos |
| Chamada feita referenciando um arquivo YAML específico | Chamada feita referenciando um repositório ou diretório no qual a ação está definida |
| Chamada feita diretamente em uma tarefa, não em uma etapa | Execução feita como uma etapa dentro de uma tarefa |
| Pode conter várias tarefas | Não contém tarefas |
| Cada etapa é registrada em tempo real | Logado como uma única etapa, mesmo que contenha várias etapas |
| Pode conectar no máximo dez níveis de fluxos de trabalho | O aninhamento pode ser feito para ter até 10 ações compostas em um único fluxo de trabalho |
| Pode usar segredos | Não pode usar segredos |
| Não é possível publicar no [marketplace](https://github.com/marketplace?type=actions) | Pode ser publicado no [marketplace](https://github.com/marketplace?type=actions) |

## Modelos de fluxo de trabalho { #workflow-templates }

Os modelos de fluxo de trabalho permitem que todos em sua organização que tenham permissão para criar fluxos de trabalho façam isso com mais rapidez e facilidade. Quando as pessoas criam um novo fluxo de trabalho, podem escolher um modelo de fluxo de trabalho, e uma parte ou todo o trabalho de escrita do fluxo de trabalho será realizado para elas. Dentro de um modelo de fluxo de trabalho, você também pode fazer referência a fluxos de trabalho reutilizáveis para facilitar a utilização de código de fluxo de trabalho gerenciado centralmente.

Se você usar uma confirmação SHA ao fazer referência ao fluxo de trabalho reutilizável, você poderá garantir que todos que reutilizarem esse fluxo de trabalho sempre usarão o mesmo código YAML. No entanto, se você fizer referência a um fluxo de trabalho reutilizável por uma tag ou branch, certifique-se de que você poderá confiar nessa versão do fluxo de trabalho. Para saber mais, confira [Referência de uso seguro](../../reference/security/secure-use.md#reusing-third-party-workflows).

GitHub oferece modelos de fluxo de trabalho para uma variedade de linguagens e ferramentas. Quando você configura fluxos de trabalho em seu repositório, GitHub analisa o código em seu repositório e recomenda fluxos de trabalho com base no idioma e na estrutura em seu repositório. Por exemplo, se você usar Node.js, GitHub sugerirá um arquivo de modelo de fluxo de trabalho que instala seus pacotes de Node.js e executa seus testes. É possível pesquisar e filtrar para encontrar modelos de fluxo de trabalho relevantes.

GitHub fornece modelos de fluxo de trabalho prontos para uso para as seguintes categorias de alto nível:

* **Implantação (CD)**. Para saber mais, confira [Implantação contínua](../../get-started/continuous-deployment.md).

* **Segurança**. Para obter mais informações, consulte [Como definir a configuração avançada para verificação de código](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning#configuring-code-scanning-using-third-party-actions).

* **CI (integração contínua)** . Para saber mais, confira [Integração contínua](../../get-started/continuous-integration.md).

* **Automação**. Os modelos de fluxo de trabalho de automação oferecem soluções para automatizar os fluxos de trabalho, como a triagem de solicitações de pull e a aplicação de um rótulo com base nos caminhos modificados na solicitação de pull ou a saudação de usuários que estão colaborando pela primeira vez no repositório.

Use esses fluxos de trabalho como ponto de partida para criar seu fluxo de trabalho personalizado ou usá-los no estado em que se encontram. É possível navegar pela lista completa de modelos de fluxo de trabalho no repositório [actions/starter-workflows](https://github.com/actions/starter-workflows).

Para saber mais, confira [Criar modelos de fluxo de trabalho para sua organização](../../how-tos/reuse-automations/create-workflow-templates.md).

As organizações também podem compartilhar e controlar modelos aprovados agentic workflows juntamente com ações compartilhadas e fluxos de trabalho reutilizáveis. Para criar modelos com GitHub Agentic Workflows, consulte [Criando fluxos de trabalho agênticos do GitHub](https://docs.github.com/pt/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows).

## Âncoras e aliases YAML { #yaml-anchors-and-aliases }

Você pode usar âncoras e aliases YAML para reduzir a repetição nos fluxos de trabalho. Uma âncora (marcada com `&`) identifica uma parte do conteúdo que você deseja reutilizar, enquanto um alias (marcado com `*`) repete esse conteúdo em outro local. Pense em uma âncora como se fosse a criação de um modelo nomeado e em um alias como se fosse o uso desse modelo. Isso é particularmente útil quando você tem trabalhos ou etapas que compartilham configurações comuns.

Para obter informações de referência e exemplos, confira [Reutilizando configurações de fluxo de trabalho](../../reference/workflows-and-actions/reusing-workflow-configurations.md#yaml-anchors-and-aliases).

## Próximas etapas { #next-steps }

Para começar a reutilizar fluxos de trabalho, consulte [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

Para encontrar informações sobre os meandros da reutilização de fluxos de trabalho, consulte [Reutilizando configurações de fluxo de trabalho](../../reference/workflows-and-actions/reusing-workflow-configurations.md).
