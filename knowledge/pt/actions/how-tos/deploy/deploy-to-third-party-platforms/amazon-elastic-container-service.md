---
title: Implantar no Amazon Elastic Container Service
description: Saiba como implantar um projeto no Amazon Elastic Container Service (ECS) como parte de um fluxo de trabalho de CD (implantação contínua).
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/amazon-elastic-container-service
captured: '2026-10-11'
section: How tos / Deploy / Deploy to third party platforms
---

# Implantar no Amazon Elastic Container Service

_Saiba como implantar um projeto no Amazon Elastic Container Service (ECS) como parte de um fluxo de trabalho de CD (implantação contínua)._

## Pré-requisitos

Antes de criar seu GitHub Actions fluxo de trabalho, primeiro você precisará concluir as seguintes etapas de configuração para Amazon ECR e ECS:

1. Crie um repositório Amazon ECR para armazenar suas imagens.

   Por exemplo, usando [a CLI da AWS](https://aws.amazon.com/cli/):

            ```bash copy
   aws ecr create-repository \
       --repository-name MY_ECR_REPOSITORY \
       --region MY_AWS_REGION

   ```

   Certifique-se de usar o mesmo nome de repositório do Amazon ECR (representado aqui por `MY_ECR_REPOSITORY`) para a variável `ECR_REPOSITORY` no fluxo de trabalho abaixo.

   Certifique-se de usar o mesmo valor de região da AWS para a variável `AWS_REGION` (representada aqui por `MY_AWS_REGION`) no fluxo de trabalho abaixo.

2. Crie uma definição de tarefa, um cluster e um serviço do Amazon ECS.

   Para obter detalhes, siga o [Assistente de introdução no console do Amazon ECS](https://us-east-2.console.aws.amazon.com/ecs/home?region=us-east-2#/firstRun) ou o [Guia de introdução](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html) na documentação do Amazon ECS.

   Certifique-se de anotar os nomes que você definiu para o serviço e o cluster do Amazon ECS e use-os para as variáveis `ECS_SERVICE` e `ECS_CLUSTER` no fluxo de trabalho abaixo.

3. Armazene sua definição de tarefa do Amazon ECS como um arquivo JSON em seu GitHub repositório.

   O formato do arquivo deve ser o mesmo da saída gerada por:

            ```bash copy

   aws ecs register-task-definition --generate-cli-skeleton

   ```

   Certifique-se de que você definiu a variável `ECS_TASK_DEFINITION` no fluxo de trabalho abaixo como o caminho para o arquivo JSON.

   Certifique-se de definir a variável `CONTAINER_NAME` no fluxo de trabalho abaixo como o nome do contêiner na seção `containerDefinitions` da definição da tarefa.

4. Crie GitHub Actions segredos nomeados `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` para armazenar os valores da sua chave de acesso do Amazon IAM.

   Para obter mais informações sobre como criar segredos para GitHub Actions, consulte [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md#creating-secrets-for-a-repository).

   Consulte a documentação de cada ação usada abaixo para obter as políticas do IAM recomendadas para o usuário do IAM e os métodos para lidar com as credenciais de chave de acesso.

5. Opcionalmente, configure um ambiente de implantação. Os ambientes são usados para descrever um destino de implantação geral, como `production`, `staging` ou `development`. Quando um GitHub Actions fluxo de trabalho é implantado em um ambiente, o ambiente é exibido na página principal do repositório. Você pode usar ambientes para exigir aprovação para um trabalho prosseguir, restringir quais ramificações podem acionar um fluxo de trabalho, bloquear implantações com regras de proteção de implantação personalizadas ou limitar o acesso a segredos. Para saber mais sobre como criar ambientes, confira [Gerenciar ambientes para implantação](../configure-and-manage-deployments/manage-environments.md).

## Criar o fluxo de trabalho

Depois de preencher os pré-requisitos, você pode prosseguir com a criação do fluxo de trabalho.

O fluxo de trabalho de exemplo a seguir demonstra como criar uma imagem de contêiner e enviá-la ao Amazon ECR. Em seguida, ele atualiza a definição de tarefa com a nova ID de imagem e implanta a definição da tarefa no Amazon ECS.

Certifique-se de fornecer seus próprios valores para todas as variáveis na chave `env` do fluxo de trabalho.

Se você configurou um ambiente de implantação, altere o valor de `environment` para que ele seja o nome do seu ambiente. Se você não tiver configurado um ambiente ou se o fluxo de trabalho estiver em um repositório privado e você não usar o GitHub Enterprise Cloud, exclua a chave `environment`.

```yaml copy
# Esse fluxo de trabalho usa ações que não são certificadas pelo GitHub.
# São fornecidas por terceiros e regidas por
# termos de serviço, política de privacidade e suporte separados
# online.

# O GitHub recomenda fixar ações em um SHA de commit.
# Para obter uma versão mais recente, você precisará atualizar o SHA.
# Você também pode fazer referência a uma marca ou branch, mas a ação pode ser alterada sem aviso.

name: Deploy to Amazon ECS

on:
  push:
    branches:
      - main

env:
  AWS_REGION: MY_AWS_REGION                   # set this to your preferred AWS region, e.g. us-west-1
  ECR_REPOSITORY: MY_ECR_REPOSITORY           # set this to your Amazon ECR repository name
  ECS_SERVICE: MY_ECS_SERVICE                 # set this to your Amazon ECS service name
  ECS_CLUSTER: MY_ECS_CLUSTER                 # set this to your Amazon ECS cluster name
  ECS_TASK_DEFINITION: MY_ECS_TASK_DEFINITION # set this to the path to your Amazon ECS task definition
                                               # file, e.g. .aws/task-definition.json
  CONTAINER_NAME: MY_CONTAINER_NAME           # set this to the name of the container in the
                                               # containerDefinitions section of your task definition

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@0e613a0980cbf65ed5b322eb7a1e075d28913a83
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@62f4f872db3836360b72999f4b87f1ff13310f3a

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          # Build a docker container and
          # push it to ECR so that it can
          # be deployed to ECS.
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@c804dfbdd57f713b6c079302a4c01db7017a36fc
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@df9643053eda01f169e64a0e60233aacca83799a
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

## Leitura adicional

Para o modelo de fluxo de trabalho original, consulte [`aws.yml`](https://github.com/actions/starter-workflows/blob/main/deployments/aws.yml) no GitHub Actions`starter-workflows` repositório.

Para mais informações sobre os serviços utilizados nestes exemplos, veja a seguinte documentação:

* [Melhores práticas de segurança no IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) na documentação da Amazon AWS.
* Ação oficial [Configurar credenciais da AWS](https://github.com/aws-actions/configure-aws-credentials).
* Ação oficial ["Logon" no Amazon ECR](https://github.com/aws-actions/amazon-ecr-login) da AWS.
* Ação oficial ["Renderizar Definição de Tarefa" do Amazon ECS](https://github.com/aws-actions/amazon-ecs-render-task-definition) da AWS.
* Ação oficial ["Implantar Definição de Tarefa" do Amazon ECS](https://github.com/aws-actions/amazon-ecs-deploy-task-definition) da AWS.
