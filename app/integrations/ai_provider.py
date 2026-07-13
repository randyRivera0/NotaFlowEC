from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AISuggestion:
    field: str
    value: str
    confidence: float
    source: str


class AIProvider(ABC):
    """Contract for providers that assist document intake."""

    @abstractmethod
    def extract_title_data(self, document_name: str) -> list[AISuggestion]:
        """Return suggestions without persisting or approving them."""


class MockAIProvider(AIProvider):
    """Deterministic provider used by the offline hackathon demo."""

    def extract_title_data(self, document_name: str) -> list[AISuggestion]:
        source = document_name or "Ingreso manual"
        return [
            AISuggestion("Titular", "Corporación Andina S.A.", 0.96, source),
            AISuggestion("RUC", "1790012345001", 0.98, source),
            AISuggestion("Número de título", "NC-002145", 0.93, source),
            AISuggestion("Tipo de nota", "Nota de crédito tributaria", 0.91, source),
            AISuggestion("Valor nominal", "48500.00", 0.89, source),
            AISuggestion("Saldo", "48500.00", 0.87, source),
        ]
