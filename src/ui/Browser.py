import tkinter
from src.domain.http.URL import URL
from src.domain.html.Text import Text
from src.domain.html.Tag import Tag
from src.adapters.parser.HTMLParser import HTMLExtractor
from src.services.RequestService import RequestService

class Browser:
    def __init__(self):
        self.HSTEP = 13
        self.VSTEP = 18
        self.SCROLLSTEP = 100
        self.WIDTH = 800
        self.HEIGHT = 600
        self.extractor = HTMLExtractor()
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
        self.scroll = 0
        self.request_service = RequestService()

    def load(self, url: URL) -> None:
        body = self.request_service.fetch(url)
        content_tokens = self.extractor.extract(body)
        self.layout(content_tokens)
        self.draw()

    def layout(self, content_tokens: list):
        font = tkinter.font.Font()
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for token in content_tokens:
            if isinstance(token, Text):
                for word in token.text.split():
                    word_width = font.measure(word)
                    if cursor_x + word_width > self.WIDTH - self.HSTEP:
                        cursor_y += font.metrics("linespace") * 1.25
                        cursor_x = self.HSTEP
            self.display_list.append((cursor_x, cursor_y, word))
            cursor_x += word_width + font.measure(" ")
        return self.display_list

    def draw(self):
        self.canvas.delete("all")
        for x_coord, y_coord, character in self.display_list:
            if y_coord > self.scroll + self.HEIGHT: continue
            if y_coord + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x_coord, y_coord - self.scroll, text=character)

    def scrolldown(self, e):
        self.scroll += self.SCROLLSTEP
        self.draw()