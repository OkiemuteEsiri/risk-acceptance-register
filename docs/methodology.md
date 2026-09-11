# Methodology

## Objective

This project models risk-acceptance governance for vulnerability and exposure management. It is designed to help security teams distinguish a formally governed exception from an untracked remediation delay.

## Governance principles

1. Every exception has a unique identifier, named asset, owner, severity, business justification, decision, reviewer, start date and expiry date.
2. Acceptance is time-bounded. An approved exception that passes its expiry date is a governance finding.
3. Compensating controls should reduce exposure during the exception period and should be testable.
4. Validation evidence should demonstrate that the stated compensating controls exist and remain effective.
5. Residual risk remains explicit. Approval does not erase the underlying risk.
6. Closure should follow remediation and revalidation, not the passage of time alone.

## Residual-risk interpretation

The sample register uses a 0–100 residual-risk field supplied by the governed process. The assessment engine does not infer exploit success or compromise. It adds governance context such as expired approval, missing control evidence, missing ownership and elevated residual risk.

## Assessment logic

The engine highlights:

- approved exceptions past expiry;
- approved exceptions without compensating controls;
- approved exceptions without validation evidence;
- records without accountable ownership;
- approved records with residual risk of 75 or greater.

A governance score is derived from the record severity, number of governance issues and residual-risk level. This score is intended for review prioritization, not as a replacement for CVSS, EPSS, business impact analysis or threat intelligence.

## Workflow

`finding -> remediation plan -> exception request -> reviewer decision -> compensating controls -> evidence validation -> periodic review -> expiry/remediation -> revalidation -> closure`

## Exception review questions

- Is the business justification still valid?
- Has the asset or service criticality changed?
- Has exploitability or threat context materially changed?
- Are compensating controls still implemented and monitored?
- Is evidence recent enough to support continued acceptance?
- Has the remediation date slipped?
- Is risk ownership still assigned to the correct accountable team?

## MITRE ATT&CK context

Risk acceptance can govern exposures relevant to techniques such as T1190 (Exploit Public-Facing Application), T1210 (Exploitation of Remote Services) and T1078 (Valid Accounts). These mappings provide threat context only. They are not evidence that an ATT&CK technique occurred.

## Limitations

This lab uses synthetic data and offline deterministic logic. It does not connect to ticketing systems, vulnerability scanners, GRC platforms or production assets. The sample score is intentionally explainable and should be calibrated before operational use.
