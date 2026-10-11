---
title: Documentação do GitHub Actions
description: Automatize, personalize e execute seus fluxos de trabalho de desenvolvimento de software diretamente em seu repositório com GitHub Actions. Você pode descobrir, criar e compartilhar ações para realizar qualquer trabalho que desejar, incluindo CI/CD, bem como combinar ações em um fluxo de trabalho co
product: GitHub Actions
documentType: product
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions
captured: '2026-10-11'
section: GitHub Actions
---

# Documentação do GitHub Actions

_Automatize, personalize e execute seus fluxos de trabalho de desenvolvimento de software diretamente em seu repositório com GitHub Actions. Você pode descobrir, criar e compartilhar ações para realizar qualquer trabalho que desejar, incluindo CI/CD, bem como combinar ações em um fluxo de trabalho completamente personalizado._

## Recommended

* [Guia Rápido do GitHub Actions](get-started/quickstart.md)

  Experimente os principais recursos em GitHub Actions minutos.

* [Noções básicas sobre GitHub Actions](get-started/understand-github-actions.md)

  Aprenda os conceitos fundamentais e a terminologia essencial em GitHub Actions.

* [Usar executores hospedados no GitHub](how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners.md)

  Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub.

* [Sintaxe de fluxo de trabalho para o GitHub Actions](reference/workflows-and-actions/workflow-syntax.md)

  Um fluxo de trabalho é um processo automatizado configurável constituído de um ou mais trabalhos. Você deve criar um arquivo YAML para definir a configuração do seu fluxo de trabalho.

* [Eventos que disparam fluxos de trabalho](reference/workflows-and-actions/events-that-trigger-workflows.md)

  Você pode configurar seus fluxos de trabalho para serem executados quando uma atividade GitHub específica ocorrer, em um horário agendado ou quando ocorrer um evento fora dele GitHub .

* [Usar atestados de artefatos para estabelecer a procedência de compilações](how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md)

  Os atestados de artefatos permitem que você aumente a segurança da cadeia de fornecedores de suas compilações, estabelecendo onde e como seu software foi criado.

* [Migrar para o GitHub Actions](tutorials/migrate-to-github-actions.md)

  Aprenda como fazer a migração dos seus fluxos de trabalho de CI/CD existentes para GitHub Actions.

* [Reutilizar fluxos de trabalho](how-tos/reuse-automations/reuse-workflows.md)

  Aprenda a evitar a duplicação ao criar um fluxo de trabalho reutilizando os fluxos de trabalho existentes.

* [Como ver as métricas do GitHub Actions](how-tos/administer/view-metrics.md)

  Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo.

## Links

### Getting started

* [Noções básicas sobre GitHub Actions](get-started/understand-github-actions.md)

  Aprenda os conceitos fundamentais e a terminologia essencial em GitHub Actions.

* [Guia Rápido do GitHub Actions](get-started/quickstart.md)

  Experimente os principais recursos em GitHub Actions minutos.

## Articles

* [Guia Rápido do GitHub Actions](get-started/quickstart.md)

  Experimente os principais recursos em GitHub Actions minutos.

* [Noções básicas sobre GitHub Actions](get-started/understand-github-actions.md)

  Aprenda os conceitos fundamentais e a terminologia essencial em GitHub Actions.

* [Integração contínua](get-started/continuous-integration.md)

  Você pode criar fluxos de trabalho personalizados de integração contínua (CI) diretamente no seu repositório GitHub com GitHub Actions.

* [Implantação contínua](get-started/continuous-deployment.md)

  Você pode criar fluxos de trabalho personalizados de CD (implantação contínua) diretamente no seu repositório GitHub com GitHub Actions.

* [GitHub Actions vs GitHub Apps](get-started/actions-vs-apps.md)

  Saiba mais sobre as principais diferenças entre o GitHub Actions e o GitHub Apps para ajudar você a decidir qual é o ideal para seus casos de uso.

* [Fluxos de trabalho](concepts/workflows-and-actions/workflows.md)

  Obtenha uma visão geral de alto nível dos fluxos de GitHub Actions trabalho, incluindo gatilhos, sintaxe e recursos avançados.

* [Variáveis](concepts/workflows-and-actions/variables.md)

  Saiba mais sobre variáveis em GitHub Actions fluxos de trabalho.

* [Contextos](concepts/workflows-and-actions/contexts.md)

  Saiba mais sobre contextos em GitHub Actions.

* [Expressões](concepts/workflows-and-actions/expressions.md)

  Você pode avaliar expressões em fluxos de trabalho e ações.

* [Reutilizando configurações de fluxo de trabalho](concepts/workflows-and-actions/reusing-workflow-configurations.md)

  Aprenda a evitar a duplicação ao criar um fluxo de trabalho.

* [Sobre ações personalizadas](concepts/workflows-and-actions/custom-actions.md)

  As ações são tarefas individuais que podem ser combinadas para criar trabalhos e personalizar seu fluxo de trabalho. Você pode criar suas próprias ações ou usar e personalizar ações compartilhadas pela GitHub comunidade.

* [Ambientes de implantação](concepts/workflows-and-actions/deployment-environments.md)

  Você pode criar e implementar em ambientes diferentes.

* [Concorrência](concepts/workflows-and-actions/concurrency.md)

  Saiba mais sobre como executar fluxos de trabalho e trabalhos ao mesmo tempo.

* [Artefatos do fluxo de trabalho](concepts/workflows-and-actions/workflow-artifacts.md)

  Saiba mais sobre como armazenar e compartilhar dados como artefatos de fluxos de GitHub Actions trabalho.

* [Cache de dependência](concepts/workflows-and-actions/dependency-caching.md)

  Saiba mais sobre o cache de dependência para velocidade e eficiência do fluxo de trabalho.

* [Notificações para execuções de fluxo de trabalho](concepts/workflows-and-actions/notifications-for-workflow-runs.md)

  Você pode se inscrever para receber notificações sobre as execuções do fluxo de trabalho que você iniciar.

