---
title: Obtendo ajuda do suporte GitHub sobre GitHub Actions
description: Saiba como Suporte do GitHub ajudar com GitHub Actions
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/get-support
captured: '2026-10-19'
section: How tos
---

# Obtendo ajuda do suporte GitHub sobre GitHub Actions

_Saiba como Suporte do GitHub ajudar com GitHub Actions_

Você pode [entrar em contato Suporte do GitHub](https://docs.github.com/pt/support/contacting-github-support) para obter assistência com GitHub Actions.

## Fornecendo informações de diagnóstico e solução de problemas

O conteúdo dos repositórios privados e internos não é visível Suporte do GitHub, portanto Suporte do GitHub , pode solicitar informações adicionais para entender o contexto completo da investigação e reproduzir qualquer comportamento inesperado. Você pode acelerar a resolução do seu inquérito fornecendo essas informações ao gerar inicialmente um tíquete com Suporte do GitHub.

Algumas informações que Suporte do GitHub serão solicitadas podem incluir, mas não se limitam a:

* A URL da execução do fluxo de trabalho.

  Por exemplo: `https://github.com/ORG/REPO/actions/runs/0123456789`

* O(s) arquivo(s) de fluxo de trabalho `.yml` anexado(s) ao tíquete como arquivos `.txt`. Para obter mais informações sobre os fluxos de trabalho, consulte [Fluxos de trabalho](../concepts/workflows-and-actions/workflows.md#about-workflows).

* Uma cópia dos logs de execução do fluxo de trabalho para um exemplo de falha de execução do fluxo de trabalho. Para obter mais informações sobre logs de execução de workflows, consulte [Usando registros de execução de fluxo de trabalho](monitor-workflows/use-workflow-run-logs.md#downloading-logs).

* se você estiver executando esse fluxo de trabalho em um executor auto-hospedado, logs de executor auto-hospedado que podem ser encontrados na `_diag` pasta dentro do executor. Para saber mais sobre executores auto-hospedados, confira [Monitorar e solucionar problemas de executores auto-hospedados](manage-runners/self-hosted-runners/monitor-and-troubleshoot.md#reviewing-the-self-hosted-runner-application-log-files).

  Os nomes de arquivo de log do executor auto-hospedado são formatados: `Runner_YYYY####-xxxxxx-utc.log` e `Worker_YYYY####-xxxxxx-utc.log`.

!!! note
    Anexe arquivos ao seu tíquete de suporte alterando a extensão do arquivo para `.txt` ou `.zip`. Se você incluir dados textuais, como trechos de arquivo de log ou de fluxo de trabalho, embutidos no seu tíquete, verifique se eles estão formatados corretamente como blocos de código de Markdown. Para obter mais informações sobre a formatação correta do Markdown, consulte [Sintaxe básica de escrita e formatação](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#quoting-code).

    Se as informações fornecidas não forem ilegíveis devido à perda de formatação por sintaxe Markdown inadequada, Suporte do GitHub poderá solicitar que as informações sejam reenviadas como um anexo ou com a formatação markdown correta.

    [!WARNING]
    Verifique se todos os arquivos e textos fornecidos Suporte do GitHub foram redigidos corretamente para remover informações confidenciais, como tokens e outros segredos.

### Arquivos de log do aplicativo do executor efêmero

Suporte do GitHub pode solicitar os arquivos de log do aplicativo executor de executores de executores efêmeros.
GitHub espera e recomenda que você tenha implementado um mecanismo para encaminhar e preservar os arquivos de log do aplicativo executor de executores efêmeros auto-hospedados. Para obter mais informações sobre arquivos de log do aplicativo do executor e solução de problemas de executores auto-hospedados, consulte [Monitorar e solucionar problemas de executores auto-hospedados](manage-runners/self-hosted-runners/monitor-and-troubleshoot.md#reviewing-the-self-hosted-runner-application-log-files).

### Actions Runner Controller

Se você estiver usando Actions Runner Controller (ARC), Suporte do GitHub poderá solicitar que você envie os logs completos para os pods controlador, ouvinte e executor. Para obter mais informações sobre como coletar Actions Runner Controllerlogs, consulte [Solução de problemas dos erros do Actions Runner Controller](../tutorials/use-actions-runner-controller/troubleshoot.md#checking-the-logs-of-the-controller-and-runner-set-listener).

Para obter mais informações sobre o escopo do suporte, Actions Runner Controllerconsulte [Suporte para o Controlador do Executor de Ações](../concepts/runners/support-for-arc.md).

### CodeQL e GitHub Actions

Se você estiver solicitando assistência com um Fluxo de trabalho de análise do CodeQL, Suporte do GitHub poderá solicitar uma cópia dos CodeQL artefatos de depuração. Para obter mais informações sobre a depuração de artefatos para um Fluxo de trabalho de análise do CodeQL, consulte [Os logs não são detalhados o suficiente](https://docs.github.com/pt/code-security/reference/code-scanning/troubleshoot-analysis-errors/logs-not-detailed-enough#creating-codeql-debugging-artifacts).

Para fornecer os artefatos de depuração, Suporte do GitHubbaixe os CodeQL artefatos de depuração de uma execução de fluxo de trabalho de exemplo e anexe-os ao seu tíquete como um `.zip` arquivo. Para obter mais informações sobre como baixar artefatos de fluxo de trabalho, confira [Baixar artefatos do fluxo de trabalho](manage-workflow-runs/download-workflow-artifacts.md).

Se o CodeQL arquivo de artefatos `.zip` de depuração for muito grande para carregar no tíquete, informe Suporte do GitHube trabalharemos com você para determinar as próximas etapas.

## Escopo do suporte

Se sua solicitação de suporte estiver fora do escopo com o qual nossa equipe pode ajudar, poderemos recomendar os próximos passos para resolver seu problema fora de Suporte do GitHub. Sua solicitação de suporte possivelmente estará fora do Suporte do GitHubescopo se a solicitação for principalmente sobre:

* Integrações de terceiros, como o Jira
* CI/CD, como Jenkins
* Azure DevOps (entre em contato com o Suporte do Azure)
* Criação de scripts
* Configuração de sistemas de autenticação externa, como provedores de identidade SAML
* Projetos de software livre
* Gravando ou depurando novas consultas para CodeQL
* Configurações do provedor de nuvem, como configuração de rede virtual, firewall personalizado ou regras de proxy
* Orquestração de contêineres, como configuração do Kubernetes ou redes
* Assistência detalhada com fluxos de trabalho e gerenciamento de dados
* Suporte abrangente para personalização e instalação de ferramentas em GitHub Actions imagens personalizadas
* Recursos em versão prévia. Os recursos Versão preliminar pública, versão prévia privada e versão prévia técnica estão fora do escopo de Suporte do GitHub.
* GitHub Copilot Sugestões
* GitHub Copilot dúvidas sobre consumo.
  Suporte do GitHub não audita nem divide o Copilot consumo de uso. O suporte pode explicar o modelo de cobrança e apontá-lo para a documentação de relatório de uso disponível, mas não pode determinar por que o uso parece alto ou por que o uso incluído foi esgotado mais cedo do que o esperado.
* Explicações sobre a cobrança medida.
  Suporte do GitHub não interpreta o relatório de uso ou as tendências de gastos para produtos de cobrança limitada GitHub , nem fornece recomendações com base nesses dados. Para obter mais informações, consulte [Ciclos de cobrança](https://docs.github.com/pt/billing/concepts/billing-cycles).

GitHub Copilot fornece sugestões de código e respostas com tecnologia de IA. Conforme descrito em nossos termos legais, você tem total responsabilidade pelo seu código, incluindo pelas sugestões que optar por incorporar. A qualidade, a precisão, a relevância ou a funcionalidade das respostas de Copilot's podem nem sempre atender às suas expectativas, e erros podem ocorrer. Cabe a você decidir se deseja usar as sugestões de Copilot, e o GitHub recomenda enfaticamente a implementação de políticas e práticas razoáveis para impedir o uso de qualquer sugestão de forma que possa violar os direitos de terceiros. Isso inclui, mas não se limita a, usar os recursos de filtragem disponíveis em Copilot.

CopilotAs sugestões e as saídas geradas estão fora do escopo do suporte. GitHub Suporte não pode garantir a correção ou a adequação das respostas de Copilot e não é responsável pelos resultados produzidos. Se tiver preocupações com sugestões específicas, examine todos os links e informações fornecidas para garantir a precisão e a conformidade com seus requisitos. Para obter mais informações, consulte [GitHub Copilot Termos](https://docs.github.com/pt/site-policy/github-terms/github-terms-for-additional-products-and-features#github-copilot) e [práticas recomendadas para usar Copilot](https://docs.github.com/pt/copilot/get-started/best-practices).

\*\*
Suporte do GitHub não fornece suporte para versões descontinuadas GitHub Enterprise Server .\*\* Se você estiver executando uma versão descontinuada, atualize para uma versão com suporte antes de abrir um tíquete de suporte para que possamos ajudá-lo com eficiência.

Para obter assistência com tópicos fora do escopo de suporte, para consultoria guiada, workshops ou treinamento para suas equipes, consulte os [GitHub Serviços Especializados](https://github.com/services/), que oferecem serviços especializados para ajudá-lo a otimizar o uso de nossa plataforma.

Se não tem certeza se o problema está fora do escopo, abra um tíquete e ficaremos felizes em ajudá-lo a determinar a melhor maneira de prosseguir.
