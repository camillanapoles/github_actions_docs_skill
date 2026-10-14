"""Blueprint BPMN-like: gates determinísticos, ordem e critérios de aceite.

Cada gate é um nó do fluxo; o gateway final (`release`) roteia a continuidade:
aprovou → próxima issue indexada; reprovou → issue do próprio gate (fix/retry).
"""
from __future__ import annotations

from .domain import GateSpec

BLUEPRINT_ID = "github-actions-docs-skill/gate-driven/1"

GATES: tuple[GateSpec, ...] = (
    GateSpec(
        id="tests",
        name="Testes determinísticos do extrator e do pipeline",
        order=10,
        action="python3 -m pytest tests/ -q",
        produces=(".ci/pipeline-state.json",),
        acceptance=(
            "python3 -m pytest tests/ -q → 100% verde (0 failed)",
            "todo defeito novo descoberto entra como teste de regressão antes do fix",
        ),
        description="Suíte offline (sem rede) do extrator, do polish e do orquestrador.",
    ),
    GateSpec(
        id="capture",
        name="Captura completa (inventário pt-BR)",
        order=20,
        action="scripts/extract.py (relatório em .ci/extract-report.md)",
        produces=(".ci/extract-report.md", "knowledge/pt/manifest.json"),
        acceptance=(
            "247/247 páginas pt capturadas, 0 falhas (relatório .ci/extract-report.md)",
            "score de qualidade = 0 em todas as páginas (0 = impecável)",
            "nenhuma página com aviso de cura via HTML pendente",
        ),
        description="Verifica inventário e qualidade da base capturada de docs.github.com/pt/actions.",
    ),
    GateSpec(
        id="conformity",
        name="Completude e conformidade (mandato de validação)",
        order=30,
        action="python3 scripts/validate.py --langs pt,en --report knowledge/validation.md "
               "--json .ci/validation.json",
        produces=("knowledge/validation.md", ".ci/validation.json"),
        acceptance=(
            "scripts/validate.py → 0 falhas nos 8 grupos",
            "knowledge/validation.md e .ci/validation.json atualizados e commitados",
        ),
        description="Grupos 1-6 do validador: inventário, estrutura, conversão, links, nav, skill.",
    ),
    GateSpec(
        id="site",
        name="Site MkDocs buildável em modo estrito",
        order=40,
        action="python3 -m mkdocs build --strict --site-dir site",
        produces=("site/index.html",),
        acceptance=(
            "mkdocs build --strict → 0 avisos (âncoras, links, nav, arquivos órfãos)",
            "nav gerado por scripts/build_site.py cobre 100% das páginas",
        ),
        description="Garante que o conhecimento é navegável e publicável (Pages).",
    ),
    GateSpec(
        id="skill",
        name="Skill completa (references, templates, scripts)",
        order=50,
        action="pipeline.engine.SkillAction (inventário do SKILL.md × disco)",
        produces=("skills/github-actions/references/", "skills/github-actions/templates/"),
        acceptance=(
            "todas as references citadas no SKILL.md existem e não estão vazias",
            "todos os templates prometidos existem e passam em check-jsonschema + actionlint",
            "os 4 scripts da skill existem e passam em bash -n / py_compile",
        ),
        description="Entrega do pedido 3: templates válidos por contexto (CI/CD, GitOps, DevOps).",
    ),
    GateSpec(
        id="ci-issues",
        name="CI/CD verde e sem issues pendentes",
        order=60,
        action="gh run list / gh issue list (verificação de continuidade)",
        kind="task",
        required=True,
        produces=(".ci/next-issue.md",),
        acceptance=(
            "nenhuma corrida de CI com conclusion=failure nos últimos runs do branch",
            "nenhuma issue aberta com rótulo gate:* sem responsável/andamento",
            "se houver pendência, a próxima issue indexada existe e está publicada",
        ),
        description="Gatilho de continuidade: enquanto houver issue aberta, CI com erro ou "
                    "ausência de testes, o fluxo não é dado como concluído.",
    ),
    GateSpec(
        id="release",
        name="Gateway exclusivo de produção",
        order=90,
        action="pipeline.engine.ReleaseGateway",
        kind="gateway",
        produces=("ENTREGA.md", "README.md"),
        acceptance=(
            "todos os gates anteriores com status 0 (sucesso)",
            "ENTREGA.md atualizado com os números medidos da execução",
            "próxima issue indexada = 'Concluir e publicar' ou nenhuma (fluxo completo)",
        ),
        next_on_success=None,
        description="Aprova a entrega pronta para uso; caso contrário devolve erro + continuidade.",
    ),
)

BY_ID: dict[str, GateSpec] = {g.id: g for g in GATES}


def ordered() -> list[GateSpec]:
    return sorted(GATES, key=lambda g: g.order)


def after(gate_id: str) -> GateSpec | None:
    """Próximo gate indexado na ordem do blueprint (usado quando o atual aprova)."""
    seq = ordered()
    for i, g in enumerate(seq):
        if g.id == gate_id:
            return seq[i + 1] if i + 1 < len(seq) else None
    return None


def as_bpmn_dict() -> dict:
    """Representação legível do fluxo (nós + transições) para documentação/auditoria."""
    seq = ordered()
    return {
        "blueprint": BLUEPRINT_ID,
        "nodes": [
            {
                "id": g.id,
                "name": g.name,
                "type": g.kind,
                "order": g.order,
                "action": g.action,
                "acceptance": list(g.acceptance),
                "out": {
                    "success": (after(g.id).id if after(g.id) else "END"),
                    "failure": g.next_on_failure or f"issue:{g.id}",
                },
            }
            for g in seq
        ],
    }
