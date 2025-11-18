import os

from src.adapters.repositories.connection.BaseAdapter import BaseConnectionAdapter
from src.domain.url.URL import URL

class FileAdapter(BaseConnectionAdapter):
    def get_socket_connection(self, url: URL): pass

    def request(self, url: URL):
        absolute_path = os.path.abspath(url.file_path)
        if not os.path.exists(absolute_path):
            return "No file found"

        if os.path.isdir(absolute_path):
            return "Cannot read directory"

        with open(absolute_path, 'r') as input_file:
            return input_file.readlines()
