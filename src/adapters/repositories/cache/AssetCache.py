import time
from typing import Optional

from src.domain.cache.CacheEntry import CacheEntry
from src.domain.http.URL import URL
from src.ports.CacheRepository import CacheRepository

class AssetCache(CacheRepository):
    def __init__(self):
        self.cache: dict[str, CacheEntry] = {}

    def acquire(self, url: URL) -> Optional[CacheEntry]:
        entry = self.cache.get(url.path)
        if not entry: return None

        if entry.expiry < time.time():
            del self.cache[url.path]
            return None

        return entry

    def release(self, url: URL, entry: CacheEntry) -> None:
        self.cache[url.path] = entry