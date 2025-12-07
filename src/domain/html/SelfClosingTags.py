from src.domain.html.Node import Node

class SelfClosingTags(Node):
    SELF_CLOSING_TAGS :list[str] = [
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]