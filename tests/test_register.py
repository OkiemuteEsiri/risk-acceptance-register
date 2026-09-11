import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from src.models import RiskAcceptance, parse_date
from src.register import governance_findings, load_register, portfolio_metrics, render_markdown


class RiskAcceptanceTests(unittest.TestCase):
    def sample(self, **overrides):
        data = dict(
            record_id="RA-T1",
            title="Synthetic exception",
            severity="high",
            asset="synthetic-asset",
            owner="Platform Team",
            business_justification="Temporary exception for validated maintenance dependency.",
            compensating_controls=("segmentation",),
            decision="accept",
            status="approved",
            requested_on=parse_date("2026-01-01"),
            expires_on=parse_date("2026-12-31"),
            reviewer="Risk Committee",
            validation_evidence="Control test CT-1",
            residual_risk_score=50,
        )
        data.update(overrides)
        return RiskAcceptance(**data)

    def test_invalid_severity_rejected(self):
        with self.assertRaises(ValueError):
            self.sample(severity="urgent")

    def test_invalid_date_order_rejected(self):
        with self.assertRaises(ValueError):
            self.sample(expires_on=parse_date("2025-12-31"))

    def test_approved_requires_reviewer(self):
        with self.assertRaises(ValueError):
            self.sample(reviewer="")

    def test_high_residual_risk_creates_finding(self):
        findings = governance_findings([self.sample(residual_risk_score=80)], date(2026, 9, 11))
        self.assertTrue(any("residual risk remains high" in f["issues"] for f in findings))

    def test_expired_approved_exception_flagged(self):
        record = self.sample(expires_on=parse_date("2026-08-01"))
        findings = governance_findings([record], date(2026, 9, 11))
        self.assertTrue(any("past expiry" in issue for issue in findings[0]["issues"]))

    def test_approved_missing_evidence_flagged(self):
        findings = governance_findings([self.sample(validation_evidence="")], date(2026, 9, 11))
        self.assertTrue(any("validation evidence" in issue for issue in findings[0]["issues"]))

    def test_metrics_measure_evidence_coverage(self):
        records = [self.sample(record_id="A"), self.sample(record_id="B", validation_evidence="")]
        metrics = portfolio_metrics(records, date(2026, 9, 11))
        self.assertEqual(metrics["evidence_coverage_pct"], 50.0)

    def test_duplicate_record_ids_fail_closed(self):
        payload = [
            {
                "record_id": "RA-1", "title": "A", "severity": "low", "asset": "a", "owner": "o",
                "business_justification": "j", "compensating_controls": [], "decision": "accept",
                "status": "pending", "requested_on": "2026-01-01", "expires_on": "2026-02-01",
                "reviewer": "r", "residual_risk_score": 10
            },
            {
                "record_id": "RA-1", "title": "B", "severity": "low", "asset": "b", "owner": "o",
                "business_justification": "j", "compensating_controls": [], "decision": "accept",
                "status": "pending", "requested_on": "2026-01-01", "expires_on": "2026-02-01",
                "reviewer": "r", "residual_risk_score": 10
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "register.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_register(path)

    def test_report_contains_governance_language(self):
        report = render_markdown([self.sample()], date(2026, 9, 11))
        self.assertIn("Risk Acceptance Register Assessment", report)
        self.assertIn("do not prove exploitation", report)

    def test_zero_approved_records_have_zero_coverage(self):
        record = self.sample(status="pending")
        metrics = portfolio_metrics([record], date(2026, 9, 11))
        self.assertEqual(metrics["evidence_coverage_pct"], 0.0)
        self.assertEqual(metrics["control_coverage_pct"], 0.0)


if __name__ == "__main__":
    unittest.main()
