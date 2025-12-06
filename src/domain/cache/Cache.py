from dataclasses import dataclass

@dataclass
class Cache:
    content: bytes
    headers: dict
    expiry: float