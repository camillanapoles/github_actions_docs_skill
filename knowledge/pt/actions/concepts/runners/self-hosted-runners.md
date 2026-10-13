---
title: Executores auto-hospedados
description: Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus fluxos de trabalho GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/runners/self-hosted-runners
captured: '2026-10-13'
section: Concepts / Runners
---

# Executores auto-hospedados

_Você pode hospedar seus próprios executores e personalizar o ambiente usado para executar trabalhos em seus fluxos de trabalho GitHub Actions._

Um executor auto-hospedado é um sistema que você implanta e gerencia para executar trabalhos do GitHub Actions no GitHub.

Executores auto-hospedados:

* Oferecem a você mais controle sobre o hardware, o sistema operacional e as ferramentas de software do que os executores hospedados em GitHub. Lembre-se de que você é responsável por atualizar o sistema operacional e todos os outros softwares.
* Permitir que você use computadores e serviços que sua empresa já mantém e paga para usar.
* São gratuitos para uso com o GitHub Actions, mas você é responsável pelo custo de manter as máquinas do executor.
* Permitem que você crie configurações de hardware personalizadas que atendam às suas necessidades, com poder de processamento ou memória para executar trabalhos maiores, instalar o software disponível em sua rede local.
* Receba atualizações automáticas apenas para o aplicativo do executor auto-hospedado, embora você possa desabilitar atualizações automáticas do executor.
* Não é necessário ter uma instância limpa para cada execução de tarefa.
* Podem ser físicos, virtuais, em um contêiner, no local ou em uma nuvem.

Você pode usar executores auto-hospedados em qualquer lugar na hierarquia de gerenciamento. Os executores do nível do repositório são dedicados a um só repositório, enquanto os executores do nível da organização podem processar trabalhos para vários repositórios em uma organização. Os proprietários da organização podem escolher quais repositórios têm permissão para criar executores auto-hospedados no nível do repositório. Confira [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#limiting-the-use-of-self-hosted-runners). Por fim, executores de nível empresarial podem ser atribuídos a várias organizações em uma conta corporativa.

## Próximas etapas

Para configurar um executor auto-hospedado em seu workspace, consulte [Adicionar executores auto-hospedados](../../how-tos/manage-runners/self-hosted-runners/add-runners.md).

Para encontrar informações sobre os requisitos e o software e o hardware com suporte para executores auto-hospedados, confira [Referência de executores auto-hospedados](../../reference/runners/self-hosted-runners.md).
