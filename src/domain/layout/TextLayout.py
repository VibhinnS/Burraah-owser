from dataclasses import dataclass

@dataclass
class TextLayout:
    x: int
    y: int
    text: str
    style: str
