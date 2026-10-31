import pandas as pd

def classify_risk(score, bands):
    if score <= bands["low"]:
        return "Low"
    if score <= bands["medium"]:
        return "Medium"
    if score <= bands["high"]:
        return "High"
    return "Critical"

def assess_risks(df, config):
    result = df.copy()
    bands = config["risk_scoring"]["bands"]
    result["inherent_score"] = result["likelihood"] * result["impact"]
    result["inherent_rating"] = result["inherent_score"].apply(lambda x: classify_risk(x, bands))
    # Illustrative residual-risk calculation; formal methodology needs Risk approval.
    result["residual_score"] = (result["inherent_score"] *
                                (1 - result["control_effectiveness"] / 100)).round(2)
    result["residual_rating"] = result["residual_score"].apply(lambda x: classify_risk(x, bands))
    return result
