from unittest.mock import patch

from src.injector import Dependency, Injector, inject, declare


class FakeDependency:
    def __init__(self):
        self.value = "fake_value"


def test_injector_register_and_resolve():
    Injector.register(FakeDependency)
    resolved_dependency = Injector.resolve("FakeDependency")
    assert isinstance(resolved_dependency, FakeDependency)
    assert resolved_dependency.value == "fake_value"


def test_declare_decorator():
    @declare
    class NewDependency:
        pass

    assert "NewDependency" in Injector.dependencies
    assert isinstance(Injector.resolve("NewDependency"), NewDependency)


def test_inject_decorator():
    @inject("FakeDependency")
    class TestClass:
        pass

    with patch.dict(
        Injector.dependencies, {"FakeDependency": Dependency(FakeDependency)}
    ):
        instance = TestClass()
        assert instance.fake_dependency.value == "fake_value"
