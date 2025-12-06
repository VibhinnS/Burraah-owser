import tkinter
import tkinter.font
from typing import Literal

from src.domain.html.Text import Text
from src.domain.html.Tag import Tag

class Layout:
    def __init__(self, tokens):
        self.HSTEP = 13
        self.VSTEP = 18
        self.SCROLLSTEP = 100
        self.WIDTH = 800
        self.HEIGHT = 600
        self.display_list: list = []
        self.line: list = []
        self.cursor_x = 13
        self.cursor_y = 18
        self.size: int = 12
        self.weight: Literal["normal","bold"] = "normal"
        self.style: Literal["roman","italic"] = "roman"
        print("Tokens received from parser - ", tokens)
        for token in tokens:
            self.token(token)
        self.flush()

    def token(self, token):
        if isinstance(token, Text):
            self.handle_text(token)
        if isinstance(token, Tag):
            self.handle_tags(token)


    def handle_text(self, token : Text):
        font = tkinter.font.Font(
            size=self.size,
            weight=self.weight,
            slant=self.style
        )
        for word in token.text.split():
            word_width = font.measure(word)
            if self.cursor_x + word_width > self.WIDTH - self.HSTEP:
                self.flush()
                self.cursor_y += font.metrics("linespace") * 1.25
                self.cursor_x = self.HSTEP
            self.line.append((self.cursor_x, word, font))
            self.cursor_x += word_width + font.measure(" ")

    def handle_tags(self, token: Tag):
        if token.tag == "i":
            self.style = "italic"
        elif token.tag == "/i":
            self.style = "roman"
        elif token.tag == "b":
            self.weight = "bold"
        elif token.tag == "/b":
            self.weight = "normal"
        elif token.tag == "small":
            self.size -= 2
        elif token.tag == "/small":
            self.size += 2
        elif token.tag == "big":
            self.size += 4
        elif token.tag == "/big":
            self.size -= 4
        elif token.tag == "br":
            self.flush()
        elif token.tag == "/p":
            self.flush()
            self.cursor_y += self.VSTEP

    def flush(self):
        if not self.line: return
        metrics = [font.metrics() for x,word,font in self.line]
        max_ascent = max([metric["ascent"] for metric in metrics])
        baseline = self.cursor_y + 1.25 * max_ascent
        for x, word, font in self.line:
            y = baseline - font.metrics("ascent")
            self.display_list.append((x,y,word,font))

        max_descent = max(metric["descent"] for metric in metrics)
        self.cursor_y = baseline + 1.25 * max_descent
        self.cursor_x = self.HSTEP
        self.line = []