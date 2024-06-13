from dataclasses import dataclass
import pytest
from unittest.mock import MagicMock, patch
from src import BaseModel
from chocolatine import Col

from src.injector import Dependency, Injector


@dataclass
class TestModel(BaseModel):
    name: str
    value: int


@pytest.fixture(autouse=True)
def clear_injector_registry():
    Injector.dependencies = {}


@pytest.fixture
def db_service_class_mock():
    mock = MagicMock()
    mock.__name__ = "MockDatabaseService"
    Injector.dependencies["DatabaseService"] = Dependency(mock)
    yield mock


def test_get_table_name():
    assert TestModel.get_table_name() == "test_model"


@patch("src.base_model.Service")
def test_create(service_get_mock: MagicMock):
    service_get_mock.get.return_value.create_object.return_value = TestModel(
        name="Test", value=True
    )
    created_obj = TestModel.create(name="Test", value=True)
    assert created_obj.name == "Test"
    assert created_obj.value is True


def test_save():
    with patch.object(BaseModel, "database_service", MagicMock()) as db_service_mock:
        test_object = TestModel(name="Test", value=True)
        returned_test_object = TestModel(name="Test", value=True)
        returned_test_object.id = 1
        db_service_mock.create_or_update_object.return_value = returned_test_object
        saved_obj = test_object.save()
        assert db_service_mock.create_or_update_object.called
        assert saved_obj.id == 1


def test_delete() -> None:
    with patch.object(BaseModel, "database_service", MagicMock()) as db_service_mock:
        test_model = TestModel(name="Test", value=True)
        test_model.id = 1
        test_model.delete()
        assert test_model.id is None
        assert db_service_mock.delete_object_by_id.called


@patch("src.base_model.Service")
def test_get(service_get_mock: MagicMock) -> None:
    TestModel.get(id == 1)
    assert service_get_mock.get.return_value.get_object_by_id.called


@patch("src.base_model.Service")
def test_filter(service_get_mock: MagicMock) -> None:
    obj = TestModel(name="Test", value=True)
    obj.id = 1
    service_get_mock.get.return_value.filter_objects.return_value = [obj, obj]
    results = TestModel.filter(Col("id") == 1)
    assert len(results) == 2
    assert results[0].id == 1
