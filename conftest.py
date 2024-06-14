from importlib import reload
import pytest

from src.injector import Injector


@pytest.fixture(autouse=True)
def isolate_tests():
    # Reset dependencies
    Injector.dependencies = {}
    # Reload modules to auto-declare dependencies
    import tests.mocks.in_memory_database_service
    reload(tests.mocks.in_memory_database_service)
    import src.services.dispatch_service
    reload(src.services.dispatch_service)
    import src.services.code_sender_service
    reload(src.services.code_sender_service)
    import src.services.registration_service
    reload(src.services.registration_service)
    import src.services.activation_service
    reload(src.services.activation_service)
    import src.services.cryptography_service
    reload(src.services.cryptography_service)
    import src.services.logging_service
    reload(src.services.logging_service)
    import src.services.smtp_service
    reload(src.services.smtp_service)
    import src.services.validation_service
    reload(src.services.validation_service)
