---
title: Reexecutando fluxos de trabalho e tarefas
description: Você pode executar novamente um fluxo de trabalho, todos os trabalhos que falharam na execução de um fluxo de trabalho, ou trabalhos específicos em uma execução de fluxo de trabalho até 30 dias após sua execução inicial.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
captured: '2026-10-11'
section: GitHub Actions
---

# Reexecutando fluxos de trabalho e tarefas

_Você pode executar novamente um fluxo de trabalho, todos os trabalhos que falharam na execução de um fluxo de trabalho, ou trabalhos específicos em uma execução de fluxo de trabalho até 30 dias após sua execução inicial._

As re-execuções usam os privilégios do ator que inicialmente disparou o fluxo de trabalho, não os privilégios do ator que iniciou a nova execução. O fluxo de trabalho também usará o mesmo `GITHUB_SHA` (commit SHA) e `GITHUB_REF` (git ref) do evento original que disparou a execução do fluxo de trabalho.

Uma execução de fluxo de trabalho pode ser executada novamente no máximo 50 vezes. Esse limite inclui tanto reexecuções completas quanto reexecuções de um subconjunto de tarefas.

## Reexecutar todos os trabalhos em um fluxo de trabalho

<div class="ghd-tool webui">

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. No canto superior direito do fluxo de trabalho, execute novamente os trabalhos.

   * Se algum trabalho falhar, selecione o **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-sync" aria-label="sync" role="img"><path d="M1.705 8.005a.75.75 0 0 1 .834.656 5.5 5.5 0 0 0 9.592 2.97l-1.204-1.204a.25.25 0 0 1 .177-.427h3.646a.25.25 0 0 1 .25.25v3.646a.25.25 0 0 1-.427.177l-1.38-1.38A7.002 7.002 0 0 1 1.05 8.84a.75.75 0 0 1 .656-.834ZM8 2.5a5.487 5.487 0 0 0-4.131 1.869l1.204 1.204A.25.25 0 0 1 4.896 6H1.25A.25.25 0 0 1 1 5.75V2.104a.25.25 0 0 1 .427-.177l1.38 1.38A7.002 7.002 0 0 1 14.95 7.16a.75.75 0 0 1-1.49.178A5.5 5.5 0 0 0 8 2.5Z"></path></svg> menu suspenso Executar trabalhos novamente** e clique **Executar novamente todos os trabalhos**.
   * Se nenhum trabalho falhar, clique em **Executar novamente todos os trabalhos**.

6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).

7. Clique em **Executar trabalhos novamente**.

</div>

<div class="ghd-tool cli">

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

</div>

## Reexecutar trabalhos que falharam em um fluxo de trabalho

<div class="ghd-tool webui">

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. No canto superior direito do fluxo de trabalho, selecione o menu suspenso <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-sync" aria-label="sync" role="img"><path d="M1.705 8.005a.75.75 0 0 1 .834.656 5.5 5.5 0 0 0 9.592 2.97l-1.204-1.204a.25.25 0 0 1 .177-.427h3.646a.25.25 0 0 1 .25.25v3.646a.25.25 0 0 1-.427.177l-1.38-1.38A7.002 7.002 0 0 1 1.05 8.84a.75.75 0 0 1 .656-.834ZM8 2.5a5.487 5.487 0 0 0-4.131 1.869l1.204 1.204A.25.25 0 0 1 4.896 6H1.25A.25.25 0 0 1 1 5.75V2.104a.25.25 0 0 1 .427-.177l1.38 1.38A7.002 7.002 0 0 1 14.95 7.16a.75.75 0 0 1-1.49.178A5.5 5.5 0 0 0 8 2.5Z"></path></svg> e clique em **Reexecutar trabalhos com falha**.
6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).
7. Clique em **Executar trabalhos novamente**.

</div>

<div class="ghd-tool cli">

Para executar os trabalhos com falha novamente em uma execução de fluxo de trabalho, use o subcomando `run rerun` com o sinalizador `--failed`. Substitua `RUN_ID` pelo ID da execução para a qual você deseja reiniciar os trabalhos que falharam. Se você não especificar um `run-id`, GitHub CLI retornará um menu interativo para escolher uma execução com falha recente.

```shell
gh run rerun RUN_ID --failed
```

Para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, use o sinalizador `--debug`.

```shell
gh run rerun RUN_ID --failed --debug
```

</div>

## Reexecutando um trabalho específico em um fluxo de trabalho

<div class="ghd-tool webui">

1. Em GitHub, acesse a página principal do repositório.

2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)

3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)

4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.

5. Na seção "Trabalhos" da barra lateral esquerda, ao lado do trabalho que você deseja executar novamente, clique em <svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-sync" aria-label="The re-run icon" role="img"><path d="M1.705 8.005a.75.75 0 0 1 .834.656 5.5 5.5 0 0 0 9.592 2.97l-1.204-1.204a.25.25 0 0 1 .177-.427h3.646a.25.25 0 0 1 .25.25v3.646a.25.25 0 0 1-.427.177l-1.38-1.38A7.002 7.002 0 0 1 1.05 8.84a.75.75 0 0 1 .656-.834ZM8 2.5a5.487 5.487 0 0 0-4.131 1.869l1.204 1.204A.25.25 0 0 1 4.896 6H1.25A.25.25 0 0 1 1 5.75V2.104a.25.25 0 0 1 .427-.177l1.38 1.38A7.002 7.002 0 0 1 14.95 7.16a.75.75 0 0 1-1.49.178A5.5 5.5 0 0 0 8 2.5Z"></path></svg>.

6. Opcionalmente, para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, selecione **Habilitar o log de depuração**. Para saber mais, confira [Habilitando o log de depuração](../monitor-workflows/enable-debug-logging.md).

7. Clique em **Executar trabalhos novamente**.

</div>

<div class="ghd-tool cli">

Para executar novamente um trabalho específico em uma execução de fluxo de trabalho, use o subcomando `run rerun` com o sinalizador `--job`. Substitua `JOB_ID` pela ID do trabalho que deseja executar novamente.

```shell
gh run rerun --job JOB_ID
```

Para habilitar o log de diagnóstico do executor e o log de depuração de etapas para a nova execução, use o sinalizador `--debug`.

```shell
gh run rerun --job JOB_ID --debug
```

</div>

## Revisando execuções de workflows anteriores

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Actions**.

   ![Captura de tela das guias do repositório "github/docs". A guia "Ações" está realçada com um contorno laranja.](/assets/images/help/repository/actions-tab-global-nav-update.png)
3. Na barra lateral esquerda, clique no fluxo de trabalho que deseja ver.

   ![Captura de tela da barra lateral esquerda da guia "Ações". Um fluxo de trabalho, "CodeQL", é descrito em laranja escuro.](/assets/images/help/actions/superlinter-workflow-sidebar.png)
4. Na lista de execuções de fluxo de trabalho, clique no nome da execução para ver o resumo da execução do fluxo de trabalho.
5. À direita do nome da execução, selecione o menu suspenso **Mais recente** e clique em uma tentativa de execução anterior.
