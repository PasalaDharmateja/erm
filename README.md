# Banking Enterprise Risk Management (ERM) Framework

Python starter framework: ingest a risk register, validate records, calculate
illustrative inherent and residual risk scores, monitor an overdue-days KRI,
and generate CSV, JSON and HTML reports.

**Important:** This is a technical starter, not a regulatory-approved risk model.
Risk taxonomy, scoring, control effectiveness, thresholds, governance and reports
must be approved by the bank's Risk, Compliance, Model Risk and Information
Security teams before production use. Do not use real customer PII in sample data.

## Project structure

```text
banking_erm_framework/
  config/erm_config.yml
  data/input/risk_register.csv
  data/output/
  logs/
  src/erm/
    config.py ingestion.py assessment.py monitoring.py reporting.py
    audit.py logging_setup.py main.py
  tests/test_assessment.py
  scripts/run_erm.sh
  requirements.txt
```

## Setup (Linux / WSL)

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH="$PWD/src"
```

## Run

```bash
python -m erm.main --config config/erm_config.yml
```

Outputs:
- `data/output/risk_assessment.csv`: risk-level scores and KRI flags.
- `data/output/risk_summary.json`: counts and summary metrics.
- `data/output/risk_dashboard.html`: simple HTML report.
- `logs/erm_framework.log`: operational log.
- `logs/audit.jsonl`: run-started, succeeded and failed audit events.

## Processing sequence

1. Load YAML configuration.
2. Read CSV risk register.
3. Validate mandatory columns, nulls, duplicate IDs and numeric ranges.
4. Calculate inherent score = likelihood × impact.
5. Calculate illustrative residual score = inherent score × (1 − control effectiveness / 100).
6. Classify risks using configurable bands.
7. Flag overdue-days KRI.
8. Generate reports and write audit events.

## Risk bands

The sample uses 1–5 likelihood and impact scales. Scores 1–4 are Low,
5–9 Medium, 10–16 High, and 17–25 Critical. This is illustrative only.

## Autosys example (JIL)

Replace placeholders with the approved Autosys agent, service account and paths.

```jil
insert_job: BANK_ERM_DAILY
job_type: c
machine: <approved_autosys_agent>
command: /bin/bash /opt/banking_erm_framework/scripts/run_erm.sh
owner: <approved_service_account>
date_conditions: 1
days_of_week: all
start_times: "06:00"
std_out_file: /opt/banking_erm_framework/logs/autosys.out
std_err_file: /opt/banking_erm_framework/logs/autosys.err
alarm_if_fail: 1
```

The Python job exits 0 on success and 1 on failure. Configure alerting,
dependencies, rerun policy and calendars under your bank's Autosys standards.

## Tests

```bash
pip install pytest
pytest -q
```

## Production hardening

- Replace sample CSV with approved source systems and a documented data contract.
- Use service accounts, secrets management and least-privilege access.
- Encrypt data in transit and at rest; mask sensitive data.
- Add maker-checker approvals and risk-owner sign-off.
- Version scoring methodology and thresholds; independently validate changes.
- Add lineage, source timestamps, reconciliation and historical snapshots.
- Add idempotency, rerun, backfill, recovery and SLA controls.
- Add integration, regression, security and UAT testing.
- Align the framework with applicable bank policy and regulatory requirements.

## Next phases

Phase 2: Database integration, risk history, control testing and action-plan tracking.
Phase 3: Credit, market and liquidity feeds, dashboards and workflow approvals.
Phase 4: Formal model governance, independent validation and production deployment.
