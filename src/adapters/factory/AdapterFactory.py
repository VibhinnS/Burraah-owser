from src.domain.url.URL import URL
from src.domain.url.Scheme import Scheme
from src.adapters.repositories.HTTPSAdapter import HTTPSAdapter
from src.adapters.repositories.HTTPAdapter import HTTPAdapter
from src.adapters.repositories.FileAdapter import FileAdapter

class AdapterFactory:
    @staticmethod
    def get(url: URL):
        if url.scheme == Scheme.FILE.value:
            return FileAdapter()
        if url.scheme == Scheme.HTTP.value:
            return HTTPAdapter()
        if url.scheme == Scheme.HTTPS.value:
            return HTTPSAdapter()
        return HTTPAdapter()