* [Executores hospedados no GitHub](concepts/runners/github-hosted-runners.md)

  GitHub oferece máquinas virtuais hospedadas para executar fluxos de trabalho. A máquina virtual contém um ambiente de ferramentas, pacotes e configurações disponíveis para GitHub Actions usar.

* [Executores avançados](concepts/runners/larger-runners.md)

  Organize e governe seus fluxos de trabalho com executores maiores hospedados em GitHub usando grupos de executores, políticas de concorrência e controles de acesso granulares.

* [Executores auto-hospedados](concepts/runners/self-hosted-runners.md)

  Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus fluxos de trabalho GitHub Actions.

* [Rede privada com executores hospedados pelo GitHub](concepts/runners/private-networking.md)

  Você pode conectar executores hospedados no GitHub a recursos em uma rede privada, incluindo registros de pacotes, gerentes secretos e outros serviços locais.

* [Grupos de runners](concepts/runners/runner-groups.md)

  Use grupos de executores para controlar o acesso aos executores e organizar os executores em toda a sua organização ou empresa.

* [Conjuntos de dimensionamento de executor](concepts/runners/runner-scale-sets.md)

  Saiba mais sobre o que é um runner scale set e como ele pode interagir com o Actions Runner Controller.

* [Controlador de Ações Runner](concepts/runners/actions-runner-controller.md)

  Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus GitHub Actions fluxos de trabalho.

* [Suporte para o Controlador do Executor de Ações](concepts/runners/support-for-arc.md)

  O que você precisa saber antes de entrar em contato Suporte do GitHub para obter ajuda com o Actions Runner Controller.

* [Segredos](concepts/security/secrets.md)

  Saiba mais sobre segredos e como são usados em fluxos de trabalho GitHub Actions.

* [GITHUB\_TOKEN](concepts/security/github_token.md)

  Saiba o que `GITHUB_TOKEN` é, como funciona e por que ele é importante para a automação segura em GitHub Actions fluxos de trabalho.

* [OpenID Connect](concepts/security/openid-connect.md)

  O OpenID Connect permite que seus fluxos de trabalho troquem tokens de curta duração diretamente do seu provedor da nuvem.

* [Atestados de artefatos](concepts/security/artifact-attestations.md)

  Entenda os benefícios de uso e segurança dos atestados de artefato.

* [Injeções de script](concepts/security/script-injections.md)

  Entenda os riscos de segurança associados a injeções de script e GitHub Actions fluxos de trabalho.

* [Executores comprometidos](concepts/security/compromised-runners.md)

  Entenda os riscos de segurança associados a runners comprometidosGitHub Actions.

* [Controlador de admissão do Kubernetes](concepts/security/kubernetes-admissions-controller.md)

  Saiba como você pode usar um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes.

* [Sobre as métricas do GitHub Actions](concepts/metrics.md)

  Saiba mais sobre as GitHub Actions métricas disponíveis para suas organizações e repositórios.

* [Cobrança e uso](concepts/billing-and-usage.md)

  Há limites de uso para GitHub Actions fluxos de trabalho. As taxas de uso são aplicadas a repositórios que excedem a quantidade de minutos gratuitos e armazenamento disponíveis gratuitamente.

* [Sobre as políticas do Actions](concepts/about-actions-policies.md)

  Governe como GitHub Actions os fluxos de trabalho são executados em seu repositório, organização ou empresa.

* [Usando modelos de fluxo de trabalho](how-tos/write-workflows/use-workflow-templates.md)

  GitHub fornece modelos de fluxo de trabalho para uma variedade de linguagens e ferramentas.

* [Acionando um fluxo de trabalho](how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow.md)

  Como disparar GitHub Actions fluxos de trabalho automaticamente

* [Usando condições para controlar a execução do trabalho](how-tos/write-workflows/choose-when-workflows-run/control-jobs-with-conditions.md)

  Impeça que um trabalho seja executado a menos que suas condições sejam atendidas.

* [Controlar a simultaneidade de fluxos de trabalho e tarefas](how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency.md)

  Gerencie os fluxos de trabalho e os trabalhos que podem ser executados juntos.

* [Escolhendo o executor para um trabalho](how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job.md)

  Defina o tipo de máquina que processará um trabalho no seu fluxo de trabalho.

* [Executar trabalhos em um contêiner](how-tos/write-workflows/choose-where-workflows-run/run-jobs-in-a-container.md)

  Use um contêiner para executar as etapas de um trabalho.

* [Usando tarefas em um fluxo de trabalho](how-tos/write-workflows/choose-what-workflows-do/use-jobs.md)

  Use fluxos de trabalho para executar vários trabalhos.

* [Usando blocos de construção pré-gravados no seu fluxo de trabalho](how-tos/write-workflows/choose-what-workflows-do/find-and-customize-actions.md)

  Você pode usar e personalizar ações escritas previamente para alimentar o fluxo de trabalho.

* [Usando GitHub CLI em fluxos de trabalho](how-tos/write-workflows/choose-what-workflows-do/use-github-cli.md)

  Você pode fazer o script com GitHub CLI em fluxos de trabalho GitHub Actions.

* [Adicionar scripts ao seu fluxo de trabalho](how-tos/write-workflows/choose-what-workflows-do/add-scripts.md)

  Você pode usar GitHub Actions fluxos de trabalho para executar scripts.

* [Usar segredos em ações do GitHub](how-tos/write-workflows/choose-what-workflows-do/use-secrets.md)

  Aprenda a criar segredos nos níveis de repositório, ambiente e organização para fluxos de trabalho GitHub Actions.

* [Armazenar informações em variáveis](how-tos/write-workflows/choose-what-workflows-do/use-variables.md)

  GitHub define variáveis padrão para cada GitHub Actions execução de fluxo de trabalho. Você também pode definir variáveis personalizadas para uso em um ou vários fluxos de trabalho.

