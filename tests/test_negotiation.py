import pytest

from app.services.negotiation import NegotiationService


def make_case() -> dict[str, object]:
    return {
        "id": "EXP-TEST-001",
        "holder": "Cliente de prueba",
        "ruc": "1790012345001",
        "title": "NC-TEST",
        "amount": 10_000.00,
        "balance": 8_000.00,
        "responsible": "Ana Ortiz",
        "history": [],
        "observations": [],
    }


def test_draft_calculates_gross_commission_and_net() -> None:
    case = make_case()
    draft = NegotiationService().generate_draft(case, 90, 2)

    assert draft["gross_value"] == 7_200.00
    assert draft["commission"] == 144.00
    assert draft["net_value"] == 7_056.00
    assert draft["status"] == "BORRADOR"
    assert case["history"]


def test_sensitive_action_requires_a_draft() -> None:
    case = make_case()

    with pytest.raises(ValueError, match="borrador"):
        NegotiationService().request_approval(case, "Transferencia", "Revisar soporte")


@pytest.mark.parametrize("action", ["Negociación", "Liquidación", "Transferencia", "Endoso"])
def test_regulated_actions_only_create_human_approval_requests(action: str) -> None:
    case = make_case()
    service = NegotiationService()
    service.generate_draft(case, 100, 1)

    service.request_approval(case, action, "Validar antes de continuar")

    assert case["status"] == "Aprobación solicitada"
    assert case["next_action"] == f"Revisión humana de {action.lower()}"
    assert case["observations"] == ["Validar antes de continuar"]
    assert "aprobación humana" in case["history"][-1]["event"]


def test_invalid_percentages_are_rejected() -> None:
    service = NegotiationService()

    with pytest.raises(ValueError):
        service.generate_draft(make_case(), 0, 1)
    with pytest.raises(ValueError):
        service.generate_draft(make_case(), 100, -1)
