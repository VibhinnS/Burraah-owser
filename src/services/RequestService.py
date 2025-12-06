from src.adapters.factory.http.ConnectionFactory import ConnectionFactory
from src.domain.http.Response import Response
from src.domain.http.URL import URL
from src.adapters.parser.URLParser import URLParser

class RequestService:
    MAX_REDIRECTS: int = 10

    def __init__(self):
        self.response: Response = Response()

    def fetch(self, url: URL):
        adapter = ConnectionFactory.get(url)

        for _ in range(self.MAX_REDIRECTS):
            self.response = adapter.request(url)

            if self.response.status.startswith("3") and "location" in self.response.headers:
                redirect_url = self.response.headers["location"]
                url = URLParser.parse(redirect_url)
                adapter = ConnectionFactory.get(url)
                continue

            return self.response.content

        raise Exception("Too many redirects")
