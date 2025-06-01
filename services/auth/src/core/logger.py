import logging
import json
import os
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def __init__(self, service_name: str = "shop-app"):
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        data = {
            "custom_field": getattr(record, "custom_field", ""),
            "environment": os.getenv("ENV", "development"),
            "@timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "message": record.getMessage(),
            "level": record.levelname,
            "service": self.service_name,
        }
        return json.dumps(data)

def setup_logging(log_file_path: str = "/tmp/logs/logs.txt", service_name: str = "shop-app") -> None:
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_formatter = JSONFormatter(service_name=service_name)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    root_logger.addHandler(console_handler)
