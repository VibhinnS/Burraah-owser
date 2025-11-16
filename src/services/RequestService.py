from src.adapters.factory.AdapterFactory import AdapterFactory
from src.domain.url.URL import URL
from src.adapters.parser.URLParser import URLParser

class RequestService:
    MAX_REDIRECTS: int = 10

    def fetch(self, url: URL):
        adapter = AdapterFactory.get(url)

        for _ in range(self.MAX_REDIRECTS):
            status, content, headers = adapter.request(url)

            if status.startswith("3") and "location" in headers:
                redirect_url = headers["location"]
                url = URLParser.parse(redirect_url)
                adapter = AdapterFactory.get(url)
                continue

            return content

        raise Exception("Too many redirects")
