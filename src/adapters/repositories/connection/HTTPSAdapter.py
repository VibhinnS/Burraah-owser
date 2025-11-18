import socket
import ssl

from src.adapters.repositories.connection.BaseAdapter import BaseConnectionAdapter
from src.domain.url.URL import URL

class HTTPSAdapter(BaseConnectionAdapter):
    def __init__(self):
        super().__init__()

    def get_socket_connection(self, url: URL):
        socket_connection = self.socket_cache.acquire(url)
        if not socket_connection:
            socket_connection = socket.socket(family=socket.AF_INET,
                              type=socket.SOCK_STREAM,
                              proto=socket.IPPROTO_TCP)

        socket_connection.connect((url.host, url.port))
        ctx = ssl.create_default_context()
        socket_connection = ctx.wrap_socket(socket_connection, server_hostname=url.host)

        return socket_connection