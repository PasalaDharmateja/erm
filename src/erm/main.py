import argparse
from datetime import datetime, timezone
from erm.audit import write_audit_event
from erm.assessment import assess_risks
from erm.config import load_config
from erm.ingestion import load_risk_register, validate_risk_register
from erm.logging_setup import configure_logging
from erm.monitoring import apply_kri_flags
from erm.reporting import generate_reports

def run(config_path):
    config = load_config(config_path)
    paths = config["paths"]
    logger = configure_logging(paths["log_file"])
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    try:
        logger.info("ERM run started: %s", run_id)
        write_audit_event(paths["audit_file"], "RUN_STARTED", {"run_id": run_id})
        risks = load_risk_register(paths["input_file"])
        logger.info("Loaded %s records", len(risks))
        validate_risk_register(risks, config)
        assessed = assess_risks(risks, config)
        monitored = apply_kri_flags(assessed, config)
        reports = generate_reports(monitored, paths["output_dir"], config["reporting"]["top_risks"])
        write_audit_event(paths["audit_file"], "RUN_SUCCEEDED",
                          {"run_id": run_id, "record_count": len(monitored), "reports": reports})
        logger.info("ERM run completed: %s", reports)
        return 0
    except Exception as exc:
        logger.exception("ERM run failed")
        write_audit_event(paths["audit_file"], "RUN_FAILED",
                          {"run_id": run_id, "error_type": type(exc).__name__, "error": str(exc)})
        return 1

def main():
    parser = argparse.ArgumentParser(description="Banking ERM framework")
    parser.add_argument("--config", default="config/erm_config.yml")
    args = parser.parse_args()
    raise SystemExit(run(args.config))

if __name__ == "__main__":
    main()