* [Passando informações entre tarefas](how-tos/write-workflows/choose-what-workflows-do/pass-job-outputs.md)

  Você pode definir saídas para passar informações de um trabalho para outro.

* [Definindo um shell padrão e diretório de trabalho](how-tos/write-workflows/choose-what-workflows-do/set-default-values-for-jobs.md)

  Defina as configurações padrão que serão aplicadas a todos os trabalhos no fluxo de trabalho ou todas as etapas de um trabalho.

* [Implantação em um ambiente específico](how-tos/write-workflows/choose-what-workflows-do/deploy-to-environment.md)

  Especifique um ambiente de implantação em seu fluxo de trabalho.

* [Executando variações de tarefas em um workflow](how-tos/write-workflows/choose-what-workflows-do/run-job-variations.md)

  Crie uma matriz para definir as variações de cada trabalho.

* [Reutilizar fluxos de trabalho](how-tos/reuse-automations/reuse-workflows.md)

  Aprenda a evitar a duplicação ao criar um fluxo de trabalho reutilizando os fluxos de trabalho existentes.

* [Criar modelos de fluxo de trabalho para sua organização](how-tos/reuse-automations/create-workflow-templates.md)

  Saiba como você pode criar modelos de fluxo de trabalho para ajudar as pessoas de sua equipe a adicionar novos fluxos de trabalho com mais facilidade.

* [Compartilhamento de ações e fluxos de trabalho de seu repositório privado](how-tos/reuse-automations/share-across-private-repositories.md)

  É possível compartilhar uma ação ou um fluxo de trabalho reutilizável sem publicá-lo publicamente.

* [Compartilhamento de ações e fluxos de trabalho com sua organização](how-tos/reuse-automations/share-with-your-organization.md)

  É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua organização sem publicá-lo publicamente.

* [Compartilhando ações e fluxos de trabalho com sua empresa](https://docs.github.com/pt/share-with-your-enterprise)

  É possível compartilhar uma ação ou um fluxo de trabalho reutilizável com sua empresa sem publicar a ação ou fluxo de trabalho publicamente.

* [Usar atestados de artefatos para estabelecer a procedência de compilações](how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md)

  Os atestados de artefatos permitem que você aumente a segurança da cadeia de fornecedores de suas compilações, estabelecendo onde e como seu software foi criado.

* [Usando atestados de artefatos e fluxos de trabalho reutilizáveis para alcançar o SLSA v1 Build Level 3](how-tos/secure-your-work/use-artifact-attestations/increase-security-rating.md)

  A criação de software com fluxos de trabalho reutilizáveis e atestados de artefatos pode simplificar a segurança da sua cadeia de fornecedores e ajudar você a alcançar o SLSA v1.0 Build Level 3.

* [Impondo atestados de artefatos com um controlador de admissão do Kubernetes](how-tos/secure-your-work/use-artifact-attestations/enforce-artifact-attestations.md)

  Use um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes.

* [Verificação de atestados offline](how-tos/secure-your-work/use-artifact-attestations/verify-attestations-offline.md)

  Os atestados de artefato podem ser verificados sem uma conexão de Internet.

* [Como gerenciar o ciclo de vida dos atestados de artefato](how-tos/secure-your-work/use-artifact-attestations/manage-attestations.md)

  Pesquise e exclua atestados de que você não precisa mais.

* [Configurando o OpenID Connect no Amazon Web Services](how-tos/secure-your-work/security-harden-deployments/oidc-in-aws.md)

  Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com Amazon Web Services.

* [Configurando o OpenID Connect no Azure](how-tos/secure-your-work/security-harden-deployments/oidc-in-azure.md)

  Use o OpenID Connect em seus fluxos de trabalho para autenticar com Azure.

* [Configurando OpenID Connect na Google Cloud Platform](how-tos/secure-your-work/security-harden-deployments/oidc-in-google-cloud-platform.md)

  Use OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com a Google Cloud Platform.

* [Configurando o OpenID Connect no HashiCorp Vault](how-tos/secure-your-work/security-harden-deployments/oidc-in-hashicorp-vault.md)

  Use o OpenID Connect nos seus fluxos de trabalho para efetuar a autenticação com o HashiCorp Vault.

* [Configurando o OpenID Connect no JFrog](how-tos/secure-your-work/security-harden-deployments/oidc-in-jfrog.md)

  Use o OpenID Connect em seus fluxos de trabalho para se autenticar no JFrog.

* [Configurando o OpenID Connect no Octopus Deploy](how-tos/secure-your-work/security-harden-deployments/oidc-in-octopus-deploy.md)

  Use OpenID Connect em seus fluxos de trabalho para autenticar com o Octopus Deploy.

* [Configurando o OpenID Connect no PyPI](how-tos/secure-your-work/security-harden-deployments/oidc-in-pypi.md)

  Use o OpenID Connect em seus fluxos de trabalho para se autenticar no PyPI.

* [Configurando OpenID Connect em provedores da nuvem](how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers.md)

  Use o OpenID Connect dentro de seus fluxos de trabalho para efetuar a autenticação com provedores de nuvem.

* [Usando o OpenID Connect com fluxos de trabalho reutilizáveis](how-tos/secure-your-work/security-harden-deployments/oidc-with-reusable-workflows.md)

  Você pode usar fluxos de trabalho reutilizáveis com o OIDC para padronizar e melhorar as suas etapas de implantação.

* [Implantando com GitHub Actions](how-tos/deploy/configure-and-manage-deployments/control-deployments.md)

  GitHub Actions fornece controle detalhado sobre implantações com ambientes, grupos de concorrência e regras de proteção.

* [Exibir o histórico de implantações](how-tos/deploy/configure-and-manage-deployments/view-deployment-history.md)

  Veja as implantações atuais e anteriores para o seu repositório.

* [Gerenciar ambientes para implantação](how-tos/deploy/configure-and-manage-deployments/manage-environments.md)

  Você pode criar ambientes e proteger esses ambientes com regras de proteção de implantação. Um trabalho que faz referência a um ambiente deve seguir quaisquer regras de proteção para o ambiente antes de executar ou acessar os segredos do ambiente.

* [Revisar implantações](how-tos/deploy/configure-and-manage-deployments/review-deployments.md)

  Você pode aprovar ou rejeitar trabalhos que estão aguardando revisão.

* [Criar regras de proteção de implantação personalizadas](how-tos/deploy/configure-and-manage-deployments/create-custom-protection-rules.md)

  Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros.

* [Configurar regras de proteção de implantação personalizadas](how-tos/deploy/configure-and-manage-deployments/configure-custom-protection-rules.md)

  Use GitHub Apps para automatizar a proteção de implantações com sistemas de terceiros.

* [Implantando Node.js em Azure App Service](how-tos/deploy/deploy-to-third-party-platforms/nodejs-to-azure-app-service.md)

  Saiba como implantar um projeto de Node.js para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Implantando Python em Azure App Service](how-tos/deploy/deploy-to-third-party-platforms/python-to-azure-app-service.md)

  Saiba como implantar um projeto Python para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Implantando Java em Azure App Service](how-tos/deploy/deploy-to-third-party-platforms/java-to-azure-app-service.md)

  Saiba como implantar um projeto Java para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Implantando .NET em Azure App Service](how-tos/deploy/deploy-to-third-party-platforms/net-to-azure-app-service.md)

  Saiba como implantar um projeto de .NET para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Implantando o PHP em Azure App Service](how-tos/deploy/deploy-to-third-party-platforms/php-to-azure-app-service.md)

  Saiba como implantar um projeto PHP para Azure App Service como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Implantando o Docker no Serviço de Aplicativo do Azure](how-tos/deploy/deploy-to-third-party-platforms/docker-to-azure-app-service.md)

  Saiba como implantar um contêiner do Docker para Serviço de Aplicativo do Azure como parte de seus fluxos de trabalho de CD (implantação contínua).

