import socket
from abc import ABC, abstractmethod
from src.domain.url.URL import URL

class CacheRepository(ABC):
    @abstractmethod
    def acquire(self, item: URL):
        pass

    @abstractmethod
    def release(self, item: URL, sock: socket.socket):
        pass

