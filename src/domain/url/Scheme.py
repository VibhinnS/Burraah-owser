from enum import Enum

class Scheme(Enum):
    HTTP = "HTTP/1.0"
    HTTP_1 = "HTTP/1.1"
    HTTPS = "HTTPS"
    FILE = "FILE"