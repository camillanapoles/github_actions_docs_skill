---
title: Aplicar lockfiles para dependências de ação
description: Exija os arquivos de bloqueio de dependências do fluxo de trabalho em seus repositórios e mantenha os arquivos atualizados automaticamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/administer/enforce-workflow-lockfiles
captured: '2026-11-02'
section: How tos / Administer
---

# Aplicar lockfiles para dependências de ação

_Exija os arquivos de bloqueio de dependências do fluxo de trabalho em seus repositórios e mantenha os arquivos atualizados automaticamente._

A exigência de arquivos de bloqueio fornece uma garantia consistente e auditável de que cada fluxo de trabalho executa código verificado, sem pedir a cada equipe que adote a prática por conta própria. Para obter uma introdução, confira [Arquivos de bloqueio de dependências do fluxo de trabalho](../../concepts/security/workflow-dependency-lockfiles.md).

Este guia ajuda você a executar um piloto em repositórios selecionados e configurar automações para manter os lockfiles atualizados. Quando estiver confiante de que os arquivos de bloqueio estão funcionando conforme o esperado e não causando dificuldades para os desenvolvedores, você pode impor a política **Require lockfile**.

## Prerequisites

Antes de impor os lockfiles de workflow e criar processos para mantê-los atualizados, o arquivo de bloqueio deve existir em seus repositórios. Para obter instruções, consulte [Bloqueio de dependências de ação nos fluxos de trabalho de um repositório](../secure-your-work/lock-workflow-dependencies.md). Você não precisa ser um administrador para criar um arquivo de bloqueio. Qualquer pessoa com acesso de gravação a um repositório pode fazer isso, para que você possa delegar a integração inicial a equipes individuais antes de impor a política centralmente.

Se seus fluxos de trabalho chamarem fluxos de trabalho reutilizáveis de outros repositórios, confirme se esses repositórios de origem também estão integrados. O lockfile do repositório chamador não os cobre. Se um fluxo de trabalho reutilizável chamado não estiver integrado/configurado em seu próprio repositório, a política **Exigir arquivo de bloqueio** bloqueará a execução do fluxo de trabalho de chamada.

## 1. Teste a política "Exigir lockfile"

!!! important
    **O modo de** avaliação para políticas só está disponível em GitHub Enterprise Cloud. Não habilite essa política no modo **Ativo** até ter certeza de que tem sistemas em vigor para manter o arquivo de bloqueio atualizado para todos os fluxos de trabalho direcionados.

A política **Exigir lockfile** bloqueia execuções de fluxos de trabalho direcionados que não estão integrados ao arquivo de bloqueio do repositório, incluindo fluxos de trabalho sem `uses:` dependências.

Execute um piloto antes de impor essa política em todos os repositórios. Você deve:

* Limite a política a repositórios específicos que aderiram a lockfiles.
* Direcione fluxos de trabalho específicos que foram adicionados ao lockfile, até que todos os fluxos de trabalho sejam adicionados e você tenha processos automatizados para adicionar novos.
* Comece com a política no modo **Avaliar** e analise os resultados em **Insights da política**.

