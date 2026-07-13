from __future__ import annotations

from dataclasses import asdict

from app.frontend.data import CASES
from app.integrations.sri_source import MockSRISource
from app.rules.title_rules import ValidationResult, validate_case


ACTION_PRIORITY = {
    "Enviar a cumplimiento": 0,
    "Solicitar documento": 1,
    "Actualizar dato": 2,
    "Revisar expediente previo": 3,
    "Preparar negociación": 4,
}


class ValidationService:
    def __init__(self, source: MockSRISource) -> None:
        self.source = source

    def validate(self, case: dict[str, object]) -> dict[str, object]:
        title = str(case.get("title") or "")
        registry = self.source.find_title(title)
        duplicate_count = sum(1 for item in CASES if item.get("title") == title)
        results = validate_case(case, registry, duplicate_count)
        failed = [item for item in results if not item.passed]
        next_action = (
            min((item.action for item in failed), key=lambda action: ACTION_PRIORITY[action])
            if failed
            else "Preparar negociación"
        )
        return {
            "results": [asdict(item) for item in self._prioritize(results)],
            "next_action": next_action,
            "source": "SRI simulado · corte 11 jul 2026",
            "requires_human_approval": True,
        }

    @staticmethod
    def _prioritize(results: list[ValidationResult]) -> list[ValidationResult]:
        severity = {"critical": 0, "warning": 1, "info": 2}
        return sorted(results, key=lambda item: (item.passed, severity[item.severity]))
