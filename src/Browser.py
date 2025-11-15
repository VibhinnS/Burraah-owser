import tkinter
from src.URL import URL
from src.HTMLExtractor import HTMLExtractor

class Browser:
    def __init__(self):
        self.HSTEP = 13
        self.VSTEP = 18
        self.SCROLLSTEP = 100
        self.width = 800
        self.height = 600
        self.extractor = HTMLExtractor()
        self.main_window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.main_window,
            width=self.width,
            height=self.height
        )
        self.main_window.bind("<Down>", self.scrolldown)
        self.main_window.focus_set()
        self.canvas.pack()
        self.display_list: list = []
        self.scroll = 0

    def load(self, url: URL) -> None:
        body = url.request()
        raw_content = self.extractor.extract(body)
        self.layout(raw_content)
        self.draw()

    def layout(self, raw_content: str):
        cursor_x, cursor_y = self.HSTEP, self.VSTEP
        for character in raw_content:
            if cursor_x >= self.width:
                cursor_y += self.VSTEP
                cursor_x = self.HSTEP
            self.display_list.append((cursor_x, cursor_y, character))
            cursor_x += self.HSTEP

    def draw(self):
        self.canvas.delete("all")
        for x_coord, y_coord, character in self.display_list:
            if y_coord > self.scroll + self.height: continue
            if y_coord + self.VSTEP < self.scroll: continue
            self.canvas.create_text(x_coord, y_coord - self.scroll, text=character)

    def scrolldown(self, e):
        self.scroll += self.SCROLLSTEP
        self.draw()