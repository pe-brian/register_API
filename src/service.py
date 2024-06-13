from typing import Self

from src.injector import Injector
from .subscriber import Subscriber


class ServiceNotAvailableError(Exception):
    def __init__(self, service_name: str) -> None:
        super().__init__(f"Service {service_name} not available")


class Service(Subscriber):
    """ Service """
    @staticmethod
    def get(name: str) -> Self:
        return Injector.resolve(name)
