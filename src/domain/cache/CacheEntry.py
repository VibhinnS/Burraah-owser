from dataclasses import dataclass

@dataclass
class CacheEntry:
    content: bytes
    headers: dict
    expiry: float