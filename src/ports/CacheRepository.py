from abc import ABC, abstractmethod

class Cache(ABC):
    @abstractmethod
    def get(self, item):
        pass

    @abstractmethod
    def set(self, item):
        pass

