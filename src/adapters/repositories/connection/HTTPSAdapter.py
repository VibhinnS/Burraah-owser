import json
import socket
import ssl
from src.ports.ConnectionRepository import ConnectionRepository
from src.domain.url.URL import URL
from src.domain.url.Request import Request
from src.adapters.parser.URLParser import URLParser

class HTTPSAdapter(ConnectionRepository):
    def request(self, url: URL):
        socket_connection = socket.socket(family=socket.AF_INET,
                                          type=socket.SOCK_STREAM,
                                          proto=socket.IPPROTO_TCP)
        socket_connection.connect((url.host, url.port))
        ctx = ssl.create_default_context()
        socket_connection = ctx.wrap_socket(socket_connection, server_hostname=url.host)

        request = (
            f"{Request.GET.value} {url.path} HTTP/1.1\r\n"
            f"{Request.HOST.value}: {url.host}\r\n"
            f"{Request.CONNECTION.value}: Close\r\n"
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
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        response_headers["status"] = status
        print(json.dumps(response_headers, indent=2))

        content = response.read()
        socket_connection.close()
        return status, content, response_headers

