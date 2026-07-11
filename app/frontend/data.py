CASES: list[dict[str, object]] = [
    {"id": "EXP-2026-001", "holder": "Corporación Andina S.A.", "ruc": "1790012345001", "title": "NC-001872", "amount": 48500.00, "status": "En validación", "updated": "10 jul 2026"},
    {"id": "EXP-2026-002", "holder": "Exportadora del Pacífico Cía. Ltda.", "ruc": "0992456789001", "title": "NC-001945", "amount": 72150.75, "status": "Documentos pendientes", "updated": "09 jul 2026"},
    {"id": "EXP-2026-003", "holder": "Servicios Integrales Quito S.A.", "ruc": "1791987654001", "title": "NC-002011", "amount": 25300.00, "status": "Listo para negociar", "updated": "08 jul 2026"},
    {"id": "EXP-2026-004", "holder": "Industrias Sierra Norte S.A.", "ruc": "1792233445001", "title": "NC-002034", "amount": 93800.50, "status": "Revisión de cumplimiento", "updated": "07 jul 2026"},
]

for case in CASES:
    case["amount_display"] = f"$ {case['amount']:,.2f}"


def find_case(case_id: str) -> dict[str, object] | None:
    return next((case for case in CASES if case["id"] == case_id), None)
