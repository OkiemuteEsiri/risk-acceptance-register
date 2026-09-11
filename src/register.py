from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Iterable

from .models import RiskAcceptance, controls, parse_date

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def load_register(path: str | Path) -> list[RiskAcceptance]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("register input must be a JSON array")

    records: list[RiskAcceptance] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("each register entry must be an object")
        record_id = str(item.get("record_id", "")).strip()
        if record_id in seen:
            raise ValueError(f"duplicate record_id: {record_id}")
        seen.add(record_id)
        records.append(
            RiskAcceptance(
                record_id=record_id,
                title=str(item.get("title", "")).strip(),
                severity=str(item.get("severity", "")).lower(),
                asset=str(item.get("asset", "")).strip(),
                owner=str(item.get("owner", "")).strip(),
                business_justification=str(item.get("business_justification", "")).strip(),
                compensating_controls=controls(item.get("compensating_controls", [])),
                decision=str(item.get("decision", "")).lower(),
                status=str(item.get("status", "")).lower(),
                requested_on=parse_date(str(item.get("requested_on", ""))),
                expires_on=parse_date(str(item.get("expires_on", ""))),
                reviewer=str(item.get("reviewer", "")).strip(),
                validation_evidence=str(item.get("validation_evidence", "")).strip(),
                residual_risk_score=int(item.get("residual_risk_score", 0)),
            )
        )
    return records


def governance_findings(records: Iterable[RiskAcceptance], as_of: date) -> list[dict]:
    findings: list[dict] = []
    for record in records:
        issues: list[str] = []
        if record.status == "approved" and record.expires_on < as_of:
            issues.append("approved exception is past expiry")
        if record.status == "approved" and not record.compensating_controls:
            issues.append("approved exception has no compensating controls")
        if record.status == "approved" and not record.validation_evidence:
            issues.append("approved exception lacks validation evidence")
        if not record.owner:
            issues.append("risk owner is missing")
        if record.residual_risk_score >= 75:
            issues.append("residual risk remains high")

        if issues:
            base = SEVERITY_WEIGHT[record.severity] * 15
            score = min(100, base + 10 * len(issues) + record.residual_risk_score // 5)
            findings.append(
                {
                    "record_id": record.record_id,
                    "asset": record.asset,
                    "severity": record.severity,
                    "governance_score": score,
                    "issues": issues,
                }
            )
    return sorted(findings, key=lambda f: f["governance_score"], reverse=True)


def portfolio_metrics(records: Iterable[RiskAcceptance], as_of: date) -> dict:
    rows = list(records)
    by_status = Counter(r.status for r in rows)
    approved = [r for r in rows if r.status == "approved"]
    expired_approved = [r for r in approved if r.expires_on < as_of]
    high_residual = [r for r in approved if r.residual_risk_score >= 75]
    evidence_complete = [r for r in approved if r.validation_evidence]
    control_complete = [r for r in approved if r.compensating_controls]
    return {
        "total_records": len(rows),
        "by_status": dict(sorted(by_status.items())),
        "approved": len(approved),
        "expired_approved": len(expired_approved),
        "approved_high_residual": len(high_residual),
        "evidence_coverage_pct": round((len(evidence_complete) / len(approved) * 100), 1) if approved else 0.0,
        "control_coverage_pct": round((len(control_complete) / len(approved) * 100), 1) if approved else 0.0,
    }


def to_serializable(record: RiskAcceptance) -> dict:
    output = asdict(record)
    output["requested_on"] = record.requested_on.isoformat()
    output["expires_on"] = record.expires_on.isoformat()
    output["compensating_controls"] = list(record.compensating_controls)
    return output


def render_markdown(records: Iterable[RiskAcceptance], as_of: date) -> str:
    rows = list(records)
    metrics = portfolio_metrics(rows, as_of)
    findings = governance_findings(rows, as_of)
    lines = [
        "# Risk Acceptance Register Assessment",
        "",
        f"Assessment date: {as_of.isoformat()}",
        "",
        "## Portfolio metrics",
        "",
        f"- Total records: {metrics['total_records']}",
        f"- Approved: {metrics['approved']}",
        f"- Approved but expired: {metrics['expired_approved']}",
        f"- Approved with high residual risk: {metrics['approved_high_residual']}",
        f"- Validation evidence coverage: {metrics['evidence_coverage_pct']}%",
        f"- Compensating-control coverage: {metrics['control_coverage_pct']}%",
        "",
        "## Governance findings",
        "",
    ]
    if not findings:
        lines.append("No governance findings identified in the supplied register.")
    for finding in findings:
        lines.append(
            f"- **{finding['record_id']}** | {finding['severity'].upper()} | score {finding['governance_score']}: "
            + "; ".join(finding["issues"])
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "Findings identify governance conditions requiring review. They do not prove exploitation, compromise, or control failure.",
    ])
    return "\n".join(lines)
