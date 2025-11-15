from src.URL import URL

class HTMLRenderer:
    def __init__(self): pass

    @staticmethod
    def show(body):
        in_tag: bool = False
        for character in body:
            if character == "<": in_tag = True
            elif character == ">": in_tag = False
            elif not in_tag: print(character, end= "")

    def load(self, url: URL):
        body = url.request()
        self.show(body)