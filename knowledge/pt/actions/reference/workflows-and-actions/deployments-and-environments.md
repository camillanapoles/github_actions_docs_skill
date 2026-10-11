---
title: Implantações e ambientes
description: Encontre informações sobre regras de proteção de implantação, segredos de ambiente e variáveis de ambiente.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/deployments-and-environments
captured: '2026-10-11'
section: GitHub Actions
---

# Implantações e ambientes

_Encontre informações sobre regras de proteção de implantação, segredos de ambiente e variáveis de ambiente._

## Regras de proteção de implantação

As normas de proteção de implantação exigem a aprovação de condições específicas antes que um trabalho que faz referência ao ambiente possa prosseguir. Você pode usar regras de proteção de implantação para exigir aprovação manual, atrasar uma tarefa ou restringir o ambiente a determinadas ramificações. Você também pode criar e aplicar regras de proteção personalizadas viabilizadas por GitHub Apps que usam sistemas de terceiros para controlar implantações referentes a ambientes configurados no GitHub.

Os sistemas de terceiros podem ser sistemas de observabilidade, sistemas de gerenciamento de alterações, sistemas de qualidade de código ou outras configurações manuais que você usa para avaliar a prontidão antes que as implantações sejam implementadas com segurança nos ambientes.

> \[!NOTE]
> Qualquer quantidade de regras de proteção de implantação baseadas no GitHub Apps pode ser instalada em um repositório. No entanto, no máximo seis regras de proteção de implantação podem ser habilitadas em qualquer ambiente ao mesmo tempo.

### Revisores necessários

Use os revisores necessários para exigir que uma pessoa ou equipe específica aprove os trabalhos do fluxo de trabalho que fazem referência ao ambiente. Você pode listar até seis usuários ou equipes como revisores. Os revisores devem ter, pelo menos, acesso de leitura ao repositório. Apenas um dos revisores precisam aprovar o trabalho para que prossiga.

Você também tem a opção de impedir auto-revisões para implantações em ambientes protegidos. Se você habilitar essa configuração, os usuários que iniciarem uma implantação não poderão aprovar o trabalho de implantação, mesmo que sejam revisores obrigatórios. Isso garante que as implantações em ambientes protegidos sejam sempre revisadas por mais de uma pessoa.

Para obter mais informações sobre como revisar trabalhos que referenciam um ambiente com revisores obrigatórios, confira [Revisar implantações](../../how-tos/deploy/configure-and-manage-deployments/review-deployments.md).

> \[!NOTE]
> Se você estiver em um plano GitHub Free, GitHub Pro ou GitHub Team, os revisores obrigatórios só estarão disponíveis para repositórios públicos.

### Temporizador de espera

Use o temporizador de espera para atrasar o trabalho por um período específico de tempo depois que o trabalho for inicialmente acionado. O tempo (em minutos) deve ser um número inteiro entre 1 e 43.200 (30 dias). O tempo de espera não será contabilizado no tempo de cobrança.

> \[!NOTE]
> Se você estiver em um GitHub Free, GitHub Proou GitHub Team plano, os temporizadores de espera só estarão disponíveis para repositórios públicos.

### Branches e tags de implantação

Use branches e tags de implantação para restringir quais branches e tags podem ser implantados no ambiente. Confira abaixo as opções de branches e tags de implantação para um ambiente:

* **Sem restrição**: nenhuma restrição sobre qual branch ou tag pode ser implementada no ambiente.

