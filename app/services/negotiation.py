from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class NegotiationDraft:
    case_id: str
    holder: str
    ruc: str
    title: str
    confirmed_balance: float
    negotiation_percentage: float
    gross_value: float
    commission: float
    net_value: float
    responsible: str
    status: str = "BORRADOR"


class NegotiationService:
    def generate_draft(
        self,
        case: dict[str, object],
        negotiation_percentage: float,
        commission_percentage: float,
    ) -> dict[str, object]:
        if not 0 < negotiation_percentage <= 100:
            raise ValueError("El porcentaje de negociación debe estar entre 0 y 100.")
        if not 0 <= commission_percentage <= 100:
            raise ValueError("La comisión debe estar entre 0 y 100.")

        balance = float(case.get("balance") or case.get("amount") or 0)
        gross = round(balance * negotiation_percentage / 100, 2)
        commission = round(gross * commission_percentage / 100, 2)
        draft = NegotiationDraft(
            case_id=str(case["id"]),
            holder=str(case.get("holder") or ""),
            ruc=str(case.get("ruc") or ""),
            title=str(case.get("title") or ""),
            confirmed_balance=balance,
            negotiation_percentage=negotiation_percentage,
            gross_value=gross,
            commission=commission,
            net_value=round(gross - commission, 2),
            responsible=str(case.get("responsible") or "Ana Ortiz"),
        )
        case["draft"] = asdict(draft)
        self._record(case, "Borrador de negociación generado")
        return asdict(draft)

    def request_approval(
        self,
        case: dict[str, object],
        action: str,
        observation: str,
    ) -> None:
        allowed = {"Negociación", "Liquidación", "Transferencia", "Endoso"}
        if action not in allowed:
            raise ValueError("Acción de aprobación no permitida.")
        if not case.get("draft"):
            raise ValueError("Genere el borrador antes de solicitar aprobación.")

        case["status"] = "Aprobación solicitada"
        case["next_action"] = f"Revisión humana de {action.lower()}"
        case.setdefault("observations", []).append(observation or "Sin observaciones")  # type: ignore[union-attr]
        self._record(case, f"Solicitud de {action.lower()} enviada a aprobación humana")

    @staticmethod
    def _record(case: dict[str, object], event: str) -> None:
        history = case.setdefault("history", [])
        assert isinstance(history, list)
        history.append(
            {
                "date": datetime.now().strftime("%d jul 2026 · %H:%M"),
                "responsible": str(case.get("responsible") or "Ana Ortiz"),
                "event": event,
            }
        )
