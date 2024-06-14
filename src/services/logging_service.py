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

    def on_event(self, event: str, *_, **kwargs):
        """Listen an event"""
        print(event, "|", kwargs)
        if event.startswith("ERROR_"):
            self.log(
                f"{event} | {kwargs}", severity="error"
            )
        else:
            self.log(
                f"{event} | {kwargs}", severity="info"
            )

    def log(self, msg: str, severity: str = "info"):
        """Log a message"""
        match severity:
            case "error":
                self._logger.error(msg)
            case "info":
                self._logger.info(msg)
