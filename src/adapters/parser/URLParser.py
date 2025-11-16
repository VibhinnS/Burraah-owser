from src.domain.url.URL import URL
from src.domain.url.Scheme import Scheme

class URLParser:
    @staticmethod
    def parse(raw: str) -> URL:
        scheme_str, remainder = raw.split("://", 1)
        scheme = scheme_str.upper()

        if scheme == Scheme.FILE.value:
            return URL(
                scheme=scheme,
                file_path=remainder
            )

        port = 80 if scheme == Scheme.HTTP.value else 443

        if "/" not in remainder:
            remainder += "/"

        host, path = remainder.split("/", 1)

        if ":" in host:
            host, port_str = host.split(":", 1)
            port = int(port_str)

        return URL(
            scheme=scheme,
            host=host,
            port=port,
            path="/" + path
        )