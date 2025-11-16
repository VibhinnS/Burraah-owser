from dataclasses import dataclass
from typing import Optional

@dataclass
class URL:
    scheme: str
    host: Optional[str] = None
    port: Optional[int] = None
    path: Optional[str] = None
    file_path: Optional[str] = None
