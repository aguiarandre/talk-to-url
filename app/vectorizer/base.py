from abc import ABC, abstractmethod


class Vectorizer(ABC):
    @abstractmethod
    def create_vector(self, text):
        "Generate vector of the given text"
        pass
