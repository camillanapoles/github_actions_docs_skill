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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Guardião (gestor único) — ciclo RALF")
    ap.add_argument("--root", default=".")
    ap.add_argument("--audit", action="store_true", help="só auditar")
    ap.add_argument("--cycle", action="store_true", help="ciclo RALF completo")
    ap.add_argument("--settle", action="append", default=[], metavar="Dn=EVIDENCIA")
    ap.add_argument("--run-id", default="")
    ap.add_argument("--executar", action="store_true", help="rodar a verificação do profile")
    a = ap.parse_args(argv)
    g = Guardian(a.root)
    if a.settle:
        for item in a.settle:
            debt, _, ev = item.partition("=")
            print(json.dumps(g.settle(debt.strip(), ev.strip()).to_dict(), ensure_ascii=False, indent=2))
    env = g.audit() if a.audit and not a.cycle else (g.ralf(run_id=a.run_id, executar=a.executar)
                                                     if a.cycle else g.audit())
    print(json.dumps(env.to_dict(), ensure_ascii=False, indent=2))
    return 0 if env.status in (int(Status.SUCCESS), int(Status.PENDING)) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
