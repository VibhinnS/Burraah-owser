class URL:
    def __init__(self, url: str):
        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https", "file"]

        if self.scheme in ["http", "https"]:
            self.port: int = 80 if self.scheme == "http" else 443

            if not "/" in url: url = url + "/"

            self.host, url = url.split("/", 1)
            if ":" in self.host:
                self.port = int(self.host.split(":", 1)[1])
            self.path = "/" + url
        else:
            self.file_path = url

obj = URL("file://D:/Alvin/Logs/")
print(obj.file_path)