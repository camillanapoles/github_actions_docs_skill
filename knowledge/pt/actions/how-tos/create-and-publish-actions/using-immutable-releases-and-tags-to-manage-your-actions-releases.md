---
title: Como usar versões e marcas imutáveis para gerenciar as versões da sua ação
description: Saiba como você pode usar uma combinação de lançamentos imutáveis no GitHub e tags Git para gerenciar os lançamentos da sua ação.
product: GitHub Actions
documentType: article
lang: pt-BR
plan: free-pro-team@latest
source: https://docs.github.com/pt/actions/how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases
captured: '2026-10-11'
section: GitHub Actions
---

# Como usar versões e marcas imutáveis para gerenciar as versões da sua ação

_Saiba como você pode usar uma combinação de lançamentos imutáveis no GitHub e tags Git para gerenciar os lançamentos da sua ação._

Se você habilitar as versões imutáveis no repositório da sua ação, poderá gerenciar essas versões da seguinte maneira:

1. Para iniciar o ciclo de lançamento, desenvolva e valide uma possível versão para sua ação em um branch de lançamento.
2. Determine como você deseja compartilhar suas alterações:
   * Se você estiver pronto para compartilhar uma versão inalterável de sua ação, crie uma versão em GitHub com uma marca específica da versão (por exemplo, `v1.0.0`). Confira [Gerenciar versões em repositórios](https://docs.github.com/pt/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release).
   * Se você quiser poder atualizar a tag Git de um lançamento depois, não crie um lançamento em GitHub. Em vez disso, crie uma etiqueta da seguinte maneira:
     * Se sua versão contiver alterações interruptivas para fluxos de trabalho existentes, crie uma marca de versão principal (por exemplo, `v1`).
     * Se sua versão contiver nova funcionalidade compatível com versões anteriores, crie uma marca de versão secundária (por exemplo, `v1.1`).
     * Se sua versão contiver correções de bug compatíveis com versões anteriores, crie uma marca de versão de patch (por exemplo, `v1.1.1`).
3. Para tags do Git que não estão vinculadas a uma versão em GitHub, certifique-se de que os usuários tenham acesso à versão mais recente compatível da sua ação atualizando-os da seguinte maneira:

   * Para uma versão principal, atualize a marca para apontar para a referência do Git da versão secundária ou do patch mais recente relacionada.
   * Para uma versão secundária, atualize a marca para apontar para a referência do Git da versão de patch relacionada mais recente.

   Para mover uma marca Git existente para a confirmação mais recente, force o envio por push da marca com os seguintes comandos:

            ```bash copy
   git tag -f TAG-NAME
   git push -f --tags
   ```
