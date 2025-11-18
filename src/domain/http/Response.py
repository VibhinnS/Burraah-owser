from dataclasses import dataclass
from typing import Optional

@dataclass
class Response:
    status: Optional[str] = None
    content: Optional[bytes] = None
    response_headers: Optional[dict] = None