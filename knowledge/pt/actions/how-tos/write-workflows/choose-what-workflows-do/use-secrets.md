---
title: Usar segredos em ações do GitHub
description: Aprenda a criar segredos nos níveis de repositório, ambiente e organização para fluxos de trabalho GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
captured: '2026-10-11'
section: How tos / Write workflows / Choose what workflows do
---

# Usar segredos em ações do GitHub { #using-secrets-in-github-actions }

_Aprenda a criar segredos nos níveis de repositório, ambiente e organização para fluxos de trabalho GitHub Actions._

## Como criar segredos para um repositório { #creating-secrets-for-a-repository }

Para criar segredos ou variáveis em GitHub para um repositório de organização, você deve ter `write` acesso. Para um repositório de conta pessoal, você deve ser um colaborador do repositório.

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na seção "Security" da barra lateral, selecione **(key-asterisk) Secrets and variables** e clique em **Actions**.
4. Clique na guia **Segredos**.

![Captura de tela da página "Segredos e variáveis das ações". A guia "Segredos" está delimitada em laranja escuro.](/assets/images/help/repository/actions-secrets-tab.png)

1. Clique em **Novo segredo de repositório**.
2. No campo **Nome**, digite um nome para o segredo.
3. No campo **Segredo**, insira o valor do segredo.
4. Clique em **Adicionar segredo**.

Se o seu repositório tiver segredos de ambiente ou puder acessar segredos da organização principal, esses segredos também serão listados nesta página.

Para adicionar um segredo do repositório, use o subcomando `gh secret set`. Substitua `secret-name` pelo nome do segredo.

```shell
gh secret set SECRET_NAME
```

A CLI solicitará que você digite o valor de um segredo. Como alternativa, você pode ler o valor do segredo a partir de um arquivo.

```shell
gh secret set SECRET_NAME < secret.txt
```

Para listar todos os segredos do repositório, use o subcomando `gh secret list`.

## Criação de segredos para um ambiente { #creating-secrets-for-an-environment }

Para criar segredos ou variáveis para um ambiente em um repositório de conta pessoal, você deve ser o proprietário do repositório. Para criar segredos ou variáveis para um ambiente em um repositório de uma organização, é necessário ter acesso `admin`. Para saber mais sobre os ambientes, confira [Gerenciar ambientes para implantação](../../deploy/configure-and-manage-deployments/manage-environments.md).

1. Em GitHub, acesse a página principal do repositório.
2. No nome do repositório, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela de um cabeçalho de repositório que mostra as guias. A guia "Configurações" é realçada por um contorno laranja-escuro.](/assets/images/help/repository/repo-actions-settings.png)
3. Na barra lateral esquerda, clique em **Ambientes**.
4. Clique no ambiente ao qual você deseja adicionar um segredo.
5. Em **Segredos do ambiente**, clique em **Adicionar segredo**.
6. Digite um nome para o segredo na caixa de entrada **Nome**.
7. Digite o valor para sua chave secreta.
8. Clique em **Adicionar segredo**.

Para adicionar um segredo a um ambiente, use o subcomando `gh secret set` com o sinalizador `--env` ou `-e` seguido do nome do ambiente.

```shell
gh secret set --env ENV_NAME SECRET_NAME
```

Para listar todos os segredos de um ambiente, use o subcomando `gh secret list` com o sinalizador `--env` ou `-e` seguido do nome do ambiente.

```shell
gh secret list --env ENV_NAME
```

## Criando segredos para uma organização { #creating-secrets-for-an-organization }

!!! note
    Os segredos e variáveis no nível da organização não são acessíveis por repositórios privados para GitHub Free. Para obter mais informações sobre como atualizar sua GitHub assinatura, consulte [Atualizando o plano da sua conta](https://docs.github.com/pt/billing/how-tos/manage-plan-and-licenses/upgrade-plan).

Ao criar um segredo ou uma variável em uma organização, você poderá usar uma política para limitar o acesso por repositório. Por exemplo, você pode conceder acesso a todos os repositórios ou limitar o acesso a apenas repositórios privados ou a uma lista específica de repositórios.

Os proprietários "Gerenciar variáveis de ações da organização" ou "Gerenciar segredos de ações da organização" podem criar segredos ou variáveis no nível da organização.

1. Em GitHub, acesse a página principal da organização.

2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)