* [Fazendo a implantação nos Aplicativos Web Estáticos do Azure](how-tos/deploy/deploy-to-third-party-platforms/azure-static-web-app.md)

  Saiba como implantar um aplicativo web no Azure Static Web App como parte de seus fluxos de trabalho de implantação contínua (CD).

* [Implantando no Azure Kubernetes Service](how-tos/deploy/deploy-to-third-party-platforms/azure-kubernetes-service.md)

  Saiba como implantar um projeto no serviço Azure Kubernetes (AKS) como parte de um fluxo de trabalho de implantação contínua (CD).

* [Implantar no Amazon Elastic Container Service](how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service.md)

  Saiba como implantar um projeto no Amazon Elastic Container Service (ECS) como parte de um fluxo de trabalho de CD (implantação contínua).

* [Implantar no Google Kubernetes Engine](how-tos/deploy/deploy-to-third-party-platforms/google-kubernetes-engine.md)

  Saiba como implantar um projeto no Google Kubernetes Engine (GKE) como parte de um fluxo de trabalho de CD (implantação contínua).

* [Instalar um certificado da Apple em executores do macOS para desenvolvimento do Xcode](how-tos/deploy/deploy-to-third-party-platforms/sign-xcode-applications.md)

  Saiba como assinar apps do Xcode em um fluxo de trabalho de integração contínua (CI) instalando um certificado de assinatura de código da Apple nos executores GitHub Actions.

* [Como gerenciar ações personalizadas](how-tos/create-and-publish-actions/manage-custom-actions.md)

  Saiba como criar e gerenciar suas próprias ações e personalizar ações compartilhadas pela GitHub comunidade.

* [Criar uma ação da CLI de terceiros](how-tos/create-and-publish-actions/create-a-cli-action.md)

  Saiba como desenvolver uma ação para configurar uma CLI nos executores GitHub Actions.

* [Definindo códigos de saída para ações](how-tos/create-and-publish-actions/set-exit-codes.md)

  Você pode usar códigos de saída para definir o status de uma ação.
  GitHub exibe status para indicar ações bem-sucedidas ou com falha.

* [Publicar ações no GitHub Marketplace](how-tos/create-and-publish-actions/publish-in-github-marketplace.md)

  Você pode publicar ações em GitHub Marketplace e compartilhar as ações que você criou com a comunidade GitHub.

* [Aprovando e mantendo ações](how-tos/create-and-publish-actions/release-and-maintain-actions.md)

  Você pode aproveitar a automação e as melhores práticas de código aberto para liberar e manter ações automatizadas.

* [Como usar versões e marcas imutáveis para gerenciar as versões da sua ação](how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases.md)

  Saiba como você pode usar uma combinação de lançamentos imutáveis no GitHub e tags Git para gerenciar os lançamentos da sua ação.

* [Executar um fluxo de trabalho manualmente](how-tos/manage-workflow-runs/manually-run-a-workflow.md)

  Quando um fluxo de trabalho é configurado para ser executado no `workflow_dispatch` evento, você pode executar o fluxo de trabalho usando a guia GitHubGitHub CLIAções, ou a API REST.

* [Reexecutando fluxos de trabalho e tarefas](how-tos/manage-workflow-runs/re-run-workflows-and-jobs.md)

  Você pode executar novamente um fluxo de trabalho, todos os trabalhos que falharam na execução de um fluxo de trabalho, ou trabalhos específicos em uma execução de fluxo de trabalho até 30 dias após sua execução inicial.

* [Cancelar a execução do fluxo de trabalho](how-tos/manage-workflow-runs/cancel-a-workflow-run.md)

  Você pode cancelar uma execução de fluxo de trabalho que está em andamento, incluindo todas as tarefas e etapas.

* [Desabilitar e habilitar um fluxo de trabalho](how-tos/manage-workflow-runs/disable-and-enable-workflows.md)

  Você pode desabilitar e habilitar novamente um fluxo de trabalho usando a interface do usuário de GitHub, a API REST, ou GitHub CLI.

