from src.domain.html.Text import Text
from src.domain.html.Tag import Tag

class HTMLExtractor:
    def __init__(self): pass

    @staticmethod
    def extract(body):
        output: list[Text | Tag] = []
        buffer: str = ""
        in_tag: bool = False
        body = body.decode("utf-8")

        for character in body:
            if character == "<":
                in_tag = True
                if buffer: output.append(Text(buffer))
                buffer = ""
            elif character == ">":
                in_tag = False
                output.append(Tag(buffer))
                buffer = ""
            else:
                buffer += character
        if not in_tag and buffer:
            output.append(Text(buffer))
        return output
