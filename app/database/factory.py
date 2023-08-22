from .in_memory import InMemoryDB
from .disk import DiskDB
from .datastore import DatastoreDB
from enum import Enum


class DatabaseType(Enum):
    IN_MEMORY = "in_memory"
    DISK = "disk"
    DATASTORE = "google_datastore"


class DatabaseFactory:
    @staticmethod
    def create_database(database_type: DatabaseType, *args, **kwargs):
        if database_type == DatabaseType.IN_MEMORY:
            return InMemoryDB(*args, **kwargs)
        elif database_type == DatabaseType.DISK:
            return DiskDB(*args, **kwargs)
        elif database_type == DatabaseType.DATASTORE:
            return DatastoreDB(*args, **kwargs)
        else:
            raise NotImplementedError("This DB is not implemented.")
