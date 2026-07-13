from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegistryTitle:
    title: str
    ruc: str
    balance: float
    status: str
    blocked: bool


class MockSRISource:
    """Deterministic title registry used instead of a production SRI connection."""

    _titles = {
        "NC-001872": RegistryTitle("NC-001872", "1790012345001", 48_500.00, "ACTIVO", False),
        "NC-001945": RegistryTitle("NC-001945", "0992456789001", 70_000.00, "ACTIVO", False),
        "NC-002011": RegistryTitle("NC-002011", "1791987654001", 25_300.00, "ACTIVO", True),
    }

    def find_title(self, title_number: str) -> RegistryTitle | None:
        return self._titles.get(title_number.strip().upper())


RISK_RUCS: set[str] = {"1792233445001", "0999999999001"}
