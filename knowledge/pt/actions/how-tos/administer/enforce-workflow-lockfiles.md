---
title: Aplicar lockfiles para dependências de ação
description: Exija os arquivos de bloqueio de dependências do fluxo de trabalho em seus repositórios e mantenha os arquivos atualizados automaticamente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/administer/enforce-workflow-lockfiles
captured: '2026-10-26'
section: How tos / Administer
---

# Aplicar lockfiles para dependências de ação

_Exija os arquivos de bloqueio de dependências do fluxo de trabalho em seus repositórios e mantenha os arquivos atualizados automaticamente._

> [!NOTE] Os arquivos de bloqueio de dependência de fluxo de trabalho estão em prévia pública e sujeitos a alterações.

A exigência de arquivos de bloqueio fornece uma garantia consistente e auditável de que cada fluxo de trabalho executa código verificado, sem pedir a cada equipe que adote a prática por conta própria. Para obter uma introdução, confira [Arquivos de bloqueio de dependências do fluxo de trabalho](../../concepts/security/workflow-dependency-lockfiles.md).

Este guia ajuda você a executar um piloto em repositórios selecionados e configurar automações para manter os lockfiles atualizados. Quando estiver confiante de que os arquivos de bloqueio estão funcionando conforme o esperado e não causando dificuldades para os desenvolvedores, você pode impor a política **Require lockfile**.

## Prerequisites

Antes de impor os lockfiles de workflow e criar processos para mantê-los atualizados, o arquivo de bloqueio deve existir em seus repositórios. Para obter instruções, consulte [Bloqueio de dependências de ação nos fluxos de trabalho de um repositório](../secure-your-work/lock-workflow-dependencies.md).

## 1. Teste a política "exigir lockfile"

!!! important
    **O modo de** avaliação para políticas só está disponível em GitHub Enterprise. Não habilite essa política no modo **Ativo** até ter certeza de que tem sistemas em vigor para manter o arquivo de bloqueio atualizado para todos os fluxos de trabalho direcionados.

A política **Exigir lockfile** bloqueia execuções de fluxos de trabalho direcionados que incluem dependências de ação, mas **não** estão incluídos no lockfile do repositório. Para configurar a política, consulte [Controle da execução de GitHub Actions fluxos de trabalho](control-workflow-execution.md).

Execute um piloto antes de impor essa política em todos os repositórios. Você deve:

* Limite a política a repositórios específicos que aderiram a lockfiles.
* Direcionar fluxos de trabalho específicos que foram integrados ao lockfile. Faça isso até que todos os fluxos de trabalho sejam integrados *e* você tenha processos em vigor para garantir que novos fluxos de trabalho sejam integrados automaticamente.
* Comece com a política no modo **Avaliar** e analise os resultados em **Insights de política**

## 2. Manter os arquivos de bloqueio atuais

A aplicação só funcionará se os arquivos de bloqueio permanecerem atualizados. Adicione automações para que os desenvolvedores não precisem se lembrar de executar o comando de bloqueio sempre que criarem ou editarem fluxos de trabalho.

As seções a seguir dão exemplos de como evitar arquivos de bloqueio obsoletos em diferentes pontos do ciclo de vida de desenvolvimento.

* Mantenha o arquivo atualizado habilitando Dependabot e criando um fluxo de trabalho para executar o comando lock.
* Adicione uma skill e um hook de pre-commit para reduzir o ciclo de feedback para desenvolvedores.

Para implementações prontas para copiar do fluxo de trabalho e da habilidade, consulte o repositório [gh-actions-lock](https://github.com/github/gh-actions-lock) .

### Dependabot atualizações de versão

Quando Dependabot atualiza a versão de uma ação, ela regenera a entrada no arquivo de bloqueio correspondente no mesmo pull request.

Você não precisa de nenhuma configuração além de ter Dependabot gerenciar GitHub Actions dependências. Consulte [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions).

Dependabot
**não** incorporará um fluxo de trabalho que ainda não tem entradas de arquivo de bloqueio, portanto, essa opção mantém a cobertura em vez de estendê-la.

### Um fluxo de trabalho dedicado GitHub Actions

Quando alguém adiciona ou edita um fluxo de trabalho, execute outro fluxo de trabalho que executa o comando de bloqueio. Dispare o fluxo de trabalho em alterações em `.github/workflows/**` e em qualquer arquivo `action.yml` ou `action.yaml`, depois dê a ele dois trabalhos:

* Um trabalho de **atualização** que regenera o arquivo de bloqueio no push e faz commit do resultado. Esse trabalho precisa das permissões `contents: write`, e suas regras ou conjuntos de regras de proteção de ramificação devem permitir que GitHub Actions faça push para os branches em que ele é executado.
* Um trabalho **de verificação** executado `gh actions-lock --verify` em pull requests. Isso deve falhar com erro se o arquivo de bloqueio estiver obsoleto, tornando-o útil para uma verificação necessária.

### Uma Copilot habilidade

Ao Copilot editar um arquivo de fluxo de trabalho, faça com que execute o comando para atualizar o arquivo de bloqueio no mesmo conjunto de alterações.

O recurso deve informar Copilot para regenerar o arquivo de bloqueio com a CLI sempre que houver alterações em um fluxo de trabalho ou em uma ação local, e nunca editar o arquivo de bloqueio diretamente. Isso abrange apenas edições feitas com Copilot, portanto, trate-a como uma conveniência em vez de um controle. Consulte [Habilidades do agente](https://docs.github.com/pt/copilot/concepts/agents/about-agent-skills).

### Um hook de pré-commit

Isso captura um arquivo de bloqueio obsoleto antes que um commit exista, que é o feedback mais antigo que um desenvolvedor pode obter.

Use `gh actions-lock --verify-local --no-fix` no hook. Ele funciona offline, não precisa de autenticação e é rápido o suficiente para ser executado a cada commit. Esse comando confirma que cada dependência tem uma entrada de arquivo de bloqueio, mas não verifica novamente as versões fixadas em relação a GitHub.

## 3. Configurar um processo de revisão para alterações de lockfile

Um arquivo de bloqueio será apenas um controle de segurança se alguém ler o diff. Uma SHA de commit alterada informa que o código executado pelos seus fluxos de trabalho foi alterado.

1. Adicione `.github/workflows/actions.lock` ao arquivo `CODEOWNERS` para que a equipe responsável pela segurança do build seja solicitada automaticamente para revisão. Consulte [Sobre os proprietários de código](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
2. Configure uma regra de proteção de branch ou um conjunto de regras de repositório para exigir aprovação de um proprietário de código.
3. Diga aos revisores o que procurar. Para obter diretrizes, confira [Bloqueio de dependências de ação nos fluxos de trabalho de um repositório](../secure-your-work/lock-workflow-dependencies.md#reviewing-lockfile-changes).

## 4. Aplicar a política

Quando você estiver confiante de que os arquivos de bloqueio estão em vigor e permanecerão atualizados, altere o status de imposição da política **Exigir arquivo de bloqueio** para **Ativo** e verifique se todos os repositórios e fluxos de trabalho integrados são direcionados.

Deixe a verificação da etapa 2 como está. A política bloqueará uma execução de workflow que não tem nenhum lockfile válido, mas uma verificação informa a um autor que seu lockfile está obsoleto enquanto ainda está trabalhando no pull request.
