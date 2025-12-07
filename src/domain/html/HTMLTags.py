from src.domain.html.Node import Node

class HTMLTags(Node):
    SELF_CLOSING_TAGS: list[str] = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
    ]

    HEAD_TAGS: list[str] = [
        "base", "basefont", "bgsound", "noscript",
        "link", "meta", "title", "style", "script"
    ]