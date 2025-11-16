from abc import ABC, abstractmethod
from src.domain.url.URL import URL

class ConnectionRepository(ABC):
    @abstractmethod
    def request(self, url: URL) -> tuple[str, str, dict]:
        pass