* [Ignorar execuções de fluxo de trabalho](how-tos/manage-workflow-runs/skip-workflow-runs.md)

  Você pode ignorar as execuções de fluxo de trabalho disparadas pelos eventos `push` e `pull_request` incluindo um comando na mensagem de commit.

* [Excluir a execução de um fluxo de trabalho](how-tos/manage-workflow-runs/delete-a-workflow-run.md)

  Você pode excluir uma execução do fluxo de trabalho que foi concluída ou que tem mais de duas semanas.

* [Baixar artefatos do fluxo de trabalho](how-tos/manage-workflow-runs/download-workflow-artifacts.md)

  Você pode fazer o download de artefatos arquivados antes que expirem automaticamente.

* [Remover artefatos de fluxo de trabalho](how-tos/manage-workflow-runs/remove-workflow-artifacts.md)

  Você pode recuperar o armazenamento usado GitHub Actions excluindo artefatos antes que eles expirem GitHub.

* [Gerenciando caches](how-tos/manage-workflow-runs/manage-caches.md)

  Você pode monitorar, filtrar e excluir caches de dependência criados com base em seus fluxos de trabalho.

* [Aprovando execuções de fluxo de trabalho de forks](how-tos/manage-workflow-runs/approve-runs-from-forks.md)

  Você pode aprovar manualmente as execuções de fluxo de trabalho disparadas pela solicitação de pull de um colaborador.

* [Usar executores hospedados no GitHub](how-tos/manage-runners/github-hosted-runners/use-github-hosted-runners.md)

  Você pode atribuir um trabalho para ser executado em uma máquina virtual hospedada por GitHub.

* [Personalizando executores hospedados no GitHub](how-tos/manage-runners/github-hosted-runners/customize-runners.md)

  Você pode instalar software adicional em executores hospedados em GitHub como parte do fluxo de trabalho.

* [Visualizando suas tarefas atuais](how-tos/manage-runners/github-hosted-runners/view-current-jobs.md)

  Monitore como GitHubos executores hospedados estão processando trabalhos em sua organização ou empresa e identifique quaisquer restrições relacionadas.

* [Usando um gateway de API com o OIDC](how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-oidc.md)

  Você pode usar tokens OpenID Connect (OIDC) para autenticar seu fluxo de trabalho.

* [Usar o WireGuard para criar uma sobreposição de rede](how-tos/manage-runners/github-hosted-runners/connect-to-a-private-network/connect-with-wireguard.md)

  Você pode criar uma rede de sobreposição entre seu executor e um serviço em sua rede privada.

* [Adicionar executores auto-hospedados](how-tos/manage-runners/self-hosted-runners/add-runners.md)

  Você pode adicionar um runner autogerenciado a um repositório, a uma organização ou a uma empresa.

* [Como executar scripts antes ou depois de um trabalho](how-tos/manage-runners/self-hosted-runners/run-scripts.md)

  Os scripts podem ser executado automaticamente em um executor autohospedado, diretamente antes ou depois de um trabalho.

* [Como personalizar os contêineres usados por trabalhos](how-tos/manage-runners/self-hosted-runners/customize-containers.md)

  Você pode personalizar como o executor auto-hospedado invoca um contêiner para um trabalho.

* [Configurar o aplicativo do executor auto-hospedado como um serviço](how-tos/manage-runners/self-hosted-runners/configure-the-application.md)

  Você pode configurar o aplicativo do executor auto-hospedado como um serviço para que inicie o aplicativo do executor automaticamente quando a máquina for iniciada.

* [Usar rótulos com os executores auto-hospedados](how-tos/manage-runners/self-hosted-runners/apply-labels.md)

  Você pode usar etiquetas para organizar os seus executores auto-hospedados com base em suas características.

* [Usar os executores auto-hospedados em um fluxo de trabalho](how-tos/manage-runners/self-hosted-runners/use-in-a-workflow.md)

  Para usar executores auto-hospedados em um fluxo de trabalho, você pode usar rótulos ou grupos para especificar o executor para uma tarefa.

* [Gerenciar o acesso a executores auto-hospedados usando grupos](how-tos/manage-runners/self-hosted-runners/manage-access.md)

  Você pode usar políticas para limitar o acesso a runners auto-hospedados que foram adicionados a uma conta corporativa.

* [Monitorar e solucionar problemas de executores auto-hospedados](how-tos/manage-runners/self-hosted-runners/monitor-and-troubleshoot.md)

  Você pode monitorar seus executores auto-hospedados para visualizar sua atividade e diagnosticar problemas comuns.

* [Remover executores auto-hospedados](how-tos/manage-runners/self-hosted-runners/remove-runners.md)

  Você pode remover permanentemente um executor auto-hospedado de um repositório.

* [Gerenciar executores maiores](how-tos/manage-runners/larger-runners/manage-larger-runners.md)

  Você pode configurar executor avançados para sua organização ou empresa.

* [Como controlar o acesso a executores maiores](how-tos/manage-runners/larger-runners/control-access.md)

  Você pode usar políticas para limitar o acesso a executor avançados que foram adicionados a uma organização ou empresa.

* [Como executar trabalhos em executores maiores](how-tos/manage-runners/larger-runners/use-larger-runners.md)

  Identifique os executor avançados disponíveis e, em seguida, direcione os trabalhos para os executores corretos usando grupos de executores e rótulos de fluxo de trabalho.

* [Usando imagens personalizadas](how-tos/manage-runners/larger-runners/use-custom-images.md)

  Crie, gerencie e use imagens personalizadas para Executores maiores hospedados no GitHub sua organização ou empresa.

* [Autenticando o ARC na API de GitHub](how-tos/manage-runners/use-actions-runner-controller/authenticate-to-the-api.md)

  Autenticar Actions Runner Controller na API GitHub.

