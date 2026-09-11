from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from thinking_patterns.core.decision_compiler import (
    Assumption,
    DecisionCase,
    Evidence,
    Option,
    compile_decision,
)


def _tuple_of_strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("evidence_ids debe ser una lista")
    return tuple(str(item) for item in value)


def decision_case_from_dict(payload: dict[str, Any]) -> DecisionCase:
    try:
        options = tuple(
            Option(
                id=str(item["id"]),
                title=str(item["title"]),
                rationale=str(item.get("rationale", "")),
                evidence_ids=_tuple_of_strings(item.get("evidence_ids", [])),
            )
            for item in payload["options"]
        )
        evidence = tuple(
            Evidence(
                id=str(item["id"]),
                claim=str(item["claim"]),
                source=str(item["source"]),
                quality=float(item.get("quality", 0.5)),
            )
            for item in payload.get("evidence", [])
        )
        assumptions = tuple(
            Assumption(
                id=str(item["id"]),
                statement=str(item["statement"]),
                falsifier=str(item.get("falsifier", "")),
                consequence_if_false=str(
                    item.get("consequence_if_false", "")
                ),
            )
            for item in payload.get("assumptions", [])
        )

        reversibility = str(payload.get("reversibility", "unknown"))
        if reversibility not in {"high", "medium", "low", "unknown"}:
            raise ValueError(
                "reversibility debe ser high, medium, low o unknown"
            )

        return DecisionCase(
            decision_id=str(payload["decision_id"]),
            question=str(payload["question"]),
            options=options,
            selected_option_id=str(payload["selected_option_id"]),
            evidence=evidence,
            assumptions=assumptions,
            expected_outcome=str(payload.get("expected_outcome", "")),
            success_metric=str(payload.get("success_metric", "")),
            review_by=str(payload.get("review_by", "")),
            reversibility=reversibility,  # type: ignore[arg-type]
            rollback_trigger=str(payload.get("rollback_trigger", "")),
        )
    except KeyError as exc:
        raise ValueError(f"Falta campo requerido: {exc.args[0]}") from exc
    except TypeError as exc:
        raise ValueError("El JSON de decisión tiene una estructura inválida") from exc


def compile_file(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("La raíz del archivo debe ser un objeto JSON")

    case = decision_case_from_dict(payload)
    return asdict(compile_decision(case))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="decision-compile",
        description=(
            "Compila una decisión estructurada y ejecuta revisión adversarial "
            "determinística."
        ),
    )
    parser.add_argument("file", type=Path, help="Ruta al decision case JSON")
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Devuelve exit code 2 si el veredicto no es ready.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Imprime JSON en una sola línea.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        result = compile_file(args.file)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(
            json.dumps(
                {"ok": False, "error": str(exc)},
                ensure_ascii=False,
            )
        )
        return 1

    print(
        json.dumps(
            {"ok": True, "compiled_decision": result},
            ensure_ascii=False,
            indent=None if args.compact else 2,
        )
    )

    if args.require_ready and result["verdict"] != "ready":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
