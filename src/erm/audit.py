import json
from datetime import datetime, timezone
from pathlib import Path

def write_audit_event(audit_file, event, details):
    path = Path(audit_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"event_time_utc": datetime.now(timezone.utc).isoformat(),
           "event": event, "details": details}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, default=str) + "\n")
