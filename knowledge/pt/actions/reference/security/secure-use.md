---
title: Referência de uso seguro
description: Práticas de segurança para escrever fluxos de trabalho e usar GitHub Actions recursos.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/security/secure-use
captured: '2026-10-13'
section: Reference / Security
---

# Referência de uso seguro

_Práticas de segurança para escrever fluxos de trabalho e usar GitHub Actions recursos._

Encontre informações sobre as práticas recomendadas de segurança ao escrever fluxos de trabalho e usar GitHub Actions recursos de segurança.

## Escrevendo fluxos de trabalho

### Usar segredos para informações confidenciais

Como há várias maneiras de transformar o valor de um segredo, a ocultação automática não é garantida. Siga as práticas recomendadas a seguir para limitar os riscos associados aos segredos.

* **Princípio de privilégios mínimos**
  * Qualquer usuário com permissão de escrita no seu repositório tem acesso de leitura a todos os segredos configurados no repositório. Portanto, você deve garantir que as credenciais que estão sendo usadas nos fluxos de trabalho tenham os privilégios mínimos necessários.
  * Ações podem usar o `GITHUB_TOKEN` acessando-o a partir do contexto `github.token`. Para saber mais, confira [Referência de contextos](../workflows-and-actions/contexts.md#github-context). Portanto, você deve verificar se o `GITHUB_TOKEN` recebeu as permissões mínimas necessárias. É uma boa prática de segurança definir a permissão padrão para o `GITHUB_TOKEN` como somente acesso de leitura no conteúdo do repositório. As permissões podem ser aumentadas, conforme necessário, para tarefas individuais dentro do arquivo do fluxo de trabalho. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).
* **Mascarar dados confidenciais**
  * Dados confidenciais **nunca** devem ser armazenados como texto sem formatação em arquivos de fluxo de trabalho. Mascarar todas as informações confidenciais que não são um GitHub segredo usando `::add-mask::VALUE`. Isso faz com que o valor seja tratado como um segredo e ocultado dos logs. Para obter mais informações sobre como colocar máscara em dados, confira [Comandos de fluxo de trabalho para o GitHub Actions](../workflows-and-actions/workflow-commands.md#masking-a-value-in-a-log).
* **Excluir e girar segredos expostos**
  * A ocultação dos segredos é realizada pelos seus executores de fluxos de trabalho. Isso significa que um segredo será ocultado somente se tiver sido usado em um trabalho e for acessível pelo executor. Caso um segredo não ocultado seja enviado para um log de execução de fluxos de trabalho, você deverá excluir o log e substituir o segredo. Para obter mais informações sobre como excluir logs, confira [Usando registros de execução de fluxo de trabalho](../../how-tos/monitor-workflows/use-workflow-run-logs.md#deleting-logs).
* **Nunca usar dados estruturados como um segredo**
  * Os dados estruturados podem fazer com que ocorra uma falha nos registros de segredos, pois a redação depende, em grande parte, de encontrar uma correspondência exata para o valor específico do segredo. Por exemplo, não use um blob de JSON, XML, ou YAML (ou similar) para encapsular o valor de um segredo, já que isso reduz significativamente a probabilidade de os segredos serem devidamente redigidos. Em vez disso, crie segredos individuais para cada valor sensível.
* **Registrar todos os segredos usados nos fluxos de trabalho**
  * Se um segredo for usado para gerar outro valor confidencial em um fluxo de trabalho, esse valor gerado deverá ser [formalmente registrado como um segredo](https://github.com/actions/toolkit/tree/main/packages/core#setting-a-secret), para que seja editado se aparecer nos logs. Por exemplo, se, ao usar uma chave privada para gerar um JWT assinado para acessar uma API web, certifique-se de registrar que JWT é um segredo ou não será redigido se entrar na saída de do registro.
  * O registro de segredos também aplica-se a qualquer tipo de transformação/codificação. Se seu segredo foi transformado de alguma forma (como Base64 ou URL codificada), certifique-se de registrar o novo valor como um segredo também.
* **Auditar a forma como os segredos são tratados**
  * Audite como os segredos são usados, para ajudar a garantir que estejam sendo tratados conforme o esperado. Você pode fazer isso revisando o código-fonte do repositório que executa o fluxo de trabalho e verificando quaisquer ações usadas no fluxo de trabalho. Por exemplo, verifique se eles não são enviados para hosts não pretendidos, ou impressos explicitamente na saída de um registro.
  * Visualize os registros de execução do seu fluxo de trabalho depois de testar entradas válidas/inválidas e, em seguida, verifique se os segredos estão sendo editados corretamente ou não são mostrados. Nem sempre é óbvio como um comando ou uma ferramenta que você está invocando enviará erros para `STDOUT` e `STDERR`, e os segredos podem acabar nos logs de erros. Como resultado, considera-se uma boa prática rever manualmente os registros do fluxo de trabalho depois de testar entradas válidas e inválidas. Para obter informações sobre como limpar logs de fluxo de trabalho que podem conter dados confidenciais involuntariamente, consulte [Usando registros de execução de fluxo de trabalho](../../how-tos/monitor-workflows/use-workflow-run-logs.md#deleting-logs).
* **Auditar e substituir os segredos registrados**
  * Reveja, periodicamente, os segredos registrados para confirmar se ainda são necessários. Remova aqueles que não são mais necessários.
  * Gire os segredos periodicamente para reduzir a janela de tempo durante a qual um segredo comprometido é válido.
* **Considerar a necessidade de revisão para acesso a segredos**
  * Você pode usar revisores necessários para proteger os segredos do ambiente. Um trabalho de fluxo de trabalho não pode acessar segredos de ambiente até que a aprovação seja concedida por um revisor. Para obter mais informações sobre como armazenar segredos em ambientes ou exigir revisões de ambientes, confira [Usar segredos em ações do GitHub](../../how-tos/write-workflows/choose-what-workflows-do/use-secrets.md) e [Gerenciar ambientes para implantação](../../how-tos/deploy/configure-and-manage-deployments/manage-environments.md).

### Práticas recomendadas para mitigar ataques de injeção de script

Abordagens recomendadas para atenuar o risco de injeção de script em seus fluxos de trabalho:

#### Usar uma ação em vez de um script embutido

A abordagem recomendada é criar uma ação JavaScript que processa o valor do contexto como um argumento. Essa abordagem não é vulnerável ao ataque de injeção, pois o valor do contexto não é usado para gerar um script do shell, mas é passado para a ação como um argumento:

```yaml
uses: fakeaction/checktitle@v3
with:
  title: ${{ github.event.pull_request.title }}
```

#### Usar uma variável de ambiente intermediária

Para scripts em linha, a abordagem preferida para manipular entradas não confiáveis é definir o valor da expressão para uma variável de ambiente intermediário. O seguinte exemplo usa o Bash para processar o valor `github.event.pull_request.title` como uma variável de ambiente:

```yaml
      - name: Check PR title
        env:
          TITLE: ${{ github.event.pull_request.title }}
        run: |
          if [[ "$TITLE" =~ ^octocat ]]; then
          echo "PR title starts with 'octocat'"
          exit 0
          else
          echo "PR title did not start with 'octocat'"
          exit 1
          fi
```

Neste exemplo, a tentativa de injeção de script não é bem-sucedida, o que é refletido pelas seguintes linhas no log:

```shell
   env:
     TITLE: a"; ls $GITHUB_WORKSPACE"
PR title did not start with 'octocat'
```

Com essa abordagem, o valor da `${{ github.event.pull_request.title }}` expressão é armazenado na memória e usado como uma variável e não interage com o processo de geração de script. Além disso, considere usar variáveis de shell de aspas duplas para evitar a [divisão de palavras](https://github.com/koalaman/shellcheck/wiki/SC2086), mas essa é [uma das muitas](https://mywiki.wooledge.org/BashPitfalls) recomendações gerais para escrever scripts de shell e não é específica para GitHub Actions.

#### Usando modelos de fluxo de trabalho para code scanning

Code scanning permite que você encontre vulnerabilidades de segurança antes que elas cheguem à produção.
GitHub fornece modelos de fluxo de trabalho para code scanning. Você pode usar esses fluxos de trabalho sugeridos para construir seus code scanning fluxos de trabalho, em vez de começar do zero. o fluxo de trabalho de GitHub, o Fluxo de trabalho de análise do CodeQL, é alimentado por CodeQL. Também existem modelos de fluxo de trabalho de terceiros disponíveis.

Para saber mais, confira [Análise de código](https://docs.github.com/pt/code-security/concepts/code-scanning/code-scanning) e [Como definir a configuração avançada para verificação de código](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configuring-advanced-setup-for-code-scanning#configuring-code-scanning-using-third-party-actions).

#### Restringir permissões para tokens

Para ajudar a mitigar o risco de um token exposto, considere restringir as permissões atribuídas. Para saber mais, confira [Usar GITHUB_TOKEN para autenticação em fluxos de trabalho](../../tutorials/authenticate-with-github_token.md#modifying-the-permissions-for-the-github_token).

## Mitigando os riscos do check-out de código não confiável

De maneira semelhante aos ataques de injeção de script, conteúdos de pull request não confiáveis que disparam automaticamente o processamento de ações também podem representar um risco de segurança. Os gatilhos de fluxo de trabalho `pull_request_target` e `workflow_run`, quando usados com o check-out de uma pull request não confiável, expõem o repositório a comprometimentos de segurança. Esses fluxos de trabalho são privilegiados, o que significa que compartilham o mesmo cache da ramificação principal com outros gatilhos de fluxo de trabalho privilegiados, e podem ter acesso de gravação ao repositório e acesso a segredos referenciados. Essas vulnerabilidades podem ser exploradas para roubar um repositório.

Para saber mais sobre esses gatilhos, como usá-los e os riscos associados, confira [Eventos que disparam fluxos de trabalho](../workflows-and-actions/events-that-trigger-workflows.md#pull_request_target) e [Eventos que disparam fluxos de trabalho](../workflows-and-actions/events-that-trigger-workflows.md#workflow_run).

Para obter mais exemplos e orientações sobre os riscos do checkout de código não confiável, consulte [Prevenção de solicitações pwn](https://securitylab.github.com/research/github-actions-preventing-pwn-requests/) a partir de GitHub Security Lab e a documentação [Dangerous-Workflow](https://github.com/ossf/scorecard/blob/main/docs/checks.md#dangerous-workflow) do OpenSSF Scorecard.

Para obter orientações detalhadas sobre como decidir se deseja usar `pull_request_target`, proteger esses fluxos de trabalho e recusar a `actions/checkout` proteção, consulte [Uso seguro de pull_request_target](securely-using-pull_request_target.md).

### Boas práticas

* Evite usar o gatilho do fluxo de trabalho `pull_request_target` se não for necessário. Para fins de separação de privilégios entre fluxos de trabalho, `workflow_run` é um gatilho melhor. Use esses gatilhos de fluxo de trabalho somente quando o fluxo de trabalho realmente precisar do contexto privilegiado.

* Evite usar os gatilhos de fluxo de trabalho `pull_request_target` e `workflow_run` com conteúdo de código ou pull requests não confiáveis. Fluxos de trabalho que usam esses gatilhos não devem fazer check-out explicitamente de código não confiável, incluindo forks de pull requests ou repositórios que não estão sob seu controle. Fluxos de trabalho disparados em `workflow_run` devem tratar artefatos carregados de outros fluxos de trabalho com cautela.

* CodeQL pode examinar e detectar fluxos de trabalho potencialmente vulneráveis GitHub Actions . Você pode definir as configurações padrão do repositório e garantir que a verificação GitHub Actions esteja ativada. Para saber mais, confira [Como definir a configuração padrão da verificação de código](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning).

* O OpenSSF Scorecards pode ajudá-lo a identificar fluxos de trabalho potencialmente vulneráveis, juntamente com outros riscos de segurança ao usar GitHub Actions. Confira [Como usar o OpenSSF Scorecards para proteger dependências de fluxo de trabalho](#using-openssf-scorecards-to-secure-workflow-dependencies) mais adiante neste artigo.

## Usando ações de terceiros

Os trabalhos individuais em fluxo de trabalho podem interagir com (e comprometer) outros trabalhos. Por exemplo, um trabalho que consulta as variáveis de ambiente usadas por um trabalho posterior, que escreve arquivos para um diretório compartilhado que um trabalho posterior processa, ou ainda mais diretamente, que interage com o conector do Docker e inspeciona outros contêineres em execução e executa comandos neles.

Isso significa que comprometer uma só ação em um fluxo de trabalho pode ser muito significativo, pois essa ação comprometida terá acesso a todos os segredos configurados no repositório e poderá usar o `GITHUB_TOKEN` para fazer gravações no repositório. Consequentemente, há um risco significativo em obter ações de repositórios de terceiros em GitHub.

A melhor medida é **bloquear suas dependências do fluxo de trabalho** com um lockfile. Isso registra o commit exato de cada ação da qual seus fluxos de trabalho dependem, incluindo dependências transitivas, e verifica a identidade de cada repositório de origem em tempo de execução. Essa é a proteção mais forte disponível e substitui o pinning SHA para repositórios que a adotam. Para saber mais, confira [Arquivos de bloqueio de dependências do fluxo de trabalho](../../concepts/security/workflow-dependency-lockfiles.md).

Para repositórios que **não podem** adotar um arquivo de bloqueio, você pode:

* **Fixar as ações em um SHA de commit de comprimento completo**

  Fixe as referências de ações em um SHA de commit em seus arquivos de fluxo de trabalho. Isso ajuda a reduzir o risco de um agente mal-intencionado adicionar um backdoor ao repositório da ação, pois ele precisaria gerar uma colisão SHA-1 para uma carga de objeto Git válida. Ao selecionar um SHA, verifique se ele está no repositório da ação e não em uma bifurcação do repositório.

  Para obter um exemplo de como usar um SHA de commit de comprimento completo em um fluxo de trabalho, confira [Usando blocos de construção pré-gravados no seu fluxo de trabalho](../../how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions.md#using-shas).

* **Fixar ações em uma marca somente se você confiar no criador**

  Se você desejar de especificar uma etiqueta, certifique-se de que você confia nos criadores da ação. O selo GitHub Marketplace 'Criador verificado' é um sinal útil, pois indica que a ação foi escrita por uma equipe cuja identidade foi verificada por GitHub. Observe que há risco para esta abordagem, mesmo que você confie no autor, porque uma etiqueta pode ser movida ou excluída se um ator malicioso obtiver acesso ao repositório que armazena a ação.

Independentemente das medidas adotadas, sempre **audite o código-fonte da ação**. Certifique-se de que a ação está tratando o conteúdo do seu repositório e os segredos, como esperado. Por exemplo, verifique se os segredos não são enviados para hosts não autorizados ou se não estejam registrados inadvertidamente.

### Reutilizando fluxos de trabalho de terceiros

Os mesmos princípios descritos acima para o uso de ações de terceiros também se aplicam ao uso de fluxos de trabalho de terceiros. Você pode ajudar a mitigar os riscos associados à reutilização de fluxos de trabalho, seguindo as mesmas práticas recomendadas descritas acima. Para saber mais, confira [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md).

## recursos de segurança de GitHub

GitHub fornece muitos recursos para tornar seu código mais seguro. Você pode usar os recursos integrados de GitHub para entender as ações das quais seus fluxos de trabalho dependem, garantir que você seja notificado sobre vulnerabilidades nas ações que utiliza ou automatizar o processo de manter atualizadas as ações usadas em seus fluxos de trabalho. Se você publicar e manter ações, poderá usar GitHub para se comunicar com sua comunidade sobre vulnerabilidades e como corrigi-las. Para obter mais informações sobre os recursos de segurança oferecidos GitHub , consulte [GitHub recursos de segurança](https://docs.github.com/pt/code-security/getting-started/github-security-features#about-githubs-security-features).

### Como usar `CODEOWNERS` para monitorar alterações

Use o recurso `CODEOWNERS` para controlar como são feitas alterações nos seus arquivos de fluxo de trabalho. Por exemplo, se todos os arquivos de fluxo de trabalho forem armazenados em `.github/workflows`, você poderá adicionar esse diretório à lista de proprietários do código, de modo que todas as alterações propostas nesses arquivos exijam primeiro a aprovação de um revisor designado.

Para saber mais, confira [Sobre os proprietários de código](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).

### Usando o OpenID Connect para acessar os recursos da nuvem

Se seus GitHub Actions fluxos de trabalho precisarem acessar recursos de um provedor de nuvem que dê suporte ao OpenID Connect (OIDC), você poderá configurar seus fluxos de trabalho para autenticar diretamente no provedor de nuvem. Isso permitirá que você pare de armazenar essas credenciais como segredos de longa duração e proporcione outros benefícios de segurança. Para saber mais, confira [OpenID Connect](../../concepts/security/openid-connect.md).

!!! note
    O suporte para declarações personalizadas de OIDC não está disponível na AWS.

### Usar Dependabot version updates para manter as ações atualizadas

Você pode usar Dependabot para garantir que as referências a ações e fluxos de trabalho reutilizáveis usados em seu repositório sejam mantidas atualizadas. Ações são frequentemente atualizadas com correções de bugs e novos recursos para tornar os processos automatizados mais rápidos, seguros e confiáveis.
Dependabot elimina o esforço de manter suas dependências, pois faz isso automaticamente para você. Para saber mais, confira [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions) e [Atualizações de segurança do Dependabot](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependabot-security-updates).

### Impedir GitHub Actions de criar ou aprovar pull requests

Você pode optar por permitir ou impedir que fluxos de trabalho do GitHub Actions criem ou aprovem pull requests. Permitir que fluxos de trabalho, ou qualquer outro tipo de automação, criem ou aprovem pull requests pode representar um risco à segurança se a solicitação de pull for mesclada sem a devida supervisão.

Para obter mais informações sobre como definir essa configuração, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#preventing-github-actions-from-creating-or-approving-pull-requests) e [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#preventing-github-actions-from-creating-or-approving-pull-requests).

### Usar code scanning para proteger fluxos de trabalho

Code scanning pode detectar e sugerir melhorias automaticamente para padrões vulneráveis comuns usados em GitHub Actions fluxos de trabalho.
Para obter mais informações sobre como habilitar code scanning, consulte [Como definir a configuração padrão da verificação de código](https://docs.github.com/pt/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning).

### Como usar o OpenSSF Scorecards para proteger dependências de fluxo de trabalho

O [Scorecards](https://github.com/ossf/scorecard) é uma ferramenta de segurança automatizada que sinaliza as práticas suspeitas da cadeia de fornecedores. Você poderá usar a [ação Scorecards](https://github.com/marketplace/actions/ossf-scorecard-action) e o [modelo de fluxo de trabalho](https://github.com/actions/starter-workflows) para seguir as melhores práticas de segurança. Depois de configurada, a ação Scorecards é executada automaticamente quando há alterações no repositório e alerta os desenvolvedores sobre práticas arriscadas na cadeia de suprimentos por meio da experiência integrada code scanning. O projeto Scorecards executa um número de verificações, incluindo ataques de injeção de script, permissões de token e ações fixadas.

### Fortalecimento de segurança para executáveis hospedados GitHub

GitHubexecutáveis hospedados tomam medidas para ajudar a mitigar os riscos de segurança.

#### Análise da cadeia de suprimentos para GitHubexecutáveis hospedados

Para os GitHubexecutáveis hospedados criados a partir de imagens mantidas por GitHub, é possível visualizar uma lista de componentes de software (SBOM) para verificar quais softwares estavam pré-instalados no executável. Você pode fornecer a SBOM aos usuários, e eles podem executá-la por meio de um verificador de vulnerabilidades, que pode validar se há vulnerabilidades no produto. Se você estiver criando artefatos, poderá incluir essa SBOM na sua lista de materiais para obter uma lista completa de tudo o que foi feito para criar o software.

As SBOMs estão disponíveis para imagens de executáveis do Ubuntu, Windows e macOS mantidas por GitHub, incluindo executáveis com processadores ARM. Você pode localizar a SBOM do seu build nos ativos de versão, em <https://github.com/actions/runner-images/releases>. Uma SBOM com um nome de arquivo em formato de `sbom.IMAGE-NAME.json.zip` pode ser encontrada nos anexos de cada versão.

#### Negar acesso a hosts

Os executores hospedados pelo GitHub são provisionados com um arquivo `etc/hosts` que bloqueia o acesso à rede a vários pools de mineração de criptomoedas e sites mal-intencionados. Hosts como MiningMadness.com e cpu-pool.com são redirecionados para localhost para que não apresentem um risco de segurança significativo. Para obter mais informações, consulte [Executores hospedados no GitHub](../../concepts/runners/github-hosted-runners.md).

### Fortalecimento para executores auto-hospedados

\*\*
GitHubOs executores hospedados executam\*\* código em máquinas virtuais isoladas efêmeras e limpas, o que significa que não há como comprometer persistentemente esse ambiente ou obter acesso a mais informações do que foi colocado nesse ambiente durante o processo de inicialização.

**Auto-hospedado** para GitHub não oferecem garantias de execução em máquinas virtuais efêmeras e limpas e podem ficar comprometidos de forma persistente por código não confiável em um fluxo de trabalho.

Como resultado, os executores auto-hospedados quase [nunca devem ser usados para repositórios públicos](secure-use.md)GitHub, porque qualquer usuário pode abrir solicitações de pull no repositório e comprometer o ambiente. Da mesma forma, cuidado ao usar executores auto-hospedados em repositórios privados ou internos, pois qualquer pessoa capaz de criar um fork do repositório e abrir uma solicitação de pull (geralmente aqueles com acesso de leitura ao repositório) pode comprometer o ambiente do executável auto-hospedado, incluindo o acesso a segredos e ao `GITHUB_TOKEN` que, dependendo de suas configurações, pode conceder acesso de gravação ao repositório. Embora os fluxos de trabalho possam controlar o acesso a segredos de ambiente usando os ambientes e revisões necessários, estes fluxos de trabalho não são executados em um ambiente isolado e continuam sendo susceptíveis aos mesmos riscos quando são executados por um executor auto-hospedado.

organização podem escolher quais repositórios têm permissão para criar executores auto-hospedados em nível de repositório.

Para obter mais informações, consulte [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners).

Quando um executor auto-hospedado é definido no nível da organização ou da empresa, GitHub pode agendar fluxos de trabalho de vários repositórios para o mesmo executor. Consequentemente, uma falha de segurança nestes ambientes pode ter um grande impacto. Para ajudar a reduzir o escopo de um compromisso, você pode criar limites organizando seus executores auto-hospedados em grupos separados. Você pode restringir quais organizações e repositórios podem acessar grupos de executores. Para saber mais, confira [Gerenciar o acesso a executores auto-hospedados usando grupos](../../how-tos/manage-runners/self-hosted-runners/manage-access.md).

Você também deve considerar o ambiente das máquinas de executores auto-hospedadas:

* Que informação sensível reside na máquina configurada como um executor auto-hospedado? Por exemplo, chaves SSH privadas, tokens de acesso à API, entre outros.
* A máquina tem acesso à rede a serviços sensíveis? Por exemplo, serviços de metadados Azure ou AWS. A quantidade de informações confidenciais neste ambiente deve ser limitada ao mínimo, e você deve estar sempre ciente de que qualquer usuário capaz de invocar fluxos de trabalho terá acesso a esse ambiente.

Alguns clientes podem tentar mitigar parcialmente esses riscos implementando sistemas que destroem automaticamente o executor autogerenciado após cada execução da tarefa. No entanto, esta abordagem poderá não ser tão eficaz como pretendido, uma vez que não há forma de garantir que um executor auto-hospedado execute apenas um trabalho. Alguns trabalhos usarão segredos como argumentos de linha de comando que podem ser vistos por outro trabalho em execução no mesmo executor, como `ps x -w`. Isso pode levar a vazamento de segredos.

#### Usar os executores just-in-time

Para melhorar a segurança de registro do executor, você pode usar a API REST para criar executores JIT (just-in-time) efêmeros. Esses executores auto-hospedados executam no máximo um trabalho antes de serem removidos automaticamente do repositório, da organização ou da empresa. Para obter mais informações sobre como configurar executores JIT, confira [Pontos de extremidade da API REST para executores auto-hospedados](https://docs.github.com/pt/rest/actions/self-hosted-runners#create-configuration-for-a-just-in-time-runner-for-an-organization).

!!! note
    A reutilização de hardware para hospedar executores JIT pode gerar o risco de exposição das informações do ambiente. Use a automação para garantir que o executor JIT use um ambiente limpo. Para saber mais, confira [Referência de executores auto-hospedados](../runners/self-hosted-runners.md#ephemeral-runners-for-autoscaling).

Assim que tiver o arquivo de configuração da resposta da API REST, você poderá passá-lo para o executor na inicialização.

```shell
./run.sh --jitconfig ${encoded_jit_config}
```

#### Planejando sua estratégia de gerenciamento para executores auto-hospedados

É possível adicionar um executor auto-hospedado a vários níveis da sua hierarquia GitHub: o nível da empresa, da organização ou do repositório. Este posicionamento determina quem será poderá de gerenciar o executor:

**Gerenciamento centralizado:**

* Se você planeja ter uma equipe centralizada que detém os executores auto-hospedados, recomenda-se adicionar seus executores ao nível mais alto da organização mútua ou da empresa. Isto fornece à sua equipe um único local para visualizar e gerenciar seus executores.
* Se você tiver apenas uma única organização, adicionar seus executores ao nível da organização é, de fato, a mesma abordagem, mas você pode encontrar dificuldades se você adicionar outra organização no futuro.

**Gerenciamento descentralizado:**

* Se cada equipe gerenciar seus próprios corredores hospedados, a recomendação será adicionar os executores ao mais alto nível de propriedade da equipe. Por exemplo, se cada equipe possui sua própria organização, será mais simples se os executores também forem adicionados ao nível da organização.
* Você também pode adicionar executores no nível de repositório, mas isso adicionará uma sobrecarga de gerenciamento e também aumentará o número de executores necessários já que você não pode compartilhar executores entre repositórios.

#### Efetuando a autenticação para seu provedor de nuvem

Se você estiver usando GitHub Actions para implantar em um provedor de nuvem, ou pretender usar o HashiCorp Vault para gerenciamento de segredos, é recomendável considerar o uso do OpenID Connect para criar tokens de acesso de curta duração e com escopo bem definido para as execuções do fluxo de trabalho. Para saber mais, confira [OpenID Connect](../../concepts/security/openid-connect.md).

### Auditoria de GitHub Actions eventos

Você pode usar o log de segurança para monitorar a atividade de sua conta de usuário e o log de auditoria para monitorar a atividade em sua organização. Os logs de segurança e auditoria registram o tipo de ação, quando ela foi executada e qual conta pessoal a executou.

Por exemplo, você pode usar o log de auditoria para acompanhar o evento `org.update_actions_secret`, que acompanha as alterações nos segredos da organização.

![Captura de tela mostrando uma busca por "action:org.update_actions_secret" no log de auditoria de uma organização. Dois resultados são mostrados.](https://docs.github.com/assets/images/help/repository/audit-log-entries.png)

Para obter a lista completa de eventos que você pode encontrar no log de auditoria de cada tipo de conta, confira os seguintes artigos:

* [Eventos do log de segurança](https://docs.github.com/pt/authentication/keeping-your-account-and-data-secure/security-log-events)
* [Eventos de registro de auditoria para a sua organização](https://docs.github.com/pt/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization)

### Noções básicas sobre dependências em seus fluxos de trabalho

Você pode usar o grafo de dependência para explorar as ações que os fluxos de trabalho em seu repositório usam. O grafo de dependência é um resumo do manifesto e dos arquivos de bloqueio armazenados em um repositório. Ele também reconhece arquivos em `./github/workflows/` como manifestos, o que significa que quaisquer ações ou fluxos de trabalho referenciados usando a sintaxe `jobs[*].steps[*].uses` ou `jobs.<job_id>.uses` serão analisados como dependências.

O grafo de dependência mostra as seguintes informações sobre ações usadas em fluxos de trabalho:

* A conta ou organização proprietária da ação.
* O arquivo de fluxo de trabalho que faz referência à ação.
* A versão ou SHA à qual a ação está fixada.

No grafo de dependência, as dependências são classificadas automaticamente pela gravidade da vulnerabilidade. Se qualquer uma das ações que você usar tiver avisos de segurança, eles serão exibidos na parte superior da lista. Você pode navegar até o aviso pelo grafo de dependência e acessar as instruções para resolver a vulnerabilidade.

O grafo de dependência está habilitado para repositórios públicos e você pode optar por habilitá-lo em repositórios privados. Para obter mais informações sobre como usar o grafo de dependência, consulte [Explorar as dependências de um repositório](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/explore-dependencies).

### Estar ciente das vulnerabilidades de segurança nas ações que você usa

Para ações disponíveis no marketplace, GitHub revise os avisos de segurança relacionados e, em seguida, adicione esses avisos ao GitHub Advisory Database. Você pode pesquisar no banco de dados as ações que você usa para encontrar informações sobre vulnerabilidades existentes e instruções sobre como corrigi-las. Para simplificar sua pesquisa, use o GitHub Actions filtro no [GitHub Advisory Database](https://github.com/advisories?query=type%3Areviewed+ecosystem%3Aactions).

Você pode configurar seus repositórios para:

* Receber alertas quando as ações usadas em seus fluxos de trabalho receberem um relatório de vulnerabilidade. Para obter mais informações, confira [Monitorar as ações em seus fluxos de trabalho](#monitoring-the-actions-in-your-workflows).
* Receber notificações sobre avisos existentes quando você adiciona ou atualiza uma ação em um fluxo de trabalho. Para obter mais informações, confira [Ações de triagem para vulnerabilidades em fluxos de trabalho novos ou atualizados](#screening-actions-for-vulnerabilities-in-new-or-updated-workflows).

#### Monitorar as ações em seus fluxos de trabalho

Você pode usar Dependabot para monitorar as ações em seus fluxos de trabalho e habilitar Dependabot alerts a notificação quando uma ação usada tiver uma vulnerabilidade relatada.
Dependabot realiza uma verificação do ramo padrão dos repositórios nos quais está habilitado para detectar dependências inseguras.
Dependabot gera Dependabot alerts quando um novo aviso é adicionado ao GitHub Advisory Database ou quando uma ação que você utiliza é atualizada.

!!! note
    Dependabot só cria alertas para ações vulneráveis que usam controle de versão semântico e não criarão alertas para ações fixadas em valores SHA.

Você pode habilitar Dependabot alerts para sua conta pessoal, para um repositório ou para uma organização. Para obter mais informações, consulte [Configurando alertas do Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-dependabot-alerts).

Você pode visualizar todos os Dependabot alerts abertos e fechados e os correspondentes Dependabot security updates na guia Dependabot do repositório. Para obter mais informações, consulte [Visualizando e atualizando alertas do Dependabot](https://docs.github.com/pt/code-security/how-tos/manage-security-alerts/manage-dependabot-alerts/view-dependabot-alerts).

#### Ações de triagem para vulnerabilidades em fluxos de trabalho novos ou atualizados

Quando você abre pull requests para atualizar seus fluxos de trabalho, é uma boa prática usar a revisão de dependência para entender o impacto na segurança das alterações feitas nas ações usadas. Revisão de dependências ajuda você a entender as alterações de dependência e o impacto de segurança dessas alterações em cada pull request. Ele fornece uma visualização facilmente compreensível de mudanças de dependência, com um diff avançado na aba "Arquivos alterados" de uma solicitação de pull. A revisão de dependências informa você:

* Quais dependências foram adicionadas, removidas ou atualizadas, junto com as datas de lançamento
* Quantos projetos usam esses componentes
* Dados de vulnerabilidade para essas dependências

Se qualquer uma das alterações feitas em seus fluxos de trabalho for sinalizada como vulnerável, você poderá evitar adicioná-las ao seu projeto ou atualizá-las para uma versão segura.

Para obter mais informações sobre a revisão de dependência, confira [Análise de dependência](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependency-review).

O "ação de revisão de dependência" se refere à ação específica que pode relatar diferenças em um pull request dentro do contexto do GitHub Actions. Consulte [`dependency-review-action`](https://github.com/actions/dependency-review-action). É possível usar o ação de revisão de dependência no repositório para impor revisões de dependência em solicitações de pull. A ação examina versões vulneráveis de dependências introduzidas por alterações de versão do pacote em solicitações de pull e avisa você sobre as vulnerabilidades de segurança associadas. Isso oferece uma melhor visibilidade do que está mudando em uma solicitação de pull e ajuda a evitar que vulnerabilidades sejam adicionadas ao repositório. Para obter mais informações, consulte [Análise de dependência](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependency-review#about-the-dependency-review-action).

### Manter as ações em seus fluxos de trabalho seguras e atualizadas

Você pode usar Dependabot para garantir que as referências a ações e fluxos de trabalho reutilizáveis usados em seu repositório sejam mantidas atualizadas. Ações são frequentemente atualizadas com correções de bugs e novos recursos para tornar os processos automatizados mais rápidos, seguros e confiáveis.
Dependabot elimina o esforço de manter suas dependências, pois faz isso automaticamente para você. Para saber mais, confira [Manter as suas ações atualizadas com o Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/auto-update-actions) e [Atualizações de segurança do Dependabot](https://docs.github.com/pt/code-security/concepts/supply-chain-security/dependabot-security-updates).

Os recursos a seguir podem atualizar automaticamente as ações em seus fluxos de trabalho.

* **Dependabot version updates** abra solicitações de pull para atualizar as ações para a versão mais recente quando uma nova versão for lançada.
* **Dependabot security updates** abra solicitações de pull para atualizar ações com vulnerabilidades relatadas para a versão mínima corrigida.

!!! note
    * Dependabot suporta apenas atualizações de GitHub Actions usando a sintaxe de repositório GitHub, como `actions/checkout@v6` ou `actions/checkout@<commit>` .
      Dependabot ignorará ações ou fluxos de trabalho reutilizáveis referenciados localmente (por exemplo, `./.github/actions/foo.yml`).
    * Dependabot atualiza a documentação de versão de GitHub Actions quando o comentário está na mesma linha, como `actions/checkout@<commit> #<tag or link>` ou `actions/checkout@<tag> #<tag or link>`.
    * Se o commit que você usa não estiver associado a nenhuma tag, Dependabot atualizará a GitHub Actions para o commit mais recente (que pode ser diferente da release mais recente).
    * Docker Hub e URLs GitHub PackagesContainer registry não têm suporte no momento. Por exemplo, não há suporte para referências a ações de contêiner do Docker usando a sintaxe `docker://`.
    * Dependabot dá suporte a repositórios públicos e privados para GitHub Actions. Para opções de configuração de registro privado, consulte `git` em [Configurando o acesso a registros privados para Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-access-to-private-registries#git).

Para obter informações sobre como configurar Dependabot version updates, consulte [Configuração de atualizações de versão do Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-version-updates).

Para obter informações sobre como configurar Dependabot security updates, consulte [Configuração de atualizações de segurança do Dependabot](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates).

### Proteger ações que você criou

GitHub permite a colaboração entre pessoas que publicam e mantêm ações e repórteres de vulnerabilidade para promover a codificação segura. Os avisos de segurança do repositório permitem que os mantenedores dos repositórios públicos discutam e corrijam de modo privado as vulnerabilidades de segurança em um projeto. Depois de colaborar em uma correção, os responsáveis pelo repositório podem publicar o aviso de segurança para divulgar publicamente a vulnerabilidade de segurança na comunidade do projeto. Ao publicar avisos de segurança, os responsáveis pelo repositório facilitam para a comunidade a atualização das dependências do pacote e a pesquisa sobre o impacto das vulnerabilidades de segurança.

Se você for alguém que mantém uma ação usada em outros projetos, poderá usar os seguintes GitHub recursos para aprimorar a segurança das ações publicadas.

* Use o modo de exibição de dependentes no grafo de dependência para ver quais projetos dependem do seu código. Se você receber um relatório de vulnerabilidade, ele dará uma ideia de com quem você precisa se comunicar sobre a vulnerabilidade e como corrigi-la. Para saber mais, confira [Explorar as dependências de um repositório](https://docs.github.com/pt/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/explore-dependencies#dependents-view).
* Use os avisos de segurança do repositório para criar um aviso de segurança, colabore de forma privada para corrigir a vulnerabilidade em um fork privado temporário e publique um aviso de segurança para alertar sua comunidade sobre a vulnerabilidade assim que um patch for lançado. Para saber mais, confira [Como configurar relatórios privados de vulnerabilidades em um repositório](https://docs.github.com/pt/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository) e [Criando uma consultoria de segurança do repositório](https://docs.github.com/pt/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/create-repository-advisory).
