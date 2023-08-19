from .base import Database


class DiskDB(Database):
    def __init__(self, db_filename):
        self.db_filename = db_filename

    # TODO: Implement methods using disk-based storage
