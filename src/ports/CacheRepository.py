from abc import ABC, abstractmethod
from typing import Generic, TypeVar

K = TypeVar("K")
V = TypeVar("V")

class CacheRepository(ABC, Generic[K, V]):
    @abstractmethod
    def acquire(self, key: K) -> V | None:
        pass

    @abstractmethod
    def release(self, key: K, value: V) -> None:
        pass
