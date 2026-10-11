---
title: Uso seguro de pull_request_target
description: Saiba mais sobre os riscos de segurança do pull_request_target evento.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/security/securely-using-pull_request_target
captured: '2026-10-11'
section: GitHub Actions
---

# Uso seguro de pull_request_target

_Saiba mais sobre os riscos de segurança do pull_request_target evento._

Este guia ajuda você a avaliar se o fluxo de trabalho deve usar o `pull_request_target` evento e entender os riscos de segurança envolvidos. Ele também explica as proteções que GitHub se aplicam a esses riscos por padrão e como recusar essas proteções, se necessário.

## Riscos de `pull_request_target`

Fluxos de trabalho acionados por `pull_request_target` são executados com confiança elevada: o job recebe o `GITHUB_TOKEN` do repositório base e acesso aos segredos do repositório e da organização. São os mesmos privilégios dados a eventos como `push`, que apenas colaboradores podem disparar, e é isso que torna `pull_request_target` útil para automações que respondem a solicitações pull de bifurcações, como rotulagem, triagem ou a publicação de verificações de status autenticadas.

Para entender por que isso é seguro por padrão e como essa segurança geralmente é comprometida, analise `pull_request_target` em relação a [`pull_request`](../workflows-and-actions/events-that-trigger-workflows.md#pull_request).

O evento `pull_request` (assim como `pull_request_review` e `pull_request_review_comment`) é incomum: ele executa o arquivo do fluxo de trabalho a partir da **confirmação de mescla da solicitação pull**. Para uma solicitação pull aberta em uma bifurcação, essa confirmação é controlada por alguém sem acesso de gravação ao repositório base. Para executar com segurança um código de fluxo de trabalho não confiável, GitHub restringe esses eventos a um `GITHUB_TOKEN`somente leitura, bloqueia o acesso a outros segredos e aplica políticas de aprovação para bifurcações para evitar abuso de recursos computacionais. Por padrão, `actions/checkout` em um `pull_request` fluxo de trabalho também verifica a confirmação de mesclagem da solicitação de pull, de modo que o código verificado e o fluxo de trabalho executado são consistentes.

`pull_request_target` faz uma mudança crítica e sutil: o fluxo de trabalho e qualquer chamada subsequente de `actions/checkout` que não especifique um `ref` são obtidos da **ramificação padrão do repositório base**, e não da solicitação pull. Como apenas o código confiável do branch padrão é executado, é seguro conceder segredos e um token de leitura/gravação. Nenhum código da bifurcação é executado por padrão.

Você gera um risco quando o autor do fluxo de trabalho substitui esse padrão para executar o código da bifurcação. Os desenvolvedores geralmente escolhem `pull_request_target` porque desejam executar a solicitação de pull de uma bifurcação por meio da CI *e* têm acesso a segredos, por exemplo, para executar testes que precisam de um registro privado. Para fazer isso, eles apontam `actions/checkout` para o cabeçalho da solicitação pull em vez da ramificação padrão, o que não é seguro:

```yaml
# INSECURE. Provided as an example only.
on:
  pull_request_target:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - name: Test
        run: make test
```

A etapa de check-out por si só não executa código não confiável. O arquivo de fluxo de trabalho em si ainda vem da ramificação padrão. A vulnerabilidade é concluída pela *próxima* etapa que executa o check-out de código no diretório de trabalho atual. Aqui, `make test` executa uma `Makefile` obtida do cabeçalho da solicitação pull. Um invasor só precisa abrir um pull request a partir de um fork em que `Makefile` (ou script de build, comando de teste, dependência ou arquivo de configuração) contenha comandos maliciosos. Esses comandos são executados com os segredos e o token do repositório base.

Esse padrão é conhecido como "pwn request" e tem sido a causa raiz de vários comprometimentos na cadeia de suprimentos. Para obter mais informações, consulte [Como evitar solicitações pwn](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/) no GitHub Security Lab. Formas vulneráveis comuns incluem:

* Verificando o cabeçalho de uma solicitação pull ou a confirmação de mescla em `actions/checkout` (`ref: ${{ github.event.pull_request.head.sha }}`, `ref: refs/pull/${{ github.event.pull_request.number }}/merge`) e, em seguida, compilando, testando ou executando o resultado.
* Definindo `repository:` para a bifurcação (`repository: ${{ github.event.pull_request.head.repo.full_name }}`) para receber a ramificação da bifurcação diretamente.
* Buscando o código da solicitação pull fora de `actions/checkout` (por exemplo, com `git fetch`, `gh pr checkout` ou baixando um artefato de uma execução de `pull_request` de uma bifurcação) e executando-o.

As solicitações pwn também não são exclusivas para `pull_request_target`. Qualquer evento que seja executado com segredos pode introduzir uma solicitação pwn se fizer check-out ou baixar e executar código não confiável. Por exemplo, um fluxo de trabalho `issue_comment` ou `workflow_run` que busca e executa o código de uma pull request de um fork é vulnerável da mesma forma. Um fluxo de trabalho `workflow_run` deve tratar artefatos carregados por outros fluxos de trabalho como dados não confiáveis, pois o conteúdo pode vir de uma bifurcação.

## Política padrão para `pull_request_target`

Para ajudar a proteger seus fluxos de trabalho contra solicitações de pull não confiáveis, GitHub fornece uma política de evento padrão que bloqueia o `pull_request_target` evento em repositórios públicos.

### Como funciona a política padrão

Para repositórios públicos que ainda não têm uma política de evento actions aplicável, GitHub adiciona uma política padrão que bloqueia os fluxos de trabalho disparados por `pull_request_target`. Para obter mais informações sobre políticas, consulte [Sobre as políticas do Actions](../../concepts/about-actions-policies.md).

<!-- expires 2026-11-02 -->

<!-- default policy flips to active -->

A política padrão:

* Não se aplica a repositórios privados ou internos.
* Não substitui uma política de evento aplicável que você já configurou.
* Atualmente, é executado no modo **de avaliação** . Nesse modo, as execuções do fluxo de trabalho continuam, mas você pode usar as informações da política para identificar execuções que seriam bloqueadas após a aplicação da política.

Em 2 de novembro de 2026, GitHub imporá a política padrão para repositórios afetados que estavam usando a política padrão `pull_request_target` antes da disponibilidade geral.

<!-- end expires 2026-11-02 -->

### Revisar o impacto antes da imposição

Enquanto a política estiver no modo de avaliação, examine seus insights de política para identificar os fluxos de trabalho que usam `pull_request_target` e serão bloqueados quando a política for imposta.

Para cada fluxo de trabalho afetado, decida se `pull_request_target` ainda é necessário:

* Se o fluxo de trabalho não precisar `pull_request_target`, atualize-o para usar um evento mais seguro quando apropriado, como `pull_request`.
* Se o fluxo de trabalho precisar continuar a usar `pull_request_target`, crie ou atualize uma política de evento de Ações aplicável que permita `pull_request_target`explicitamente.
* Se você não quiser permitir `pull_request_target`, deixe a política padrão em vigor. Após a imposição, GitHub bloqueará os fluxos de trabalho disparados por esse evento.

> \[!WARNING]
> `pull_request_target` Permitir somente quando for necessário. Os fluxos de trabalho acionados por este evento não devem obter, compilar nem executar código de um pull request não confiável com acesso aos segredos do repositório ou a um `GITHUB_TOKEN` privilegiado.

Para obter mais informações sobre como configurar políticas de eventos e exibir insights, consulte [Controlando quem pode executar GitHub Actions fluxos de trabalho](../../how-tos/administer/control-workflow-execution.md). Para gerenciar políticas programaticamente, consulte [Pontos de extremidade da API REST para políticas de GitHub Actions](https://docs.github.com/pt/rest/actions/policies).

## Decidir se deve ser usado `pull_request_target`

Alguns fluxos de trabalho precisam obter o código da solicitação pull de uma bifurcação com mais privilégios, e foi por isso que `pull_request_target` foi criado desde o início. Por exemplo, gerar relatórios de cobertura que exigem um registro privado de artefatos ou gerar e executar verificações autenticadas nas alterações introduzidas pelo pull request. Considere as perguntas abaixo antes de usar `pull_request_target` ou ativar a flag `allow-unsafe-pr-checkout` em `actions/checkout`.

* **Você pode usar `pull_request` em vez disso?**
  `pull_request` é acionado pelos mesmos eventos que `pull_request_target` e executa o código do fluxo de trabalho do branch de mesclagem `pull_request`. Ele faz isso com segurança em solicitações pull de bifurcações com as proteções detalhadas acima. Se o acesso ao segredo adicional não for necessário, use `pull_request`. Fluxos de trabalho mais complexos podem ser reestruturados para separar o tratamento potencialmente perigoso do código de solicitação de pull do acesso a segredos. Para obter mais informações, consulte [Como evitar solicitações pwn](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/#preventing-pwn-requests) no GitHub Security Lab.

* **O código de check-out já foi executado?** Essa é a falha que apresenta vulnerabilidades de solicitação pwn. Isso costuma ser introduzido com `actions/checkout` ao fazer check-out do cabeçalho de uma solicitação pull no diretório de trabalho e, em seguida, executá-la. A menos que a `path` entrada seja definida, `actions/checkout` grava o código no `$GITHUB_WORKSPACE` diretório, que normalmente é o diretório de trabalho em que os comandos subsequentes são executados. A execução não está limitada às suas próprias etapas: comandos de compilação e teste, como `npm install` e `npm run build`, além de arquivos de configuração e dependências que o código traz com ele, podem executar código controlado pelo invasor. A execução não requer uma etapa de build óbvia.
  **Você deve garantir que o código extraído seja inspecionado apenas como dados e nunca executado antes de usar um evento `pull_request_target`**.

## Reforço da segurança de um `pull_request_target` fluxo de trabalho

Se você tiver confirmado que precisa `pull_request_target`, aplique esses controles para limitar o impacto desse evento de alto risco. Elas se aplicam se o fluxo de trabalho verifica ou não o código da solicitação pull.

* **Restringir segredos.** Confirme se as permissões definidas em `GITHUB_TOKEN` têm os privilégios mínimos e se somente os segredos necessários do repositório e da organização são usados para o fluxo de trabalho. Para obter mais informações, consulte [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).

* **Entenda o impacto no cache.** Para reduzir o risco de envenenamento por cache, os fluxos de trabalho disparados por `pull_request_target` têm acesso somente leitura ao cache no escopo do branch padrão. Esses fluxos de trabalho podem restaurar entradas de cache existentes, mas não podem criá-las ou substituí-las, portanto, não podem afetar a execução de outros fluxos de trabalho não relacionados por meio do cache compartilhado. Se esse fluxo de trabalho tentar salvar um cache, o salvamento falhará, mas a etapa e o trabalho continuarão, e a falha será relatada como um aviso no log de fluxo de trabalho. Se o fluxo de trabalho precisar preencher o cache, salve-o de um fluxo de trabalho executado em um gatilho confiável, como `push`. Um fluxo de trabalho ou tarefa pode ficar isento desta restrição de somente leitura ao declarar explicitamente um `cache-mode` com permissão de gravação, mas fazer isso em um fluxo de trabalho `pull_request_target` reintroduz o risco de envenenamento de cache que esta restrição foi criada para evitar. Para obter mais informações, consulte [Referência do cache de dependência](../workflows-and-actions/dependency-caching.md#cache-access-for-low-trust-workflow-triggers).

* **Verifique se a computação subjacente é isolada e efêmera.** Se os executores auto-hospedados forem usados, você deverá confirmar se o ambiente do executor está devidamente restrito nos recursos internos e não é reutilizado entre execuções de GitHub Actions. Para obter mais informações, consulte [Referência de uso seguro](secure-use.md#hardening-for-self-hosted-runners).

* **Impor práticas recomendadas de GitHub Actions segurança.** Além dos riscos específicos de solicitações pwn, outras vulnerabilidades comuns, como injeção de comando, podem existir e afetar o código executado neste evento privilegiado. Para obter mais informações, consulte [Como manter seus GitHub Actions e fluxos de trabalho seguros: entrada não confiável](https://securitylab.github.com/resources/github-actions-untrusted-input/) no GitHub Security Lab. Para identificar e proteger proativamente contra vulnerabilidades comuns GitHub Actions , habilite CodeQL para GitHub Actions. Para obter mais informações, consulte [Como definir a configuração padrão da verificação de código](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning).

## Recusar proteções internas

Se você analisou as perguntas acima e confirmou que seu fluxo de trabalho requer `pull_request_target` e o utiliza com segurança, pode desativar a política padrão de eventos e a proteção `actions/checkout`.

Definir `allow-unsafe-pr-checkout: true` como uma entrada de `actions/checkout` permite fazer check-out de referências de cabeçalho de solicitações pull de bifurcações. Faça isso somente após confirmar que o código extraído nunca é executado. A entrada é nomeada intencionalmente para ser fácil de detectar na revisão de código e na análise estática.

Essa proteção abrange somente referências de solicitação pull de bifurcações. Verificar outro código não confiável, como um repositório de terceiros não relacionado, buscar código com `git fetch` ou `gh pr checkout`executar um artefato baixado, não é coberto pelas `actions/checkout` verificações.
