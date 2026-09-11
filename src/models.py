from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterable

ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
ALLOWED_STATUSES = {"pending", "approved", "expired", "rejected", "closed"}
ALLOWED_DECISIONS = {"accept", "mitigate", "transfer", "avoid"}


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(f"invalid ISO date: {value}") from exc


@dataclass(frozen=True)
class RiskAcceptance:
    record_id: str
    title: str
    severity: str
    asset: str
    owner: str
    business_justification: str
    compensating_controls: tuple[str, ...]
    decision: str
    status: str
    requested_on: date
    expires_on: date
    reviewer: str
    validation_evidence: str = ""
    residual_risk_score: int = 0

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id is required")
        if not self.title.strip():
            raise ValueError("title is required")
        if self.severity not in ALLOWED_SEVERITIES:
            raise ValueError(f"unsupported severity: {self.severity}")
        if self.status not in ALLOWED_STATUSES:
            raise ValueError(f"unsupported status: {self.status}")
        if self.decision not in ALLOWED_DECISIONS:
            raise ValueError(f"unsupported decision: {self.decision}")
        if self.expires_on <= self.requested_on:
            raise ValueError("expires_on must be after requested_on")
        if not 0 <= self.residual_risk_score <= 100:
            raise ValueError("residual_risk_score must be between 0 and 100")
        if self.status == "approved" and not self.reviewer.strip():
            raise ValueError("approved records require a reviewer")
        if self.status == "approved" and not self.business_justification.strip():
            raise ValueError("approved records require business justification")


def controls(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(v.strip() for v in values if v.strip())
