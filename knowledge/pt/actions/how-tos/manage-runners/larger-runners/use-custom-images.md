---
title: Usando imagens personalizadas
description: Crie, gerencie e use imagens personalizadas para Executores maiores hospedados no GitHub sua organização ou empresa.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/manage-runners/larger-runners/use-custom-images
captured: '2026-10-11'
section: GitHub Actions
---

# Usando imagens personalizadas

_Crie, gerencie e use imagens personalizadas para Executores maiores hospedados no GitHub sua organização ou empresa._

## Imagens personalizadas

Você pode criar uma imagem personalizada para definir o ambiente exato que você Executores maiores hospedados no GitHub usa. As imagens personalizadas permitem pré-instalar ferramentas, dependências e configurações para acelerar fluxos de trabalho e melhorar a consistência entre trabalhos.

Quando o executor usa uma imagem personalizada, ele atua como um ambiente "pré-aquecido", permitindo que os fluxos de trabalho sejam concluídos mais rapidamente, baixando pacotes e binários uma vez durante a criação da imagem, em vez de cada vez que um fluxo de trabalho é executado. Para obter mais informações sobre imagens personalizadas, consulte [imagens do Runner](../../../concepts/runners/github-hosted-runners.md#runner-images).

O processo de uso de uma imagem personalizada envolve três etapas principais:

1. [Configurando um executor de geração de imagem](#setting-up-an-image-generation-runner): crie um executor avançado para criar e armazenar sua imagem personalizada.
2. [Gerando uma imagem personalizada](#generating-a-custom-image): gere sua imagem personalizada executando um fluxo de trabalho usando o executor de geração de imagem.
3. [Instalando imagens personalizadas](#installing-custom-images): crie um executor que use sua imagem personalizada.

## Pré-requisitos

Antes de criar imagens personalizadas, verifique se os requisitos a seguir são atendidos.

* **Política**: as imagens personalizadas devem ser habilitadas para sua organização ou empresa. Os proprietários da empresa podem gerenciar o acesso a imagens personalizadas e definir políticas de retenção nas configurações de política de Ações. Para saber mais, confira [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#custom-images).
* **Permissões**: Para criar e gerenciar imagens personalizadas, você deve ser um proprietário de organização ou empresa, ou ter a `CI/CD Admin` função ou ter uma função com as seguintes permissões detalhadas.

  * Exibir imagens personalizadas de runners hospedados pela organização
  * Gerenciar imagens personalizadas de executores hospedados pela organização
  * Gerenciar executores e grupos de executores da organização

  Para saber mais, confira [Permissões de funções de organização personalizadas](https://docs.github.com/pt/organizations/managing-peoples-access-to-your-organization-with-roles/permissions-of-custom-organization-roles).

## Configurando um executor de geração de imagem

Para criar uma imagem personalizada, primeiro você deve configurar um executor de geração de imagem. Quando você cria o executor, a plataforma selecionada para ele deve corresponder à plataforma da imagem que você deseja criar. A plataforma do executor pode ser Linux x64, Linux ARM64 ou Windows x64.

1. Criar um executor avançado:
   * Para organizações, consulte [Como adicionar um executor maior a uma organização](manage-larger-runners.md#adding-a-larger-runner-to-an-organization).
   * Para empresas, consulte [Como adicionar um executor maior a uma empresa](manage-larger-runners.md#adding-a-larger-runner-to-an-enterprise).
2. Ao configurar o executor, selecione as seguintes configurações para o seu executor de geração de imagem:
   * **Plataforma**: selecione uma plataforma com suporte que corresponda à plataforma da imagem que você planeja criar (Linux x64, Linux ARM64 ou Windows x64).
   * **Imagem**: Selecione uma imagem na qual criar e habilite a caixa de seleção **Habilitar esse executor para gerar imagens personalizadas**.
     * Você pode começar com uma imagem pertencente a GitHub ou escolher uma imagem base para começar com um sistema operacional limpo.
     * Você pode começar a partir de uma imagem personalizada existente como base, habilitando fluxos de trabalho de imagem em camadas.
     * Para plataformas ARM64, você também pode selecionar uma imagem mantida pelo ARM com ferramentas pré-instaladas.
   * **Grupo de runners**: selecione o grupo do qual o runner será associado. Depois que a imagem personalizada for criada, apenas os executores neste grupo de executores poderão gerar novas versões dessa imagem.

## Gerando uma imagem personalizada

Depois de criar um executor de geração de imagem, execute um fluxo de trabalho que inclui a `snapshot` palavra-chave para gerar uma imagem personalizada.

Para configurar um fluxo de trabalho para a geração de imagem:

* Defina o `runs-on` valor como o nome do executor de geração de imagem que você criou.
* Adicione a `snapshot` palavra-chave ao trabalho usando a sintaxe da cadeia de caracteres ou a sintaxe de mapeamento mostrada abaixo.
  * Cada trabalho que inclui a `snapshot` palavra-chave cria uma imagem separada. Para gerar apenas uma imagem ou versão de imagem, inclua todas as etapas de fluxo de trabalho em um único trabalho.
  * Cada execução bem-sucedida de um trabalho que inclui a `snapshot` palavra-chave cria uma nova versão dessa imagem.

> \[!NOTE]
> GitHub recomenda configurar a geração de imagem como um fluxo de trabalho agendado semanalmente. Essa abordagem garante que as dependências permaneçam up-to-date e tenham os patches de segurança mais recentes. Para saber mais, confira [Eventos que disparam fluxos de trabalho](../../../reference/workflows-and-actions/events-that-trigger-workflows.md#schedule).

Pode levar algum tempo para que sua imagem seja totalmente gerada e pronta para ser usada após a conclusão do fluxo de trabalho. O tempo de provisionamento varia de acordo com o tamanho e a configuração do executor e pode levar várias horas para executores maiores.

A imagem é gerada somente quando o trabalho é concluído com êxito. Isso impede que novas versões de imagem sejam criadas quando um fluxo de trabalho falhar ou terminar em um estado incompleto.

Depois que a imagem é gerada, ela está disponível para uso em seus fluxos de trabalho. Para obter mais informações sobre como gerenciar imagens personalizadas, consulte [Gerenciando imagens personalizadas](#managing-custom-images).

### Sintaxe de cadeia de caracteres

Você pode usar a sintaxe de cadeia de caracteres com `snapshot` para definir o nome da imagem. Esse método cria uma nova imagem ou adiciona uma nova versão a uma imagem existente com o mesmo nome. Não é possível especificar um número de versão usando essa sintaxe.

```yaml
jobs:
  build:
    runs-on: my-image-generation-runner
    snapshot: my-custom-image
    steps:
      # Add any steps to download and setup any dependencies here
```

### Sintaxe de mapeamento

Você pode usar a sintaxe de mapeamento com `snapshot` para definir tanto o `image-name` quanto o opcional `version`. Quando você especifica uma versão principal, a versão secundária é incrementada automaticamente se essa versão principal já existir. Não há suporte para versões de patch.

```yaml
jobs:
  build:
    runs-on: my-image-generation-runner
    snapshot:
        image-name: my-custom-image
        version: 2.*
    steps:
      # Add any steps to download and setup any dependencies here
```

### Condicionais

A palavra-chave `snapshot` dá suporte à execução condicional usando a palavra-chave `if` em torno do mapeamento de instantâneo. Você pode usar condições para controlar quando um instantâneo de imagem é criado. Por exemplo, o seguinte trabalho ignora a criação de imagem para compilações com marcação.

```yaml
jobs:
  build:
    runs-on: my-image-generation-runner
    snapshot:
        if: ${{ ! startsWith(github.ref, 'refs/tags/') }}
        image-name: my-custom-image
        version: 2.*
    steps:
      # Add any steps to download and setup any dependencies here
```

Para obter mais informações sobre a palavra-chave `if`, confira [Usando condições para controlar a execução do trabalho](../../write-workflows/choose-when-workflows-run/control-jobs-with-conditions.md).

## Controle de versão

Quando você gera imagens personalizadas, GitHub atribui automaticamente números de versão para ajudá-lo a gerenciar atualizações e acompanhar o histórico de imagens.

### Comportamento padrão

Se uma imagem com o nome especificado não existir em sua organização ou empresa, GitHub crie-a com um número de versão inicial de 1.0.0.
Se uma imagem com o mesmo nome já existir, GitHub criará uma nova versão incrementando o número de versão secundária (por exemplo, 1.1.0, 1.2.0 etc.).

Se você não especificar uma versão em seu arquivo YAML, a geração de imagem usará esse comportamento padrão.

### Especificando uma versão em seu fluxo de trabalho

Se você incluir uma versão no mapeamento YAML, GitHub verifique primeiro o número da versão principal.

* Se a versão principal especificada já existir, a nova imagem usará a próxima versão secundária (por exemplo, 1.0 se tornará 1.1).
* Se a versão principal não existir, GitHub criará uma nova versão principal (por exemplo, 2.0).

Não há suporte para versões de patch.

### Última etiqueta

A execução de fluxo de trabalho mais recente para uma imagem é sempre identificada como a última.
Se você especificar uma versão principal mais antiga no YAML (por exemplo, versão: 1.\* quando existe uma versão 2.0), GitHub gerará uma nova versão secundária na versão principal mais antiga e a marcará como mais recente.

> \[!NOTE]
> A criação de Runner maior hospedado no GitHub não dá suporte a curingas na seleção da versão da imagem.

## Expiração para imagens criadas a partir de imagens personalizadas

Quando uma imagem personalizada é criada a partir de outra imagem personalizada, a imagem derivada herda a linha do tempo de expiração de sua imagem base. A idade máxima da versão é calculada de quando a imagem personalizada base foi criada, não quando a imagem derivada foi criada.

Por exemplo, se a Imagem Personalizada A for criada no dia 2 e a Imagem Personalizada B for criada a partir de A no dia 4 com uma política de idade máxima de versão de 7 dias, A e B expirarão no dia 9.

## Cobrança e armazenamento de imagens personalizadas

Trabalhos que usam imagens personalizadas são cobrados na mesma taxa por minuto que o executor avançado que usa a imagem. O armazenamento para imagens personalizadas é cobrado separadamente por meio do armazenamento GitHub Actions.

Se você recompilar imagens com frequência e reter versões mais antigas, o uso do armazenamento poderá crescer rapidamente porque cada trabalho de fluxo de trabalho bem-sucedido que inclui a palavra-chave `snapshot` cria uma nova versão de imagem. Para obter mais informações, consulte [Cobrança do GitHub Actions](https://docs.github.com/pt/billing/concepts/product-billing/github-actions#custom-image-storage) e [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#custom-images-retention-policies).

## Gerenciando imagens personalizadas

Você pode exibir informações detalhadas sobre cada imagem, excluir imagens não utilizados ou versões específicas e acompanhar versões de imagem ao longo do tempo.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-gear" aria-label="gear" role="img"><path d="M8 0a8.2 8.2 0 0 1 .701.031C9.444.095 9.99.645 10.16 1.29l.288 1.107c.018.066.079.158.212.224.231.114.454.243.668.386.123.082.233.09.299.071l1.103-.303c.644-.176 1.392.021 1.82.63.27.385.506.792.704 1.218.315.675.111 1.422-.364 1.891l-.814.806c-.049.048-.098.147-.088.294.016.257.016.515 0 .772-.01.147.038.246.088.294l.814.806c.475.469.679 1.216.364 1.891a7.977 7.977 0 0 1-.704 1.217c-.428.61-1.176.807-1.82.63l-1.102-.302c-.067-.019-.177-.011-.3.071a5.909 5.909 0 0 1-.668.386c-.133.066-.194.158-.211.224l-.29 1.106c-.168.646-.715 1.196-1.458 1.26a8.006 8.006 0 0 1-1.402 0c-.743-.064-1.289-.614-1.458-1.26l-.289-1.106c-.018-.066-.079-.158-.212-.224a5.738 5.738 0 0 1-.668-.386c-.123-.082-.233-.09-.299-.071l-1.103.303c-.644.176-1.392-.021-1.82-.63a8.12 8.12 0 0 1-.704-1.218c-.315-.675-.111-1.422.363-1.891l.815-.806c.05-.048.098-.147.088-.294a6.214 6.214 0 0 1 0-.772c.01-.147-.038-.246-.088-.294l-.815-.806C.635 6.045.431 5.298.746 4.623a7.92 7.92 0 0 1 .704-1.217c.428-.61 1.176-.807 1.82-.63l1.102.302c.067.019.177.011.3-.071.214-.143.437-.272.668-.386.133-.066.194-.158.211-.224l.29-1.106C6.009.645 6.556.095 7.299.03 7.53.01 7.764 0 8 0Zm-.571 1.525c-.036.003-.108.036-.137.146l-.289 1.105c-.147.561-.549.967-.998 1.189-.173.086-.34.183-.5.29-.417.278-.97.423-1.529.27l-1.103-.303c-.109-.03-.175.016-.195.045-.22.312-.412.644-.573.99-.014.031-.021.11.059.19l.815.806c.411.406.562.957.53 1.456a4.709 4.709 0 0 0 0 .582c.032.499-.119 1.05-.53 1.456l-.815.806c-.081.08-.073.159-.059.19.162.346.353.677.573.989.02.03.085.076.195.046l1.102-.303c.56-.153 1.113-.008 1.53.27.161.107.328.204.501.29.447.222.85.629.997 1.189l.289 1.105c.029.109.101.143.137.146a6.6 6.6 0 0 0 1.142 0c.036-.003.108-.036.137-.146l.289-1.105c.147-.561.549-.967.998-1.189.173-.086.34-.183.5-.29.417-.278.97-.423 1.529-.27l1.103.303c.109.029.175-.016.195-.045.22-.313.411-.644.573-.99.014-.031.021-.11-.059-.19l-.815-.806c-.411-.406-.562-.957-.53-1.456a4.709 4.709 0 0 0 0-.582c-.032-.499.119-1.05.53-1.456l.815-.806c.081-.08.073-.159.059-.19a6.464 6.464 0 0 0-.573-.989c-.02-.03-.085-.076-.195-.046l-1.102.303c-.56.153-1.113.008-1.53-.27a4.44 4.44 0 0 0-.501-.29c-.447-.222-.85-.629-.997-1.189l-.289-1.105c-.029-.11-.101-.143-.137-.146a6.6 6.6 0 0 0-1.142 0ZM11 8a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9.5 8a1.5 1.5 0 1 0-3.001.001A1.5 1.5 0 0 0 9.5 8Z"></path></svg> Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-kebab-horizontal" aria-label="More" role="img"><path d="M8 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM1.5 9a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Zm13 0a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path></svg>** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na barra lateral esquerda, clique em **<svg version="1.1" width="16" height="16" viewBox="0 0 16 16" class="octicon octicon-play" aria-label="play" role="img"><path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Zm4.879-2.773 4.264 2.559a.25.25 0 0 1 0 .428l-4.264 2.559A.25.25 0 0 1 6 10.559V5.442a.25.25 0 0 1 .379-.215Z"></path></svg> Ações** e clique em **Imagens personalizadas**.
4. Na página "Imagens personalizadas", você pode exibir todas as imagens personalizadas que foram criadas em sua organização ou empresa.
5. Para exibir detalhes sobre uma imagem específica, clique no nome da imagem.

## Instalando imagens personalizadas

Depois que sua imagem personalizada estiver pronta, você poderá instalá-la em um novo Runner maior hospedado no GitHub.

1. Siga as etapas para criar um executor avançado:
   * Para organizações, consulte [Como adicionar um executor maior a uma organização](manage-larger-runners.md#adding-a-larger-runner-to-an-organization).
   * Para empresas, consulte [Como adicionar um executor maior a uma empresa](manage-larger-runners.md#adding-a-larger-runner-to-an-enterprise).

2. Ao configurar o executor:
   * **Plataforma**: selecione a mesma plataforma usada para gerar a imagem (Linux x64, Linux ARM64 ou Windows x64).
   * **Imagem**: Selecione a guia **Personalizado** e escolha sua imagem personalizada na lista.
     * Se você não vir sua imagem, verifique se selecionou a plataforma correta e se está criando o executor no mesmo nível (organização ou empresa) em que a imagem foi gerada.
   * **Versão da imagem**: escolha **Mais recente** para usar automaticamente a versão mais recente ou selecione um número de versão específico para fixar o executor nessa versão.
     * Se você selecionar **Última Versão**, seu executor será atualizado automaticamente quando uma nova versão da imagem estiver disponível. Se você fixar o executor em uma versão específica, será necessário editar o executor manualmente para atualizar mais tarde.
   * **Tamanho**: escolha um tamanho de runner com armazenamento igual ou maior que o tamanho da sua imagem. Por exemplo, se a imagem foi gerada em um executor de 8 núcleos, selecione um 8 núcleos ou maior para executar essa imagem.
   * **Grupo de executores**: atribua o executor a um grupo de executores compartilhado com os repositórios que precisam usar essa imagem.

3. Em seu trabalho de fluxo de trabalho GitHub Actions, defina a chave `runs-on` para o nome do seu executor.

            ```yaml
   jobs:
     build:
       runs-on: my-custom-runner
       steps:
       # Add any steps for your workflow here
   ```

4. Execute seu fluxo de trabalho para verificar se ele foi concluído com êxito. Os registros de trabalho mostrarão o nome da imagem e a versão na seção "Configuração da tarefa".

## Práticas recomendadas de segurança para imagens personalizadas

Para evitar alterações não autorizadas em suas imagens, siga estas práticas recomendadas.

* **Use grupos de executores dedicados para geração de imagem.** Os executores que geram imagens de produção devem permanecer em um grupo de executores dedicado. Não compartilhe grupos de executores entre repositórios de produção e desenvolvimento ou teste, pois qualquer pessoa com acesso a um repositório de desenvolvimento ou teste pode injetar código mal-intencionado em uma imagem de produção.
* **Não permita que repositórios públicos acessem os executores de geração de imagem.** Limite os repositórios que podem usar os executores de geração de imagem apenas àqueles que realmente o necessitam e revise o acesso regularmente.
* **Aplique privilégios mínimos a repositórios.** Evite conceder acesso a toda a `write` organização para repositórios que têm acesso a executores de geração de imagem. Como as imagens podem ser geradas de qualquer branch, qualquer pessoa com acesso de gravação pode criar um branch com código arbitrário e disparar a geração de imagem.
