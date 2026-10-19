---
title: Controlador de admissão do Kubernetes
description: Saiba como você pode usar um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/concepts/security/kubernetes-admissions-controller
captured: '2026-10-19'
section: Concepts / Security
---

# Controlador de admissão do Kubernetes

_Saiba como você pode usar um controlador de admissão para impor atestados de artefato em seu cluster Kubernetes._

## Sobre o controlador de admissão do Kubernetes

Os [atestados de artefatos](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md) permitem que você crie garantias de procedência e integridade infalsificáveis para o software que você cria. Por sua vez, as pessoas que consomem seu software podem verificar onde e como seu software foi criado.

Os controladores de admissão do Kubernetes são plug-ins que governam o comportamento do servidor de API do Kubernetes. Eles são comumente usados para impor políticas de segurança e práticas recomendadas em um cluster do Kubernetes.

Usando o projeto de código aberto [Sigstore Policy Controller](https://docs.sigstore.dev/policy-controller/overview/), você pode adicionar um controlador de admissão ao seu cluster do Kubernetes que pode impor atestados de artefatos. Dessa forma, você pode garantir que apenas artefatos com atestados válidos possam ser implantados.

Para [instalar o controlador](../../how-tos/secure-your-work/use-artifact-attestations/enforce-artifact-attestations.md), oferecemos [dois gráficos Helm](https://github.com/github/artifact-attestations-helm-charts): um para implantar o Sigstore Policy Controller e outro para carregar a raiz de confiança do GitHub e uma política padrão.

### Sobre a verificação de imagens

Quando o Policy Controller estiver instalado, ele interceptará todas as solicitações de pull de imagens e verificará a atestação da imagem. O atestado deve ser armazenado no registro de imagem como um [artefato anexado OCI](https://oras.land/docs/concepts/reftypes/) contendo um [pacote Sigstore](https://docs.sigstore.dev/about/bundle/) que contém o atestado e o material criptográfico (por exemplo, certificados e assinaturas) usados para verificar o atestado. Em seguida, é executado um processo de verificação que garante que a imagem foi criada com a procedência de build especificada e corresponde a todas as políticas habilitadas pelo administrador do cluster.

Para que uma imagem seja verificável, ela precisa ter um atestado de procedência válido no registro, o que pode ser feito habilitando o atributo `push-to-registry: true` na ação `actions/attest`. Consulte [Gerando proveniência de compilação para imagens de contêiner](../../how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations.md) para obter mais detalhes sobre como gerar atestações para imagens de contêiner.

### Sobre raízes e políticas de confiança

O Sigstore Policy Controller é configurado principalmente com raízes e políticas de confiança, representadas pelos Recursos Personalizados `TrustRoot` e `ClusterImagePolicy`. Um `TrustRoot` representa um canal de distribuição confiável para o material de chave pública usado para verificar atestados. Uma `ClusterImagePolicy` representa uma política para aplicar atestados em imagens.

Um `TrustRoot` também pode conter uma raiz de repositório [TUF](https://theupdateframework.io/), possibilitando que seu cluster receba atualizações contínuas e seguras para seu material de chave pública confiável. Se não for especificado, uma `ClusterImagePolicy` usará por padrão o material para chave da Sigstore Public Good de código aberto. Ao verificar os atestados gerados para repositórios privados, o `ClusterImagePolicy` deve fazer referência ao GitHub `TrustRoot`.

## Próximas etapas

Quando você estiver pronto para utilizar um controlador de admissão, consulte [Impondo atestados de artefatos com um controlador de admissão do Kubernetes](../../how-tos/secure-your-work/use-artifact-attestations/enforce-artifact-attestations.md).
