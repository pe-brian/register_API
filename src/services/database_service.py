from dataclasses import asdict, fields
from os import getenv
from typing import Iterable, Tuple

from chocolatine import Query, Condition, Col
import mysql.connector
from mysql.connector import errorcode

from ..service import Service
from ..injector import declare, inject
from ..utils import cast_to_sql_type
from ..base_model import BaseModel


@declare
@inject("DispatchService")
class DatabaseService(Service):
    """Interface between the database and the models"""

    def __init__(self) -> None:
        db = getenv("MYSQL_DB")
        user = getenv("MYSQL_USER")
        password = getenv("MYSQL_PASSWORD")
        url = getenv("MYSQL_URL")
        if not db or not user or not password or not url:
            raise EnvironmentError(
                "MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD & MYSQL_URL environement variables must be defined"
            )
        self._db_name = db
        self._models = {}
        self._db_connection = self.connect_to_db(user, password, url, db)
        self._db_cursor = self._db_connection.cursor(buffered=True)
        super().__init__()

    def close(self):
        """Close the service properly"""
        self._db_connection.close()

    def register_models(self, *models) -> None:
        """Register the models"""
        for model in models:
            self._models[model.get_table_name()] = model

    def drop_tables(self) -> None:
        """Drop the tables"""
        for table_name in self._models:
            self.drop_table(table_name)

    def drop_table(self, table_name: str) -> None:
        """Drop the table"""
        self.exec_query(f"DROP TABLE IF EXISTS {table_name}")

    def get_model_cols(self, model) -> Tuple[Col]:
        """Get the columns from the model"""
        return tuple(
            Col(name=field.name, type=cast_to_sql_type(field.type))
            for field in fields(model)
            if field.name != "id"
        )

    def create_table(self, table_name: str) -> None:
        """Create the table according to the registered models"""
        model = self._models[table_name]
        req = Query.create_table(
            table=table_name, cols=self.get_model_cols(model), auto_id=True
        ).build()
        self.exec_query(req)

    def create_tables(self, drop_old: bool = False) -> None:
        """Create the tables according to the registered models"""
        if drop_old:
            self.drop_tables()
        for model in self._models:
            self.create_table(model)

    def update_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Update the object and return it"""
        assignations = tuple((Col(key) == value) for key, value in kwargs.items())
        self.exec_query(
            Query.update_rows(
                table_name,
                *args,
                filters=[Col("id") == kwargs["id"]],
                assignations=assignations,
            )
            .build()
            .replace("(", "")
            .replace(")", "")
        )
        return self.get_object_by_id(table_name, kwargs["id"])

    def create_or_update_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Update the object in db if the object doesn't exit, otherwise create it and return it"""
        if "id" in kwargs and kwargs["id"] != None:
            return self.update_object(table_name, *args, **kwargs)
        return self.create_object(table_name, *args, **kwargs)

    def create_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Create the object and return it"""
        if "id" in kwargs:
            del kwargs["id"]
        model = self._models[table_name]
        object = model(*args, **kwargs)
        row = tuple(value for key, value in asdict(object).items() if key != "id")
        query = Query.insert_row(
            table=model.get_table_name(), cols=self.get_model_cols(model), row=row
        ).build()
        self.exec_query(query)
        id = self._db_cursor.lastrowid
        object.id = id
        return object

    def delete_objects(self, table_name: str, condition: Condition) -> None:
        """Delete the objects matching the condition"""
        self.exec_query(Query.delete_rows(table=table_name, filter=condition).build())

    def delete_object_by_id(self, table_name: str, id: int) -> None:
        """Delete the object by id"""
        self.exec_query(
            Query.delete_rows(table=table_name, filter=(Col("id") == id).build())
        )

    def connect_to_db(self, user: str, password: str, host: str, db: str):
        """Connect to the MySQL database"""
        try:
            db_connection = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=db,
                charset="utf8",
                autocommit=True,
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.dispatch_service.dispatch(
                    "ERROR_OCCURRED",
                    emitter="DatabaseService",
                    err="DB_ACCESS_DENIED_ERROR",
                )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.dispatch_service.dispatch(
                    "ERROR_OCCURRED", emitter="DatabaseService", err="DB_NOT_FOUND"
                )
            else:
                self.dispatch_service.dispatch(
                    "ERROR_OCCURRED", emitter="DatabaseService", err="DB_UNKNOW_ERROR"
                )
            raise err
        else:
            self.dispatch_service.dispatch(
                "DB_CONNECTION_ESTABLISHED", emitter="DatabaseService"
            )
            return db_connection

    def get_object_by_id(self, table_name: str, id: int) -> object:
        """Get object by id"""
        res = self.filter_objects(table_name, Col("id") == id)
        if res:
            return res[0]

    def filter_objects(self, table_name: str, condition: Condition) -> Iterable[object]:
        """Filter the object(s) and return them/it"""
        self.exec_query(Query.get_rows(table=table_name, filters=[condition]).build())
        rows = self._db_cursor.fetchall()
        objects = []
        for row in rows:
            obj = self._models[table_name](*row[1:])
            obj.id = row[0]
            objects.append(obj)
        return objects

    def exec_query(self, query: str) -> None:
        """Execute the query"""
        self._db_cursor.execute(query)
        self.dispatch_service.dispatch("QUERY_EXECUTED", query=query)
