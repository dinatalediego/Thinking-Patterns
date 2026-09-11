import json

from thinking_patterns.cli import main


def test_cli_compiles_ready_case(tmp_path, capsys):
    payload = {
        "decision_id": "pricing-test",
        "question": "¿Aumentar precio?",
        "options": [
            {
                "id": "hold",
                "title": "Mantener",
                "rationale": "Control",
                "evidence_ids": ["e1"],
            },
            {
                "id": "raise",
                "title": "Subir",
                "rationale": "Captura valor",
                "evidence_ids": ["e1", "e2"],
            },
        ],
        "selected_option_id": "raise",
        "evidence": [
            {"id": "e1", "claim": "Absorción alta", "source": "DW", "quality": 0.95},
            {"id": "e2", "claim": "Gap mercado", "source": "Mercado", "quality": 0.90},
        ],
        "assumptions": [
            {
                "id": "a1",
                "statement": "Elasticidad tolerable",
                "falsifier": "Conversión cae >15%",
                "consequence_if_false": "Rollback",
            }
        ],
        "expected_outcome": "Ingreso incremental",
        "success_metric": "Margen + conversión",
        "review_by": "2026-10-11",
        "reversibility": "high",
    }
    path = tmp_path / "decision.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = main([str(path), "--require-ready", "--compact"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output["ok"] is True
    assert output["compiled_decision"]["verdict"] == "ready"


def test_cli_gate_fails_not_ready_case(tmp_path, capsys):
    payload = {
        "decision_id": "bad-decision",
        "question": "¿Hacerlo?",
        "options": [{"id": "yes", "title": "Sí"}],
        "selected_option_id": "yes",
    }
    path = tmp_path / "decision.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    exit_code = main([str(path), "--require-ready", "--compact"])
    output = json.loads(capsys.readouterr().out)

    assert exit_code == 2
    assert output["compiled_decision"]["verdict"] == "not_ready"
