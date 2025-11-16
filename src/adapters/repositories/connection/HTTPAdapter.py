import socket

from src.adapters.repositories.cache.SocketCache import SocketCache
from src.ports.ConnectionRepository import ConnectionRepository
from src.domain.url.URL import URL
from src.domain.url.Request import Request

class HTTPAdapter(ConnectionRepository):
    def __init__(self):
        self.socket_cache = SocketCache()

    def request(self, url: URL):
        persisted_connection = self.socket_cache.acquire(url)

        if not persisted_connection:
            socket_connection = socket.socket(family=socket.AF_INET,
                              type=socket.SOCK_STREAM,
                              proto=socket.IPPROTO_TCP)
        else:
            socket_connection = persisted_connection

        socket_connection.connect((url.host, url.port))

        request = (
            f"{Request.GET.value} {url.path} HTTP/1.1\r\n"
            f"{Request.HOST.value}: {url.host}\r\n"
            f"{Request.CONNECTION.value}: Keep-alive\r\n"
            "\r\n"
        )

        socket_connection.send(request.encode("utf8"))
        response = socket_connection.makefile("r", encoding="utf8", newline="\r\n")
        status_line = response.readline()
        version, status, explanation = status_line.split(" ", 2)
        response_headers = {}

        while True:
            line = response.readline()
            if line == "\r\n": break
            if line:
                header, value = line.split(":", 1)
                response_headers[header.casefold()] = value.strip()

        self.socket_cache.release(url, socket_connection)
        content = response.read()
        socket_connection.close()
        return status, content, response_headers
