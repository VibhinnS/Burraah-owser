from dataclasses import dataclass, field

from src.domain.html.Element import Element
from src.domain.html.Node import Node

@dataclass
class Text(Node):
    text: str
    parent: Element
    children: list[Node] = field(default_factory=list)

    def __repr__(self):
        return repr(self.text)
