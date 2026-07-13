from app.integrations.ai_provider import MockAIProvider


def test_agent_returns_coherent_traceable_suggestions() -> None:
    suggestions = MockAIProvider().extract_title_data("nota_credito_demo.pdf")

    fields = {suggestion.field for suggestion in suggestions}
    assert fields == {
        "Titular",
        "RUC",
        "Número de título",
        "Tipo de nota",
        "Valor nominal",
        "Saldo",
    }
    assert all(suggestion.value for suggestion in suggestions)
    assert all(0 <= suggestion.confidence <= 1 for suggestion in suggestions)
    assert all(suggestion.source == "nota_credito_demo.pdf" for suggestion in suggestions)
