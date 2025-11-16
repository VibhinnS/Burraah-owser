class URL:
    def __init__(self, scheme, host=None, port=None, path=None, file_path=None):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.path = path
        self.file_path = file_path
