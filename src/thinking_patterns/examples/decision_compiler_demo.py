from thinking_patterns.core.decision_compiler import (
    Assumption,
    DecisionCase,
    Evidence,
    Option,
    compile_decision,
    summarize_findings,
)

case = DecisionCase(
    decision_id="pricing-demo",
    question="¿Aumentar precio de una tipología con absorción alta?",
    options=(
        Option(
            id="hold",
            title="Mantener",
            rationale="Minimiza riesgo de frenar absorción",
            evidence_ids=("absorption",),
        ),
        Option(
            id="raise",
            title="Aumentar 3%",
            rationale="Captura disposición a pagar observada",
            evidence_ids=("absorption", "market_gap"),
        ),
    ),
    selected_option_id="raise",
    evidence=(
        Evidence(
            id="absorption",
            claim="Absorción 90d por encima de meta",
            source="medallio_dw",
            quality=0.95,
        ),
        Evidence(
            id="market_gap",
            claim="Precio m² por debajo de comparables",
            source="mercado longitudinal",
            quality=0.85,
        ),
    ),
    assumptions=(
        Assumption(
            id="elasticity",
            statement="El aumento no deteriorará fuertemente la conversión",
            falsifier="Conversión cae más de 15% vs baseline",
            consequence_if_false="Rollback de precio",
        ),
    ),
    expected_outcome="Aumentar ingreso esperado sin perder absorción objetivo",
    success_metric="Margen incremental + conversión a 30 días",
    review_by="2026-10-11",
    reversibility="high",
)

compiled = compile_decision(case)
print(compiled)
for line in summarize_findings(compiled.findings):
    print(line)
