from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.integrations.sri_source import RISK_RUCS, RegistryTitle

Severity = Literal["critical", "warning", "info"]


@dataclass(frozen=True)
class ValidationResult:
    code: str
    passed: bool
    severity: Severity
    explanation: str
    evidence: str
    action: str


def result(
    code: str,
    passed: bool,
    severity: Severity,
    failure: str,
    evidence: str,
    action: str,
) -> ValidationResult:
    return ValidationResult(
        code=code,
        passed=passed,
        severity="info" if passed else severity,
        explanation="Control superado." if passed else failure,
        evidence=evidence,
        action="Continuar" if passed else action,
    )


def validate_case(
    case: dict[str, object],
    registry: RegistryTitle | None,
    duplicate_count: int,
) -> list[ValidationResult]:
    title = str(case.get("title") or "")
    ruc = str(case.get("ruc") or "")
    amount = float(case.get("amount") or 0)
    balance = float(case.get("balance") or amount)
    documents = list(case.get("documents") or [])
    required_present = all(str(case.get(field) or "").strip() for field in ("holder", "ruc", "title"))

    return [
        result("TITLE_EXISTS", registry is not None, "critical", "El título no consta en la fuente simulada.", "Consulta por número de título.", "Enviar a cumplimiento"),
        result("TITLE_ACTIVE", registry is not None and registry.status == "ACTIVO", "critical", "El título no está activo.", "Estado reportado por la fuente simulada.", "Enviar a cumplimiento"),
        result("TITLE_NOT_BLOCKED", registry is not None and not registry.blocked, "critical", "El título tiene un bloqueo registrado.", "Certificado de estado y motivo del bloqueo.", "Enviar a cumplimiento"),
        result("BALANCE_MATCH", registry is not None and abs(registry.balance - balance) < 0.01, "warning", "El saldo ingresado no coincide con la fuente.", "Saldo del título y documento de respaldo.", "Actualizar dato"),
        result("RUC_MATCH", registry is not None and registry.ruc == ruc, "critical", "El RUC no coincide con el titular registrado.", "Identificación del titular y registro del título.", "Enviar a cumplimiento"),
        result("NO_DUPLICATE", duplicate_count <= 1, "warning", "Existe otro expediente para el mismo título.", "Expedientes anteriores asociados al título.", "Revisar expediente previo"),
        result("REQUIRED_FIELDS", required_present, "warning", "Faltan campos obligatorios.", "Titular, RUC y número de título.", "Actualizar dato"),
        result("REQUIRED_DOCUMENTS", "nota_credito" in documents, "warning", "Falta la nota de crédito como respaldo.", "PDF de la nota de crédito.", "Solicitar documento"),
        result("NO_RISK_MATCH", ruc not in RISK_RUCS, "critical", "El RUC coincide con una lista simulada de riesgo.", "Resultado de debida diligencia y soportes del cliente.", "Enviar a cumplimiento"),
        result("VALUE_VALID", amount > 0 and 0 <= balance <= amount, "warning", "El valor o saldo está fuera del rango válido.", "Valor nominal y saldo vigente.", "Actualizar dato"),
    ]
