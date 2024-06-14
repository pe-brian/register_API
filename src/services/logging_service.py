import logging

from ..injector import declare
from ..service import Service


@declare
class LoggingService(Service):
    """Logging service"""

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="app.log",
            encoding="utf-8",
            format="%(asctime)s %(levelname)-8s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
        self._logger.info("[ALERT] Started logging service")
        super().__init__()

    def __del__(self) -> None:
        self._logger.info("[ALERT] Ended logging service")

    def on_event(self, event: str, *args, **kwargs):
        """Listen an event"""
        if event.startswith("ERROR_"):
            self.log(
                f"[ERROR] {event} (args: {args} | kwargs: {kwargs}))", severity="error"
            )
        else:
            self.log(
                f"[INFO] {event} (args: {args} | kwargs: {kwargs}))", severity="info"
            )

    def log(self, msg: str, severity: str = "info"):
        """Log a message"""
        print(msg)
        match severity:
            case "error":
                self._logger.error(msg)
            case "info":
                self._logger.info(msg)
