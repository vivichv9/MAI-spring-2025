import json
from datetime import datetime, timezone

def save_log(
    custom_field: str,
    environment: str,
    message: str,
    level: str,
    service: str,
    file_path: str = "/tmp/logs/logs.txt"
):
    log_entry = {
        "custom field": custom_field,
        "environment": environment,
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "level": level,
        "service": service
    }

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")
