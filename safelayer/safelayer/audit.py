import json
from datetime import datetime

def audit_log(**kwargs):
    entry = dict(**kwargs)
    entry["timestamp"] = datetime.now().isoformat()
    with open("audit.log", "a") as logf:
        logf.write(json.dumps(entry) + "\n")
