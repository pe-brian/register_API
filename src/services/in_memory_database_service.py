from chocolatine import Condition

from src.base_model import BaseModel
from src.service import Service


class InMemoryDatabaseService(Service):
    """In memory Database service"""

    def __init__(self) -> None:
        super().__init__()
        self._models = {}
        self._objects = {}
        self._id_counters = {}

    def close(self):
        """Close the service properly"""
        pass

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
        del self._models[table_name]
        del self._objects[table_name]
        del self._id_counters[table_name]

    def create_table(self, table_name: str) -> None:
        """Create the table according to the registered models"""
        self._objects[table_name] = []
        self._id_counters[table_name] = 0

    def create_tables(self, drop_old: bool = False) -> None:
        """Create the tables according to the registered models"""
        if drop_old:
            self.drop_tables()
        for model in self._models:
            self.create_table(model)

    def update_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Update the object and return it"""
        obj = self.get_object_by_id(table_name, kwargs["id"])
        for key, value in kwargs.items():
            setattr(obj, key, value)
        return obj

    def create_or_update_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Update the object in db if the object doesn't exit, otherwise create it and return it"""
        if "id" in kwargs and kwargs["id"] != None:
            return self.update_object(table_name, *args, **kwargs)
        return self.create_object(table_name, *args, **kwargs)

    def create_object(self, table_name: str, *args, **kwargs) -> BaseModel:
        """Create the object and return it"""
        model = self._models[table_name]
        if "id" in kwargs:
            del kwargs["id"]
        obj = model(*args, **kwargs)
        self._objects[table_name].append(obj)
        self._id_counters[table_name] += 1
        obj.id = self._id_counters[table_name]
        return obj

    def delete_object_by_id(self, table_name: str, id: int) -> None:
        """Delete the object by id"""
        self.get_object_by_id(table_name, id)
        self._objects[table_name] = filter(
            lambda row: row.id != id, self._objects[table_name]
        )

    def get_object_by_id(self, table_name: str, id: int) -> object:
        """Get object by id"""
        for row in self._objects[table_name]:
            if row.id == id:
                return row
        raise IndexError(f"Object in table {table_name} with id {id} not found")

    def filter_objects(self, table_name: str, condition: Condition) -> object:
        """Filter objects by condition"""
        res = []
        if condition.op == "=":
            key = condition.left_val._name
            value = condition.right_val
            if isinstance(value, str):
                value = value.strip("'")
            for obj in self._objects[table_name]:
                if getattr(obj, key) == value:
                    res.append(obj)
        return res
