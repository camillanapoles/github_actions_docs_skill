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
