CASES: list[dict[str, object]] = [
    {"id": "EXP-2026-001", "holder": "Corporación Andina S.A.", "ruc": "1790012345001", "title": "NC-001872", "amount": 48500.00, "balance": 48500.00, "documents": ["nota_credito"], "status": "En validación", "updated": "10 jul 2026"},
    {"id": "EXP-2026-002", "holder": "Exportadora del Pacífico Cía. Ltda.", "ruc": "0992456789001", "title": "NC-001945", "amount": 72150.75, "balance": 72150.75, "documents": [], "status": "Documentos pendientes", "updated": "09 jul 2026"},
    {"id": "EXP-2026-003", "holder": "Servicios Integrales Quito S.A.", "ruc": "1791987654001", "title": "NC-002011", "amount": 25300.00, "balance": 25300.00, "documents": ["nota_credito"], "status": "Revisión de cumplimiento", "updated": "08 jul 2026"},
    {"id": "EXP-2026-004", "holder": "Industrias Sierra Norte S.A.", "ruc": "1792233445001", "title": "NC-002034", "amount": 93800.50, "balance": 93800.50, "documents": ["nota_credito"], "status": "Revisión de cumplimiento", "updated": "07 jul 2026"},
]

for case in CASES:
    case["amount_display"] = f"$ {case['amount']:,.2f}"
    case.setdefault("responsible", "Ana Ortiz")
    case.setdefault("observations", [])
    case.setdefault(
        "history",
        [{"date": case["updated"], "responsible": "Ana Ortiz", "event": "Expediente creado"}],
    )
    case.setdefault("next_action", "Ejecutar validaciones")


def find_case(case_id: str) -> dict[str, object] | None:
    return next((case for case in CASES if case["id"] == case_id), None)
