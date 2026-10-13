---
title: Suporte do Dockerfile para GitHub Actions
description: Ao criar um Dockerfile para uma ação do contêiner Docker, você deverá ter em mente como algumas instruções do Docker interagem com o GitHub Actions e com um arquivo de metadados da ação.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/reference/workflows-and-actions/dockerfile-support
captured: '2026-10-13'
section: Reference / Workflows and actions
---

# Suporte do Dockerfile para GitHub Actions { #dockerfile-support-for-github-actions }

_Ao criar um Dockerfile para uma ação do contêiner Docker, você deverá ter em mente como algumas instruções do Docker interagem com o GitHub Actions e com um arquivo de metadados da ação._

### USUÁRIO { #user }

As ações do Docker devem ser executadas pelo usuário-padrão do Docker (raiz). Não use a instrução `USER` no `Dockerfile`, porque você não poderá acessar o diretório `GITHUB_WORKSPACE`. Para obter mais informações, confira [Referência de variáveis](variables.md#default-environment-variables) e [Referência de USER](https://docs.docker.com/engine/reference/builder/#user) na documentação do Docker.

### FROM

A primeira instrução no `Dockerfile` precisa ser `FROM`, que seleciona uma imagem base do Docker. Para obter mais informações, confira a [Referência de FROM](https://docs.docker.com/engine/reference/builder/#from) na documentação do Docker.

Estas são algumas melhores práticas ao definir o argumento `FROM`:

* Recomendamos o uso de imagens oficiais do Docker. Por exemplo, `python` ou `ruby`.
* Use uma tag da versão, se houver, preferencialmente com uma versão principal. Por exemplo, use `node:10` ao invés de `node:latest`.
* Recomendamos usar imagens do Docker com base no sistema operacional [Debian](https://www.debian.org/).

### WORKDIR (diretório de trabalho) { #workdir }

GitHub define o caminho do diretório de trabalho na variável de `GITHUB_WORKSPACE` ambiente. Recomendamos não usar a instrução `WORKDIR` no `Dockerfile`. Antes que a ação seja executada, GitHub montará o `GITHUB_WORKSPACE` diretório sobre qualquer coisa que estava naquele local na imagem do Docker e definirá `GITHUB_WORKSPACE` como o diretório de trabalho. Para obter mais informações, confira [Referência de variáveis](variables.md#default-environment-variables) e [Referência de WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir) na documentação do Docker.

### Ponto de Entrada { #entrypoint }

Se você definir `entrypoint` no arquivo de metadados de uma ação, ele substituirá o `ENTRYPOINT` definido no `Dockerfile`. Para saber mais, confira [Referência de sintaxe de metadados](metadata-syntax.md#runsentrypoint).

A instrução `ENTRYPOINT` do Docker tem um formulário de *shell* e um formulário de *execução*. A documentação de `ENTRYPOINT` do Docker recomenda o uso do formulário *exec* da instrução `ENTRYPOINT`. Para obter mais informações sobre os formulários *exec* e *shell*, confira a [Referência de ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint) na documentação do Docker.

Você não deve usar `WORKDIR` para especificar o ponto de entrada no Dockerfile. Em vez disso, você deverá usar um caminho absoluto. Para obter mais informações, confira [WORKDIR](#workdir).

Se você configurar o contêiner para usar o formulário *exec* da instrução `ENTRYPOINT`, os `args` configurados no arquivo de metadados da ação não serão executados em um shell de comando. Se os `args` da ação contiverem uma variável de ambiente, a variável não será substituída. Por exemplo, o uso do formato *exec* a seguir não imprimirá o valor armazenado em `$GITHUB_SHA`, mas imprimirá `"$GITHUB_SHA"`.

```dockerfile
ENTRYPOINT ["echo $GITHUB_SHA"]
```

Caso deseje fazer a substituição da variável, use o formulário *shell* ou execute um shell diretamente. Por exemplo, usando o formato *exec* a seguir, você pode executar um shell para imprimir o valor armazenado na variável de ambiente `GITHUB_SHA`.

```dockerfile
ENTRYPOINT ["sh", "-c", "echo $GITHUB_SHA"]
```

Para fornecer os `args` definidos no arquivo de metadados da ação para um contêiner do Docker que usa o formulário *exec*, `ENTRYPOINT`recomendamos criar um script de shell com o nome `entrypoint.sh` que é chamado por meio da instrução `ENTRYPOINT`:

#### Exemplo de *Dockerfile* { #example-dockerfile }

```dockerfile
```
# Container image that runs your code
FROM debian:9.5-slim

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh /entrypoint.sh

# Executes `entrypoint.sh` when the Docker container starts up
ENTRYPOINT ["/entrypoint.sh"]
```

```
#### Exemplo de arquivo *entrypoint.sh* { #example-entrypointsh-file }

Usando o exemplo de Dockerfile acima, GitHub enviará o `args` configurado no arquivo de metadados da ação como argumentos para `entrypoint.sh`. Adicione o `#!/bin/sh`[shebang](https://en.wikipedia.org/wiki/Shebang_\(Unix\)) no início do arquivo `entrypoint.sh` para usar explicitamente o shell compatível com [POSIX](https://en.wikipedia.org/wiki/POSIX) do sistema.

```shell
#!/bin/sh

```
# `$#` expands to the number of arguments and `$@` expands to the supplied `args`
printf '%d args:' "$#"
printf " '%s'" "$@"
printf '\n'
```

O seu código deve ser executável. Verifique se o arquivo `entrypoint.sh` tem as permissões `execute` antes de usá-lo em um fluxo de trabalho. Você pode modificar as permissões a partir do seu terminal usando este comando:

```
chmod +x entrypoint.sh
```

Quando um script de shell `ENTRYPOINT` não for executável, você receberá um erro semelhante a este:

```
Error response from daemon: OCI runtime create failed: container_linux.go:348: starting container process caused "exec: \"/entrypoint.sh\": permission denied": unknown
```

```
### CMD

Se você definir `args` no arquivo de metadados da ação, `args` substituirá a instrução `CMD` especificada no `Dockerfile`. Para saber mais, confira [Referência de sintaxe de metadados](metadata-syntax.md#runsargs).

Se você usar `CMD` no `Dockerfile`, siga estas diretrizes:

1. Documente os argumentos necessários no README da ação e omita-os da instrução `CMD`.
2. Use padrões que permitam o uso da ação sem a especificação de `args`.
3. Se a ação expuser um sinalizador `--help` ou algo semelhante, use-o para tornar a ação autodocumentada.

## Recursos compatíveis com o Linux

GitHub Actions dá suporte aos recursos padrão do Linux compatíveis com o Docker. Não é possível adicionar ou remover recursos. Para obter mais informações sobre os recursos padrão do Linux com suporte pelo Docker, consulte [Recursos do kernel Linux](https://docs.docker.com/engine/security/#linux-kernel-capabilities) na documentação do Docker. Para saber mais sobre as funcionalidades do Linux, confira [Visão geral das funcionalidades do Linux](http://man7.org/linux/man-pages/man7/capabilities.7.html) nas páginas do manual do Linux.
