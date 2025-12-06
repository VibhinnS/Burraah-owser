from abc import ABC, abstractmethod
from io import BufferedReader

from src.domain.http.URL import URL

class ConnectionRepository(ABC):
    @abstractmethod
    def request(self, url: URL) -> tuple[str, str, dict]:
        pass

    @staticmethod
    def readline_as_string(response: BufferedReader):
        return response.readline().decode("utf-8").strip()
