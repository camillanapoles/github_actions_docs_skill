---
title: Instalar um certificado da Apple em executores do macOS para desenvolvimento do Xcode
description: Saiba como assinar apps do Xcode em um fluxo de trabalho de integração contínua (CI) instalando um certificado de assinatura de código da Apple nos executores GitHub Actions.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/deploy/deploy-to-third-party-platforms/sign-xcode-applications
captured: '2026-10-19'
section: How tos / Deploy / Deploy to third party platforms
---

# Instalar um certificado da Apple em executores do macOS para desenvolvimento do Xcode

_Saiba como assinar apps do Xcode em um fluxo de trabalho de integração contínua (CI) instalando um certificado de assinatura de código da Apple nos executores GitHub Actions._

## Pré-requisitos

Você deve estar familiarizado com YAML e a sintaxe para GitHub Actions. Para saber mais, veja:

* [Escrevendo fluxos de trabalho](../../write-workflows.md)
* [Sintaxe de fluxo de trabalho para o GitHub Actions](../../../reference/workflows-and-actions/workflow-syntax.md)

Você deve ter um entendimento sobre construção e assinatura de aplicativos no Xcode. Para obter mais informações, confira a [documentação de desenvolvedor da Apple](https://developer.apple.com/documentation/).

## Criar segredos para seu certificado e perfil de provisionamento

O processo de assinatura envolve o armazenamento de certificados e provisionamento de perfis, transferindo-os para o executor, importando-os para a keychain e usando-os na sua compilação.

Para usar seu certificado e perfil de provisionamento em um executor, recomendamos fortemente que você use segredos GitHub. Para saber mais sobre como criar segredos e usá-los em um fluxo de trabalho, confira [Usar segredos em ações do GitHub](../../write-workflows/choose-what-workflows-do/use-secrets.md).

Crie segredos no seu repositório ou organização para os seguintes itens:

* Seu certificado de assinatura Apple.

  * Esse é o arquivo de certificado `p12`. Para obter mais informações sobre como exportar seu certificado de autenticação do Xcode, confira a [documentação do Xcode](https://help.apple.com/xcode/mac/current/#/dev154b28f09).

  * Você deve converter seu certificado em Base64 ao salvá-lo como um segredo. Neste exemplo, o segredo é chamado `BUILD_CERTIFICATE_BASE64`.

  * Use o comando a seguir para converter seu certificado para Base64 e copiá-lo para a sua área de transferência:

                ```shell
    base64 -i BUILD_CERTIFICATE.p12 | pbcopy
    ```

* A senha para seu certificado de assinatura da Apple.
  * Neste exemplo, o segredo é chamado `P12_PASSWORD`.

* O seu perfil de provisionamento da Apple.

  * Para obter mais informações sobre como exportar seu perfil de provisionamento do Xcode, confira a [documentação do Xcode](https://help.apple.com/xcode/mac/current/#/deva899b4fe5).

  * Você deve converter o seu perfil de provisionamento para Base64 ao salvá-lo como segredo. Neste exemplo, o segredo é chamado `BUILD_PROVISION_PROFILE_BASE64`.

  * Use o comando a seguir para converter o seu perfil de provisionamento para Base64 e copiá-lo para a sua área de transferência:

                ```shell
    base64 -i PROVISIONING_PROFILE.mobileprovision | pbcopy
    ```

* Uma senha do Keychain.

  * Uma nova keychain será criada no executo. Portanto, a senha para a nova keychain pode ser qualquer nova string aleatória. Neste exemplo, o segredo é chamado `KEYCHAIN_PASSWORD`.

## Adicionar uma etapa ao seu fluxo de trabalho

Este fluxo de trabalho de exemplo inclui uma etapa que importa o certificado da Apple e o perfil de provisionamento dos segredos de GitHub e os instala no executor.

```yaml copy
name: App build
on: push

jobs:
  build_with_signing:
    runs-on: macos-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v6
      - name: Install the Apple certificate and provisioning profile
        env:
          BUILD_CERTIFICATE_BASE64: ${{ secrets.BUILD_CERTIFICATE_BASE64 }}
          P12_PASSWORD: ${{ secrets.P12_PASSWORD }}
          BUILD_PROVISION_PROFILE_BASE64: ${{ secrets.BUILD_PROVISION_PROFILE_BASE64 }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          # create variables
          CERTIFICATE_PATH=$RUNNER_TEMP/build_certificate.p12
          PP_PATH=$RUNNER_TEMP/build_pp.mobileprovision
          KEYCHAIN_PATH=$RUNNER_TEMP/app-signing.keychain-db

          # import certificate and provisioning profile from secrets
          echo -n "$BUILD_CERTIFICATE_BASE64" | base64 --decode -o $CERTIFICATE_PATH
          echo -n "$BUILD_PROVISION_PROFILE_BASE64" | base64 --decode -o $PP_PATH

          # create temporary keychain
          security create-keychain -p "$KEYCHAIN_PASSWORD" $KEYCHAIN_PATH
          security set-keychain-settings -lut 21600 $KEYCHAIN_PATH
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" $KEYCHAIN_PATH

          # import certificate to keychain
          security import $CERTIFICATE_PATH -P "$P12_PASSWORD" -A -t cert -f pkcs12 -k $KEYCHAIN_PATH
          security set-key-partition-list -S apple-tool:,apple: -k "$KEYCHAIN_PASSWORD" $KEYCHAIN_PATH
          security list-keychain -d user -s $KEYCHAIN_PATH

          # apply provisioning profile
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          cp $PP_PATH ~/Library/MobileDevice/Provisioning\ Profiles
      - name: Build app
          # ...
```

!!! note
    Para destinos de build do iOS, seu perfil de provisionamento deve ter a extensão `.mobileprovision`. Para destinos de build do macOS, a extensão deve ser `.provisionprofile`. O fluxo de trabalho de exemplo acima deve ser atualizado para refletir sua plataforma de destino.

## Limpeza necessária nos executores auto-hospedados

Os executores hospedados em GitHub são máquinas virtuais isoladas, destruídas automaticamente ao final da execução do trabalho. Isso significa que os certificados e o perfil de provisionamento usados no executor durante o trabalho serão destruídos com o executor quando o trabalho for concluído.

Em executores auto-hospedados, o diretório `$RUNNER_TEMP` é limpo no final da execução do trabalho, mas o conjunto de chaves e o perfil de provisionamento ainda podem existir no executor.

Se você usa executores auto-hospedados, você deve adicionar uma última etapa ao seu fluxo de trabalho para ajudar a garantir que esses arquivos sensíveis sejam excluídos no final do trabalho. A etapa do fluxo de trabalho abaixo é um exemplo de como fazer isso.

```yaml
- name: Clean up keychain and provisioning profile
  if: ${{ always() }}
  run: |
    security delete-keychain $RUNNER_TEMP/app-signing.keychain-db
    rm ~/Library/MobileDevice/Provisioning\ Profiles/build_pp.mobileprovision
```
