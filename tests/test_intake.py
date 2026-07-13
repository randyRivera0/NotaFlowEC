from app.integrations.ai_provider import MockAIProvider
from app.services.intake import IntakeService


def test_mock_ai_suggestions_include_traceability() -> None:
    suggestions = IntakeService(MockAIProvider()).suggest("nota.pdf")

    assert len(suggestions) == 6
    assert all(item["source"] == "nota.pdf" for item in suggestions)
    assert all(item["date"] for item in suggestions)
    assert all(item["status"] == "Pendiente" for item in suggestions)


def test_background_search_finds_ruc_or_title() -> None:
    service = IntakeService(MockAIProvider())

    by_ruc = service.find_background("1790012345001", "")
    by_title = service.find_background("", "NC-001945")

    assert by_ruc[0]["case_id"] == "EXP-2026-001"
    assert by_title[0]["case_id"] == "EXP-2026-002"
    assert by_ruc[0]["source"] == "Expediente interno"
