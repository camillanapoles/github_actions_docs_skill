---
title: Reexecutando fluxos de trabalho e tarefas
description: Você pode executar novamente um fluxo de trabalho, todos os trabalhos que falharam na execução de um fluxo de trabalho, ou trabalhos específicos em uma execução de fluxo de trabalho até 30 dias após sua execução inicial.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
captured: '2026-10-26'
section: How tos / Manage workflow runs
---

# Reexecutando fluxos de trabalho e tarefas

_Você pode executar novamente um fluxo de trabalho, todos os trabalhos que falharam na execução de um fluxo de trabalho, ou trabalhos específicos em uma execução de fluxo de trabalho até 30 dias após sua execução inicial._

As re-execuções usam os privilégios do ator que inicialmente disparou o fluxo de trabalho, não os privilégios do ator que iniciou a nova execução. O fluxo de trabalho também usará o mesmo `GITHUB_SHA` (commit SHA) e `GITHUB_REF` (git ref) do evento original que disparou a execução do fluxo de trabalho.

Uma execução de fluxo de trabalho pode ser executada novamente no máximo 50 vezes. Esse limite inclui tanto reexecuções completas quanto reexecuções de um subconjunto de tarefas.

Você não pode executar novamente uma execução de fluxo de trabalho ou qualquer um de seus trabalhos enquanto o fluxo de trabalho está desabilitado. Você precisa habilitar o fluxo de trabalho primeiro. Consulte [Desabilitar e habilitar um fluxo de trabalho](disable-and-enable-workflows.md).

## Reexecutar todos os trabalhos em um fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. No canto superior direito do fluxo de trabalho, execute novamente os trabalhos.

   * Se algum trabalho falhar, selecione o **(sync) menu suspenso Executar trabalhos novamente** e clique **Executar novamente todos os trabalhos**.
   * Se nenhum trabalho falhar, clique em **Executar novamente todos os trabalhos**.

6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).

7. Clique em **Executar trabalhos novamente**.

1. Para executar novamente uma execução de fluxo de trabalho com falha, use o subcomando `run rerun`, substituindo `RUN_ID` pela ID da execução com falha que você deseja executar novamente. Se você não especificar um `run-id`, GitHub CLI retornará um menu interativo para escolher uma execução com falha recente.

            ```shell copy
   gh run rerun RUN_ID
   ```

   Para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, use o sinalizador `--debug`.

            ```shell copy
   gh run rerun RUN_ID --debug
   ```

2. Para ver o progresso da execução do fluxo de trabalho, use o subcomando `run watch` e selecione a execução na lista interativa.

            ```shell copy
   gh run watch
   ```

## Reexecutar trabalhos que falharam em um fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. No canto superior direito do fluxo de trabalho, selecione o menu suspenso (sync) e clique em **Reexecutar trabalhos com falha**.
6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).
7. Clique em **Executar trabalhos novamente**.

Para executar os trabalhos com falha novamente em uma execução de fluxo de trabalho, use o subcomando `run rerun` com o sinalizador `--failed`. Substitua `RUN_ID` pelo ID da execução para a qual você deseja reiniciar os trabalhos que falharam. Se você não especificar um `run-id`, GitHub CLI retornará um menu interativo para escolher uma execução com falha recente.

```shell
gh run rerun RUN_ID --failed
```

Para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, use o sinalizador `--debug`.

```shell
gh run rerun RUN_ID --failed --debug
```

## Reexecutando um trabalho específico em um fluxo de trabalho

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. Na seção "Trabalhos" da barra lateral esquerda, ao lado do trabalho que você deseja executar novamente, clique em (The re-run icon).

6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).

7. Clique em **Executar trabalhos novamente**.

Para executar novamente um trabalho específico em uma execução de fluxo de trabalho, use o subcomando `run rerun` com o sinalizador `--job`. Substitua `JOB_ID` pela ID do trabalho que deseja executar novamente.

```shell
gh run rerun --job JOB_ID
```

Para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, use o sinalizador `--debug`.

```shell
gh run rerun --job JOB_ID --debug
```

## Revisando execuções de workflows anteriores

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(play) Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](https://docs.github.com/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](https://docs.github.com/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. À direita do nome da execução, selecione o menu suspenso **Mais recente** e clique em uma tentativa de execução anterior.