* [Como implantar conjuntos de dimensionamento de executores com o Actions Runner Controller](how-tos/manage-runners/use-actions-runner-controller/deploy-runner-scale-sets.md)

  Implante conjuntos de escalonadores com Actions Runner Controller, e use opções avançadas de configuração para adaptar Actions Runner Controller às suas necessidades.

* [Usar executores do Controlador do Executor de Ações em um fluxo de trabalho](how-tos/manage-runners/use-actions-runner-controller/use-arc-in-a-workflow.md)

  Usar executores Actions Runner Controller em um arquivo de fluxo de trabalho.

* [Utilizando servidores proxy com um executor](how-tos/manage-runners/use-proxy-servers.md)

  Você pode configurar executores em ambientes isolados para usar um servidor proxy para comunicação segura com GitHub.

* [Usar o gráfico de visualização](how-tos/monitor-workflows/use-the-visualization-graph.md)

  Cada execução de fluxo de trabalho gera um gráfico em tempo real que ilustra o progresso da execução. Você pode usar este gráfico para monitorar e depurar fluxos de trabalho.

* [Visualizar o histórico de execução do fluxo de trabalho](how-tos/monitor-workflows/view-workflow-run-history.md)

  Você pode visualizar registros para cada execução de um fluxo de trabalho. Os registros incluem a situação de cada trabalho e a etapa de um fluxo de trabalho.

* [Visualizar o tempo de execução do trabalho](how-tos/monitor-workflows/view-job-execution-time.md)

  Você pode visualizar o tempo de execução de um trabalho, incluindo os minutos faturáveis que um trabalho acumulou.

* [Adicionar um selo de status de fluxo de trabalho](how-tos/monitor-workflows/add-a-status-badge.md)

  Você pode exibir um selo de status no seu repositório para indicar o status dos seus fluxos de trabalho.

* [Usando registros de execução de fluxo de trabalho](how-tos/monitor-workflows/use-workflow-run-logs.md)

  Você pode visualizar, pesquisar e fazer download dos logs para cada trabalho em uma execução de fluxo de trabalho.

* [Exibindo logs de expressão de condição de tarefa](how-tos/monitor-workflows/view-job-condition-logs.md)

  Aprenda como acessar e interpretar os logs de avaliação de expressões para condições de nível de tarefa `if` em GitHub Actions.

* [Habilitando o log de depuração](how-tos/monitor-workflows/enable-debug-logging.md)

  Se os logs do fluxo de trabalho não fornecerem detalhes suficientes para diagnosticar o motivo pelo qual um fluxo de trabalho, um trabalho ou uma etapa não está funcionando como esperado, habilite o log de depuração adicional.

* [Solução de problemas de fluxos de trabalho](how-tos/troubleshoot-workflows.md)

  Você pode usar as ferramentas GitHub Actions para depurar seus fluxos de trabalho.

* [Controlando quem pode executar GitHub Actions fluxos de trabalho](how-tos/administer/control-workflow-execution.md)

  Controle quem pode disparar fluxos de trabalho GitHub Actions e quais eventos podem executá-los em toda a empresa, organização e repositório.

* [Como ver as métricas do GitHub Actions](how-tos/administer/view-metrics.md)

  Você pode visualizar métricas para monitorar onde sua organização ou repositórios usam GitHub Actions e como elas estão se saindo.

