"""Motor do pipeline: actions (cada uma devolve Envelope), fábrica de issues e orquestrador."""
from __future__ import annotations

import dataclasses
import hashlib
import json
import re
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Sequence

from . import blueprint
from .domain import Addendum, Envelope, GateSpec, NextIssue, Status, utcnow
from .store import IssueRecord, PipelineStore


@dataclasses.dataclass(slots=True)
class Context:
    root: Path
    run_id: str
    langs: tuple[str, ...] = ("pt", "en")
    online: bool = False
    trigger: str = "manual"
    artifacts: tuple[str, ...] = ()

    @property
    def ci(self) -> Path:
        d = self.root / ".ci"
        d.mkdir(parents=True, exist_ok=True)
        return d


def _run(cmd: Sequence[str], cwd: Path, timeout: int = 900) -> tuple[int, str, str]:
    proc = subprocess.run(list(cmd), cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr


class Action:
    """Base: mede tempo, captura exceção como erro de infra (status 2)."""

    spec: GateSpec

    def __init__(self, spec: GateSpec) -> None:
        self.spec = spec

    def envelope(self, status: Status, message: str, *, started: float,
                 addenda: Sequence[Addendum] = (), metrics: dict[str, Any] | None = None) -> Envelope:
        env = Envelope.of(self.spec.id, self.spec.action, status, message,
                          addenda=addenda, metrics=metrics or {}, started_at=utcnow())
        return env.close(started)

    def execute(self, ctx: Context) -> Envelope:
        started = time.monotonic()
        try:
            return self.run(ctx, started)
        except subprocess.TimeoutExpired:
            return self.envelope(Status.ERROR_INFRA, f"timeout em {self.spec.action}", started=started)
        except Exception as exc:  # pragma: no cover - defesa
            return self.envelope(Status.ERROR_INFRA, f"{type(exc).__name__}: {exc}", started=started)

    def run(self, ctx: Context, started: float) -> Envelope:  # pragma: no cover - abstract
        raise NotImplementedError


class TestsAction(Action):
    def run(self, ctx: Context, started: float) -> Envelope:
        if shutil.which("pytest") is None and not _mod("pytest"):
            return self.envelope(Status.ERROR_INFRA, "pytest indisponível (instale: pip install pytest)",
                                 started=started)
        code, out, err = _run(["python3", "-m", "pytest", "tests/", "-q"], ctx.root)
        tail = (out or err).strip().splitlines()[-1:] or ["sem saída"]
        m = re.search(r"(\d+) passed", out)
        failed = re.search(r"(\d+) failed", out)
        metrics = {"passed": int(m.group(1)) if m else 0, "failed": int(failed.group(1)) if failed else 0}
        status = Status.SUCCESS if code == 0 else Status.ERROR_CONTENT
        return self.envelope(status, tail[0][:300], started=started, metrics=metrics)


class CaptureAction(Action):
    report = ".ci/extract-report.md"

    def run(self, ctx: Context, started: float) -> Envelope:
        path = ctx.root / self.report
        addenda = [Addendum("report", self.report)] if path.exists() else []
        counts: dict[str, int] = {}
        for lang in ctx.langs:
            root = ctx.root / "knowledge" / lang
            counts[lang] = len(list(root.rglob("*.md"))) if root.exists() else 0
        if not path.exists():
            return self.envelope(Status.ERROR_CONTENT, "relatório de captura ausente (.ci/extract-report.md)",
                                 started=started, metrics=counts)
        text = path.read_text(encoding="utf-8")
        ok = _int(text, r"\*\*Páginas OK:\*\*\s*(\d+)")
        fail = _int(text, r"\*\*Falhas:\*\*\s*(\d+)")
        score = _int(text, r"\*\*Score de qualidade[^:]*:\*\*\s*(\d+)")
        metrics = {**counts, "pages_ok": ok, "pages_failed": fail, "quality_score": score}
        if fail:
            return self.envelope(Status.ERROR_CONTENT, f"{fail} página(s) com falha de captura",
                                 started=started, addenda=addenda, metrics=metrics)
        if score:
            return self.envelope(Status.ERROR_CONTENT, f"score de qualidade {score} ≠ 0 (markdown não impecável)",
                                 started=started, addenda=addenda, metrics=metrics)
        if counts.get("pt", 0) < 247:
            return self.envelope(Status.ERROR_CONTENT, f"cobertura pt incompleta: {counts.get('pt')} páginas",
                                 started=started, addenda=addenda, metrics=metrics)
        return self.envelope(Status.SUCCESS,
                             f"captura completa: {ok} páginas pt, 0 falhas, score 0",
                             started=started, addenda=addenda, metrics=metrics)


class ConformityAction(Action):
    def run(self, ctx: Context, started: float) -> Envelope:
        cmd = ["python3", "scripts/validate.py", "--langs", ",".join(ctx.langs),
               "--report", "knowledge/validation.md", "--json", ".ci/validation.json"]
        if not (ctx.root / "scripts" / "validate.py").exists():
            return self.envelope(Status.ERROR_INFRA, "scripts/validate.py ausente", started=started)
        code, out, err = _run(cmd, ctx.root)
        summary = (out.strip().splitlines() or ["sem saída"])[-1]
        fails = [l for l in out.splitlines() if l.startswith("❌")]
        warns = [l for l in out.splitlines() if l.startswith("⚠️")]
        metrics = {"failures": len(fails), "warnings": len(warns), "exit_code": code}
        addenda = [Addendum("report", "knowledge/validation.md"), Addendum("json", ".ci/validation.json")]
        if fails:
            return self.envelope(Status.ERROR_CONTENT, f"{len(fails)} falha(s) de conformidade",
                                 started=started, addenda=addenda, metrics=metrics)
        return self.envelope(Status.SUCCESS, summary[:300], started=started,
                             addenda=addenda, metrics=metrics)


class SiteAction(Action):
    def run(self, ctx: Context, started: float) -> Envelope:
        if not _mod("mkdocs"):
            return self.envelope(Status.ERROR_INFRA,
                                 "mkdocs indisponível (pip install 'mkdocs-material>=9.5')", started=started)
        code, out, err = _run(["python3", "-m", "mkdocs", "build", "--strict", "--site-dir", "site"],
                              ctx.root, timeout=1200)
        blob = out + err
        warnings = len(re.findall(r"WARNING", blob))
        metrics = {"warnings": warnings, "exit_code": code}
        addenda = [Addendum("site", "site/index.html")] if (ctx.root / "site" / "index.html").exists() else []
        if code != 0:
            first = next((l for l in blob.splitlines() if "Aborted" in l or "ERROR" in l), "build falhou")
            return self.envelope(Status.ERROR_CONTENT, f"{first.strip()[:240]} ({warnings} avisos)",
                                 started=started, addenda=addenda, metrics=metrics)
        return self.envelope(Status.SUCCESS, f"site buildado em modo estrito ({warnings} avisos)",
                             started=started, addenda=addenda, metrics=metrics)


class SkillAction(Action):
    """Inventário do que o SKILL.md promete × o que existe no disco."""

    def run(self, ctx: Context, started: float) -> Envelope:
        skill = ctx.root / "skills" / "github-actions"
        md = skill / "SKILL.md"
        if not md.exists():
            return self.envelope(Status.ERROR_CONTENT, "skills/github-actions/SKILL.md ausente", started=started)
        text = md.read_text(encoding="utf-8")
        promised_refs = sorted(set(re.findall(r"references/([a-z0-9\-]+)\.md", text)))
        # catálogo do SKILL.md cita `workflows/x.yml`, `gitops/x.yaml`, `actions/x/`
        promised_tpl = sorted({f"{d}/{n}" for d, n in re.findall(
            r"`(?:templates/)?(workflows|gitops|actions)/([A-Za-z0-9._\-]+)`", text)})
        # só os scripts DA skill (linha de tabela `| \`scripts/x.sh\` |`);
        # os do repositório aparecem como `../../scripts/...` e não contam
        promised_scripts = sorted(set(
            re.findall(r"^\|\s*`scripts/([A-Za-z0-9._\-]+)`\s*\|", text, re.M)))
        have_refs = {p.stem for p in (skill / "references").glob("*.md")} if (skill / "references").exists() else set()
        tpl_root = skill / "templates"
        have_tpl = {p.relative_to(tpl_root).as_posix() for p in tpl_root.rglob("*") if p.is_file()} \
            if tpl_root.exists() else set()
        have_scripts = {p.name for p in (skill / "scripts").glob("*") } if (skill / "scripts").exists() else set()
        missing = {
            "references": [r for r in promised_refs if r not in have_refs],
            "templates": [t for t in promised_tpl
                          if not any(h == t or h.startswith(t + "/") for h in have_tpl)],
            "scripts": [s for s in promised_scripts if s not in have_scripts],
        }
        metrics = {
            "promised": {"references": len(promised_refs), "templates": len(promised_tpl),
                         "scripts": len(promised_scripts)},
            "delivered": {"references": len(have_refs), "templates": len(have_tpl),
                          "scripts": len(have_scripts)},
            "missing": missing,
        }
        total_missing = sum(len(v) for v in missing.values())
        if total_missing:
            resumo = ", ".join(f"{k}: {len(v)}" for k, v in missing.items() if v)
            return self.envelope(Status.PENDING, f"skill incompleta ({resumo} pendentes)",
                                 started=started, metrics=metrics)
        return self.envelope(Status.SUCCESS, "skill completa: references, templates e scripts entregues",
                             started=started, metrics=metrics)


class CiIssuesAction(Action):
    """Gatilho de continuidade: CI sem erros + sem issues abertas (gh) ou estado local."""

    def run(self, ctx: Context, started: float) -> Envelope:
        addenda = [Addendum("issue", ".ci/next-issue.md")] if (ctx.ci / "next-issue.md").exists() else []
        if not ctx.online or shutil.which("gh") is None:
            return self.envelope(Status.SKIPPED,
                                 "verificação de CI/issues requer gh + rede (roda no workflow gate-pipeline.yml)",
                                 started=started, addenda=addenda, metrics={"mode": "offline"})
        code, out, _ = _run(["gh", "run", "list", "--limit", "10",
                             "--json", "databaseId,conclusion,workflowName"], ctx.root, timeout=120)
        runs: list[dict[str, Any]] = json.loads(out) if code == 0 and out.strip() else []
        failures = [r for r in runs if r.get("conclusion") == "failure"]
        code2, out2, _ = _run(["gh", "issue", "list", "--state", "open",
                               "--json", "number,title,labels"], ctx.root, timeout=120)
        issues: list[dict[str, Any]] = json.loads(out2) if code2 == 0 and out2.strip() else []
        gate_issues = [i for i in issues
                       if any(str(l.get("name", "")).startswith("gate:") for l in i.get("labels", []))]
        metrics = {"runs": len(runs), "failed_runs": len(failures), "open_issues": len(issues),
                   "open_gate_issues": len(gate_issues), "mode": "online"}
        if failures or gate_issues:
            motivo = []
            if failures:
                motivo.append(f"{len(failures)} corrida(s) de CI com falha")
            if gate_issues:
                motivo.append(f"{len(gate_issues)} issue(s) de gate aberta(s)")
            return self.envelope(Status.PENDING, "continuidade necessária: " + "; ".join(motivo),
                                 started=started, addenda=addenda, metrics=metrics)
        return self.envelope(Status.SUCCESS, "CI verde e sem issues de gate abertas",
                             started=started, addenda=addenda, metrics=metrics)


class ReleaseGateway(Action):
    """Gateway exclusivo BPMN: agrega os envelopes anteriores e roteia a continuidade."""

    def __init__(self, spec: GateSpec, previous: Sequence[Envelope] = ()) -> None:
        super().__init__(spec)
        self.previous = list(previous)

    def run(self, ctx: Context, started: float) -> Envelope:
        blocking = [e for e in self.previous if e.status not in (Status.SUCCESS, Status.SKIPPED)]
        metrics = {
            "gates_ok": sum(1 for e in self.previous if e.status == Status.SUCCESS),
            "gates_total": len(self.previous),
            "blocking": [e.gate for e in blocking],
        }
        if blocking:
            first = blocking[0]
            return self.envelope(Status(first.status) if first.status != Status.PENDING else Status.PENDING,
                                 f"produção bloqueada por '{first.gate}': {first.message}",
                                 started=started, metrics=metrics)
        return self.envelope(Status.SUCCESS,
                             "todos os gates aprovados — entrega pronta para uso (produção)",
                             started=started, metrics=metrics)


class IssueFactory:
    """Gera a instrução da próxima issue (mesma se reprovou; próxima indexada se aprovou)."""

    def __init__(self, store: PipelineStore) -> None:
        self.store = store

    def build(self, envelopes: Sequence[Envelope]) -> NextIssue | None:
        blocking = [e for e in envelopes if e.status not in (Status.SUCCESS, Status.SKIPPED)]
        if blocking:
            env = blocking[0]
            spec = blueprint.BY_ID.get(env.gate)
            gate, direction = env.gate, env.direction
            nxt = blueprint.after(gate)
            reason = f"gate '{gate}' reprovado (status {env.status}): {env.message}"
            title = f"[gate:{gate}] {spec.name if spec else gate}"
        else:
            last = envelopes[-1] if envelopes else None
            spec = blueprint.BY_ID.get(last.gate) if last else None
            gate = last.gate if last else "release"
            direction = "continue"
            nxt = None
            reason = "todos os gates aprovados — entrega concluída"
            title = "[gate:done] Fluxo concluído: publicação e uso da base + skill"

        instructions = list(spec.acceptance) if spec else []
        if spec:
            instructions = [f"executar: `{spec.action}`", *instructions]
        if nxt:
            instructions.append(f"após aprovar, o próximo gate indexado é '{nxt.id}' ({nxt.name})")
        state_blob = json.dumps([e.to_dict() for e in envelopes], ensure_ascii=False, sort_keys=True)
        digest = hashlib.sha1(state_blob.encode("utf-8")).hexdigest()[:8]
        key = f"{gate}:{direction}:{digest}"

        body = self._body(title, reason, gate, direction, instructions,
                          list(spec.acceptance) if spec else [], envelopes, key)
        rec = self.store.issue(key)
        self.store.save_issue(IssueRecord(key=key, title=title, gate=gate, direction=direction,
                                          reason=reason, body=body,
                                          number=rec.number if rec else None,
                                          url=rec.url if rec else None,
                                          state="proposed"))
        return NextIssue(key=key, title=title, gate=gate, direction=direction, reason=reason,
                         number=rec.number if rec else None, url=rec.url if rec else None,
                         instructions=instructions,
                         acceptance=list(spec.acceptance) if spec else [])

    @staticmethod
    def _body(title: str, reason: str, gate: str, direction: str, instructions: Sequence[str],
              acceptance: Sequence[str], envelopes: Sequence[Envelope], key: str) -> str:
        linhas = [
            f"## {title}",
            "",
            f"**Gate:** `{gate}` · **Direção:** `{direction}` · **Chave determinística:** `{key}`",
            f"**Motivo:** {reason}",
            "",
            "### Instruções (ordem determinística)",
            "",
        ]
        linhas += [f"{i}. {txt}" for i, txt in enumerate(instructions, 1)]
        linhas += ["", "### Critérios de aceite", ""]
        linhas += [f"- [ ] {a}" for a in acceptance] or ["- [ ] gate aprovado com status 0"]
        linhas += [
            "",
            "### Saída obrigatória (contrato do envelope JSON)",
            "",
            "```json",
            json.dumps({"id": "<gate>:<hash>", "gate": gate, "status": 0,
                        "message": "<mensagem>", "direction": direction,
                        "addenda": [{"kind": "report", "path": "<caminho>"}],
                        "next_issue": {"key": key, "gate": gate}}, ensure_ascii=False, indent=2),
            "```",
            "",
            "### Estado medido nesta execução",
            "",
            "| Gate | Status | Mensagem |",
            "| --- | --- | --- |",
        ]
        for e in envelopes:
            linhas.append(f"| `{e.gate}` | {e.status} ({e.direction}) | {e.message[:120]} |")
        linhas += ["", f"_Gerado por `pipeline.factory` em {utcnow()} — blueprint "
                       f"{blueprint.BLUEPRINT_ID}._"]
        return "\n".join(linhas)


class Orchestrator:
    """Executa o blueprint em ordem, persiste envelopes e decide a continuidade."""

    ACTIONS: dict[str, type[Action]] = {
        "tests": TestsAction, "capture": CaptureAction, "conformity": ConformityAction,
        "site": SiteAction, "skill": SkillAction, "ci-issues": CiIssuesAction,
    }

    def __init__(self, store: PipelineStore, ctx: Context) -> None:
        self.store = store
        self.ctx = ctx
        self.factory = IssueFactory(store)

    def run(self, only: Sequence[str] | None = None) -> dict[str, Any]:
        started = time.monotonic()
        self.store.start_run(self.ctx.run_id, self.ctx.trigger)
        envelopes: list[Envelope] = []
        specs = [g for g in blueprint.ordered() if not only or g.id in only]
        for spec in specs:
            if spec.kind == "gateway":
                action: Action = ReleaseGateway(spec, previous=envelopes)
            else:
                action = self.ACTIONS[spec.id](spec)
            env = action.execute(self.ctx)
            self.store.record(self.ctx.run_id, env)
            envelopes.append(env)

        next_issue = self.factory.build(envelopes)
        if next_issue:
            (self.ctx.ci / "next-issue.md").write_text(
                self.store.issue(next_issue.key).body, encoding="utf-8")
            for env in envelopes:
                env.next_issue = next_issue

        blocking = [e for e in envelopes if e.status not in (Status.SUCCESS, Status.SKIPPED)]
        final = blocking[0].status if blocking else Status.SUCCESS
        direction = blocking[0].direction if blocking else "continue"
        summary = f"{len(envelopes) - len(blocking)}/{len(envelopes)} gates aprovados"
        self.store.finish_run(self.ctx.run_id, int(final), direction,
                              next_issue.key if next_issue else None, summary)

        state = {
            "blueprint": blueprint.BLUEPRINT_ID,
            "run_id": self.ctx.run_id,
            "trigger": self.ctx.trigger,
            "status": int(final),
            "status_label": Status(int(final)).name.lower(),
            "direction": direction,
            "message": summary,
            "next_issue": next_issue.to_dict() if next_issue else None,
            "envelopes": [e.to_dict() for e in envelopes],
            "store": self.store.state(),
            "generated_at": utcnow(),
        }
        out = self.ctx.ci / "pipeline-state.json"
        out.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        state["_path"] = str(out)
        state["_duration_s"] = round(time.monotonic() - started, 3)
        return state


def _mod(name: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(name) is not None


def _int(text: str, pattern: str) -> int:
    m = re.search(pattern, text)
    return int(m.group(1)) if m else 0
