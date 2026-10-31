from pathlib import Path
import pandas as pd

REQUIRED = ["risk_id", "risk_title", "risk_category", "business_unit",
            "description", "likelihood", "impact", "control_effectiveness",
            "owner", "status", "overdue_days"]

def load_risk_register(input_file):
    path = Path(input_file)
    if not path.exists():
        raise FileNotFoundError(f"Risk input file not found: {path}")
    return pd.read_csv(path)

def validate_risk_register(df, config):
    missing = sorted(set(REQUIRED) - set(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if df.empty:
        raise ValueError("Risk register is empty.")
    if df["risk_id"].isna().any() or df["risk_id"].astype(str).str.strip().eq("").any():
        raise ValueError("risk_id contains null or blank values.")
    duplicates = df.loc[df["risk_id"].duplicated(), "risk_id"].astype(str).tolist()
    if duplicates:
        raise ValueError(f"Duplicate risk_id values: {duplicates}")
    rules = {
        "likelihood": (config["risk_scoring"]["likelihood_min"], config["risk_scoring"]["likelihood_max"]),
        "impact": (config["risk_scoring"]["impact_min"], config["risk_scoring"]["impact_max"]),
        "control_effectiveness": (config["controls"]["effectiveness_min"], config["controls"]["effectiveness_max"]),
        "overdue_days": (0, None),
    }
    for col, (low, high) in rules.items():
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any() or (values < low).any() or (high is not None and (values > high).any()):
            raise ValueError(f"Invalid values in {col}; expected range {low} to {high}.")
        df[col] = values
    for col in ["risk_title", "risk_category", "business_unit", "owner", "status"]:
        if df[col].isna().any() or df[col].astype(str).str.strip().eq("").any():
            raise ValueError(f"{col} contains null or blank values.")
