from functools import wraps

from .utils import camel_to_snake


class Dependency:
    """ Dependency """
    def __init__(self, cls) -> None:
        self.cls = cls
        self.instance = None

    def get(self, *args, **kwargs) -> object:
        if not self.instance:
            self.instance = self.cls(*args, **kwargs)
        return self.instance
    
    def __str__(self):
        return f"Not resolved {self.cls.__name__}" if not self.instance else f"Resolved {self.cls.__name__}"
    
    def __repr__(self):
        return f"Not resolved {self.cls.__name__}" if not self.instance else f"Resolved {self.cls.__name__}"


class Injector:
    """ Injector """
    dependencies = {}

    @classmethod
    def register(cls, dependency: object) -> None:
        """ Register a dependency """
        cls.dependencies[dependency.__name__] = Dependency(dependency)

    @classmethod
    def resolve(cls, name, *args, **kwargs):
        """ Get the dependency """
        return cls.dependencies[name].get(*args, **kwargs)
    
    @classmethod
    def resolve_all(cls):
        """ Get the dependency """
        for dependency in cls.dependencies.values():
            dependency.get()
    

def declare(cls):
    """ Decorator to declare a dependency """
    Injector.register(cls)
    return cls


def inject(dependency: str):
    """ Decorator to inject a dependency (function, static method or class) """
    def decorator(obj):
        name = camel_to_snake(dependency)
        if isinstance(obj, type): # obj is a class
            setattr(obj, name, property(lambda self: Injector.resolve(dependency)))
            return obj
        else: # obj is a function
            @wraps(obj)
            def wrapper(*args, **kwargs):
                if not dependency in kwargs:
                    # object method
                    if args and hasattr(args[0], dependency):
                        kwargs[name] = getattr(args[0], dependency)
                    else:
                        # class method or normal function
                        kwargs[name] = Injector.resolve(dependency)
                return obj(*args, **kwargs)
            return wrapper
    return decorator
