from dataclasses import dataclass, field

from unittest.mock import call, patch, MagicMock
import pytest
from chocolatine import Col, SqlType

from src.base_model import BaseModel
from src.services.database_service import DatabaseService


@dataclass
class FakeModel(BaseModel):
    test_field: str

    @classmethod
    def get_table_name(cls):
        return "fake_model"

    @property
    def check(self):
        return True


class TestDatabaseService:
    @pytest.fixture(autouse=True)
    def setup_class(self):
        with patch("src.services.database_service.getenv") as mock_getenv, patch(
            "src.services.database_service.mysql.connector.connect"
        ) as mock_connect, patch.object(
            DatabaseService, "dispatch_service", MagicMock()
        ) as mock_dispatch:
            mock_getenv.side_effect = [
                "test_db",
                "test_user",
                "test_password",
                "test_url",
            ]
            mock_db_connection = MagicMock()
            mock_db_cursor = MagicMock()
            mock_connect.return_value = mock_db_connection
            mock_db_connection.cursor.return_value = mock_db_cursor
            self.db_service = DatabaseService()
            self.dispatch_service = mock_dispatch
            self.mock_db_cursor = mock_db_cursor
            yield

    def test_register_models(self):
        self.db_service._models = {}
        self.db_service.register_models(FakeModel)
        assert "fake_model" in self.db_service._models
        assert self.db_service._models["fake_model"].__name__ == "FakeModel"

    def test_drop_table(self):
        self.db_service.drop_table("test")
        self.mock_db_cursor.execute.assert_called_with(f"DROP TABLE IF EXISTS test")

    @patch("src.services.database_service.cast_to_sql_type", return_value="VARCHAR")
    @patch("src.services.database_service.Col")
    def test_get_model_cols(self, mock_Col, mock_cast_to_sql_type):
        mock_Col.return_value = MagicMock()
        mock_Col.return_value.name = "test_field"
        mock_Col.return_value.type = "VARCHAR"
        cols = self.db_service.get_model_cols(FakeModel)
        mock_cast_to_sql_type.assert_called_once_with(str)
        mock_Col.assert_called_once_with(name="test_field", type="VARCHAR")
        assert isinstance(cols, tuple)
        assert len(cols) == 1
        assert cols[0].name == "test_field"
        assert cols[0].type == "VARCHAR"

    @patch("src.services.database_service.Query.create_table")
    def test_create_table(self, mock_query_create_table):
        mock_query_create_table.return_value.build.return_value = (
            "CREATE TABLE fake_model"
        )
        self.db_service._models = {"fake_model": FakeModel}
        self.db_service.create_table("fake_model")
        self.mock_db_cursor.execute.assert_called_with("CREATE TABLE fake_model")

    def test_create_tables(self):
        self.db_service._models = {"test_table": MagicMock()}
        with patch.object(self.db_service, "create_table") as mock_create_table:
            self.db_service.create_tables()
            mock_create_table.assert_called_with("test_table")

    @patch("src.services.database_service.Query.update_rows")
    def test_update_object(self, mock_update_rows):
        mock_update_rows.return_value.build.return_value = "UPDATE test_table SET ..."
        self.db_service._models = {"test_table": MagicMock()}
        self.db_service.update_object("test_table", id=1)
        self.mock_db_cursor.execute.assert_called()
        call_list = self.mock_db_cursor.execute.call_args_list
        assert call("UPDATE test_table SET ...") in call_list
        assert call("SELECT * FROM test_table WHERE (id = 1)") in call_list

    def test_create_or_update_object(self):
        with patch(
            "src.services.database_service.DatabaseService.update_object"
        ) as mock_update_object, patch(
            "src.services.database_service.DatabaseService.create_object"
        ) as mock_create_object:
            self.db_service.create_or_update_object("test_table", age=25, id=1)
            mock_update_object.assert_called_once()
            mock_create_object.assert_not_called()
        with patch(
            "src.services.database_service.DatabaseService.update_object"
        ) as mock_update_object, patch(
            "src.services.database_service.DatabaseService.create_object"
        ) as mock_create_object:
            self.db_service.create_or_update_object("test_table", age=25)
            mock_create_object.assert_called_once()
            mock_update_object.assert_not_called()

    @patch("src.services.database_service.asdict")
    @patch("src.services.database_service.Query.insert_row")
    def test_create_object(self, mock_insert_row, mock_asdict):
        mock_asdict.items.return_value = {"id": None, "field": "value"}
        mock_insert_row.return_value.build.return_value = (
            "INSERT INTO test_table (field) VALUES (value)"
        )
        self.db_service._models = {"fake_model": FakeModel}
        self.db_service.create_object("fake_model", test_field="test")
        self.mock_db_cursor.execute.assert_called_with(
            "INSERT INTO test_table (field) VALUES (value)"
        )

    @patch("src.services.database_service.Query.delete_rows")
    def test_delete_objects(self, mock_delete_rows):
        mock_delete_rows.return_value.build.return_value = (
            "DELETE FROM test_table WHERE id = 1"
        )
        condition = MagicMock()
        self.db_service.delete_objects("test_table", condition)
        mock_delete_rows.assert_called_with(table="test_table", filter=condition)
        self.mock_db_cursor.execute.assert_called_with(
            "DELETE FROM test_table WHERE id = 1"
        )

    @patch("src.services.database_service.mysql.connector.connect")
    def test_connect_to_db(self, mock_connect):
        mock_connect.return_value = MagicMock()
        result = self.db_service.connect_to_db("user", "password", "host", "db")
        mock_connect.assert_called_with(
            user="user",
            password="password",
            host="host",
            database="db",
            charset="utf8",
            autocommit=True,
        )
        assert result == mock_connect.return_value

    @patch("src.services.database_service.Query.get_rows")
    def test_filter(self, mock_get_rows):
        mock_get_rows.return_value.build.return_value = (
            "SELECT * FROM test_table WHERE id = 1"
        )
        condition = MagicMock()
        self.mock_db_cursor.fetchall.return_value = [(1, "data")]
        mock_model = MagicMock(spec=FakeModel)
        self.db_service._models = {"test_table": mock_model}
        result = self.db_service.filter_objects("test_table", condition)[0]
        mock_get_rows.assert_called_with(table="test_table", filters=[condition])
        self.mock_db_cursor.execute.assert_called_with(
            "SELECT * FROM test_table WHERE id = 1"
        )
        assert result.check()

    def test_exec_query(self):
        with patch(
            "src.services.database_service.DatabaseService.dispatch_service"
        ) as mock_dispatch_service:
            query = "UPDATE test_table SET field = value WHERE id = 1"
            self.db_service.exec_query(query)
            self.mock_db_cursor.execute.assert_called_with(query)
            mock_dispatch_service.dispatch.assert_called_with(
                "QUERY_EXECUTED", query=query
            )
