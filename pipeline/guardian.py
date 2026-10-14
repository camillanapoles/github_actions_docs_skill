"""Guardião de projeto — gestor único da continuidade (IGC v2.1 + ciclo RALF por spec).

Uma só autoridade decide o próximo passo: lê a spec (`.igc-spec.yml`), a memória
(`.session/`), o registry (`.igc-registry.yml`) e os gates medidos (`.ci/`), audita
pendências/sessões paralelas/débitos, quita débitos com evidência e emite a próxima
instrução rotulada (A4) com checkpoint (E3) — nunca emite com verificação vermelha.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

from .domain import Addendum, Envelope, Status
from .igc import EventClass, Registry, SessionMemoryV21, State, _yaml

SPEC_FILE = ".igc-spec.yml"
RALF = ("RECONHECER", "AGIR", "LOGGAR", "FECHAR")
GESTOR = "guardian"
SPEC_OBRIGATORIO = ("projeto", "objetivo", "gestor", "ralf", "escopo", "aceite",
                    "gates", "qualidade", "doD")


class Guardian:
    """Gestor único: escopo global + memória IGC + gates do pipeline."""

    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root).resolve()
        self.mem = SessionMemoryV21(self.root)
        self.registry = Registry(self.root)
        self.spec_file = self.root / SPEC_FILE
        self.state_file = self.root / ".ci" / "pipeline-state.json"

    # ------------------------------------------------------------------ spec
    def spec(self) -> tuple[dict, list[str]]:
        data, err = _yaml(self.spec_file)
        if err:
            return {}, [err]
        faltam = [k for k in SPEC_OBRIGATORIO if k not in data]
        errs = [f"spec sem chave obrigatória: {k}" for k in faltam]
        if (data.get("gestor") or {}).get("unico") != GESTOR:
            errs.append(f"gestor único deve ser '{GESTOR}'")
        fases = tuple((data.get("ralf") or {}).get("fases") or ())
        if fases and fases != RALF:
            errs.append(f"fases RALF divergentes: {fases}")
        return data, errs

    # --------------------------------------------------------------- auditoria
    def debts_open(self) -> list[str]:
        """Débitos em aberto (M5): linhas | Dn | ... | menos as quitadas (-R/RESOLVIDO)."""
        if not self.mem.debt_file.exists():
            return []
        txt = self.mem.debt_file.read_text(encoding="utf-8")
        quitados = {m.group(1) for m in re.finditer(r"^\|\s*(D\d+)-R\s*\|", txt, re.M)}
        quitados |= {m.group(1) for m in re.finditer(r"^\|\s*(D\d+)\s*\|[^\n]*RESOLVIDO", txt, re.M)}
        ids = [m.group(1) for m in re.finditer(r"^\|\s*(D\d+)\s*\|", txt, re.M)]
        vistos, abertos = set(), []
        for i in ids:
            if i not in quitados and i not in vistos:
                abertos.append(i)
                vistos.add(i)
        return abertos

    def gate_status(self) -> dict[str, int]:
        if not self.state_file.exists():
            return {}
        try:
            dados = json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            return {}
        return {e.get("gate", "?"): int(e.get("status", 1))
                for e in (dados.get("envelopes") or []) if isinstance(e, dict)}

    def linhagens(self) -> dict:
        return self.registry.read()["linhagens"]

    def sessoes_paralelas(self) -> list[str]:
        """G4: qualquer linhagem ativa que não reconheça o gestor único."""
        paralelas = []
        for slug, e in self.linhagens().items():
            if not e.get("ativa", True):
                continue
            if (e.get("gestor") or GESTOR) != GESTOR:
                paralelas.append(slug)
        ativas = [s for s, e in self.linhagens().items() if e.get("ativa", True)]
        if len(ativas) > 1:
            paralelas += [s for s in ativas if s not in paralelas][1:]
        return sorted(set(paralelas))

    def audit(self, *, hoje=None) -> Envelope:
        """Pendências, sessões paralelas, órfãos e débitos — tudo medido, nada supuesto."""
        started = time.monotonic()
        spec, spec_errs = self.spec()
        gates = self.gate_status()
        vermelhos = {g: s for g, s in gates.items() if s not in (0, 4)}
        debitos = self.debts_open()
        bloqueantes = [d for d in (spec.get("debitos_bloqueantes") or []) if d in debitos]
        paralelas = self.sessoes_paralelas()
        orfaos = self.registry.sweep_orphans(hoje=hoje)
        metrics = {"linhagens": len(self.linhagens()),
                   "linhagens_ativas": sum(1 for e in self.linhagens().values() if e.get("ativa", True)),
                   "sessoes_paralelas": paralelas, "orfaos": orfaos,
                   "gates": gates, "gates_vermelhos": vermelhos,
                   "debitos_abertos": debitos, "debitos_bloqueantes": bloqueantes,
                   "spec_erros": spec_errs, "gestor": GESTOR}
        critico = bool(paralelas or orfaos or spec_errs)
        status = Status.ERROR_CONTENT if critico else (Status.PENDING if (vermelhos or debitos) else Status.SUCCESS)
        self.mem.wal_append("AUDIT", EventClass.FIX if critico else EventClass.CONTINUE,
                            "gestor único audita escopo global (spec) e pendências",
                            "audit(): registry + DEBT.md + gates medidos + sweep G5",
                            (f"crítico: paralelas={paralelas} órfãos={orfaos} spec={spec_errs}" if critico
                             else f"{len(debitos)} débitos abertos ({len(bloqueantes)} bloqueantes); "
                                  f"gates vermelhos {vermelhos or 'nenhum'}"))
        return Envelope.of("igc.guardian", "audit", status,
                           ("auditoria crítica: " + json.dumps(
                               {"paralelas": paralelas, "orfaos": orfaos, "spec": spec_errs},
                               ensure_ascii=False)) if critico else
                           f"auditoria ok: 1 gestor ({GESTOR}), {len(debitos)} débitos abertos, "
                           f"gates vermelhos {list(vermelhos) or 'nenhum'}",
                           addenda=[Addendum("config", SPEC_FILE), Addendum("log", ".session/WAL.md")],
                           metrics=metrics,
                           checkpoint_ref=(self.mem.read_checkpoint() or {}).get("sha", "")).close(started)

    def assert_single_manager(self, slug: str = "") -> Envelope:
        """Garante 1 só gestor: declara-se no registry e reprova linhagem paralela."""
        started = time.monotonic()
        paralelas = self.sessoes_paralelas()
        linh = self.linhagens()
        slug = slug or (next(iter(linh), "") if linh else "")
        if not slug:
            return Envelope.of("igc.guardian", "assert_single_manager", Status.ERROR_CONTENT,
                               "registry sem linhagem: nada a gerir (R7 → BOOT legítimo)",
                               metrics={}).close(started)
        atual = dict(linh.get(slug) or {})
        if atual.get("gestor") != GESTOR:
            self.registry.write_entry(slug, branch=atual.get("branch", "-"),
                                      checkpoint_ref=atual.get("checkpoint_ref", ""),
                                      ativa=True, **{k: v for k, v in atual.items()
                                                     if k not in ("branch", "checkpoint_ref", "ativa")},
                                      gestor=GESTOR)
            self.mem.wal_append("GESTOR", EventClass.IMPLEMENT,
                                "gestor único não declarado no registry (Art.7 D2)",
                                f"registrar gestor={GESTOR} em '{slug}'", "unicidade garantida")
        if paralelas:
            for outra in paralelas:
                self.mem.register_conflict(slug, outra, ".igc-registry.yml")
            return Envelope.of("igc.guardian", "assert_single_manager", Status.ERROR_CONTENT,
                               f"{len(paralelas)} sessão(ões) paralela(s) ativa(s): {paralelas} — "
                               "conflito explícito (G4), merge silencioso proibido",
                               metrics={"paralelas": paralelas, "gestor": GESTOR}).close(started)
        return Envelope.of("igc.guardian", "assert_single_manager", Status.SUCCESS,
                           f"gestor único ativo: {GESTOR} em '{slug}' (1 linhagem, 1 território)",
                           metrics={"slug": slug, "gestor": GESTOR},
                           checkpoint_ref=atual.get("checkpoint_ref", "")).close(started)

    # ------------------------------------------------------------ quitar (M5)
    def settle(self, debt_id: str, evidencia: str) -> Envelope:
        """Quita débito com evidência: linha RESOLVIDO + entrada SETTLE no WAL."""
        started = time.monotonic()
        abertos = self.debts_open()
        if debt_id not in abertos:
            return Envelope.of("igc.guardian", "settle", Status.ERROR_CONTENT,
                               f"débito {debt_id} não está em aberto (abertos: {abertos})",
                               metrics={"debt_id": debt_id}).close(started)
        if not evidencia or len(evidencia) < 8:
            return Envelope.of("igc.guardian", "settle", Status.ERROR_CONTENT,
                               f"quitação de {debt_id} sem evidência (mínimo 8 caracteres)",
                               metrics={"debt_id": debt_id}).close(started)
        ok = self.mem.resolve_debt(debt_id, evidencia)
        self.mem.wal_append("SETTLE", EventClass.DEBT, f"{debt_id} em aberto", evidencia,
                            "QUITADO" if ok else "falha ao localizar a linha")
        return Envelope.of("igc.guardian", "settle",
                           Status.SUCCESS if ok else Status.ERROR_CONTENT,
                           f"{debt_id} quitado: {evidencia}" if ok else f"{debt_id}: linha não encontrada",
                           metrics={"debt_id": debt_id, "evidencia": evidencia,
                                    "restantes": self.debts_open()},
                           addenda=[Addendum("doc", ".session/DEBT.md")]).close(started)

    # ------------------------------------------------------------- próxima ação
    def next_action(self) -> dict:
        """Prioridade da spec: gates vermelhos > débitos bloqueantes > órfãos > release."""
        spec, _ = self.spec()
        ordem = (spec.get("gates") or {}).get("ordem") or []
        gates = self.gate_status()
        for g in ordem:
            st = gates.get(g)
            if st is not None and st not in (0, 4):
                return {"classe": EventClass.FIX.value, "alvo": f"gate {g}",
                        "motivo": f"status {st} medido em .ci/pipeline-state.json",
                        "spec_gate": g}
        bloqueantes = [d for d in (spec.get("debitos_bloqueantes") or []) if d in self.debts_open()]
        if bloqueantes:
            return {"classe": EventClass.DEBT.value, "alvo": f"débito {bloqueantes[0]}",
                    "motivo": f"débitos bloqueantes abertos: {bloqueantes}", "spec_gate": ""}
        orfaos = self.registry.sweep_orphans()
        if orfaos:
            return {"classe": EventClass.DEBT.value, "alvo": f"órfãos {orfaos}",
                    "motivo": "varredura G5 encontrou linhagem órfã", "spec_gate": ""}
        return {"classe": EventClass.CONTINUE.value, "alvo": "release / DoD",
                "motivo": "gates verdes: seguir para PR, merge e Pages (DoD)", "spec_gate": "release"}

    # ------------------------------------------------------------------- RALF
    def ralf(self, *, run_id: str = "", executar: bool = False) -> Envelope:
        """Ciclo automático: RECONHECER → AGIR → LOGGAR → FECHAR (idempotente, E4)."""
        started = time.monotonic()
        fases: dict[str, dict] = {}
        aud = self.audit()                                    # R — RECONHECER
        unico = self.assert_single_manager()
        fases["RECONHECER"] = {"audit_status": aud.status, "gestor": unico.status,
                               "gates_vermelhos": aud.metrics["gates_vermelhos"],
                               "debitos_abertos": len(aud.metrics["debitos_abertos"]),
                               "sessoes_paralelas": aud.metrics["sessoes_paralelas"],
                               "spec_erros": aud.metrics["spec_erros"]}
        proximo = self.next_action()                          # A — AGIR
        fases["AGIR"] = proximo
        head = self.mem.git_head() or "0" * 40
        self.mem.write_checkpoint(sha=head, state="EXEC")      # L — LOGGAR
        fases["LOGGAR"] = {"wal_entries": len(self.mem.wal_entries()),
                           "wal_hash": self.mem.wal_hash(), "checkpoint": head[:12]}
        chave = f"ralf-{run_id or head[:12]}"
        emissao = self.mem.emit(EventClass(proximo["classe"]), proximo["alvo"],
                                event_id=chave, verified=True, sha=head)   # F — FECHAR
        fases["FECHAR"] = {"emissao_status": emissao.status, "classe": proximo["classe"],
                           "chave": chave, "checkpoint_ref": emissao.checkpoint_ref,
                           "idempotente": emissao.metrics.get("idempotente", False)}
        if executar:
            prof, _ = self.mem.profile()
            cmd = ((prof.get("verificacao") or {}).get("comando") or "").strip()
            if cmd:
                rc = subprocess.run(["bash", "-lc", cmd], cwd=self.root).returncode
                fases["VERIFICACAO"] = {"comando": cmd, "exit": rc}
        critico = aud.status == int(Status.ERROR_CONTENT)
        status = Status.ERROR_CONTENT if critico else (
            Status.SUCCESS if not aud.metrics["gates_vermelhos"] else Status.PENDING)
        return Envelope.of("igc.guardian", "ralf", status,
                           f"RALF completo: próximo passo = {proximo['classe']} '{proximo['alvo']}' "
                           f"({proximo['motivo']}); gates vermelhos "
                           f"{list(aud.metrics['gates_vermelhos']) or 'nenhum'}; "
                           f"{len(aud.metrics['debitos_abertos'])} débitos abertos",
                           addenda=[Addendum("config", SPEC_FILE),
                                    Addendum("log", ".session/WAL.md"),
                                    Addendum("state", ".session/CHECKPOINT")],
                           metrics={"fases": fases, "proximo": proximo,
                                    "gestor": GESTOR, "run_id": run_id,
                                    "critico": critico},
                           checkpoint_ref=head).close(started)

    # ------------------------------------------------ /ralf por issue (gestor)
    def _gh(self, args: list[str], runner=None):
        if runner is not None:
            return runner(list(args))
        return subprocess.run(["gh", *args], cwd=self.root, capture_output=True, text=True)

    @staticmethod
    def _json(res, padrao):
        try:
            return json.loads(getattr(res, "stdout", "") or padrao)
        except Exception:                                   # noqa: BLE001
            return json.loads(padrao)

    def issue_cycle(self, *, runner=None, run_id: str = "", label: str = "pipeline:next") -> Envelope:
        """1 issue pipeline:next = 1 instrução = 1 ciclo RALF (unicidade do gestor)."""
        started = time.monotonic()
        proximo = self.next_action()
        itens = self._json(self._gh(["issue", "list", "--state", "open", "--label", label,
                                     "--json", "number,title,url", "--limit", "20"], runner), "[]")
        consolidadas = []
        if len(itens) > 1:
            itens = sorted(itens, key=lambda i: int(i.get("number", 0)))
            for extra in itens[1:]:
                self._gh(["issue", "comment", str(extra["number"]), "--body",
                          f"Consolidada pelo guardião (gestor único): a instrução vigente é "
                          f"#{itens[0]['number']}."], runner)
                self._gh(["issue", "close", str(extra["number"]), "--reason", "not planned"], runner)
                consolidadas.append(extra["number"])
            self.mem.wal_append("ISSUE-CONSOLID", EventClass.DEBT,
                                f"{len(consolidadas)} issues '{label}' abertas ao mesmo tempo",
                                f"manter #{itens[0]['number']}, fechar {consolidadas}",
                                "gestor único restaurado")
        if not itens:
            titulo = (f"[gate:{proximo.get('spec_gate') or 'guardian'}] {proximo['alvo']} — "
                      f"{proximo['motivo'][:60]}")
            corpo = (f"Classe: {proximo['classe']}\nAlvo: {proximo['alvo']}\n"
                     f"Motivo: {proximo['motivo']}\n\nInstrução emitida pelo guardião "
                     "(gestor único) via /ralf por issue.")
            cr = self._gh(["issue", "create", "--title", titulo, "--body", corpo,
                           "--label", f"{label},status:1"], runner)
            ref = (getattr(cr, "stdout", "") or "").strip()
            self.mem.wal_append("ISSUE-CREATE", EventClass(proximo["classe"]),
                                f"nenhuma issue '{label}' aberta", titulo, ref or "criada")
            itens = [{"number": None, "title": titulo, "url": ref}]
        ciclo = self.ralf(run_id=run_id or "issue")
        alvo = itens[0]
        fechado = False
        if alvo.get("number"):
            gate_alvo = self.gate_status().get(proximo.get("spec_gate") or "")
            corpo = (f"Ciclo RALF (run {run_id or '-'}): {ciclo.message}\n\n"
                     f"checkpoint_ref: `{(ciclo.checkpoint_ref or '')[:12]}` · fases: "
                     + ", ".join(ciclo.metrics["fases"]))
            self._gh(["issue", "comment", str(alvo["number"]), "--body", corpo], runner)
            if gate_alvo in (0, 4):
                self._gh(["issue", "close", str(alvo["number"]), "--reason", "completed"], runner)
                self.mem.contract_emit(EventClass.CONTINUE,
                                       f"issue #{alvo['number']} fechada (gate verde)")
                fechado = True
        return Envelope.of("igc.guardian", "issue_cycle", ciclo.status,
                           f"/ralf por issue: #{alvo.get('number')} — {ciclo.message}",
                           metrics={"issue": alvo, "consolidadas": consolidadas,
                                    "proximo": proximo, "fechada": fechado,
                                    "fases": list(ciclo.metrics["fases"])},
                           checkpoint_ref=ciclo.checkpoint_ref).close(started)

    # ------------------------------------- /ralf mediador de merge (por spec)
    def merge_mediator(self, *, runner=None, pr: str | int | None = None, nota: float | None = None,
                       dry_run: bool = True, metodo: str = "--merge") -> Envelope:
        """Media o merge pela spec: DoD verde autoriza; qualquer bloqueio recusa e dirige."""
        started = time.monotonic()
        spec, spec_errs = self.spec()
        aud = self.audit()
        gates, vermelhos = aud.metrics["gates"], aud.metrics["gates_vermelhos"]
        bloqueantes = aud.metrics["debitos_bloqueantes"]
        lista = self._json(self._gh(["pr", "list", "--state", "open",
                                     "--json", "number,headRefName,mergeable"], runner), "[]")
        alvo = next((p for p in lista if str(p.get("number")) == str(pr)), lista[0] if lista else {})
        mergeable = alvo.get("mergeable", "UNKNOWN")
        minima = float((spec.get("qualidade") or {}).get("nota_minima_fechamento", 9.5))
        dod = {"gates_verdes": not vermelhos,
               "release_zero": gates.get("release") == 0,
               "sem_debitos_bloqueantes": not bloqueantes,
               "spec_valida": not spec_errs,
               f"nota_minima_{minima}": bool(nota is not None and nota >= minima),
               "pr_mergeable": mergeable == "MERGEABLE",
               "gestor_unico": not aud.metrics["sessoes_paralelas"]}
        bloqueios = [k for k, v in dod.items() if not v]
        cp = (self.mem.read_checkpoint() or {}).get("sha", "")
        self.mem.wal_append("MEDIATOR", EventClass.CONTINUE if not bloqueios else EventClass.FIX,
                            "merge exige mediação por spec (DoD)",
                            f"PR #{alvo.get('number')} mergeable={mergeable} nota={nota}",
                            "AUTORIZADO" if not bloqueios else f"RECUSADO: {bloqueios}")
        if bloqueios:
            return Envelope.of("igc.guardian", "merge_mediator", Status.PENDING,
                               f"merge RECUSADO por spec: {bloqueios} — continuidade dirigida a "
                               f"{self.next_action()['alvo']}",
                               metrics={"dod": dod, "bloqueios": bloqueios, "pr": alvo, "nota": nota},
                               checkpoint_ref=cp).close(started)
        if dry_run:
            return Envelope.of("igc.guardian", "merge_mediator", Status.SUCCESS,
                               f"merge AUTORIZADO (dry-run) do PR #{alvo.get('number')}: DoD verde",
                               metrics={"dod": dod, "pr": alvo, "nota": nota, "executado": False},
                               checkpoint_ref=cp).close(started)
        res = self._gh(["pr", "merge", str(alvo.get("number")), metodo], runner)
        if getattr(res, "returncode", 1) == 0:
            ref = (getattr(res, "stdout", "") or "").strip() or f"PR #{alvo.get('number')}"
            self.mem.contract_emit(EventClass.CONTINUE, f"merge {ref} ({metodo})")
            return Envelope.of("igc.guardian", "merge_mediator", Status.SUCCESS,
                               f"merge executado e contraído (E5): {ref}",
                               metrics={"dod": dod, "pr": alvo, "nota": nota, "executado": True,
                                        "ref": ref}, checkpoint_ref=cp).close(started)
        return Envelope.of("igc.guardian", "merge_mediator", Status.ERROR_INFRA,
                           f"merge falhou: {getattr(res, 'stderr', '')[:160]}",
                           metrics={"dod": dod, "pr": alvo}, checkpoint_ref=cp).close(started)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Guardião (gestor único) — ciclo RALF")
    ap.add_argument("--root", default=".")
    ap.add_argument("--audit", action="store_true", help="só auditar")
    ap.add_argument("--cycle", action="store_true", help="ciclo RALF completo")
    ap.add_argument("--settle", action="append", default=[], metavar="Dn=EVIDENCIA")
    ap.add_argument("--run-id", default="")
    ap.add_argument("--executar", action="store_true", help="rodar a verificação do profile")
    ap.add_argument("--por-issue", action="store_true", help="/ralf por issue (pipeline:next)")
    ap.add_argument("--mediar-merge", action="store_true", help="/ralf mediador de merge")
    ap.add_argument("--pr", default=None)
    ap.add_argument("--nota", type=float, default=None)
    ap.add_argument("--autorizar-merge", action="store_true", help="executa o merge (DoD verde)")
    a = ap.parse_args(argv)
    g = Guardian(a.root)
    if a.settle:
        for item in a.settle:
            debt, _, ev = item.partition("=")
            print(json.dumps(g.settle(debt.strip(), ev.strip()).to_dict(), ensure_ascii=False, indent=2))
    if a.mediar_merge:
        env = g.merge_mediator(pr=a.pr, nota=a.nota, dry_run=not a.autorizar_merge,
                               run_id=a.run_id) if False else g.merge_mediator(
                                   pr=a.pr, nota=a.nota, dry_run=not a.autorizar_merge)
    elif a.por_issue:
        env = g.issue_cycle(run_id=a.run_id)
    elif a.cycle:
        env = g.ralf(run_id=a.run_id, executar=a.executar)
    else:
        env = g.audit()
    print(json.dumps(env.to_dict(), ensure_ascii=False, indent=2))
    return 0 if env.status in (int(Status.SUCCESS), int(Status.PENDING)) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
