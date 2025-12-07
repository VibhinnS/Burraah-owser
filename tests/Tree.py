from src.adapters.parser.HTMLParser import HTMLParser, print_tree
from src.services.RequestService import RequestService
from src.adapters.parser.URLParser import URLParser

service = RequestService()
parser = HTMLParser()
url_parser = URLParser()

url = url_parser.parse("http://www.example.org")
body = service.fetch(url)
nodes = parser.extract(body)
print_tree(nodes)
