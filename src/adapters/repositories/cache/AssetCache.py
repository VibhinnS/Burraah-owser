import time
from typing import Optional

from src.domain.cache.Cache import Cache
from src.domain.http.URL import URL
from src.ports.repositories.cache.CacheRepository import CacheRepository

class AssetCache(CacheRepository):
    def __init__(self):
        self.cache: dict[str, Cache] = {}

    def acquire(self, url: URL) -> Optional[Cache]:
        entry = self.cache.get(url.path)
        if not entry: return None

        if entry.expiry < time.time():
            del self.cache[url.path]
            return None

        return entry

    def release(self, url: URL, entry: Cache) -> None:
        self.cache[url.path] = entry