from src.domain.html.HTMLTags import HTMLTags
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
        self.implicit_tags(None)
        parent_node = self.unfinished[-1]
        child_node = Text(text, parent_node)
        parent_node.children.append(child_node)

    def add_tag(self, tag: str):
        tag, attributes = self.get_attributes(tag)

        if tag.startswith("!"): return
        self.implicit_tags(tag)
        if tag.startswith("/"):
            if len(self.unfinished) == 1: return
            completed_node = self.unfinished.pop()
            parent_node = self.unfinished[-1]
            parent_node.children.append(completed_node)

        elif tag in HTMLTags.SELF_CLOSING_TAGS:
            parent_node = self.unfinished[-1]
            child_node = Element(tag, parent_node, attributes)
            parent_node.children.append(child_node)

        else:
            parent_node = self.unfinished[-1] if self.unfinished else None
            child_node = Element(tag, parent_node, attributes)
            self.unfinished.append(child_node)

    def finish(self):
        if not self.unfinished:
            self.implicit_tags(None)
        while len(self.unfinished) > 1:
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        return self.unfinished.pop()

    def get_attributes(self, text: str):
        parts = text.split()
        tag = parts[0].casefold()
        attributes = {}

        for attribute_pair in parts[1:]:
            if "=" in attribute_pair:
                key,value = attribute_pair.split("=", 1)
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]
                attributes[key.casefold()] = value
            else:
                attributes[attribute_pair.casefold()] = ""

        return tag, attributes

    def implicit_tags(self, tag):
        while True:
            open_tags = [node.tag for node in self.unfinished]
            if not open_tags and tag != "html":
                self.add_tag("html")
            elif open_tags == ["html"] and tag not in ["head", "body", "/html"]:
                if tag in HTMLTags.HEAD_TAGS:
                    self.add_tag("head")
                else:
                    self.add_tag("body")
            elif open_tags == ["html", "head"] and tag not in ["/head"] + HTMLTags.HEAD_TAGS:
                self.add_tag("/head")
            else:
                break

def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)