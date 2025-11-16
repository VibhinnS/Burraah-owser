class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split("://", 1)

        if self.scheme == "file":
            self.file_path = url
            return

        self.scheme = self.scheme.upper()
        if "/" not in url: url += "/"

        self.host, url = url.split("/", 1)
        if ":" in self.host:
            self.port = int(self.host.split(":", 1)[1])
        else:
            self.port = 80 if self.scheme == "HTTP" else 443
        self.path = "/" + url
