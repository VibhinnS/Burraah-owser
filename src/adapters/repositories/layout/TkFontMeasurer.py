import tkinter.font

from src.domain.layout.TextStyle import TextStyle
from src.ports.repositories.layout.LayoutRepository import TextMeasurer

class TkTextMeasurer(TextMeasurer):
    def __init__(self):
        self.cache = {}

    def measure(self, word: str, style: TextStyle) -> int:
        key = (style.size, style.weight, style.slant)
        if key not in self.cache:
            self.cache[key] = tkinter.font.Font(size=style.size, weight=style.weight, slant=style.slant)
        return self.cache[key].measure(word)

    def get_font(self, style) -> tkinter.font.Font:
        key = (style.size, style.weight, style.slant)
        if key not in self.cache:
            self.cache[key] = tkinter.font.Font(size=style.size, weight=style.weight, slant=style.slant)
        return self.cache[key]
