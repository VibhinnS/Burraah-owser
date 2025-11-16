import socket
from collections import deque, defaultdict
from src.domain.url.URL import URL
from src.ports.CacheRepository import CacheRepository


class SocketCache(CacheRepository):
    def __init__(self):
        self.connection_pool: dict = defaultdict(deque)

    def acquire(self, item: URL):
        scheme = URL.scheme
        host = URL.host
        port = URL.port

        key = (scheme, host, port)

        if self.connection_pool[key]:
            return self.connection_pool[key].pop()
        return None

    def release(self, item: URL, sock: socket.socket):
        scheme = URL.scheme
        host = URL.host
        port = URL.port

        key = (scheme, host, port)

        self.connection_pool[key].append(sock)
