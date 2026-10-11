---
title: Impondo atestados de artefatos com um controlador de admissão do Kubernetes
description: Use um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/secure-your-work/use-artifact-attestations/enforce-artifact-attestations
captured: '2026-10-11'
section: How tos / Secure your work / Use artifact attestations
---

# Impondo atestados de artefatos com um controlador de admissão do Kubernetes { #enforcing-artifact-attestations-with-a-kubernetes-admission-controller }

_Use um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes._

> [!NOTE] Antes de continuar, verifique se você habilitou a procedência do build para imagens de contêiner, incluindo a definição do atributo `push-to-registry` na [ação `attest`](https://github.com/actions/attest), conforme documentado em [Gerando a procedência do build para imagens de contêiner](use-artifact-attestations.md#generating-build-provenance-for-container-images). Isso é necessário para que o Controlador de Política verifique o atestado.

## Introdução ao controlador de admissão do Kubernetes { #getting-started-with-kubernetes-admission-controller }

Para configurar um controlador de admissão para aplicar atestados de artefato do GitHub, você precisa:

1. [Implantar o Sigstore Policy Controller](#deploy-the-sigstore-policy-controller).
2. [Adicionar o GitHub `TrustRoot` e um `ClusterImagePolicy` ao cluster](#add-the-github-trustroot-and-a-clusterimagepolicy).
3. [Habilitar a política em seu namespace](#enable-the-policy-in-your-namespace).

### Implantar o Sigstore Policy Controller { #deploy-the-sigstore-policy-controller }

O Sigstore Policy Controller foi empacotado e disponibilizado por meio de um [Helm chart](https://github.com/sigstore/helm-charts). Antes de começar, verifique se de que tem os seguintes pré-requisitos:

* Um cluster do Kubernetes com versão 1.27 ou posterior
* [Helm](https://helm.sh/docs/intro/install/) 3.0 ou posterior
* [kubectl](https://kubernetes.io/docs/tasks/tools/)

Primeiro, instale o gráfico Helm que implanta o Sigstore Policy Controller:

```bash copy
helm upgrade policy-controller --install --atomic \
  --create-namespace --namespace artifact-attestations \
  oci://ghcr.io/sigstore/helm-charts/policy-controller \
  --version 0.10.5
```

Isso instala o Controlador de Política no namespace `artifact-attestations`. Neste ponto, nenhuma política foi configurada e não imporá atestados.

### Adicione o GitHub `TrustRoot` e um `ClusterImagePolicy` { #add-the-github-trustroot-and-a-clusterimagepolicy }

Depois que o controlador de política tiver sido implantado, você precisará adicionar o GitHub `TrustRoot` e um `ClusterImagePolicy` ao cluster. Use o gráfico Helm que fornecemos para fazer isso. Certifique-se de substituir `MY-ORGANIZATION` pelo nome da sua organização do GitHub (por exemplo, `github` ou `octocat-inc`).

```bash copy
helm upgrade trust-policies --install --atomic \
 --namespace artifact-attestations \
 oci://ghcr.io/github/artifact-attestations-helm-charts/trust-policies \
 --version v0.7.0 \
 --set policy.enabled=true \
 --set policy.organization=MY-ORGANIZATION
```

Agora você instalou a raiz de confiança do GitHub e uma política de atestado de artefato em seu cluster. Essa política rejeitará artefatos que não tenham se originado de sua organização do GitHub.

### Habilitar a política em seu namespace { #enable-the-policy-in-your-namespace }

!!! warning
    Essa política não será aplicada até que você especifique a quais namespaces ela deve se aplicar.

Cada namespace em seu cluster pode impor políticas de forma independente. Para habilitar a imposição em um namespace, você pode adicionar o seguinte rótulo ao namespace:

```yaml
metadata:
  labels:
    policy.sigstore.dev/include: "true"
```

Depois que o rótulo for adicionado, a política de atestado de artefato do GitHub será imposta no namespace.

Como alternativa, você pode executar:

```bash copy
kubectl label namespace MY-NAMESPACE policy.sigstore.dev/include=true
```

### Imagens correspondentes { #matching-images }

Por padrão, a política instalada com o Helm chart `trust-policies` verificará a conformidade de todas as imagens antes de admiti-las no cluster. Se você pretende impor atestados apenas para um subconjunto de imagens, pode usar os valores do Helm `policy.images` e `policy.exemptImages` para especificar uma lista de imagens para correspondência. Esses valores podem ser definidos por meio de uma lista de padrões globais que correspondem aos nomes das imagens. A sintaxe de globbing usa a semântica Go [filepath](https://pkg.go.dev/path/filepath#Match), com a adição de `**` para corresponder a qualquer sequência de caracteres, incluindo barras.

Por exemplo, para impor atestados para imagens que correspondem ao padrão `ghcr.io/MY-ORGANIZATION/*` e admitem `busybox` sem um atestado válido, é possível executar:

```bash copy
helm upgrade trust-policies --install --atomic \
 --namespace artifact-attestations \
 oci://ghcr.io/github/artifact-attestations-helm-charts/trust-policies \
 --version v0.7.0 \
 --set policy.enabled=true \
 --set policy.organization=MY-ORGANIZATION \
 --set-json 'policy.exemptImages=["index.docker.io/library/busybox**"]' \
 --set-json 'policy.images=["ghcr.io/MY-ORGANIZATION/**"]'
```

Todos os padrões devem usar o nome totalmente qualificado, mesmo que as imagens sejam originadas do Docker Hub. Neste exemplo, se quisermos isentar a imagem `busybox`, devemos fornecer o nome completo, incluindo o domínio, e o glob com asterisco duplo para corresponder a todas as versões da imagem: `index.docker.io/library/busybox**`.

Observe que qualquer imagem que você pretenda admitir *deve* ter um padrão glob correspondente na lista `policy.images`. Se uma imagem não corresponder a padrão, ela será rejeitada. Além disso, se uma imagem corresponder a ambos `policy.images` e `policy.exemptImages`, ela será rejeitada.

### Uso avançado { #advanced-usage }

Para ver o conjunto completo de opções que você pode configurar com o gráfico Helm, você pode executar um dos seguintes comandos.
Para opções do controlador de políticas:

```bash copy
helm show values oci://ghcr.io/sigstore/helm-charts/policy-controller --version 0.10.5
```

Para opções de política de confiança:

```bash copy
helm show values oci://ghcr.io/github/artifact-attestations-helm-charts/trust-policies --version v0.7.0
```

Para obter mais informações sobre o Sigstore Policy Controller, consulte a [documentação do Sigstore Policy Controller](https://docs.sigstore.dev/policy-controller/overview/).
