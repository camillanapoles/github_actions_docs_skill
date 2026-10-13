---
title: Limites do Actions
description: Há limites no GitHub Actions que você pode atingir à medida que escala seu uso; alguns deles podem aumentar ao entrar em contato com o suporte.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/limits
captured: '2026-10-11'
section: Reference
---

# Limites do Actions { #actions-limits }

_Há limites no GitHub Actions que você pode atingir à medida que escala seu uso; alguns deles podem aumentar ao entrar em contato com o suporte._

Você pode sofrer limitação de taxa pelo GitHub Actions ao escalar seu uso. Alguns limites podem aumentar ao entrar em contato com o nos por meio do portal .

A menos que seja indicado de outra forma, o comportamento esperado quando um limite é atingido é que o fluxo de trabalho/trabalho seja cancelado.

Estes limites estão sujeitos a mudanças.

## Limites do sistema existente { #existing-system-limits }

| Categoria do limite | Limite | Limite | Descrição | É possível aumentar o suporte GitHub? |
| :-- | :-- | :-- | :-- | :-- |
| Limite de execução do fluxo de trabalho | Tempo de execução de fluxo de trabalho | 35 dias / execução do fluxo de trabalho | Se a execução de um fluxo de trabalho atingir esse limite, a execução do fluxo de trabalho será cancelada. Esse período inclui a duração da execução e o tempo gasto em espera e aprovação. | ❌ |
| Limite de execução do fluxo de trabalho | Tempo de aprovação do portão | 30 dias | Um fluxo de trabalho pode aguardar até [30 dias para aprovações ambientais](workflows-and-actions/deployments-and-environments.md#wait-timer). | ❌ |
| Limite de execução do fluxo de trabalho | Matriz de trabalho | 256 tarefas / execução de fluxo de trabalho | Uma matriz de trabalho pode gerar um máximo de 256 trabalhos por execução de fluxo de trabalho. Esse limite se aplica a executores hospedados em GitHub e auto-hospedados. | ❌ |
| Limite de execução do fluxo de trabalho | Executar novamente | 50 repetições | Uma execução de fluxo de trabalho pode ser executada novamente no máximo 50 vezes. Esse limite inclui tanto reexecuções completas quanto reexecuções de um subconjunto de tarefas. |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Arquivo de fluxo de trabalho | Tamanho do arquivo de fluxo de trabalho | 500 KB por arquivo | Um arquivo de fluxo de trabalho maior que 500 KB não iniciará as execuções. Consulte o [tamanho do arquivo de fluxo de trabalho](#workflow-file-size). | ❌ |
| Cheques | Verificar execuções por conjunto de verificações | 50.000 execuções de verificação / conjunto de verificação | Um conjunto de verificação pode ter um máximo de 50.000 execuções de verificação. Esse limite se aplica às execuções de verificação criadas por meio da API de Verificações e por execuções de fluxo de trabalho GitHub Actions. Quando um pacote de seleção atinge esse limite, não é possível criar execuções de verificação adicionais para esse pacote de seleção. |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Enfileiramento de fluxos de trabalho | Limite de taxa de eventos de gatilho de fluxo de trabalho | 1500 eventos / 10 segundos / repositório | Cada repositório é limitado a eventos que acionam a execução de um fluxo de trabalho. |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Enfileiramento de fluxos de trabalho | Execução do fluxo de trabalho enfileirada | 500 execuções de fluxo de trabalho / 10 segundos | Quando o limite for atingido, as execuções de fluxo de trabalho que deveriam ser acionadas pelos eventos do webhook serão bloqueadas e não serão enfileiradas. Fluxos de trabalho reutilizáveis ​​são vistos como uma única entidade. Por exemplo, uma execução com 30 fluxos de trabalho reutilizáveis ​​conta como 1 neste caso. | ❌ |
| Enfileiramento de fluxos de trabalho | Fila de grupo de concorrência | 100 execuções de fluxo de trabalho/grupo de concorrência | Ao usar `queue: max` na seção `concurrency`, até 100 trabalhos ou execuções de fluxo de trabalho podem ser enfileirados por grupo de concorrência. Tentativas além desse limite serão rejeitadas. | ❌ |
| Auto-hospedado | Registros de executores | 1500 executores / 5 minutos / repositório / organização / empresa | Os executores podem ser registrados por repositório / organização / empresa. |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Auto-hospedado | Executores por grupo de executores | 10,000 executores | Os executores se registraram ao mesmo tempo em cada grupo. | ❌ |
| Auto-hospedado | Tempo de execução do trabalho | 5 dias | O tempo de execução de cada trabalho no fluxo pode ser de até cinco dias. Se um trabalho atingir esse limite, ele será terminado e falhará. | ❌ |
| Auto-hospedado | Tempo da fila de trabalhos | 24 horas | Um trabalho pode ficar na fila por 24 horas antes do cancelamento automático. | ❌ |
| Todos os runners hospedados pelo GitHub | Simultaneidade de Trabalho | Varia | Consulte [Limites de simultaneidade de trabalhos para executores hospedados pelo GitHub](#job-concurrency-limits-for-github-hosted-runners). |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Todos os runners hospedados pelo GitHub | Tempo de execução do trabalho | 6 horas | Cada trabalho em um fluxo de trabalho pode ter um tempo de execução de até seis horas. Se um trabalho atingir esse limite, ele será terminado e falhará. | ❌ |
| Todos os runners hospedados pelo GitHub | Limites de armazenamento | Varia | Para obter mais informações, consulte [Limites de armazenamento para todos os executores hospedados pelo GitHub](#storage-limits-for-all-github-hosted-runners). | ❌ |
| Executores avançados | Limite de concorrência por executor | Varia de acordo com o tipo de executor | Estabelecido ao configurar um executor. Em geral, até 1.000 para executores de CPU do Linux, mas varia conforme o tipo. Consulte [Limites de simultaneidade de trabalhos para executores hospedados pelo GitHub](#job-concurrency-limits-for-github-hosted-runners). |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Executores avançados | Limites de IP estático | 10 endereços IP | 10 IPs por empresa e organização. |  |
| ✅ Tíquete de suporte |  |  |  |  |
| Executores avançados | Dimensionamento de IP privado para injeção de vnet | Buffer de 30% | Você precisa de um buffer para acomodar a simultaneidade máxima do trabalho prevista. Confira [Dimensionamento de IP privado para injeção de Vnet em executores avançados](#private-ip-scaling-for-vnet-injection-on-larger-runners). |  |
| ✅ rede virtual de Azure configurável |  |  |  |  |
| Cache de dependência | Carregamentos por minuto | 200 por minuto | Cada repositório é limitado a 200 uploads de entrada de cache por minuto. Se esse limite for excedido, as tentativas de upload de cache subsequentes falharão até que o limite de taxa seja redefinido. | ❌ |
| Cache de dependência | Downloads por minuto | 1500 por minuto | Cada repositório é limitado a 1500 downloads de entrada de cache por minuto. Se esse limite for excedido, as tentativas de download de cache subsequentes falharão até que o limite de taxa seja redefinido. | ❌ |
| Cache de dependência | Exclusões por minuto | 400 por minuto | Cada repositório é limitado a 400 operações de exclusão de cache por minuto. Se esse limite for excedido, as tentativas subsequentes de exclusão de cache falharão até que o limite de taxa seja redefinido. Cada solicitação para excluir caches por chave ou por ID conta para esse limite. | ❌ |

### Tamanho do arquivo de fluxo de trabalho { #workflow-file-size }

Cada arquivo de fluxo de trabalho no `.github/workflows` diretório deve ter 500 KB ou menor para disparar uma execução. Para reduzir o tamanho de um arquivo de fluxo de trabalho, mova a lógica compartilhada para um fluxo de trabalho reutilizável ou uma ação composta. Confira [Reutilizar fluxos de trabalho](../how-tos/reuse-automations/reuse-workflows.md) ou [Criar uma ação composta](../tutorials/create-actions/create-a-composite-action.md).

### Limites de simultaneidade de trabalhos para executores hospedados pelo GitHub { #job-concurrency-limits-for-github-hosted-runners }

GitHub O suporte **pode** aumentar os limites de concorrência de tarefas para GitHub Actions. Para solicitar um aumento, envie um tíquete de suporte.

| Tipo de executor |
GitHub Plano | Total de tarefas simultâneas | Máximo de tarefas macOS simultâneas | Máximo de trabalhos de GPU simultâneos |
|---|---|---|---|---|
| Executor padrão hospedado pelo GitHub | Gratuito | 20 | 5 | Não aplicável |
| Executor padrão hospedado pelo GitHub | Pro | 40 | 5 | Não aplicável |
| Executor padrão hospedado pelo GitHub | Equipe | 60 | 5 | Não aplicável |
| Executor padrão hospedado pelo GitHub | Enterprise | 500 | 50 | Não aplicável |
| Executor avançado | Equipe | 1000 | 5 | 100 |
| Executor avançado | Enterprise | 1000 | 50 | 100 |

!!! note
    O número máximo de trabalhos simultâneos no macOS é compartilhado entre os executores padrão hospedados pelo GitHub e os executores maiores hospedados pelo GitHub

### Limites de armazenamento para todos os executores hospedados pelo GitHub { #storage-limits-for-all-github-hosted-runners }

GitHub O **suporte não pode** aumentar os limites de armazenamento para GitHub Actions.

| Plano                         | Armazenamento de artefatos | Minutos (por mês) | Armazenamento em cache (por repositório) | Armazenamento de imagens personalizadas |
|-----------------------------|--------------------------|-----------------|----------------------------------------|---------------------------------------|
| GitHub Free                   | 500 MB                     | 2.000             | 10 GB                                    | Não aplicável                           |
| GitHub Pro                    | 1 GB                       | 3.000             | 10 GB                                    | Não aplicável                           |
| GitHub Free para organizações | 500 MB                     | 2.000             | 10 GB                                    | Não aplicável                           |
| GitHub Team                   | 2 GB                       | 3.000             | 10 GB                                    | 75 GB                                   |
| GitHub Enterprise Cloud       | 50 GB                      | 50,000            | 10 GB                                    | 150 GB                                  |

Para obter informações sobre os limites de armazenamento em cache e como aumentá-los, consulte [limites de uso e política de remoção](workflows-and-actions/dependency-caching.md#usage-limits-and-eviction-policy).

### Dimensionamento de IP privado para injeção de Vnet em executores avançados { #private-ip-scaling-for-vnet-injection-on-larger-runners }

Ao usar executores avançados com injeção vnet, você precisa determinar o intervalo de endereços IP de sub-rede apropriado, recomendamos adicionar um buffer à simultaneidade máxima de trabalho prevista. Por exemplo, se os executores da configuração de rede estiverem definidos para uma simultaneidade de trabalho máxima de 300, utilize um intervalo de endereços IP de sub-rede que possa acomodar pelo menos 390 executores. Observe que Azure reserva 5 IPs em cada sub-rede (primeiro 4 e último 1), o que define um tamanho mínimo de sub-rede prática dependendo dos requisitos do executor. Sub-redes muito pequenas (como /29 ou menor) podem não fornecer endereços utilizáveis suficientes para suas necessidades.

## Limites de serviço dependentes que costumam ser atingidos { #commonly-hit-dependent-service-limits }

GitHubOs [limites de taxa da API REST](https://docs.github.com/pt/rest/using-the-rest-api/rate-limits-for-the-rest-api) se aplicam aos GitHub Actions usuários, aqueles que geralmente são atingidos são:

* **Usuários não autenticados**-Será possível fazer solicitações não autenticadas se você estiver buscando apenas dados públicos. As solicitações não autenticadas estão associadas ao endereço IP original, e não ao usuário ou aplicativo que fez a solicitação.

  O limite de taxa primária para solicitações não autenticadas é de 60 por hora.
* **Usuários autenticados**-É possível usar um personal access token para fazer solicitações à API. Além disso, você pode autorizar um GitHub App ou OAuth app, que depois podem fazer solicitações à API em seu nome.

  Todas essas solicitações contam para o limite de taxa pessoal de solicitações de 5.000 por hora. O limite de taxa será mais alto (15.000 solicitações por hora) se as solicitações forem feitas em seu nome por um GitHub App pertencente a uma organização do GitHub Enterprise Cloud. Da mesma forma, as solicitações feitas em seu nome por um OAuth app que pertence ou é aprovado por uma organização GitHub Enterprise Cloud têm um limite de taxa mais alto de 15.000 solicitações por hora se você é membro da organização GitHub Enterprise Cloud. No entanto, as solicitações feitas por um aplicativo de limite mais alto reduzem o orçamento restante disponível para métodos de autenticação de limite inferior. Por exemplo, se um aplicativo com um limite de solicitação de 15.000 fizer 10.000 solicitações em seu nome, você terá esgotado o orçamento de 5.000 solicitações para o personal access tokens, mesmo que o aplicativo tenha 5.000 solicitações restantes.
* instalações de aplicativo **GitHub**-Os GitHub Apps que se autenticam com um token de acesso de instalação usam o limite mínimo da taxa de instalação de 5.000 solicitações por hora. Se a instalação estiver em uma organização do GitHub Enterprise Cloud, a instalação terá um limite de taxa de 15 mil solicitações por hora.

  Para instalações que não estão em uma organização do GitHub Enterprise Cloud, o limite de taxa para a instalação será dimensionado com o número de usuários e repositórios. As instalações com mais de 20 repositórios recebem outras 50 solicitações por hora para cada repositório. Instalações que estão em uma organização com mais de 20 usuários recebem outras 50 solicitações por hora para cada uma dessas pessoas. Não é possível ampliar o limite de taxa para além de 12.500 solicitações por hora.

  Os limites de taxa primária para tokens de acesso do usuário do GitHub App (diferentemente dos tokens de acesso de instalação) são determinados pelos limites de taxa primária do usuário autenticado. Esse limite de taxa é combinado com todas as solicitações que outro GitHub App ou OAuth app faça em nome do usuário, bem como todas as solicitações realizadas pelo usuário com um personal access token. Para saber mais, confira [Limites de taxa para a API REST](https://docs.github.com/pt/rest/using-the-rest-api/rate-limits-for-the-rest-api#primary-rate-limit-for-authenticated-users).
* \*\*Aplicativos OAuth -\*\*Nesse caso, o limite de taxa é de 5.000 solicitações por hora, por OAuth app. Se o aplicativo pertencer a uma organização do GitHub Enterprise Cloud, o limite de taxa será de 15.000 solicitações por hora.
* **GITHUB TOKEN**-O limite de taxa de `GITHUB_TOKEN` é de mil solicitações por hora e por repositório. Para solicitações de recursos que pertencem a uma conta de GitHub Enterprise Cloud, o limite é de 15.000 solicitações por hora e por repositório.
* **Limites de taxa secundários**- Além dos limites de taxa primária, GitHub impõe limites de taxa secundários para evitar abusos e manter a API disponível para todos os usuários, elas não são configuráveis com GHEC. Para saber mais, confira [Limites de taxa para a API REST](https://docs.github.com/pt/rest/using-the-rest-api/rate-limits-for-the-rest-api#about-secondary-rate-limits).

### Limite de taxa do Docker Hub para GitHub Actions { #docker-hubs-rate-limit-for-github-actions }

* \*\*              Executores hospedados pelo GitHub extraindo imagens públicas:\*\* não se aplica o limite de taxa do Docker Hub.
* \*\*              Executores hospedados pelo GitHub que extraem imagens privadas:\*\* a extração de imagens privadas do Docker Hub está sujeita ao limite de taxa.
* **Executores auto-hospedados que extraem imagens públicas ou privadas:** a extração de imagens do Docker Hub está sempre sujeita ao limite de taxa.
