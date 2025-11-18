from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Request:
    method: str = "GET"
    path: str = "/"
    http_version: str = "HTTP/1.1"
    headers: Dict[str, str] = field(default_factory=dict)

    def set_header(self, key: str, value: str):
        self.headers[key] = value

    def get_encoded_header(self, encoding_type: str = "utf-8") -> bytes:
        request_line = f"{self.method} {self.path} {self.http_version}\r\n"
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        end_headers = "\r\n"

        return (request_line + header_lines + end_headers).encode(encoding_type)
