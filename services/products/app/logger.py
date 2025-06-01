import logging
import os
from pythonjsonlogger import jsonlogger
from datetime import datetime


SERVICE_NAME = os.getenv("SERVICE_NAME", "example-service")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "/tmp/logs/logs.txt")
CUSTOM_FIELD_DEFAULT = os.getenv("CUSTOM_FIELD_DEFAULT", "some value")

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(
            fmt=(
                "@timestamp level service environment custom_field message"
            ),
            *args,
            **kwargs
        )

    def add_fields(self, log_record, record, message_dict):
        log_record["@timestamp"] = datetime.utcfromtimestamp(record.created).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )

        log_record["level"] = record.levelname


        log_record["service"] = SERVICE_NAME


        log_record["environment"] = ENVIRONMENT


        log_record["custom_field"] = getattr(record, "custom_field", CUSTOM_FIELD_DEFAULT)

        log_record["message"] = record.getMessage()

        super().add_fields(log_record, record, message_dict)


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)


json_formatter = CustomJsonFormatter()
file_handler.setFormatter(json_formatter)


root_logger.addHandler(file_handler)
