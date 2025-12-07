from dataclasses import dataclass, field
from typing import Optional

from src.domain.html.Node import Node

@dataclass
class Element(Node):
    tag: str
    parent: Optional["Element"]
    attributes: dict
    children: list[Node] = field(default_factory=list)

    def __repr__(self):
        return "<" + self.tag + ">"