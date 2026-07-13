from __future__ import annotations

from dataclasses import asdict
from datetime import date

from app.frontend.data import CASES
from app.integrations.ai_provider import AIProvider, AISuggestion


class IntakeService:
    def __init__(self, ai_provider: AIProvider) -> None:
        self.ai_provider = ai_provider

    def suggest(self, document_name: str) -> list[dict[str, object]]:
        return [
            {
                **asdict(item),
                "date": date.today().isoformat(),
                "status": "Pendiente",
            }
            for item in self.ai_provider.extract_title_data(document_name)
        ]

    def find_background(self, ruc: str, title: str) -> list[dict[str, object]]:
        normalized_ruc = ruc.strip().lower()
        normalized_title = title.strip().lower()
        return [
            {
                "case_id": case["id"],
                "holder": case["holder"],
                "ruc": case["ruc"],
                "title": case["title"],
                "date": case["updated"],
                "source": "Expediente interno",
                "status": case["status"],
            }
            for case in CASES
            if (normalized_ruc and normalized_ruc in str(case["ruc"]).lower())
            or (normalized_title and normalized_title in str(case["title"]).lower())
        ]

    def create_case(self, values: dict[str, object]) -> dict[str, object]:
        sequence = len(CASES) + 1
        amount = float(values.get("amount") or 0)
        case = {
            "id": f"EXP-2026-{sequence:03d}",
            "holder": str(values.get("holder") or "Sin titular"),
            "ruc": str(values.get("ruc") or ""),
            "title": str(values.get("title") or ""),
            "amount": amount,
            "balance": float(values.get("balance") or amount),
            "documents": list(values.get("documents") or ["nota_credito"]),
            "amount_display": f"$ {amount:,.2f}",
            "status": "Datos confirmados",
            "updated": date.today().strftime("%d %b %Y"),
            "responsible": "Ana Ortiz",
            "observations": [],
            "history": [
                {
                    "date": date.today().strftime("%d %b %Y"),
                    "responsible": "Ana Ortiz",
                    "event": "Expediente creado con datos aprobados",
                }
            ],
            "next_action": "Ejecutar validaciones",
        }
        CASES.append(case)
        return case
