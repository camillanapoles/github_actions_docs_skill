---
title: Referência do cache de dependência
description: Encontre informações sobre a funcionalidade do cache de dependência em fluxos de trabalho.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/dependency-caching
captured: '2026-10-13'
section: Reference / Workflows and actions
---

# Referência do cache de dependência

_Encontre informações sobre a funcionalidade do cache de dependência em fluxos de trabalho._

## Uso de ações do `cache`

A [`cache` ação](https://github.com/actions/cache) tentará a seguinte sequência ao restaurar um cache:

1. Primeiro, ela pesquisa por uma correspondência exata com o `key`fornecido.
2. Se nenhuma correspondência exata for encontrada, ela pesquisará por correspondências parciais de `key`.
3. Se ainda não houver correspondência e você tiver fornecido `restore-keys`, essas chaves serão verificadas sequencialmente em busca de correspondências parciais. Para obter mais informações, confira [Correspondência de chave de cache](#cache-key-matching).

Se houver uma correspondência exata com o `key` fornecido, isso será considerado uma ocorrência no cache. Se nenhum cache corresponder exatamente ao `key` fornecido, isso é considerado uma perda no cache. Em uma perda no cache, a ação cria automaticamente um cache quando o trabalho é concluído com sucesso. O novo cache usará a `key` fornecida e conterá os arquivos especificados no `path`. Para saber como isso é feito, confira [Ocorrências e perdas no cache](#cache-hits-and-misses).

Não é possível alterar o conteúdo de um cache existente. Em vez disso, crie um cache com uma nova chave.

### Os parâmetros de entrada da ação `cache`

* `key`: **Obrigatório** A chave criada ao salvar um cache, e a chave usada para pesquisar um cache. Pode ser qualquer combinação de variáveis, valores de contexto, cadeias de caracteres estáticas e funções. As chaves têm um tamanho máximo de 512 caracteres e as chaves maiores que o tamanho máximo gerarão uma falha na ação.

* `path`: **Obrigatório** Os caminhos no executor para armazenamento em cache ou restauração.
  * Você pode especificar um só caminho ou adicionar vários caminhos em linhas separadas. Por exemplo:

                ```yaml
    - name: Cache Gradle packages
      uses: actions/cache@v4
      with:
        path: |
          ~/.gradle/caches
          ~/.gradle/wrapper
    ```

  * Você pode especificar diretórios ou arquivos únicos e os padrões glob são compatíveis.

  * Você pode especificar caminhos absolutos ou caminhos relativos ao diretório do espaço de trabalho.

* `restore-keys`: **Opcional** Uma cadeia de caracteres que contém chaves de restauração alternativas, com cada chave de restauração colocada em uma nova linha. Se não houver nenhuma ocorrência da `key`no cache, essas chaves de restauração serão usadas sequencialmente na ordem fornecida para localizar e restaurar um cache. Por exemplo:

        ```yaml
  restore-keys: |
    npm-feature-${{ hashFiles('package-lock.json') }}
    npm-feature-
    npm-
  ```

* `enableCrossOsArchive`: **Optional** Um valor booliano que, quando habilitado, permite que Windows executores salvem ou restaurem caches independentemente do sistema operacional em que o cache foi criado. Se esse parâmetro não estiver definido, ele usará como padrão `false`. Para obter mais informações, confira [Cache entre sistemas operacionais](https://github.com/actions/cache/blob/main/tips-and-workarounds.md#cross-os-cache) na documentação do Actions Cache.

!!! note
    Recomendamos que você não armazene informações confidenciais, como tokens de acesso ou credenciais de logon, em arquivos no caminho do cache. Qualquer pessoa com acesso de leitura pode criar uma solicitação de pull em um repositório e acessar o conteúdo de um cache. Além disso, os forks de um repositório podem criar pull requests no branch-base e acessar as caches no branch-base.

### Parâmetros de saída para a ação `cache`

* `cache-hit`: um valor booliano para indicar que uma correspondência exata foi encontrada para a chave.

### Ocorrências e perdas no cache

Quando `key` corresponde exatamente a um cache existente, isso é chamado de *ocorrência no cache* e a ação restaura os arquivos em cache no diretório `path`.

Quando `key` não corresponde a um cache existente, isso é chamado de *perda no cache* e um cache é criado automaticamente se o trabalho for concluído com sucesso.

Quando ocorre uma perda no cache, a ação também pesquisa o `restore-keys` especificado para encontrar correspondências:

1. Se você fornecer `restore-keys`, a ação `cache` vai procurar sequencialmente os caches que correspondem à lista de `restore-keys`.
   * Se houver uma correspondência exata, a ação vai restaurar os arquivos no cache no diretório `path`.
   * Se não houver correspondências exatas, a ação pesquisará correspondências parciais das chaves de restauração. Quando uma ação encontra uma correspondência parcial, o último cache é restaurado no diretório `path`.
2. A ação `cache` é concluída e a próxima etapa é executada no trabalho.
3. Se o trabalho for concluído com sucesso, a ação criará automaticamente um cache com o conteúdo do diretório `path`.

Para obter uma explicação mais detalhada do processo de correspondência de cache, consulte [Correspondência de chave de cache](#cache-key-matching).

### Exemplo que usa a ação `cache`

Este exemplo cria um cache quando os pacotes do arquivo `package-lock.json` são alterados ou quando o sistema operacional do executor é alterado. A chave de cache usa contextos e expressões para gerar uma chave que inclui o sistema operacional do executor e um hash SHA-256 do arquivo `package-lock.json`.

```yaml copy
name: Caching with npm
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - name: Cache node modules
        id: cache-npm
        uses: actions/cache@v4
        env:
          cache-name: cache-node-modules
        with:
          # npm cache files are stored in `~/.npm` on Linux/macOS
          path: ~/.npm
          key: ${{ runner.os }}-build-${{ env.cache-name }}-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-build-${{ env.cache-name }}-
            ${{ runner.os }}-build-
            ${{ runner.os }}-

      - if: ${{ steps.cache-npm.outputs.cache-hit != 'true' }}
        name: List the state of node modules
        continue-on-error: true
        run: npm list

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Test
        run: npm test
```

### Usar contextos para criar chaves da cache

Uma chave de cache pode incluir qualquer um entre os contextos, as funções, os literais e os operadores compatíveis com GitHub Actions. Para saber mais, confira [Referência de contextos](contexts.md) e [Avaliar expressões em fluxos de trabalho e ações](expressions.md).

O uso de expressões para criar uma `key` permite que você crie automaticamente um cache quando as dependências são alteradas.

Por exemplo, você pode criar uma `key` usando uma expressão que calcula o hash de um arquivo `package-lock.json` npm. Portanto, quando as dependências que compõem o arquivo `package-lock.json` são alteradas, a chave de cache é alterada e um novo cache é criado automaticamente.

```yaml
npm-${{ hashFiles('package-lock.json') }}
```

GitHub avalia a expressão `hash "package-lock.json"` para derivar o final `key`.

```yaml
npm-d5ea0750
```

### Usando a saída da ação `cache`

Você pode usar a saída da ação `cache` para fazer algo com base na ocorrência ou na perda no cache. Quando uma correspondência exata é encontrada para um cache do `key` especificado, a saída `cache-hit` é definida como `true`.

No exemplo de fluxo de trabalho acima, há uma etapa que lista o estado dos módulos de nó na ocorrência de uma perda no cache:

```yaml
- if: ${{ steps.cache-npm.outputs.cache-hit != 'true' }}
  name: List the state of node modules
  continue-on-error: true
  run: npm list
```

## Correspondência de chave de cache

A ação `cache` primeiro pesquisa ocorrências de `key` no cache e a *versão* do cache no branch que contém a execução de fluxo de trabalho. Se não houver nenhum resultado, ela pesquisará por correspondências de prefixo para `key` e, se ainda não houver resultado, pesquisará por `restore-keys` e pela *versão*. Se ainda não houver resultados no branch atual, a ação `cache` repetirá as mesmas etapas no branch padrão. Observe que as restrições de escopo se aplicam durante a pesquisa. Para saber mais, confira [Restrições de acesso a um cache](#restrictions-for-accessing-a-cache).

A versão do cache é uma maneira de marcar um cache com metadados de `path` e a ferramenta de compactação usada durante a criação dele. Isso garante que a execução de fluxo de trabalho de consumo corresponda exclusivamente a um cache que possa realmente descompactar e usar. Para saber mais, confira [Versão de cache](https://github.com/actions/cache#cache-version) na documentação do cache de ações.

O `restore-keys` permite que você especifique uma lista de chaves de restauração alternativas a serem usadas quando houver uma perda no cache na `key`. Você pode criar múltiplas chaves de restauração ordenadas da mais específica para a menos específica. A ação `cache` procura o `restore-keys` em ordem sequencial. Quando uma chave não corresponde diretamente, a ação pesquisa as chaves prefixadas com a chave de restauração. Se houver múltiplas correspondências parciais para uma chave de restauração, a ação retornará a cache criada por último.

### Exemplo do uso de múltiplas chaves de restauração

```yaml
restore-keys: |
  npm-feature-${{ hashFiles('package-lock.json') }}
  npm-feature-
  npm-
```

O executor avalia as expressões, que são resolvidas para estas `restore-keys`:

```yaml
restore-keys: |
  npm-feature-d5ea0750
  npm-feature-
  npm-
```

A chave de restauração `npm-feature-` corresponde a qualquer chave que comece com a cadeia de caracteres `npm-feature-`. Por exemplo, as chaves `npm-feature-fd3052de` e `npm-feature-a9b253ff` correspondem à chave de restauração. Será usada a cache com a data de criação mais recente. As chaves neste exemplo são pesquisadas na ordem a seguir:

1. \*\*
   `npm-feature-d5ea0750`
   \*\* corresponde a um hash específico.
2. \*\*
   `npm-feature-`
   \*\* corresponde às chaves de cache precedidas com `npm-feature-`.
3. \*\*
   `npm-`
   \*\* corresponde a qualquer chave precedida com `npm-`.

#### Exemplo de prioridade de pesquisa

```yaml
key:
  npm-feature-d5ea0750
restore-keys: |
  npm-feature-
  npm-
```

Por exemplo, se uma solicitação de pull contiver um branch `feature` e for direcionada ao branch padrão (`main`), a ação vai procurar `key` e `restore-keys` na seguinte ordem:

1. Chave `npm-feature-d5ea0750` no branch `feature`
2. Chave `npm-feature-` no branch `feature`
3. Chave `npm-` no branch `feature`
4. Chave `npm-feature-d5ea0750` no branch `main`
5. Chave `npm-feature-` no branch `main`
6. Chave `npm-` no branch `main`

## Ações de `setup-*` para gerenciadores de pacotes específicos

Se você estiver armazenando em cache os gerenciadores de pacotes listados abaixo, o uso das respectivas ações setup-\* exigirá configuração mínima e criará e restaurará caches de dependência para você.

| Gerenciadores de pacotes | ação setup-\* para cache |
| --- | --- |
| npm, YARN, pnpm |  |
| [setup-node](https://github.com/actions/setup-node#caching-global-packages-data) |  |
| pip, pipenv, Poesia |  |
| [setup-python](https://github.com/actions/setup-python#caching-packages-dependencies) |  |
| Gradle, Maven |  |
| [setup-java](https://github.com/actions/setup-java#caching-packages-dependencies) |  |
| RubyGems |  |
| [setup-ruby](https://github.com/ruby/setup-ruby#caching-bundle-install-automatically) |  |
| Ir `go.sum` |  |
| [setup-go](https://github.com/actions/setup-go#caching-dependency-files-and-build-outputs) |  |
| NuGet para .NET |  |
| [setup-dotnet](https://github.com/actions/setup-dotnet?tab=readme-ov-file#caching-nuget-packages) |  |

## Restrições para acessar uma cache

As restrições de acesso fornecem o isolamento da cache e a segurança ao criar um limite lógico entre os diferentes branches ou marcas.
As execuções de fluxo de trabalho podem restaurar caches criados no branch atual ou no branch padrão (geralmente `main`). Se uma execução de fluxo de trabalho for disparada para uma solicitação de pull, ela também poderá restaurar caches criados no branch base, incluindo branches base de repositórios com fork. Por exemplo, se o branch `feature-b` tiver o branch base `feature-a`, uma execução de fluxo de trabalho disparada em uma solicitação de pull terá acesso aos caches criados no branch `main` padrão, no branch `feature-a` base e no branch `feature-b` atual.

As execuções de fluxo de trabalho não podem restaurar caches criados para ramificações filhos ou irmãos. Por exemplo, um cache criado para o branch `feature-b` filho não estaria acessível a uma execução de fluxo de trabalho disparada no branch `main` pai. Da mesma forma, um cache criado para o branch `feature-a` com o `main` base não seria acessível ao branch `feature-c` irmão com o `main` base. As execuções de fluxo de trabalho também não podem restaurar caches criados para nomes de marcas diferentes. Por exemplo, um cache criado para a marca `release-a` com o `main` base não seria acessível a uma execução de fluxo de trabalho disparada para a marca `release-b` com o `main` base.

Quando um cache é criado por uma execução de fluxo de trabalho disparada em uma solicitação de pull, ele é criado para a referência de mesclagem (`refs/pull/.../merge`). Por isso, ele terá um escopo limitado e só poderá ser restaurado por novas execuções da solicitação de pull. Ele não poderá ser restaurado pelo branch base ou por outras solicitações de pull direcionadas a esse branch.

Diversas execuções de fluxo de trabalho em um repositório podem compartilhar caches. Um cache criado para um branch em uma execução de fluxo de trabalho pode ser acessado e restaurado por meio de outra execução de fluxo de trabalho para o mesmo repositório e branch.

## Acesso ao cache para gatilhos de fluxo de trabalho de baixa confiança

Alguns fluxos de trabalho são executados em resposta a eventos que podem ser iniciados por pessoas que não têm acesso de gravação ao repositório, como uma solicitação de pull de bifurcação ou um comentário de problema. Quando esses eventos são executados no contexto do ramo padrão, eles podem ser usados para gravar um cache malicioso que um fluxo de trabalho posterior, com mais privilégios, restaura e considera confiável. Essa classe de ataque é conhecida como *envenenamento por cache*.

Para reduzir esse risco, apenas os seguintes gatilhos de fluxo de trabalho podem criar ou sobrescrever caches no escopo do branch padrão:

* `push`
* `workflow_dispatch`
* `repository_dispatch`
* `delete`
* `registry_package`
* `page_build`
* `schedule`

As execuções acionadas por qualquer outro evento que resulte na branch padrão recebem acesso somente de leitura aos caches no escopo da branch padrão. Essas execuções podem restaurar caches existentes, mas não podem criá-los ou substituí-los. Isso inclui gatilhos cujo conteúdo ou ator iniciador pode ser influenciado por alguém fora do repositório, como `pull_request_target`, `issue_comment`e `workflow_run`. Um repositório pode não aderir a essa restrição para um fluxo de trabalho ou trabalho específico declarando explicitamente um(a) `cache-mode` com permissão de gravação. Consulte [Ignorar a restrição de cache de gatilho não confiável padrão](#bypassing-the-default-untrusted-trigger-cache-restriction).

O evento `pull_request` não é afetado. Os caches criados por uma execução de `pull_request` já estão no escopo do ref de merge (`refs/pull/.../merge`) e não podem ser gravados no escopo da branch padrão. Para saber mais, confira [Restrições de acesso a um cache](#restrictions-for-accessing-a-cache).

Quando uma execução com acesso somente leitura ao cache tenta salvar um cache, o salvamento falha, mas a etapa e o trabalho não falham. O fluxo de trabalho continua e a falha é relatada como um aviso no log de fluxo de trabalho. Nesse caso, considere o seguinte:

* Para manter os benefícios de desempenho do cache no escopo da branch padrão, verifique se há um fluxo de trabalho confiável para manter o cache atualizado, por exemplo, uma compilação de CI acionada por um `push` para a branch padrão. Essas entradas de cache podem ser restauradas por fluxos de trabalho disparados por eventos de baixa confiança, como `pull_request_target`.
* Em fluxos de trabalho de baixa confiança, mude para uma operação de cache apenas para restauração, como `actions/cache/restore`, para deixar claro o uso pretendido do cache e evitar o aviso nos logs da execução do fluxo de trabalho.

## Controlando o acesso ao cache com `cache-mode`

Use a chave de fluxo de trabalho `cache-mode` para conceder aos jobs o nível mínimo de acesso ao cache de que precisam. Você pode definir `cache-mode` no nível do fluxo de trabalho, no nível do trabalho ou em ambos. Um valor no nível do trabalho substitui o valor no nível do fluxo de trabalho para esse trabalho. Para obter a sintaxe, consulte [Sintaxe de fluxo de trabalho para o GitHub Actions](workflow-syntax.md#cache-mode).

`cache-mode` controla o acesso ao cache concedido ao token da tarefa e é aplicado por meio de tokens de cache com escopo. A chave aceita os valores a seguir.

| Value        | Restaurar caches | Salvar caches |
|------------|----------------|-------------|
| `read`       | Sim              | No            |
| `write`      | Sim              | Sim           |
| `write-only` | No               | Sim           |
| `none`       | No               | No            |

Se você omitir `cache-mode`, um `read` ou `write` padrão será usado com base no tipo de gatilho. Consulte [Configurações padrão](#defaults) e [Ignorando a restrição padrão do cache de gatilhos não confiáveis](#bypassing-the-default-untrusted-trigger-cache-restriction).

### Defaults

| Configuration            | Tipo de acionador               | Acesso efetivo |
|------------------------|-------------------------------|--------------|
| `cache-mode` omitido     | Confiável                       | `write`        |
| `cache-mode` omitido     | Baixa confiança                 | `read`         |
| `cache-mode: write`      | Confiável ou de baixa confiança | `write`        |
| `cache-mode: write-only` | Confiável ou de baixa confiança | `write-only`   |
| `cache-mode: read`       | Confiável ou de baixa confiança | `read`         |
| `cache-mode: none`       | Confiável ou de baixa confiança | `none`         |

Para o detalhamento dos gatilhos confiáveis versus os de baixa confiança, consulte [acesso ao cache para gatilhos de fluxo de trabalho de baixa confiança](#cache-access-for-low-trust-workflow-triggers).

O executor expõe o modo efetivo na variável de ambiente `ACTIONS_CACHE_MODE`, e a ação `actions/cache` e o kit de ferramentas `@actions/cache` o respeitam. A restauração é ignorada quando o modo não permite leituras (`none` ou `write-only`), e o salvamento é ignorado quando o modo não permite gravações (`none` ou `read`). Quando uma operação de cache é ignorada devido ao modo, a ação registra uma mensagem informativa, e a etapa e a execução continuam sem falhar. Uma restauração ignorada é tratada como uma falha de cache; uma salvação ignorada simplesmente não é executada.

### Acesso ao cache em fluxos de trabalho reutilizáveis

`cache-mode` é propagado do fluxo de trabalho chamador para os fluxos de trabalho reutilizáveis que ele chama. Um explícito `cache-mode` no trabalho de chamada ou herdado do fluxo de trabalho do chamador limita o acesso ao cache que o fluxo de trabalho chamado pode solicitar.

Se o trabalho chamador não definir nem herdar um `cache-mode` explícito, o workflow chamado pode solicitar explicitamente `write` mesmo quando o gatilho de baixa confiança do chamador tem `read` como padrão. Para limitar um workflow chamado a acesso somente leitura, defina `cache-mode: read` no job que o invoca.

Se um fluxo de trabalho chamado declarar um `cache-mode` que solicita acesso além desse limite explícito, a execução não será iniciada e GitHub relatará um erro de validação. Por exemplo, um chamador que permite, no máximo, `read` não pode chamar um fluxo de trabalho que declare `write`. Como `read` e `write-only` conceder recursos diferentes e não sobrepostos, uma incompatibilidade entre eles também é uma solicitação excessiva. Por exemplo, um `write-only` chamador não pode chamar um fluxo de trabalho que declare `read`. Para obter mais informações sobre como chamar fluxos de trabalho reutilizáveis, consulte [Reutilizar fluxos de trabalho](../../how-tos/reuse-automations/reuse-workflows.md#controlling-cache-access-in-reusable-workflows).

### Ignorando a restrição de cache de gatilho não confiável padrão

Um trabalho ou fluxo de trabalho que declara `cache-mode: write` ou `cache-mode: write-only` substitui explicitamente o padrão de somente leitura seguro que, de outra forma, se aplicaria a uma execução disparada por um evento de baixa confiança. Consulte [o acesso ao Cache para gatilhos de fluxo de trabalho de baixa confiança](#cache-access-for-low-trust-workflow-triggers).

!!! warning
    Declarar explicitamente `cache-mode: write-only` ou `cache-mode: write` reintroduz o risco de envenenamento de cache que as permissões padrão de somente leitura para gatilhos não confiáveis foram projetadas para evitar. Se um fluxo de trabalho executado por um gatilho não confiável, como `pull_request_target`, `issue_comment` ou `workflow_run`, declarar um `cache-mode` com permissão de gravação, vulnerabilidades ou a execução de código não confiável no fluxo de trabalho poderão então ser usadas para salvar um cache. Um fluxo de trabalho mais privilegiado que restaura posteriormente esse cache pode executar conteúdo controlado pelo invasor.

Antes de definir um `cache-mode` com permissão de gravação em um fluxo de trabalho com um gatilho não confiável, considere se uma mitigação mais restrita atende às suas necessidades:

* Mantenha em vigor a restrição de acesso seguro ao cache, declarando explicitamente `cache-mode: read` no job, e deixe que um fluxo de trabalho confiável, disparado por `push`, gerencie o cache. Consulte [Acesso ao cache para gatilhos de fluxo de trabalho de baixa confiança](#cache-access-for-low-trust-workflow-triggers).
* Declare apenas um `cache-mode` com permissão de gravação para gatilhos de baixa confiança em trabalhos que não processam entrada não confiável antes de gravar no cache. Isso inclui código obtido de fontes não confiáveis, como forks e pull requests.
* Se você substituir o padrão seguro, trate o cache resultante como não confiável em todo fluxo de trabalho em que ele for restaurado e evite restaurá-lo em uma execução que tenha acesso de gravação aos segredos ou permissões elevadas.
* Siga as diretrizes sobre as [práticas recomendadas para usar caches com segurança](#best-practices-for-using-caches-securely).

## Práticas recomendadas para usar caches com segurança

O conteúdo do cache não está assinado ou verificado e qualquer execução de fluxo de trabalho que possa ler um cache pode extrair seu conteúdo. Os caches extraídos podem modificar arquivos que são executados posteriormente em uma execução de fluxo de trabalho, levando à execução de código mal-intencionado. Siga estas práticas para reduzir o risco de segurança de usar caches.

* **Não armazene informações confidenciais em um cache.** Qualquer pessoa que possa abrir uma solicitação de pull no repositório pode ler o conteúdo dos caches no branch base. Não escreva segredos, tokens ou credenciais em um caminho armazenado em cache. Armazene valores confidenciais como segredos. Consulte [Segredos](../../concepts/security/secrets.md).
* **Salva caches usando gatilhos confiáveis.** Restringir gravações de cache a fluxos de trabalho disparados por atores confiáveis (normalmente aqueles com acesso de gravação ao repositório). Consulte [Acesso ao cache para gatilhos de fluxo de trabalho de baixa confiança](#cache-access-for-low-trust-workflow-triggers) para conhecer as restrições padrão impostas para limitar quais gatilhos de fluxo de trabalho podem gravar no cache. Além disso, considere o uso de ambientes com regras de proteção de implantação para limitar ainda mais os fluxos de trabalho que podem modificar o cache. Consulte [Gerenciar ambientes para implantação](../../how-tos/deploy/configure-and-manage-deployments/manage-environments.md).
* **Siga as melhores práticas de segurança do fluxo de trabalho para proteger seus fluxos de trabalho:** Limite os fluxos de trabalho que têm acesso de gravação em cache àqueles que foram protegidos contra vulnerabilidades de fluxo de trabalho. Siga as diretrizes em [Referência de uso seguro](../security/secure-use.md#writing-workflows) para evitar vulnerabilidades em seus fluxos de trabalho que possam levar à execução de código e à introdução de entradas de cache mal-intencionadas.

Para obter orientações mais amplas sobre como proteger seus fluxos de trabalho, consulte [Referência de uso seguro](../security/secure-use.md).

## Limites de uso e política de eliminação

GitHub aplica limites ao armazenamento e à retenção em cache para gerenciar os custos de armazenamento e evitar abusos. Entender esses limites ajuda você a otimizar o uso do cache.

### Limites padrão

GitHub removerá as entradas de cache que não foram acessadas em mais de 7 dias. Não há limite para o número de caches que você pode armazenar, mas o tamanho total de todos os caches em um repositório é limitado. Por padrão, o limite é de 10 GB por repositório, mas esse limite pode ser aumentado por proprietários corporativos, proprietários da organização ou administradores de repositório.
Qualquer uso além de 10 GB é cobrado em sua conta. Após um repositório atingir seu volume máximo de armazenamento em cache, a política de remoção de cache criará espaço excluindo os caches na ordem da última data de acesso, da mais antiga para a mais recente.

Se você exceder o limite, GitHub salvará o novo cache, mas começará a despejar caches até que o tamanho total seja menor que o limite do repositório. O processo de despejo de cache pode causar oscilação excessiva do cache, em que os caches são criados e excluídos com alta frequência. Para reduzir isso, você pode examinar os caches de um repositório e executar etapas corretivas, como remover o cache de fluxos de trabalho específicos ou aumentar o tamanho do cache. Essa funcionalidade só está disponível para usuários com um método de pagamento cadastrado que aderirem ao configurar as configurações
de cache. Consulte [Gerenciando caches](../../how-tos/manage-workflow-runs/manage-caches.md).

Você pode criar entradas de cache a uma taxa de até 200 uploads por minuto por repositório e baixá-las a uma taxa de 1500 downloads por minuto por repositório. Se você exceder essa taxa, as tentativas subsequentes de upload ou download de cache falharão até que o limite de taxa relevante seja redefinido. O tempo até que o limite de taxa seja redefinido é retornado no `Retry-After` cabeçalho da resposta. Consulte [Limites do Actions](../limits.md) para obter mais informações sobre GitHub Actions limites de taxa.

### Aumentando o tamanho do cache

Se você quiser reduzir a taxa na qual as entradas de cache são removidas, você pode aumentar os limites de armazenamento para o cache nas Configurações de Ações. Os repositórios de propriedade dos usuários podem configurar até 10 TB por repositório. Para repositórios de propriedade das organizações, o limite máximo configurável é determinado pelas configurações da organização. Para organizações pertencentes a uma empresa, o limite máximo configurável é determinado pelas configurações da empresa. Aumentar o limite além dos 10 GB padrão incorrerá em custos adicionais se esse armazenamento for usado.

Para obter mais informações, consulte:

* [Gerenciando configurações de GitHub Actions para um repositório](https://docs.github.com/pt/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#configuring-cache-settings-for-your-repository)
* [Desabilitando ou limitando GitHub Actions para sua organização](https://docs.github.com/pt/organizations/managing-organization-settings/disabling-or-limiting-github-actions-for-your-organization#managing-github-actions-cache-storage-for-your-organization)
* [Impor políticas para GitHub Actions em sua empresa](https://docs.github.com/pt/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise#artifact-and-log-retention)

O uso de armazenamento adicional também é controlado pelos orçamentos configurados para GitHub Actions ou para o SKU de Armazenamento em Cache de Ações. Se você tiver limites configurados e exceder um orçamento, seu cache se tornará somente leitura até que seu status de cobrança seja resolvido ou até que seu uso caia abaixo do limite gratuito de 10 GB devido ao vencimento dos caches ou à sua exclusão explícita. Para obter mais informações sobre como configurar orçamentos, consulte [Definir orçamentos para controlar gastos com produtos limitados](https://docs.github.com/pt/billing/how-tos/set-up-budgets).

Definir seus orçamentos de SKU do Armazenamento em Cache do Actions inferiores ao custo total de usar o armazenamento configurado durante o período de cobrança pode levar o cache a entrar frequentemente no modo somente leitura. Por exemplo, se o orçamento da SKU for de US$ 0 e você tiver configurado o tamanho máximo de cache do repositório em 20 GB, o cache entrará no modo somente leitura assim que o armazenamento exceder o limite gratuito.

Abaixo estão alguns custos mensais ilustrativos para informar os orçamentos que talvez você deseje definir para o SKU de Armazenamento de Cache de Ações.

| Tamanho do cache | Custo mensal (se totalmente utilizado) |
|----------------|--------------------------------------|
| 50GB             | US$ 2,80                               |
| 200 GB           | $13.30                                 |
| 1000 GB          | US$ 69,30                              |

## Próximas etapas

Para gerenciar seus caches de dependência, consulte [Gerenciando caches](../../how-tos/manage-workflow-runs/manage-caches.md).
