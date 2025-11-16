from src.domain.url.URL import URL
from src.ports.ConnectionRepository import ConnectionRepository

class URLService:
    def __init__(self, connection: ConnectionRepository):
        self.connection_fetcher = connection

    def get(self, url_str: str):
        url = URL(url_str)
        return self.connection_fetcher.request(url)