3. Na seção "Security" da barra lateral, selecione **(key-asterisk) Secrets and variables** e clique em **Actions**.

4. Clique na guia **Segredos**.

   ![Captura de tela da página "Segredos e variáveis das ações". A guia "Segredos" está contornada em laranja escuro.](/assets/images/help/repository/actions-secrets-tab.png)

5. Clique em **Novo segredo da organização**.

6. Digite um nome para o segredo na caixa de entrada **Nome**.

7. Insira o **Valor** do segredo.

8. Na lista suspensa **Acesso do repositório**, escolha uma política de acesso.

9. Clique em **Adicionar segredo**.

!!! note
    Por padrão, GitHub CLI autentica com os escopos `repo` e `read:org`. Para gerenciar os segredos da organização, você também precisa autorizar o escopo `admin:org`.

                ```shell
    gh auth login --scopes "admin:org"
    ```

Para adicionar um segredo a uma organização, use o subcomando `gh secret set` com o sinalizador `--org` ou `-o` seguido do nome da organização.

```shell
gh secret set --org ORG_NAME SECRET_NAME
```

Por padrão, o segredo só está disponível para repositórios privados. Para especificar que o segredo deve estar disponível para todos os repositórios na organização, use o sinalizador `--visibility` ou `-v`.

```shell
gh secret set --org ORG_NAME SECRET_NAME --visibility all
```

Para especificar que o segredo deve estar disponível para repositórios selecionados na organização, use o sinalizador `--repos` ou `-r`.

```shell
gh secret set --org ORG_NAME SECRET_NAME --repos REPO-NAME-1, REPO-NAME-2
```

Para listar todos os segredos de uma organização, use o subcomando `gh secret list` com o sinalizador `--org` ou `-o` seguido do nome da organização.

```shell
gh secret list --org ORG_NAME
```

## Revisão do acesso aos segredos a nível organizacional { #reviewing-access-to-organization-level-secrets }

Você pode verificar quais políticas de acesso são aplicadas a um segredo na sua organização.

1. Em GitHub, acesse a página principal da organização.
2. No nome da organização, clique em **(gear) Settings**. Caso não consiga ver a guia "Configurações", selecione o menu suspenso **(More)** , clique em **Configurações**.

   ![Captura de tela das guias no perfil de uma organização. A guia "Configurações" está contornada em laranja escuro.](/assets/images/help/discussions/org-settings-global-nav-update.png)
3. Na seção "Security" da barra lateral, selecione **(key-asterisk) Secrets and variables** e clique em **Actions**.
4. A lista de segredos inclui quaisquer permissões e políticas configuradas. Para obter mais detalhes sobre as permissões configuradas para cada segredo, clique em **Atualizar**.

## Usar segredos em um fluxo de trabalho { #using-secrets-in-a-workflow }

