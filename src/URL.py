import os
import ssl
import socket

class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https", "file"]

        if self.scheme in ["http", "https"]:
            self.port: int = 80 if self.scheme == "http" else 443

            if not "/" in url: url = url + "/"

            self.host, url = url.split("/", 1)
            if ":" in self.host:
                self.port = int(self.host.split(":", 1)[1])
            self.path = "/" + url
        else:
            self.file_path = url

    def request(self):
        if self.scheme == "file":
            absolute_path = os.path.abspath(self.file_path)
            if not os.path.exists(absolute_path):
                return "No file found"
            if os.path.isdir(absolute_path):
                return "Cannot read directory"
            with open(absolute_path, 'r') as input_file:
                return input_file.readlines()

        socket_connection = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_IP
        )
        socket_connection.connect((self.host, self.port))

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            socket_connection = ctx.wrap_socket(socket_connection, server_hostname=self.host)

        request = (
            f"GET {self.path} HTTP/1.0\r\n"
            f"Host: {self.host}\r\n"
            "Connection: Close\r\n"
            "\r\n"
        )

        socket_connection.send(request.encode("utf8"))
        response = socket_connection.makefile("r", encoding="utf8", newline="\r\n")
        status_line = response.readline()
        version, status, explanation = status_line.split(" ", 2)

        response_headers = {}

        while True:
            line = response.readline()
            if line == "\r\n":
                break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        content = response.read()

        socket_connection.close()
        return content
