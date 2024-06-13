import logging
from logging import Logger
from io import StringIO

import pytest
from unittest.mock import patch

from src.services.logging_service import LoggingService


class TestLoggingService:
    @pytest.fixture
    def mock_logger(self):
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        logger = logging.getLogger(__name__)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger, stream

    def test_log_info(self, mock_logger: tuple[Logger, StringIO]):
        logger, stream = mock_logger
        with patch(
            "src.services.logging_service.logging.getLogger", return_value=logger
        ):
            logging_service = LoggingService()
            logging_service.log("Test info message", severity="info")
            stream.seek(0)
            assert "Test info message" in stream.getvalue()

    def test_log_error(self, mock_logger: tuple[Logger, StringIO]):
        logger, stream = mock_logger
        with patch(
            "src.services.logging_service.logging.getLogger", return_value=logger
        ):
            logging_service = LoggingService()
            logging_service.log("Test error message", severity="error")
            stream.seek(0)
            assert "Test error message" in stream.getvalue()

    def test_on_event_info(self, mock_logger: tuple[Logger, StringIO]):
        logger, stream = mock_logger
        with patch(
            "src.services.logging_service.logging.getLogger", return_value=logger
        ):
            logging_service = LoggingService()
            logging_service.on_event("FAKE_EVENT", "1", param="2")
            stream.seek(0)
            assert (
                "[INFO] FAKE_EVENT (args: ('1',) | kwargs: {'param': '2'}))"
                in stream.getvalue()
            )

    def test_on_event_error(self, mock_logger: tuple[Logger, StringIO]):
        logger, stream = mock_logger
        with patch(
            "src.services.logging_service.logging.getLogger", return_value=logger
        ):
            logging_service = LoggingService()
            logging_service.on_event("ERROR_FAKE_EVENT", "1", param="2")
            stream.seek(0)
            assert (
                "[ERROR] ERROR_FAKE_EVENT (args: ('1',) | kwargs: {'param': '2'}))"
                in stream.getvalue()
            )
