from .base import Database
from google.cloud import datastore

class DatastoreDB(Database):
    """
    This implements a connection to Google Datastore.
    """
    def __init__(self, kind: str):
        self.client = datastore.Client()
        # Entity kind
        self.kind = kind

    def add_url(self, url, content):
        item = datastore.Entity(client.key(self.kind))
        item.update({url: content})

        # Save the entity to Datastore
        client.put(item)

    # TODO: implement other methods
