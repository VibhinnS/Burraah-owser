import socket
from abc import abstractmethod

from lockpy import private

from src.domain.url.URL import URL
from src.domain.url.Request import Request
from src.ports.ConnectionRepository import ConnectionRepository
from src.adapters.repositories.cache.SocketCache import SocketCache

class BaseConnectionAdapter(ConnectionRepository):
    def __init__(self):
        self.socket_cache = SocketCache()

    @abstractmethod
    def get_socket_connection(self, url: URL):
        pass

    def request(self, url: URL) -> tuple[bytes, bytes, dict]:
        socket_connection = self.get_socket_connection(url)
        return self.send_request(url, socket_connection)


    @private
    def send_request(self, url: URL, socket_connection: socket.socket):
        request = (
            f"{Request.GET.value} {url.path} HTTP/1.1\r\n"
            f"{Request.HOST.value}: {url.host}\r\n"
            f"{Request.CONNECTION.value}: Keep-alive\r\n"
            "\r\n"
        )

        socket_connection.send(request.encode("utf8"))
        response = socket_connection.makefile("rb", newline="\r\n")
        status_line = self.readline_as_string(response)
        version, status, explanation = status_line.split(" ", 2)
        response_headers = {}

        while True:
            line = self.readline_as_string(response)
            if line == "": break
            if line:
                header, value = line.split(":", 1)
                response_headers[header.casefold()] = value.strip()

        content_length: int = int(response_headers.get("content-length"))
        content = response.read(content_length)
        self.socket_cache.release(url, socket_connection)
        return status, content, response_headers
