class HTMLExtractor:
    def __init__(self): pass

    @staticmethod
    def extract(body):
        text: str = ""
        in_tag: bool = False
        for character in body:
            if character == "<": in_tag = True
            elif character == ">": in_tag = False
            elif not in_tag: text += character
        return text
