# Risk Acceptance Register

A recruiter-facing vulnerability and exposure governance project that models how security teams track, review, evidence, expire and close formal risk-acceptance decisions.

## Problem statement

Vulnerability backlogs often contain findings that cannot be remediated immediately because of operational dependencies, vendor constraints, maintenance windows or business risk trade-offs. Without disciplined governance, temporary exceptions can quietly become permanent exposure.

This project demonstrates how to turn risk acceptance into a controlled lifecycle with explicit ownership, evidence, compensating controls, expiry dates, residual risk and revalidation.

## Architecture

```text
Synthetic JSON register
        |
        v
Validated domain model
        |
        v
Governance assessment engine
        |
        +--> expiry checks
        +--> ownership checks
        +--> control coverage
        +--> evidence coverage
        +--> residual-risk review
        |
        v
Portfolio metrics + prioritized findings
        |
        v
Markdown executive report
```

## Core capabilities

- Immutable, validated risk-acceptance records.
- Fail-closed duplicate-ID and schema validation.
- Formal decision states: accept, mitigate, transfer and avoid.
- Pending, approved, expired, rejected and closed lifecycle states.
- Time-bounded exception governance.
- Compensating-control and validation-evidence checks.
- Explicit residual-risk tracking on a 0-100 scale.
- Explainable governance-priority scoring.
- Portfolio metrics for expired approvals, evidence coverage and control coverage.
- Offline CLI for deterministic register assessment.
- Synthetic example data and executive reporting.
- Unit-test coverage for validation and governance logic.
- Least-privilege GitHub Actions workflow.

## Repository structure

```text
.github/workflows/ci.yml        Least-privilege CI
src/models.py                   Validated domain model
src/register.py                 Governance assessment and reporting
src/cli.py                      Offline CLI
data/synthetic_register.json    Synthetic risk-acceptance records
tests/test_register.py          Unit tests
docs/methodology.md             Governance methodology
reports/example-executive-report.md
```

## Example controls

The assessment highlights records where:

- an approved exception is past expiry;
- approved risk has no compensating controls;
- approved risk lacks validation evidence;
- accountable ownership is missing;
- residual risk remains high after acceptance.

These are governance signals, not proof of exploitation or compromise.

## Usage

Run the unit tests:

```bash
python -m unittest discover -s tests -v
```

Generate a report from the synthetic register:

```bash
python -m src.cli data/synthetic_register.json --as-of 2026-09-11
```

Write the report to a file:

```bash
python -m src.cli data/synthetic_register.json --as-of 2026-09-11 --output report.md
```

## Risk-acceptance lifecycle

```text
Finding
  -> remediation analysis
  -> exception request
  -> accountable-owner review
  -> decision
  -> compensating controls
  -> evidence validation
  -> periodic review
  -> expiry or remediation
  -> technical revalidation
  -> closure or reacceptance
```

A key design principle is that **approval does not remove the risk**. The register keeps residual risk visible until the underlying exposure is mitigated, transferred, avoided or formally reaccepted.

## Metrics demonstrated

The sample engine produces:

- total register population;
- status distribution;
- number of approved records;
- approved-but-expired count;
- approved records with elevated residual risk;
- validation-evidence coverage percentage;
- compensating-control coverage percentage.

This supports vulnerability-management reporting without presenting accepted exceptions as remediated findings.

## MITRE ATT&CK context

Threat context can be attached to accepted exposure where relevant, for example:

- **T1190** - Exploit Public-Facing Application
- **T1210** - Exploitation of Remote Services
- **T1078** - Valid Accounts

These mappings are contextual only. They do not assert that an ATT&CK technique occurred.

## Skills demonstrated

- Vulnerability and exposure management
- Risk acceptance and exception governance
- Security metrics and executive reporting
- Python security engineering
- Data validation and fail-closed processing
- Residual-risk analysis
- Compensating-control assurance
- Remediation and revalidation workflow design
- Unit testing
- CI/CD security hygiene
- MITRE ATT&CK contextual mapping

## Security and data handling

All records in this repository are synthetic. The project contains no employer or client data, production assets, credentials, scanner exports or confidential risk decisions.

## Limitations

The scoring model is deliberately explainable and deterministic. It is not a replacement for enterprise GRC tooling, legal review, business-impact analysis, CVSS, EPSS, threat intelligence or formal executive risk authority. Operational deployment would require calibration, access control, immutable audit history and integration with asset, vulnerability and ticketing systems.

## Roadmap

- Add reviewer-role and approval-threshold policy checks.
- Add renewal-history and immutable decision audit trail.
- Add SLA linkage to remediation milestones.
- Add KEV/EPSS-aware exception re-review triggers using synthetic feeds.
- Add CSV import/export and schema versioning.
- Add trend reporting for exception age and renewal frequency.
- Add dashboard-ready JSON metrics output.