* [Como disponibilizar namespaces desativados no GHE.com](https://docs.github.com/pt/reuse-namespaces-on-ghecom)

  Permita que as pessoas usem namespaces que correspondam às ações que você usou no GitHub.com.

* [Obtendo ajuda do suporte GitHub sobre GitHub Actions](how-tos/get-support.md)

  Saiba como Suporte do GitHub ajudar com GitHub Actions

* [Sintaxe de fluxo de trabalho para o GitHub Actions](reference/workflows-and-actions/workflow-syntax.md)

  Um fluxo de trabalho é um processo automatizado configurável constituído de um ou mais trabalhos. Você deve criar um arquivo YAML para definir a configuração do seu fluxo de trabalho.

* [Eventos que disparam fluxos de trabalho](reference/workflows-and-actions/events-that-trigger-workflows.md)

  Você pode configurar seus fluxos de trabalho para serem executados quando uma atividade GitHub específica ocorrer, em um horário agendado ou quando ocorrer um evento fora dele GitHub .

* [Comandos de fluxo de trabalho para o GitHub Actions](reference/workflows-and-actions/workflow-commands.md)

  Você pode usar comandos do fluxo de trabalho ao executar comandos do shell em um fluxo de trabalho ou no código de uma ação.

* [Referência de variáveis](reference/workflows-and-actions/variables.md)

  Encontre informações para variáveis com suporte, convenções de nomenclatura, limites e contextos em GitHub Actions fluxos de trabalho.

* [Avaliar expressões em fluxos de trabalho e ações](reference/workflows-and-actions/expressions.md)

  Encontre informações sobre expressões em GitHub Actions.

* [Referência de contextos](reference/workflows-and-actions/contexts.md)

  Encontre informações sobre contextos disponíveis em GitHub Actions fluxos de trabalho, incluindo propriedades disponíveis, métodos de acesso e exemplos de uso.

* [Implantações e ambientes](reference/workflows-and-actions/deployments-and-environments.md)

  Encontre informações sobre regras de proteção de implantação, segredos de ambiente e variáveis de ambiente.

* [Referência do cache de dependência](reference/workflows-and-actions/dependency-caching.md)

  Encontre informações sobre a funcionalidade do cache de dependência em fluxos de trabalho.

* [Reutilizando configurações de fluxo de trabalho](reference/workflows-and-actions/reusing-workflow-configurations.md)

  Encontre informações sobre como evitar a duplicação ao criar um fluxo de trabalho reutilizando fluxos de trabalho existentes YAML.

* [Referência de sintaxe de metadados](reference/workflows-and-actions/metadata-syntax.md)

  É possível criar ações para realizar tarefas no repositório. Se você estiver fazendo uma ação personalizada, ela exigirá um arquivo de metadados que use a sintaxe YAML.

* [Referência de cancelamento de fluxo de trabalho](reference/workflows-and-actions/workflow-cancellation.md)

  Encontre informações sobre as etapas que GitHub executa para cancelar uma execução de um fluxo de trabalho.

* [Suporte do Dockerfile para GitHub Actions](reference/workflows-and-actions/dockerfile-support.md)

  Ao criar um `Dockerfile` para uma ação do contêiner Docker, você deverá ter em mente como algumas instruções do Docker interagem com o GitHub Actions e com um arquivo de metadados da ação.

* [Referência de executores hospedados pelo GitHub](reference/runners/github-hosted-runners.md)

  Encontre informações sobre executores hospedados em GitHub, incluindo suas especificações e opções de personalização.

* [Referência de executores avançados](reference/runners/larger-runners.md)

  Encontre informações sobre corredores maiores, incluindo suas especificações e opções de personalização.

* [Referência de executores auto-hospedados](reference/runners/self-hosted-runners.md)

  Encontre informações sobre como configurar e usar executores auto-hospedados.

* [Referência de uso seguro](reference/security/secure-use.md)

  Práticas de segurança para escrever fluxos de trabalho e usar GitHub Actions recursos.

* [Uso seguro de pull\_request\_target](reference/security/securely-using-pull_request_target.md)

  Saiba mais sobre os riscos de segurança do `pull_request_target` evento.

* [Referência de segredos](reference/security/secrets.md)

  Encontre informações técnicas sobre segredos em GitHub Actions.

* [Referência do OpenID Connect](reference/security/oidc.md)

  Encontre informações sobre como usar o OpenID Connect (OIDC) para autenticar GitHub Actions fluxos de trabalho com provedores de nuvem.

* [Limites do Actions](reference/limits.md)

  Há limites no GitHub Actions que você pode atingir à medida que escala seu uso; alguns deles podem aumentar ao entrar em contato com o suporte.

* [Argumentos e configurações complementares](reference/github-actions-importer/supplemental-arguments-and-settings.md)

  GitHub Actions Importer tem vários argumentos e configurações complementares para adaptar o processo de migração às suas necessidades.

* [Estendendo o Importador do GitHub Actions com transformadores personalizados](reference/github-actions-importer/custom-transformers.md)

  GitHub Actions Importer oferece a capacidade de estender seu mapeamento interno.

* [Criando um exemplo de fluxo de trabalho](tutorials/create-an-example-workflow.md)

  Neste tutorial, você aprenderá a criar um fluxo de trabalho básico disparado por um evento push.

* [Como criar e testar projetos com o Go](tutorials/build-and-test-code/go.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Go.

* [Construir e testar Java com Ant](tutorials/build-and-test-code/java-with-ant.md)

  Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Ant.

* [Compilar e testar Java com o Gradle](tutorials/build-and-test-code/java-with-gradle.md)

  Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Gradle.

* [Compilar e testar Java com o Maven](tutorials/build-and-test-code/java-with-maven.md)

  Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu projeto de Java com o Maven.

* [Criar e testar .NET](tutorials/build-and-test-code/net.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto .NET.

* [Criar e testar Node.js](tutorials/build-and-test-code/nodejs.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto Node.js.

* [Criar e testar PowerShell](tutorials/build-and-test-code/powershell.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do PowerShell.

* [Compilar e testar Python](tutorials/build-and-test-code/python.md)

  Saiba como criar um fluxo de trabalho de CI (integração contínua) para criar e testar seu projeto de Python.

* [Criar e testar o Ruby](tutorials/build-and-test-code/ruby.md)

  É possível criar um fluxo de trabalho de integração contínua (CI) para criar e testar o seu projeto do Ruby.

* [Como criar e testar o Rust](tutorials/build-and-test-code/rust.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto do Rust.

* [Construção e teste Swift](tutorials/build-and-test-code/swift.md)

  Saiba como criar um fluxo de trabalho de integração contínua (CI) para criar e testar seu projeto Swift.

* [Compilar e testar aplicativos Xamarin](tutorials/build-and-test-code/xamarin-apps.md)

  Saiba como criar um fluxo de trabalho de CI (integração contínua) em GitHub Actions para criar e testar seu aplicativo Xamarin.

* [Usar GITHUB\_TOKEN para autenticação em fluxos de trabalho](tutorials/authenticate-with-github_token.md)

  Saiba como usar a autenticação `GITHUB_TOKEN` em nome de GitHub Actions.

* [Migrando de executores auto-hospedados para executores hospedados no GitHub](tutorials/migrate-to-github-runners.md)

  Saiba como avaliar sua infraestrutura atual de CI e migrar fluxos de trabalho de executores auto-hospedados para executores GitHubhospedados.

* [Criando uma ação de JavaScript](tutorials/create-actions/create-a-javascript-action.md)

  Neste tutorial, você aprenderá como criar uma ação JavaScript usando o conjunto de ferramentas de ações.

* [Criar uma ação composta](tutorials/create-actions/create-a-composite-action.md)

  Neste tutorial, você aprenderá a criar uma ação composta.

* [Publicando imagens do Docker](tutorials/publish-packages/publish-docker-images.md)

  Neste tutorial, você aprenderá a publicar imagens do Docker em um registro, como Docker Hub ou GitHub Packages, como parte do fluxo de trabalho de CI (integração contínua).

* [Publicando pacotes Java com o Gradle](tutorials/publish-packages/publish-java-packages-with-gradle.md)

  Neste tutorial, você aprenderá a usar o Gradle para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua).

* [Publicando pacotes de Java com o Maven](tutorials/publish-packages/publish-java-packages-with-maven.md)

  Neste tutorial, você aprenderá a usar o Maven para publicar pacotes Java em um registro como parte do fluxo de trabalho de CI (integração contínua).

* [Publicar pacotes do Node.js](tutorials/publish-packages/publish-nodejs-packages.md)

  Neste tutorial, você aprenderá a publicar pacotes do Node.js em um registro como parte do fluxo de trabalho de CI (integração contínua).

* [Adicionando etiquetas a problemas](tutorials/manage-your-work/add-labels-to-issues.md)

  Você pode usar GitHub Actions para rotular problemas automaticamente.

* [Fechar questões inativas](tutorials/manage-your-work/close-inactive-issues.md)

  Você pode usar o GitHub Actions para comentar ou fechar problemas inativos por um determinado período de tempo.

* [Comentar sobre um problema quando uma etiqueta é adicionada](tutorials/manage-your-work/add-comments-with-labels.md)

  Você pode usar GitHub Actions para comentar automaticamente sobre problemas quando um rótulo específico é aplicado.

* [Agendar a criação de problemas](tutorials/manage-your-work/schedule-issue-creation.md)

  Você pode usar o GitHub Actions para criar um problema regularmente para itens como reuniões diárias ou revisões trimestrais.

* [Armazenar e compartilhar dados com artefatos de fluxo de trabalho](tutorials/store-and-share-data.md)

  Use artefatos para compartilhar dados entre trabalhos em um fluxo e armazene dados quando o fluxo de trabalho estiver concluído.

* [Criando uma ação de contêiner do Docker](tutorials/use-containerized-services/create-a-docker-container-action.md)

  Neste tutorial, você aprenderá a criar uma ação de contêiner do Docker.

* [Comunicar-se com os contêineres de serviço do Docker](tutorials/use-containerized-services/use-docker-service-containers.md)

  Saiba como usar contêineres de serviço do Docker para conectar bancos de dados, serviços web, memória cache e outras ferramentas ao seu fluxo de trabalho.

* [Criar contêineres de serviço PostgreSQL](tutorials/use-containerized-services/create-postgresql-service-containers.md)

  Você pode criar um contêiner de serviço PostgreSQL para usar no seu fluxo de trabalho. Este guia mostra exemplos para criar um serviço PostgreSQL para trabalhos executados em contêineres ou diretamente na máquina executora.

* [Criando contêineres de serviço Redis](tutorials/use-containerized-services/create-redis-service-containers.md)

  Você pode usar os contêineres de serviço para criar um cliente Redis no seu fluxo de trabalho. Este guia mostra exemplos de criação de serviço Redis para trabalhos executados em contêineres ou diretamente na máquina executora.

* [Automatizando a migração com o importador de GitHub Actions](tutorials/migrate-to-github-actions/automated-migrations/use-github-actions-importer.md)

  Use o GitHub Actions Importer para planejar e automatizar sua migração para o GitHub Actions.

* [Migrando de Azure DevOps com o Importador de GitHub Actions](tutorials/migrate-to-github-actions/automated-migrations/azure-devops-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de Azure DevOps para GitHub Actions.

* [Migrando do Bamboo para o GitHub Actions Importer](tutorials/migrate-to-github-actions/automated-migrations/bamboo-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do Bamboo para GitHub Actions.

* [Migrando do Bitbucket Pipelines com o importador de GitHub Actions](tutorials/migrate-to-github-actions/automated-migrations/bitbucket-pipelines-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Bitbucket para GitHub Actions.

* [Migrando do CircleCI com GitHub Actions Importer](tutorials/migrate-to-github-actions/automated-migrations/circleci-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do CircleCI para GitHub Actions.

* [Migrando do GitLab com o Importador de GitHub Actions](tutorials/migrate-to-github-actions/automated-migrations/gitlab-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines do GitLab para GitHub Actions.

* [Migrando do Jenkins com o Importador de GitHub Actions](tutorials/migrate-to-github-actions/automated-migrations/jenkins-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração dos pipelines do Jenkins para GitHub Actions.

* [Migrando do Travis CI com GitHub Actions Importer](tutorials/migrate-to-github-actions/automated-migrations/travis-ci-migration.md)

  Saiba como usar GitHub Actions Importer para automatizar a migração de seus pipelines de CI travis para GitHub Actions.

* [Migrando de Azure Pipelines para GitHub Actions](tutorials/migrate-to-github-actions/manual-migrations/migrate-from-azure-pipelines.md)

  GitHub Actions e Azure Pipelines compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples.

* [Migrando do CircleCI para o GitHub Actions](tutorials/migrate-to-github-actions/manual-migrations/migrate-from-circleci.md)

  GitHub Actions e CircleCI compartilham várias semelhanças na configuração, o que torna a migração para GitHub Actions relativamente simples.

* [Migrando de CI/CD do GitLab para GitHub Actions](tutorials/migrate-to-github-actions/manual-migrations/migrate-from-gitlab-cicd.md)

  GitHub Actions e o GITLab CI/CD compartilham várias semelhanças de configuração, o que torna a migração para GitHub Actions relativamente simples.

* [Migrando do Jenkins para o GitHub Actions](tutorials/migrate-to-github-actions/manual-migrations/migrate-from-jenkins.md)

  GitHub Actions e Jenkins compartilham várias semelhanças, o que torna a migração para GitHub Actions relativamente simples.

* [Migrando de Travis CI para GitHub Actions](tutorials/migrate-to-github-actions/manual-migrations/migrate-from-travis-ci.md)

  GitHub Actions e Travis CI compartilham várias semelhanças, o que ajuda a tornar relativamente simples migrar para GitHub Actions.

* [Comece a usar o Actions Runner Controller](tutorials/use-actions-runner-controller/get-started.md)

  Neste tutorial, você experimentará as noções básicas de Actions Runner Controller.

* [Solução de problemas dos erros do Actions Runner Controller](tutorials/use-actions-runner-controller/troubleshoot.md)

  Saiba como solucionar Actions Runner Controller erros.

* [Desenvolver fluxos de trabalho agente no GitHub Actions](tutorials/develop-agentic-workflows-in-github-actions.md)

  Use GitHub Agentic Workflows para transformar instruções do Markdown em automações alimentadas por agentes de codificação de terceiros.
