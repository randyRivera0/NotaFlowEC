from app.frontend.data import CASES
from app.integrations.sri_source import MockSRISource
from app.services.validation import ValidationService


def result_by_code(report: dict[str, object], code: str) -> dict[str, object]:
    results = report["results"]
    assert isinstance(results, list)
    return next(item for item in results if item["code"] == code)


def test_valid_title_can_prepare_negotiation() -> None:
    report = ValidationService(MockSRISource()).validate(CASES[0])

    assert report["next_action"] == "Preparar negociación"
    assert all(item["passed"] for item in report["results"])
    assert report["requires_human_approval"] is True


def test_balance_mismatch_and_missing_document_are_explained() -> None:
    report = ValidationService(MockSRISource()).validate(CASES[1])

    assert result_by_code(report, "BALANCE_MATCH")["passed"] is False
    assert result_by_code(report, "REQUIRED_DOCUMENTS")["passed"] is False
    assert result_by_code(report, "BALANCE_MATCH")["evidence"]
    assert report["next_action"] == "Solicitar documento"


def test_blocked_title_is_sent_to_compliance() -> None:
    report = ValidationService(MockSRISource()).validate(CASES[2])

    assert result_by_code(report, "TITLE_NOT_BLOCKED")["passed"] is False
    assert report["next_action"] == "Enviar a cumplimiento"


def test_unknown_risky_title_is_sent_to_compliance() -> None:
    report = ValidationService(MockSRISource()).validate(CASES[3])

    assert result_by_code(report, "TITLE_EXISTS")["passed"] is False
    assert result_by_code(report, "NO_RISK_MATCH")["passed"] is False
    assert report["next_action"] == "Enviar a cumplimiento"
