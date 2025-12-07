import gzip
import socket
import time
from abc import abstractmethod
from typing import Optional

from lockpy import private

from src.domain.cache.Cache import Cache
from src.domain.http.URL import URL
from src.domain.http.Request import Request
from src.domain.http.Response import Response
from src.ports.repositories.connection.ConnectionRepository import ConnectionRepository
from src.adapters.repositories.cache.SocketCache import SocketCache
from src.adapters.repositories.cache.AssetCache import AssetCache

class BaseConnectionAdapter(ConnectionRepository):
    def __init__(self):
        self.socket_cache = SocketCache()
        self.asset_cache = AssetCache()

    @abstractmethod
    def get_socket_connection(self, url: URL):
        pass

    def request(self, url: URL) -> Response:
        cached_response = self.asset_cache.acquire(url)

        if cached_response:
            return Response(content=cached_response.content)

        socket_connection = self.get_socket_connection(url)
        return self.send_request(url, socket_connection)

    @private
    def send_request(self, url: URL, socket_connection: socket.socket):
        request_object = Request(
            method="GET",
            path=url.path
        )

        request_object.set_header("Host", url.host)
        request_object.set_header("Connection", "Keep-alive")
        request_object.set_header("Accept-Encoding", "gzip")

        request = request_object.get_encoded_header()
        socket_connection.send(request)
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

        content_length_str: str = response_headers.get("content-length","")
        if not content_length_str:
            content_length: int = 0
        else:
            content_length: int = int(content_length_str)
        content = response.read(content_length)
        if response_headers.get("content-encoding","") == "gzip":
            content = gzip.decompress(content)
        if response_headers.get("connection") == "keep-alive":
            self.socket_cache.release(url, socket_connection)

        output =  Response(
            status=status,
            content=content,
            response_headers=response_headers
        )

        if self.is_cacheable(output):
            cache_entry = self.generate_cache_entry(output)
            self.asset_cache.release(url, cache_entry)

        return output

    @private
    def is_cacheable(self, response: Response) -> bool:
        cache_control: str = response.response_headers.get("cache-control", "")
        if cache_control.startswith("max-age"): return True
        return False

    @private
    def generate_cache_entry(self, response: Response) -> Optional[Cache]:
        cache_control: str = response.response_headers.get("cache-control")
        try:
            _, value = cache_control.split("max-age=")
            max_age = int(value.split(",")[0])
        except Exception:
            return None

        cache_expiry = time.time() + max_age

        return Cache(
            content=response.content,
            headers=response.response_headers,
            expiry=cache_expiry
        )
