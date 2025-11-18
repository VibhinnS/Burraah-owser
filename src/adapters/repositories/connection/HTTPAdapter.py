import socket

from src.adapters.repositories.connection.BaseAdapter import BaseConnectionAdapter
from src.domain.url.URL import URL

class HTTPAdapter(BaseConnectionAdapter):
    def __init__(self):
        super().__init__()

    def get_socket_connection(self, url: URL):
        socket_connection = self.socket_cache.acquire(url)
        if not socket_connection:
            socket_connection = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP
            )
        socket_connection.connect((url.host, url.port))
        return socket_connection
