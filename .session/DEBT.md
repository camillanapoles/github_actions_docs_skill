# DEBT — débitos identificados e não executados (M5)

| # | Descrição | Causa | Impacto | Gatilho de retomada |
| --- | --- | --- | --- | --- |
| D1 | `mkdocs build --strict` com avisos de âncora/links | `align_anchors` cobre 205/500 páginas; links absolutos sem `.md` no espelho EN | gate `site` vermelho → Pages não publica | fechar gate `site` (ordem do pipeline) |
| D2 | Skill incompleta: 7 references, 24 templates, 4 scripts | entrega em andamento | gate `skill` status 3 | após `site`, ou por decisão de priorizar entrega visível |
| D3 | 34 linhas de tabela inconsistentes + 1 link interno | dano do markdown da API revelado após `repair_fences` | gate `conformity` vermelho | recaptura + reparo de tabelas |
| D4 | Score de qualidade 46 em 3 páginas | cura via HTML ainda não reexecutada após os fixes | gate `capture` vermelho → issue #1 aberta | recaptura (`extract-docs`) |
| D5 | Governança não aplicada: `rulesets: nenhum`, Pages 404 | `ADMIN_TOKEN` não chegou ao job (403 confirmado p/ GITHUB_TOKEN) | checks não obrigatórios; Pages desabilitado | `admin-bootstrap` com secret correto → `.ci/admin-bootstrap.log` |
| D6 | Required checks não configuráveis por esta sessão | token sem `Administration: write` | merge em `main` sem gate obrigatório | D5 resolvido |
| D7 | `LICENSE` + `NOTICE.md` ausentes | conteúdo derivado (CC-BY-4.0 © GitHub) não atribuído formalmente | risco de redistribuição | antes de publicar/mergear |
| D8 | `.ci/actionlint.txt` não é gerado quando actionlint passa | `tee` só roda com saída; passo verde não cria arquivo | diagnóstico ausente em sucesso | criar arquivo vazio explícito no passo |
| D9 | Nenhum PR aberto; `main` só tem `0ddafab` | decisão pendente de merge | `docs-publish` e `workflow_dispatch` do bootstrap inativos | gates verdes ou autorização explícita |
| D10 | `.igc-registry.yml` versionado na linhagem, não no default branch | runtime proíbe push em `main` (DEV-1) | descoberta R1 por outro repo fica incompleta até o merge | gate `release` verde ⇒ PR ⇒ merge leva o registry a `main` | 2026-10-13 |
| D11 | 3 testes pulados: `pandoc indisponível no ambiente` (marcador `requer_pandoc`) | sandbox sem pandoc/pypandoc-binary nesta geração | conversão HTML→MD não é exercitada localmente; M6 exige justificativa (dada aqui e em INTENT.md) | instalar `pypandoc-binary` ou rodar no CI, onde pandoc existe | 2026-10-13 |
| D12 | Round-trip T8 real (bundle deste repo → clone frio → suíte) executado uma vez, não agendado | modo da linhagem é `continuidade`, não `HANDOFF` (Art. 12 torna T8 condicional) | se a sessão virar HANDOFF, o aceite precisa ser reexecutado | classificar emissão como HANDOFF ⇒ obrigar T8 antes do CLOSE | 2026-10-13 |
| D13 | Varredura de órfãos remotos (G5/W6) implementada como função, sem agendamento | `sweep_orphans()` existe e é testada, mas nenhum cron a chama | linhagem órfã >30d não gera DEBT automaticamente | adicionar `schedule` que rode `sweep_orphans` + `add_debt` | 2026-10-13 |
