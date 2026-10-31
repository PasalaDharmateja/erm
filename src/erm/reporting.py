import json
from pathlib import Path

def generate_reports(df, output_dir, top_risks):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    detailed = out / "risk_assessment.csv"
    summary_file = out / "risk_summary.json"
    html_file = out / "risk_dashboard.html"
    df.to_csv(detailed, index=False)
    summary = {
        "total_risks": int(len(df)),
        "inherent_rating_counts": df["inherent_rating"].value_counts().to_dict(),
        "residual_rating_counts": df["residual_rating"].value_counts().to_dict(),
        "kri_status_counts": df["overdue_kri_status"].value_counts().to_dict(),
        "critical_residual_risks": int((df["residual_rating"] == "Critical").sum()),
        "open_risks": int((df["status"].str.lower() != "closed").sum())
    }
    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    top = df.sort_values(["residual_score", "inherent_score"], ascending=False).head(top_risks)
    table = top.to_html(index=False, escape=True)
    html = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Banking ERM Dashboard</title>"
        "<style>body{font-family:Arial;margin:30px}table{border-collapse:collapse;width:100%}"
        "td,th{border:1px solid #ddd;padding:8px}th{background:#eee}</style></head><body>"
        "<h1>Banking Enterprise Risk Management</h1>"
        "<p>Illustrative risk monitoring output. Obtain Risk approval before production.</p>"
        f"<h2>Total risks: {summary['total_risks']}</h2>"
        f"<h2>Critical residual risks: {summary['critical_residual_risks']}</h2>"
        "<h2>Top risks by residual score</h2>" + table + "</body></html>"
    )
    html_file.write_text(html, encoding="utf-8")
    return {"detailed_report": str(detailed), "summary_report": str(summary_file),
            "html_dashboard": str(html_file)}
