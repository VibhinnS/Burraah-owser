import sys
from src.URL import URL
from src.HTMLRenderer import HTMLRenderer

renderer = HTMLRenderer()

if __name__ == "__main__":
    renderer.load(URL(sys.argv[1]))