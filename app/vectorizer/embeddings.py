from .base import Vectorizer


class Embeddings(Vectorizer):
    def __init__(self, text):
        self.text = text