!!! note
    * Com exceção do `GITHUB_TOKEN`, os segredos não são transmitidos para o executor quando um fluxo de trabalho é disparado de um repositório com fork.
    * Os segredos não são passados automaticamente para fluxos de trabalho reutilizáveis. Para saber mais, confira [Reutilizar fluxos de trabalho](../../reuse-automations/reuse-workflows.md#passing-inputs-and-secrets-to-a-reusable-workflow).
    * Os segredos não estão disponíveis para fluxos de trabalho ativados por Dependabot eventos. Para saber mais, confira [Solução de problemas do Dependabot no GitHub Actions](https://docs.github.com/pt/code-security/reference/supply-chain-security/troubleshoot-dependabot/dependabot-on-actions#accessing-secrets).
    * Se seus GitHub Actions fluxos de trabalho precisarem acessar recursos de um provedor de nuvem que dê suporte ao OpenID Connect (OIDC), você poderá configurar seus fluxos de trabalho para autenticar diretamente no provedor de nuvem. Isso permitirá que você pare de armazenar essas credenciais como segredos de longa duração e proporcione outros benefícios de segurança. Para saber mais, confira [OpenID Connect](../../../concepts/security/openid-connect.md).

    [!WARNING] Mascarar todas as informações confidenciais que não são um GitHub segredo usando `::add-mask::VALUE`. Isso faz com que o valor seja tratado como um segredo e ocultado dos logs.

Para fornecer uma ação com um segredo como uma entrada ou uma variável de ambiente, use o contexto `secrets` para acessar os segredos criados no seu repositório. Para saber mais, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md) e [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md).

```yaml
steps:
  - name: Hello world action
    with: # Set the secret as an input
      super_secret: ${{ secrets.SuperSecret }}
    env: # Or as an environment variable
      super_secret: ${{ secrets.SuperSecret }}
```

Não é possível referenciar segredos diretamente em condicionais `if:`. Em vez disso, considere definir segredos como variáveis de ambiente no nível de trabalho e, em seguida, fazer referência às variáveis de ambiente para executar etapas condicionalmente no trabalho. Para obter mais informações, confira [Referência de contextos](../../../reference/workflows-and-actions/contexts.md#context-availability) e [`jobs.<job_id>.steps[*].if`](/pt/actions/reference/workflows-and-actions/workflow-syntax#jobsjob_idstepsif).

Se um segredo não tiver sido definido, o valor retornado de uma expressão referenciando o segredo (como `${{ secrets.SuperSecret }}` no exemplo) será uma cadeia de caracteres vazia.

Evite a transmissão de segredos entre processos da linha de comando sempre que possível. Os processos de linha de comando podem estar visíveis para outros usuários (por meio do comando `ps`) ou ser capturados por [eventos de auditoria de segurança](https://docs.microsoft.com/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing). Para ajudar a proteger os segredos, considere o uso de variáveis de ambiente, `STDIN` ou outros mecanismos compatíveis com o processo de destino.

Se você passar segredos dentro de uma linha de comando, inclua-os dentro das regras de aspas corretas. Muitas vezes, os segredos contêm caracteres especiais que não intencionalmente podem afetar o seu shell. Para escapar desses caracteres especiais, use aspas com suas variáveis de ambiente. Por exemplo:

### Exemplo de uso do Bash { #example-using-bash }

```yaml
steps:
  - shell: bash
    env:
      SUPER_SECRET: ${{ secrets.SuperSecret }}
    run: |
      example-command "$SUPER_SECRET"
```

### Exemplo de uso do PowerShell { #example-using-powershell }

```yaml
steps:
  - shell: pwsh
    env:
      SUPER_SECRET: ${{ secrets.SuperSecret }}
    run: |
      example-command "$env:SUPER_SECRET"
```

### Exemplo de uso do Cmd.exe { #example-using-cmdexe }

```yaml
steps:
  - shell: cmd
    env:
      SUPER_SECRET: ${{ secrets.SuperSecret }}
    run: |
      example-command "%SUPER_SECRET%"
```

## Armazenamento de grandes segredos { #storing-large-secrets }

Para usar segredos maiores que 48 KB, você pode usar uma solução alternativa para armazenar segredos em seu repositório e salvar a frase secreta de descriptografia em GitHub. Por exemplo, você pode usar `gpg` para criptografar um arquivo que contém seu segredo localmente antes de verificar o arquivo criptografado no repositório.GitHub Para obter mais informações, confira a [Página do manual do GPG](https://www.gnupg.org/gph/de/manual/r1023.html).

!!! warning
    Certifique-se de que seus segredos não sejam impressos quando o fluxo de trabalho estiver em execução. Ao usar essa solução alternativa, GitHub não mascara os segredos que são registrados em logs.

1. Execute o comando a seguir no terminal para criptografar o arquivo que contém o segredo usando `gpg` e o algoritmo de criptografia AES256. Neste exemplo, `my_secret.json` é o arquivo que contém o segredo.

            ```shell
   gpg --symmetric --cipher-algo AES256 my_secret.json
   ```

2. Você receberá a solicitação para inserir a frase secreta. Lembre-se da frase secreta, pois você precisará criar um novo segredo em GitHub que utilize a frase secreta como valor.

3. Criar um novo segredo que contém a frase secreta. Por exemplo, crie um segredo com o nome `LARGE_SECRET_PASSPHRASE` e defina o valor do segredo como a frase secreta usada na etapa acima.

4. Copie o arquivo criptografado para um caminho no repositório e faça commit. Neste exemplo, o arquivo criptografado é `my_secret.json.gpg`.

!!! warning

   > Copie o arquivo `my_secret.json.gpg` criptografado que termina com a extensão de arquivo `.gpg` e não o arquivo \*\*\*\* não criptografado.

            ```shell
   git add my_secret.json.gpg
   git commit -m "Add new secret JSON file"
   ```

5. Crie um shell script no seu repositório para descriptografar o arquivo secreto. Neste exemplo, o script se chama `decrypt_secret.sh`.

            ```shell copy
   #!/bin/sh

   # Decrypt the file
   mkdir $HOME/secrets
   # --batch to prevent interactive command
   # --yes to assume "yes" for questions
   gpg --quiet --batch --yes --decrypt --passphrase="$LARGE_SECRET_PASSPHRASE" \
   --output $HOME/secrets/my_secret.json my_secret.json.gpg
   ```

6. Confirme que o shell script é executável antes de colocá-lo no repositório.

            ```shell
   chmod +x decrypt_secret.sh
   git add decrypt_secret.sh
   git commit -m "Add new decryption script"
   git push
   ```

7. Em sua GitHub Actions rotina de trabalho, use um `step` para chamar o script shell e decodificar a chave secreta. Para ter uma cópia do repositório no ambiente em que o fluxo de trabalho é executado, você precisará usar a ação [`actions/checkout`](https://github.com/actions/checkout). Referencie o script do shell usando o comando `run` relativo à raiz do repositório.

            ```yaml
   name: Workflows with large secrets

   on: push

   jobs:
     my-job:
       name: My Job
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v6
         - name: Decrypt large secret
           run: ./decrypt_secret.sh
           env:
             LARGE_SECRET_PASSPHRASE: ${{ secrets.LARGE_SECRET_PASSPHRASE }}
         # This command is just an example to show your secret being printed
         # Ensure you remove any print statements of your secrets. GitHub does
         # not hide secrets that use this workaround.
         - name: Test printing your secret (Remove this step in production)
           run: cat $HOME/secrets/my_secret.json
   ```

## Armazenamento de blobs binários em Base64 como segredos { #storing-base64-binary-blobs-as-secrets }

Você pode usar a codificação de Base64 para armazenar pequenos blobs binários como segredos. Em seguida, você pode referenciar o segredo em seu fluxo de trabalho e decodificá-lo para uso no runner. Para ver os limites de tamanho, confira [Referência de segredos](../../../reference/security/secrets.md#limits-for-secrets).

!!! note
    * Observe que o Base64 converte apenas binário em texto e não substitui a criptografia real.
    * O uso de outro shell pode exigir comandos diferentes para decodificar o segredo em um arquivo. Em executores do Windows, recomendamos [usar um shell do bash](../../../reference/workflows-and-actions/workflow-syntax.md#jobsjob_idstepsshell) com `shell: bash` para usar os comandos na etapa `run` acima.

1. Use `base64` para codificar seu arquivo em uma cadeia de caracteres Base64. Por exemplo:

   No macOS, você pode executar:

            ```shell
   base64 -i cert.der -o cert.base64
   ```

   No Linux, você pode executar:

            ```shell
   base64 -w 0 cert.der > cert.base64
   ```

2. Crie um segredo que contenha a string de Base64. Por exemplo:

            ```shell
   $ gh secret set CERTIFICATE_BASE64 < cert.base64
   ✓ Set secret CERTIFICATE_BASE64 for octocat/octorepo
   ```

3. Para acessar a string Base64 por meio do runner, encaminhe o segredo para `base64 --decode`. Por exemplo:

            ```yaml
   name: Retrieve Base64 secret
   on:
     push:
       branches: [ octo-branch ]
   jobs:
     decode-secret:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v6
         - name: Retrieve the secret and decode it to a file
           env:
             CERTIFICATE_BASE64: ${{ secrets.CERTIFICATE_BASE64 }}
           run: |
             echo $CERTIFICATE_BASE64 | base64 --decode > cert.der
         - name: Show certificate information
           run: |
             openssl x509 -in cert.der -inform DER -text -noout
   ```

## Próximas etapas { #next-steps }

Para obter informações de referência, confira [Referência de segredos](../../../reference/security/secrets.md).
