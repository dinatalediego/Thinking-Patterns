from thinking_patterns.core.decision_compiler import (
    Assumption,
    DecisionCase,
    Evidence,
    Option,
    compile_decision,
)


def test_well_formed_decision_is_ready():
    case = DecisionCase(
        decision_id="pricing-001",
        question="¿Subimos 3% el precio de la tipología M1?",
        options=(
            Option(
                id="hold",
                title="Mantener precio",
                rationale="Preservar velocidad de absorción",
                evidence_ids=("e1",),
            ),
            Option(
                id="raise",
                title="Subir 3%",
                rationale="Absorción por encima del objetivo",
                evidence_ids=("e1", "e2"),
            ),
        ),
        selected_option_id="raise",
        evidence=(
            Evidence("e1", "Absorción supera objetivo", "DW", 0.95),
            Evidence("e2", "Gap de precio vs comparables", "Mercado", 0.85),
        ),
        assumptions=(
            Assumption(
                id="a1",
                statement="La demanda tolera el incremento",
                falsifier="La conversión cae >15% vs baseline",
                consequence_if_false="Revertir el aumento",
            ),
        ),
        expected_outcome="Mayor ingreso sin deterioro material de conversión",
        success_metric="Ingreso incremental y conversión a 30 días",
        review_by="2026-10-11",
        reversibility="high",
    )

    result = compile_decision(case)

    assert result.verdict == "ready"
    assert result.readiness_score >= 0.80
    assert not [f for f in result.findings if f.severity == "error"]


def test_missing_alternative_blocks_readiness():
    case = DecisionCase(
        decision_id="lead-001",
        question="¿Asignar este lead al asesor A?",
        options=(Option(id="a", title="Asesor A"),),
        selected_option_id="a",
    )

    result = compile_decision(case)

    assert result.verdict == "not_ready"
    assert any(f.code == "O001" for f in result.findings)
    assert any(f.code == "E001" for f in result.findings)
