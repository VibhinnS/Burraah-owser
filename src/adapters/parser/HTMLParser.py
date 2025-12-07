from src.domain.html.Text import Text
from src.domain.html.Element import Element

class HTMLParser:
    def __init__(self):
        self.unfinished: list[Element] = []

    def extract(self, body: bytes):
        text: str = ""
        in_tag: bool = False

        for character in body.decode('utf-8'):
            if character == "<":
                in_tag = True
                if text: self.add_text(text)
                text = ""
            elif character == ">":
                in_tag = False
                self.add_tag(text)
                text = ""
            else:
                text += character
        if not in_tag and text:
            self.add_text(text)
        return self.finish()


    def add_text(self, text: str):
        if text.isspace(): return
        parent_node = self.unfinished[-1]
        child_node = Text(text, parent_node)
        parent_node.children.append(child_node)

    def add_tag(self, tag: str):
        if tag.startswith("!"): return
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            completed_node = self.unfinished.pop()
            parent_node = self.unfinished[-1]
            parent_node.children.append(completed_node)

        else:
            parent_node = self.unfinished[-1] if self.unfinished else None
            child_node = Element(tag, parent_node)
            self.unfinished.append(child_node)

    def finish(self):
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()


def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)