* **Somente ramificações protegidas:** Somente ramificações com regras de proteção de ramificação ativadas podem ser implantadas no ambiente. Se nenhuma regra de proteção de branch for definida para qualquer branch no repositório, todos os branches poderão implantar. Para obter mais informações sobre as regras de proteção do branch, consulte [Sobre branches protegidos](https://docs.github.com/pt/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

  > \[!NOTE]
  > As execuções de fluxo de trabalho de implantação disparadas por tags com o mesmo nome de uma branch protegida e forks com branches que correspondem ao nome da branch protegida não podem ser implantadas no ambiente.

* **Branches e tags selecionadas**: somente branches e tags que correspondem aos seus padrões de nomenclatura especificados podem ser implantados no ambiente.

  A regra de ramificação ou tag de implantação é comparada com a `GITHUB_REF` da execução do fluxo de trabalho. Para os valores de `GITHUB_REF` para cada gatilho de fluxo de trabalho, consulte [Eventos que disparam fluxos de trabalho](events-that-trigger-workflows.md). Se você especificar `releases/*` como uma regra de ramificação ou tag de implantação, somente uma `GITHUB_REF` cujo nome comece com `releases/` poderá ser implantada no ambiente. Adicionar outra regra de branch `refs/pull/*/merge` também permitiria que fluxos de trabalho disparados por eventos `pull_request` fossem implantados no ambiente. Caracteres curinga não corresponderão a `/` para corresponder a ramificações ou marcações que começam com `release/` e contêm uma barra simples adicional, use `release/*/*`. Para obter mais informações sobre opções de sintaxe para ramificações de implantação, consulte a [documentação do Ruby `File.fnmatch`](https://ruby-doc.org/core-2.5.1/File.html#method-c-fnmatch).

  > \[!NOTE]
  > Os padrões de nomes devem ser configurados individualmente para branches ou rótulos.

> \[!NOTE]
> As ramificações e tags de implantação estão disponíveis para todos os repositórios públicos. Para usuários nos planos GitHub Pro ou GitHub Team, ramificações de implantação e marcações também estão disponíveis para repositórios privados.

### Permitir que os administradores ignorem as regras de proteção configuradas

Por padrão, os administradores podem ignorar as regras de proteção e forçar implantações para ambientes específicos. Para saber mais, confira [Revisar implantações](../../how-tos/deploy/configure-and-manage-deployments/review-deployments.md#bypassing-deployment-protection-rules).

Como alternativa, você pode configurar ambientes para não permitir ignorar as regras de proteção para todas as implantações no ambiente.

> \[!NOTE]
> Permitir que os administradores ignorem as regras de proteção está disponível apenas para repositórios públicos para usuários dos planos GitHub Free, GitHub Pro e GitHub Team.

### Regras de proteção de implantação personalizadas

> \[!NOTE]
> Regras de proteção de implementação personalizada estão em prévia pública e estão sujeitas a alterações.

Você pode habilitar suas próprias regras de proteção personalizadas para bloquear implantações com serviços de terceiros. Por exemplo, você pode usar serviços como Datadog, Honeycomb e ServiceNow para fornecer aprovações automatizadas para implantações no GitHub. Para obter mais informações, consulte [Criar regras de proteção de implantação personalizadas](../../how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules.md).

Depois que as regras de proteção de implantação personalizadas forem criadas e instaladas em um repositório, você poderá habilitar a regra de proteção de implantação personalizada para qualquer ambiente no repositório. Para obter mais informações sobre como configurar e habilitar regras de proteção de implantação personalizadas, confira [Configurar regras de proteção de implantação personalizadas](../../how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules.md).

> \[!NOTE]
> As regras personalizadas de proteção de implantação estão disponíveis apenas para repositórios públicos para usuários dos planos GitHub Free, GitHub Pro e GitHub Team.

## Segredos do ambiente

Os segredos armazenados em um ambiente só estão disponíveis para trabalhos de fluxo de trabalho que fazem referência ao ambiente. Se o ambiente exigir aprovação, um trabalho não poderá acessar segredos de ambiente até que um dos revisores necessários o aprove. Para saber mais sobre segredos, confira [Segredos](../../concepts/security/secrets.md).

> \[!NOTE]
>
> * Os fluxos de trabalho executados em executores auto-hospedados não são executados em um contêiner isolado, mesmo que usem ambientes. Os segredos de ambiente devem ser tratados com o mesmo nível de segurança que os segredos do repositório e da organização. Para saber mais, confira [Referência de uso seguro](../security/secure-use.md#hardening-for-self-hosted-runners).
> * Se você estiver usando GitHub Free, os segredos do ambiente só estarão disponíveis em repositórios públicos. Para acessar segredos de ambiente em repositórios privados ou internos, você deve usar GitHub Pro, GitHub Teamou GitHub Enterprise. Para mais informações sobre como alterar seu plano, consulte [Atualizando o plano da sua conta](https://docs.github.com/pt/billing/how-tos/manage-plan-and-licenses/upgrade-plan).

## Variáveis de ambiente

As variáveis armazenadas em um ambiente só ficam disponíveis para trabalhos de fluxos de trabalho que fazem referência ao ambiente. Essas variáveis só podem ser acessadas usando o contexto [`vars`](contexts.md#vars-context). Para saber mais, confira [Armazenar informações em variáveis](../../how-tos/write-workflows/choose-what-workflows-do/use-variables.md).

> \[!NOTE]
> As variáveis de ambiente estão disponíveis para todos os repositórios públicos. Para usuários nos planos GitHub Pro ou GitHub Team, as variáveis de ambiente também estão disponíveis em repositórios privados.