**Exigir lockfile** é uma política separada de **Exigir que as ações sejam fixadas em uma SHA do commit de comprimento completo**. Você pode manter ambos habilitados durante a distribuição. Para configurar a política e ver como os dois interagem, consulte [Controle da execução de GitHub Actions fluxos de trabalho](control-workflow-execution.md#require-lockfile).

## 2. Manter os arquivos de bloqueio atuais

A aplicação só funcionará se os arquivos de bloqueio permanecerem atualizados. Adicione automações para que os desenvolvedores não precisem se lembrar de executar o comando de bloqueio sempre que criarem ou editarem fluxos de trabalho.

As seções a seguir fornecem exemplos de como evitar arquivos de bloqueio obsoletos em diferentes pontos do ciclo de vida de desenvolvimento:

* Mantenha o arquivo atualizado habilitando Dependabot.
* Crie um fluxo de trabalho para executar o comando lock e verificá-lo como parte dos requisitos da pull request.

### Dependabot atualizações de versão

Quando Dependabot atualiza a versão de uma ação, ela regenera a entrada no arquivo de bloqueio correspondente no mesmo pull request.

Você não precisa de nenhuma configuração além de ter Dependabot gerenciar GitHub Actions dependências. Consulte [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

Dependabot
**não** incorporará um fluxo de trabalho que ainda não tem entradas de arquivo de bloqueio, portanto, essa opção mantém a cobertura em vez de estendê-la.

### Um fluxo de trabalho dedicado ou Copilot

Quando alguém adiciona ou edita um fluxo de trabalho, execute outro fluxo de trabalho que executa o comando de bloqueio. Dispare o fluxo de trabalho em alterações em `.github/workflows/**` e em qualquer arquivo `action.yml` ou `action.yaml`, depois dê a ele dois trabalhos:

* Um trabalho de **atualização** que regenera o arquivo de bloqueio no push e faz commit do resultado. Esse trabalho precisa de permissões `contents: write`, e suas regras ou conjuntos de regras de proteção de branch devem permitir GitHub Actions enviar por push para os branches em que o fluxo de trabalho é executado. Gravar no arquivo de bloqueio requer o escopo OAuth `workflow` , portanto, confirme se suas ferramentas têm esse escopo.
* Um trabalho **de verificação** executado `gh actions-lock --verify` em pull requests. Isso deve falhar com erro se o arquivo de bloqueio estiver obsoleto, tornando-o útil para uma verificação necessária.

Para obter um fluxo de trabalho de exemplo pronto para uso, consulte [verify-lockfile.yml](https://github.com/github/gh-actions-lock/blob/main/.github/workflows/verify-lockfile.yml?utm_source=enforcing-lockfiles-docs-linking-verify-lockfile-workflow\&utm_medium=docs\&utm_campaign=universe-2026) no `gh-actions-lock` repositório. Se você usar Copilot para editar fluxos de trabalho, também poderá configurá-lo para regenerar o arquivo de bloqueio no mesmo conjunto de alterações. Consulte a [habilidade gh-actions-lock](https://github.com/github/gh-actions-lock/blob/main/skills/gh-actions-lock/SKILL.md?utm_source=another-docs-about-lockfiles\&utm_medium=docs\&utm_campaign=universe-2026) e [Habilidades do agente](https://docs.github.com/pt/copilot/concepts/agents/about-agent-skills).

## 3. Configurar um processo de revisão para alterações de lockfile

Um arquivo de bloqueio será apenas um controle de segurança se alguém ler o diff. Uma SHA do commit alterada, especificamente, informa que o código que seus fluxos de trabalho executam foi alterado.

1. Adicione `.github/workflows/actions.lock` ao arquivo `CODEOWNERS` para que a equipe responsável pela segurança do build seja solicitada automaticamente para revisão. Consulte [Sobre os proprietários de código](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
2. Configure uma regra de proteção de branch ou um conjunto de regras de repositório para exigir aprovação de um proprietário de código.
3. Diga aos revisores o que procurar. Para obter diretrizes, confira [Bloqueio de dependências de ação nos fluxos de trabalho de um repositório](../secure-your-work/lock-workflow-dependencies.md#reviewing-lockfile-changes).

## 4. Aplicar a política

Quando você estiver confiante de que os arquivos de bloqueio estão em vigor e permanecerão atualizados, altere o status de imposição da política **Exigir arquivo de bloqueio** para **Ativo**. Verifique se todos os repositórios e fluxos de trabalho integrados estejam configurados como destino.

> [!IMPORTANT] Quando **Exigir arquivo de bloqueio** está **ativo**, todos os fluxos de trabalho direcionados que não estão adotados no arquivo de bloqueio do repositório são bloqueados, mesmo que outros fluxos de trabalho no mesmo repositório estejam adotados. Antes de ativar a política, execute `gh actions-lock --verify` em cada repositório de destino ou examine **os insights de política** no modo **Avaliar** , para confirmar se cada fluxo de trabalho direcionado está coberto.

Deixe a verificação da etapa 2 como está. A política bloqueia uma execução de fluxo de trabalho que não tem nenhum arquivo de bloqueio válido. Uma verificação, por outro lado, informa a um autor que seu lockfile está obsoleto enquanto ele ainda está trabalhando no pull request.

Se uma verificação falhar, consulte o [guia de solução de problemas do gh-actions-lock](https://github.com/github/gh-actions-lock/blob/main/docs/troubleshooting.md?utm_source=lockfiles-doc-linking-gh-actions-lock-troubleshooting\&utm_medium=docs\&utm_campaign=universe-2026) no repositório `gh-actions-lock`.
