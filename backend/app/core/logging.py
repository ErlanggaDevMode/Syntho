import json
import logging
from datetime import UTC, datetime


class JSONFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(
                timespec="seconds"
            ),
            "service": "backend",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
        }
        # Include custom attributes if present
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        if hasattr(record, "trace_id"):
            log_data["trace_id"] = record.trace_id

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Force Uvicorn access logs to use our JSON handler
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers = [handler]
    uvicorn_access.propagate = False

    # Adjust sqlalchemy logging verbosity
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
