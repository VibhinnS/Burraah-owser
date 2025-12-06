import tkinter
import tkinter.font
from typing import Literal

from src.domain.http.URL import URL
from src.domain.layout.LayoutEngine import Layout
from src.adapters.parser.HTMLParser import HTMLParser
from src.services.RequestService import RequestService

class Browser:
    def __init__(self):
        self.HSTEP = 13
        self.VSTEP = 18
        self.SCROLLSTEP = 100
        self.WIDTH = 800
        self.HEIGHT = 600
        self.style: Literal["italic", "roman"] = "roman"
        self.weight: Literal["normal", "bold"] = "normal"
        self.size: int = 12
        self.parser = HTMLParser()
        self.main_window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.main_window,
            width=self.WIDTH,
            height=self.HEIGHT
        )
        self.main_window.bind("<Down>", self.scrolldown)
        self.main_window.focus_set()
        self.canvas.pack()
        self.display_list: list = []
        self.line: list = []
        self.scroll = 0
        self.request_service = RequestService()

    def load(self, url: URL) -> None:
        body = self.request_service.fetch(url)
        content_tokens = self.parser.extract(body)
        self.display_list = Layout(content_tokens).display_list
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x_coord, y_coord, character, font in self.display_list:
            if y_coord > self.scroll + self.HEIGHT: continue
            if y_coord + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x_coord, y_coord - self.scroll, text=character, font=font, anchor="nw")

    def scrolldown(self, e):
        self.scroll += self.SCROLLSTEP
        self.draw()