from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Literal


Severity = Literal["info", "warning", "error"]
Verdict = Literal["ready", "conditional", "not_ready"]


@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    source: str
    quality: float = 0.5

    def normalized_quality(self) -> float:
        return max(0.0, min(1.0, self.quality))


@dataclass(frozen=True)
class Assumption:
    id: str
    statement: str
    falsifier: str = ""
    consequence_if_false: str = ""


@dataclass(frozen=True)
class Option:
    id: str
    title: str
    rationale: str = ""
    evidence_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class DecisionCase:
    decision_id: str
    question: str
    options: tuple[Option, ...]
    selected_option_id: str
    evidence: tuple[Evidence, ...] = ()
    assumptions: tuple[Assumption, ...] = ()
    expected_outcome: str = ""
    success_metric: str = ""
    review_by: str = ""
    reversibility: Literal["high", "medium", "low", "unknown"] = "unknown"
    rollback_trigger: str = ""


@dataclass(frozen=True)
class ReviewFinding:
    code: str
    severity: Severity
    message: str


@dataclass(frozen=True)
class CompiledDecision:
    decision_id: str
    readiness_score: float
    verdict: Verdict
    dimensions: dict[str, float]
    findings: tuple[ReviewFinding, ...] = field(default_factory=tuple)


class DecisionCompiler:
    """Compile a decision into an auditable packet and adversarial review.

    This module intentionally does not call an LLM. It acts as a deterministic
    contract that an LLM, analyst, notebook, API, or human can use upstream.
    """

    weights = {
        "evidence": 0.30,
        "assumptions": 0.20,
        "alternatives": 0.20,
        "measurement": 0.20,
        "reversibility": 0.10,
    }

    def compile(self, case: DecisionCase) -> CompiledDecision:
        findings: list[ReviewFinding] = []
        evidence_score = self._evidence_score(case, findings)
        assumptions_score = self._assumptions_score(case, findings)
        alternatives_score = self._alternatives_score(case, findings)
        measurement_score = self._measurement_score(case, findings)
        reversibility_score = self._reversibility_score(case, findings)

        dimensions = {
            "evidence": evidence_score,
            "assumptions": assumptions_score,
            "alternatives": alternatives_score,
            "measurement": measurement_score,
            "reversibility": reversibility_score,
        }

        readiness = sum(
            dimensions[name] * weight for name, weight in self.weights.items()
        )
        readiness = round(max(0.0, min(1.0, readiness)), 4)

        if any(f.severity == "error" for f in findings) or readiness < 0.60:
            verdict: Verdict = "not_ready"
        elif readiness < 0.80 or any(f.severity == "warning" for f in findings):
            verdict = "conditional"
        else:
            verdict = "ready"

        return CompiledDecision(
            decision_id=case.decision_id,
            readiness_score=readiness,
            verdict=verdict,
            dimensions=dimensions,
            findings=tuple(findings),
        )

    def _evidence_score(
        self, case: DecisionCase, findings: list[ReviewFinding]
    ) -> float:
        if not case.evidence:
            findings.append(
                ReviewFinding(
                    "E001",
                    "error",
                    "La decisión no tiene evidencia explícita.",
                )
            )
            return 0.0

        evidence_ids = {item.id for item in case.evidence}
        referenced = {
            evidence_id
            for option in case.options
            for evidence_id in option.evidence_ids
            if evidence_id in evidence_ids
        }
        invalid_refs = {
            evidence_id
            for option in case.options
            for evidence_id in option.evidence_ids
            if evidence_id not in evidence_ids
        }
        if invalid_refs:
            findings.append(
                ReviewFinding(
                    "E002",
                    "error",
                    "Hay referencias de evidencia inexistentes: "
                    + ", ".join(sorted(invalid_refs)),
                )
            )

        quality = sum(e.normalized_quality() for e in case.evidence) / len(case.evidence)
        coverage = len(referenced) / len(evidence_ids)
        if coverage < 0.5:
            findings.append(
                ReviewFinding(
                    "E003",
                    "warning",
                    "Menos de la mitad de la evidencia está conectada a opciones.",
                )
            )

        return round(0.7 * quality + 0.3 * coverage, 4)

    def _assumptions_score(
        self, case: DecisionCase, findings: list[ReviewFinding]
    ) -> float:
        if not case.assumptions:
            findings.append(
                ReviewFinding(
                    "A001",
                    "warning",
                    "No se declararon supuestos; probablemente siguen implícitos.",
                )
            )
            return 0.4

        falsifiable = [
            a for a in case.assumptions if a.falsifier.strip()
        ]
        consequence_known = [
            a for a in case.assumptions if a.consequence_if_false.strip()
        ]

        for assumption in case.assumptions:
            if not assumption.falsifier.strip():
                findings.append(
                    ReviewFinding(
                        "A002",
                        "warning",
                        f"Supuesto {assumption.id} no tiene falsificador.",
                    )
                )

        return round(
            0.65 * (len(falsifiable) / len(case.assumptions))
            + 0.35 * (len(consequence_known) / len(case.assumptions)),
            4,
        )

    def _alternatives_score(
        self, case: DecisionCase, findings: list[ReviewFinding]
    ) -> float:
        option_ids = {option.id for option in case.options}
        if len(case.options) < 2:
            findings.append(
                ReviewFinding(
                    "O001",
                    "error",
                    "Una decisión necesita al menos dos alternativas comparables.",
                )
            )

        if case.selected_option_id not in option_ids:
            findings.append(
                ReviewFinding(
                    "O002",
                    "error",
                    "La alternativa seleccionada no existe en el set de opciones.",
                )
            )
            selected_valid = 0.0
        else:
            selected_valid = 1.0

        diversity = min(len(case.options) / 3.0, 1.0)
        rationale_rate = (
            sum(bool(option.rationale.strip()) for option in case.options)
            / max(len(case.options), 1)
        )
        return round(
            0.4 * diversity + 0.3 * rationale_rate + 0.3 * selected_valid,
            4,
        )

    def _measurement_score(
        self, case: DecisionCase, findings: list[ReviewFinding]
    ) -> float:
        checks = {
            "expected_outcome": bool(case.expected_outcome.strip()),
            "success_metric": bool(case.success_metric.strip()),
            "review_by": bool(case.review_by.strip()),
        }
        missing = [name for name, present in checks.items() if not present]
        if missing:
            findings.append(
                ReviewFinding(
                    "M001",
                    "warning",
                    "Falta cerrar el loop de medición: " + ", ".join(missing),
                )
            )
        return round(sum(checks.values()) / len(checks), 4)

    def _reversibility_score(
        self, case: DecisionCase, findings: list[ReviewFinding]
    ) -> float:
        base = {
            "high": 1.0,
            "medium": 0.8,
            "low": 0.55,
            "unknown": 0.35,
        }[case.reversibility]

        if case.reversibility == "unknown":
            findings.append(
                ReviewFinding(
                    "R001",
                    "warning",
                    "No se declaró la reversibilidad de la decisión.",
                )
            )

        if case.reversibility in {"medium", "low"} and not case.rollback_trigger.strip():
            findings.append(
                ReviewFinding(
                    "R002",
                    "warning",
                    "Una decisión difícil de revertir debería declarar un trigger de rollback.",
                )
            )
            base *= 0.75

        return round(base, 4)


def compile_decision(case: DecisionCase) -> CompiledDecision:
    return DecisionCompiler().compile(case)


def summarize_findings(findings: Iterable[ReviewFinding]) -> list[str]:
    return [f"[{item.severity.upper()}] {item.code}: {item.message}" for item in findings]
