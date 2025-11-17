from src.domain.url.URL import URL
from src.domain.url.Scheme import Scheme
from src.adapters.repositories.connection.HTTPSAdapter import HTTPSAdapter
from src.adapters.repositories.connection.HTTPAdapter import HTTPAdapter
from src.adapters.repositories.connection.FileAdapter import FileAdapter

class ConnectionFactory:
    @staticmethod
    def get(url: URL):
        if url.scheme == Scheme.FILE.value:
            return FileAdapter()
        if url.scheme == Scheme.HTTP.value:
            return HTTPAdapter()
        if url.scheme == Scheme.HTTPS.value:
            return HTTPSAdapter()
        return HTTPAdapter()
