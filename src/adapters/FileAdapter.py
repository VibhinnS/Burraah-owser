import os
from src.domain.url.URL import URL
from src.ports.ConnectionRepository import ConnectionRepository

class FileAdapter(ConnectionRepository):
    def request(self, url: URL):
        absolute_path = os.path.abspath()
        if not os.path.exists(url.file_path):
            return "No file found"

        if os.path.isdir(absolute_path):
            return "Cannot read directory"

        with open(absolute_path, 'r') as input_file:
            return input_file.readlines()
