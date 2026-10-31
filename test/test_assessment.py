import pandas as pd
from erm.assessment import assess_risks, classify_risk

BANDS = {"low": 4, "medium": 9, "high": 16}

def test_classification():
    assert classify_risk(3, BANDS) == "Low"
    assert classify_risk(7, BANDS) == "Medium"
    assert classify_risk(12, BANDS) == "High"
    assert classify_risk(20, BANDS) == "Critical"

def test_assessment():
    df = pd.DataFrame([{"likelihood": 4, "impact": 5, "control_effectiveness": 50}])
    result = assess_risks(df, {"risk_scoring": {"bands": BANDS}})
    assert result.loc[0, "inherent_score"] == 20
    assert result.loc[0, "residual_score"] == 10
